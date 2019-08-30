# Angles++ : we can detect the bad frames by the walking model
# Usage : python3 findwrong_lcr.py <nb_video> <direction(front/back)> <showfigures> ex : 1 front True')


import pandas as pd 
import os
import sys
import re
import matplotlib.pyplot as plt
import tools_lcr


if (len(sys.argv)!=4):
    print('usage : python3 findwrong_lcr.py <nb_video> <direction(front/back)> <showfigures> ex : 1 front True')
nb_video=sys.argv[1]
direction=sys.argv[2]
show=sys.argv[3]
# read files
files=os.listdir('testVideos/test'+nb_video+'/') 
print(direction[1:])
    
for i in files:
    if (len(re.findall('LCR-NET_joints_3DKinect_.'+direction[1:]+'[^2]', i))!=0):
        filecm=i
print(filecm)   
k=pd.DataFrame(pd.read_csv('testVideos/test'+nb_video+'/'+filecm))
kk=k

# walking model : find wrong points
badpoints=0
for i in range(len(k['frames'])):
    akdis=k['z_lak'][i]-k['z_rak'][i]
    kndis=k['z_lkn'][i]-k['z_rkn'][i]
    l_kn_ak=tools_lcr.get_distance((k['x_lkn'][i], k['y_lkn'][i], k['z_lkn'][i]), (k['x_lak'][i], k['y_lak'][i], k['z_lak'][i])) 
    r_kn_ak=tools_lcr.get_distance((k['x_rkn'][i], k['y_rkn'][i], k['z_rkn'][i]), (k['x_rak'][i], k['y_rak'][i], k['z_rak'][i]))
    if i==20:    
        print(i,akdis, kndis)
    if k['kangle_r'][i]<0 or (akdis**2<=400 and kndis<100 and kndis>-20) or (akdis**2<=400 and kndis>220):
        k.loc[i,['bad_frame']]=10
        badpoints+=1
        print(i, kndis)
    elif k['kangle_l'][i]<0 or (akdis**2<=400 and kndis<-205) or (akdis**2<=400 and kndis>-100 and kndis<10):
        k.loc[i,['bad_frame']]=11
        badpoints+=1
        print(i,kndis)
     
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
ax1.set_title('Wrong points searaching for ak')
ax1.set_xlabel('frame')
ax1.set_ylabel('z ak_kinect')
ax1.plot(kk['frames'],kk['z_lak'], marker='.', color='b', lw=1.8)
ax1.plot(kk['frames'],kk['z_rak'], marker='.', color='r', lw=1.8)
for i in range(len(k['frames'])):
    if k['bad_frame'][i]==0:
        ax1.text(kk['frames'][i],kk['z_lak'][i], str(k['bad_frame'][i]), color='g',size=10)
    else:
        ax1.text(kk['frames'][i],kk['z_rak'][i], str(k['bad_frame'][i]), color='#B22222',size=10)

# show result as kinect
fig2=plt.figure()
ax4=fig2.add_subplot(111)
ax4.set_title('Wrong points searching for as')
ax4.set_xlabel('frame')
ax4.set_ylabel('z as_kinect')
ax4.plot(kk['frames'],kk['z_las'], marker='.', color='b', lw=1.8)
ax4.plot(kk['frames'],kk['z_ras'], marker='.', color='r', lw=1.8)
for i in range(len(k['frames'])):
    if k['bad_frame'][i]==0:
        ax4.text(kk['frames'][i],kk['z_las'][i], str(k['bad_frame'][i]), color='g',size=10)
    else:
        ax4.text(kk['frames'][i],kk['z_ras'][i], str(k['bad_frame'][i]), color='#B22222',size=10)
#ax5=fig2.add_subplot(212)
#ax5.set_title('height as_kinect')
#ax5.plot(kk['frames'],kk['y_las'], marker='.', color='b', lw=0.2)
#ax5.plot(kk['frames'],kk['y_ras'], marker='.', color='y', lw=0.2)

fig3=plt.figure()
ax2=fig3.add_subplot(211)
ax3=fig3.add_subplot(212)
ax2.set_title('Left Angles_kinect')
ax3.set_title('Right Angles_kinect')
ax2.plot(kk['frames'],kk['kangle_l'], lw=1.8, color='b', marker='.')
ax3.plot(kk['frames'],kk['kangle_r'], lw=1.8, color='r', marker='.')

for i in range(len(k['frames'])):
    if k['bad_frame'][i]==0:
        ax2.text(kk['frames'][i],kk['kangle_l'][i], str(k['bad_frame'][i]), color='black',size=10)
    else:
        ax2.text(kk['frames'][i],kk['kangle_l'][i], str(k['bad_frame'][i]), color='r',size=10)
for i in range(len(k['frames'])):
    if k['bad_frame'][i]==0:
        ax3.text(kk['frames'][i],kk['kangle_r'][i], str(k['bad_frame'][i]), color='black',size=10)
    else:
        ax3.text(kk['frames'][i],kk['kangle_r'][i], str(k['bad_frame'][i]), color='r',size=10)
if show=='True':
    plt.show()

# save new file
number=(re.search('[0-9]+',filecm).group(0)) 
for c in k.keys():
    if len(re.findall('Unnamed',c))!=0:
        k.drop([c],axis=1,inplace=True)
if direction=='back':
    k.to_csv('testVideos'+'/test'+nb_video+'/'+number+'_LCR-NET_joints_3DKinect_back2.csv',encoding='gbk')
else:
    k.to_csv('testVideos'+'/test'+nb_video+'/'+number+'_LCR-NET_joints_3DKinect_front2.csv',encoding='gbk')
print(number,': File is saved!')

#⁼