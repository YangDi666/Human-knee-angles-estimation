#!/bin/bash
#! You should run the "run_model.sh" first and put the vicon file in the folder like test1 - test5 :

# Usage : ./calibration.sh <nb_video> <frame_begin> <frame_end> <algo(LCR-NET/OpenPose/PifPaf)> <direction(f/b)> <show figures> (frame begin and end should be the same with "run_model")
# example : ./calibration.sh 2 50 150 LCR-NET f True

echo $1 $2 $3 $4 $5
python3 time_recalage.py $1 $5 $2 $3 $4 $6
python3 space_recalage.py $1 $5 $2 $3 $4 $6
python3 gt_generator.py $1 $5 $2 $3 $4 $6
