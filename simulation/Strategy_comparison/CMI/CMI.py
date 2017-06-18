# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 18:42:59 2015

@author: Sriram
email  : sriramn@ncbs.res.in
"""


import chemotaxis as ct
import numpy as np
import time
import csv
import pickle
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches


####################################
"""Path and filename to save data"""
####################################

save='yes' #yes or no
datapath='E:/Work/Rotation/Comparison/CMI/'
filename='CMIVDS'

newpath = datapath+filename
if save=='yes':
    if not os.path.exists(newpath): os.makedirs(newpath)
    path=newpath+'/'
     
     
#######################################################
"""Simulation condition and parameter initialization"""
#######################################################
from ctvariables import (ncells,size,simtime,runduration,runvelocity,min_d,min_v,max_d,
max_v,mtau,mscale_d,mscale_v,attractant_source,attractant_concentration,gtau,sensor_max)

strategy='VD'       #Stategy to use (V,D or VD: vary velocity, duration or both)
turn_direction='skewed' #random or skewed distribution to choose turn angle 

displacement=runvelocity*runduration
init_runduration=runduration
init_runvelocity=runvelocity

#List of parameters
parameters=[[ncells,size,simtime,runduration,runvelocity,attractant_source,
            attractant_concentration,gtau,sensor_max,strategy],['ncells','size','simtime',
            'runduration','runvelocity','attractant_source',
            'attractant_concentration','gtau','sensor_max','strategy']] 

#Array to save all the data
group_data=[]
group_pos=[]

fig=plt.figure(figsize=[10,10])
axis=fig.add_axes([.1,.1,.8,.8])
axis.set_xlim(-100,size+100)
axis.set_ylim(-100,size+100)

start_time=time.time()


##############################################
"""Run through the simulation for each cell"""
##############################################

for i in np.arange(0,ncells,1):
    
    #Initialize for each cell
    runduration=init_runduration
    runvelocity=init_runvelocity
    gradient_memory=0 
    t=0
    
    prev_runduration=runduration
    prev_runvelocity=runvelocity
    prev_memory=gradient_memory    
    
    POS=np.zeros(2)
    
    #The World with cells scattered about at random locations
    pos=ct.initial_state(size)    
    POS=pos
    
    data=np.zeros(5)
    
    prev_tumble=np.random.random_integers(360)
    init_concentration=ct.gradient_equation(attractant_source,attractant_concentration,gtau,pos)
    prev_concentration=init_concentration
    
    #Simulate Tumble-Sense-Run sequence
    while t<simtime+init_runduration:    
        #TUMBLE
        if turn_direction=='random':
            turn=ct.random_tumble(pos,size,prev_tumble)
        if turn_direction=='skewed':
            turn=ct.skewed_tumble(pos,size,prev_tumble)

        prev_tumble=turn        
        
        #SENSE
        elapsed_time=prev_runduration
        concentration=ct.gradient_equation(attractant_source,attractant_concentration,gtau,pos)    
        gradient_memory=ct.memory_I(concentration,prev_concentration,prev_memory,elapsed_time,mtau)
        #Calculate next run velocity, duration and displacement
        if strategy=='D':
            runduration=ct.update_runduration_with_both(concentration,init_runduration,sensor_max,
                                                        gradient_memory,mscale_d)
            runduration=ct.laplace_estimate(runduration,min_d,max_d)
            runvelocity=ct.gaussian_estimate(init_runvelocity,min_v,max_v)
                
        if strategy=='V':        
            runvelocity=ct.update_runvelocity_with_both(concentration,init_runvelocity,sensor_max,
                                                        gradient_memory,mscale_v)
            runduration=ct.laplace_estimate(init_runduration,min_d,max_d)
            runvelocity=ct.gaussian_estimate(runvelocity,min_v,max_v)
            
        if strategy=='VD':
            runduration=ct.update_runduration_with_both(concentration,init_runduration,sensor_max,
                                                        gradient_memory,mscale_d)                                                         
            runvelocity=ct.update_runvelocity_with_both(concentration,init_runvelocity,sensor_max,
                                                        gradient_memory,mscale_v)
            runduration=ct.laplace_estimate(runduration,min_d,max_d)
            runvelocity=ct.gaussian_estimate(runvelocity,min_v,max_v)     
            
        displacement=ct.run_displacement(runvelocity,runduration)

        data=np.vstack((data,[t,turn,runvelocity,runduration,gradient_memory]))        
        
        prev_runduration=runduration                                                                      
        prev_runvelocity=runvelocity
        prev_concentration=concentration
        prev_memory=gradient_memory
        
        #RUN
        pos=ct.run(pos,turn,displacement)
        POS=np.vstack((POS,pos))
        
        t+=runduration
        
    data=data[1::]
    POS=POS[1::]
    group_pos.append(POS)
    group_data.append(data)
    

    #Plot start points, end points or trajectories    
    axis.add_patch(patches.Ellipse((POS[0,0],POS[0,1]),20,20,facecolor='none',linewidth='1'))
    axis.add_patch(patches.Ellipse((POS[len(POS)-1,0],POS[len(POS)-1,1]),20,20,facecolor='green'))                        
    #plt.plot(POS[:,0],POS[:,1],linewidth=2)
    

#Mark the source of attractant with a ball    
axis.add_patch(patches.Ellipse((attractant_source[0],attractant_source[1]),100,100,
                                facecolor='grey',alpha=0.5,edgecolor='grey'))
axis.add_patch(patches.Ellipse((attractant_source[0],attractant_source[1]),gtau,gtau,
                                facecolor='grey',alpha=0.25,edgecolor='grey'))

print('Run Time = '+str(round(time.time()-start_time))+'s')

#########################################
"""Save the generated figures and data"""
#########################################

if save=='yes':
    
    saveparams=path+filename+'_params.csv'
    writedata_params= open(saveparams, 'w')
    writer=csv.writer(writedata_params,quoting=csv.QUOTE_ALL,lineterminator = '\n')
    for data in parameters:
        writer.writerow(data)
        
    writedata_params.flush()    
    writedata_params.close
    
    savedata=path+filename+'_data'
    with open(savedata, 'wb') as f:
        pickle.dump(group_data, f)
        
    savetracks=path+filename+'_tracks'    
    with open(savetracks, 'wb') as f:
        pickle.dump(group_pos, f)
        
    fig.savefig(path+filename+'.tiff')

plt.show()