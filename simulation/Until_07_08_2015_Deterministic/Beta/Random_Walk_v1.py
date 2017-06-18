# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 10:45:58 2015

@author: Sriram
"""

import numpy as np
import matplotlib.pyplot as plt

def initial_state(cells,world_size):
    i=0
    init_pos=np.zeros((2,cells))
    while i<cells:
        init_pos[0,i]=np.random.random_integers(world_size)
        init_pos[1,i]=np.random.random_integers(world_size)
        i+=1
    
    return init_pos
    

def run_next_step(current_position,turn_angle,run_velocity):
    next_position=np.zeros((2,current_position.shape[1]))
    delta_position=np.zeros((2,current_position.shape[1]))    
    for i in np.arange(0,current_position.shape[1],1):
        delta_position[0,:]=run_velocity*np.cos(np.deg2rad(turn_angle[:]))
        delta_position[1,:]=run_velocity*np.sin(np.deg2rad(turn_angle[:]))
        next_position[0,:]=current_position[0,:]+delta_position[0,:]
        next_position[1,:]=current_position[1,:]+delta_position[1,:]
        
    return next_position
        

def tumble(cells):
    angle=np.zeros(cells)
    for i in np.arange(0,cells,1):
        angle[i]=np.random.random_integers(360)
        
    return angle
    

#Parameters to set up the simulation
ncells=1
size=100

runduration=5
runvelocity=0.01
runcounter=0

tstop=10000
dt=0.1

#Lists to save data for plotting
TURN=[]
XPOS=[]
YPOS=[]

#Initialize the world with cells scattered about at random locations
pos=initial_state(ncells,size)
xpos=pos[0,:]
ypos=pos[1,:]
XPOS+=xpos.tolist()
YPOS+=ypos.tolist() 


#Run through the simulation
state=0
t=0

while t<tstop:
    
    #TUMBLE
    if state==0:
        turn=tumble(ncells)
        TURN+=turn.tolist()
        state=1
    
    #SENSE

    #RUN
    r=0
    while r<runduration:
        state=1
        pos=run_next_step(pos,turn,runvelocity)
        xpos=pos[0,:]
        ypos=pos[1,:]
        XPOS+=xpos.tolist()
        YPOS+=ypos.tolist()        
        
        r+=dt
        t+=dt
    runcounter+=1
    state=0
    


fig=plt.figure(figsize=[10,10])
axis=fig.add_axes([.1,.1,.8,.8])
axis.set_xlim(0,size)
axis.set_ylim(0,size)

plt.plot(XPOS,YPOS,color='slateblue',linewidth=2)

plt.show()

