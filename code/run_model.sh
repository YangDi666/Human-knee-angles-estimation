#!/bin/bash

# Usage : ./run_model.sh <nb_video> <frame_begin> <frame_end> <algo(LCR-NET/OpenPose/PifPaf)> <model(Angles/Angles+/Angles++)> <showfiguers(True/False)> <filter type(gaussian/mean/median/no)> <filter size>
# example1 : ./run_model.sh 1 50 150 LCR-NET Angles++ True gaussian 5
# example2 : ./run_model.sh 1 50 150 OpenPose Angles False


if [ $5 = "Angles" ]; then
    echo $1 $2 $3 $4 $5 $6 $7 $8
    python3 show_result.py $1 angles $2 $3 $4 $5 $6 
elif [ $5 = "Angles+" ]; then
    echo $1 $2 $3 $4 $5 $6 $7 $8
    python3 show_result.py $1 angles $2 $3 $4 $5 $6 
elif [ $5 = "Angles++" ]; then
    echo $1 $2 $3 $4 $5 $6 $7 $8
    python3 show_result.py $1 angles $2 $3 $4 $5 $6 
    if [ $4 = "LCR-NET" ]; then
        python3 findwrong_lcr.py $1 front $6
        python3 correcte_lcr.py $1 front no 0 $6
        python3 findwrong_lcr.py $1 front $6
        python3 correcte_lcr.py $1 front $7 $8 $6
    elif [ $4 = "OpenPose" ]; then
        python3 findwrong_op.py $1 front $6
        python3 correcte_op.py $1 front no 0 $6
        python3 findwrong_op.py $1 front $6
        python3 correcte_op.py $1 front $7 $8 $6
    elif [ $4 = "PifPaf" ]; then
        python3 findwrong_pp.py $1 front $6
        python3 correcte_pp.py $1 front no 0 $6
        python3 findwrong_pp.py $1 front $6 
        python3 correcte_pp.py $1 front $7 $8 $6
    else
        echo "Algorithme error! -- LCR-NET / OpenPose / PifPaf"
    fi
else
    echo "Model error! -- Angles / Angles+ / Angles++"
fi