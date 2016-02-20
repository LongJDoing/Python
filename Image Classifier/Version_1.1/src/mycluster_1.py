#coding=utf-8
'''
Created on 2014��4��23��

@author: Administrator

function: 
'''
'''
计算两幅图像之差，然后根据方差，来层聚类
'''

import myimgfunction as myif
import myhcluster
#import mymath
import cluster_class as myclass
import numpy as np
import extra_var
import mymath

#from skimage.morphology import skeletonize

'''利用图像的差的方差进行比较来分类；这里是区分颜色不同形状完全相同的图像'''

def var_cluster(m_ImageNode, ClusterNode, cluster_id, thr):
    
    m_length = len(m_ImageNode)
    m_ind = []
    im = []
    
    for i in xrange(m_length):
        im.append(myif.make_regalur_image(m_ImageNode[i].vec, B_Ch=True).flatten())
    for i in xrange(m_length-1):
        if i not in m_ind:
            b_is = True
            im1 = im[i]
            #im1[im1>0] = 1            
            for j in xrange(i+1, m_length):
                if j not in m_ind:
                    im2 = im[j]                    
                    #im2[im2>0] = 1                    
                    #var_tmp = sum(abs(im1-im2))
                    var_tmp = mymath.L2var(im1, im2)

                    #print var_tmp
                    if var_tmp < thr:  # 需要调
                        if b_is:
                            cluster_id += 1                    
                            new_node = myclass.Cluster(m_ImageNode[i].vec, cluster_id, m_ImageNode[i].filename)
                            ClusterNode.append(new_node)
                            b_is = False
                        new_node = myclass.Cluster(m_ImageNode[j].vec, cluster_id, m_ImageNode[j].filename)
                        ClusterNode.append(new_node)
                        m_ind.append(j)
    return ClusterNode, cluster_id

'''
    对镜像图像进行分类
'''
def  mirror_cluster(m_ImageNode, ClusterNode, cluster_id, thr):
    
    m_length = len(m_ImageNode)
    m_ind = []
    im = []
    im2_1 =[]
    im2_2 =[]
    for i in xrange(m_length):
        tmp = myif.make_regalur_image(m_ImageNode[i].vec, B_Ch = True)
        im.append(tmp)
        tmp1 = myif.arraymirror(tmp, 25, 25, B_ch = True)
        im2_1.append(tmp1)
        tmp2 = myif.arraymirror(tmp, 25, 25, B_ch = False)
        im2_2.append(tmp2)
    for i in xrange(m_length-1):
        if i not in m_ind:
            b_is = True
            im1 = im[i]
            #im1[im1>0] = 1            
            for j in xrange(i+1, m_length):
                if j not in m_ind:
                    #im2[im2>0] = 1                    
                    #var_tmp = sum(abs(im1-im2))
                    tp1 = im2_1[j]
                    tp2 = im2_2[j]
                    var_tmp1 = mymath.L2var(im1.flatten(), tp1.flatten())
                    var_tmp2 = mymath.L2var(im1.flatten(), tp2.flatten())
                    var_tmp = min(var_tmp1,var_tmp2)
                    #print var_tmp
                    if var_tmp < thr:  # 需要调
                        if b_is:
                            cluster_id += 1                    
                            new_node = myclass.Cluster(m_ImageNode[i].vec, cluster_id, m_ImageNode[i].filename)
                            ClusterNode.append(new_node)
                            b_is = False
                        new_node = myclass.Cluster(m_ImageNode[j].vec, cluster_id, m_ImageNode[j].filename)
                        ClusterNode.append(new_node)
                        m_ind.append(j)
    return ClusterNode, cluster_id
                            

'''利用图像差的方差聚类函数'''
def var_hcluster(m_ImageNode, ClusterNode, cluster_id):
    m_length = len(m_ImageNode)
    Grays = np.zeros([m_length, 25*25])
    for ind, image in enumerate(m_ImageNode):
        im_rg = myif.make_regalur_image(image.vec)
        #rg_img.show()
        Grays[ind] = im_rg.flatten()
    
    tree = myhcluster.hcluster(Grays)
    
    h = tree.get_height()

    if h < 5:
        ratio = 2.5
    elif h < 10:
        ratio = 0.6
        
    elif h< 20:
        #print "0"
        ratio = 0.8
    else:
        ratio = 0.5*np.math.pow(np.math.e, (-1*((h-20)*(h-20))/extra_var.H_par1)) + extra_var.H_par1_1
    #print extra_var.H_par1
    #print h
    clusters = tree.extract_clusters(float(ratio)/h*tree.distance)
    #print len(clusters)
    
    for c in clusters:
        elements = c.get_cluster_elements()
        nbr_elements = len(elements)
        if nbr_elements > 1:
            cluster_id += 1
            for p in xrange(nbr_elements):
                new_node = myclass.Cluster(m_ImageNode[elements[p]].vec, cluster_id, m_ImageNode[elements[p]].filename)
                ClusterNode.append(new_node)
            
    return ClusterNode, cluster_id

'''计算骨骼线，进行聚类的函数,修改该计算区域来聚类'''
def skeleton_hcluster(m_ImageNode, ClusterNode, cluster_id):
    
    Grays = []
    #m_length = len(m_ImageNode)
    for ind, image in enumerate(m_ImageNode):
        w,h = image.vec.size
        h0 = int(h*64/w)  #因为我开始就对其按照比例，所以这里添加一个比例约束
        im_rg = myif.make_regalur_image(image.vec, size=(64,h0))
        im_b = myif.choose_featureregion(im_rg)
        '''
        #这段代码是使用骨骼线来聚类
        im_sk = skeletonize(im_b)
        w, h = im_sk.shape
        im = np.zeros([w,h])
        for i in range(w):
            for j in range(h):
                if im_sk[i,j] == True:
                    im[i,j] = 255
                else:
                    im[i,j] = 0
        '''
        Grays.append(im_b)
        
    tree = myhcluster.hcluster(Grays, True)
    h = tree.get_height()
    #print len(m_ImageNode), h
    #===========================================================================
    # if h < 5:
    #     ratio = 0.5
    # elif h < 30:
    #     ratio = 0.20
    # else:
    #     ratio = 0.15
    #===========================================================================
    #a = 1.5
    #b = 0.125
    ratio = extra_var.H_par2_1/h + extra_var.H_par2_2    
    #print extra_var.H_par2_1, extra_var.H_par2_2
    clusters = tree.extract_clusters(float(ratio)*tree.distance)

    for c in clusters:
        elements = c.get_cluster_elements()
        nbr_elements = len(elements)
        if nbr_elements > 1:
            cluster_id += 1
            for p in xrange(nbr_elements):
                new_node = myclass.Cluster(m_ImageNode[elements[p]].vec, cluster_id, m_ImageNode[elements[p]].filename)
                ClusterNode.append(new_node)
            
    return ClusterNode, cluster_id


'''PCA+AP 进行聚类'''
#from PCV.tools import  pca
from sklearn.cluster import AffinityPropagation
#from sklearn import metrics

def pca(X):
    """    Principal Component Analysis
        input: X, matrix with training data stored as flattened arrays in rows
        return: projection matrix (with important dimensions first), variance and mean.
    """
    
    # get dimensions
    num_data,dim = X.shape
    
    # center data
    mean_X = X.mean(axis=0)
    X = X - mean_X
    
    if dim>num_data:
        # PCA - compact trick used
        M = np.dot(X,X.T) # covariance matrix
        e,EV = np.linalg.eigh(M) # eigenvalues and eigenvectors
        tmp = np.dot(X.T,EV).T # this is the compact trick
        V = tmp[::-1] # reverse since last eigenvectors are the ones we want
        S = np.sqrt(e)[::-1] # reverse since eigenvalues are in increasing order
        for i in xrange(V.shape[1]):
            V[:,i] /= S
    else:
        # PCA - SVD used
        U,S,V = np.linalg.svd(X)
        V = V[:num_data] # only makes sense to return the first num_data
    
    # return the projection matrix, the variance and the mean
    return V,S,mean_X


def PCA_APcluster(m_ImageNode, ClusterNode, cluster_id):
    
    #print len(m_ImageNode)
    #将其大小扩大到64*64

    immatrix = np.array([myif.make_regalur_image(m_image.vec).flatten() for m_image in m_ImageNode], 'f')
    #print immatrix.shape
    V, S, immean = pca(immatrix)
    #print V
    imnbr = len(m_ImageNode)
    projected = np.array([np.dot(V[1,2], immatrix[i] - immean) for i in xrange(imnbr)]) 

    #print projected
    tpmax = np.amax(abs(projected))
    #print tpmax
    if tpmax < 1.0e-5 or np.isnan(tpmax) or np.isinf(tpmax):
        return ClusterNode, cluster_id
    #print tpmax
    #print projected/tpmax
    af = AffinityPropagation(preference= extra_var.S_par3).fit(projected/tpmax)
    
    cluster_centers_indices = af.cluster_centers_indices_
    
    #if cluster_centers_indices == None:
        #return ClusterNode, cluster_id

    labels = af.labels_
    
    k = len(cluster_centers_indices)
    #print k
    #print len(ClusterNode)
    for c in xrange(k):
        ind = np.where(labels==c)[0]
        if len(ind) > 1:
            cluster_id = cluster_id + 1
            for i in xrange(len(ind)):

                #print cluster_id
                new_node = myclass.Cluster(m_ImageNode[ind[i]].vec, cluster_id, m_ImageNode[ind[i]].filename)
                ClusterNode.append(new_node)
   
    #print len(ClusterNode)
    '''
    #显示，调试代码
    import numpy as np
    from matplotlib.pyplot import *
    #print k
    for c in range(cluster_id-3, cluster_id):
        ind = []
        for n in range(len(ClusterNode)):
            if (ClusterNode[n].extract_clusters_id() == c+1):
                print ClusterNode[n].get_cluster_elements(), ClusterNode[n].get_cluster_filename()
                ind.append([ClusterNode[n].get_cluster_elements(), ClusterNode[n].get_cluster_filename()])
            
        fig = figure()
        b_is = False
        for i in range(np.minimum(len(ind),40)):
            im = ind[i][0]
            #print ind[i]
            ax = fig.add_subplot(10,4, i+1)
            ax.autoscale_view(True, True, True)
    
            imshow(np.array(im), cmap ='gray',filternorm = 1, aspect='auto')
            #print ind[i][1]
            xtext=ax.set_title(ind[i][1], fontsize = 3)
            axis('equal')
            axis('off')
            b_is = True
    show()
    '''
    return ClusterNode, cluster_id

    