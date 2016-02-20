#coding=utf-8
'''
Created on 2014��4��24��

@author: Administrator
'''
import numpy as np
from skimage.morphology import  disk,  dilation
from scipy import ndimage
#from skimage.feature import peak_local_max
import extra_var
import myimportimg
import re
def impxml():
    xmllist = myimportimg.get_xmllist(extra_var.xmlpath)
    
    imgname = []
    framecount = []
    
    for i, f in enumerate(xmllist):
        fp = open(f)
        xmlid = []
        for eachline in fp:
            xmlid.append(eachline)
    
        fp.close()
        #print f
        for n in xrange(len(xmlid)):
            if 'textureName_' in xmlid[n]:
                str = re.sub('\<.*?\>','', xmlid[n])
                str = str.replace(' ', '')
                text = str.split('/')
                tex = text[len(text)-1]
                text = tex.replace('\t','')
                text = text.replace('\n','')
                if text not in imgname:
                    imgname.append(unicode(text, "UTF-8"))
                    str = re.sub('\<.*?\>','', xmlid[n+1])
                    str = str.replace(' ', '')
                    num = str.split('/')
                    tex = num[len(num)-1]
                    num = tex.replace('\t','')
                    num = num.replace('\n','')
                    #print text, num
                    
                    framecount.append(float(num))        
    return imgname, framecount
 
def getregions_count(img, filename, imgname, framecount):

    if "xulie"  in filename:
        return 2
    if "xuelie" in filename:
        return 2
    text = filename.split('\\')
    text = text[len(text)-1]
    #print repr(text)
    #print imgname
    try:
        index = imgname.index(text)
        #print index, framecount[index]
        #print framecount[160], imgname[291], imgname[160]
        if framecount[index] >= 4:
            #print "YES"
            return 2
        if (framecount[index]) == 0.0 or ((framecount[index] < 4) and (framecount[index] >= 1)):
            #print 'No'
            return 1
    except:
            
        image = img.convert("L")
        if len(img.getbands()) == 4:
            ir,ig,ib,ia = img.split()
            im_a = np.array(ia).flatten()
            im_av = np.var(im_a)
            im = np.array(image).flatten()
            im_v = np.var(im)
            if abs(im_av) <  abs(im_v):
                image = image
            else:
                image = ia   
        else:
            image = image
        #image = image.resize((64,64))
        
        w,h = image.size
        im = np.array(image)    
        im[im > 0] = 1
        im = dilation(im, disk(1))
    
        labels, count = ndimage.label(im)
        ind = np.zeros(count)
        for i in xrange(count):
            ind[i] = np.sum(labels==i+1)
        ind = sorted(ind, reverse=True)
    
        tmp = ind[0]/sum(ind)
        if tmp > 0.5:  #有很大的概率，它是单纹理的图像，经过测试，效果不错
            im1 = np.ones((h,w))
            #im1[im1>0] = 1
            im1 = im1 - im
            labels, count = ndimage.label(im1)
            ind = np.zeros(count)
            for i in xrange(count):
                ind[i] = np.sum(labels==i+1)
            if not ind.size:
                return 1
            ind = sorted(ind, reverse=True)
    
            tmp = ind[0]/sum(ind)
            if tmp > 0.2:
                return 1
            n = sum(np.asarray(ind) > 50)
            if n < 9:
                return 1
            if ind[8]/ind[0] > 0.2:
                return 2
            else:
                return 1
        else:
            n = sum(np.asarray(ind) > 200)
            if n < 3:
                return 1
            tmp =  sum(ind[1:n])/(n-1) # 第一个一般都是融合到一起的，因此把第一个加进去的话，不准确
            n = sum(np.asarray(ind) > tmp)
            if n < 3:
                return 1
            if (ind[n-1]/ind[n-2] > 0.8)&(ind[n-3]/ind[n-2] > 0.4) &(ind[1]/ind[0] > 0.4):
                return 2
            else:
                return 1
        
'''
#sample
path = 'D:/Python_Pg/Image_Classifier/data_new/2911_paopao3.tga'
image = Image.open(path)
print getregions_count(image)
'''