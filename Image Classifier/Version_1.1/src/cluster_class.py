#coding=utf-8
'''
Created on 2014��4��23��

@author: Administrator
'''

'''图像聚类之后的类别
输出   : 
        id:  类的ID
        vec: 图像内容
        filename: 图像的路径
'''
class Cluster(object):
    def __init__(self, vec, id, filename=""):
        self.vec = vec
        self.id = id
        self.filename = filename
    
    def extract_clusters_id(self):
        return self.id
    
    def get_cluster_elements(self):
        return self.vec
    
    def get_cluster_filename(self):
        return self.filename