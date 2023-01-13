import numpy as np
import os
from shutil import copy2

origin_path = r'D:\迅雷下载\AI数据集汇总\test_vidoe_Image_dataset\train\images'
save_labels_path = r'D:\迅雷下载\AI数据集汇总\test_vidoe_Image_dataset\train\labels'
images_name_list = os.listdir(origin_path)
for image_name in images_name_list:
    save_label_path = os.path.join(save_labels_path,image_name.replace('.jpg','.txt'))

    label_txt_cur = open(save_label_path,'w')
    label_txt_cur.write(image_name)
    label_txt_cur.close()
    # print(save_label_path)