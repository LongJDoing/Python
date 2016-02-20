#coding=utf-8
'''
Created on 2014��5��13��

@author: Administrator
'''
import wx
from matplotlib.pyplot import *

import extra_var
from numpy import *
import mymath
import cluster_class as myclass
import myimgfunction

def mycopy(clusternode):
    clusternode_copy = []
    for i in xrange(len(clusternode)):
            clusternode_copy.append(myclass.Cluster(clusternode[i].vec, clusternode[i].id, clusternode[i].filename))
    return clusternode_copy



import os

def Onsaveall(ClusterNode, path1, path2, path3, path4, path5, path6, path9, path10,trainernode, trainerid):
        
        #print extra_var.Part0_ID,extra_var.Part1_ID, extra_var.Part9_ID,extra_var.Part2_ID,extra_var.Part10_ID
        #print extra_var.Part3_ID,extra_var.Part4_ID, extra_var.Part5_ID,extra_var.Part6_ID,extra_var.Part7_ID, extra_var.Part8_ID
        progressMax = 100
        processdlg =  wx.ProgressDialog(u"图像保存中...", u"剩余时间", progressMax,
                    style=wx.PD_AUTO_HIDE | wx.PD_APP_MODAL)
        fig = figure()
        Leafpath = os.getcwd()
        for c in xrange(extra_var.cluster_ID+1):
            ind = []
            for n in xrange(len(ClusterNode)):
                if (ClusterNode[n].extract_clusters_id() == c):
                    ind.append([ClusterNode[n].get_cluster_elements(), ClusterNode[n].get_cluster_filename()])
            for id in xrange(5):
                iind = []
                for i in xrange(len(ind)):
                    if (i < (id+1)*40) &(i >= id*40):
                        iind.append([ind[i][0], ind[i][1]])

                b_is = False
                #print len(ind)
                all_text = ''
                for i in xrange(minimum(len(iind),40)):
                    im = iind[i][0]
                    #print ind[i]
                    ax = fig.add_subplot(10,4, i+1)
                    ax.autoscale_view(True, True, True)
                    if c == extra_var.Part0_ID:
                        lef = extra_var.smallregion0[iind[i][1]]
                        rig = extra_var.smallregion1[iind[i][1]]
                        wid = extra_var.smallregionw[iind[i][1]]
                        hei = extra_var.smallregionh[iind[i][1]]
                        rect1 = matplotlib.patches.Rectangle( (lef,rig), width = wid, height=hei,
                                     facecolor='None', edgecolor='green')
                        ax.add_patch(rect1)
                        w,h = iind[i][0].size
                        rect2 = matplotlib.patches.Rectangle((0,0), width = w, height=h,
                                    facecolor='None', edgecolor='blue')
                        ax.add_patch(rect2)
                        
                    imshow(array(im), cmap ='gray',filternorm = 1, aspect='auto')
                    #print ind[i][1]
                    ax.set_title(iind[i][1], fontsize = 2.5)
                    axis('equal')
                    axis('off')
                    
                    # д���ļ���
                    myfilename = iind[i][1] + '\n'
                    all_text += myfilename
                    #print all_text
                    b_is = True
                if b_is:
                    
                    for it in xrange(len(trainernode)):
                        if len(trainernode[it]):
                            for ic in xrange(len(trainernode[it])):
                                if c == trainernode[it][ic][0]:                                                                                    
                                    path = Leafpath+ "/result/" + str(extra_var.name) + "/trainer_cluster/" + trainernode[it][ic][1]+'/'
                                    filename = path +'%d'%ic + '_%d.png'%id
                                    fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                                    
                                    txtfilename = path + '%d'%ic + '_%d.txt'%id                                    #print txtfilename
                                    f = open(txtfilename, 'w')
                                    f.write(all_text.encode('utf8'))
                                    f.close()
                                    clf()

                    if c not in  trainerid:
                        if (c == extra_var.Part0_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path1 + s +'_%d.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                            
                            txtfilename = path1 + s +'_%d.txt'%id
                            f = open(txtfilename, 'w')
                            f.write(all_text.encode('utf8'))
                            f.close()   
                        elif (c > extra_var.Part0_ID)and(c <= extra_var.Part1_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path2 + s +'_%d.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                            
                            txtfilename = path2 + s +'_%d.txt'%id
                            f = open(txtfilename, 'w')
                            f.write(all_text.encode('utf8'))
                            f.close()
                            
                        elif (c > extra_var.Part1_ID)and(c <= extra_var.Part9_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path9 + s +'_%d.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                            
                            txtfilename = path9 + s +'_%d.txt'%id
                            f = open(txtfilename, 'w')
                            f.write(all_text.encode('utf8'))
                            f.close()
                        elif (c > extra_var.Part9_ID)and(c <= extra_var.Part2_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path4 + s +'_%d.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                            
                            txtfilename = path4 + s +'_%d.txt'%id
                            f = open(txtfilename, 'w')
                            f.write(all_text.encode('utf8'))
                            f.close()
                        elif (c <= extra_var.Part10_ID) and(c > extra_var.Part2_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            
                            filename = path10 + s +'_%d.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                            
                            txtfilename = path10 + s +'_%d.txt'%id
                            f = open(txtfilename, 'w')
                            f.write(all_text.encode('utf8'))
                            f.close()
    
                        elif (c <= extra_var.Part3_ID) and (c > extra_var.Part10_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path3 + s +'_%d.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                            
                            txtfilename = path3 + s +'_%d.txt'%id
                            f = open(txtfilename, 'w')
                            f.write(all_text.encode('utf8'))
                            f.close()
    
                        elif (c <= extra_var.Part4_ID) and (c > extra_var.Part3_ID) :
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path5 + s +'_%d.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                            
                            txtfilename = path5 + s +'_%d.txt'%id
                            f = open(txtfilename, 'w')
                            f.write(all_text.encode('utf8'))
                            f.close()
    
                        elif (c <= extra_var.Part5_ID) and(c > extra_var.Part4_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path3 + s +'_%d.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                            
                            txtfilename = path3 + s +'_%d.txt'%id
                            f = open(txtfilename, 'w')
                            f.write(all_text.encode('utf8'))
                            f.close()
    
                        elif (c <= extra_var.Part6_ID) and (c > extra_var.Part5_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path5 + s +'_%d.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                            
                            txtfilename = path5 + s +'_%d.txt'%id
                            f = open(txtfilename, 'w')
                            f.write(all_text.encode('utf8'))
                            f.close()
    
                        elif (c <= extra_var.Part7_ID) and (c > extra_var.Part6_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path3 + s +'_%d.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                            
                            txtfilename = path3 + s +'_%d.txt'%id
                            f = open(txtfilename, 'w')
                            f.write(all_text.encode('utf8'))
                            f.close()
    
                        elif (c <= extra_var.Part8_ID) and (c > extra_var.Part7_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path5 + s +'_%d.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                            
                            txtfilename = path5 + s +'_%d.txt'%id
                            f = open(txtfilename, 'w')
                            f.write(all_text.encode('utf8'))
                            f.close()
    
                        else:
                            pass
                    clf()
                
                for i in xrange(minimum(len(iind),40)):
                    im = iind[i][0]
                    im_gray = myimgfunction.make_regalur_image(im, B_Ch=True, B_is=False)
                    ax = fig.add_subplot(10,4, i+1)
                    ax.autoscale_view(True, True, True)
                    if c == extra_var.Part0_ID:
                        lef = extra_var.smallregion0[iind[i][1]]
                        rig = extra_var.smallregion1[iind[i][1]]
                        wid = extra_var.smallregionw[iind[i][1]]
                        hei = extra_var.smallregionh[iind[i][1]]
                        rect1 = matplotlib.patches.Rectangle( (lef,rig), width = wid, height=hei,
                                     facecolor='None', edgecolor='green')
                        ax.add_patch(rect1)
                        w,h = iind[i][0].size
                        rect2 = matplotlib.patches.Rectangle((0,0), width = w, height=h,
                                    facecolor='None', edgecolor='blue')
                        ax.add_patch(rect2)
                    imshow((im_gray), cmap ='gray',filternorm = 1, aspect='auto')
                    #print ind[i][1]
                    ax.set_title(iind[i][1], fontsize = 2.5)
                    axis('equal')
                    axis('off')
                    
                if b_is:
                    
                    for it in xrange(len(trainernode)):
                        if len(trainernode[it]):

                            for ic in xrange(len(trainernode[it])):
                                if c == trainernode[it][ic][0]:                                                                                    
                                    path = Leafpath+ "/result/" + str(extra_var.name) + "/trainer_cluster/" + trainernode[it][ic][1]+'/'
                                    filename = path +'%d'%ic + '_%dgray.png'%id
                                    fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                                    clf()

                    if c not in  trainerid:
                        if (c == extra_var.Part0_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path1 + s +'_%dgray.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
    
                        elif (c > extra_var.Part0_ID)and(c <= extra_var.Part1_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path2 + s +'_%dgray.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                        elif (c > extra_var.Part1_ID)and(c <= extra_var.Part9_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path9 + s +'_%dgray.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
    
                        elif (c > extra_var.Part9_ID)and(c <= extra_var.Part2_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path4 + s +'_%dgray.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                            
                        elif (c <= extra_var.Part10_ID) and(c > extra_var.Part2_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path10 + s +'_%dgray.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
    
                        elif (c <= extra_var.Part3_ID) and (c > extra_var.Part10_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path3 + s +'_%dgray.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
    
    
                        elif (c <= extra_var.Part4_ID) and (c > extra_var.Part3_ID) :
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path5 + s +'_%dgray.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
    
                        elif (c <= extra_var.Part5_ID) and(c > extra_var.Part4_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path3 + s +'_%dgray.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
    
                        elif (c <= extra_var.Part6_ID) and (c > extra_var.Part5_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path5 + s +'_%dgray.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
    
                        elif (c <= extra_var.Part7_ID) and (c > extra_var.Part6_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path3 + s +'_%dgray.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
    
                        elif (c <= extra_var.Part8_ID) and (c > extra_var.Part7_ID):
                            s = str(c)
                            if len(s) == 1:
                                s = '00'+ s
                            if len(s) ==2:
                                s ='0'+s
                            filename = path5 + s +'_%dgray.png'%id
                            fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
    
                        else:
                            pass
                    clf()
            processdlg.Update(c*100/(extra_var.cluster_ID+1))        
        
        delindex = []
        for i in xrange(len(extra_var.ImageLeafNode)):
            for j in xrange(len(ClusterNode)):
                if extra_var.ImageLeafNode[i].vec == ClusterNode[j].vec:
                    delindex.append(i)
        ImageLeafNode = mycopy(extra_var.ImageLeafNode)
        ImageLeafNode= mymath.multi_list_del(ImageLeafNode, delindex)
        
        #print len(ImageLeafNode)
        '''保存未聚类的'''
        fig = figure() 
        for c in xrange(25):
            
            b_is = False
            ind = []
            all_text = ''

            for i in xrange(len(ImageLeafNode)):  
                if (i < (c+1)*40) &(i >= c*40):
                    ind.append([ImageLeafNode[i].vec, ImageLeafNode[i].filename])
            
            for i in xrange(minimum(len(ind),40)):
                
                im = ind[i][0]
                ax = fig.add_subplot(10, 4, i+1)
                imshow(array(im), cmap ='gray',filternorm = 1, aspect='auto')
                ax.set_title(ind[i][1], fontsize =2.5)
                axis('equal')
                axis('off')
                b_is = True
                myfilename = ind[i][1] + '\n'
                all_text += myfilename
            
            if (b_is):
                s = str(c)
                if len(s) == 1:
                    s = '00'+ s
                if len(s) ==2:
                    s ='0'+s
                filename = path6 + s+'.png'
                fig.savefig(filename, bbox_inches='tight', dpi = 300, encoding='utf-8')
                
                txtfilename = path6 + s +'.txt'
                f = open(txtfilename, 'w')
                f.write(all_text.encode('utf8'))
                f.close()
            
            clf()

            for i in xrange(minimum(len(ind),40)):
                
                im = ind[i][0]
                im_gray = myimgfunction.make_regalur_image(im, B_Ch=True, B_is=False)
                ax = fig.add_subplot(10, 4, i+1)
                imshow((im_gray), cmap ='gray',filternorm = 1, aspect='auto')
                ax.set_title(ind[i][1], fontsize =2.5)
                axis('equal')
                axis('off')
            
            if (b_is):
                
                s = str(c)
                if len(s) == 1:
                    s = '00'+ s
                if len(s) ==2:
                    s ='0'+s
                filename = path6 + s +'gray.png'
                fig.savefig(filename, bbox_inches='tight', dpi=300) 
            clf()

        import mysaveexcel
        mysaveexcel.mysavexls()
        import mytrainerexcel
        mytrainerexcel.mysavexls()
        print u"图像保存完成!"
        processdlg.Destroy()