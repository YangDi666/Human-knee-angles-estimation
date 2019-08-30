#!/bin/bash

#! You should run the "run_model.sh" first and the different colors represent different result :
# orange : primitive LCR-NET 
# green : primitive OpenPose 
# pink : primitive PifPaf 
# yellow : GT general transformation
# black : GT respective transformation
# purple in 3D : the result of walking model (Angle/Angle+/Angles++)

# Usage : ./3Dshow.sh <nb_video> <frame> <algo(LCR-NET/OpenPose/PifPaf)> <GT calibrated?(True/False)> 
# example : ./3Dshow.sh 2 104 LCR-NET True




if [ $3 = "LCR-NET" ]; then
    python3 3DReconstruction_lcr.py $1 $2 $4
elif [ $3 = "OpenPose" ]; then
    python3 3DReconstruction_op.py $1 $2 $4
elif [ $3 = "PifPaf" ]; then
    python3 3DReconstruction_pp.py $1 $2 $4
else
    echo "Algorithme error! -- LCR-NET / OpenPose / PifPaf"
fi
