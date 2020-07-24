#from preprocessing import json_2_bitmap, resize_320x240, list_files, preprocess_file
from preprocessing import *
import cv2
from pathlib import Path
import os
import concurrent.futures


# Parametros
dataset_dir = '/home/jeff/datasets/Supervisely Person Dataset/ds13'
work_dir = '/home/jeff/datasets/SPD'

# Criar diretorios de trabalho
base_path = Path(work_dir)
base_path.mkdir(exist_ok=True)
(base_path/'train_img').mkdir(exist_ok=True)
(base_path/'train_mask').mkdir(exist_ok=True)
(base_path/'test_img').mkdir(exist_ok=True)
(base_path/'test_mask').mkdir(exist_ok=True)

# Obter lista de todas as imagens do dataset
file_list = list_files(dataset_dir)

# Processa as imagens e máscaras na lista, redimensionando para 320x240
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_img = {executor.submit(
        preprocess_file, img_file, work_dir): img_file for img_file in file_list}

# Divide o dataset
file_list = list_files(work_dir+'/train_img')
train_imgs, test_imgs = split_dataset(file_list)
for filename in test_imgs:
    newimgfilename = filename.replace('train_', 'test_')
    os.rename(filename, newimgfilename)
    maskfilename = filename.replace('train_img', 'train_mask')
    newmaskfilename = maskfilename.replace('train_mask', 'test_mask')
    os.rename(maskfilename, newmaskfilename)

# imagenet mean/std will be used as the resnet backbone is trained on imagenet stats
mean, std = (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)
