# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:48:55 2015

@author: Sriram
"""
import numpy as np
import matplotlib.pyplot as plt


def init_pos(n):
    init_pos=np.zeros(n)
    i=0
    while i<n:
        init_pos[i]=np.random.randint(-500,500)
        i+=1

    return init_pos
    
    
def update_pos(current_pos,duration,velocity):
    displacement=duration*velocity
    turn=np.random.randint(0,2)
    if turn==0:
        displacement=-displacement
    
    next_pos=current_pos+displacement
    if next_pos>500:
        next_pos=1000-next_pos
    if next_pos<-500:
        next_pos=-1000-next_pos
            
    return next_pos
    
    
def set_velocity(current_pos):
    if current_pos>0:
        velocity=15
    else:
        velocity=1.5

    return velocity
    

def set_duration(current_pos):
    if current_pos>0:
        duration=2
    else:
        duration=0.2

    return duration
    
    
    
ncells=100
simtime=100000
d=2
v=15


i=0
POS=np.zeros(ncells)

while i<ncells:
    pos=init_pos(1)
    t=0
    while t<simtime:
        #v=set_velocity(pos)
        d=set_duration(pos)    
        pos=update_pos(pos,d,v)
        t+=d

    POS[i]=pos
    i+=1
    

fig=plt.figure(figsize=[12,8])
axis=fig.add_axes([.1,.1,.8,.8])    
axis.set_xlim(-550,550)
axis.set_ylim(-10,10)    


plt.plot(POS,np.zeros(ncells),'o',markersize=10,color='green')    


plt.show()    