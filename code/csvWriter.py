# You can create .csv file by this code for each joint
# Usage : <nb_video> <videoname without ".mp4"> <algo>
import json
import pandas as pd
from tqdm import tqdm
import sys
import re

if len(sys.argv)!=4:
    print('Usage : <nb_video> <videoname without ".mp4"> <algo>')
n=sys.argv[1]
name=sys.argv[2]
algo=sys.argv[3]
print(name)
if algo=='LCR-NET':
    with open('testVideos'+'/test'+n+'/'+name+'.json') as json_data:
        d = json.load(json_data)
if algo=='OpenPose':
    with open('testVideos'+'/test'+n+'/'+name+'openpose.json') as json_data:
        d = json.load(json_data)
if algo=='PifPaf':
    with open('testVideos'+'/test'+n+'/'+name+'pifpaf.json') as json_data:
        d = json.load(json_data)

njts = d['njts']
list_frames=d['frames']
print(len(list_frames))
for j in tqdm(range(14)):
    if(j<=12):
        data={'frame':[], 'x2d_'+str(j+1):[], 'y2d_'+str(j+1):[],'x3d_'+str(j+1):[], 'y3d_'+str(j+1):[],'z3d_'+str(j+1):[]}
        for i in range(len(list_frames)):    
            data['frame'].append(i+1)
            if (list_frames[i]==[]):
                data['x2d_'+str(j+1)].append('No')
                data['y2d_'+str(j+1)].append('No')
                data['x3d_'+str(j+1)].append('No')
                data['y3d_'+str(j+1)].append('No')
                data['z3d_'+str(j+1)].append('No')
            else:
                data['x2d_'+str(j+1)].append(list_frames[i][0]['pose2d'][j])
                data['y2d_'+str(j+1)].append(list_frames[i][0]['pose2d'][j+njts])
                if algo=='LCR-NET':
                    data['x3d_'+str(j+1)].append(list_frames[i][0]['pose3d'][j])
                    data['y3d_'+str(j+1)].append(list_frames[i][0]['pose3d'][j+njts])
                    data['z3d_'+str(j+1)].append(list_frames[i][0]['pose3d'][j+2*njts])
                else:
                    data['x3d_'+str(j+1)].append('no')
                    data['y3d_'+str(j+1)].append('no')
                    data['z3d_'+str(j+1)].append('no')
        data=pd.DataFrame(data)

        data.to_csv('testVideos'+'/test'+n+'/test'+n+'_'+algo+'_point'+str(j+1)+'.csv',encoding='gbk')

    else:
        if algo!='PifPaf':
            data={'frame':[], 'angle_left':[], 'angle_right':[]}
            for i in range(len(list_frames)):    
                data['frame'].append(i+1)
                if (list_frames[i]==[]):
                    data['angle_left'].append('No')
                    data['angle_right'].append('No')
                else:
                    data['angle_left'].append(list_frames[i][0]['angle_left'])
                    data['angle_right'].append(list_frames[i][0]['angle_right'])
            data=pd.DataFrame(data)

            data.to_csv('testVideos'+'/test'+n+'/test'+n+'_'+algo+'_angles.csv',encoding='gbk')
   
