#coding=utf-8
'''
Created on 2014��5��5��

@author: Administrator
'''
'''
一步一步聚类图像：
 1. 导出2类：A.均匀图像类， iD = 0  B.特征区域很小的类  iD = 1
 2. 根据长宽比，先将图像进行分类；然后按照2步执行
          A.利用图像之差的数组，计算方差，层聚类； B.计算图像的骨骼线，计算差，层聚类
 3. 计算灰度共生矩阵，按照contrast信息进行分类，然后按照PCA+AP聚类 
'''

import os
import time
import wx
#from matplotlib.pyplot import *
#from numpy import *

import extra_var
import mycluster
import myimportimg
import cluster_class as myclass
import mychild_gui1 as child1
import mychild_gui2 as child2

#import myimgfunction
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.FRAME_TOOL_WINDOW
        wx.Frame.__init__(self, *args, **kwds)
        self.button_1 = wx.Button(self, -1, u"选择XML目录")
        self.button_2 = wx.Button(self, -1, u"选择图像目录") 
        self.button_4 = wx.Button(self, -1, u"选择训练器") 
        self.button_5 = wx.Button(self, -1, u"显示训练器的类")       
        self.sizer_1_staticbox = wx.StaticBox(self, -1, u"训练器")
        self.sizer_20_staticbox = wx.StaticBox(self, -1, u"导入")
        self.text_ctrl_1 = wx.TextCtrl(self, -1, str(extra_var.SmallRegion_par))
        self.text_ctrl_7 = wx.TextCtrl(self, -1, str(extra_var.SmallRegion_par0))
        self.sizer_21_staticbox = wx.StaticBox(self, -1, u"设置特征区域非常小的灰度阈值和比较阈值")
        self.text_ctrl_2 = wx.TextCtrl(self, -1, str(extra_var.SimilarColor_par1))
        self.text_ctrl_3 = wx.TextCtrl(self, -1, str(extra_var.SimilarColor_par2))
        self.sizer_29_staticbox = wx.StaticBox(self, -1, u"设置颜色相似参数H,V")
        self.button_3 = wx.Button(self, -1, u"开始聚类")
        self.sizer_30_staticbox = wx.StaticBox(self, -1, u"聚类开始")
        self.sizer_2_staticbox = wx.StaticBox(self, -1, u"显示训练器类")
        self.label_1 = wx.StaticText(self, -1, u"\n1. 设置特征区域的阈值范围0-1，阈值越\n小，越严格;\n-------------------------------------\n2. 颜色相似第一个参数标示颜色，第二个\n参数标示亮度，越小越严格;\n-------------------------------------\n3. 聚类参数1越大，类越容易分离;\n-------------------------------------\n4. 聚类参数2中A,B越大，越容易聚合;\n-------------------------------------\n5. 聚类参数1和2，一般不需要调;\n-------------------------------------\n6. 聚类参数3越小；越容易聚类，聚类越不\n精确;\n")
        self.sizer_24_staticbox = wx.StaticBox(self, -1, u"提示")
        self.text_ctrl_4 = wx.TextCtrl(self, -1, str(extra_var.H_par1))
        self.text_ctrl_8 = wx.TextCtrl(self, -1, str(extra_var.H_par1_1))

        self.sizer_26_staticbox = wx.StaticBox(self, -1, u"聚类参数1")
        self.text_ctrl_5 = wx.TextCtrl(self, -1, str(extra_var.H_par2_1))
        self.text_ctrl_6 = wx.TextCtrl(self, -1, str(extra_var.H_par2_2))
        self.sizer_31_staticbox = wx.StaticBox(self, -1, u"聚类参数2")
        self.slider_1 = wx.Slider(self, -1, -50, -100, 0, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.sizer_32_staticbox = wx.StaticBox(self, -1, u"聚类参数3")
        self.sizer_25_staticbox = wx.StaticBox(self, -1, u"聚类参数设置")
        self.sizer_7_staticbox = wx.StaticBox(self, -1, u"聚类")

        
        self.__set_properties()
        self.__do_layout()
        self.Center()
        # end wxGlade
        '''
        '''
        self.button_1.Bind(wx.EVT_BUTTON, self.OnOpenXMLPath, self.button_1)
        self.button_2.Bind(wx.EVT_BUTTON, self.OnOpenPath, self.button_2)
        self.text_ctrl_1.Bind(wx.EVT_TEXT, self.GetSmallP, self.text_ctrl_1)
        self.text_ctrl_2.Bind(wx.EVT_TEXT, self.GetSimilarP1, self.text_ctrl_2)
        self.text_ctrl_3.Bind(wx.EVT_TEXT, self.GetSimilarP2, self.text_ctrl_3)

        self.text_ctrl_4.Bind(wx.EVT_TEXT, self.GetP1, self.text_ctrl_4)
        self.text_ctrl_8.Bind(wx.EVT_TEXT, self.GetP1_1, self.text_ctrl_8)

        self.text_ctrl_5.Bind(wx.EVT_TEXT, self.GetP2_1, self.text_ctrl_5)
        self.text_ctrl_6.Bind(wx.EVT_TEXT, self.GetP2_2, self.text_ctrl_6)
        self.text_ctrl_7.Bind(wx.EVT_TEXT, self.GetSmallP0, self.text_ctrl_7)

        self.button_3.Bind(wx.EVT_BUTTON, self.OnCluster, self.button_3)
        self.slider_1.Bind(wx.EVT_SLIDER, self.OnGetP3, self.slider_1)
        self.button_4.Bind(wx.EVT_BUTTON, self.OnOpenTrainer, self.button_4)
        self.button_5.Bind(wx.EVT_BUTTON, self.OnShowTrainer, self.button_5)

    def OnOpenTrainer(self, event):
        pos = self.GetPosition()
        #print pos
        dialog = child1.MyFrame1(self,-1)
        dialog.Show()
        #print dialog
        dialog.SetPosition(((pos[0],pos[1])))
        
    def OnShowTrainer(self, event):
       
        pos = self.GetPosition()
        #print pos
        dialog = child2.MyFrame2(self,-1)
        dialog.Show()
        #print dialog
        dialog.SetPosition(((pos[0],pos[1])))
        
    def OnOpenPath(self, event):
        extra_var.path = myimportimg.GetPath()
        extra_var.B_path = True
        #print path
        #print self.text_ctrl_6.GetValue()
        #a = float(self.text_ctrl_6.GetValue())
        #print a/3
    def OnOpenXMLPath(self, event):
        extra_var.xmlpath = myimportimg.GetPath()
        extra_var.B_path = True

    def GetSmallP(self, event):
        f = self.text_ctrl_1.GetValue()
        extra_var.B_Small = True # 参数1发生改变
        extra_var.SmallRegion_par = float(f)
    def GetSmallP0(self, event):
        f = self.text_ctrl_7.GetValue()
        extra_var.B_Small = True # 参数1发生改变
        extra_var.SmallRegion_par0 = float(f)
    
    def GetSimilarP1(self, event):
        f = self.text_ctrl_2.GetValue()
        extra_var.B_Similar = True # 参数1发生改变
        extra_var.SimilarColor_par1 = float(f)   
    def GetSimilarP2(self, event):
        f = self.text_ctrl_3.GetValue()
        extra_var.B_Similar = True # 参数1发生改变
        extra_var.SimilarColor_par2 = float(f)
    def GetP1(self, event):
        f = self.text_ctrl_4.GetValue()
        extra_var.B_par1 = True # 参数1发生改变
        #print "YES"
        extra_var.H_par1 = float(f)
    def GetP1_1(self, event):
        f = self.text_ctrl_8.GetValue()
        extra_var.B_par1 = True # 参数1发生改变
        #print "YES"
        extra_var.H_par1_1 = float(f)
    def GetP2_1(self, event):
        f = self.text_ctrl_5.GetValue()
        extra_var.H_par2_1 = float(f)
        extra_var.B_par2 = True # 参数2发生改变

    def GetP2_2(self, event):
        f = self.text_ctrl_6.GetValue()  
        extra_var.H_par2_2 = float(f)
        extra_var.B_par2 = True # 参数2发生改变
    
    def OnGetP3(self, event):
        f = self.slider_1.GetValue()
        extra_var.S_par3 = float(f)  
        extra_var.B_par3 = True
        #print f
    def mycopy(self, clusternode):
        clusternode_copy = []
        for i in xrange(len(clusternode)):
                clusternode_copy.append(myclass.Cluster(clusternode[i].vec, clusternode[i].id, clusternode[i].filename))
        return clusternode_copy
    def reclusterid(self, ClusterNode):
        cluster_ID = 0    
        for i in xrange(len(ClusterNode)):
            if cluster_ID < ClusterNode[i].id:
                cluster_ID = ClusterNode[i].id
        return cluster_ID
    def updateclusterid(self, ClusterNode, dela):
        delb = sorted(dela,reverse=False)
        id = 0
        for j in xrange(len(delb)):
            for i in xrange(len(ClusterNode)):
                if ClusterNode[i].id > delb[j]:
                    id += 1
                    break
        for j in xrange(len(delb)):
            for i in xrange(len(ClusterNode)):
                if ClusterNode[i].id > delb[j]:
                    ClusterNode[i].id -= 1
        minid = 0
        for i in xrange(len(ClusterNode)):
            if minid < ClusterNode[i].id:
                minid = ClusterNode[i].id
        return ClusterNode, minid, id
    def OnCluster(self, event):
        
        timestart = time.time() 
           
        ''' 重复性操作，只需要执行一次'''
        b_path = False
        if extra_var.B_path or extra_var.B_Small: # 更换目录时候才执行
            #print "0 error"
            b_path = True
            #extra_var.B_path = False
            mycluster.Cluster_1()
            mycluster.Classify()
            
            extra_var.ClusterNode1 = []
            extra_var.ImagesingleLeafNode, extra_var.ClusterNode1, extra_var.cluster_ID = mycluster.Cluster_Same(extra_var.ImagesingleLeafNode, extra_var.ClusterNode1, extra_var.cluster_ID)
            extra_var.Part1_ID = extra_var.cluster_ID
            extra_var.ImagesingleLeafNode += extra_var.trainersingleLeafNode
            extra_var.ImagesingleLeafNode, extra_var.ClusterNode1, extra_var.cluster_ID, extra_var.m_sigleleafID = mycluster.Cluster_Mirror(extra_var.ImagesingleLeafNode, extra_var.ClusterNode1, extra_var.cluster_ID)
            extra_var.Part9_ID = extra_var.cluster_ID
            '''存储中间值'''
            extra_var.ImagesingleLeafNode_0 = []
            extra_var.ClusterNode1_0 = []

            extra_var.ImagesingleLeafNode_0 = self.mycopy(extra_var.ImagesingleLeafNode)
            extra_var.ClusterNode1_0 = self.mycopy(extra_var.ClusterNode1)
            
            extra_var.ClusterNode2 = []
            extra_var.ImagearrayLeafNode, extra_var.ClusterNode2, extra_var.cluster_ID = mycluster.Cluster_Same(extra_var.ImagearrayLeafNode, extra_var.ClusterNode2, extra_var.cluster_ID)
            extra_var.ImagearrayLeafNode += extra_var.trainerarrayLeafNode
            extra_var.Part2_ID = extra_var.cluster_ID
            extra_var.ImagearrayLeafNode, extra_var.ClusterNode2, extra_var.cluster_ID, extra_var.m_arrayleafID = mycluster.Cluster_Mirror(extra_var.ImagearrayLeafNode, extra_var.ClusterNode2, extra_var.cluster_ID)
            extra_var.Part10_ID = extra_var.cluster_ID

            
            #print extra_var.Part2_ID
            extra_var.ImagearrayLeafNode_0 = []
            extra_var.ClusterNode2_0 = []
            extra_var.ImagearrayLeafNode_0 = self.mycopy(extra_var.ImagearrayLeafNode)
            extra_var.ClusterNode2_0 = self.mycopy(extra_var.ClusterNode2)
            
            extra_var.cluster_ID_0 = extra_var.cluster_ID
        
        #for i in range(len(extra_var.ImagesingleLeafNode_0)):
            #print extra_var.ImagesingleLeafNode_0[i].id, extra_var.ImagesingleLeafNode[i].id  
       
        
        
        '''当参数发生改变，执行不同的函数'''
        b_par1 = False
        if extra_var.B_par1 or extra_var.B_path or extra_var.B_Small:  #当参数1发生改变时候才执行
            if (not extra_var.B_path) and (not extra_var.B_Small):
                extra_var.ClusterNode1 = []
                extra_var.ClusterNode1 = self.mycopy(extra_var.ClusterNode1_0)
                extra_var.ClusterNode2 = []
                extra_var.ClusterNode2 = self.mycopy(extra_var.ClusterNode2_0)
                extra_var.ImagesingleLeafNode = []
                extra_var.ImagesingleLeafNode = self.mycopy(extra_var.ImagesingleLeafNode_0)
                extra_var.ImagearrayLeafNode = []
                extra_var.ImagearrayLeafNode = self.mycopy(extra_var.ImagearrayLeafNode_0)
                extra_var.cluster_ID = extra_var.cluster_ID_0
            
            #print "1 error"
            #print len(extra_var.ClusterNode1), len(extra_var.ImagesingleLeafNode)
            b_par1 = True
            #extra_var.B_par1 = False
            extra_var.singlelast = len(extra_var.ClusterNode1)
            extra_var.ImagesingleLeafNode, extra_var.ClusterNode1, extra_var.cluster_ID, extra_var.Add_singleClusterNode= mycluster.varcluster(extra_var.ImagesingleLeafNode, extra_var.ClusterNode1, extra_var.cluster_ID, extra_var.m_sigleleafID)
            extra_var.Part3_ID = extra_var.cluster_ID
            extra_var.arraylast = len(extra_var.ClusterNode2)
            extra_var.ImagearrayLeafNode, extra_var.ClusterNode2, extra_var.cluster_ID, extra_var.Add_arrayClusterNode = mycluster.varcluster(extra_var.ImagearrayLeafNode, extra_var.ClusterNode2, extra_var.cluster_ID, extra_var.m_arrayleafID)
            #extra_var.Part4_ID = extra_var.cluster_ID

            extra_var.ImagesingleLeafNode_1 = []
            extra_var.ClusterNode1_1 = []
            extra_var.ImagesingleLeafNode_1 = self.mycopy(extra_var.ImagesingleLeafNode)
            extra_var.ClusterNode1_1 = self.mycopy(extra_var.ClusterNode1)
            extra_var.ImagearrayLeafNode_1 = []
            extra_var.ClusterNode2_1 = []
            extra_var.ImagearrayLeafNode_1 = self.mycopy(extra_var.ImagearrayLeafNode)
            extra_var.ClusterNode2_1 = self.mycopy(extra_var.ClusterNode2)
            extra_var.Add_singleClusterNode_1 = []
            extra_var.Add_singleClusterNode_1 = self.mycopy(extra_var.Add_singleClusterNode)
            extra_var.Add_arrayClusterNode_1 = []
            extra_var.Add_arrayClusterNode_1 = self.mycopy(extra_var.Add_arrayClusterNode)
            extra_var.cluster_ID_1 = extra_var.cluster_ID
        
        #for i in range(len(extra_var.ClusterNode1)):
            #print extra_var.ClusterNode1[i].id , extra_var.ClusterNode1[i].filename
        #print "======"
        #for i in range(len(extra_var.ClusterNode2)):
            #print extra_var.ClusterNode2[i].id , extra_var.ClusterNode2[i].filename
        b_par2 = False
        if extra_var.B_par2 or extra_var.B_par1 or extra_var.B_path or extra_var.B_Small: # 当参数2发生改变时候才执行
            if (not extra_var.B_par1) and (not extra_var.B_path) and (not extra_var.B_Small):
                extra_var.ImagesingleLeafNode = []
                extra_var.ClusterNode1 = []
                extra_var.ImagesingleLeafNode = self.mycopy(extra_var.ImagesingleLeafNode_1)
                extra_var.ClusterNode1 = self.mycopy(extra_var.ClusterNode1_1)
                extra_var.ImagearrayLeafNode = []
                extra_var.ClusterNode2 = []
                extra_var.ImagearrayLeafNode = self.mycopy(extra_var.ImagearrayLeafNode_1)
                extra_var.ClusterNode2 = self.mycopy(extra_var.ClusterNode2_1)
                extra_var.Add_singleClusterNode = []
                extra_var.Add_singleClusterNode = self.mycopy(extra_var.Add_singleClusterNode_1)
                extra_var.Add_arrayClusterNode = []
                extra_var.Add_arrayClusterNode = self.mycopy(extra_var.Add_arrayClusterNode_1)
                extra_var.cluster_ID = extra_var.cluster_ID_1
            #print "2 error"
            b_par2 = True
            #extra_var.B_par2 = False

            extra_var.ImagesingleLeafNode, extra_var.ClusterNode1, extra_var.cluster_ID, dela = mycluster.regioncluster(extra_var.ImagesingleLeafNode, extra_var.ClusterNode1, extra_var.cluster_ID, extra_var.m_sigleleafID, extra_var.Add_singleClusterNode, extra_var.singlelast)
            idtemp = extra_var.cluster_ID
            extra_var.ClusterNode2, minid, id = self.updateclusterid(extra_var.ClusterNode2, dela)
            extra_var.Part4_ID = minid
            extra_var.Part3_ID = extra_var.Part3_ID-id
            ClusterNode = []
            ClusterNode = extra_var.ClusterNode1 + extra_var.ClusterNode2
            extra_var.cluster_ID = self.reclusterid(ClusterNode)
            extra_var.Part5_ID = extra_var.cluster_ID 
            
            extra_var.ImagearrayLeafNode, extra_var.ClusterNode2, extra_var.cluster_ID, dela = mycluster.regioncluster(extra_var.ImagearrayLeafNode, extra_var.ClusterNode2, extra_var.cluster_ID, extra_var.m_arrayleafID, extra_var.Add_arrayClusterNode, extra_var.arraylast)
            extra_var.ClusterNode1, minid, id= self.updateclusterid(extra_var.ClusterNode1, dela)
            extra_var.Part5_ID = minid
            ClusterNode = []
            ClusterNode = extra_var.ClusterNode1 + extra_var.ClusterNode2
            extra_var.cluster_ID = self.reclusterid(ClusterNode)
            
            extra_var.Part6_ID = extra_var.cluster_ID
            
            extra_var.ImagesingleLeafNode_2 = []
            extra_var.ClusterNode1_2 = []
            extra_var.ImagesingleLeafNode_2 = self.mycopy(extra_var.ImagesingleLeafNode)
            extra_var.ClusterNode1_2 = self.mycopy(extra_var.ClusterNode1)
            extra_var.ImagearrayLeafNode_2 = []
            extra_var.ClusterNode2_2 = []
            extra_var.ImagearrayLeafNode_2 = self.mycopy(extra_var.ImagearrayLeafNode)
            extra_var.ClusterNode2_2 = self.mycopy(extra_var.ClusterNode2)
            extra_var.cluster_ID_2 = extra_var.cluster_ID

        #print "========="
        #for i in range(len(extra_var.ClusterNode1)):
            #print extra_var.ClusterNode1[i].id , extra_var.ClusterNode1[i].filename
        #print "========="
        #for i in range(len(extra_var.ClusterNode2)):
            #print extra_var.ClusterNode2[i].id , extra_var.ClusterNode2[i].filename
            
        b_par3 = False
        if extra_var.B_par3 or extra_var.B_par2 or extra_var.B_par1 or extra_var.B_path or extra_var.B_Small: # 当参数3发生改变的时候执行
            if (not extra_var.B_par1) and (not extra_var.B_path) and (not extra_var.B_par2)and (not extra_var.B_Small):
                extra_var.ImagesingleLeafNode = []
                extra_var.ClusterNode1 = []
                extra_var.ImagesingleLeafNode = self.mycopy(extra_var.ImagesingleLeafNode_2)
                extra_var.ClusterNode1 = self.mycopy(extra_var.ClusterNode1_2)
                extra_var.ImagearrayLeafNode = []
                extra_var.ClusterNode2 = []
                extra_var.ImagearrayLeafNode = self.mycopy(extra_var.ImagearrayLeafNode_2)
                extra_var.ClusterNode2 = self.mycopy(extra_var.ClusterNode2_2)
                extra_var.cluster_ID = extra_var.cluster_ID_2

            #print "3 error"
            b_par3 = True
            #extra_var.B_par3 = False
            #print extra_var.cluster_ID
            extra_var.ClusterNode1, extra_var.cluster_ID = mycluster.pca_apcluster(extra_var.ImagesingleLeafNode, extra_var.ClusterNode1, extra_var.cluster_ID, extra_var.m_sigleleafID)
            extra_var.Part7_ID = extra_var.cluster_ID

            extra_var.ClusterNode2, extra_var.cluster_ID = mycluster.pca_apcluster(extra_var.ImagearrayLeafNode, extra_var.ClusterNode2, extra_var.cluster_ID, extra_var.m_arrayleafID)   
            extra_var.Part8_ID = extra_var.cluster_ID
            
            extra_var.ClusterNode = extra_var.ClusterNode0 + extra_var.ClusterNode1 + extra_var.ClusterNode2

        
        
       
        
        #print extra_var.Part0_ID,extra_var.Part1_ID,extra_var.Part2_ID,extra_var.Part3_ID,extra_var.Part4_ID
        #print extra_var.Part5_ID,extra_var.Part6_ID,extra_var.Part7_ID,extra_var.Part8_ID
        
        '''补充一种新的类型，形状完全相同，颜色近似的类型'''
        #for c in range(extra_var.Part0_ID+1, extra_var.Part1_ID+1):
            #ind = []
            #for n in range(len(ClusterNode)):
                #if (ClusterNode[n].extract_clusters_id() == c):
                    #ind.append([ClusterNode[n].get_cluster_elements(), ClusterNode[n].get_cluster_filename()])
            #mycluster.Same(ind)

        extra_var.name += 1
        '''创建保存图像目录'''
        Leafpath = os.getcwd()
        path1 = Leafpath+ "/result/"  + str(extra_var.name)+ "/small_feature/" 
        path2 = Leafpath+ "/result/" + str(extra_var.name)+ "/single_texture/same_shape/"
        path3 = Leafpath+ "/result/" + str(extra_var.name)+ "/single_texture/similar_shape/"
        path4 = Leafpath+ "/result/" + str(extra_var.name)+ "/sequence_texture/same_shape/"
        path5 = Leafpath+ "/result/" + str(extra_var.name)+ "/sequence_texture/similar_shape/"
        path6 = Leafpath+ "/result/" + str(extra_var.name) + "/un_cluster/"
        path7 = Leafpath+ "/result/" + str(extra_var.name)+ "/single_texture/same/"
        path8 = Leafpath+ "/result/" + str(extra_var.name)+ "/sequence_texture/same/"
        path9 = Leafpath+ "/result/" + str(extra_var.name)+ "/single_texture/mirror/"
        path10 = Leafpath+ "/result/" + str(extra_var.name)+ "/sequence_texture/mirror/"

        myimportimg.mkdir(path1)
        myimportimg.mkdir(path2)
        myimportimg.mkdir(path3)
        myimportimg.mkdir(path4)
        myimportimg.mkdir(path5)
        myimportimg.mkdir(path6)
        myimportimg.mkdir(path7)
        myimportimg.mkdir(path8)
        myimportimg.mkdir(path9)
        myimportimg.mkdir(path10)

        length = len(extra_var.choosetrainer)
        for i in xrange(length):
            ind = extra_var.choosetrainer[i]
            name = extra_var.alltrainer[ind][2]
            path = Leafpath+ "/result/" + str(extra_var.name) + "/trainer_cluster/" + name
            myimportimg.mkdir(path)
        
        for i in xrange(length):
            ind = extra_var.choosetrainer[i]
            name = extra_var.alltrainer[ind][2]
            path = Leafpath+ "/result/" +  "/trainer_cluster/" + name
            myimportimg.mkdir(path)
        
       
        print u"进行分类图像的保存!"

        if extra_var.B_Similar or extra_var.B_par3 or extra_var.B_par2 or extra_var.B_par1 or extra_var.B_path or extra_var.B_Small: # 当参数3发生改变的时候执行
            if (not extra_var.B_par3) and(not extra_var.B_par1) and (not extra_var.B_path) and (not extra_var.B_par2)and (not extra_var.B_Small):
                extra_var.ClusterNode = [] 
                extra_var.ClusterNode = self.mycopy(extra_var.ClusterNode_A)
                        
            extra_var.ClusterNode_A = []
            #for i in range(len(extra_var.ClusterNode)):
                #extra_var.ClusterNode_A.append(myclass.Cluster(extra_var.ClusterNode[i].vec, extra_var.ClusterNode[i].id, extra_var.ClusterNode[i].filename))
            extra_var.ClusterNode_A = self.mycopy(extra_var.ClusterNode)
            '''后来添加的，保存形状完全相同，颜色非常类似的一类'''  
            import mysavetrainer
            trainernode, trainerid = mysavetrainer.OnsaveTrainer(extra_var.ClusterNode)
            import mysavesame
            mysavesame.Onsavesame(extra_var.ClusterNode, path7, path8, trainerid)
            '''保存所有的分类'''      
            import mysaveall
            mysaveall.Onsaveall(extra_var.ClusterNode, path1, path2, path3, path4, path5, path6, path9, path10,trainernode, trainerid)
        
        extra_var.B_path = False
        extra_var.B_par1 = False
        extra_var.B_par2 = False
        extra_var.B_par3 = False
        extra_var.B_Small = False        
        extra_var.B_Similar = False
        timeend = time.time()    

        '''Step4 结果与显示 '''
        leng = len(extra_var.trainerarrayLeafNode)+len(extra_var.trainersingleLeafNode)
        print u"运行时间: %fs" % (timeend- timestart)
        print u"总共的图像数: %d" %(len(extra_var.ImageLeafNode)+leng)
        print u"聚类后的类个数: %d" % (extra_var.cluster_ID+1)
        print u"未聚类的图像个数: %d" % (len(extra_var.ImageLeafNode)+leng*2 -len(extra_var.ClusterNode))
        
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(u"图像聚类器")
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))
        self.button_4.SetMinSize((610, 30))
        self.button_4.SetForegroundColour(wx.Colour(142, 35, 35))
        self.button_4.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.button_5.SetMinSize((610, 30))
        self.button_5.SetForegroundColour(wx.Colour(142, 35, 35))
        self.button_5.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

        self.button_1.SetMinSize((306, 30))
        self.button_1.SetForegroundColour(wx.Colour(142, 35, 35))
        self.button_1.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.button_2.SetMinSize((306, 30))
        self.button_2.SetForegroundColour(wx.Colour(142, 35, 35))
        self.button_2.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.text_ctrl_7.SetMinSize((307, 30))
        self.text_ctrl_7.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_1.SetMinSize((307, 30))
        self.text_ctrl_1.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_2.SetMinSize((307, 30))
        self.text_ctrl_2.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_3.SetMinSize((307, 30))
        self.text_ctrl_3.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.button_3.SetMinSize((615, 30))
        self.button_3.SetForegroundColour(wx.Colour(142, 35, 35))
        self.button_3.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_1.SetForegroundColour(wx.Colour(79, 47, 47))
        self.label_1.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_4.SetMinSize((145, 30))
        self.text_ctrl_4.SetForegroundColour(wx.Colour(0, 0, 0))
        self.text_ctrl_8.SetMinSize((145, 30))
        self.text_ctrl_8.SetForegroundColour(wx.Colour(0, 0, 0))
        self.text_ctrl_4.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_8.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))

        self.text_ctrl_5.SetMinSize((145, 30))
        self.text_ctrl_5.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_6.SetMinSize((144, 30))
        self.text_ctrl_6.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.slider_1.SetMinSize((288, -1))

        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_7_staticbox.Lower()
        sizer_7 = wx.StaticBoxSizer(self.sizer_7_staticbox, wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_25_staticbox.Lower()
        sizer_25 = wx.StaticBoxSizer(self.sizer_25_staticbox, wx.VERTICAL)
        self.sizer_32_staticbox.Lower()
        sizer_32 = wx.StaticBoxSizer(self.sizer_32_staticbox, wx.HORIZONTAL)
        self.sizer_31_staticbox.Lower()
        sizer_31 = wx.StaticBoxSizer(self.sizer_31_staticbox, wx.HORIZONTAL)
        self.sizer_26_staticbox.Lower()
        sizer_26 = wx.StaticBoxSizer(self.sizer_26_staticbox, wx.HORIZONTAL)
        self.sizer_24_staticbox.Lower()
        sizer_24 = wx.StaticBoxSizer(self.sizer_24_staticbox, wx.HORIZONTAL)
        sizer_19 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_30_staticbox.Lower()
        sizer_30 = wx.StaticBoxSizer(self.sizer_30_staticbox, wx.HORIZONTAL)
        self.sizer_29_staticbox.Lower()
        sizer_29 = wx.StaticBoxSizer(self.sizer_29_staticbox, wx.HORIZONTAL)
        self.sizer_21_staticbox.Lower()
        sizer_21 = wx.StaticBoxSizer(self.sizer_21_staticbox, wx.HORIZONTAL)
        self.sizer_1_staticbox.Lower()
        sizer_1 = wx.StaticBoxSizer(self.sizer_1_staticbox, wx.HORIZONTAL)
        sizer_1.Add(self.button_4, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2 = wx.StaticBoxSizer(self.sizer_2_staticbox, wx.HORIZONTAL)
        sizer_2.Add(self.button_5, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.sizer_20_staticbox.Lower()
        sizer_20 = wx.StaticBoxSizer(self.sizer_20_staticbox, wx.HORIZONTAL)
        sizer_20.Add(self.button_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_20.Add(self.button_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_19.Add(sizer_1, 1, wx.EXPAND, 0)
        sizer_19.Add(sizer_20, 1, wx.EXPAND, 0)
        sizer_21.Add(self.text_ctrl_7, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_21.Add(self.text_ctrl_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_19.Add(sizer_21, 1, wx.EXPAND, 0)
        sizer_29.Add(self.text_ctrl_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_29.Add(self.text_ctrl_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_19.Add(sizer_29, 1, wx.EXPAND, 0)
        sizer_30.Add(self.button_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_19.Add(sizer_30, 1, wx.EXPAND, 0)
        sizer_19.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_7.Add(sizer_19, 1, wx.EXPAND, 0)
        sizer_24.Add(self.label_1, 0, wx.EXPAND, 0)
        sizer_11.Add(sizer_24, 1, wx.EXPAND, 0)
        sizer_26.Add(self.text_ctrl_4, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_26.Add(self.text_ctrl_8, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_25.Add(sizer_26, 1, wx.EXPAND, 0)
        sizer_31.Add(self.text_ctrl_5, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_31.Add(self.text_ctrl_6, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_25.Add(sizer_31, 1, wx.EXPAND, 0)
        sizer_32.Add(self.slider_1, 0, 0, 0)
        sizer_25.Add(sizer_32, 1, wx.EXPAND, 0)
        sizer_11.Add(sizer_25, 1, wx.EXPAND, 0)
        sizer_7.Add(sizer_11, 1, wx.EXPAND, 0)
        sizer_6.Add(sizer_7, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_6)
        sizer_6.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyFrame



if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
