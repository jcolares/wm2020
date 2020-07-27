#from preprocessing import json_2_bitmap, resize_320x240, list_files, preprocess_file
from preprocessing import list_files
from training import *
import segmentation_models_pytorch as smp


global df, img_dir, mask_dir, mean, std
#img_dir = '/home/jeff/datasets/SPD/train_img'
#mask_dir = '/home/jeff/datasets/SPD/train_mask'
img_dir = 'data/train_img'
mask_dir = 'data/train_mask'

# imagenet mean/std will be used as the resnet backbone is trained on imagenet stats
mean, std = (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)

# Obter lista de todas as imagens do dataset
df = list_files(img_dir)


# Treinamento
model = smp.Unet("resnet18", encoder_weights="imagenet",
                 classes=1, activation=None)
model_trainer = Trainer(model, df, img_dir, mask_dir, mean, std)
model_trainer.start()
