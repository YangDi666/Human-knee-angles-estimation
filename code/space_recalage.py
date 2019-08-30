# Space calibration
# ! You should run it after time_recalage
# Usage : python3 space_recalage.py <nb_video> <direction(f/b)> <frame_begin> <frame_end> <algo> <showfigures(True/False)>


import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import math
import sys
import cv2
from mpl_toolkits.mplot3d import Axes3D
import json
import tools_lcr
from tqdm import tqdm
import os
import pandas as pd
import re
from scipy import signal


def space_recalage(nb_video, aix, frames, direction, algo, show):
    articulations=['ak','kn','as','wr','el','sh']
    files=os.listdir('testVideos/test'+nb_video+'/') 

    for i in files:
        if direction=='f':
            if (len(re.findall('.*'+algo+'_joints_3DKinect_'+direction+'ront.csv', i))!=0):
                fileank=i
        else:
            if (len(re.findall('.*'+algo+'_joints_3DKinect_'+direction+'ack.csv', i))!=0):
                fileang=i
                
        if (len(re.findall('gt_.*\_left_'+direction+'.csv', i))!=0):
            filename1=i
        if (len(re.findall('gt_.*\_right_'+direction+'.csv', i))!=0):
            filename2=i
        if (len(re.findall('tempstams_.*\.csv', i))!=0):
            filetime=i  

    print(fileank, filename1, filename2, filetime)
    timestamps=np.array(pd.read_csv('testVideos/test'+nb_video+'/'+filetime))
    time=[0]
    for t in timestamps:
        time.append((t[0]-44471900000))
    fig=plt.figure()
    ax=fig.add_subplot(211)
    ax2=fig.add_subplot(212)
    anks=pd.DataFrame(pd.read_csv('testVideos/test'+nb_video+'/'+fileank))
    data1=pd.DataFrame(pd.read_csv('testVideos/test'+nb_video+'/'+filename1))
    data2=pd.DataFrame(pd.read_csv('testVideos/test'+nb_video+'/'+filename2))

    output={}
    #with open('../../semaine11/time calibration/testVideos/test'+nb_video+'/time_recalage_general.json') as json_data:
    with open('testVideos/test'+nb_video+'/'+algo+'_time_recalage_'+direction+'.json') as json_data:
        jsondata = json.load(json_data)
 
    dt=jsondata['dt']
    print('dt:',dt)
      
    for arts in articulations: 
    # For aix Y (z)

        if aix=='Y':
            ax.set_xlabel('t/ms')
            ax.set_ylabel('Joint_left_Y(z)')
            ax2.set_xlabel('t/ms')
            ax2.set_ylabel('Joint_right_Y(z)')

            anklesl=anks['z_l'+arts]
            anklesr=anks['z_r'+arts]
            data11=data1[['field','Y_'+arts]].dropna(axis=0, how='any')
            data22=data2[['field','Y_'+arts]].dropna(axis=0, how='any')
            
            ankle_l=data11['Y_'+arts]
            ankle_r=data22['Y_'+arts]
            fieldl=data11['field']
            fieldr=data22['field']
           
            ankle_l=[-i for i in ankle_l]
            ankle_r=[-i for i in ankle_r]

        if aix=='X':
            ax.set_xlabel('t/ms')
            ax.set_ylabel('Joint_left_X(x)')
            ax2.set_xlabel('t/ms')
            ax2.set_ylabel('Joint_right_X(x)')

            anklesl=anks['x_l'+arts]
            anklesr=anks['x_r'+arts]
            #b, a = signal.butter(8, 0.3, 'lowpass') 
            #anglesl = signal.filtfilt(b, a, anglesl) 
            #anglesr = signal.filtfilt(b, a, anglesr)  

            #for i in range(50): y1.append(i) # 每迭代一次，将i放入y1中画出来 ax.cla() # 清除键 ax.bar(y1, label='test', height=y1, width=0.3) ax.legend() plt.pause(0.1)
            data11=data1[['field','X_'+arts]].dropna(axis=0, how='any')
            data22=data2[['field','X_'+arts]].dropna(axis=0, how='any')
            
            ankle_l=data11['X_'+arts]
            ankle_r=data22['X_'+arts]
            fieldl=data11['field']
            fieldr=data22['field']
            ankle_l=[-i for i in ankle_l]
            ankle_r=[-i for i in ankle_r]
            

        if aix=='Z':
            ax.set_xlabel('t/ms')
            ax.set_ylabel('Joints_left_Z(y)')
            ax2.set_xlabel('t/ms')
            ax2.set_ylabel('Joints_right_Z(y)')

            anklesl=anks['y_l'+arts]
            anklesr=anks['y_r'+arts]

            data11=data1[['field','Z_'+arts]].dropna(axis=0, how='any')
            data22=data2[['field','Z_'+arts]].dropna(axis=0, how='any')
            
            ankle_l=list(data11['Z_'+arts])
            ankle_r=list(data22['Z_'+arts])
            fieldl=data11['field']
            fieldr=data22['field']
           
        # ax.set_xticks([])
        # axleft.set_yticks([])
        fieldl=[i*10 for i in fieldl]
        fieldr=[i*10 for i in fieldr] 
        ax.plot(time[frames[0]:frames[1]], anklesl, marker='.')
        ax2.plot(time[frames[0]:frames[1]], anklesr, marker='.')#, marker='.')  
        ax.plot(fieldl, ankle_l, color='b', marker='.', label='Joint_'+aix)
        ax2.plot(fieldr, ankle_r, color='r', marker='.', label='Joint_'+aix)
        #ax.plot(field, angleY, color='g', marker='.', label='Angle_Y')
        #ax.plot(field, angleZ, color='b', marker='.', label='Angle_Z')
        t1=time[frames[0]:frames[1]]
        errsl=[]
        dy=[]

        
        t1=[i-dt for i in t1]
        for d in range(-4000, 5000, 50):
            errsl.append(tools_lcr.comps(t1, anklesl, fieldl, ankle_l, d))
            dy.append(d)
        fig3=plt.figure()
        ax3=fig3.add_subplot(211)
        ax3.set_xlabel('d'+aix)
        ax3.set_ylabel('Err')
        ax3.plot(dy, errsl, marker='.')
        dt_best_l=dy[errsl.index(min(errsl))]
        errsl=[]
        dy=[]
        for d in range(dt_best_l-80, dt_best_l+80):
            errsl.append(tools_lcr.comps(t1, anklesl, fieldl, ankle_l, d))
            dy.append(d)
        ax4=fig3.add_subplot(212)
        ax4.set_xlabel('d'+aix)
        ax4.set_ylabel('Err')
        ax4.plot(dy, errsl, marker='.')
        dy_best_l=dy[errsl.index(min(errsl))]
        errmin_l=tools_lcr.comps(t1, anklesl, fieldl, ankle_l, dy_best_l, True)
        print(arts, ' left d'+aix+': ', dy_best_l, 'Err : ', min(errsl))
        
        errsr=[]
        dy=[]
        for d in range(-4000, 5000, 50):
            errsr.append(tools_lcr.comps(t1, anklesr, fieldr, ankle_r, d))
            dy.append(d)
        ax3.plot(dy, errsr, marker='.')
        dt_best_r=dy[errsr.index(min(errsr))]
        errsr=[]
        dy=[]
        for d in range(dt_best_r-80, dt_best_r+80):
            errsr.append(tools_lcr.comps(t1, anklesr, fieldr, ankle_r, d))
            dy.append(d)
        ax4.plot(dy, errsr, marker='.')
        dy_best_r=dy[errsr.index(min(errsr))]

        errmin_r=tools_lcr.comps(t1, anklesr, fieldr, ankle_r, dy_best_r, True)
        print(arts, ' right d'+aix+': ', dy_best_r, 'Err : ', min(errsr))
        output['r'+arts]=[dy_best_r, min(errsr)]
        output['l'+arts]=[dy_best_l, min(errsl)]
    dm_l=[i[0] for i in output.values()]
    for l in dm_l:
        if l ==-4080:
            dm_l.remove(l)
    dm=sum(dm_l)/len(dm_l)
    print('Mean : ', dm)
    if show=='True':
        plt.show()
    return output, dm
   
print("Usage : python3 space_recalage.py <nb_video> <direction(f/b)> <frame_begin> <frame_end> <algo> <showfigures(True/False)>")
frames=[int(sys.argv[3]),int(sys.argv[4])]
nb_video=sys.argv[1]
direction=sys.argv[2]
algo=sys.argv[5]
show=sys.argv[6]

outjson={}

output, dXm=space_recalage(nb_video, 'X', frames, direction, algo, show)
outjson['dX']=output
outjson['dXm']=dXm
output, dYm=space_recalage(nb_video, 'Y', frames, direction, algo, show)
outjson['dY']=output
outjson['dYm']=dYm
output, dZm=space_recalage(nb_video, 'Z', frames, direction, algo, show)
outjson['dZ']=output
outjson['dZm']=dZm
print(outjson)
if direction=='b':
    with open('testVideos/test'+nb_video+'/space_recalage_back_'+algo+'.json', 'w') as json_out:
        json.dump(outjson, json_out)
else:
    with open('testVideos/test'+nb_video+'/space_recalage_front_'+algo+'.json', 'w') as json_out:
        json.dump(outjson, json_out)
