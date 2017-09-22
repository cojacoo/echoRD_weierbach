
mcinif='mcini_weierbach_z025'
mcpick='weierbach_z025.pickle3'
runname='weiherbach_z025x'
wdir='/beegfs/work/ka_oj4748/echoRD_weierbach'
pathdir='../echoRD/'

import sys
from pathlib import Path
import numpy as np
sys.path.append(pathdir)

import run_echoRD as rE
rE.echoRD_job(mcinif=mcinif, mcpick=mcpick, runname=runname, update_mf=update_mf, wdir=wdir, pathdir=pathdir, hdf5pick=True, macscale=macscale, fsize=(2.5,4),w_rat=[3.5,0.6],h_rat=[0.8,9])
