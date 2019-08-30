""" LCR-Net: Localization-Classification-Regression for Human Pose
Copyright (C) 2017 Gregory Rogez & Philippe Weinzaepfel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>"""

import sys, os, pdb, json
import numpy as np
import pickle
from PIL import Image
import cv2
import scene
import matplotlib.pylab as plt

from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm
import math

plt.ion()

def show_animation(outputname,animation_meta, njts):
    fig = plt.figure()

    ax2d = fig.add_subplot(211)

    ax2d.set_xticks([])
    ax2d.set_yticks([])

    ax3d = fig.add_subplot(235, projection='3d')
    ax3d.set_aspect('equal')
    ax3d.elev = -90
    ax3d.azim = 90
    ax3d.dist = 8
    ax3d.set_xlabel('X axis', labelpad=-5)
    ax3d.set_ylabel('Y axis', labelpad=-5)
    ax3d.set_zlabel('Z axis', labelpad=-5)
    ax3d.set_xticklabels([])
    ax3d.set_yticklabels([])
    ax3d.set_zticklabels([])

    ax3d_left = fig.add_subplot(234, projection='3d')
    ax3d_left.set_aspect('equal')
    ax3d_left.elev = -90
    ax3d_left.azim = 90
    ax3d_left.dist = 8
    ax3d_left.set_xlabel('X axis', labelpad=-5)
    ax3d_left.set_ylabel('Y axis', labelpad=-5)
    ax3d_left.set_zlabel('Z axis', labelpad=-5)
    ax3d_left.set_xticklabels([])
    ax3d_left.set_yticklabels([])
    ax3d_left.set_zticklabels([])

    ax3d_right = fig.add_subplot(236, projection='3d')
    ax3d_right.set_aspect('equal')
    ax3d_right.elev = -90
    ax3d_right.azim = 90
    ax3d_right.dist = 8
    ax3d_right.set_xlabel('X axis', labelpad=-5)
    ax3d_right.set_ylabel('Y axis', labelpad=-5)
    ax3d_right.set_zlabel('Z axis', labelpad=-5)
    ax3d_right.set_xticklabels([])
    ax3d_right.set_yticklabels([])
    ax3d_right.set_zticklabels([])

    bones = get_bones(njts)

    def animate(i):
        image, detections = animation_meta[i]
        for a in animate.anims:
            a.remove()
        animate.anims = []
        animate.anims += [ax2d.imshow(image)]

        for det in detections:
            score = det['cumscore']
            angle_left = det['angle_left']
            angle_right = det['angle_right']
            lw = 2

            det_left=[0]*njts*3
            det_left[0:njts]=det['pose3d'][2*njts:3*njts]# zhi qu 3 ge jiu xing
            det_left[njts:2*njts]=det['pose3d'][njts:2*njts]
            det_left[2*njts:3*njts]=[-x for x in det['pose3d'][:njts]]
            
            det_right=[0]*njts*3
            det_right[0:njts]=[-x for x in det['pose3d'][2*njts:3*njts]]# zhi qu 3 ge jiu xing
            det_right[njts:2*njts]=det['pose3d'][njts:2*njts]
            det_right[2*njts:3*njts]=det['pose3d'][:njts]
            # 2d axis
            animate.anims += display_2d(ax2d,det['pose2d'],bones,njts,score,lw)
            # 3d axis
            animate.anims += display_3d(ax3d,det['pose3d'],bones,njts,score,lw,'m')
            # 3d axis_left
            animate.anims += display_3d(ax3d_left,det_left,bones,13,angle_left,lw,'l')          
            # 3d axis_right
            animate.anims += display_3d(ax3d_right,det_right,bones,13,angle_right,lw,'r')
            

        return animate.anims

    animate.anims = []

    anim = animation.FuncAnimation(fig, animate, frames=len(animation_meta), interval=50, blit=True)

    anim.save(outputname)
    # plt.show()
    # pdb.set_trace()

def get_bones(njts):
    bones = {}
    if njts==13:
        bones['left']  = [(9,11),(7,9),(1,3),(3,5)] # bones on the left
        bones['right'] = [(0,2),(2,4),(8,10),(6,8)] # bones on the right
        bones['right'] += [(4,5),(10,11)] # bones on the torso
        # (manually add bone between middle of 4,5 to middle of 10,11, and middle of 10,11 and 12)
        bones['head'] = 12
    elif njts==17:
        bones['left']  = [(9,11),(7,9),(1,3),(3,5)] # bones on the left
        bones['right'] = [(0,2),(2,4),(8,10),(6,8)] # bones on the right and the center
        bones['right'] += [(4,13),(5,13),(13,14),(14,15),(15,16),(12,16),(10,15),(11,15)]  # bones on the torso
        bones['head'] = 16
    return bones

def display_2d(ax,pose2d,bones,njts,score,lw):
    # draw green lines on the left side
    artists = []
    for i,j in bones['left']:
        p, = ax.plot( [pose2d[i],pose2d[j]],[pose2d[i+njts],pose2d[j+njts]],'g', scalex=None, scaley=None, lw=lw)
        artists += [p]
    # draw blue linse on the right side and center
    for i,j in bones['right']:
        p, = ax.plot( [pose2d[i],pose2d[j]],[pose2d[i+njts],pose2d[j+njts]],'b', scalex=None, scaley=None, lw=lw)
        artists += [p]
        
    if njts==13:   # other bones on torso for 13 jts
        def avgpose2d(a,b,offset=0): # return the coordinate of the middle of joint of index a and b
            return (pose2d[a+offset]+pose2d[b+offset])/2.0         
        p1, = ax.plot( [avgpose2d(4,5),  avgpose2d(10,11)], [avgpose2d(4,5,offset=njts),  avgpose2d(10,11,offset=njts)], 'b', scalex=None, scaley=None, lw=lw)
        p2, = ax.plot( [avgpose2d(12,12),avgpose2d(10,11)], [avgpose2d(12,12,offset=njts),avgpose2d(10,11,offset=njts)], 'b', scalex=None, scaley=None, lw=lw)        
        artists += [p1,p2]
    # put red markers for all joints
    p, = ax.plot(pose2d[0:njts], pose2d[njts:2*njts], color='r', marker='.', linestyle = 'None', scalex=None, scaley=None)
    # legend and ticks
    t = ax.text(pose2d[bones['head']]-20, pose2d[bones['head']+njts]-20, '%.1f'%(score), color='blue')
    
    artists += [p,t]
    return artists


def display_3d(ax,pose3d,bones,njts,score,lw,a):
    artists = []
    def get_pair(i,j,offset): 
        return [pose3d[i+offset],pose3d[j+offset]]
    def get_xyz_coord(i,j): 
        return get_pair(i,j,0), get_pair(i,j,njts), get_pair(i,j,njts*2)
    # draw green lines on the left side
    for i,j in bones['left']:
        x,y,z = get_xyz_coord(i,j)
        p, = ax.plot( x, y, z, 'g', scalex=None, scaley=None, lw=lw)
        artists += [p]
    # draw blue linse on the right side and center
    for i,j in bones['right']:
        x,y,z = get_xyz_coord(i,j)
        p, = ax.plot( x, y, z, 'b', scalex=None, scaley=None, lw=lw)
        artists += [p]
    if njts==13: # other bones on torso for 13 jts
        def avgpose3d(a,b,offset=0): 
            return (pose3d[a+offset]+pose3d[b+offset])/2.0
        def get_avgpair(i1,i2,j1,j2,offset):
            return [avgpose3d(i1,i2,offset),avgpose3d(j1,j2,offset)]
        def get_xyz_avgcoord(i1,i2,j1,j2): 
            return get_avgpair(i1,i2,j1,j2,0), get_avgpair(i1,i2,j1,j2,njts), get_avgpair(i1,i2,j1,j2,njts*2)
        x,y,z = get_xyz_avgcoord(4,5,10,11)
        p1, = ax.plot( x, y, z, 'b', scalex=None, scaley=None, lw=lw)
        x,y,z = get_xyz_avgcoord(12,12,10,11)
        p2, = ax.plot( x, y, z, 'b', scalex=None, scaley=None, lw=lw)
        artists += [p1,p2]
    # put red markers for all joints
    p, = ax.plot( pose3d[0:njts], pose3d[njts:2*njts], pose3d[2*njts:3*njts], color='r', marker='.', linestyle = 'None', scalex=None, scaley=None)
    # score
    if(a=='m'):
        t = ax.text(pose3d[bones['head']]+0.1, pose3d[bones['head']+njts]+0.1, pose3d[bones['head']+2*njts], '%.1f'%(score), color='blue')
    elif(a=='l'):
        t = ax.text(pose3d[3]+0.1, pose3d[3+njts]+0.1, pose3d[3+2*njts], '%.1f'%(score), color='blue')
    elif(a=='r'):
        t = ax.text(pose3d[2]+0.1, pose3d[2+njts]+0.1, pose3d[2+2*njts], '%.1f'%(score), color='blue')
    artists += [p,t]
    return artists

def display_poses(i, image, detections, njts):

    

    fig = plt.figure()
    
    # 2D 
    ax2d = fig.add_subplot(211)
    ax2d.imshow(image)
    ax2d.set_xticks([])
    ax2d.set_yticks([])

    # 3D 
    ax3d = fig.add_subplot(212, projection='3d')
    ax3d.set_aspect('equal')
    ax3d.elev = -90
    ax3d.azim = 90
    ax3d.dist = 8
    ax3d.set_xlabel('X axis', labelpad=-5)
    ax3d.set_ylabel('Y axis', labelpad=-5)
    ax3d.set_zlabel('Z axis', labelpad=-5)
    ax3d.set_xticklabels([])
    ax3d.set_yticklabels([])
    ax3d.set_zticklabels([])

    # detections
    bones = get_bones(njts)
    for det in detections:
        score = det['cumscore']
        lw = 2
        # 2d axis
        display_2d(ax2d,det['pose2d'],bones,njts,score,lw)
        # 3d axis
        display_3d(ax3d,det['pose3d'],bones,njts,score,lw,'m')

    plt.show()
    # pdb.set_trace()

def RGBtoD(p):
    CAMERA={
    'FX_C':1081.3720703125,
    'FY_C':-1081.3720703125,
    'CX_C':960.5,
    'CY_C':539.5,
    'FX_D':366.864685058594,
    'FY_D':-366.864685058594,
    'CX_D':263.148010253906, 
    'CY_D':200.292007446289}

    x_c=p[0]
    y_c=p[1]
    x_d=round((x_c-CAMERA['CX_C'])/CAMERA['FX_C']*CAMERA['FX_D']+CAMERA['CX_D'])+30
    y_d=round((y_c-CAMERA['CY_C'])/CAMERA['FY_C']*CAMERA['FY_D']+CAMERA['CY_D'])
    #print(x_d)
    #print(y_d)
    #print(type(im[y_d][x_d][0]))
    #print(im[y_d+424][x_d][0])
   
    return (x_d, y_d)

def demo( imagename):

    with open(imagename[:-5]+'C.json') as json_data:
        d = json.load(json_data)

    K = d['K']
    njts = d['njts']

    if imagename[-4:] == '.mp4':
        img_output_list = []
        video_reader = cv2.VideoCapture(imagename)
        nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
        for i in tqdm(range(nb_frames-1)):
            _, image = video_reader.read()
            img_output_list += [(image, None)]
        video_reader.release()

    else:
        image=cv2.imread(imagename)
        img_output_list = [(image, None)]

    projmat = np.load( os.path.join(os.path.dirname(__file__),'standard_projmat.npy') )
    projMat_block_diag, M = scene.get_matrices(projmat, njts)

    animation_meta = []

    for i,(image,_) in  tqdm(enumerate(img_output_list)): # for each image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        resolution = image.shape[:2]

        # perform postprocessing
        # print('postprocessing (PPI) on image ', str(i))
        
        detections = []

        for detection in d['frames'][i]:
            for i in range(13):
                p2d=RGBtoD((detection['pose2d'][i], detection['pose2d'][i+13]))
                detection['pose2d'][i]=p2d[0]
                detection['pose2d'][i+13]=p2d[1]
            det = {}
            det['cumscore'] = np.float32(detection['cumscore'])
            det['angle_left'] = np.float32(detection['angle_left'])
            det['angle_right'] = np.float32(detection['angle_right'])
            det['pose2d'] = np.array(detection['pose2d'])
            det['pose3d'] = np.array(detection['pose3d'])
            detections.append(det)
        # move 3d pose into scene coordinates
        # print('3D scene coordinates regression on image ', str(i))
        for detection in detections:
          delta3d = scene.compute_reproj_delta_3d(detection, projMat_block_diag, M, njts)
          detection['pose3d'][      :  njts] += delta3d[0]
          detection['pose3d'][  njts:2*njts] += delta3d[1]
          detection['pose3d'][2*njts:3*njts] -= delta3d[2]
        animation_meta += [(image,detections)];
        # show results
        # print('displaying results of image ', str(i))
        # display_poses(i, image, detections, njts)
    show_animation(imagename[:-4]+'_detected.mp4',animation_meta,njts)
    


if __name__=="__main__":
    if len(sys.argv) not in [1, 2]:
        print("Usage: python demo.py <imagename>")
        sys.exit(1)
    imagename = sys.argv[1]
    if not os.path.isfile(imagename):
        print("ERROR: Image {:s} does not exist".format(imagename))
        sys.exit(1)
    #if modelname not in ['H36_R50_1M4_K100_fg7
    #    print("ERROR: Unknown modelname {:s}, it should be R50FPN_2M7_K100x2_fg5".format(modelname))
    #    sys.exit(1)
    
    demo(imagename)
