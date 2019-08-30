# Angles+ : This code is for draw a image which represent the histogram of a entire video
# Usage : <nb_video> <right/left> <size>
#and you can see the image of right/left ankle, hip, knee.

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
#import hist_image
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
    (x_d, y_d)=tools_lcr.RGBtoD((x, y), frame)
    ndg_h1=img_m[y_d, x_d][0]# Original Depth_high
    ndg_b1=img_m[y_d+424, x_d][0]# Depth Original_low
    #print(img_m[(y_d-int((size-1)/2)):(y_d+int((size-1)/2)),(x_d-int((size-1)/2)):(x_d+int((size-1)/2))] )
    for i in range(y_d-int((size-1)/2), y_d+int((size-1)/2)+1):
        for j in range(x_d-int((size-1)/2), x_d+int((size-1)/2)+1):
            z0=(img_m[i,j]*256/6+img_m[i+424,j])[0]/10
            if z0>200 and z0<700:
                ng.append(int(round(z0))-200)
    
    #print(len(ng))
  

    img_hist = np.zeros((1,500),np.uint8)
    for h in set(ng):
        img_hist[0, h]=ng.count(h)
    maxi=np.max(img_hist)
    mini=np.min(img_hist)
    for im in range(500):
        img_hist[0,im]=round((img_hist[0,im]-mini)/(maxi-mini)*255)     
    #print(img_hist)


    # mask first 8 bits (high)
    mask = np.zeros(img_m.shape[:2],np.uint8)
    mask[(y_d-int((size-1)/2)):(y_d+int((size-1)/2))+1,(x_d-int((size-1)/2)):(x_d+int((size-1)/2))+1] = 255
    masked_img = cv2.bitwise_and(img_m, img_m, mask=mask) 

    # mask_bas last 8 bits (low)
    mask_bas = np.zeros(img_m.shape[:2],np.uint8)
    mask_bas[(y_d+424-int((size-1)/2)):(y_d+424+int((size-1)/2))+1,(x_d-int((size-1)/2)):(x_d+int((size-1)/2)+1)] = 255
    masked_bas_img = cv2.bitwise_and(img_m, img_m, mask=mask_bas) 
  
    #opencv方法读取
    hist_bas = cv2.calcHist([img_m],[0],mask_bas,[256],[0,256])#11178
    hist_mask = cv2.calcHist([img_m],[0],mask,[256],[0,256])

    '''
    ndg_b=ndg_b1
    number=hist_bas[ndg_b]
    for i in signal.argrelextrema(hist_bas, np.greater)[0]:       
            #print(i, hist_bas[i])
            if(hist_bas[i]>=number):
                number=hist_bas[i]
                ndg_b=i
    ndg_h=ndg_h1
    number=hist_mask[ndg_h]
    for i in signal.argrelextrema(hist_mask, np.greater)[0]:  
            #print(i, hist_mask[i])         
            if(hist_mask[i]>=number and ((i>=35) and i<155)):
                number=hist_mask[i]
                ndg_h=i
    '''

    return (ndg_h1, ndg_b1, ndg_h1*256/6+ndg_b1, img_hist)

im_h=np.zeros((500,65),np.uint8)
print('Usage : <nb_video> <right/left> <size>')
nb=sys.argv[1]
d=sys.argv[2]
size=int(sys.argv[3])

if d=='right':
    for frame in tqdm(range(70,135)):
        hist=his(nb, frame, size, 'rankle')
        img=hist[3] 
        im_h[ :, frame-70]=img
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.set_xlabel('frame (70 à 135)', labelpad=-3)
    ax.set_ylabel('distance-200 (cm)', labelpad=-3)
    ax.set_title('Right Ankle_'+str(size)+'*'+str(size))
    ax.imshow(im_h, 'gray')

    for frame in tqdm(range(70,135)):
        hist=his(nb, frame, size, 'rthi')
        img=hist[3] 
        im_h[ :, frame-70]=img
    fig2=plt.figure()
    ax2=fig2.add_subplot(111)
    ax2.set_xlabel('frame (70 à 135)', labelpad=-3)
    ax2.set_ylabel('distance-200 (cm)', labelpad=-3)
    ax2.set_title('Right Thigh_'+str(size)+'*'+str(size))
    ax2.imshow(im_h, 'gray')

    for frame in tqdm(range(70,135)):
        hist=his(nb, frame, size, 'rknee')
        img=hist[3] 
        im_h[ :, frame-70]=img
    fig3=plt.figure()
    ax3=fig3.add_subplot(111)
    ax3.set_xlabel('frame (70 à 135)', labelpad=-3)
    ax3.set_ylabel('distance-200 (cm)', labelpad=-3)
    ax3.set_title('Right Knee_'+str(size)+'*'+str(size))
    ax3.imshow(im_h, 'gray')
else:
    for frame in tqdm(range(70,135)):
        hist=his(nb, frame, size, 'lankle')
        img=hist[3] 
        im_h[ :, frame-70]=img
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.set_xlabel('frame (70 à 135)', labelpad=-3)
    ax.set_ylabel('distance-200 (cm)', labelpad=-3)
    ax.set_title('Left Ankle_'+str(size)+'*'+str(size))
    ax.imshow(im_h, 'gray')

    for frame in tqdm(range(70,135)):
        hist=his(nb, frame, size, 'lthi')
        img=hist[3] 
        im_h[ :, frame-70]=img
    fig2=plt.figure()
    ax2=fig2.add_subplot(111)
    ax2.set_xlabel('frame (70 à 135)', labelpad=-3)
    ax2.set_ylabel('distance-200 (cm)', labelpad=-3)
    ax2.set_title('Left Thigh_'+str(size)+'*'+str(size))
    ax2.imshow(im_h, 'gray')

    for frame in tqdm(range(70,135)):
        hist=his(nb, frame, size, 'lknee')
        img=hist[3] 
        im_h[ :, frame-70]=img
    fig3=plt.figure()
    ax3=fig3.add_subplot(111)
    ax3.set_xlabel('frame (70 à 135)', labelpad=-3)
    ax3.set_ylabel('distance-200 (cm)', labelpad=-3)
    ax3.set_title('Left Knee_'+str(size)+'*'+str(size))
    ax3.imshow(im_h, 'gray')
plt.show()
