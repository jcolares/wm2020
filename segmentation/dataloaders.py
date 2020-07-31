# Adapted from:
# https://medium.com/analytics-vidhya/pytorch-implementation-of-semantic-segmentation-for-single-class-from-scratch-81f96643c98c

import cv2
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset, sampler
from sklearn.model_selection import train_test_split
from albumentations import (
    HorizontalFlip, ShiftScaleRotate, Normalize, Resize, Compose, GaussNoise)
from albumentations.pytorch import ToTensor
import os
import random


def get_transform(phase, mean, std):
    list_trans = []
    if phase == 'train':
        list_trans.extend([HorizontalFlip(p=0.5)])
    # normalizing the data & then converting to tensors
    list_trans.extend([Normalize(mean=mean, std=std, p=1), ToTensor()])
    list_trans = Compose(list_trans)
    return list_trans


class PersonDataset(Dataset):
    def __init__(self, df, img_dir, mask_dir, mean, std, phase):
        self.fname = df
        self.img_dir = img_dir
        self.mask_dir = mask_dir
        self.mean = mean
        self.std = std
        self.phase = phase
        self.trasnform = get_transform(phase, mean, std)

    def __getitem__(self, idx):
        name = self.fname[idx]
        img_name_path = os.path.join(self.img_dir, name)
        mask_name_path = img_name_path.replace('_img', '_mask')
        img = cv2.imread(img_name_path)
        mask = cv2.imread(mask_name_path, cv2.IMREAD_UNCHANGED)
        augmentation = self.trasnform(image=img, mask=mask)
        img_aug = augmentation['image']  # [3,128,128] type:Tensor
        mask_aug = augmentation['mask']  # [1,128,128] type:Tensor
        return img_aug, mask_aug

    def __len__(self):
        return len(self.fname)


def PersonDataloader(df, img_dir, mask_dir, mean, std, phase, batch_size, num_workers):
    df_train, df_valid = train_test_split(df, test_size=0.2, random_state=69)
    df = df_train if phase == 'train' else df_valid
    for_loader = PersonDataset(df, img_dir, mask_dir, mean, std, phase)
    dataloader = DataLoader(for_loader, batch_size=batch_size,
                            num_workers=num_workers, pin_memory=True)
    return dataloader
