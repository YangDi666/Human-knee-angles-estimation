import cv2
import matplotlib.pylab as plt
import numpy as np
import math
import pylab as pl
import scipy.signal as signal

CAMERA={
    'FX_C':1081.3720703125,
    'FY_C':-1081.3720703125,
    'CX_C':960.5,
    'CY_C':539.5,
    'FX_D':366.864685058594,
    'FY_D':-366.864685058594,
    'CX_D':263.148010253906, 
    'CY_D':200.292007446289}

def RGBtoD(p, frame):
    if frame<=30:
        c=3.5
    elif frame>=130:
        c=4.5
    else:
        c=4
    x_c=p[0]
    y_c=p[1]
    x_d=round((x_c-CAMERA['CX_C'])/CAMERA['FX_C']*CAMERA['FX_D']+CAMERA['CX_D']+c)
    y_d=round((y_c-CAMERA['CY_C'])/CAMERA['FY_C']*CAMERA['FY_D']+CAMERA['CY_D'])
    #print(x_d)
    #print(y_d)
    #print(type(im[y_d][x_d][0]))
    #print(im[y_d+424][x_d][0])
   
    return (x_d, y_d)

def filter(p, im, size):
    s=(size-1)/2
    (x_d, y_d)=RGBtoD(p)
    win=[im[i,j] for i in range(y_d-s, y_d+s+1) for j in range(x_d-s, x_d+s+1)]
    for k in win:
        if (k>=0 and k<=23) or k>175:
            win.remove(k)
    win=np.array(win)
    return np.median(win)

def RGBto3D(p, im, frame, filter=False, size=0):
        
    x_c=p[0]
    y_c=p[1]
    if frame<=30:
        c=3.5
    elif frame>=130:
        c=4.5
    else:
        c=4
    x_d=round((x_c-CAMERA['CX_C'])/CAMERA['FX_C']*CAMERA['FX_D']+CAMERA['CX_D']+c)
    y_d=round((y_c-CAMERA['CY_C'])/CAMERA['FY_C']*CAMERA['FY_D']+CAMERA['CY_D'])
    #print(x_d)
    #print(y_d)
    #print(type(im[y_d][x_d][0]))
    #print(im[y_d+424][x_d][0])
    if len(p)==2:
        if filter:
            z=his_image(im, size, p, frame)[0]
        else:
            #print(im[round(y_d)][round(x_d)][0])
            z=im[round(y_d)][round(x_d)][0]*256/6+im[round(y_d+424)][round(x_d)][0]
        '''
        if(z==0):
            z1=max([im[y_d+i][x_d+j][0] for i in range(-2,3) for j in range(-2,3)])
            z0=min([im[y_d+i][x_d+j][0] for i in range(-2,3) for j in range(-2,3)])
        
            z=z1*256+z0    
        '''
        x=(x_d-CAMERA['CX_D'])*z/CAMERA['FX_D']
        y=(y_d-CAMERA['CY_D'])*(z)/CAMERA['FY_D']
    else:
        z=p[2]
        x=(x_d-CAMERA['CX_D'])*z/CAMERA['FX_D']
        y=(y_d-CAMERA['CY_D'])*(z)/CAMERA['FY_D']
        
    return (x, y, z)

def angle(p1,p2,p3,alwaysPositive=True):
    n=len(p1)
    # vectors
    v1=[(p1[i]-p2[i]) for i in range(n)]
    v2=[(p3[i]-p2[i]) for i in range(n)]
    # angle = acos( dot(v1,v2) / (len(v1)*len(v2)) )
    dot=sum([(v1[i]*v2[i]) for i in range(n)])
    len_v1=math.sqrt(sum([(v1[i]**2) for i in range(n)]))
    len_v2=math.sqrt(sum([(v2[i]**2) for i in range(n)]))
    if(len_v1!=0 and len_v2!=0):
        if not alwaysPositive and n==3 and (v1[2]<0 and v2[2]<=0):
            return 360-math.degrees(math.acos(dot/(len_v1*len_v2)))
        else:
            return math.degrees(math.acos(dot/(len_v1*len_v2)))
    else:
        return 180

def v2i(cap, frame, save=False): 
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame)  # 设置帧数标记
    ret, im = cap.read()  # read方法返回一个布尔值和一个视频帧
    if ret: 
        if save:
            cv2.imwrite("test1/img/" + str(frame) + "C.jpg", im)
        return im
    else:
        return 'No image!!'
    
def his_image(im, size, p, frame):

    # médian
    #img_m=cv2.medianBlur(im,5)
    #font=cv2.FONT_HERSHEY_SIMPLEX
    img_m=im[0:828, 0:512]
    '''
    img_m_h=img_m[0:424, 0:512]
    img_m_b=img_m[424:828, 0:512]
    for i in range(424):
        for j in range(512):
            img_m[i,j]=img_m_h[i,j]*256/6+img_m_b[i,j]
    '''
   
    x=p[0]
    y=p[1]
    (x_d, y_d)=RGBtoD((x, y),frame)
    ndg_h1=img_m[y_d, x_d][0]# Original Depth_high
    ndg_b1=img_m[y_d+424, x_d][0]# Depth Original_low
    #print(ndg_h1, ndg_b1)
    #print(img_m[(y_d-int((size-1)/2)):(y_d+int((size-1)/2)),(x_d-int((size-1)/2)):(x_d+int((size-1)/2))] )
    ng=[]
    #print(img_m[(y_d-int((size-1)/2)):(y_d+int((size-1)/2)),(x_d-int((size-1)/2)):(x_d+int((size-1)/2))] )
    for i in range(y_d-int((size-1)/2), y_d+int((size-1)/2)+1):
        for j in range(x_d-int((size-1)/2), x_d+int((size-1)/2)+1):
            z0=(img_m[i,j]*256/6+img_m[i+424,j])[0]/10
            if z0>120 and z0<850:
                ng.append(int(round(z0)))
    
    #print(len(ng))
    ngh=[0]*851
    for h in set(ng):
        ngh[h]=ng.count(h)

    zm=ngh.index(max(ngh))*10
    #print(zm)

    return (zm, ndg_h1*256/6+ndg_b1)

def compt(t1, vd, t2, gt, dt, show=False):
    gt_r=[]
    t=[]
    t1=[j-dt for j in t1]
    for i in t1:
        
        if i<=0:
            continue
        elif i<t2[-1]: 
            if ((math.floor(i/10)*10) in t2):
                gt_r.append(gt[t2.index(math.floor(i/10)*10)]+((i%10)/10)*(gt[t2.index(math.floor(i/10)*10)+1]-gt[t2.index(math.floor(i/10)*10)]))
                t.append(i)
            
        else:
            break

    vd_r=[vd[t1.index(j)] for j in t]  
    #err=math.sqrt(sum([(vd_r[k]-gt_r[k])**2 for k in range(len(t))]))    
    err=sum([abs(vd_r[k]-gt_r[k]) for k in range(len(t))])/len(t)  #MSE
    if show:
        fig2=plt.figure()
        axx=fig2.add_subplot(111)
        axx.plot(t1, vd, marker='.')
        axx.plot(t2, gt, marker='.')
        axx.plot(t, gt_r, marker='.')
        axx.text(1000, 60, 'Err: '+str(err))
        axx.text(1000, 70, 'dt: '+str(dt))
    t=[i+dt for i in t]
    return [err, t, gt_r]

def comps(t1, vd, t2, gt, ds, show=False):
    gt_r=[]
    t=[]
    vd=[j-ds for j in vd]
    for i in t1:      
        if i<=0:
            continue
        elif i<t2[-1]: 
            if math.floor(i/10)*10 in t2 and t2.index(math.floor(i/10)*10)<len(gt):
                gt_r.append(gt[t2.index(math.floor(i/10)*10)]+((i%10)/10)*(gt[t2.index(math.floor(i/10)*10)+1]-gt[t2.index(math.floor(i/10)*10)]))
                t.append(i)           
        else:
            break

    vd_r=[vd[t1.index(j)] for j in t]  
    #err=math.sqrt(sum([(vd_r[k]-gt_r[k])**2 for k in range(len(t))]))    
    err=sum([abs(vd_r[k]-gt_r[k]) for k in range(len(t))])/len(t)  #MSE
    if show:
        fig2=plt.figure()
        axx=fig2.add_subplot(111)
        axx.plot(t1, vd, marker='.')
        axx.plot(t2, gt, marker='.')
        axx.plot(t, gt_r, marker='.')
        axx.text(3000, 3000, 'Err: '+str(err))
        axx.text(3000, 2000, 'dy: '+str(ds))
    
    return err

def VIto3D(p, jsondata, aix, joint=0):
    j=jsondata
    dm=j['d'+aix+'m']
    if joint==0:
        if aix=='X':
            k=-p+dm
        if aix=='Y':
            k=-p+dm
        if aix=='Z':
            k=p+dm
    else:
        d=j['d'+aix][joint][0]       
        if aix=='X':
            k=-p+d
        if aix=='Y':
            k=-p+d
        if aix=='Z':
            k=p+d
    return k

def K3DtoRGB(p):
    x=p[0]*(CAMERA['FX_C']/p[2])+CAMERA['CX_C']
    y=p[1]*(CAMERA['FY_C']/p[2])+CAMERA['CY_C']
    return (x,y)

def K3DtoD(p):
    x_d=p[0]*(CAMERA['FX_D']/p[2])+CAMERA['CX_D']
    y_d=p[1]*(CAMERA['FY_D']/p[2])+CAMERA['CY_D']  
    return (x_d,y_d)
    
def DtoRGB(p):
    x_d=p[0]
    y_d=p[1]
    x_c=round((x_d-CAMERA['CX_D']-4)/CAMERA['FX_D']*CAMERA['FX_C']+CAMERA['CX_C'])
    y_c=round((y_d-CAMERA['CY_D'])/CAMERA['FY_D']*CAMERA['FY_C']+CAMERA['CY_C'])
    return (x_c, y_c)

def get_distance(p1, p2):
    s=0
    for i in range(len(p1)):
        s+=(p1[i]-p2[i])**2
    return math.sqrt(s)