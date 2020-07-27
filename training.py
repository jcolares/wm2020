
# Adapted from:
# https://medium.com/analytics-vidhya/pytorch-implementation-of-semantic-segmentation-for-single-class-from-scratch-81f96643c98c

import cv2
from torch.optim.lr_scheduler import ReduceLROnPlateau
import torch
import torch.optim as optim
import torch.backends.cudnn as cudnn
import segmentation_models_pytorch as smp
import time
from dataloaders import PersonDataloader
from scoring import Scores
from scoring import epoch_log


class Trainer(object):
    def __init__(self, model, df, img_dir, mask_dir, mean, std):
        self.df = df
        self.img_dir = img_dir
        self.mask_dir = mask_dir
        self.mean = mean
        self.std = std
        self.num_workers = 4
        self.batch_size = {'train': 1, 'val': 1}
        self.accumulation_steps = 4//self.batch_size['train']
        self.lr = 5e-4
        self.num_epochs = 10
        self.phases = ['train', 'val']
        self.best_loss = float('inf')
        self.device = torch.device("cuda:0")
        torch.set_default_tensor_type("torch.cuda.FloatTensor")
        self.net = model.to(self.device)
        cudnn.benchmark = True
        self.criterion = torch.nn.BCEWithLogitsLoss()
        self.optimizer = optim.Adam(self.net.parameters(), lr=self.lr)
        self.scheduler = ReduceLROnPlateau(
            self.optimizer, mode='min', patience=3, verbose=True)
        self.dataloaders = {phase: PersonDataloader(df, img_dir,
                                                    mask_dir, mean, std,
                                                    phase=phase, batch_size=self.batch_size[phase],
                                                    num_workers=self.num_workers) for phase in self.phases}

        self.losses = {phase: [] for phase in self.phases}
        self.dice_score = {phase: [] for phase in self.phases}

    def forward(self, inp_images, tar_mask):
        inp_images = inp_images.to(self.device)
        tar_mask = tar_mask.to(self.device)
        pred_mask = self.net(inp_images)
        loss = self.criterion(pred_mask, tar_mask)
        return loss, pred_mask

    def iterate(self, epoch, phase):
        measure = Scores(phase, epoch)
        start = time.strftime("%H:%M:%S")
        print(f"Starting epoch: {epoch} | phase:{phase} | 🙊':{start}")
        batch_size = self.batch_size[phase]
        self.net.train(phase == "train")
        dataloader = self.dataloaders[phase]
        running_loss = 0.0
        total_batches = len(dataloader)
        self.optimizer.zero_grad()
        for itr, batch in enumerate(dataloader):
            images, mask_target = batch
            loss, pred_mask = self.forward(images, mask_target)
            loss = loss/self.accumulation_steps
            if phase == 'train':
                loss.backward()
                if (itr+1) % self.accumulation_steps == 0:
                    self.optimizer.step()
                    self.optimizer.zero_grad()
            running_loss += loss.item()
            pred_mask = pred_mask.detach().cpu()
            measure.update(mask_target, pred_mask)
        epoch_loss = (running_loss*self.accumulation_steps)/total_batches
        dice = epoch_log(epoch_loss, measure)
        self.losses[phase].append(epoch_loss)
        self.dice_score[phase].append(dice)
        torch.cuda.empty_cache()
        return epoch_loss

    def start(self):
        for epoch in range(self.num_epochs):
            self.iterate(epoch, "train")
            state = {
                "epoch": epoch,
                "best_loss": self.best_loss,
                "state_dict": self.net.state_dict(),
                "optimizer": self.optimizer.state_dict(),
            }
            with torch.no_grad():
                val_loss = self.iterate(epoch, "val")
                self.scheduler.step(val_loss)
            if val_loss < self.best_loss:
                print("******** New optimal found, saving state ********")
                state["best_loss"] = self.best_loss = val_loss
                torch.save(state, "./model_office.pth")
            print()
