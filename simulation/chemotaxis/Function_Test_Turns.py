# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 16:09:17 2015

@author: Sriram
"""
import random
import numpy as np
import matplotlib.pyplot as plt


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
    
    
def calculate_turn_angle(heading_angle):
    length=len(heading_angle)
    turn=np.zeros(length-1)    
    i=0
    while i<length-1:
        turn[i]=heading_angle[i+1]-heading_angle[i]
        if turn[i]>180:
            turn[i]=360-turn[i]
        if turn[i]<-180:
            turn[i]=360+turn[i]
        turn[i]=abs(turn[i])
        i+=1
    
    return turn


nsamples=1000    
s=np.zeros(nsamples)
r=np.zeros(nsamples)
i=0
a=np.random.randint(360)
while i<nsamples:
    pos=np.array([np.random.randint(-100,5100),np.random.randint(-100,5100)])
    #pos=np.array([500,500])
    s[i]=skewed_tumble(pos,5000,a)
    r[i]=random_tumble(pos,5000,a)
    a=s[i]
    i+=1

skewed_turns=calculate_turn_angle(s)    
random_turns=calculate_turn_angle(r)

mean_rt=np.mean(random_turns)
stdv_rt=np.std(random_turns)

svalues,sbins=np.histogram(skewed_turns,bins=60,range=[0,180])
rvalues,rbins=np.histogram(random_turns,bins=60,range=[0,180])

x=np.arange(0,180,3)

pdf_s=svalues/sum(svalues)
pdf_r=rvalues/sum(rvalues)
print(sum(pdf_r))
print(sum(pdf_s))

fig=plt.figure(figsize=[12,8])
plt.rc('xtick', labelsize=18) 
plt.rc('ytick', labelsize=18)

axis=fig.add_axes([.15,.15,.8,.8])
axis.set_xlim(0,180)
axis.set_ylim(0,max(pdf_s))
axis.set_xticks(np.arange(0,240,60))
axis.set_yticks(np.arange(0.01,0.060,0.01))
axis.set_xlabel('Turn Angle (degrees)',fontsize=20,labelpad=20)
axis.set_ylabel('Probability Density',fontsize=20,labelpad=20)

plt.plot(x,pdf_r,linewidth=2,color='blue',label='Random Turns')
plt.plot(x,pdf_s,linewidth=2,color='green',label='Skewed Turns')

plt.legend(loc=[0.65,0.75],fontsize=18,frameon=False)

plt.figure()
i=0
k=[]
while i<500:
    p=random.gauss(62,30)
    while p<0:
        p=random.gauss(62,30)
    p=round(p*2400/360)
    k.append(p)
    i+=1
plt.hist(k,20)
print(len(k))
print(k)
plt.show()