# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:03:42 2015

@author: Sriram
"""

import numpy as np
import matplotlib.pyplot as plt
import math


def init_pos(n):
    init_pos=np.zeros(n)
    i=0
    while i<n:
        init_pos[i]=np.random.randint(-1000,1000)
        i+=1

    return init_pos
    
    
def update_pos(n,current_pos,duration,velocity):
    displacement=duration*velocity
    i=0
    while i<n:
        turn=np.random.randint(0,2)
        if turn==0:
            displacement[i]=-displacement[i]
        i+=1
    
    next_pos=np.zeros(n)
    i=0
    while i<n:
        next_pos[i]=current_pos[i]+displacement[i]
        if next_pos[i]>1000:
            next_pos[i]=2000-next_pos[i]
        if next_pos[i]<-1000:
            next_pos[i]=-2000-next_pos[i]
        i+=1
    
    return next_pos
    
    
def set_velocity(n,current_pos):
    velocity=np.zeros(n)
    i=0
    while i<n:
        if current_pos[i]>0:
            velocity[i]=15
        else:
            velocity[i]=1.5
        i+=1

    return velocity
    

def set_duration(n,current_pos):
    duration=np.zeros(n)
    i=0
    while i<n:
        if current_pos[i]>0:
            duration[i]=2
        else:
            duration[i]=0.2
        i+=1

    return duration
    
    
def set_velocity_with_gradient(n,concentration):
    velocity=np.zeros(n)
    i=0
    while i<n:
        velocity[i]=15-(15*concentration[i])
        if velocity[i]<1.5:
            velocity[i]=1.5
        i+=1

    return velocity
    

def set_duration_with_gradient(n,concentration):
    duration=np.zeros(n)
    i=0
    while i<n:
        duration[i]=2-(2*concentration[i])
        if duration[i]<0.2:
            duration[i]=0.2
        i+=1
        
    return duration
    

def gradient(n,current_pos,tau):
    concentration=np.zeros(n)
    i=0
    while i<n:
        concentration[i]=math.exp(-(1000+current_pos[i])/tau)
        i+=1
    
    return concentration
    

def score(pos,ncells):
    pos[pos==0]=1
    score=(sum(pos/abs(pos)))/ncells
    
    return score
    
    
ncells=500
runs=10000
init_d=2
init_v=15

tau=1000

vscore=[]
dscore=[]

dpos=init_pos(ncells)
#vpos=init_pos(ncells)
vpos=dpos
t=0
while t<runs:
    
    #v=set_velocity(ncells,vpos)
    #d=set_duration(ncells,dpos)

    vconc=gradient(ncells,vpos,tau)
    dconc=gradient(ncells,dpos,tau)
    
    v=set_velocity_with_gradient(ncells,vconc)
    d=set_duration_with_gradient(ncells,dconc)  
    
    dpos=update_pos(ncells,dpos,d,init_v)
    vpos=update_pos(ncells,vpos,init_d,v)

    vscore.append(score(vpos,ncells))
    dscore.append(score(dpos,ncells))    
    
    t+=1


fig=plt.figure(figsize=[12,2])
axis=fig.add_axes([.1,.1,.8,.8])
axis.set_xlim(-1050,1050)
axis.set_ylim(-1,1)
axis.set_yticks([])

plt.plot(dpos,np.zeros(ncells),'o',markersize=10,color='green',
         alpha=0.05,markeredgecolor=None)
         
fig2=plt.figure(figsize=[12,2])
axis2=fig2.add_axes([.1,.1,.8,.8])
axis2.set_xlim(-1050,1050)
axis2.set_ylim(-1,1)
axis2.set_yticks([])

plt.plot(vpos,np.zeros(ncells),'o',markersize=10,color='red',
         alpha=0.05,markeredgecolor=None)         


plt.figure()
nbins=20

dcount,dbins=np.histogram(dpos,bins=nbins,range=[-1000,1000])
plt.plot(np.arange(-1000,1000,2000/nbins),dcount,linewidth=2,color='green')

vcount,vbins=np.histogram(vpos,bins=nbins,range=[-1000,1000])
plt.plot(np.arange(-1000,1000,2000/nbins),vcount,linewidth=2,color='red')


plt.figure()
plt.plot(vscore,color='red')
plt.plot(dscore,color='green')


plt.show()  