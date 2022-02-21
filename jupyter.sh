#!/bin/bash

. ./env/bin/activate

# When running implicit ALS
# export OPENBLAS_NUM_THREADS=1

konsole -e "jupyter notebook notebooks --ip 0.0.0.0"
