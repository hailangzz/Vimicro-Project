import warnings
warnings.filterwarnings("ignore")

import os
import xml.etree.cElementTree as ET
from PIL import Image
import shutil
from tqdm import tqdm
import random
import copy

image_path = r'D:\迅雷下载\AI数据集汇总\红绿灯检测数据集\traffic_light_detection\traffic_light_detection\new_mask_sample\GAL_1\image.0044.jpg'

# 对新的标注区图进行resize操作
def create_random_shape_mask_img(resize=(24,24)):

    mask_img = Image.open(image_path)
    resize_mask1 = mask_img.resize(resize, Image.BILINEAR) # 双现行插值
    resize_mask2 = mask_img.resize(resize, Image.ANTIALIAS)

    resize_mask1.save('resize_mask1.jpg')
    resize_mask2.save('resize_mask2.jpg')

create_random_shape_mask_img(resize=(24,24))