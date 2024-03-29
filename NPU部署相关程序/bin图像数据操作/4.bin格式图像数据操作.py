import cv2
import os
import numpy as np


# 注：保存bin格式图像数据
output_path = r'C:\Users\zhangzuo\Desktop\02.DebugTools\\'
image = r'C:\Users\zhangzuo\Desktop\toluchang_20230608\cross\\1.jpg'

def jpg2bin(img_path, bin_path):
    # img_ori = cv2.imread(img_path)
    img_ori = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)

    img_ori = cv2.resize(img_ori, (640, 352))
    print(img_ori.shape)
    img = img_ori[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB,
    img = np.ascontiguousarray(img)

    # im = im.half() if half else im.float()  # uint8 to fp16/32

    #############################################################
    #  保存输入网络的bin文件
    binName = img_path.split('\\')[-1].split('.')[0]
    binPath = bin_path + binName + '_in640_352.bin'


    img.astype(np.int8).tofile(binPath)
    return binPath, img_ori

binPath, img_ori=jpg2bin(image,output_path)

# binPath = r'D:\中星微人工智能工作\pytorch迁移学习\yolov5s_face\in0.bin'
#注：读取bin图像数据文件
y = np.fromfile(binPath, dtype=np.int8)
print(y.shape)