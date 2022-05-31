#!/bin/bash

# make datacards for both old (-o) and new ADD samples with full data sample
# blinded (-b) and non-blinded
python python/runLimits.py -c -b True -o 
python python/runLimits.py -c -o
python python/runLimits.py -c -b True
python python/runLimits.py -c

# only use newer ADD samples
for year in 2016 2017 2018 2016,2017 2016,2018 2017,2018
do 
    python python/runLimits.py -c -b True -y $year
    python python/runLimits.py -c -y $year
done

# compute limits for old (-o) and new samples with full data sample
# blinded (-b) and non-blinded
#python python/runLimits.py -c -b True -o -r 
#python python/runLimits.py -c -o -r 
#python python/runLimits.py -c -b True -r 
#python python/runLimits.py -c -r 

# with new samples

python python/makeNuisance.py
for years in 2016 2017 2018 2016,2017 2016,2018 2017,2018
do 
    python python/makeNuisance.py -y $year
done
