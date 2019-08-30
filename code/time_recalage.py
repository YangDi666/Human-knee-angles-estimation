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
# xianshi zai tong yi ge tushang
#hengzuobiaotoushi t(ms)
from pandas import Series
from numpy import nan as NaN
from pandas import DataFrame
import sys

frames=[int(sys.argv[3]),int(sys.argv[4])]
nb_video=sys.argv[1]
files=os.listdir('testVedios/test'+nb_video+'/') 
direction=sys.argv[2]


if int(nb_video)<=14:
    if direction=='f':
        keywords_file12='julia'+str(100+2*int(nb_video))+'.*'
    else:
        keywords_file12='julia'+str(101+2*int(nb_video))+'.*'
else:
    if direction=='f':
        keywords_file12='hugo'+str(100+2*(int(nb_video)-14))+'.*'
    else:
        keywords_file12='hugo'+str(101+2*(int(nb_video)-14))+'.*'
    
for i in files:
    if (len(re.findall('.*joints_3DKinect_'+direction+'ront.csv', i))!=0):
        fileang=i
    if (len(re.findall(keywords_file12+'left', i))!=0):
        filename1=i
    if (len(re.findall(keywords_file12+'right', i))!=0):
        filename2=i
    if (len(re.findall('tempstams_.*\.csv', i))!=0):
        filetime=i   
print(fileang, filename1, filename2, filetime)

timestamps=np.array(pd.read_csv('testVedios/test'+nb_video+'/'+filetime))
time=[0]
for t in timestamps:
    time.append((t[0]-44471900000))
fig=plt.figure()
ax=fig.add_subplot(211)
ax2=fig.add_subplot(212)

ax.set_xlabel('t/ms')
ax.set_ylabel('Angle_left')
ax2.set_xlabel('t/ms') 
ax2.set_ylabel('Angle_right')
fileang3d='test'+nb_video+'_LCR-NET_angles.csv'
angs=pd.DataFrame(pd.read_csv('testVedios/test'+nb_video+'/'+fileang))
anglesl=angs['kangle_l']
anglesr=angs['kangle_r']
angs3d=pd.DataFrame(pd.read_csv('testVedios/test'+nb_video+'/'+fileang3d))
anglesl3d=[180-k for k in list(map(float,angs3d['angle_left'][frames[0]:frames[1]]))]
anglesr3d=[180-k for k in list(map(float,angs3d['angle_right'][frames[0]:frames[1]]))]
print(type(anglesl3d[1]))

#b, a = signal.butter(8, 0.3, 'lowpass') 
#anglesl = signal.filtfilt(b, a, anglesl) 
#anglesr = signal.filtfilt(b, a, anglesr)  

#k=2792
#time[frames[0]:frames[1]]=[i-k for i in time[frames[0]:frames[1]]]

ax.plot(time[frames[0]:frames[1]], anglesl, marker='.')
ax2.plot(time[frames[0]:frames[1]], anglesr, color='r', marker='.')#, marker='.')
#for i in range(50): y1.append(i) # 每迭代一次，将i放入y1中画出来 ax.cla() # 清除键 ax.bar(y1, label='test', height=y1, width=0.3) ax.legend() plt.pause(0.1)

data1=pd.read_csv('testVedios/test'+nb_video+'/'+filename1)
data2=pd.read_csv('testVedios/test'+nb_video+'/'+filename2)
data1=(pd.DataFrame(data1))
data2=(pd.DataFrame(data2))
#data1.dropna(axis=0, how='any')
#data2=data2.drop(range(300,1004000), inplace=True)

'''
print(frames[0])
fields=range(times[frames[0]]-350, times[frames[1]]-350)
print(fields)
'''

angleX_l=data1['X_ag']

angleY=data1['Y_ag']
angleZ=data1['Z_ag']
field=data2['field']
angleX_r=data2['X_ag']


field=[i*10 for i in field]

# ax.set_xticks([])
# axleft.set_yticks([])
ax.plot(field, angleX_l, color='b', marker='.', label='Angle_X')
ax2.plot(field, angleX_r, color='r', marker='.', label='Angle_X')
#ax.plot(field, angleY, color='g', marker='.', label='Angle_Y')
#ax.plot(field, angleZ, color='b', marker='.', label='Angle_Z')
t1=time[frames[0]:frames[1]]
errs=[]
dt=[]
for d in range(t1[0], int(t1[-1]-field[-1]), 50):
    errs.append(tools.compt(t1, anglesl3d, field, angleX_l, d)[0]+tools.compt(t1, anglesr3d, field, angleX_r, d)[0])
    dt.append(d)
fig3=plt.figure()
ax3=fig3.add_subplot(211)
ax3.set_xlabel('dt')
ax3.set_ylabel('Err')
ax3.plot(dt, errs, marker='.')
dt_best=2500#dt[errs.index(min(errs))]
errs=[]
dt=[]
for d in range(dt_best-50, dt_best+50):
    errs.append(tools.compt(t1, anglesl3d, field, angleX_l, d)[0]+tools.compt(t1, anglesr3d, field, angleX_r, d)[0])
    dt.append(d)
ax4=fig3.add_subplot(212)
ax4.set_xlabel('dt')
ax4.set_ylabel('Err')
ax4.plot(dt, errs, marker='.')
dt_best=1949.6666666666667#dt[errs.index(min(errs))]
errmin_l=tools.compt(t1, anglesl3d, field, angleX_l, dt_best, True)
errmin_r=tools.compt(t1, anglesr3d, field, angleX_r, dt_best, True)
print('dt : ', dt_best, 'Err mse : ', min(errs))
plt.show()


with open('testVedios/test'+nb_video+'/time_recalage.json') as json_data:
    jsondata = json.load(json_data)
if direction=='f':
    jsondata['dt1']=dt_best
    jsondata['err1']=min(errs)
else:
    jsondata['dt2']=dt_best
    jsondata['err2']=min(errs)
with open('testVedios/test'+nb_video+'/time_recalage.json', 'w') as outfile:
    json.dump(jsondata, outfile)