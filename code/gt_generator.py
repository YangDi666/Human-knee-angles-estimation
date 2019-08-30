import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import math
import sys
import cv2
from mpl_toolkits.mplot3d import Axes3D
import json
import tools
from tqdm import tqdm
import os
import pandas as pd
import re
from scipy import signal

articulations=['ak','kn','as','wr','el','sh','ag']

frames=[int(sys.argv[3]),int(sys.argv[4])]
nb_video=sys.argv[1]
direction=sys.argv[2]
files=os.listdir('testVedios/test'+nb_video+'/') 

if int(nb_video)<=14:
    if direction=='Front':
        keywords_file12='julia'+str(100+2*int(nb_video))+'.*'
    else:
        keywords_file12='julia'+str(101+2*int(nb_video))+'.*'
else:
    if direction=='Front':
        keywords_file12='hugo'+str(100+2*(int(nb_video)-14))+'.*'
    else:
        keywords_file12='hugo'+str(101+2*(int(nb_video)-14))+'.*'
    
for i in files:
    if (len(re.findall(keywords_file12+'left', i))!=0):
        filename1=i
    if (len(re.findall(keywords_file12+'right', i))!=0):
        filename2=i
    if (len(re.findall('tempstams_.*\.csv', i))!=0):
        filetime=i 
number=filetime[10:-4]  
print(filename1, filename2, filetime)

timestamps=np.array(pd.read_csv('testVedios/test'+nb_video+'/'+filetime))
time=[0]
for t in timestamps:
    time.append((t[0]-44471900000))
data1=pd.read_csv('testVedios/test'+nb_video+'/'+filename1)
data2=pd.read_csv('testVedios/test'+nb_video+'/'+filename2)
data1=(pd.DataFrame(data1))
data2=(pd.DataFrame(data2))
#with open('testVedios/test'+nb_video+'/time_recalage.json') as json_data:
with open('../../semaine11/time calibration/testVideos/test'+nb_video+'/time_recalage_general.json') as json_data:   
    jsondataT = json.load(json_data)
if direction=='Front':
    dt=jsondataT['dt1']
    with open('testVedios/test'+nb_video+'/space_recalage.json') as json_data:
        jsondataS = json.load(json_data)
else:
    dt=jsondataT['dt2']
    with open('testVedios/test'+nb_video+'/space_recalage_back.json') as json_data:
        jsondataS = json.load(json_data)
print('dt:', dt)
field=data2['field']
field=[i*10 for i in field]
jsonfinal={'frame': []}
t1=time[frames[0]:frames[1]]
for arts in articulations:
    gt_lx=data1['X_'+arts]
    gt_rx=data2['X_'+arts] 

    gt_ly=data1['Y_'+arts]
    gt_ry=data2['Y_'+arts]

    gt_lz=data1['Z_'+arts]
    gt_rz=data2['Z_'+arts]   
    t1=time[frames[0]:frames[1]]
    outlx=tools.compt(t1, t1, field, gt_lx, dt)
    outly=tools.compt(t1, t1, field, gt_ly, dt)
    outlz=tools.compt(t1, t1, field, gt_lz, dt)
    tfl=[time.index(i) for i in outlx[1]]
    
    gtlx=outlx[2]
    gtly=outly[2]
    gtlz=outlz[2]
    jsonfinal['X_l'+arts]=gtlx
    jsonfinal['Y_l'+arts]=gtly
    jsonfinal['Z_l'+arts]=gtlz
    #print(tfl, gtl)

    #print(outl)
    outrx=tools.compt(t1, t1, field, gt_rx, dt)
    outry=tools.compt(t1, t1, field, gt_ry, dt)
    outrz=tools.compt(t1, t1, field, gt_rz, dt)
    gtrx=outrx[2]
    gtry=outry[2]
    gtrz=outrz[2]

    jsonfinal['X_r'+arts]=gtrx
    jsonfinal['Y_r'+arts]=gtry
    jsonfinal['Z_r'+arts]=gtrz

jsonfinal['frame']=tfl   
#plt.plot(jsonfinal['frame'], jsonfinal['X_rag'], marker='.')
#plt.show()
jsonfinal['akdis']=[]
jsonfinal['kndis']=[]
jsonfinal['step']=[]

for i in range(len(tfl)):
    dak=(jsonfinal['Y_lak'][i]-jsonfinal['Y_rak'][i])
    dkn=(jsonfinal['Y_lkn'][i]-jsonfinal['Y_rkn'][i])
    jsonfinal['akdis'].append(dak)
    jsonfinal['kndis'].append(dkn)

    # Model : step automatic by Vicon!!!!!back front

    if dkn<=0 and dak>-100:
        jsonfinal['step'].append(0)
    elif dak<=-100 and dkn<0:
        jsonfinal['step'].append(1)
    elif dkn>=0 and dak<100:
        jsonfinal['step'].append(2)
    elif dak>=100 and dkn>0:
        jsonfinal['step'].append(3)
    else:
        jsonfinal['step'].append(-1)
# save jsonfinal : gt 
data=pd.DataFrame(jsonfinal)
data.to_csv('testVedios'+'/test'+nb_video+'/'+number+'GT-Vicon_'+direction+'.csv', encoding='gbk')
print('GT_'+keywords_file12.upper()[:-2]+'.csv', 'saved!')

# save jsonfifinal : gt transformée individuelle à Kinect par rapport de l'Algo
jsonfifinal={}
for joint in jsonfinal.keys():
    if joint!='frame' and joint.find('ag')==-1 and joint.find('dis')==-1 and joint.find('step')==-1:
        new_pos=[]
        for jf in jsonfinal[joint]:
            jf=tools.VIto3D(jf, jsondataS, joint[0], joint[2:])
            new_pos.append(jf)
        jj=joint.replace('Y', 'z')
        jj=jj.replace('Z', 'y')
        jj=jj.replace('X', 'x')
        jsonfifinal[jj]=new_pos
jsonfifinal['frame']=tfl
jsonfifinal['step']=jsonfinal['step']
jsonfifinal['kangle_l']=[]
jsonfifinal['kangle_r']=[]
for i in range(len(tfl)):
    jsonfifinal['kangle_l'].append(180-tools.angle((jsonfifinal['x_las'][i],jsonfifinal['y_las'][i],jsonfifinal['z_las'][i]),(jsonfifinal['x_lkn'][i], jsonfifinal['y_lkn'][i],jsonfifinal['z_lkn'][i]),(jsonfifinal['x_lak'][i],jsonfifinal['y_lak'][i],jsonfifinal['z_lak'][i])))
    jsonfifinal['kangle_r'].append(180-tools.angle((jsonfifinal['x_ras'][i],jsonfifinal['y_ras'][i],jsonfifinal['z_ras'][i]),(jsonfifinal['x_rkn'][i], jsonfifinal['y_rkn'][i],jsonfifinal['z_rkn'][i]),(jsonfifinal['x_rak'][i],jsonfifinal['y_rak'][i],jsonfifinal['z_rak'][i])))

data=pd.DataFrame(jsonfifinal)
data.to_csv('testVedios'+'/test'+nb_video+'/'+number+'_GT-Vicon_LCR-NET_3DKinect_'+direction+'_respectiveTF.csv', encoding='gbk')
print('GT_Kinect'+keywords_file12.upper()[:-2]+'.csv', 'saved!')

# save jsonfififinal : gt transformée générale à Kinect par rapport de l'Algo
jsonfififinal={}
for joint in jsonfinal.keys():
    if joint!='frame' and joint.find('ag')==-1 and joint.find('dis')==-1 and joint.find('step')==-1:
        new_pos_g=[]
        for jf in jsonfinal[joint]:
            jf=tools.VIto3D(jf, jsondataS, joint[0])
            new_pos_g.append(jf)
        jj=joint.replace('Y', 'z')
        jj=jj.replace('Z', 'y')
        jj=jj.replace('X', 'x')
        jsonfififinal[jj]=new_pos_g
jsonfififinal['frame']=tfl
jsonfififinal['step']=jsonfinal['step']
jsonfififinal['kangle_l']=[]
jsonfififinal['kangle_r']=[]

for i in range(len(tfl)):
    jsonfififinal['kangle_l'].append(180-tools.angle((jsonfififinal['x_las'][i],jsonfififinal['y_las'][i],jsonfififinal['z_las'][i]),(jsonfififinal['x_lkn'][i], jsonfififinal['y_lkn'][i],jsonfififinal['z_lkn'][i]),(jsonfififinal['x_lak'][i],jsonfififinal['y_lak'][i],jsonfififinal['z_lak'][i])))
    jsonfififinal['kangle_r'].append(180-tools.angle((jsonfififinal['x_ras'][i],jsonfififinal['y_ras'][i],jsonfififinal['z_ras'][i]),(jsonfififinal['x_rkn'][i], jsonfififinal['y_rkn'][i],jsonfififinal['z_rkn'][i]),(jsonfififinal['x_rak'][i],jsonfififinal['y_rak'][i],jsonfififinal['z_rak'][i])))
    
data=pd.DataFrame(jsonfififinal)
data.to_csv('testVedios'+'/test'+nb_video+'/'+number+'_GT-Vicon_LCR-NET_3DKinect_'+direction+'_generalTF.csv', encoding='gbk')
print('GT_Kinect_general'+keywords_file12.upper()[:-2]+'.csv', 'saved!')

# save jsonfifififinal : gt à 2D Color Tf individuelle
jsonfifififinal={}
j=['rak','lak','rkn','lkn','ras','las','rwr','lwr','rel','lel','rsh','lsh']
jsonfifififinal['frame']=tfl
for joint in j:
    jsonfifififinal['x_'+joint]=[]
    jsonfifififinal['y_'+joint]=[]
    for i in range(len(tfl)):
        (x,y)=tools.K3DtoD((jsonfifinal['x_'+joint][i], jsonfifinal['y_'+joint][i], jsonfifinal['z_'+joint][i]))
        (x,y)=tools.DtoRGB((x,y))
        jsonfifififinal['x_'+joint].append(x)
        jsonfifififinal['y_'+joint].append(y)  
data=pd.DataFrame(jsonfifififinal)
data.to_csv('testVedios'+'/test'+nb_video+'/'+number+'_GT-Vicon_LCR-NET_2DColor_'+direction+'_respectiveTF.csv', encoding='gbk')
print('GT_Color_respective'+keywords_file12.upper()[:-2]+'.csv', 'saved!')
# save jsonfififififinal : gt à 2D Color Tf générale
jsonfififififinal={}
jsonfififififinal['frame']=tfl
for joint in j:
    jsonfififififinal['x_'+joint]=[]
    jsonfififififinal['y_'+joint]=[]
    for i in range(len(tfl)):
        (x,y)=tools.K3DtoD((jsonfififinal['x_'+joint][i], jsonfififinal['y_'+joint][i], jsonfififinal['z_'+joint][i]))
        (x,y)=tools.DtoRGB((x,y))
        jsonfififififinal['x_'+joint].append(x)
        jsonfififififinal['y_'+joint].append(y)  
data=pd.DataFrame(jsonfififififinal)
data.to_csv('testVedios'+'/test'+nb_video+'/'+number+'_GT-Vicon_LCR-NET_2DColor_'+direction+'_generalTF.csv', encoding='gbk')
print('GT_Color_general'+keywords_file12.upper()[:-2]+'.csv', 'saved!')

# save jsonfifififififinal : gt à 2D Depth



# show results
fig=plt.figure()
ax1=fig.add_subplot(211)
ax1.plot(tfl, jsonfinal['Y_lak'], marker='.', color='r')
ax1.plot(tfl, jsonfifinal['z_lak'], marker='.', color='b')
ax1.plot(tfl, jsonfififinal['z_lak'], marker='.', color='g')
ax1.set_title('Left Ankle z (gt_r, Tfrespective_b, Tfgeneral_g)')
ax3=fig.add_subplot(212)
ax3.plot(tfl, jsonfinal['Y_rak'], marker='.', color='r')
ax3.plot(tfl, jsonfifinal['z_rak'], marker='.', color='b')
ax3.plot(tfl, jsonfififinal['z_rak'], marker='.', color='g')
ax3.set_title('Right Ankle z (gt_r, Tfrespective_b, Tfgeneral_g)')



fig2=plt.figure()
ax2=fig2.add_subplot(211)
final=pd.DataFrame(jsonfinal)
ax2.scatter(final['frame'], final['Y_lak'], marker='.', c=final['step'])
ax2.plot(final['frame'], final['Y_lak'], color='y', lw=0.1)
for i in range(len(final['frame'])):
    ax2.text(final['frame'][i], final['Y_lak'][i],str(final['step'][i]))
#ax2.plot(tfl, jsonfifinal['kangle_l'], marker='.', color='b')
#ax2.plot(tfl, jsonfififinal['kangle_l'], marker='.', color='g')
#ax2.set_title('Left Angle (gt_r, Tfrespective_b,and joint.find('step')==-1 Tfgeneral_g)')
ax2.set_title('Left Ankle_gt')
ax2.scatter(final['frame'], final['Y_rak'], marker='.', c=final['step'])
ax2.plot(final['frame'], final['Y_rak'], color='r', lw=0.1)

fig4=plt.figure()
#for i in tfl:
    #ax2.text(i,jsonfinal['X_lag'][i]+2, jsonfinal['step'], color='g')
ax4=fig4.add_subplot(111)
#ax4.scatter(final['frame'], final['X_rag'], marker='.', c=final['step']+1)
ax4.plot(final['frame'], final['X_lag'], color='r', marker='.')

ax4.plot(tfl, jsonfifinal['kangle_l'], marker='.', color='b')
ax4.plot(tfl, jsonfififinal['kangle_l'], marker='.', color='g')
ax4.set_title('Left Angle (gt_l, Tfrespective_b, Tfgeneral_g)')

fig3=plt.figure()
ax5=fig3.add_subplot(111)
ax5.plot(tfl,jsonfinal['akdis'], marker='.')
ax5.plot(tfl,jsonfinal['kndis'], marker='.')

plt.show()
