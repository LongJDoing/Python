#coding=utf-8
'''
Created on 2014��4��16��

@author: Administrator
'''
from PIL import Image
import math
import numpy as np


# Image Normalization
def make_regalur_image(img, size=(25,25), B_Ch = False, B_is = True ):
    
    if B_is:       
        img = img.resize(size, Image.ANTIALIAS)

    #w,h = img.size
    if  B_Ch:
        if len(img.getbands()) == 4:
            ir,ig,ib,ia = img.split()
            im = img.convert("L")
            im = np.array(im)
            ia = np.array(ia)
            im_av = np.var(ia[ia>0])
            im_v = np.var(im[im>0])
            if np.isnan(im_av):
                return im
            if np.isnan(im_v):
                return ia
            ia = ia/255.0
            im = np.multiply(im,ia)
            im.astype(int)
        else:
            im = img.convert("L")
            im = np.array(im)    
        #w,h = image.size
        #image = image.crop((2, 2, w-2, h-2))
        #image.show()
        return im
    else:
        #基本上都是使用alpha通道结果
        #=======================================================================
        # if len(img.getbands()) == 4:
        #     ir,ig,ib,ia = img.split()
        #     im_a = np.array(ia)
        #     im_av = np.var(im_a[im_a>0])
        #     im = img.convert("L")
        #     im = np.array(im)
        #     im_v = np.var(im[im>0])
        #     if not np.isnan(im_av):
        #         return im_a
        #     if not np.isnan(im_v):
        #         return im_a
        #     #if abs(im_av) <  abs(im_v):
        #         #return im
        #     #else:
        #         #return im_a
        #     return im_a
        #=======================================================================
        #使用alpha通道与灰度之间的一个信息比较多的
        if len(img.getbands()) == 4:
            ir,ig,ib,ia = img.split()
            im_a = np.array(ia)
            im_av = np.var(im_a[im_a>0])
            im = img.convert("L")
            im = np.array(im)
            im_v = np.var(im[im>0])
            if  np.isnan(im_av):
                return im
            if  np.isnan(im_v):
                return im_a
            if abs(im_av) <  abs(im_v):
                return im
            else:
                 return im_a
        else:
            return np.array(img.convert("L"))

def split_image(img, part_size=(64,64)):
    w,h = img.size
    pw,ph = part_size
    
    assert w %pw == h % ph == 0
    
    return [img.crop((i,j,i+pw,j+ph)).copy() \
            for i in xrange(0,w,pw) \
            for j in xrange(0,h,ph)]
    
    
def image_entropy(img):
    '''Calculate the entropy of an image:'''
    histogram = img.histogram()
    histogram_length = sum(histogram)
    
    samples_probability = [float(h) / histogram_length for h in histogram]
    
    return -sum([p * math.log(p, 2) for p in samples_probability if p != 0])


def dispersion_image(img, ind1, ind2):
    '''
    calculate the distance of interesting points
    input:
    img : image
    ind1: decide the gray level range of interesting points
    ind2: decide the distance of features
    
    sample 
            dispersion_image(image, 255/20, 15)
    '''
    X = []

    w, h = img.size
    for i in xrange(w):
        for j in xrange(h):
            px = img.getpixel((i,j))
            #print px
            if px > ind1:
                X.append([i,j])
    X = np.array(X)
    X = X.T
    meanx = np.mean(X[0])
    meany = np.mean(X[1])
    tpsumx = sum(abs(X[0]-meanx))
    tpsumy = sum(abs(X[1]-meany))
    tpsum = min(tpsumx, tpsumy)
    #print tpsum
    #print len(X[0])
    #print tpsum/len(X[0])
    ''' tpsum/len(x[0] is low 15 can be considered'''
    if tpsum/len(X[0]) > ind2:
        return False
    return True

import warnings

def histogram(image, nbins=256):
   
    sh = image.shape
    if len(sh) == 3 and sh[-1] < 4:
        warnings.warn("This might be a color image. The histogram will be "
                      "computed on the flattened image. You can instead "
                      "apply this function to each color channel.")

    if np.issubdtype(image.dtype, np.integer):
        offset = 0
        if np.min(image) < 0:
            offset = np.min(image)
        hist = np.bincount(image.ravel() - offset)
        bin_centers = np.arange(len(hist)) + offset

        idx = np.nonzero(hist)[0][0]
        return hist[idx:], bin_centers[idx:]
    else:
        hist, bin_edges = np.histogram(image.flat, nbins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
        return hist, bin_centers

def threshold_otsu(image, nbins=256):
   
    hist, bin_centers = histogram(image, nbins)
    hist = hist.astype(float)

    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]

    mean1 = np.cumsum(hist * bin_centers) / weight1
    mean2 = (np.cumsum((hist * bin_centers)[::-1]) / weight2[::-1])[::-1]

    variance12 = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:])**2

    idx = np.argmax(variance12)
    threshold = bin_centers[:-1][idx]
    return threshold
 
#import matplotlib.pyplot as plt       

def choose_featureregion(img, d = True):
    
    #img = image.convert("L")
    #I have proved it isnot good to use otsu here
    threshold = threshold_otsu(img)
    #threshold = 0 #参考了一些图像，它们具有完全相同的形状，只是颜色不同
    if d == True:
        img_bw = img > threshold
    else:
        img_bw = img < threshold
    '''
    #Speed decreases, and the result is not correct
    im_hist, edges = np.histogram(img, bins=256, range=[0,255])    
    index = max((var, index) for index, var in enumerate(im_hist))[1]    
    w, h = img.shape
    img_bw = img
    for i in range(w):
        for j in range(h):
            if img[i,j] == index:
                img_bw[i,j] = 0
            else:
                img_bw[i,j] = 1
            
   ''' 
#    plt.imshow(img_bw, cmap='gray')
    
  #  plt.show()
    
    return img_bw

def arraymirror(img, w,h,B_ch = True):

    #通过循环实现
    #===========================================================================
    # im_mir = np.zeros((h,w))
    # #print h ,w
    # if B_ch:
    #     for x in xrange(w):
    #         flipped_x = w-x-1
    #         for y in xrange(h):
    #             pixel = img[y,x]
    #             im_mir[y,flipped_x] = pixel
    # else:
    #     for y in xrange(h):
    #         flipped_y = h-y-1
    #         for x in xrange(w):
    #             pixel = img[y,x]
    #             im_mir[flipped_y,x] = pixel
    # return im_mir
    #===========================================================================
    #通过矩阵操作实现
    if B_ch:
        return np.fliplr(img)
    else:
        return np.flipud(img)

#===============================================================================
# from skimage import transform as tf   
#  
# def transform_image(img, i,j):
#     #translation = (i,j)
#     #print translation
#     tform = tf.SimilarityTransform(scale =1, rotation = 0, translation=(i,j))
#     rotated = tf.warp(img, tform)
# 
#     return rotated
#===============================================================================
'''
#sample:
path = 'D:/Python_Pg/Image_Classifier/data_new/yumao01_1383.tga'  
image1 = Image.open(path)
im1 = image1.convert("L")

im1_bw = choose_featureregion(array(im1))

path = 'D:/Python_Pg/Image_Classifier/data_new/yumao01_6368.tga'  
image2 = Image.open(path)
im2 = image2.convert("L")

im2_bw = choose_featureregion(array(im2))

im = abs(im1_bw- im2_bw)
print sum(im)
#$plt.show()
import math
import numpy as np
from skimage import transform as tf

tform = tf.SimilarityTransform(scale =1, rotation = 0, translation=(0,50))

#print (tform._matrix)\
rotated = tf.warp(im1_bw, tform)
#plt.imshow(rotated, cmap='gray')
#plt.show()
print rotated.shape
print im1_bw.shape
#im_t = im1_bw&(array(rotated))
from PIL import ImageChops
#im_t = np.logical_and(im1, rotated)
im1.show()
rotatedim1= tf.warp(array(im1), tform)
im_t = rotatedim1*rotated
plt.imshow(im_t, cmap='gray')
plt.show()
'''
'''
path = 'D:/Python_Pg/Image_Classifier/data_test/light136_5567.tga'  
image1 = Image.open(path)
im1 = make_regalur_image(image1)
im1_bw = choose_featureregion(np.array(im1))
path = 'D:/Python_Pg/Image_Classifier/data_test/light133.tga'  
image2 = Image.open(path)
im2 = make_regalur_image(image2)
im2_bw = choose_featureregion(np.array(im2))
#===============================================================================
# plt.subplot(1,2,1)
# plt.imshow(im1_bw, cmap='gray')
# plt.subplot(1,2,2)
# plt.imshow(im2_bw, cmap='gray')
# plt.show()
#===============================================================================
'''
