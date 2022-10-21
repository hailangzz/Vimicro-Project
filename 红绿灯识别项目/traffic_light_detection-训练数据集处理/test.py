import numpy as np
import imgaug as ia
import imgaug.augmenters as iaa
import cv2
import os

# Sometimes（0.5，…）在50%的情况下应用给定的增强器，
# 例如，Sometimes（0.5，GaussianBlur（0.3））大约每秒都会模糊图像。
sometimes = lambda aug: iaa.Sometimes(0.5, aug)

# 定义将应用于每个图像的增强步骤序列。
seq = iaa.Sequential(
    [
        #
        # 将以下增强器应用于大多数图像。
        #
        iaa.Fliplr(0.5),  # 水平翻转所有图像的50%
        iaa.Flipud(0.2),  # 垂直翻转所有图像的20%

        # 将部分图像裁剪为其高度/宽度的0-10%
        sometimes(iaa.Crop(percent=(0, 0.1))),

        # 对某些图像应用仿射变换
        # -缩放到图像高度/宽度的80-120%（每个轴独立）
        # -相对于高度/宽度（每轴）平移-20到+20
        # -旋转-45到+45度
        # -剪切-16至+16度
        # -顺序：使用最近邻或双线性插值（fast）
        # -模式：使用任何可用模式填充新创建的像素
        #         请参阅API或scikit图像，了解哪些模式可用
        # - -cval：如果模式恒定，则使用随机亮度对于新创建的像素（例如，有时为黑色，有时为白色）
        sometimes(iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
            translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
            rotate=(-45, 45),
            shear=(-16, 16),
            order=[0, 1],
            cval=(0, 255),
            mode=ia.ALL
        )),

        #
        # 每个图像执行以下0到5个（不太重要）增强器。不要全部执行，因为这通常会太过强烈。
        #
        iaa.SomeOf((0, 5),
                   [
                       # 将一些图像转换为其超像素表示，每个图像采样20到200个超像素，
                       # 但不要用其平均值替换所有超像素，只替换其中的一些（p_replace）。
                       sometimes(
                           iaa.Superpixels(
                               p_replace=(0, 1.0),
                               n_segments=(20, 200)
                           )
                       ),

                       # 使用不同的强度模糊每个图像
                       # 高斯模糊（sigma介于0和3.0之间）
                       # 平均/均匀模糊（内核大小在2x2和7x7之间）
                       # 中值模糊（内核大小在3x3和11x11之间）。
                       iaa.OneOf([
                           iaa.GaussianBlur((0, 3.0)),
                           iaa.AverageBlur(k=(2, 7)),
                           iaa.MedianBlur(k=(3, 11)),
                       ]),

                       # 锐化每个图像，使用介于0（无锐化）和1（完全锐化效果）之间的alpha将结果与原始图像覆盖。
                       iaa.Sharpen(alpha=(0, 1.0), lightness=(0.75, 1.5)),

                       # 与锐化相同，但用于浮雕效果。
                       iaa.Emboss(alpha=(0, 1.0), strength=(0, 2.0)),

                       # 在某些图像中搜索所有边缘或定向边缘。
                       # 然后在黑白图像中标记这些边缘，并使用0到0.7的alpha与原始图像叠加。
                       sometimes(iaa.OneOf([
                           iaa.EdgeDetect(alpha=(0, 0.7)),
                           iaa.DirectedEdgeDetect(
                               alpha=(0, 0.7), direction=(0.0, 1.0)
                           ),
                       ])),

                       # 在一些图像中添加高斯噪声。在其中50%的情况下，噪声是按通道和像素随机采样的。
                       # 在其他50%的情况下，每像素采样一次（即亮度变化）。
                       iaa.AdditiveGaussianNoise(
                           loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5
                       ),

                       # 要么随机删除所有像素的1%到10%（即将其设置为黑色），
                       # 要么将其放置在原始大小的2%到5%的图像上，从而导致大矩形的删除。
                       iaa.OneOf([
                           iaa.Dropout((0.01, 0.1), per_channel=0.5),
                           iaa.CoarseDropout(
                               (0.03, 0.15), size_percent=(0.02, 0.05),
                               per_channel=0.2
                           ),
                       ]),

                       # 以5%的概率反转每个图像的通道
                       # 这将每个像素值设置为255-v
                       iaa.Invert(0.05, per_channel=True),  # 反转颜色通道

                       # 为每个像素添加-10到10的值。
                       iaa.Add((-10, 10), per_channel=0.5),

                       # 更改图像亮度（原始值的50-150%）。
                       iaa.Multiply((0.5, 1.5), per_channel=0.5),

                       # 改善或恶化图像的对比度。
                       iaa.LinearContrast((0.5, 2.0), per_channel=0.5),

                       # 将每个图像转换为灰度，然后用随机alpha将结果与原始图像叠加。去除不同强度的颜色。
                       iaa.Grayscale(alpha=(0.0, 1.0)),

                       # 在某些图像中，局部移动像素（具有随机强度）。
                       sometimes(
                           iaa.ElasticTransformation(alpha=(0.5, 3.5), sigma=0.25)
                       ),

                       # 在一些图像中，局部区域的扭曲程度不同。
                       sometimes(iaa.PiecewiseAffine(scale=(0.01, 0.05)))
                   ],
                   # 按随机顺序执行上述所有增强
                   random_order=True
                   )
    ],
    # 按随机顺序执行上述所有增强
    random_order=True
)

# 图片文件相关路径
path = 'before/'
savedpath = 'after/'

imglist = []
filelist = os.listdir(path)

# 遍历要增强的文件夹，把所有的图片保存在imglist中
for item in filelist:
    img = cv2.imread(path + item)
    # print('item is ',item)
    # print('img is ',img)
    # images = load_batch(batch_idx)
    imglist.append(img)
# print('imglist is ' ,imglist)
print('all the picture have been appent to imglist')

# 对文件夹中的图片进行增强操作，循环100次
for count in range(100):
    images_aug = seq.augment_images(imglist)
    for index in range(len(images_aug)):
        filename = str(count) + str(index) + '.jpg'
        # 保存图片
        cv2.imwrite(savedpath + filename, images_aug[index])
        print('image of count%s index%s has been writen' % (count, index))