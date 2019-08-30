# Angles++ : These walking model is not used for Angles++ but it was an important exploration for the improvement of angles for occlusion problem
# The final walking model is "findwrong.py" and "correcte.py"

import pandas as pd 
import os
import sys
import re
import matplotlib.pyplot as plt

print('usage : <nb_video> <direction(front/back)>')
nb_video=sys.argv[1]
direction=sys.argv[2]
nb_video="3" # It's not a good solution for Angles++ so i have only the result of test3
# read files
files=os.listdir('testVideos/test'+nb_video+'/') 
print(direction[1:])
    
for i in files:
    if (len(re.findall('GT-Vicon_.'+direction[1:], i))!=0):
        filegt=i
    if (len(re.findall('joints_3DKinect_.'+direction[1:]+'.csv', i))!=0):
        filecm=i
print(filecm, filegt)   
gt=pd.DataFrame(pd.read_csv('testVideos/test'+nb_video+'/'+filegt))
k=pd.DataFrame(pd.read_csv('testVideos/test'+nb_video+'/'+filecm))

# show results_ankle gt
fig1=plt.figure()
ax1=fig1.add_subplot(111)
ax1.scatter(gt['frame'], -gt['Y_lak'], marker='.', c=gt['step'])
ax1.plot(gt['frame'], -gt['Y_lak'], color='y', lw=0.1)
#for i in range(len(gt['frame'])):
#    ax1.text(gt['frame'][i], -gt['Y_lak'][i],str(gt['step'][i]))

ax1.set_title('Distance Akles_gt and Kinect')
ax1.scatter(gt['frame'], -gt['Y_rak'], marker='.', c=gt['step'])
ax1.plot(gt['frame'], -gt['Y_rak'], color='r', lw=0.1)

# show result_ankle kinect
#ax2=fig1.add_subplot(212)
#ax2.set_title('Distance Akles_kinect')
kk=dict(k)
kk['step_gt']=[]
kk['bad_step']=[8]*len(k)
for i in range(len(k)):
    if list(gt['step'][gt['frame']==k['frames'][i]])==[]:
        kk['step_gt'].append(8)
    else:
        kk['step_gt'].append(int(gt['step'][gt['frame']==k['frames'][i]]))

kk=pd.DataFrame(kk)

ax1.scatter(kk['frames'][kk['step_gt']!=8], kk['z_rak'][kk['step_gt']!=8], marker='.', c=kk['step'][kk['step_gt']!=8])
ax1.plot(kk['frames'], kk['z_rak'], color='orange', lw=0.2,label='right')

ax1.scatter(kk['frames'][kk['step_gt']!=8], kk['z_lak'][kk['step_gt']!=8], marker='.', c=kk['step'][kk['step_gt']!=8])
ax1.plot(kk['frames'], kk['z_lak'], color='b', lw=0.2, label='left')

'''
for i in range(len(kk['frames'])): 
    
    if kk['step'][i]!=kk['step_gt'][i] and kk['step_gt'][i]!=8 or kk['step'][i]==-1:
        ax2.text(kk['frames'][i], kk['z_lak'][i],str(kk['step'][i]),color='r')
        print('Frame:', kk['frames'][i], 'Kinect:', kk['step'][i], 'Vicon:', kk['step_gt'][i])
        kk['bad'][i]=1
    elif kk['step'][i]==kk['step_gt'][i]:
        ax2.text(kk['frames'][i], kk['z_lak'][i],str(kk['step'][i]), color='g')
        kk['bad'][i]=0
    else:
        ax2.text(kk['frames'][i], kk['z_lak'][i],str(kk['step'][i]), color='black')
'''
# !!! ax2 xie xia mian
# zheng fan
# model gaijin

# show left knee angles kinect+vicon
fig2=plt.figure()
ax3=fig2.add_subplot(211)
ax3.scatter(kk['frames'][kk['step_gt']!=8], kk['kangle_l'][kk['step_gt']!=8], c=kk['step'][kk['step_gt']!=8])
ax3.plot(kk['frames'], kk['kangle_l'], color='b')
ax3.scatter(gt['frame'], gt['X_lag'], marker='.', c=gt['step'])
ax3.plot(gt['frame'], gt['X_lag'], color='y',lw=0.2)
ax3.set_title('Left Knee Angles')
'''
for i in range(len(kk['frames'])):
    if kk['bad'][i]==1:
        ax3.text(kk['frames'][i], kk['kangle_l'][i],str(kk['step'][i]),color='r')
for i in range(len(gt['frame'])):  
    ax3.text(gt['frame'][i], gt['X_lag'][i],str(gt['step'][i]))
'''
# show right knee angles kinect+vicon   
ax4=fig2.add_subplot(212)
ax4.scatter(kk['frames'][kk['step_gt']!=8], kk['kangle_r'][kk['step_gt']!=8], c=kk['step'][kk['step_gt']!=8])
ax4.plot(kk['frames'], kk['kangle_r'], color='orange')
ax4.set_title('Right Knee Angles')
ax4.scatter(gt['frame'], gt['X_rag'], marker='.', c=gt['step'])
ax4.plot(gt['frame'], gt['X_rag'], color='r', lw=0.1)
'''
for i in range(len(kk['frames'])): 
    if kk['bad'][i]==1:
        ax4.text(kk['frames'][i], kk['kangle_r'][i],str(kk['step'][i]),color='r')
    elif kk['bad'][i]==0:
        ax4.text(kk['frames'][i], kk['kangle_r'][i],str(kk['step'][i]),color='g')
    else:
        ax4.text(kk['frames'][i], kk['kangle_r'][i],str(kk['step'][i]),color='black')
'''
# show left knee ankle distance
fig3=plt.figure()
ax5=fig3.add_subplot(211)
ax5.plot(kk['frames'], kk['l_kn_ak'], marker='.', color='b')
ax5.set_title('Left Knee Ankle Distance')

# show right knee ankle distance   
ax6=fig3.add_subplot(212)
ax6.plot(kk['frames'], kk['r_kn_ak'], marker='.', color='orange')
ax6.set_title('Right Knee Ankle Distance')
  
plt.show()

# save new file
number=(re.search('[0-9]+',filegt).group(0)) 
for c in kk.keys():
    if len(re.findall('Unnamed',c))!=0:
        kk.drop([c],axis=1,inplace=True)
if direction=='back':
    kk.to_csv('testVideos'+'/test'+nb_video+'/'+number+'_LCR-NET_joints_3DKinect_back.csv',encoding='gbk')
else:
    kk.to_csv('testVideos'+'/test'+nb_video+'/'+number+'_LCR-NET_joints_3DKinect_front.csv',encoding='gbk')
print(number,': File is saved!')
