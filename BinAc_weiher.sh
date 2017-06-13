#!/bin/bash
#PBS -l nodes=1:ppn=2
#PBS -l walltime=72:00:00
#PBS -l mem=48gb
#PBS -S /bin/bash
#PBS -N echoRD_weier3
#PBS -j oe
#PBS -o LOG_weier3
#PBS -n

#cd /beegfs/work/ka_oj4748

echo "User:"
whoami
echo "Job running on node:"
uname -a
echo "started on "
date
echo "- - - - - - - - - - -\n"
echo "This script shall continue the wollef echoRD test cases on a BinAC node."
echo "- - - - - - - - - - -\n"

cd /beegfs/work/ka_oj4748/echoRD_weierbach

module load devel/python/3.5.1
module load numlib/numpy
module load lib/matplotlib
module load lib/pandas
module load numlib/scipy

python weiher_10a.py &
python weiher_05a.py #&
#python weiher_025a.py
