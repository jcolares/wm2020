from preprocessing import *
import cv2
from pathlib import Path
import os
import concurrent.futures


# Parameters
dataset_dir = '/home/jeff/datasets/Supervisely Person Dataset'
work_dir = '/home/jeff/datasets/SPD'

# Create working directories
base_path = Path(work_dir)
base_path.mkdir(exist_ok=True)
(base_path/'train_img').mkdir(exist_ok=True)
(base_path/'train_mask').mkdir(exist_ok=True)

# Get list of images in the dataset
file_list = list_files(dataset_dir)

print('Please wait pre processing images')
# Process images and corresponding masks
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_img = {executor.submit(
        preprocess_file, img_file, work_dir): img_file for img_file in file_list}

print('FINISH')
