import cv2
import numpy as np

picture = r'D:\迅雷下载\AI数据集汇总\汽车拍照检测识别\CCPD_COCO_dataset\train\images\\01-89_92-300&547_485&612-496&612_301&613_297&552_492&551-0_0_28_32_30_31_33-140-41.jpg'
img = cv2.imdecode(np.fromfile(picture, dtype=np.uint8), -1)
print(img.shape)

result = 'aasdf'
print(r"D:\迅雷下载\AI数据集汇总\汽车拍照检测识别\CCPD_rec_images\{}\{}.jpg".format('test',result))

total_rec_path_info={
                     'train':r'D:\迅雷下载\AI数据集汇总\汽车拍照检测识别\CCPD_COCO_dataset\train\images',
                     'val':r'D:\迅雷下载\AI数据集汇总\汽车拍照检测识别\CCPD_COCO_dataset\val\images',
                     'test':r'D:\迅雷下载\AI数据集汇总\汽车拍照检测识别\CCPD_COCO_dataset\test\images',
                     }

for i in total_rec_path_info.items():
    print(i)