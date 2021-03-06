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
import random

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


def resize(fn, w=512, h=512, interpolate=0):
    ratio = max(fn.shape[0]/h, fn.shape[1]/w)
    new_h = round(fn.shape[0]/ratio)
    new_w = round(fn.shape[1]/ratio)
    if interpolate == 1:
        new_fn = cv2.resize(fn, (new_w, new_h), fx=0, fy=0,
                            interpolation=cv2.INTER_AREA)
    else:
        new_fn = cv2.resize(fn, (new_w, new_h), fx=0, fy=0,
                            interpolation=cv2.INTER_NEAREST)
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
    pathlist = Path(sourcePath).glob('**/'+pattern)
    file_list = []
    for path in pathlist:
        path_in_str = str(path)  # because path is object not string
        file_list.append(path_in_str)
    return (file_list)


def preprocess_file(img_file, work_dir):
    if os.path.splitext(os.path.basename(img_file))[1] == '.json':
        img = json_2_bitmap(img_file)
        img = resize(img)
        dest_file = work_dir + '/train_mask/' + \
            os.path.splitext(os.path.basename(img_file))[0]
    else:
        img = cv2.imread(img_file, 1)
        img = resize(img)
        dest_file = work_dir + '/train_img/' + \
            os.path.basename(img_file)
    cv2.imwrite(dest_file, img)
    return


'''
def split_dataset(file_list):
    # from https://cs230.stanford.edu/blog/split/#theory-how-to-choose-the-train-train-dev-dev-and-test-sets
    file_list.sort()  # make sure that the file_list have a fixed order before shuffling
    random.seed(230)
    # shuffles the ordering of file_list (deterministic given the chosen seed)
    random.shuffle(file_list)
    split_1 = int(0.8 * len(file_list))
    split_2 = int(0.9 * len(file_list))
    train_file_list = file_list[:split_1]
    #dev_file_list = file_list[split_1:split_2]
    #test_file_list = file_list[split_2:]
    # return(train_file_list, dev_file_list, test_file_list)
    test_file_list = file_list[split_1:]
    return(train_file_list, test_file_list)
'''
