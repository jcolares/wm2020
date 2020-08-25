#from preprocessing import json_2_bitmap, resize_320x240, list_files, preprocess_file
from preprocessing import list_files
from training import *
import segmentation_models_pytorch as smp
from utils import getArgs

# load variables from file
args = getArgs('segmentation/args.yaml')
img_dir = args['img_dir']
mask_dir = args['mask_dir']
mean = args['mean']
std = args['std']


# Obter lista de todas as imagens do dataset
df = list_files(img_dir)


# Treinamento
model = smp.Unet("resnet18",  encoder_weights="imagenet",
                 classes=1, activation=None)
model_trainer = Trainer(model, df, img_dir, mask_dir, mean, std)
model_trainer.start()
