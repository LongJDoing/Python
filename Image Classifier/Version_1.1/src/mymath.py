#coding=utf-8
'''
Created on 2014��4��16��

@author: Administrator
'''
from numpy import *
from PIL import Image
import myimgfunction as myf
import math

'''
The first thing you must consider is that the points must represent a rectangular mesh.
 X is a 2D array, Y is a 2D array, and Z is a 2D array. 
 If you have an unstructured cloudpoint, 
 with a single matrix shaped Nx3 (the first column being X, the second being Y and the third being Z)
  then you can't apply this matlab function.
  '''
def gasuuian_curvature(Z):
    Zy,Zx = gradient(Z) #Return the gradient of an N-dimensional array.
    Zxy, Zxx = gradient(Zx)
    Zyy, _ = gradient(Zy)
    K = (Zxx * Zyy - (Zxy ** 2)) /  (1 + (Zx ** 2) + (Zy **2)) ** 2             
        
    return K

def mean_curvature(Z):
    Zy, Zx  = gradient(Z)
    Zxy, Zxx = gradient(Zx)
    Zyy, _ = gradient(Zy)

    H = (Zx**2 + 1)*Zyy - 2*Zx*Zy*Zxy + (Zy**2 + 1)*Zxx
    H = -H/(2*(Zx**2 + Zy**2 + 1)**(1.5))

    return H

def F(a):
    Im1 = Image.new("L",(a.shape[1], a.shape[0]))
    b = array(a).flatten()
    maxx= max(b)
    minx = min(b)
    for i in xrange(a.shape[0]):
        for j in xrange(a.shape[1]):
            pix = 255*(a[i][j]-minx)/(maxx+1)
            Im1.putpixel((j,i), int(pix))
    return Im1

def multi_list_del(target, to_delete):
    
    to_delete = sorted(to_delete, reverse=False)
    for offset, index in enumerate(to_delete):
        #print offset, index
        index -= offset
        #print target[index]
        del target[index]
    return target


def L2var(v1, v2):
    '''使用方差来进行分类'''
    v =  abs(v1-v2)
        
    m_v = v[v>0]
    #print m_v.size
    if m_v.size:
        return var(m_v)
    else:
        return var(v)
    #print mint
    '''
    for i in range(3):
        for j in range(3):
            v2_ts = myf.transform_image(v2, i, j)
            v2_f = v2_ts.flatten()
            
            tmp = abs(v1_f-v2_f)
            var_tmp = re_var(tmp)
            #print var_tmp
            if mint >var_tmp:
                mint = var_tmp
    '''

#===============================================================================
# def L2region(v1, v2):
#     '''利用区域面积的差大小来分类'''
#     v1_f = v1.flatten()
#     v2_f = v2.flatten()
#     vtp = sum(abs(v1_f-v2_f))
#     mint = vtp
#     for i in range(3):
#         for j in range(3):
#             v2_ts = myf.transform_image(v2, i, j)
#             v2_f = v2_ts.flatten()
#             
#             tmp = sum(abs(v1_f-v2_f))
#             #print var_tmp
#             if mint >tmp:
#                 mint = tmp
#     return mint
#===============================================================================