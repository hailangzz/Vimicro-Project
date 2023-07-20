import cv2
import numpy as np
import random

img = cv2.imread("6-41-38-32-31-60-40_45419strengthen1138.jpg",1)  #读取一张图片，彩色
cha=img.shape
height,width,deep=cha
cv2.imshow('img',img)
dst=np.zeros(cha,np.uint8)
randon_v=7 #用来替换的范围--这个值越大毛玻璃效果越明显
#防止越界
for m in range(height-randon_v):  #毛玻璃效果
    for n in range(width-randon_v):
        index=random.randint(1,randon_v)
        (b,g,r)=img[m+index,n+index]
        dst[m,n]=(b,g,r)
cv2.imshow('dst',dst)
cv2.waitKey()
