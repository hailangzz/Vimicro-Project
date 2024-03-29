import os
from PIL import Image


def xywh2xyxy(coco_info=[0.333854,0.559259,0.0114583,0.0537037],image_shape=[1920,1080]):
    w = image_shape[0]*coco_info[2]
    h = image_shape[1]*coco_info[3]

    x1 = image_shape[0]*coco_info[0] - w/2
    y1 = image_shape[1] * coco_info[1] - h/2
    x2 = image_shape[0] * coco_info[0] + w / 2
    y2 = image_shape[1] * coco_info[1] + h / 2

    return int(x1),int(y1),int(x2),int(y2)

def cvtx0y0whTox1y1x2y2(x0, y0, w, h, imgShape=(576,1024,3)):
    # "0.530921 0.666667 0.622368 0.666667"=>(167, 169, 639, 507)
    # labelme 的COCO标注格式就是 中心点x+中心点y+宽+高 （归一化的）
    # 此函数出来的就是 左上点  右下点  （未归一化的）
    height, width, c = imgShape
    x1, y1, x2, y2 = int((x0 - w * 0.5) * width), \
                     int((y0 - h * 0.5) * height), \
                     int((x0 + w * 0.5) * width), \
                     int((y0 + h * 0.5) * height)
    return x1, y1, x2, y2

def cut_crops_function(image_path, box_info_list,save_detect_crops_path,train_image_size=[1024,576]):
    image = Image.open(image_path)
    # print(image.size)
    for detect_box_info_index in range(len(box_info_list)):
        detect_box_info = box_info_list[detect_box_info_index]
        x1 = int(detect_box_info[0]*image.size[0]/train_image_size[0])
        y1 = int(detect_box_info[1] * image.size[1] / train_image_size[1])
        x2 = int(detect_box_info[2] * image.size[0] / train_image_size[0])
        y2 = int(detect_box_info[3] * image.size[1] / train_image_size[1])
        real_box_info=[x1,y1,x2,y2]
        # print(real_box_info)
        crops_name = image_path.split('\\')[-1].replace('.jpg','_'+str(detect_box_info_index)+'.jpg')
        save_crops_path = os.path.join(save_detect_crops_path,crops_name)
        cropped_image = image.crop(real_box_info)

        cropped_image.save(save_crops_path)
    image.close()


def get_image_box_info_list(single_image_label_path):
    box_info_list = []
    label_cur = open(single_image_label_path,'r')
    all_row_label_info = label_cur.readlines()
    for row_label in all_row_label_info:
        row_label = row_label.strip()
        row_label = [float(float_value) for float_value in row_label.split(' ')[2:]]
        box_info_list.append(row_label)
        # print(row_label)
    # print(box_info_list)
    return box_info_list

def get_total_image_info(
        origin_image_path=r'D:\Git_WareHouse\yolov5-master\traffic_light_test_DVR',
        origin_coco_label_path=r'D:\Git_WareHouse\yolov5-master\detect\exp\labels',
        save_detect_crops_path=r'D:\PycharmProgram\sample_yolov5_calMAP\crops',
        train_image_size=[1024,576]
                         ):

    total_image_name_list = os.listdir(origin_coco_label_path)
    for single_image_label_name in total_image_name_list:
        single_image_name = single_image_label_name.replace('.bin_result.txt','.jpg')
        single_image_path = os.path.join(origin_image_path,single_image_name)
        single_image_label_path = os.path.join(origin_coco_label_path, single_image_label_name)

        box_info_list = get_image_box_info_list(single_image_label_path)
        cut_crops_function(single_image_path,box_info_list,save_detect_crops_path,train_image_size)

images_path = r'D:\PycharmProgram\sample_yolov5_calMAP\images'
detect_labels_path =r'D:\PycharmProgram\sample_yolov5_calMAP\result'

save_detect_crops_path = r'D:\迅雷下载\AI数据集汇总\汽车拍照检测识别\detect_car_brand_crops\detect_car_brand_crops_focus_8' # 保存检测目标剪切图片的路径


get_total_image_info(images_path,detect_labels_path,save_detect_crops_path)


# result_file_path = os.path.join(detect_labels_path,r'20221101_125117_NF_385.bin_result.txt')
#
# box_info_list=get_image_box_info_list(result_file_path)
# cut_crops_function(r'D:\PycharmProgram\sample_yolov5_calMAP\images\20221101_125117_NF_385.jpg',box_info_list,save_detect_crops_path)


### 注：bin文件的标注坐标，是讲1920*1080 等比例缩放为1024*576后标注的坐标，因此坐标要对应放大1920/1024、1080/576的比例。