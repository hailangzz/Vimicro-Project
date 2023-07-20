import os
import json


json_dir = r'F:\AiTotalDatabase\铝片缺陷检测\aluminum\annotations\train.json'  # json文件路径
out_dir = r'F:\AiTotalDatabase\铝片缺陷检测\aluminum\annotations\train'  # 输出的 txt 文件路径


def main():
    # 读取 json 文件数据
    with open(json_dir, 'r') as load_f:
        content = json.load(load_f)
    # 循环处理
    for t in content:
        print(content.keys())
        print(len(content['info']), content['info'])
        print(len(content['categories']), content['categories'])
        print(len(content['annotations']), content['annotations'])
        print(len(content['images']),content['images'])
        tmp = t['name'].split('.')
        filename = out_dir + tmp[0] + '.txt'

        if os.path.exists(filename):
            # 计算 yolo 数据格式所需要的中心点的 相对 x, y 坐标, w,h 的值
            x = (t['bbox'][0] + t['bbox'][2]) / 2 / t['image_width']
            y = (t['bbox'][1] + t['bbox'][3]) / 2 / t['image_height']
            w = (t['bbox'][2] - t['bbox'][0]) / t['image_width']
            h = (t['bbox'][3] - t['bbox'][1]) / t['image_height']
            fp = open(filename, mode="r+", encoding="utf-8")
            file_str = str(t['category']) + ' ' + str(round(x, 6)) + ' ' + str(round(y, 6)) + ' ' + str(round(w, 6)) + \
                       ' ' + str(round(h, 6))
            line_data = fp.readlines()

            if len(line_data) != 0:
                fp.write('\n' + file_str)
            else:
                fp.write(file_str)
            fp.close()

        # 不存在则创建文件
        else:
            fp = open(filename, mode="w", encoding="utf-8")
            fp.close()


if __name__ == '__main__':
    main()