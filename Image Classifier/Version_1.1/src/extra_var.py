#coding=utf-8
'''
Created on 2014��5��22��

@author: Administrator
'''
#coding=utf-8
'''
Created on 2014��4��25��

@author: Administrator
'''
SmallRegion_par = 0.3
SmallRegion_par0 = 5
SimilarColor_par1 = 0.02
SimilarColor_par2 = 0.02
H_par1 = 2286.0
H_par1_1 = 1.0
H_par2_1 = 5
H_par2_2 = 0.03
S_par3 = -50
path = ""
xmlpath = ""
name = 0
B_path = True # 标示选择目录按钮是否按下
B_par1 = True # 标示参数1是否改变
B_par2 = True # 标示参数2是否改变
B_par3 = True # 标示参数3是否改变
B_Small = True # 标示设置小区域是否改变
B_Similar = True # 标示设置颜色相似是否改变
Part0_ID = -1 # 特征非常小类的断点标示ID
Part1_ID = 0 # 单纹理形状完全相同的断点标示ID
Part3_ID = 0 # 单纹理形状类似的断点标示ID
Part2_ID = 0 # 序列纹理形状完全相同的断点标示
Part4_ID = 0 # 序列理形状类似的断点标示ID
Part5_ID = 0 # 单理形状类似的断点标示ID
Part6_ID = 0 # 序列理形状类似的断点标示ID

Part7_ID = 0 # 单纹理形状PCA的断点标示ID
Part8_ID = 0 # 序列理形状PCA的断点标示ID
Part9_ID = 0 # 单纹理形状镜像的断点标示ID
Part10_ID = 0 # 序列纹理形状镜像的断点标示ID

ImageLeafNode = [] # 所有纹理的节点
ImagearrayLeafNode = [] #序列纹理的节点
ImagesingleLeafNode = [] # 单独纹理的节点

ClusterNode = [] #存储所有的聚类
ClusterNode0 =[] # 第一次分类存储
ClusterNode1 = [] # 单纹理的聚类存储
ClusterNode2 = [] # 序列纹理的聚类存储
cluster_ID = -1 # 标示类的ID
cluster_S_ID = -1 # 标示单纹理ID
cluster_A_ID = -1 # 标示序列纹理ID
m_sigleleafID = 0 #单纹理按照长宽分类数
m_arrayleafID = 0 #序列纹理按照长宽分类数

Add_singleClusterNode = [] #中间变量
Add_arrayClusterNode = []

singlelast = 0
arraylast = 0
'''在内存中存储每一步操作的中间值,这些值会在后续发生改变'''
ClusterNode1_0 = []
ImagesingleLeafNode_0 = []
ImagearrayLeafNode_0 =[]
ClusterNode2_0 =[]
cluster_ID_0 = 0 

ClusterNode_A =[]

ClusterNode1_1 = []
ImagesingleLeafNode_1 = []
ImagearrayLeafNode_1 =[]
ClusterNode2_1 =[]
cluster_ID_1 = 0 
Add_singleClusterNode_1 = []
Add_arrayClusterNode_1 = []

ClusterNode1_2 = []
ImagesingleLeafNode_2 = []
ImagearrayLeafNode_2 =[]
ClusterNode2_2 =[]
cluster_ID_2 = 0 

smallregion0 ={} #存储小区域的坐标左位置
smallregion1 ={} #存储小区域的坐标右位置
smallregionw ={} #存储小区域的坐标宽度
smallregionh ={} #存储小区域的坐标高度

trainfilename ='' #训练器的路径
trainernum = -1 # 图像训练的类个数
trainergetnum = -1 #选择后的图像训练器的个数
alltrainer = {} # 所有的训练类
choosetrainer = [] #选择的训练器
inversechoosetrainer = [] #取消选择的训练器
mouseleft = False
mousemove = False
ctrlkey = False
mouseup = False
inittrainerimlist = {} #初始的训练器图像路径
trainersingleLeafNode = []
trainerarrayLeafNode = []
trainerimlist = {} # 训练器的图像路径