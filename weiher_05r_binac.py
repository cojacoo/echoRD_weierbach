
mcinif='mcini_weierbach_z05'
mcpick='weierbach_z05.pickle3'
runname='weiherbach_z05r'
wdir='/beegfs/work/ka_oj4748/echoRD_weierbach'
pathdir='../echoRD/'

import sys
from pathlib import Path
import numpy as np
sys.path.append(pathdir)

import run_echoRD as rE
rE.echoRD_job(mcinif=mcinif, mcpick=mcpick, runname=runname, wdir=wdir, pathdir=pathdir, hdf5pick=True, update_stochsoil='stoch_'+runname+'.h5',fsize=(2.5,4),w_rat=[3.5,0.6],h_rat=[0.8,9])
