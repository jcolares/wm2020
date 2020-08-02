
import torch
from dataloaders import PersonDataloader
import segmentation_models_pytorch as smp
from matplotlib import pyplot as plt
from tqdm import tqdm_notebook as tqdm
import numpy as np
from preprocessing import list_files
import time
import cv2 as cv
from torchvision import transforms
from PIL import Image
from utils import getArgs

# load variables from file
args = getArgs('segmentation/args.yaml')
img_dir = args['img_dir']
mask_dir = args['mask_dir']
mean = args['mean']
std = args['std']
ckpt_path = args['ckpt_path']
df = list_files(img_dir)
dataloader = PersonDataloader(df, img_dir, mask_dir, mean, std, 'val', 1, 4)

device = torch.device("cuda")
model = smp.Unet("resnet18", encoder_weights="imagenet",
                 classes=1, activation=None)
model.to(device)
model.eval()
state = torch.load(ckpt_path, map_location=lambda storage, loc: storage)
model.load_state_dict(state["state_dict"])

inv_normalize = transforms.Normalize(
    mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
    std=[1/0.229, 1/0.224, 1/0.225]
)

'''
z = x * torch.tensor(std).view(3, 1, 1)
z = z + torch.tensor(mean).view(3, 1, 1)
'''

for itr, batch in enumerate(dataloader):
    image, mask = batch
    orig_img = np.squeeze(image)
    orig_img = inv_normalize(orig_img)
    image = torch.sigmoid(model(image.to(device)))
    image = image.detach().cpu().numpy()
    image = np.squeeze(image)
    image = image.round()
    image = image * 255
    a = Image.fromarray(image)
    mask = np.squeeze(mask)
    b = transforms.ToPILImage()(mask)
    c = transforms.ToPILImage(mode='RGB')(orig_img)
    f = plt.figure()
    f.suptitle('predicted_mask // original_mask // original image')
    f.add_subplot(1, 3, 1)
    plt.imshow(a)
    f.add_subplot(1, 3, 2)
    plt.imshow(b)
    f.add_subplot(1, 3, 3)
    plt.imshow(c)
    plt.show(block=True)
