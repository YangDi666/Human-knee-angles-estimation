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
from detect_pose import detect_pose
from lcr_net_ppi import LCRNet_PPI
import scene
from tqdm import tqdm
import cv2
import math


def demo( imagename, modelname, gpuid):

    fname = os.path.join(os.path.dirname(__file__), 'models', modelname+'.pkl')
    if not os.path.isfile(fname):
        # Download the files 
        dirname = os.path.dirname(fname)
        if not os.path.isdir(os.path.dirname(fname)):
            os.system('mkdir -p "{:s}"'.format(dirname))
        os.system('wget http://pascal.inrialpes.fr/data2/grogez/LCR-Net/pthmodels/{:s} -P {:s}'.format(modelname+'.pkl', dirname))        
        if not os.path.isfile(fname):
            raise Exception("ERROR: download incomplete")

    with open(fname, 'rb') as fid:
      model = pickle.load(fid)
            
    anchor_poses = model['anchor_poses']

    print(anchor_poses.shape)
    K = anchor_poses.shape[0]
    njts = anchor_poses.shape[1]//5 # 5 = 2D + 3D
    
    if imagename[-4:] == '.mp4':
        img_output_list = []
        video_reader = cv2.VideoCapture(imagename)

        nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))

        for i in tqdm(range(nb_frames-1)):
            _, image = video_reader.read()
            # image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
            img_output_list += [(image, None)]

        video_reader.release()

    else:
        image=cv2.imread(imagename)
        # image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        # image = np.asarray(Image.open(imagename))
        img_output_list = [(image, None)]

    print(len(img_output_list))    
    
    projmat = np.load( os.path.join(os.path.dirname(__file__),'standard_projmat.npy') )
    projMat_block_diag, M = scene.get_matrices(projmat, njts)
    jsondata = {}

    jsondata['K'] = K
    jsondata['njts'] = njts
    jsondata['frames'] = []

    # run lcrnet on a list of images
    print("Pose detection starting")
    res = detect_pose( img_output_list, model['model'], model['cfg'], anchor_poses, njts, gpuid=gpuid)
    print("Pose detection finished")
    for i,(image,_) in enumerate(img_output_list): # for each image
        
        jsondata['frames'] += [[]]


        resolution = image.shape[:2]

        # perform postprocessing
        print('postprocessing (PPI) on image ', str(i))
        detections = LCRNet_PPI(res[i], K, resolution, J=njts, **model['ppi_params'])             
        
        # move 3d pose into scene coordinates
        print('3D scene coordinates regression on image ', str(i))
        for detection in detections:
          det = {}
          det['cumscore'] = detection['cumscore'].item()
          det['pose2d'] = detection['pose2d'].tolist()
          det['pose3d'] = detection['pose3d'].tolist()

          # angle for 3 points
          det['angle_left']=angle(get_pos(det,njts,2),get_pos(det,njts,4),get_pos(det,njts,6))
          det ['angle_right']=angle(get_pos(det,njts,1),get_pos(det,njts,3),get_pos(det,njts,5))
          
          jsondata['frames'][i].append(det)

    print('Saving jsondata of image ', str(i))
    print(jsondata)
    with open(imagename[:-4]+'.json', 'w') as outfile:
        json.dump(jsondata, outfile)


def angle(p1,p2,p3):
    n=len(p1)
    # vectors
    v1=[(p1[i]-p2[i]) for i in range(n)]
    v2=[(p3[i]-p2[i]) for i in range(n)]
    # angle = acos( dot(v1,v2) / (len(v1)*len(v2)) )
    dot=sum([(v1[i]*v2[i]) for i in range(n)])
    len_v1=math.sqrt(sum([(v1[i]**2) for i in range(n)]))
    len_v2=math.sqrt(sum([(v2[i]**2) for i in range(n)]))
    if(len_v1!=0 and len_v2!=0):
        return math.degrees(math.acos(dot/(len_v1*len_v2)))
    else:
        return '999999!'


def get_pos(det, njts, point):
    return (det['pose3d'][point-1],det['pose3d'][point+njts-1],det['pose3d'][point+2*njts-1])


if __name__=="__main__":
    if len(sys.argv) not in [3,4]:
        print("Usage: python demo.py <modelname> <imagename> [<gpuid>]")
        sys.exit(1)
    modelname = sys.argv[1]
    imagename = sys.argv[2]
    gpuid = int(sys.argv[3]) if len(sys.argv)>3 else -1
    if not os.path.isfile(imagename):
        print("ERROR: Image {:s} does not exist".format(imagename))
        sys.exit(1)
    #if modelname not in ['H36_R50_1M4_K100_fg7
    #    print("ERROR: Unknown modelname {:s}, it should be R50FPN_2M7_K100x2_fg5".format(modelname))
    #    sys.exit(1)
    
    demo(imagename, modelname, gpuid)
