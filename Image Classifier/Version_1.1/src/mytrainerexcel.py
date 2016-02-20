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

    filename = path + str(extra_var.name) + '_trainer.xlsx'
    
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
    for i in xrange(len(extra_var.choosetrainer)):
        ind = extra_var.choosetrainer[i]
        name = extra_var.alltrainer[ind][2]
        worksheet = workbook.add_worksheet(name)
        worksheet.write(0, 0, u'聚类序号', bold)
        worksheet.write(0,1, u'图像位置', bold)
        worksheet.write(0, 12, u'图像', bold)    
        path = Leafpath+ "/result/" + str(extra_var.name) + "/trainer_cluster/" + name
    
        setsheet(worksheet, path, format1, format2)
        
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