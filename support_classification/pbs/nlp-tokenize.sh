#!/bin/bash -l
#PBS -l walltime=60:00:00,nodes=1:ppn=8,mem=200gb
#PBS -q ram256g
#PBS -m abe
#PBS -M eriks074@umn.edu
#PBS -N CaringBridge_Support_Tok
#PBS -o /home/srivbane/eriks074/repos/sna-social-support/support_classification/pbs/tok.stdout
#PBS -e /home/srivbane/eriks074/repos/sna-social-support/support_classification/pbs/tok.stderr

working_dir="/home/srivbane/eriks074/repos/sna-social-support/support_classification/pbs/"
cd $working_dir
echo "In '$working_dir', running the script."
python3 nlp-tokenize.py
echo "Finished."
