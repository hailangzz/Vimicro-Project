import numpy as np
import os
from shutil import copy2

total_images_path = r'D:\迅雷下载\AI数据集汇总\汽车拍照检测识别\CCPD_COCO_dataset\train\images'


origin_sample_path = r"D:\迅雷下载\AI数据集汇总\汽车拍照检测识别\CCPD2019\ccpd_base"

save_images_path = r'D:\迅雷下载\AI数据集汇总\汽车拍照检测识别\CCPD_COCO_buff\train\images'
total_images_list = os.listdir(total_images_path)
trainfiles = os.listdir(origin_sample_path)  #（图片文件夹）

print(len(total_images_list),len(trainfiles))


reduce_number = 0
for single_image in trainfiles:
    if single_image not in total_images_list:
        reduce_number+=1
        fileName = os.path.join(origin_sample_path, single_image)  # （图片文件夹）+图片名=图片地址
        copy2(fileName, save_images_path)

print(reduce_number)