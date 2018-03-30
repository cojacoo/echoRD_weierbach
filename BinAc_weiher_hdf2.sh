#!/bin/bash
#PBS -l nodes=1:ppn=4
#PBS -l walltime=120:00:00
#PBS -l mem=48gb
#PBS -S /bin/bash
#PBS -N echoRD_weiher_hdf2
#PBS -j oe
#PBS -o LOG_weiher_hdf2
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

$HOME/miniconda3/bin/python weierbach_Y05a_binac.py &
$HOME/miniconda3/bin/python weierbach_Y05b_binac.py &
$HOME/miniconda3/bin/python weierbach_Y05c_binac.py &
$HOME/miniconda3/bin/python weierbach_Y05d_binac.py
