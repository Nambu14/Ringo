#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Calculates the TanTriggs Preprocessing as described in:
#
#      Tan, X., and Triggs, B. "Enhanced local texture feature sets for face
#      recognition under difficult lighting conditions.". IEEE Transactions
#      on Image Processing 19 (2010), 1635–650.
#
# Default parameters are taken from the paper

import cv2
import numpy as np


ALPHA = 0.1
TAU = 10.0
GAMMA = 0.2
SIGMA0 = 1
SIGMA1 = 2


def tan_triggs(image):
    # Convert to float
    image = np.float32(image)

    image = cv2.pow(image, GAMMA)

    image = difference_of_gaussian(image)

    # mean
    image = cv2.pow(cv2.absdiff(image, 0), ALPHA)
    mean = cv2.mean(image)[0]
    np.divide(image, cv2.pow(mean, 1.0/ALPHA))

    show(image)


def difference_of_gaussian(image):
    kernel_size0 = SIGMA0 * 3
    kernel_size1 = SIGMA1 * 3

    kernel_size0 += 1 if kernel_size0 % 2 == 0 else 0
    kernel_size1 += 1 if kernel_size1 % 2 == 0 else 0

    gaussian0 = cv2.GaussianBlur(image, (kernel_size0, kernel_size0), SIGMA0, None, SIGMA0, cv2.BORDER_REPLICATE)
    gaussian1 = cv2.GaussianBlur(image, (kernel_size1, kernel_size1), SIGMA1, None, SIGMA1, cv2.BORDER_REPLICATE)

    return cv2.subtract(gaussian0, gaussian1)


def show(image):
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    cv2.imshow("Tan Triggs", image)
