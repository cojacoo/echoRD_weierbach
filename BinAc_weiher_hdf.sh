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

module load devel/python/3.5.1
module load numlib/numpy
module load lib/matplotlib
module load lib/pandas
module load numlib/scipy

python weiher_025x.py 
