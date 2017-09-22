#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=72:00:00
#PBS -l mem=48gb
#PBS -S /bin/bash
#PBS -N echoRD_weiher_hdf
#PBS -j oe
#PBS -o LOG_weiher_hdf
#PBS -n

#cd /beegfs/work/ka_oj4748

echo "User:"
whoami
echo "Job running on node:"
uname -a
echo "started on "
date
echo "- - - - - - - - - - -\n"
echo "Weiherbach with HDF5"
echo "- - - - - - - - - - -\n"

cd /beegfs/work/ka_oj4748/echoRD_weierbach
source activate /home/ka/ka_iwg/ka_oj4748/miniconda3/envs/test_h5py

python weiher_025x.py 
