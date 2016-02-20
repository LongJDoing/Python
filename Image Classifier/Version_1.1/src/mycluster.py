#coding=utf-8
'''
Created on 2014年4月24日

@author: Administrator
'''
import mycluster_1
import cluster_class as myclass
import mymath
import myimportimg
import extra_var
from PIL import Image
from numpy import *
import myregion_count
import myimgfunction as myif
import skimage.feature

''' 此部分的函数执行2个分类过程
        1. 提取特征非常小的一些图像，把它们的ID设置为0
        2. 提取均匀图像，把它们的ID设置为1
    '''


def ReadImg():
    
    imlist = myimportimg.get_imlist(extra_var.path) # 导入图像文件的路径

    extra_var.ImageLeafNode = []
    iimlist =[]
    for i in xrange(len(imlist)):
        if (u'_n.bmp' not in imlist[i]) and( u'_d.bmp' not in imlist[i]) and (u'_s.bmp' not in imlist[i]) and (u'_f.bmp' not in imlist[i]):
            iimlist.append(imlist[i])
    

    for i in xrange(len(iimlist)):
        fp = open(iimlist[i], 'rb')
        image = Image.open(fp)
        image.convert('L') # 添加这段代码，才能work
        #image.show()
        #image = image.load()
        extra_var.ImageLeafNode.append(myclass.Cluster(image, -1, iimlist[i]))
        fp.close()
    #print len(extra_var.ImageLeafNode)
    # 需要讨论
    #===========================================================================
    # repfile = []
    # for i in range(len(ImageLeafNode)-1): 
    #     if i not in repfile:
    #         f = ImageLeafNode[i].filename
    #         s = f.split('\\')
    #         s1 = s[len(s)-1]
    #         #print s1
    #     for j in range(i+1, len(ImageLeafNode)):
    #         if j not in repfile:
    #             f = ImageLeafNode[j].filename
    #             s = f.split('\\')
    #             s2 = s[len(s)-1]
    #             #print s2
    #             if s1 == s2:
    #                 repfile.append(j)
    #===========================================================================
    #print len(ImageLeafNode), (len(repfile))
    #extra_var.ImageLeafNode = mymath.multi_list_del(ImageLeafNode, repfile)
    #print len(extra_var.ImageLeafNode)
def Calreg(im, w, h):
    #image.show()
    index = where(im > extra_var.SmallRegion_par0)[0] # 根据我的肉眼来设置
    #print index
    if not index.size:
        return 0
    #print index
    w0 = index%w
    maxw = max(w0)
    minw = min(w0)
    h0 = index/w
    maxh = max(h0)
    minh = min(h0)
    reg =  (maxh-minh+1)*(maxw-minw+1)
    #print float(nuclear)/(w*h)
    return float(reg)/(w*h), minw, minh, (maxw-minw), (maxh-minh)
def Cluster_1():
    
    #import time
    #timestart = time.time()
    ReadImg()
    extra_var.ClusterNode2 = []
    extra_var.ClusterNode0 = []
    for i in xrange(len(extra_var.ImageLeafNode)):
        f = extra_var.ImageLeafNode[i].filename
        image = extra_var.ImageLeafNode[i].vec
        w, h = image.size
        image = myif.make_regalur_image(image, B_is=False)
        im = image.flatten()
        tmp = var(im)
        if tmp <=  1.0e-5:
            continue
        tmp, minw, minh, rw,rh = Calreg(im, w, h)
        #print tmp, minw, minh, rw,rh
      
        if (tmp < extra_var.SmallRegion_par):
            extra_var.cluster_ID = 0
            extra_var.Part0_ID = 0
            new_node = myclass.Cluster(extra_var.ImageLeafNode[i].vec, extra_var.cluster_ID, f)
            extra_var.ClusterNode0.append(new_node)   
            extra_var.smallregion0[f] =  minw
            extra_var.smallregion1[f] =  minh
            extra_var.smallregionw[f] =  rw
            extra_var.smallregionh[f] =  rh

    
    for i in xrange(len(extra_var.ImageLeafNode)):
        for j in xrange(len(extra_var.ClusterNode0)):
            if extra_var.ImageLeafNode[i].vec == extra_var.ClusterNode0[j].vec:
                extra_var.ImageLeafNode[i].id = 0
    
   # print repfile
    #timeend = time.time()
    #print len(extra_var.ImageLeafNode)
    #print timeend-timestart

'''
         区别出序列纹理和单独纹理，从而将整个纹理库区分为2类 
    
'''
def Classify():
    ''''''
    '''添加训练器的图像路径'''
    length = len(extra_var.choosetrainer)
    for i in xrange(length):
        ind = extra_var.choosetrainer[i]
        path = extra_var.alltrainer[ind][1]
        extra_var.inittrainerimlist[i] = myimportimg.get_imlist(path)
        #print len(extra_var.trainerimlist[i])
    trainerNode = []
    imlist = []
    for i in xrange(len(extra_var.inittrainerimlist)):
        #print len(extra_var.trainerimlist[i])
        imlist += extra_var.inittrainerimlist[i]

    for i in xrange(len(imlist)):
        fp = open(imlist[i], 'rb')
        image = Image.open(fp)
        image.convert('L') # 添加这段代码，才能work
        #image.show()
        #image = image.load()
        trainerNode.append(myclass.Cluster(image, -1, imlist[i]))
        fp.close()
    
    imgname, framecount = myregion_count.impxml()

    extra_var.trainerarrayLeafNode =[]   
    extra_var.trainersingleLeafNode =[]    
   
    for i, imgleafnode in enumerate(trainerNode):
        if imgleafnode.id == -1:
            label_counts = myregion_count.getregions_count(imgleafnode.vec, imgleafnode.filename, imgname, framecount)
            
            if label_counts > 1:
                extra_var.trainerarrayLeafNode.append(myclass.Cluster(imgleafnode.vec, imgleafnode.id, imgleafnode.filename))
            else:
                extra_var.trainersingleLeafNode.append(myclass.Cluster(imgleafnode.vec, imgleafnode.id, imgleafnode.filename))


    
    
    extra_var.ImagearrayLeafNode = []
    extra_var.ImagesingleLeafNode = []
    for i, imgleafnode in enumerate(extra_var.ImageLeafNode):
        if imgleafnode.id == -1:
            label_counts = myregion_count.getregions_count(imgleafnode.vec, imgleafnode.filename, imgname, framecount)
            
            if label_counts > 1:
                extra_var.ImagearrayLeafNode.append(myclass.Cluster(imgleafnode.vec, imgleafnode.id, imgleafnode.filename))
            else:
                extra_var.ImagesingleLeafNode.append(myclass.Cluster(imgleafnode.vec, imgleafnode.id, imgleafnode.filename))
    extra_var.ImagearrayLeafNode += extra_var.trainerarrayLeafNode
    extra_var.ImagesingleLeafNode += extra_var.trainersingleLeafNode
'''
       对纹理，首先直接比较来分形状相同，颜色不同
'''

'''对完全相同的图像进行一个聚类'''
def getvarcluster(ImageLeafNode, ClusterNode, cluster_ID):


    ImageLeafNode, m_leafID = ratiocluster(ImageLeafNode)
    
    for i in xrange(m_leafID): 
        m_ImageNode = []
        for index, imgleafnode in enumerate(ImageLeafNode):
            if imgleafnode.id == i:
                m_ImageNode.append(imgleafnode)

        if len(m_ImageNode) >=2:
            ClusterNode, cluster_ID = mycluster_1.var_cluster(m_ImageNode, ClusterNode, cluster_ID, thr=1.0e-5)
    return ClusterNode, cluster_ID

def Cluster_Same(ImageLeafNode, ClusterNode, cluster_ID):
    
    
    ClusterNode, cluster_ID = getvarcluster(ImageLeafNode, ClusterNode, cluster_ID)   
    
    delindex = []
    
    for i in xrange(len(ImageLeafNode)):
        for j in xrange(len(ClusterNode)):
            if ImageLeafNode[i].vec == ClusterNode[j].vec:
                delindex.append(i)
    
    ImageLeafNode= mymath.multi_list_del(ImageLeafNode, delindex)
    
    #ImageLeafNode, m_leafID = ratiocluster(ImageLeafNode)
    return ImageLeafNode, ClusterNode, cluster_ID

'''
    针对纹理，具有镜像特性的进行分类
    
'''

def getmirrorcluster(ImageLeafNode, ClusterNode, cluster_ID):
    ImageLeafNode, m_leafID = ratiocluster(ImageLeafNode)
    
    for i in xrange(m_leafID): 
        m_ImageNode = []
        for index, imgleafnode in enumerate(ImageLeafNode):
            if imgleafnode.id == i:
                m_ImageNode.append(imgleafnode)

        if len(m_ImageNode) >=2:
            ClusterNode, cluster_ID = mycluster_1.mirror_cluster(m_ImageNode, ClusterNode, cluster_ID, thr=1.0e-5)
    return ClusterNode, cluster_ID


def Cluster_Mirror(ImageLeafNode, ClusterNode, cluster_ID):
    
    ClusterNode, cluster_ID = getmirrorcluster(ImageLeafNode, ClusterNode, cluster_ID)
    delindex = []
    
    for i in xrange(len(ImageLeafNode)):
        for j in xrange(len(ClusterNode)):
            if ImageLeafNode[i].vec == ClusterNode[j].vec:
                delindex.append(i)
    
    ImageLeafNode= mymath.multi_list_del(ImageLeafNode, delindex)    

    ImageLeafNode, m_leafID = ratiocluster(ImageLeafNode)
    
    return ImageLeafNode, ClusterNode, cluster_ID, m_leafID



'''
            根据长宽比，进行分类； 此基于假设：纹理库当中，同一类的图像应该具有相同的长宽比
    ImageLeafNode 输入时候，id=-1,分类后从0开始
'''
def ratiocluster(ImageLeafNode):
    m_ratios = {}
    id = 0
    for i, imgleafnode in enumerate(ImageLeafNode):
        w,h = imgleafnode.vec.size
        m_ratio = float(w) / h
        if m_ratio not in m_ratios:
            m_ratios[m_ratio] = id
            ImageLeafNode[i].id = id
            id += 1
        else:
            ImageLeafNode[i].id = m_ratios[m_ratio]    
    
    m_leafID = id # 根节点依据长宽比的分类数目
    return ImageLeafNode, m_leafID




'''==============================================================================================================='''

'''
 对根节点的每一类，做依赖于图像之差的方差进行第一步的分类
'''
def varcluster(ImageLeafNode, ClusterNode, cluster_ID, m_leafID):  
              
    last_cluster_ID = cluster_ID
    
    #print cluster_ID    

    for i in xrange(m_leafID): 
        m_ImageNode = []
        for index, imgleafnode in enumerate(ImageLeafNode):
            #print imgleafnode.id
            if imgleafnode.id == i:
                m_ImageNode.append(imgleafnode)
        
        if len(m_ImageNode) >2:
            
            ClusterNode, cluster_ID = mycluster_1.var_hcluster(m_ImageNode, ClusterNode, cluster_ID)
        if len(m_ImageNode) == 2:
            ClusterNode, cluster_ID = mycluster_1.var_cluster(m_ImageNode, ClusterNode, cluster_ID, thr = 5000)

    '''找到未聚类的图像，同时从已聚类的图像中选择一个作为特征图像'''
    Add_ClusterNode =[]
    
    for i in xrange(last_cluster_ID, cluster_ID):
        for j in xrange(len(ClusterNode)):
            if ClusterNode[j].id == i+1: #需要加1，来保证一致
                Add_ClusterNode.append(myclass.Cluster(ClusterNode[j].vec, ClusterNode[j].id, ClusterNode[j].filename))
                break
        
    for i in xrange(cluster_ID-last_cluster_ID):
        for j in xrange(len(ImageLeafNode)):
            if ImageLeafNode[j].vec == Add_ClusterNode[i].vec:
                Add_ClusterNode[i].id = ImageLeafNode[j].id

    for i in xrange(len(ImageLeafNode)):
        for j in xrange(len(ClusterNode)):
            if ImageLeafNode[i].vec == ClusterNode[j].vec:
                ImageLeafNode[i].id = -1
                
     
    for i in xrange(cluster_ID-last_cluster_ID):
        for j in xrange(len(ImageLeafNode)):
            if ImageLeafNode[j].vec == Add_ClusterNode[i].vec:
                ImageLeafNode[j].id = Add_ClusterNode[i].id
    
    #cluster_ID = 0    
    #for i in range(len(ClusterNode)):
        #if cluster_ID < ClusterNode[i].id:
            #cluster_ID = ClusterNode[i].id
    #print cluster_ID
    
    return ImageLeafNode, ClusterNode, cluster_ID, Add_ClusterNode 
    
'''
    对根节点的每一类，依赖于图像的形状信息，做第二部的分类
    
'''    
def regioncluster(ImageLeafNode, ClusterNode, cluster_ID, m_leafID, Add_ClusterNode, lastvalue):  
    
    #m_last_length = len(ClusterNode)
    m_length_var = cluster_ID
    #print cluster_ID
    for i in xrange(m_leafID): 
        m_ImageNode = []
        for index, imgleafnode in enumerate(ImageLeafNode):
            if imgleafnode.id == i:
                
                #print imgleafnode.id, imgleafnode.filename
                m_ImageNode.append(imgleafnode)
                #imgleafnode.vec.show()
        if len(m_ImageNode) > 1:
            #print len(m_ImageNode)
            ClusterNode, cluster_ID = mycluster_1.skeleton_hcluster(m_ImageNode, ClusterNode, cluster_ID)

    #print cluster_ID
    '''合并和删除多余聚类'''
    '''先做一次检查，如果聚成的一类，其里面含有之前的两类，那么就delete'''
    Repeat_im = []
    for i in xrange(len(Add_ClusterNode)):
        Repeat_im.append(Add_ClusterNode[i].filename)
    
    Repeat_ID = []  
    for id in xrange(m_length_var, cluster_ID):
        m_repeat = 0
        for index, imgnode in enumerate(ClusterNode):
            if imgnode.id == id+1:
                if imgnode.filename in Repeat_im:
                    m_repeat += 1
                if m_repeat > 1:
                    if (id+1) not in Repeat_ID:
                        Repeat_ID.append(id+1)
    m_Repeat = []                   
    for id in xrange(len(Repeat_ID)):
        for index, imgnode in enumerate(ClusterNode):
            if imgnode.id == Repeat_ID[id]:
                m_Repeat.append(index)
            elif imgnode.id > Repeat_ID[id]:
                ClusterNode[index].id -= 1
    
    #print m_Repeat
    
    ClusterNode = mymath.multi_list_del(ClusterNode, m_Repeat)  
    
    m_Repeat = []                   
                        
    m_length = len(ClusterNode)
    #print extra_var.Part2_ID, m_length
    #print lastvalue
    dela =[]
    for i in xrange(lastvalue, m_length-1):
        for j in xrange(i+1, m_length):
            if ClusterNode[i].vec == ClusterNode[j].vec:
                for k in xrange(i+1, m_length):
                    if ClusterNode[k].id == ClusterNode[j].id:
                        dela.append(ClusterNode[j].id)
                        if ClusterNode[k].vec != ClusterNode[j].vec:
                            ClusterNode[k].id = ClusterNode[i].id
                        else:
                            #if k not in m_Repeat:
                            m_Repeat.append(k)
                    elif ClusterNode[k].id > ClusterNode[j].id:
                        ClusterNode[k].id = ClusterNode[k].id -1

    ClusterNode = mymath.multi_list_del(ClusterNode, m_Repeat)       

    #print cluster_ID
    #print len(ClusterNode)
    #print dela
    dela = list(set(dela))
    #print dela
    return ImageLeafNode, ClusterNode, cluster_ID, dela
 
 
    
'''
      聚类剩余的Images；使用的算法是PCA+AP

'''
def pca_apcluster(ImageLeafNode, ClusterNode, cluster_ID, m_leafID):
    
    for i in xrange(len(ImageLeafNode)):
        for j in xrange(len(ClusterNode)):
            if ImageLeafNode[i].vec == ClusterNode[j].vec:
                ImageLeafNode[i].id = -1
    
    #print cluster_ID 
    #cluster_ID = 0    
    #for i in range(len(ClusterNode)):
        #if cluster_ID < ClusterNode[i].id:
            #cluster_ID = ClusterNode[i].id
    #print cluster_ID      
    '''Step3 考虑先使用灰度共生矩阵，再利用PCA+Ap聚类'''
    from PIL import ImageFilter
     
    for i in xrange(m_leafID): 
        m_ImageNode1 = []
        m_ImageNode2 = []
    # 
        for index, imgleafnode in enumerate(ImageLeafNode):
            if imgleafnode.id == i:
                im_rg = imgleafnode.vec.convert("L").filter(ImageFilter.CONTOUR)
                g = skimage.feature.greycomatrix(im_rg, [1], [0], levels = 256, symmetric=False, normed = True)
                
                tmp = skimage.feature.greycoprops(g, 'contrast')[0][0]
                if tmp < 1000:
                    m_ImageNode1.append(imgleafnode)
                else:
                    #imgleafnode.vec.show()
                    m_ImageNode2.append(imgleafnode)
        #print len(m_ImageNode1), len(m_ImageNode2)
        if len(m_ImageNode1) > 1:           
            ClusterNode, cluster_ID = mycluster_1.PCA_APcluster(m_ImageNode1, ClusterNode, cluster_ID)
    
        if len(m_ImageNode2) > 1: 
            #print len(m_ImageNode2)          
            ClusterNode, cluster_ID = mycluster_1.PCA_APcluster(m_ImageNode2, ClusterNode, cluster_ID)
    
    return ClusterNode, cluster_ID

'''
新的聚类情况，形状已经判断，完全相同，而且颜色又很接近
'''
import colorsys

def CalculateH(img):
    img = img.resize((64,64))
    if len(img.getbands()) == 4:
        ir,ig,ib,ia = img.split()
    else:
        ir, ig, ib = img.split()
    
    Hdat = []
    Sdat = []
    Vdat = []    
    
    for rd,gn,bl in zip(ir.getdata(),ig.getdata(),ib.getdata()):
        h,l,s = colorsys.rgb_to_hsv(rd/255.,gn/255.,bl/255.)
        Hdat.append(h)
        Sdat.append(l)
        Vdat.append(s)
    meanV = mean(Vdat)
    return Hdat, meanV

def Same(ind):
    
    m_length = len(ind)
    same_cluster =[]
    m_ind = []
    ID = -1
    for i in xrange(m_length):
        if i not in m_ind:
            b_is = True
            H1,meanV1 = CalculateH(ind[i][0])

            for j in xrange(i+1, m_length):
                if j not in m_ind:
                    H2,meanV2 = CalculateH(ind[j][0])
                    tmp = abs(array(H1) - array(H2))
                    meanVtmp = abs(meanV1-meanV2)
                    var_tmp = mean(tmp)                    
                    if var_tmp != 0 :
                        var_tmp = mean(tmp[tmp>0])
                    #print var_tmp , meanVtmp
                    if (var_tmp < extra_var.SimilarColor_par1) and (meanVtmp <extra_var.SimilarColor_par2):  # 需要调
                        if b_is:
                            ID += 1
                            same_cluster.append([ind[i][0], ind[i][1], ID])
                            b_is = False
                        same_cluster.append([ind[j][0], ind[j][1], ID])
                        
                        m_ind.append(j)
    return same_cluster, ID
