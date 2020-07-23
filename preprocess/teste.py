from preprocessing import json_2_bitmap, resize_320x240, list_files
import cv2
from pathlib import Path
import os

# Parametros
dataset_dir = '/home/jeff/datasets/Supervisely Person Dataset'
work_dir = '/home/jeff/datasets/SPD'

# Const
base_path = Path(work_dir)

# Criar diretorios de trabalho
base_path.mkdir(exist_ok=True)
(base_path/'masks_png').mkdir(exist_ok=True)
(base_path/'images_320x240').mkdir(exist_ok=True)
(base_path/'masks_png_320x240').mkdir(exist_ok=True)

# Processar imagens e silhuetas
file_list = list_files(dataset_dir, 'bike*.*')
for img_file in file_list:
    if os.path.splitext(os.path.basename(img_file))[1] == '.json':
        img = json_2_bitmap(img_file)
        img = resize_320x240(img)
        dest_file = work_dir + '/masks_png_320x240/' + \
            os.path.splitext(os.path.basename(img_file))[0]
    else:
        img = cv2.imread(img_file, 1)
        img = resize_320x240(img)
        dest_file = work_dir + '/images_320x240/' + os.path.basename(img_file)
    cv2.imwrite(dest_file, img)
