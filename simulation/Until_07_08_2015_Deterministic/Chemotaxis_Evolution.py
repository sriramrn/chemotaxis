# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 16:00:31 2015

@author: Sriram
"""


import numpy as np
import math
from scipy.spatial import distance
import time
import csv
import os


def initial_state(world_size):
    init_pos=np.zeros(2)
    init_pos[0]=np.random.random_integers(world_size)
    init_pos[1]=np.random.random_integers(world_size)
    
    return init_pos

    
def step_distance(run_velocity,time_step):
    stepsize=run_velocity*time_step
    
    return stepsize
    

def run_next_step(current_position,turn_angle,step_size):
    next_position=np.zeros(2)
    delta_position=np.zeros(2)    
    delta_position[0]=step_size*np.cos(np.deg2rad(turn_angle))
    delta_position[1]=step_size*np.sin(np.deg2rad(turn_angle))
    next_position[0]=current_position[0]+delta_position[0]
    next_position[1]=current_position[1]+delta_position[1]
        
    return next_position
        

def tumble(current_position,current_angle,world_size):
    #Random direction change
    angle=np.random.random_integers(360)
    #Reflect off the walls with contact angle = reflection angle
    if current_position[0]>=world_size:
        angle=180-current_angle
    if current_position[0]<=0:
        angle=180-current_angle
    if current_position[1]>=world_size:
        angle=360-current_angle
    if current_position[1]<=0:
        angle=360-current_angle
    #Get out of corners effectively
    if current_position[0]<=100 and current_position[1]<=100:
        angle=45    
    if current_position[0]>=world_size-100 and current_position[1]<=100:
        angle=135
    if current_position[0]>=world_size-100 and current_position[1]>=world_size-100:
        angle=225
    if current_position[0]<=100 and current_position[1]>=world_size-100:
        angle=315

    return angle    
    
    
def pathfinder(current_index,index_range,window):
    
    next_range_max=current_index+window
    next_range_min=current_index-window
    if next_range_max>max(index_range):
        next_range_max=max(index_range)
    if next_range_min<0:
        next_range_min=0
    next_range=index_range[next_range_min:next_range_max+1]

    return next_range     


#Currently picks the same trajectory for velocity and duration from the same generator 
def mutate_now(source_concentration,max_duration,max_velocity):
    dc=100
    dd=0.6
    dv=6
    dint=1
    conc=np.arange(0,source_concentration+dc,dc)
    duration_points=np.arange(0,max_duration+dd,dd)
    velocity_points=np.arange(0,max_velocity+dv,dv)

    duration_profile=np.zeros(9)
    velocity_profile=np.zeros(9)
    k=np.arange(0,6,1)
    next_range=k
    for i in np.arange(0,9,1):
        selector=np.random.choice(next_range,size=None,replace=True,p=None)
        duration_profile[i]=duration_points[selector]
        velocity_profile[i]=velocity_points[selector]
        next_range=pathfinder(selector,k,2)
        
    
    points_to_interpolate_duration=np.arange(0,source_concentration,dint)
    points_to_interpolate_velocity=np.arange(0,source_concentration,dint)
    interpolated_duration_profile=np.interp(points_to_interpolate_duration,conc,duration_profile,
                                       left=None,right=None)
    interpolated_velocity_profile=np.interp(points_to_interpolate_velocity,conc,velocity_profile,
                                       left=None,right=None)
                                       
    return (interpolated_duration_profile,interpolated_velocity_profile)


def gradient_equation(source_coordinates,source_concentration,tau,current_position):
    distance_from_source=distance.euclidean(source_coordinates,current_position)
    concentration=source_concentration*math.exp(-distance_from_source/tau) 
    
    return concentration


def update_runduration_with_concentration(current_concentration,interpolated_duration_profile,sensor_saturation):
    if current_concentration>sensor_saturation:
        current_concentration=sensor_saturation
    conc_index=math.ceil(current_concentration)-1
    next_run_duration=interpolated_duration_profile[conc_index]
    if next_run_duration<0:
        next_run_duration=0
    
    return next_run_duration


def update_runvelocity_with_concentration(current_concentration,interpolated_velocity_profile,sensor_saturation):
    if current_concentration>sensor_saturation:
        current_concentration=sensor_saturation    
    conc_index=math.ceil(current_concentration)-1
    next_run_velocity=interpolated_velocity_profile[conc_index]
    if next_run_velocity<0:
        next_run_velocity=0    
    
    return next_run_velocity    
    

def mean_distance_from_source(source_coordinates,cells,tracks):
    distance_measure=np.zeros(cells)
    for i in np.arange(0,ncells,1):
        distance_measure[i]=distance.euclidean(source_coordinates,[tracks[2*i],tracks[2*i+1]])
    mean_distance=np.mean(distance_measure)
        
    return mean_distance
    

def normalized_mean_distance(mean_distance_from_source):
    init_mean_distance=mean_distance_from_source[0]
    normalized=mean_distance_from_source/init_mean_distance
    
    return normalized
     

#Path and filename to save data
datapath='E:/Work/Rotation/06_09_2015/'
filename='evolution_velocity'
repeat='0'

newpath = datapath+filename+repeat
if not os.path.exists(newpath): os.makedirs(newpath)
path=newpath+'/'

"""
CHECKLIST: Must go through step by step before each run
1) Verify path to save data
2) Set the filename string to identify strategy
3) Reset mutation_acceptance_threshold for thresholding distance score
4) The above value is set based on observations from the original simulations with linear sensing
5) Check the number of evolution cycles
6) Comment/uncomment the 'sensing' phase of the individual simulation runs to choose the correct strategy
7) Comment/uncomment appropriate print statements at the end of the evolution cycle 
8) Change what list to write to each csv file (velocity/duration list of the best and accepted mutations)
"""




#Parameters to set up the simulation
ncells=20
size=2000
simtime=5000    #Seconds to simulate for
dt=1            #Time step in seconds
evolution_cycles=500

runduration=3       #Maximum duration of a run in Seconds
runvelocity=30      #Maximum velocity of a run in Micrometers per second
vdt=runvelocity*dt  #Displacement per step at runvelocity
init_runduration=runduration
init_runvelocity=runvelocity

#Attractant and sensor parameters
attractant_source=np.array([size/2,size/2])
attractant_concentration=800
tau=500
sensor_max=attractant_concentration;



parameters=np.array([ncells,size,simtime,dt,evolution_cycles,runduration,runvelocity])



#Mutate concentration response
selected_duration_mutation=[]
selected_velocity_mutation=[]
mutation_list_duration=[]
mutation_list_velocity=[]
mutation_acceptance_threshold=0.5 #5th percentile distance score to accept mutations
    
mutation=mutate_now(attractant_concentration,init_runduration,init_runvelocity)
duration_profile=np.array(mutation[0])
velocity_profile=np.array(mutation[1])
 


start_time=round(time.time())

integral_distance_score=1
prev_integral_distance_score=integral_distance_score
e=0
while e<evolution_cycles:
    #Array to save all the data
    group_pos=np.zeros(((simtime/dt),ncells*2))


    #Run through the simulation for each cell
    for i in np.arange(0,ncells,1):
        
        #Initialize for each cell
        runduration=init_runduration
        runvelocity=init_runvelocity
        state=0
        t=0
        
        POS=np.zeros(2)
        
        #Initialize the world with cells scattered about at random locations
        pos=initial_state(size)    
        POS=pos
        prev_tumble=0
        
        #Simulate Tumble-Sense-Run sequence
        while t<simtime:    
            #TUMBLE
            if state==0:
                turn=tumble(pos,prev_tumble,size)
                prev_tumble=turn
                state=1
                
            #SENSE
            concentration=gradient_equation(attractant_source,attractant_concentration,tau,pos)    
            #runduration=update_runduration_with_concentration(concentration,duration_profile,sensor_max)
            runvelocity=update_runvelocity_with_concentration(concentration,velocity_profile,sensor_max)
            vdt=runvelocity*dt
            
            #RUN
            r=0
            while r<runduration:
                pos=run_next_step(pos,turn,vdt)
                POS=np.vstack((POS,pos))
                r+=dt
                t+=dt
                state=1
                
            state=0
        #Sometimes runs don't end when simulation ends
        #This is equivalent to exiting the run at the end of simtime
        POS=POS[0:group_pos.shape[0],:]

        #Group all cells together
        group_pos[:,2*i]=POS[:,0]
        group_pos[:,2*i+1]=POS[:,1]
    
                                
    mean_distance=0
    for i in np.arange(0,simtime/dt,1):
        md=mean_distance_from_source(attractant_source,ncells,group_pos[i,:])
        mean_distance=np.vstack((mean_distance,md))
    mean_distance=mean_distance[1::]
    
    distance_score=normalized_mean_distance(mean_distance)
    integral_distance_score=sum(distance_score*dt/simtime)
    
    
    if integral_distance_score<prev_integral_distance_score:
        selected_duration_mutation=[duration_profile,integral_distance_score,np.percentile(distance_score,5)]     
        selected_velocity_mutation=[velocity_profile,integral_distance_score,np.percentile(distance_score,5)]
        prev_integral_distance_score=integral_distance_score
    
    if np.percentile(distance_score,5)<mutation_acceptance_threshold:
        mutation_list_duration.append(duration_profile)
        mutation_list_velocity.append(velocity_profile)
        
    
    mutation=mutate_now(attractant_concentration,init_runduration,init_runvelocity)     
    duration_profile=np.array(mutation[0])
    velocity_profile=np.array(mutation[1])    
    
    e+=1
    
time_now=round(time.time())
print('RunTime(s) = '+str(time_now-start_time))



#Take care of empty lists when no mutations are selected

#if not selected_duration_mutation:
    #print('No mutations found')
    #selected_duration_mutation[0]='No mutations found'
#else:
    #print('Best Score = '+str(selected_duration_mutation[2]))

if not selected_velocity_mutation: 
    print('No mutations found')
    selected_velocity_mutation[0]='No mutations found'
else:
    print('Best Score = '+str(selected_velocity_mutation[2]))



writedata_best= open(path+filename+repeat+'_best.csv', 'w')
writer=csv.writer(writedata_best,lineterminator = '\n')
writer.writerow(selected_velocity_mutation[0])
    
writedata_best.flush()    
writedata_best.close

writedata_accepted= open(path+filename+repeat+'_accepted.csv', 'w')
writer=csv.writer(writedata_accepted,lineterminator = '\n')
for data in mutation_list_velocity:
    writer.writerow(data)
    
writedata_accepted.flush()    
writedata_accepted.close


writedata_params= open(path+filename+repeat+'_params.csv', 'w')
writer=csv.writer(writedata_params,lineterminator = '\n')
writer.writerow(parameters)
    
writedata_params.flush()    
writedata_params.close