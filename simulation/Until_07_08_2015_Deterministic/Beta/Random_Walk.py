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
    

def run_next_step(current_position,turn_angle,step_size):
    next_position=np.zeros((2,current_position.shape[1]))
    delta_position=np.zeros((2,current_position.shape[1]))    
    for i in np.arange(0,current_position.shape[1],1):
        delta_position[0,:]=step_size*np.cos(np.deg2rad(turn_angle[:]))
        delta_position[1,:]=step_size*np.sin(np.deg2rad(turn_angle[:]))
        next_position[0,:]=current_position[0,:]+delta_position[0,:]
        next_position[1,:]=current_position[1,:]+delta_position[1,:]
        
    return next_position
        

def tumble(cells,current_position,world_size):
    angle=np.zeros(cells)
    for i in np.arange(0,cells,1):
        if 0<=current_position[0,i]<=world_size and 0<=current_position[1,i]<=world_size:
            angle[i]=np.random.random_integers(360)
        if current_position[0,i]<=0:
            angle[i]=0
        if current_position[0,i]>=world_size:
            angle[i]=180
        if current_position[1,i]<=0:
            angle[i]=90
        if current_position[1,i]>=world_size:
            angle[i]=270    
    return angle
    

#Parameters to set up the simulation
ncells=10
size=4000

runduration=2       #Seconds
runvelocity=15      #Micrometer per second
runcount=0
turncount=0

simtime=1000       #Seconds to simulate for
dt=0.1              #Time step in seconds
vdt=runvelocity*dt  #Distance covered in one time step

#arrays to save data for plotting
TURN=np.zeros((ncells))
XPOS=np.zeros((ncells))
YPOS=np.zeros((ncells))

#Initialize the world with cells scattered about at random locations
pos=initial_state(ncells,size)
xpos=pos[0,:]
ypos=pos[1,:]
XPOS=np.vstack((XPOS,xpos))
YPOS=np.vstack((YPOS,ypos)) 


#Run through the simulation
state=0
t=dt
count=0
while t<simtime:
    #TUMBLE
    if state==0:
        turn=tumble(ncells,pos,size)
        TURN=np.vstack((TURN,turn))
        turncount+=1
        state=1
    
    #SENSE

    #RUN
    r=0
    while r<runduration:
        state=1
        pos=run_next_step(pos,turn,vdt)
        xpos=pos[0,:]
        ypos=pos[1,:]
        XPOS=np.vstack((XPOS,xpos))
        YPOS=np.vstack((YPOS,ypos))
        count+=1
        r+=dt
        t+=dt
    runcount+=1
    state=0

print(count)
TURN=TURN[1::]
XPOS=XPOS[1::]
YPOS=YPOS[1::]    

fig=plt.figure(figsize=[10,10])
axis=fig.add_axes([.1,.1,.8,.8])
axis.set_xlim(-10,size+10)
axis.set_ylim(-10,size+10)

plt.plot(XPOS,YPOS,linewidth=2)

plt.show()