#!/bin/bash
echo "Enter last iteration of training"
# read iter
../caffe/tools/caffe train -solver data/solver.prototxt -snapshot data/MYNET_iter_55000.solverstate