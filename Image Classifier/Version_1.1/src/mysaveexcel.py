#coding=utf-8
'''
Created on 2014��5��12��

@author: Administrator
'''
import extra_var
import xlsxwriter
import os
import myimportimg
from PIL import Image

def mysavexls():
    Leafpath = os.getcwd()
    path = Leafpath +'/result/'
    myimportimg.mkdir(path)

    filename = path + str(extra_var.name) + '.xlsx'
    
    #delexcel = myimportimg.get_excellist(path)
    #for i in range(len(delexcel)):
        #os.remove(delexcel[i])
    workbook = xlsxwriter.Workbook(filename)
    bold = workbook.add_format({'bold': 1})
    # Add a format. Light red fill with dark red text.
    format1 = workbook.add_format({'bg_color': '#FFC7CE',
                                   'font_color': '#9C0006'})
    
    # Add a format. Green fill with dark green text.
    format2 = workbook.add_format({'bg_color': '#C6EFCE',
                                   'font_color': '#006100'})
    worksheet0 = workbook.add_worksheet(u'纹理特征非常小')
    worksheet0.write(0, 0, u'聚类序号', bold)
    worksheet0.write(0,1, u'图像位置', bold)
    worksheet0.write(0, 12, u'图像', bold)     #worksheet0.write('C1', u'alpha通道',bold) 
     
    worksheet6 = workbook.add_worksheet(u'单纹理形状完全相同，颜色相似')
    worksheet6.write(0, 0, u'聚类序号', bold)
    worksheet6.write(0,1, u'图像位置', bold)
    worksheet6.write(0, 12, u'图像', bold)
     
    worksheet1 = workbook.add_worksheet(u'单纹理形状完全相同')
    worksheet1.write(0, 0, u'聚类序号', bold)
    worksheet1.write(0,1, u'图像位置', bold)
    worksheet1.write(0, 12, u'图像', bold) 

    worksheet8 = workbook.add_worksheet(u'单纹理形状镜像相似')
    worksheet8.write(0, 0, u'聚类序号', bold)
    worksheet8.write(0,1, u'图像位置', bold)
    worksheet8.write(0, 12, u'图像', bold) 
    
    worksheet2 = workbook.add_worksheet(u'单纹理形状相似')
    worksheet2.write(0, 0, u'聚类序号', bold)
    worksheet2.write(0,1, u'图像位置', bold)
    worksheet2.write(0, 12, u'图像', bold) 

    worksheet7 = workbook.add_worksheet(u'序列纹理形状完全相同，颜色相似')
    worksheet7.write(0, 0, u'聚类序号', bold)
    worksheet7.write(0,1, u'图像位置', bold)
    worksheet7.write(0, 12, u'图像', bold)
    
    worksheet3 = workbook.add_worksheet(u'序列纹理形状完全相同')
    worksheet3.write(0, 0, u'聚类序号', bold)
    worksheet3.write(0,1, u'图像位置', bold)
    worksheet3.write(0,12, u'图像', bold) 

    worksheet9 = workbook.add_worksheet(u'镜像纹理形状镜像相似')
    worksheet9.write(0, 0, u'聚类序号', bold)
    worksheet9.write(0,1, u'图像位置', bold)
    worksheet9.write(0, 12, u'图像', bold) 
    
    worksheet4 = workbook.add_worksheet(u'序列纹理形状相似')
    worksheet4.write(0, 0, u'聚类序号', bold)
    worksheet4.write(0,1, u'图像位置', bold)
    worksheet4.write(0, 12, u'图像', bold) 

    worksheet5 = workbook.add_worksheet(u'未成功聚类')
    worksheet5.write(0, 0, u'聚类序号', bold)
    worksheet5.write(0,1, u'图像位置', bold)
    worksheet5.write(0, 12, u'图像', bold) 

    path1 = Leafpath+ "/result/"  + str(extra_var.name)+ "/small_feature/" 
    path2 = Leafpath+ "/result/" + str(extra_var.name)+ "/single_texture/same_shape/"
    path3 = Leafpath+ "/result/" + str(extra_var.name)+ "/single_texture/similar_shape/"
    path4 = Leafpath+ "/result/" + str(extra_var.name)+ "/sequence_texture/same_shape/"
    path5 = Leafpath+ "/result/" + str(extra_var.name)+ "/sequence_texture/similar_shape/"
    path6 = Leafpath+ "/result/" + str(extra_var.name) +  "/un_cluster/"
    path7 = Leafpath+ "/result/" + str(extra_var.name)+ "/single_texture/same/"
    path8 = Leafpath+ "/result/" + str(extra_var.name)+ "/sequence_texture/same/"
    path9 = Leafpath+ "/result/" + str(extra_var.name)+ "/single_texture/mirror/"
    path10 = Leafpath+ "/result/" + str(extra_var.name)+ "/sequence_texture/mirror/"
    worksheet = [worksheet0, worksheet1,worksheet2,worksheet3,worksheet4,worksheet5,worksheet6,worksheet7,worksheet8,worksheet9]
    path = [path1,path2,path3,path4,path5,path6,path7,path8,path9, path10 ]
    for i in xrange(10):
        setsheet(worksheet[i], path[i], format1, format2)
def setsheet(worksheet, path, format1, format2):
    imlist = myimportimg.get_imlist(path)
    row = 1
    col = 0
    maxh = 0
    lastmaxh = 0
    w = 0
    b_is = True
    for i in xrange(len(imlist)):
        mystr = imlist[i].split('/')
        text = mystr[len(mystr)-1]
        if 'gray' not in text:
            text = text.split('.')
            tex = text[0]
           # print tex
            filename = imlist[i]
            filename = filename.replace('png', 'txt')
            file_object = open(filename)
            all_filename = file_object.read()
            file_object.close( )
            all_filename = all_filename.split('\n')
        
            if b_is:
                myformat = format1
                b_is = False
            else:
                myformat = format2
                b_is = True
                
            image = Image.open(imlist[i])
            w,h = image.size

            lastmaxh = maxh
            maxh = max(len(all_filename)-1, h/19)
            
            maxh = maxh + lastmaxh
            
            worksheet.conditional_format(row+lastmaxh,col, row+maxh-1, col+12+2*w/64,{'type': 'blanks',
                                                                                    'format': myformat})
            worksheet.conditional_format(row+lastmaxh,col, row+maxh-1, col+12+2*w/64,{'type': 'no_blanks',
                                                                                    'format': myformat})
            worksheet.write_string(row+lastmaxh, col, tex)
            for n in xrange(len(all_filename)-1):          
                worksheet.write_string(row+lastmaxh+n, col+1, all_filename[n])
            worksheet.insert_image(row+lastmaxh, col+12, imlist[i])#, {'x_scale': 0.5, 'y_scale': 0.5})
            grayfilename = imlist[i].replace('.png', 'gray.png')
            worksheet.insert_image(row+lastmaxh, col+13+w/64, grayfilename)
            