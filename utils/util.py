from __future__ import print_function, division

import cv2
import numpy as np
from utils import config


def write_image(path, image):
    cv2.imwrite(path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))


def resize(image, gt_boxes=None):
    ih, iw = config.image_size, config.image_size
    h, w, _ = image.shape

    scale = min(iw / w, ih / h)
    nw, nh = int(scale * w), int(scale * h)
    image_resized = cv2.resize(image, (nw, nh))

    image_padded = np.zeros(shape=[ih, iw, 3], dtype=np.uint8)
    dw, dh = (iw - nw) // 2, (ih - nh) // 2
    image_padded[dh:nh + dh, dw:nw + dw, :] = image_resized.copy()

    if gt_boxes is None:
        return image_padded

    else:
        gt_boxes[:, [0, 2]] = gt_boxes[:, [0, 2]] * scale + dw
        gt_boxes[:, [1, 3]] = gt_boxes[:, [1, 3]] * scale + dh
        return image_padded, gt_boxes


class WeightReader:
    def __init__(self, weight_file):
        self.offset = 4
        self.all_weights = np.fromfile(weight_file, dtype='float32')

    def read_bytes(self, size):
        self.offset = self.offset + size
        return self.all_weights[self.offset - size:self.offset]

    def reset(self):
        self.offset = 4
