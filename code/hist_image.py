
# Angles+ : This is an exploration for Angles+, it can draw a histogram for a joints
# Usage : <nb_video> <frame> <size> <joint(lankle/rankle/lknee/rknee/lthi/rthi)> 

import cv2
import numpy as np
import matplotlib.pyplot as plt
import tools_lcr
import json
import pylab as pl
import scipy.signal as signal
import os
from tqdm import tqdm
import re
import sys

def his(nb_video, frame, size, joint):

    files=os.listdir('testVideos/test'+nb_video+'/') 
    for i in files:
        if (len(re.findall('.*C\.json', i))!=0):
            filejson=i
        if (len(re.findall('.*D.mp4', i))!=0):
            filedepth=i
    v=cv2.VideoCapture('testVideos/test'+nb_video+'/'+filedepth)
    with open('testVideos/test'+nb_video+'/'+filejson) as json_data:
            d = json.load(json_data)
    #for t in range(frames[0],frames[1]):
        #print(t)

    v.set(cv2.CAP_PROP_POS_FRAMES, frame)
    ret, im=v.read()

    joints={'lankle': 1, 'rankle': 0, 'lknee': 3, 'rknee': 2, 'lthi': 5, 'rthi': 4}
    # médian
    img_m=cv2.medianBlur(im,5)
    font=cv2.FONT_HERSHEY_SIMPLEX
    img_m=img_m[0:828, 0:512]
    ng=[]
    
    xjoints=d['frames'][frame][0]['pose2d'][:13]
    yjoints=d['frames'][frame][0]['pose2d'][13:]
    x=xjoints[joints[joint]]
    y=yjoints[joints[joint]] 
    (x_d, y_d)=tools_lcr.RGBtoD((x, y),frame)
    ndg_h1=img_m[y_d, x_d][0]# Original Depth_high
    ndg_b1=img_m[y_d+424, x_d][0]# Depth Original_low
    #print(img_m[(y_d-int((size-1)/2)):(y_d+int((size-1)/2)),(x_d-int((size-1)/2)):(x_d+int((size-1)/2))] )
    for i in range(y_d-int((size-1)/2), y_d+int((size-1)/2)+1):
        for j in range(x_d-int((size-1)/2), x_d+int((size-1)/2)+1):
            z0=(img_m[i,j]*256/6+img_m[i+424,j])[0]/10
            if z0>120 and z0<750:
                ng.append(int(round(z0)))
    
    print(len(ng))
    print(ng)

    ngh=[0]*750
    for h in set(ng):
        ngh[h]=ng.count(h)
  
    zm=ngh.index(max(ngh))*10
    print('max: ',zm)
    print('original: ',ndg_h1*256/6+ndg_b1)
    # mask first 8 bits (high)
    mask = np.zeros(img_m.shape[:2],np.uint8)
    mask[(y_d-int((size-1)/2)):(y_d+int((size-1)/2))+1,(x_d-int((size-1)/2)):(x_d+int((size-1)/2))+1] = 255
    masked_img = cv2.bitwise_and(img_m, img_m, mask=mask) 

    # mask_bas last 8 bits (low)
    mask_bas = np.zeros(img_m.shape[:2],np.uint8)
    mask_bas[(y_d+424-int((size-1)/2)):(y_d+424+int((size-1)/2))+1,(x_d-int((size-1)/2)):(x_d+int((size-1)/2)+1)] = 255
    masked_bas_img = cv2.bitwise_and(img_m, img_m, mask=mask_bas) 
  
    #opencv方法读取-cv2.calcHist（速度最快）
    #图像，通道[0]-灰度图，掩膜-无，灰度级，像素范围
    hist_bas = cv2.calcHist([img_m],[0],mask_bas,[256],[0,256])#11178
    hist_mask = cv2.calcHist([img_m],[0],mask,[256],[0,256])

    fig=plt.figure()  
    ax1=fig.add_subplot(221)
    ax1.imshow(img_m,'gray')
    ax1.set_title('Depth map')
    ax1.scatter(x_d, y_d,s=1,color='red')
    ax1.plot([x_d-size/2,x_d-size/2,x_d+size/2,x_d+size/2,x_d-size/2], [y_d-size/2,y_d+size/2,y_d+size/2,y_d-size/2,y_d-size/2],color='orange')
    ax1.scatter(x_d, y_d+424,s=3,color='red')
    ax1.plot([x_d-size/2,x_d-size/2,x_d+size/2,x_d+size/2,x_d-size/2], [y_d+424-size/2,y_d+424+size/2,y_d+424+size/2,y_d+424-size/2,y_d+424-size/2],color='orange')
   
    ax2=fig.add_subplot(222)
    ax2.set_title('Histogramme')
    ax2.set_xlabel('Distance(cm)')
    #ax2.imshow(mask_bas,'gray')
    ax2.hist(np.array(ng), bins=size**2+1)
    #ax2.scatter(ndg_b1*256/6+ndg_b1, 15, color='orange')
    # low
    ax3=fig.add_subplot(223)
    ax3.set_title('Histogramme bas')
    ax3.plot(hist_bas)
    #print (hist_bas[signal.argrelextrema(hist_bas, np.greater)])# signal.argrelextrema(hist_mask, np.greater) jizhidexiabiao
    #print (signal.argrelextrema(hist_bas, np.greater) )
    ax3.plot(signal.argrelextrema(hist_bas,np.greater)[0],hist_bas[signal.argrelextrema(hist_bas, np.greater)],'o') 
    ax3.plot(signal.argrelextrema(-hist_bas,np.greater)[0],hist_bas[signal.argrelextrema(-hist_bas, np.greater)],'+') 
    
    ndg_b=ndg_b1
    number=hist_bas[ndg_b]
    for i in signal.argrelextrema(hist_bas, np.greater)[0]:       
            #print(i, hist_bas[i])
            if(hist_bas[i]>=number):
                number=hist_bas[i]
                ndg_b=i
    ax3.scatter(ndg_b1, hist_bas[ndg_b1], color='black', s=50)   
    #print('max: ', ndg_b, hist_bas[ndg_b])  

    # hight
    ax4=fig.add_subplot(224)
    ax4.plot(hist_mask)
    ax4.set_title('Histogramme haut')
    #print (hist_mask[signal.argrelextrema(hist_mask, np.greater)])# signal.argrelextrema(hist_mask, np.greater) jizhidexiabiao
    #print (signal.argrelextrema(hist_mask, np.greater) )
    ax4.plot(signal.argrelextrema(hist_mask,np.greater)[0],hist_mask[signal.argrelextrema(hist_mask, np.greater)[0]],'o') 
    ax4.plot(signal.argrelextrema(-hist_mask,np.greater)[0],hist_mask[signal.argrelextrema(-hist_mask, np.greater)[0]],'+') 

    ndg_h=ndg_h1
    number=hist_mask[ndg_h]
    for i in signal.argrelextrema(hist_mask, np.greater)[0]:  
            #print(i, hist_mask[i])         
            if(hist_mask[i]>=number and ((i>=35) and i<155)):
                number=hist_mask[i]
                ndg_h=i
    ax4.scatter(ndg_h1, hist_mask[ndg_h1], color='black', s=50)   
    #print('max: ', ndg_h, hist_mask[ndg_h])      

    plt.show()
    return (zm, ndg_h1*256/6+ndg_b1)


print('! Usage : <nb_video> <frame> <size> <joint(lankle/rankle/lknee/rknee/lthi/rthi)> ')
nb=sys.argv[1]
frame=int(sys.argv[2])
size=int(sys.argv[3])
joint=sys.argv[4]

hist=his(nb,frame,size,joint)
print(hist)
'''
im_h=np.zeros((500,60),np.uint8)

for frame in tqdm(range(70,130)):
    hist=his('2', frame, 11, 'lthi')
    img=hist[6] 
    im_h[ :, frame-70]=img


cv2.namedWindow('img_h', cv2.WINDOW_NORMAL)
cv2.imshow('img_h', im_h)
cv2.waitKey(0) 
cv2.destroyAllWindows()
'''