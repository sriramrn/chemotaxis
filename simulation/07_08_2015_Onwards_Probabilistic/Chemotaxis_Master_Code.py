# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 11:52:57 2015

@author: Sriram
email  : sriramn@ncbs.res.in

Simulate bacterial chemotaxis strategies:

A) Strategies without memory:
   Vary run duration, velocity or both as a function of absolute concentration
   
B) Strategies with memory:
   Use gradient information to vary run duration, velocity or both
   
Checklist:
1) If saving data, set the correct path and filename
2) Select the correct set of simulation parameters and initial states
3) Choose the correct strategy (V,D,VD, memory=True/False)
4) Choose the correct tumble method (skewed or random)   
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
        

def random_tumble(current_position,world_size):
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
    

def skewed_tumble(current_position,world_size,current_angle):
    #Skewed direction change
    direction=np.random.randint(1,3)
    delta_angle=np.random.laplace(62.5,18.5)
    if direction==1:
        delta_angle=-delta_angle
    
    angle=current_angle+delta_angle
   
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


def update_runduration_with_concentration(current_concentration,max_duration,sensor_saturation):
   
   if current_concentration>sensor_saturation:
        current_concentration=sensor_saturation
   scaling=max_duration/sensor_saturation
   next_run_duration=max_duration-current_concentration*scaling
   
   return next_run_duration


def update_runvelocity_with_concentration(current_concentration,max_velocity,sensor_saturation):

    if current_concentration>sensor_saturation:
        current_concentration=sensor_saturation    
    scaling=max_velocity/sensor_saturation
    next_run_velocity=max_velocity-current_concentration*scaling

    return next_run_velocity    


def memory_trace(current_concentration,previous_concentration,previous_memory,elapsed_time,tau):
    
    diff=current_concentration-previous_concentration
    if diff>0:
        memory=math.exp(-elapsed_time/tau)
    if diff<=0:
        memory=0

    memory=memory+previous_memory      
    
    return memory
    
    
def update_runduration_with_memory(max_duration,memory,memory_scaling):
                                       
    next_run_duration=(max_duration/2)+(memory*memory_scaling)
    if next_run_duration>max_duration:
        next_run_duration=max_duration
        
    return next_run_duration
    

def update_runvelocity_with_memory(max_velocity,memory,memory_scaling):
                                       
    next_run_velocity=(max_velocity/2)+(memory*memory_scaling)    
    if next_run_velocity>max_velocity:
        next_run_velocity=max_velocity
    
    return next_run_velocity
    

def update_runduration_with_both(current_concentration,max_duration,sensor_saturation,
                                 memory,memory_scaling):
   
   if current_concentration>sensor_saturation:
        current_concentration=sensor_saturation
        
   scaling=max_duration/sensor_saturation
   d=max_duration-current_concentration*scaling                                       
   next_run_duration=d+(memory*memory_scaling)
   
   if next_run_duration>max_duration:
       next_run_duration=max_duration
        
   return next_run_duration
    

def update_runvelocity_with_both(current_concentration,max_velocity,sensor_saturation,
                                 memory,memory_scaling):
    
    if current_concentration>sensor_saturation:
        current_concentration=sensor_saturation 
        
    scaling=max_velocity/sensor_saturation
    v=max_velocity-current_concentration*scaling
    next_run_velocity=v+(memory*memory_scaling) 
    
    if next_run_velocity>max_velocity:
        next_run_velocity=max_velocity
    
    return next_run_velocity    
    
    
def poisson_estimate(current_value,min_value):
    updated_value=np.random.poisson(current_value)
   
    if updated_value<min_value:
        updated_value=min_value

    return updated_value

            
####################################
"""Path and filename to save data"""
####################################

save='no' #yes or no
datapath='E:/Work/Rotation/08_09_2015/'
filename='test'

newpath = datapath+filename
if save=='yes':
    if not os.path.exists(newpath): os.makedirs(newpath)
    path=newpath+'/'
     
     
#######################################################
"""Simulation condition and parameter initialization"""
#######################################################

ncells=50
size=2000
simtime=10000      #Seconds to simulate for
runduration=3      #Maximum duration of a run in Seconds
runvelocity=30     #Maximum velocity of a run in Micrometers per second
strategy='V'       #Stategy to use (V,D or VD: vary velocity, duration or both)
turn_direction='random' #random or skewed distribution to choose turn angle 

memory=False       #True keeps memory of the gradient, False does not
memory_decay=1     #Memory timecourse in units of maximum run duration
mtau=memory_decay*runduration #Memory timecourse in seconds
mscale_d=1
mscale_v=10

displacement=runvelocity*runduration
init_runduration=runduration
init_runvelocity=runvelocity

#Attractant and sensor parameters
attractant_source=np.array([size/2,size/2])
attractant_concentration=800
gtau=500
sensor_max=800;

#List of parameters
parameters=[[ncells,size,simtime,runduration,runvelocity,attractant_source,
            attractant_concentration,gtau,sensor_max,strategy],['ncells','size','simtime',
            'runduration','runvelocity','attractant_source',
            'attractant_concentration','gtau','sensor_max','strategy']] 


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
    gradient_memory=0
    
    prev_runduration=runduration
    prev_runvelocity=runvelocity
    prev_memory=gradient_memory

    t=0
    
    POS=np.zeros(2)
    
    #The World with cells scattered about at random locations
    pos=initial_state(size)    
    POS=pos
    TURN=np.zeros(2)
    RUN=np.zeros(3)
    
    prev_tumble=np.random.random_integers(360)
    init_concentration=gradient_equation(attractant_source,attractant_concentration,gtau,pos)
    prev_concentration=init_concentration
    
    #Simulate Tumble-Sense-Run sequence
    while t<simtime+init_runduration:    
        #TUMBLE
        if turn_direction=='random':
            turn=random_tumble(pos,size)
        if turn_direction=='skewed':
            turn=skewed_tumble(pos,size,prev_tumble)

        TURN=np.vstack((TURN,[turn,t]))
        prev_tumble=turn        
        
        #SENSE
        elapsed_time=prev_runduration
        concentration=gradient_equation(attractant_source,attractant_concentration,gtau,pos)    
        gradient_memory=memory_trace(concentration,prev_concentration,prev_memory,elapsed_time,mtau)
        
        #Calculate next run velocity, duration and displacement
        if strategy=='D':
            
            if memory==True:
                runduration=update_runduration_with_memory(init_runduration,gradient_memory,mscale_d)
            if memory==False:                                               
                runduration=update_runduration_with_concentration(concentration,init_runduration,
                                                                  sensor_max)
            runduration=poisson_estimate(runduration,0.01)
                
        if strategy=='V':        
            
            if memory==True:
                runvelocity=update_runvelocity_with_memory(init_runvelocity,gradient_memory,mscale_v)
            if memory==False:                                          
                runvelocity=update_runvelocity_with_concentration(concentration,init_runvelocity,
                                                                  sensor_max)
            runvelocity=poisson_estimate(runvelocity,0.1)
            
        if strategy=='VD':            
            
            if memory==True:                
                runduration=update_runduration_with_memory(init_runduration,gradient_memory,mscale_d) 
                runvelocity=update_runvelocity_with_memory(init_runvelocity,gradient_memory,mscale_v)                                                           
            if memory==False:                                               
                runduration=update_runduration_with_concentration(concentration,init_runduration,
                                                                  sensor_max)
                runvelocity=update_runvelocity_with_concentration(concentration,init_runvelocity,
                                                                  sensor_max)
            runduration=poisson_estimate(runduration,0.1)
            runvelocity=poisson_estimate(runvelocity,3)
            
            
        
        displacement=run_displacement(runvelocity,runduration)
        
        RUN=np.vstack((RUN,[runduration,runvelocity,t]))

        prev_runduration=runduration                                                                      
        prev_runvelocity=runvelocity
        prev_concentration=concentration
        prev_memory=gradient_memory
        
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