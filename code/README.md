
# Knee angles estimation
## I. Pose Estimation (Deep learning)
### LCRNet Video Processing

Based on https://thoth.inrialpes.fr/src/LCR-Net/

This project separates the original demo into two parts:

- demo-predict.py
- demo-show.py

Demo predict should be executed inside the cluster. It creates from a source (.mp4 video), a .json file with the same name with the 2D and 3D skeleton information.

Demo show should be executed locally. It creates, from the original source (.mp4 video) and the previously generated .json file a new video called {source}_detected.mp4 with the original video annotated with the skeleton in 2D and 3D.

#### Cluster installation with Conda

##### Log in to cluster

```bash
ssh nef-devel2
```

##### Install miniconda and create environment

```bash
# download
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
# install
bash Miniconda3-latest-Linux-x86_64.sh
# create environment
conda create -n lcrnet python=3.6
```

##### Download and install  LCR-Net (v2.0)

```bash
# download Detectron.pytorch
git clone https://github.com/roytseng-tw/Detectron.pytorch

# download LCR-Net
git clone https://gitlab.inria.fr/inriatechsophia/lcrnet-videoprocessing

# activate environment
source activate lcrnet

# load modules
module load cuda/9.1
module load cudnn/7.0-cuda-9.1
module load gcc/6.2.0

# install dependencies
conda install pytorch
conda install torchvision
conda install cython
conda install matplotlib
conda install numpy
conda install scipy
conda install opencv
conda install pyyaml
conda install packaging
pip install pycocotools
pip install tensorboardX
pip install tqdm
pip install h5py
```

Detectron.pytorch installation should be done inside a node with a gpu. For this use an interactive job.

```bash
# reserve and enter a node
oarsub -p "gpu='YES' and gpucapability>='5.0'" -l /nodes=1/gpunum=1,walltime=2 -I

# inside the node
cd Detectron.pytorch/lib

# activate environment
source activate lcrnet

# load modules
module load cuda/9.1
module load cudnn/7.0-cuda-9.1
module load gcc/6.2.0

# install
sh make.sh

# create a symbolic link to Detectron.pytorch from lcrnet root

cd ../../lcrnet-videoprocessing
ln -s ../Detectron.pytorch/
```

##### Test installation

```bash
# still inside the node
# execute prediction over the test video
python3 demo-predict.py InTheWild-ResNet50 test/testvideo.mp4 0
```
Once the process is finished, you should see the resulting json file with the 2d and 3d poses for each frame of the video, both displayed in the console and saved into the test folder as testvideo.json

#### Process videos

##### Perform prediction in the cluster

The prediction is done with a pretrained model, downloaded automatically by the script. 

The list of available models are:

- DEMO_ECCV18: model with fast inference time (downscale image, reduce number of classes) that we use for our ECCV'18 demo
- Human3.6-17J-ResNet50: model trained (and evaluated) on Human3.6M dataset to estimate 17 joints
- InTheWild-ResNet50: model trained on real-world (and synthetic) images evaluated on MPII dataset

Downloaded from http://pascal.inrialpes.fr/data2/grogez/LCR-Net/pthmodels/

Check the job.oar file and modify it to point to your working path and conda environment accordingly.

```bash
# copy your video to the cluster
scp -r {source}.mp4 nef-devel2:/home/{user}/lcrnet-videoprocessing/

# log in to cluster
ssh nef-devel2
cd lcrnet-videoprocessing

# submit job
oarsub -S "lcrnet-videoprocessing/job.oar {source}.mp4 {modelname}"

```

After the job is finished you should find the generated {source}.json file in the lcrnet-videoprocessing folder.  Check the log files (OAR*.stdout and OAR*.stderr) for the job progress and error.

##### Install lcrnet-videoprocessing locally

To join the videos and the obtained skeleton locally, you will need to download the lcrnet-videoprocessing project and install the demo-show dependencies. No gpu is needed for this step.

Dependencies:
- python=3.6
- numpy
- opencv-python
- matplotlib
- tqdm

##### Create the annotated video

```bash
# copy the json file from the cluster
scp -r nef-devel2:/home/{user}/lcrnet-videoprocessing/{source}.json ./

# perform prediction
python3 demo-show.py {source}.mp4
```

The result will be displayed while creating the video, and will finally be saved under the name {source}_detected.mp4
 

### OpenPose 

#### Download

```bash
git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git
```
#### Installation  

https://github.com/CMU-Perceptual-Computing-Lab/openpose#quick-start

#### Run model on the NEF at Inria : 

```bash
module use --append /home/mkopersk/share/modules
module load cuda/8.0
module load cudnn/5.1-cuda-8.0
module load opencv2/no_python_with_gpu
module load Caffe/open_pose
```

Then you can notice that if you just type: openpose.bin command is available so you can just type:
openpose.bin  -help

```bash
# Example1 : 
openpose.bin --image_dir ~/workspace/videos/group_meeting_presentaiton/Drink.Fromcup_p06_r02_v09_c01/ -model_folder /home/mkopersk/3rdParty/open_pose/openpose/models/ --model_pose COCO --net_resolution 656x496 --scale_number 4 --scale_gap 0.25

# Example2 : Save results, and turn off the display
openpose.bin --image_dir ~/workspace/videos/group_meeting_presentaiton/Drink.Fromcup_p06_r02_v09_c01/ -model_folder /home/mkopersk/3rdParty/open_pose/openpose/models/ --model_pose COCO --net_resolution 656x496 --scale_number 4 --scale_gap 0.25 -write_keypoint_json ~/workspace/videos/ouput/ --no_display
```

### PifPaf

#### Download
```bash
- git clone https://github.com/vita-epfl/openpifpaf.git
```
#### Installation 

https://github.com/vita-epfl/openpifpaf#Install

#### install dependencies

```bash
- source activate pifpaf

- pip3 install openpifpaf
- pip3 install numpy cython
- pip3 install --editable '.[train,test]'
```

### Videos

```bash
export VIDEO=video.avi  # change to your video file
mkdir ${VIDEO}.images
ffmpeg -i ${VIDEO} -qscale:v 2 -vf scale=641:-1 -f image2 ${VIDEO}.images/%05d.jpg
python3 -m openpifpaf.predict --checkpoint resnet152 ${VIDEO}.images/*.jpg
ffmpeg -framerate 24 -pattern_type glob -i ${VIDEO}.images/'*.jpg.skeleton.png' -vf scale=640:-2 -c:v libx264 -pix_fmt yuv420p ${VIDEO}.pose.mp4
```

## II. Knee Angles Estimation

### File storage : 
```bash
- testVideos
    --test1
        ---...C.mp4
        ---...D.mp4
        ---...C.json  (lcrnet)
        ---...Copenpose.json
        ---...Cpifpaf.json
    --test2
    --test3
    --...
```
### Walking models

We can run the "run_model.sh" for the knee angles estimation based on the 2D pose of LCR-NET, OpenPose or PifPaf
```bash
Usage : ./run_model.sh <nb_video> <frame_begin> <frame_end> <algo(LCR-NET/OpenPose/PifPaf)> <model(Angles/Angles+/Angles++)> <showfiguers(True/False)> <filter type(gaussian/mean/median/no)> <filter size>

- # example1 : 
./run_model.sh 1 50 150 LCR-NET Angles++ True gaussian 5  (if you run the "Angles++" model you should add the last 2 parameters)
- # example2 : 
./run_model.sh 1 50 150 OpenPose Angles False
```
then we can get the result (file.csv) :

- 1536334071006611046_LCR-NET_joints_2DColor_front
- 1536334071006611046_LCR-NET_joints_2DDepth_front
- 1536334071006611046_LCR-NET_joints_3DKinect_front
- 1536334071006611046_OpenPose_joints_2DColor_front
- ...
- ...
- 1536334071006611046_PifPaf_joints_2DColor_front
- ...
- ...

### Display the results

To show the results of the models and the pose estimation, you can run "3Dshow.sh"after running "run_modle.sh" then you can see the different colors represent different result :
- orange : primitive LCR-NET 
- green : primitive OpenPose 
- pink : primitive PifPaf 
- yellow : GT general transformation
- black : GT respective transformation
- purple in 3D : the result of walking model (Angle/Angle+/Angles++)

```bash
Usage : ./3Dshow.sh <nb_video> <frame> <algo(LCR-NET/OpenPose/PifPaf)> <GTcalibrated?(True/False)> 

- # example : 
./3Dshow.sh 2 104 LCR-NET False
```
### Exploration

There are some script during the exploration of Angles+ and Angles++

#### Angles+ 
- hist_image.py : it can draw a histogram for a joints. Usage : <nb_video> <frame> <size> <joint(lankle/rankle/lknee/rknee/lthi/rthi)> 
- hist_img.py : this code is for draw a image which represent the histogram of a entire video. Usage : <nb_video> <right/left> <size> and you can see the image of right/left ankle, hip, knee.
- histogram.py : this code is for comparaing the value selection method id depth map : median or the maxum of the histogram or both. Usage : <nb_video> <size for histogram> <size for median>


#### Angles++ 
- findwrong.py : we can detect the bad frames by the walking model. Usage : python3 findwrong.py <nb_video> <direction(front/back)> <showfigures> ex : 1 front True')
- correcte.py : walking model for correcting the bad frames. Usage: python3 correcte.py <nb_video> <direction(front/back)> <filter(gaussian/mean/median)> <filter kernel size> <showfigures> ex : 1 front gaussian 5 True')
   
