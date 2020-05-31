# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 17:17:27 2020

@author: adnane
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

'''Example images used in the report'''
#filename = './Dataset/S07-33-MAX_Dm-Kr walking No 182 - NC14.lif - overview.tif'
filename = './Dataset/S04-04-MAX_Dm-Kr length No 193.lif - overview.tif'
#filename = './Dataset/S05-05-MAX_Dm-Kr mRNA B2 B3 seperate probes 3h Amp.lif - overview.tif'
#filename = './Dataset/S06-06-MAX_Dm-Kr mRNA B2 B3 seperate probes ON Amp.lif - overview.tif'
#filename = './Dataset/S01-34-MAX_Dm-Kr walking No 182.lif - overview embryo1.tif'


def cell_counter(filename, plot=False, n=100, m=100):
    '''Returns the number of cells inside the window of the image defined by
    n for height and m for width'''

    def load_image(filename):
        '''returns the image in the filename from the datatset'''
        img = cv2.imreadmulti(filename)
        img = img[1][0]
        return(img)

    img = load_image(filename)

    witness = img.copy()

    '''Initial background mask using a safe global threshold at 20'''
    th = 20
    mask = np.where(img < th)

    '''Denoising median blur'''
    img = cv2.medianBlur(img, 5)

    '''Mean Adaptive thresholding '''
    img = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 0)

    '''Applying the initial background mask'''
    img[mask] = 0

    '''Median blur as a post processing noise removal'''
    img = cv2.medianBlur(img, 9)

    img = img[img.shape[0] // 2 - n: img.shape[0] // 2 +
              n, img.shape[1] // 2 - m: img.shape[1] // 2 + m]

    if plot:
        plt.title('Mean adaptive thresholding')
        plt.imshow(img)
        plt.show()

    witness = witness[witness.shape[0] // 2 - n: witness.shape[0] //
                      2 + n, witness.shape[1] // 2 - m: witness.shape[1] // 2 + m]

    witness = cv2.cvtColor(witness, cv2.COLOR_GRAY2RGB)

    # =============================================================================
    # watershed
    # =============================================================================

    '''Distance transform'''
    sure_bg = img.copy()

    dist_transform = cv2.distanceTransform(img, cv2.DIST_L2, 5)

    if plot:
        plt.title('Distance transform')
        plt.imshow(dist_transform)
        plt.show()

    '''Watershed to separate touching cells'''
    ret, sure_fg = cv2.threshold(
        dist_transform, 0.5 * dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = markers.astype('int32')

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    markers = cv2.watershed(img, markers)
    img[markers == -1] = [0, 0, 0]

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    '''Bitwise and median blur to remove salt noise'''
    median = cv2.medianBlur(img, 5)
    img = np.bitwise_and(median, img)

    if plot:
        plt.title('Original')
        plt.imshow(witness)
        plt.show()

    if plot:
        plt.title('Final counted connected components')
        plt.imshow(img)
        plt.show()

    num_cells, labels_im = cv2.connectedComponents(img, connectivity=4)
    print('There are ' + str(num_cells - 1) +
          ' cells in an area of ' + str(2 * n * 2 * m) + ' pixels')

    def imshow_components(labels):
        # Map component labels to hue val
        label_hue = np.uint8(179 * labels / np.max(labels))
        blank_ch = 255 * np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

        # cvt to BGR for display
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

        # set bg label to black
        labeled_img[label_hue == 0] = 0

        cv2.imshow('labeled.png', labeled_img)
        cv2.waitKey()
        return(labeled_img)

    if plot:
        imshow_components(labels_im)

    return(num_cells - 1)


if __name__ == "__main__":
    count = cell_counter(filename, plot=True)
