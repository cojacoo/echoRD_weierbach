def echoRD_job(mcinif='mcini',mcpick='mc.pickle3',runname='test',
               wdir='./',pathdir='../echoRD/',saveDT=True,
               aref='Shipitalo',LTEdef='instant',infilM='MDA',exfilM='Ediss'):
    '''
    This is a wrapper for running echoRD easily.
    Be warned that some definitions are implicit in this wrapper

    mcini   -- echoRD ini file of run
    mcpick  -- pickled mode setup
    runname -- name of model run
    wdir    -- working directory path
    pathdir -- path to echoRD model

    Model parameters
    aref    -- Advection reference [Shipitalo | Weiler | Zehe | geogene | geogene2 | obs]
    infilM  -- Infiltration handling [MDA | MED | rand]
    LTEdef  -- Infiltration assumption [instant | ks | random]
    exfilM  -- Exfiltration from macropores [Ediss | RWdiff]
    saveDT  -- optional modified time steps [True | int (factor) | double (static step)]
    '''

    import numpy as np
    import pandas as pd
    import scipy as sp
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import os, sys
    try:
        import cPickle as pickle
    except:
        import pickle
    
    #connect echoRD Tools
    lib_path = os.path.abspath(pathdir)
    sys.path.append(lib_path)
    import vG_conv as vG
    from hydro_tools import plotparticles_t,hydroprofile,plotparticles_weier

    #connect to echoRD
    import run_echoRD as rE
    #connect and load project
    [dr,mc,mcp,pdyn,cinf,vG]=rE.loadconnect(pathdir='../',mcinif=mcinif,experimental=True)
    mc = mcp.mcpick_out(mc,mcpick)

    mc.advectref=aref

    precTS=pd.read_csv(mc.precf, sep=',',skiprows=3)
    mc.prects=False

    #initialise particles
    [mc,particles,npart]=dr.particle_setup(mc,paral=False)

    #define bin assignment mode for infiltration particles
    mc.LTEdef=LTEdef #'instant'#'ks' #'instant' #'random'
    mc.LTEmemory=mc.soilgrid.ravel()*0.

    #macropore reference
    mc.maccon=np.where(mc.macconnect.ravel()>0)[0] #index of all connected cells
    mc.md_macdepth=np.abs(mc.md_macdepth)

    #############
    # Run Model #
    #############

    mc.LTEpercentile=70 #new parameter

    t_end=mc.t_end

    infiltmeth=infilM
    exfiltmeth=exfilM
    film=True
    macscale=1. #scale the macropore coating 
    clogswitch=False
    infiltscale=False

    drained=pd.DataFrame(np.array([]))
    leftover=0
    output=mc.t_out #mind to set also in TXstore.index definition

    dummy=np.floor(t_end/output)
    t=0.
    ix=0
    TSstore=np.zeros((int(dummy),mc.mgrid.cells[0],2))
    thetastore=np.zeros((int(dummy),mc.mgrid.vertgrid[0],mc.mgrid.latgrid[0]))

    #check for previous runs to hook into
    try:
        #unpickle:
        with open(''.join([wdir,'/results/Z',runname,'_Mstat.pick']),'rb') as handle:
            pickle_l = pickle.load(handle)
            dummyx = pickle.loads(pickle_l)
            particles = pickle.loads(dummyx[0])
            [leftover,drained,t,TSstore,ix] = pickle.loads(dummyx[1])
            ix+=1
        print('resuming into stored run at t='+str(t)+'...')
    except:
        print('starting new run...')

    #loop through plot cycles
    for i in np.arange(dummy.astype(int))[ix:]:
        plotparticles_weier(particles,mc,pdyn,vG,runname,t,i,saving=True,relative=False,wdir=wdir)
        [particles,npart,thS,leftover,drained,t]=rE.CAOSpy_rundx1(i*output,(i+1)*output,mc,pdyn,cinf,precTS,particles,leftover,drained,6.,splitfac=4,prec_2D=False,maccoat=macscale,saveDT=saveDT,clogswitch=clogswitch,infilt_method=infiltmeth,exfilt_method=exfiltmeth,film=film,infiltscale=infiltscale)
        TSstore[i,:,:]=rE.part_store(particles,mc)
        thetastore[i,:,:]=np.reshape((mc.soilmatrix.loc[mc.soilgrid.ravel()-1,'tr']+(mc.soilmatrix.ts-mc.soilmatrix.tr)[mc.soilgrid.ravel()-1]*thS.ravel()*0.01).values,np.shape(thS))

        with open(''.join([wdir,'/results/Z',runname,'_Mstat.pick']),'wb') as handle:
        	pickle.dump(pickle.dumps([pickle.dumps(particles),pickle.dumps([leftover,drained,t,TSstore,thetastore,i])]), handle, protocol=2)

