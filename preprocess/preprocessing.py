import os
import io
from pathlib import Path
import PIL
import cv2
import numpy as np
import base64
import json
import os.path as osp
from labelme import utils
import zlib


# =========================================================
#   convert Supervise.ly JSON annotations to image files
# =========================================================

# this function from: https://docs.supervise.ly/data-organization/import-export/supervisely-format
def base64_2_mask(s):
    z = zlib.decompress(base64.b64decode(s))
    n = np.fromstring(z, np.uint8)
    mask = cv2.imdecode(n, cv2.IMREAD_UNCHANGED)[:, :, 3].astype(bool)
    return mask


def json_2_bitmap(source_file, dest_file=''):
    # Read data from JSON file
    json_file = open(source_file, 'r')
    json_data = json_file.read()
    ann = json.loads(json_data)
    image_h = ann['size']['height']
    image_w = ann['size']['width']
    mask_img = np.zeros([image_h, image_w])

    # Generate image mask
    if ann['objects'][0]['geometryType'] == 'bitmap':
        origin = ann['objects'][0]['bitmap']['origin']
        base64_data = ann['objects'][0]['bitmap']['data']
        mask_data = base64_2_mask(base64_data)
        mask_h = len(mask_data)
        mask_w = len(mask_data[0])
        for h in range(mask_h):
            for w in range(mask_w):
                if mask_data[h, w] == True:
                    mask_img[h + origin[1], w + origin[0]] = 255
    elif ann['objects'][0]['geometryType'] == 'polygon':
        poly = ann['objects'][0]['points']['exterior']
        mask_img = PIL.Image.new('L', (image_w, image_h), 0)
        poly_l = np.array(poly).flatten().tolist()
        PIL.ImageDraw.Draw(mask_img).polygon(
            poly_l, outline=255, fill=255)
    mask_img = np.array(mask_img)

    if dest_file != '':
        cv2.imwrite(dest_file, mask_img)
    else:
        return(mask_img)


def resize_320x240(fn, w=320, h=240, interpolate=0):
    ratio = max(fn.shape)/w
    new_h = round(fn.shape[0]/ratio)
    new_w = round(fn.shape[1]/ratio)
    # new_fn = cv2.resize(fn, (new_w, new_h), fx=0, fy=0,
    #                    interpolation=cv2.INTER_AREA)
    new_fn = cv2.resize(fn, (new_w, new_h), fx=0, fy=0)
    pad_h = w - new_w
    pad_v = h - new_h
    pad_l = round(pad_h / 2)
    pad_r = pad_h - pad_l
    pad_t = round(pad_v / 2)
    pad_b = pad_v - pad_t
    new_fn = cv2.copyMakeBorder(
        new_fn, pad_t, pad_b, pad_l, pad_r, cv2.BORDER_CONSTANT, value=0)
    return new_fn


def list_files(sourcePath, pattern='*.*'):
    #pattern = 'bike*.png'
    pathlist = Path(sourcePath).glob('**/'+pattern)
    directories = []
    for path in pathlist:
        path_in_str = str(path)  # because path is object not string
        #label = int(os.path.basename(path)[0:3])
        # myfile.write(path_in_str)
        directories.append(path_in_str)
    return (directories)
