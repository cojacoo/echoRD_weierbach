import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import os, sys
try:
   import cPickle as pickle
except:
   import pickle
import h5py
#connect echoRD Tools
pathdir='../echoRD/' #path to echoRD
sys.path.append(pathdir)
#lib_path = os.path.abspath(pathdir)
#sys.path.append(lib_path)
import vG_conv as vG
from hydro_tools import plotparticles_t,hydroprofile,plotparticles_weier



# Prepare echoRD

#connect to echoRD
import run_echoRD as rE
#connect and load project
[dr,mc,mcp,pdyn,cinf,vG]=rE.loadconnect(pathdir='../',mcinif='mcini_weierbach_z05',experimental=True)
mc = mcp.mcpick_out(mc,'weierbach_z05.pickle3')

runname='weierbach_z05x'

mc.advectref='Shipitalo'
mc.soilmatrix=pd.read_csv(mc.matrixbf, sep=' ')
mc.soilmatrix['m'] = np.fmax(1-1/mc.soilmatrix.n,0.1)
mc.md_macdepth=mc.md_depth[np.fmax(2,np.sum(np.ceil(mc.md_contact),axis=1).astype(int))]
mc.md_macdepth[mc.md_macdepth<=0.]=0.065


precTS=pd.read_csv(mc.precf, sep=',',skiprows=3)

precTS.tstart=360
precTS.tend=360+3600
precTS.total=0.04
precTS.intense=precTS.total/(precTS.tend-precTS.tstart)


#use modified routines for binned retention definitions
mc.part_sizefac=250
mc.gridcellA=mc.mgrid.vertfac*mc.mgrid.latfac
mc.particleA=abs(mc.gridcellA.values)/(2*mc.part_sizefac) #assume average ks at about 0.5 as reference of particle size
mc.particleD=2.*np.sqrt(mc.particleA/np.pi)
mc.particleV=3./4.*np.pi*(mc.particleD/2.)**3.
mc.particleV/=np.sqrt(abs(mc.gridcellA.values)) #assume grid size as 3rd dimension
mc.particleD/=np.sqrt(abs(mc.gridcellA.values))
mc.particlemass=dr.waterdensity(np.array(20),np.array(-9999))*mc.particleV #assume 20C as reference for particle mass
                                                                        #DEBUG: a) we assume 2D=3D; b) change 20C to annual mean T?
mc=dr.ini_bins(mc)
mc=dr.mc_diffs(mc,np.max(np.max(mc.mxbin)))

try:
    [mc,particles,npart]=dr.particle_setup(mc,True,False)
    particles = pd.read_hdf('./results/P_' + runname + '.h5', 'table')
    print('read particle positions from '+'./results/P_' + runname + '.h5')
except:
    [mc,particles,npart]=dr.particle_setup(mc,True)
    print('setup new inital particles')

#define bin assignment mode for infiltration particles
mc.LTEdef='instant'#'ks' #'instant' #'random'
mc.LTEmemory=mc.soilgrid.ravel()*0.

#new reference
mc.maccon=np.where(mc.macconnect.ravel()>0)[0] #index of all connected cells
mc.md_macdepth=np.abs(mc.md_macdepth)
mc.prects=False
#theta=mc.zgrid[:,1]*0.+0.273
#[mc,particles,npart]=rE.particle_setup_obs(theta,mc,vG,dr,pdyn)
[thS,npart]=pdyn.gridupdate_thS(particles.lat,particles.z,mc)
#[A,B]=plotparticles_t(particles,thS/100.,mc,vG,store=True)



# Run Model

mc.LTEpercentile=70 #new parameter


t_end=24.*3600.
saveDT=True

#1: MDA
#2: MED
#3: rand
infiltmeth='MDA'
#3: RWdiff
#4: Ediss
#exfiltmeth='RWdiff'
exfiltmeth='Ediss'
#5: film_uconst
#6: dynamic u
film=True
#7: maccoat1
#8: maccoat10
#9: maccoat100
macscale=1. #scale the macropore coating 
clogswitch=False
infiltscale=False

#mc.dt=0.11
#mc.splitfac=5
#pdyn.part_diffusion_binned_pd(particles,npart,thS,mc)

#import profile
#%prun -D diff_pd_prof.prof pdyn.part_diffusion_binned_pd(particles,npart,thS,mc)

wdir='/beegfs/work/ka_oj4748/echoRD_weierbach'
#wdir='./'
drained=pd.DataFrame(np.array([]))
leftover=0
output=60. #mind to set also in TXstore.index definition

dummy=np.floor(t_end/output)
t=0.
ix=0
TSstore=np.zeros((int(dummy),mc.mgrid.cells[0],2))

try:
    #load h5:
    with h5py.File(mc.stochsoil, 'r') as f:
        [t, n_particles, leftover, n_drained, ix] = f["states"].value[0]
    print('resuming into stored run at t='+str(t)+'...')
except:
    print('starting new run...')
    with h5py.File('./results/S_'+runname+'.h5', 'w') as f:
        dset = f.create_dataset("states", (1,5), dtype='f')
        dset[:] =  [t, len(particles), leftover, len(drained), ix]

#final check of lookup references
mc = rE.check_lookups(mc)

#loop through plot cycles
for i in np.arange(dummy.astype(int))[ix:]:
    plotparticles_weier(particles,mc,pdyn,vG,runname,t,i,saving=True,relative=False,wdir=wdir)
    [particles,npart,thS,leftover,drained,t]=rE.CAOSpy_rundx1(i*output,(i+1)*output,mc,pdyn,cinf,precTS,particles,leftover,drained,6.,splitfac=4,prec_2D=False,maccoat=macscale,saveDT=saveDT,clogswitch=clogswitch,infilt_method=infiltmeth,exfilt_method=exfiltmeth,film=film,infiltscale=infiltscale)
    TSstore[i,:,:]=rE.part_store(particles,mc)
    
    if i/5.==np.round(i/5.):
        particles.to_hdf('./results/P_' + runname + '.h5', 'table')

        with h5py.File(mc.stochsoil, 'r+') as f:
            dset = f["theta"]
            dset[:, :, i] = np.reshape((mc.soilmatrix.loc[mc.soilgrid.ravel() - 1, 'tr'] + (mc.soilmatrix.ts - mc.soilmatrix.tr)[mc.soilgrid.ravel() - 1] * thS.ravel() * 0.01).values, np.shape(thS))

        with h5py.File('./results/S_'+runname+'.h5', 'r+') as f:
            dset = f["states"]
            dset = [t, len(particles), leftover, len(drained), ix]
