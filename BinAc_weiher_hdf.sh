#!/bin/bash
#PBS -l nodes=1:ppn=10
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
export PATH=$PATH:$HOME/miniconda3/bin/
#source activate test_h5py

python weierbach_z05_h5_binac.py
