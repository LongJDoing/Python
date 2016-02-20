#coding=utf-8
'''
Created on 2014��4��21��

@author: Administrator
'''
import os
import wx

def get_excellist(dir):
    files = os.listdir(dir)
    return [os.path.join(root, name) for root, dirs, files in os.walk(dir) for name in files if name.endswith('xlsx')]

def get_xmllist(dir):
    files = os.listdir(dir)
    return [os.path.join(root, name) for root, dirs, files in os.walk(dir) for name in files if name.endswith('xml')]

def get_imlist(dir):
    
    files = os.listdir(dir)
   # print files
    return [os.path.join(root, name) for root, dirs, files in os.walk(dir) for name in files if name.endswith('tga') or name.endswith('.bmp') or name.endswith('.png') or name.endswith('jpg') or name.endswith('.TGA') or name.endswith('.JPG') or name.endswith('.PNG') or name.endswith('.JPG') or name.endswith('.tif') or name.endswith('.TIF')]

def GetPath():
    dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    filename = None
    if dialog.ShowModal() == wx.ID_OK:
        filename = dialog.GetPath()
            
    if filename is not None:
        return filename
    else:
        print u"请导入一个包含指定文件的路径"
        return None
    dialog.Destroy()

def mkdir(path):
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        #print (path+' 目录已存在')
        return False
''' 
# 定义要创建的目录
mkpath="d:\\qttc\\web\\"
# 调用函数
mkdir(mkpath)
'''
def getsubdirectory(directory):
    inf = os.walk(directory)
    filename = [x[0] for x in inf]
    return filename

#a = getsubdirectory('D:\\Python_Pg\\Image_Classifier\\Trainer_Data\\')    
#print a