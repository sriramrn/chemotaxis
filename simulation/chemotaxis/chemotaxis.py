# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 09:55:56 2015

@author: Sriram
email  : sriramn@ncbs.res.in


Chemotaxis module
"""


import numpy as np
import math
from scipy.spatial import distance


#Initialize a bacterium at a random location in the world
def initial_state(world_size):
    init_pos=np.zeros(2)
    
    init_pos[0]=np.random.random_integers(world_size)
    init_pos[1]=np.random.random_integers(world_size)
    
    return init_pos
    

#Calculate total displacement during a run
def run_displacement(run_velocity,run_duration):
    run_displacement=run_velocity*run_duration
        
    return run_displacement
    
    
#Calculate the new x,y coordinates of the bacterium after the run, 
#given the run displacement and angle
def run(current_position,turn_angle,step_size):
    next_position=np.zeros(2)
    delta_position=np.zeros(2)    
    
    delta_position[0]=step_size*np.cos(np.deg2rad(turn_angle))
    delta_position[1]=step_size*np.sin(np.deg2rad(turn_angle))
    
    next_position[0]=current_position[0]+delta_position[0]
    next_position[1]=current_position[1]+delta_position[1]
        
    return next_position


def random_tumble(current_position,world_size,current_angle):
    #Random direction change
    delta_angle=np.random.random_integers(360)  
    
    angle=current_angle+delta_angle
    
    if angle>=360:
        angle=angle-360
    if angle<=-360:
        angle=angle+360
   
   #Stay within the arena
    if current_position[0]<=0:
        angle=np.random.random_integers(-60,60)
        if angle<0:
            angle=angle+360
        
    if current_position[0]>=world_size:
        angle=np.random.random_integers(120,240)
        
    if current_position[1]<=0:
        angle=np.random.random_integers(30,150)
        
    if current_position[1]>=world_size:
        angle=np.random.random_integers(210,330)   

    return angle    
    
    
def skewed_tumble(current_position,world_size,current_angle):
    #Skewed direction change        
    delta_angle=np.random.normal(60,30)
    while delta_angle<0 or delta_angle>180:
        delta_angle=np.random.normal(62,28)    
    direction=np.random.randint(1,3)
    if direction==1:
        delta_angle=-delta_angle    

    angle=current_angle+delta_angle
    
    if angle>=360:
        angle=angle-360
    if angle<=-360:
        angle=angle+360
        
    if current_position[0]<=0:
        angle=np.random.random_integers(-60,60)
        if angle<0:
            angle=angle+360
        
    if current_position[0]>=world_size:
        angle=np.random.random_integers(120,240)
        
    if current_position[1]<=0:
        angle=np.random.random_integers(30,150)
        
    if current_position[1]>=world_size:
        angle=np.random.random_integers(210,330)
        
    return angle        
 

#Define the gradient to calculate concentration at known distances from source
def gradient_equation(source_coordinates,source_concentration,tau,current_position):
    distance_from_source=distance.euclidean(source_coordinates,current_position)
    concentration=source_concentration*math.exp(-distance_from_source/tau) 
    
    return concentration
    
    
def noisy_gradient_equation(source_coordinates,source_concentration,tau,current_position,noise):
    distance_from_source=distance.euclidean(source_coordinates,current_position)
    concentration=source_concentration*math.exp(-distance_from_source/tau) 
    concentration=concentration+np.random.normal(0,noise)
    
    return concentration
    
    
#Gradient memory E
def memory_E(current_concentration,previous_concentration,previous_memory,elapsed_time,tau):
    
    diff=current_concentration-previous_concentration
    trace=previous_memory*math.exp(-elapsed_time/tau)
    if diff>0:
        memory=1
    if diff<=0:
        memory=0
        
    memory=memory+trace      
    
    return memory
    
    
#Gradient memory I
def memory_I(current_concentration,previous_concentration,previous_memory,elapsed_time,tau):
    
    diff=current_concentration-previous_concentration
    trace=previous_memory*math.exp(-elapsed_time/tau)
    if diff>=0:
        memory=0
    if diff<0:
        memory=-1

    memory=memory+trace

    return memory
    

#Gradient memory E and I
def memory_EI(current_concentration,previous_concentration,previous_memory,elapsed_time,tau):
    
    diff=current_concentration-previous_concentration
    trace=previous_memory*math.exp(-elapsed_time/tau)
    if diff>0:
        memory=1
    if diff<0:
        memory=-1
    if diff==0:
        memory=0

    memory=memory+trace      
    
    return memory


#Update rule CV
def update_runduration_with_concentration(current_concentration,max_duration,sensor_saturation):

    if current_concentration>sensor_saturation:
        current_concentration=sensor_saturation    
    scaling=max_duration/sensor_saturation
    next_run_duration=max_duration-current_concentration*scaling

    return next_run_duration    


#Update rule CV
def update_runvelocity_with_concentration(current_concentration,max_velocity,sensor_saturation):

    if current_concentration>sensor_saturation:
        current_concentration=sensor_saturation    
    scaling=max_velocity/sensor_saturation
    next_run_velocity=max_velocity-current_concentration*scaling

    return next_run_velocity    


#Update rule MD     
def update_runduration_with_memory(baseline,max_duration,memory,memory_scaling):
                                       
    next_run_duration=baseline+(memory*memory_scaling)
    if next_run_duration>max_duration:
        next_run_duration=max_duration
        
    return next_run_duration
    
#Update rule MV
def update_runvelocity_with_memory(baseline,max_velocity,memory,memory_scaling):
                                       
    next_run_velocity=baseline+(memory*memory_scaling)    
    if next_run_velocity>max_velocity:
        next_run_velocity=max_velocity
    
    return next_run_velocity
    
    
#Update rule CMD 
def update_runduration_with_both(current_concentration,max_duration,
                                 sensor_saturation,memory,memory_scaling):
   
    if current_concentration>sensor_saturation:
         current_concentration=sensor_saturation
         
    scaling=max_duration/sensor_saturation
    d=max_duration-current_concentration*scaling                                     
    next_run_duration=d+(memory*memory_scaling)
    
    if next_run_duration>max_duration:
        next_run_duration=max_duration
         
    return next_run_duration
   

#Update rule CMV
def update_runvelocity_with_both(current_concentration,max_velocity,
                                 sensor_saturation,memory,memory_scaling):
    
    if current_concentration>sensor_saturation:
        current_concentration=sensor_saturation 
        
    scaling=max_velocity/sensor_saturation
    v=max_velocity-current_concentration*scaling
    next_run_velocity=v+(memory*memory_scaling) 
    
    if next_run_velocity>max_velocity:
        next_run_velocity=max_velocity
    
    return next_run_velocity    


#Update rule C2MD 
def update_runduration_like_Ecoli(current_concentration,max_duration,
                                  sensor_saturation,memory,memory_scaling):
   
    if current_concentration>sensor_saturation:
         current_concentration=sensor_saturation
         
    scaling=max_duration/sensor_saturation
    d=current_concentration*scaling                                       
    next_run_duration=d+(memory*memory_scaling)
    
    if next_run_duration>max_duration:
        next_run_duration=max_duration
         
    return next_run_duration
    

#Update rule C2MV
def update_runvelocity_like_Ecoli(current_concentration,max_velocity,
                                  sensor_saturation,memory,memory_scaling):
    
    if current_concentration>sensor_saturation:
        current_concentration=sensor_saturation 
        
    scaling=max_velocity/sensor_saturation
    v=current_concentration*scaling
    next_run_velocity=v+(memory*memory_scaling) 
    
    if next_run_velocity>max_velocity:
        next_run_velocity=max_velocity
    
    return next_run_velocity    
    

#More realistic velocity update
def gaussian_estimate(current_value,min_value,max_value):

    if current_value<=min_value:
        current_value=min_value
    
    updated_value=np.random.normal(current_value,1.0)
    while updated_value<min_value or updated_value>max_value:
        updated_value=np.random.normal(current_value,1.0)

    return updated_value


#More realistic duration update
def laplace_estimate(current_value,min_value,max_value):
    
    if current_value<=min_value:
        current_value=min_value
    
    updated_value=np.random.laplace(min_value,current_value)
    while updated_value<min_value or updated_value>max_value:
        updated_value=np.random.laplace(min_value,current_value)

    return updated_value