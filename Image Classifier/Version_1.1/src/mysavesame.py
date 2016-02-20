#coding=utf-8
'''
Created on 2014��5��13��

@author: Administrator
'''
from matplotlib.pyplot import *
import mycluster
from numpy import *

import extra_var
import myimgfunction

def Onsavesame(ClusterNode, path7, path8,trainerid):
    
    fig = figure()
    for c in xrange(extra_var.cluster_ID+1):
        if c not in trainerid:
            ind = []
            same = []
            for n in xrange(len(ClusterNode)):
                if (ClusterNode[n].extract_clusters_id() == c):
                    ind.append([ClusterNode[n].get_cluster_elements(), ClusterNode[n].get_cluster_filename()])
            ID = -1
            if(c > extra_var.Part0_ID)and(c <= extra_var.Part1_ID):
                same, ID = mycluster.Same(ind)
            if (c <= extra_var.Part2_ID) and(c > extra_var.Part9_ID):
                same, ID = mycluster.Same(ind)
            
            for n in xrange(ID+1):
                for id in xrange(5):
                        iind = []
                        for i in xrange(len(same)):
                            if (i < (id+1)*40) &(i >= id*40):
                                if same[i][2] == n:
                                    iind.append([same[i][0], same[i][1]])
        
                        b_is = False
                        #print len(ind)
                        all_text = ''
                        for i in xrange(minimum(len(iind),40)):
                            im = iind[i][0]
                            ax = fig.add_subplot(10,4, i+1)
                            ax.autoscale_view(True, True, True)
                            #print type(im)
                            imshow(array(im), cmap ='gray',filternorm = 1, aspect='auto')
                            #show()
                            ax.set_title(iind[i][1], fontsize = 2.5)
                            axis('equal')
                            axis('off')
                    
                            myfilename = iind[i][1] + '\n'
                            all_text += myfilename
                            b_is = True  
                        if b_is:
                            if(c > extra_var.Part0_ID)and(c <= extra_var.Part1_ID):
                                s = str(c)
                                if len(s) == 1:
                                    s = '00'+ s
                                if len(s) ==2:
                                    s ='0'+s
                                filename = path7 + s + '_%d'%id +'_%d.png'%n
                                fig.savefig(unicode(filename, "UTF-8"), bbox_inches='tight', dpi = 300)
                                
                                txtfilename = path7 + s + '_%d'%id +'_%d.txt'%n
                                f = open(txtfilename, 'w')
                                f.write(all_text.encode('utf8'))
                                f.close()
                            elif (c <= extra_var.Part2_ID) and(c > extra_var.Part1_ID):
                                s = str(c)
    
                                if len(s) == 1:
                                    s = '00'+ s
                                if len(s) ==2:
                                    s ='0'+s
                                filename = path8 + s + '_%d'%id +'_%d.png'%n
                                fig.savefig(unicode(filename, "UTF-8"), bbox_inches='tight', dpi = 300)
                                
                                txtfilename = path8 + s + '_%d'%id +'_%d.txt'%n
                                f = open(txtfilename, 'w')
                                f.write(all_text.encode('utf8'))
                                f.close()
                            else:
                                pass
                        clf()
                        
                        for i in xrange(minimum(len(iind),40)):
                            
                            im_gray = myimgfunction.make_regalur_image(im, B_Ch=True, B_is=False)
                            ax = fig.add_subplot(10,4, i+1)
                            ax.autoscale_view(True, True, True)
                            #print type(im)
                            imshow((im_gray), cmap ='gray',filternorm = 1, aspect='auto')                    #show()
                            ax.set_title(same[i][1], fontsize = 2.5)
                            axis('equal')
                            axis('off')
                        if b_is:
                            if(c > extra_var.Part0_ID)and(c <= extra_var.Part1_ID):
                                s = str(c)
    
                                if len(s) == 1:
                                    s = '00'+ s
                                if len(s) ==2:
                                    s ='0'+s
                                filename = path7 + s + '_%d'%id+'_%dgray.png'%n
                                fig.savefig(unicode(filename, "UTF-8"), bbox_inches='tight', dpi = 300)
                                
                            elif (c <= extra_var.Part2_ID) and(c > extra_var.Part1_ID):
                                s = str(c)
    
                                if len(s) == 1:
                                    s = '00'+ s
                                if len(s) ==2:
                                    s ='0'+s
                                filename = path8 + s + '_%d'%id +'_%dgray.png'%n
                                fig.savefig(unicode(filename, "UTF-8"), bbox_inches='tight', dpi = 300)
                                
                            else:
                                pass
                        clf()

