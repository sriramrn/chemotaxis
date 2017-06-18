# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 17:21:39 2015

@author: Sriram
"""


import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.spatial import distance
import csv
import os
import time


def initial_state(world_size):
    init_pos=np.zeros(2)
    
    init_pos[0]=np.random.random_integers(world_size)
    init_pos[1]=np.random.random_integers(world_size)
    
    return init_pos
    

def run_displacement(run_velocity,run_duration):
    run_displacement=run_velocity*run_duration
        
    return run_displacement
    

def run(current_position,turn_angle,step_size):
    next_position=np.zeros(2)
    delta_position=np.zeros(2)    
    
    delta_position[0]=step_size*np.cos(np.deg2rad(turn_angle))
    delta_position[1]=step_size*np.sin(np.deg2rad(turn_angle))
    
    next_position[0]=current_position[0]+delta_position[0]
    next_position[1]=current_position[1]+delta_position[1]
        
    return next_position
        

def tumble(current_position,world_size):
    #Random direction change
    angle=np.random.random_integers(360)
   
   #Stay within the arena
    if current_position[0]<=0:
        angle=np.random.random_integers(-60,60)
        
    if current_position[0]>=world_size:
        angle=np.random.random_integers(120,240)
        
    if current_position[1]<=0:
        angle=np.random.random_integers(30,150)
        
    if current_position[1]>=world_size:
        angle=np.random.random_integers(210,330)   

    return angle    


def gradient_equation(source_coordinates,source_concentration,tau,current_position):
    distance_from_source=distance.euclidean(source_coordinates,current_position)
    concentration=source_concentration*math.exp(-distance_from_source/tau) 
    
    return concentration
    

def memory_function(current_value,previous_value,min_value,max_value,elapsed_time,tau):
    memory_component=previous_value*math.exp(-elapsed_time/tau)
    gradient=current_value-memory_component
    updated_value=current_value+gradient
    
    if updated_value<min_value[0]:
        updated_value=min_value[0]
    if updated_value>max_value[1]:
        updated_value=max_value[1]
        
    return updated_value


def update_runduration_with_concentration(current_concentration,max_duration,
                                          sensor_saturation,limit_min):
   
   if current_concentration>sensor_saturation:
        current_concentration=sensor_saturation
   scaling=max_duration/sensor_saturation
   next_run_duration=max_duration-current_concentration*scaling

   next_run_duration=np.random.poisson(next_run_duration)
   
   if next_run_duration<limit_min:
       next_run_duration=limit_min

   return next_run_duration


def update_runvelocity_with_concentration(current_concentration,max_velocity,
                                          sensor_saturation,limit_min):

    if current_concentration>sensor_saturation:
        current_concentration=sensor_saturation    
    scaling=max_velocity/sensor_saturation
    next_run_velocity=max_velocity-current_concentration*scaling
    
    next_run_velocity=np.random.poisson(next_run_velocity)
    
    if next_run_velocity<limit_min:
        next_run_velocity=limit_min

    return next_run_velocity    
    
    
    

####################################
"""Path and filename to save data"""
####################################

datapath='E:/Work/Rotation/08_09_2015/'
filename='test'
save='no' #yes or no

newpath = datapath+filename
if save=='yes':
    if not os.path.exists(newpath): os.makedirs(newpath)
    path=newpath+'/'
     
     
#######################################################
"""Simulation condition and parameter initialization"""
#######################################################

ncells=20
size=2000
simtime=10000      #Seconds to simulate for
runduration=3      #Maximum duration of a run in Seconds
runvelocity=30     #Maximum velocity of a run in Micrometers per second
strategy='V'       #Stategy to use (V,D or VD: vary velocity, duration or both)
memory=False       #True keeps memory of the gradient, false does not
mtau=2             #Memory timecourse in units of maximum run duration

displacement=runvelocity*runduration
init_runduration=runduration
init_runvelocity=runvelocity

#Attractant and sensor parameters
attractant_source=np.array([size/2,size/2])
attractant_concentration=800
tau=500
sensor_max=800;

#List of parameters
parameters=[[ncells,size,simtime,runduration,runvelocity,attractant_source,
            attractant_concentration,tau,sensor_max,strategy],['ncells','size','simtime',
            'runduration','runvelocity','attractant_source',
            'attractant_concentration','tau','sensor_max','strategy']] 


#Array to save all the data
group_turn=[]
group_run=[]


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
    t=0
    
    POS=np.zeros(2)
    
    #Initialize the world with cells scattered about at random locations
    pos=initial_state(size)    
    POS=pos
    prev_tumble=0
    TURN=np.zeros(2)
    RUN=np.zeros(3)
   
    #Simulate Tumble-Sense-Run sequence
    while t<simtime+init_runduration:    
        #TUMBLE
        turn=tumble(pos,size)
        TURN=np.vstack((TURN,[turn,t]))
            
        #SENSE
        concentration=gradient_equation(attractant_source,attractant_concentration,tau,pos)    
        #Calculate next run velocity, duration and displacement
        if strategy=='D':
            runduration=update_runduration_with_concentration(concentration,init_runduration,
                                                              sensor_max,0.01)
        if strategy=='V':        
            runvelocity=update_runvelocity_with_concentration(concentration,init_runvelocity,
                                                              sensor_max,0.1)
        if strategy=='VD':
            runduration=update_runduration_with_concentration(concentration,init_runduration,
                                                              sensor_max,0.1)
            runvelocity=update_runvelocity_with_concentration(concentration,init_runvelocity,
                                                              sensor_max,3)
        
        
        displacement=run_displacement(runvelocity,runduration)
        
        RUN=np.vstack((RUN,[runduration,runvelocity,t]))
        
        #RUN
        pos=run(pos,turn,displacement)
        POS=np.vstack((POS,pos))
        
        t+=runduration

    
    TURN=TURN[1::]
    RUN=RUN[1::]
    group_turn.append(TURN)
    group_run.append(RUN)

    #Plot start points, end points or trajectories    
    axis.add_patch(patches.Ellipse((POS[0,0],POS[0,1]),20,20,facecolor='none',linewidth='1'))
    axis.add_patch(patches.Ellipse((POS[len(POS)-1,0],POS[len(POS)-1,1]),20,20,facecolor='green'))                        
    #plt.plot(POS[:,0],POS[:,1],linewidth=2)
    

#Mark the source of attractant with a ball    
axis.add_patch(patches.Ellipse((attractant_source[0],attractant_source[1]),100,100,
                                facecolor='grey',alpha=0.5,edgecolor='grey'))


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
    
    
    saveturns=path+filename+'_turns.csv'
    writedata_turns= open(saveturns, 'w')
    writer=csv.writer(writedata_turns,quoting=csv.QUOTE_ALL,lineterminator = '\n')
    for data in group_turn:
        writer.writerow(data)
        
    writedata_turns.flush()    
    writedata_turns.close
    
    
    saveruns=path+filename+'_runs.csv'
    writedata_runs= open(saveruns, 'w')
    writer=csv.writer(writedata_runs,quoting=csv.QUOTE_ALL,lineterminator = '\n')
    for data in group_run:
        writer.writerow(data)
        
    writedata_runs.flush()    
    writedata_runs.close
    
    
    fig.savefig(path+filename+'.tiff')


plt.show()