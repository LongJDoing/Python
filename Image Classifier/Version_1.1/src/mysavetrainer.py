#coding=utf-8
'''
Created on 2014��5��29��

@author: Administrator
'''
import extra_var
def OnsaveTrainer(ClusterNode):
    trainernode = {}
    trainerid = []
    
    for i in xrange(len(extra_var.choosetrainer)):
        ind = extra_var.choosetrainer[i]
        filename = extra_var.alltrainer[ind][1]
        filename = filename.split('\\')
        name = extra_var.alltrainer[ind][2]
        a = []
        for c in xrange(len(ClusterNode)):
            #print ClusterNode[c].filename, filename
            text = ClusterNode[c].filename.split('\\')
           # print text
            del text[-1]
            #print text, filename
            
            if (text == filename):
                if (ClusterNode[c].id not in trainerid):
                    a.append([ClusterNode[c].id, name])
                    trainerid.append(ClusterNode[c].id)
        #a = list(set(a))
        #print alltext
        trainernode[i] = a
    
    for i in xrange(len(trainernode)):
        if len(trainernode[i]):                     
            name = trainernode[i][0][1]
            alltext =''
            for x in xrange(len(trainernode[i])):
                for c in xrange(len(ClusterNode)):  
                    if (ClusterNode[c].id == trainernode[i][x][0]):
                        filetext = ClusterNode[c].filename + '\n'
                        alltext += filetext    
            #print repr(name)
            extra_var.trainerimlist[name] = alltext
    
    #print extra_var.trainerimlist
    '''进行文件的拷贝移动'''
    import os
    import shutil
    Leafpath = os.getcwd()
    for i in xrange(len(trainernode)):
        if len(trainernode[i]):
            name = trainernode[i][0][1]
            alltext = extra_var.trainerimlist[name]
            text = alltext.split('\n')
            del text[-1]
            text = list(set(text))
            #print text
            for i in xrange(len(text)):
               # print filename
                filename = text[i].split('\\')
              #  print filename
                filename = filename[-1]
               # print filename
                filename = Leafpath+ "/result/" +  "/trainer_cluster/" + name +'/' + filename
               # print filename
                shutil.copyfile(text[i], filename)
    

    return trainernode, trainerid