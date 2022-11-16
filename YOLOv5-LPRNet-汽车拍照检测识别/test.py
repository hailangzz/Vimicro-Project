import numpy as np
import random
np.random.seed(1)
traxi = np.random.uniform(0, 1, size=[1, 3, 24, 94])
print(traxi)

train_label_CHARS = ['京', '沪', '津', '渝', '冀', '晋', '蒙', '辽', '吉', '黑',
                     '苏', '浙', '皖', '闽', '赣', '鲁', '豫', '鄂', '湘', '粤',
                     '桂', '琼', '川', '贵', '云', '藏', '陕', '甘', '青', '宁',
                     '新',
                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
                     'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                     'W', 'X', 'Y', 'Z', 'I', 'O', '-'
                    ]
CHARS_DICT = {char:i for i, char in enumerate(train_label_CHARS)}   # {'京': 0, '沪': 1, '津': 2, '渝': 3, '冀': 4, '晋':

print(CHARS_DICT)