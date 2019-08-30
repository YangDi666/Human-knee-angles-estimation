# Angles++ : Walking model for PifPaf
import pandas as pd 
import os
import sys
import re
import matplotlib.pyplot as plt
import tools_pp

if (len(sys.argv)!=4):
    print('usage : python3 findwrong_pp.py <nb_video> <direction(front/back)> <showfigures> ex : 1 front True')
nb_video=sys.argv[1]
direction=sys.argv[2]
show=sys.argv[3]
# read files
files=os.listdir('testVideos/test'+nb_video+'/') 
print(direction[1:])
    
for i in files:
    if (len(re.findall('PifPaf_joints_3DKinect_.'+direction[1:]+'[^2]', i))!=0):
        filecm=i
print(filecm)   
k=pd.DataFrame(pd.read_csv('testVideos/test'+nb_video+'/'+filecm))
kk=k

# find wrong points
badpoints=0
for i in range(len(k['frames'])):
    akdis=k['z_lak'][i]-k['z_rak'][i]
    kndis=k['z_lkn'][i]-k['z_rkn'][i]
    if k['frames'][i]==59:
        print(i)
        print(k['z_lak'][i],k['z_rak'][i])
        print(kndis)
    l_kn_ak=tools_pp.get_distance((k['x_lkn'][i], k['y_lkn'][i], k['z_lkn'][i]), (k['x_lak'][i], k['y_lak'][i], k['z_lak'][i])) 
    r_kn_ak=tools_pp.get_distance((k['x_rkn'][i], k['y_rkn'][i], k['z_rkn'][i]), (k['x_rak'][i], k['y_rak'][i], k['z_rak'][i]))
    if k['kangle_r'][i]<0 or (akdis**2<=1600 and kndis<100 and kndis>-50) or (akdis**2<=400 and kndis>250):
        k.loc[i,['bad_frame']]=10
        badpoints+=1
        print(i, kndis)
    elif k['kangle_l'][i]<0 or (akdis**2<=400 and kndis<-205) or (akdis**2<=400 and kndis>-100 and kndis<10):
        k.loc[i,['bad_frame']]=11
        badpoints+=1
        print(i,kndis)
        ###!!!!!!! zuihao zuo you jiao fen kai left: 0 right: 1
    elif (k['z_las'][i]-k['z_ras'][i])>80:
        k.loc[i,['bad_frame']]=20
        badpoints+=1
    elif (k['z_las'][i]-k['z_ras'][i])<-80:
        k.loc[i,['bad_frame']]=21
        badpoints+=1
        #print(i, ':', (k['z_las'][i]-k['z_ras'][i])**2)
    elif r_kn_ak>600:
        k.loc[i,['bad_frame']]=30
        badpoints+=1
    elif l_kn_ak>600:
        k.loc[i,['bad_frame']]=31
        badpoints+=1
    else:
        k.loc[i,['bad_frame']]=0
fig1=plt.figure()
print('bad points:',badpoints)


# show result_ankle kinect
ax1=fig1.add_subplot(111)
ax1.set_title('Distance Akles_kinect')
ax1.plot(kk['frames'],kk['z_lak'], marker='.', color='b', lw=0.2)
ax1.plot(kk['frames'],kk['z_rak'], marker='.', color='y', lw=0.2)
for i in range(len(k['frames'])):
    if k['bad_frame'][i]==0:
        ax1.text(kk['frames'][i],kk['z_lak'][i], str(k['bad_frame'][i]), color='black')
    else:
        ax1.text(kk['frames'][i],kk['z_rak'][i], str(k['bad_frame'][i]), color='r')

# show result as kinect
fig2=plt.figure()
ax4=fig2.add_subplot(111)
ax4.set_title('Distance as_kinect')
ax4.plot(kk['frames'],kk['z_las'], marker='.', color='b', lw=0.2)
ax4.plot(kk['frames'],kk['z_ras'], marker='.', color='y', lw=0.2)
for i in range(len(k['frames'])):
    if k['bad_frame'][i]==0:
        ax4.text(kk['frames'][i],kk['z_las'][i], str(k['bad_frame'][i]), color='black')
    else:
        ax4.text(kk['frames'][i],kk['z_ras'][i], str(k['bad_frame'][i]), color='r')
#ax5=fig2.add_subplot(212)
#ax5.set_title('height as_kinect')
#ax5.plot(kk['frames'],kk['y_las'], marker='.', color='b', lw=0.2)
#ax5.plot(kk['frames'],kk['y_ras'], marker='.', color='y', lw=0.2)

fig3=plt.figure()
ax2=fig3.add_subplot(211)
ax3=fig3.add_subplot(212)
ax2.set_title('Left Angles_kinect')
ax3.set_title('Right Angles_kinect')
ax2.plot(kk['frames'],kk['kangle_l'], lw=0.2, color='b', marker='.')
ax3.plot(kk['frames'],kk['kangle_r'], lw=0.2, color='r', marker='.')

for i in range(len(k['frames'])):
    if k['bad_frame'][i]==0:
        ax2.text(kk['frames'][i],kk['kangle_l'][i], str(k['bad_frame'][i]), color='black')
    else:
        ax2.text(kk['frames'][i],kk['kangle_l'][i], str(k['bad_frame'][i]), color='r')
for i in range(len(k['frames'])):
    if k['bad_frame'][i]==0:
        ax3.text(kk['frames'][i],kk['kangle_r'][i], str(k['bad_frame'][i]), color='black')
    else:
        ax3.text(kk['frames'][i],kk['kangle_r'][i], str(k['bad_frame'][i]), color='r')
if show=='True':
    plt.show()

# save new file
number=(re.search('[0-9]+',filecm).group(0)) 
for c in k.keys():
    if len(re.findall('Unnamed',c))!=0:
        k.drop([c],axis=1,inplace=True)
if direction=='back':
    k.to_csv('testVideos'+'/test'+nb_video+'/'+number+'_PifPaf_joints_3DKinect_back2.csv',encoding='gbk')
else:
    k.to_csv('testVideos'+'/test'+nb_video+'/'+number+'_PifPaf_joints_3DKinect_front2.csv',encoding='gbk')
print(number,': File is saved!')

#⁼