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
    if current_position[0]<=50 and current_position[1]<=50:
        angle=45    
    if current_position[0]>=world_size-50 and current_position[1]<=50:
        angle=135
    if current_position[0]>=world_size-50 and current_position[1]>=world_size-50:
        angle=225
    if current_position[0]<=50 and current_position[1]>=world_size-50:
        angle=315

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


#Path and filename to save data
path='E:/Work/Rotation/01_09_2015/'
filename='test_D'
repeat='1'
     

#Parameters to set up the simulation
ncells=10
size=2000
simtime=20000        #Seconds to simulate for
dt=0.25              #Time step in seconds

runduration=3       #Maximum duration of a run in Seconds
runvelocity=30      #Maximum velocity of a run in Micrometers per second
vdt=runvelocity*dt  #Displacement per step at runvelocity
init_runduration=runduration
init_runvelocity=runvelocity

#Attractant and sensor parameters
attractant_source=np.array([size/2,size/2])
attractant_concentration=800
tau=500
sensor_max=800;

#Array to save all the data
group_pos=np.zeros(((simtime/dt),ncells*2))


fig=plt.figure(figsize=[10,10])
axis=fig.add_axes([.1,.1,.8,.8])
axis.set_xlim(-10,size+10)
axis.set_ylim(-10,size+10)


#Run through the simulation for each cell
for i in np.arange(0,ncells,1):
    
    #Initialize for each cell
    runduration=init_runduration
    runvelocity=init_runvelocity
    state=0
    t=dt
    
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
        runduration=update_runduration_with_concentration(concentration,init_runduration,sensor_max)
        #runvelocity=update_runvelocity_with_concentration(concentration,init_runvelocity,sensor_max)
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

    #Plot start points, end points or trajectories    
    axis.add_patch(patches.Ellipse((POS[0,0],POS[0,1]),20,20,facecolor='blue'))
    axis.add_patch(patches.Ellipse((POS[(simtime/dt)-1,0],POS[(simtime/dt)-1,1]),20,20,facecolor='green'))                        
    #plt.plot(POS[:,0],POS[:,1],linewidth=2)
    
#Mark the point source of attractant with a ball    
axis.add_patch(patches.Ellipse((attractant_source[0],attractant_source[1]),100,100,
                                facecolor='grey',alpha=0.5,edgecolor='grey'))



#Save simulation parameters and data generated
saveparams=filename+repeat+'_Parameters'
writeparams=open(path+saveparams+'.txt','w')
writeparams.write('Simulation Parameters:'+'\n'+'Number of cells= '+str(ncells)+'\n'+
                  'World size= '+str(size)+'um'+'\n'+'Simulation time= '+str(simtime)+'s'+'\n'+
                  'Max run duration= '+str(init_runduration)+'um'+'\n'+'Max run velocity= '+
                  str(init_runvelocity)+'um/s'+'\n'+'Attractant source= '+str(attractant_source)+
                  '\n'+'Source concentration= '+str(attractant_concentration)+'units'+'\n'+
                  'Spatial decay constant= '+str(tau)+'um'+'\n'+'Sensor saturation= '+
                  str(sensor_max)+'units')
       
writeparams.flush()
writeparams.close


savedata=filename+repeat+'_tracks'
writedata= open(path+savedata+'.csv', 'w')
writer=csv.writer(writedata,lineterminator = '\n')
for data in group_pos:
    writer.writerow(data)
    
writedata.flush()    
writedata.close

fig.savefig(path+filename+repeat+'_EndPoints'+'.png')


plt.show()