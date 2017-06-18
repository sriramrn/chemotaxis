# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 19:02:47 2015

@author: Sriram
email  : sriramn@ncbs.res.in
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import pickle
import csv


def interpolate_tracks(tracks,time,simulation_time,timestep):
    interpolated_xtracks=np.interp(np.arange(0,simulation_time,timestep),time,tracks[:,0])
    interpolated_ytracks=np.interp(np.arange(0,simulation_time,timestep),time,tracks[:,1])
    interpolated_tracks=np.vstack((interpolated_xtracks,interpolated_ytracks))
        
    return(interpolated_tracks)


def mean_distance_from_source(source_coordinates,cells,cell_coords):
    distance_from_source=np.zeros(cells)
    for i in np.arange(0,cells,1):
        distance_from_source[i]=distance.euclidean(source_coordinates,
                                                   [cell_coords[2*i],cell_coords[2*i+1]])
    mean_distance=np.mean(distance_from_source)
        
    return mean_distance
    
    
def normalized_mean_distance(mean_distance_from_source):
    init_mean_distance=mean_distance_from_source[0]
    normalized=mean_distance_from_source/init_mean_distance
    
    return normalized
    

def interval_diff(data,interval):

    diff=np.zeros(len(data)/interval)
    i=0
    while i<len(diff):
        diff[i]=data[i]-data[i+interval]
        i+=1
        
    return diff

def calculate_turn_angle(heading_angle):
    length=len(heading_angle)
    turn=np.zeros(length-1)    
    i=0
    while i<length-1:
        turn[i]=heading_angle[i+1]-heading_angle[i]
        if turn[i]>180:
            turn[i]=359-turn[i]
        if turn[i]<-180:
            turn[i]=359+turn[i]
        turn[i]=abs(turn[i])
        i+=1
    
    return turn


#Path and filename to save data
datapath='E:/Work/Rotation/AlgorithmTest/Conc750/'
filename='CVR'
path=datapath+filename+'/'

#Simulation parameters
simtime=5000
ncells=50
attractant_source=np.array([1000,1000])


"""
Things to Plot and/or Calculate:
1)Convergance to source-------------------Done
2)Run duration histogram,mean,stdv--------Done
3)Run velocity histogram,mean,stdv--------Done
4)Run length histogram,mean,stdv----------Done
5)Turn angle histogram,mean,stdv----------Done
6)Number of turns/runs, stdv--------------Done
"""


#Load saved data
with open(path+filename+'_tracks', 'rb') as f:
    group_tracks = pickle.load(f)
    
with open(path+filename+'_data', 'rb') as f:
    group_data = pickle.load(f) 


"""Interpolate the data from t=0 to simtime"""
dt=1 #Timestep of interpolation
tracks=np.zeros(simtime/dt)
i=0
while i<ncells:         
    t=interpolate_tracks(group_tracks[i],group_data[i][:,0],simtime,dt)
    tracks=np.vstack((tracks,t))
    i+=1
tracks=tracks[1::,:]    


#Calculate mean distance from attractant source over each timestep
mean_distance=np.zeros(simtime/dt)
for i in np.arange(0,simtime/dt,1):
    mean_distance[i]=mean_distance_from_source(attractant_source,ncells,tracks[:,i])

distance_score=normalized_mean_distance(mean_distance)
mean_score=sum(distance_score)/len(distance_score)


print('Mean Score = '+str(mean_score))


""""Number of turns/runs, run duration, velocity"""
i=0
nturns=np.zeros(ncells)
d=np.zeros(1)
v=np.zeros(1)
l=np.zeros(1)
a=np.zeros(1)
while i<ncells:         
    nturns[i]=len(group_data[i][:,1])
    d=np.hstack((d,group_data[i][:,3]))
    v=np.hstack((v,group_data[i][:,2]))
    l=np.hstack((l,group_data[i][:,3]*group_data[i][:,2]))
    a=np.hstack((a,calculate_turn_angle(group_data[i][:,1])))   
    i+=1
    
d=d[1::]
v=v[1::]    
l=l[1::]
a=a[1::]

mean_turns=np.mean(nturns)
stdv_turns=np.std(nturns)

mean_duration=np.mean(d)
stdv_duration=np.std(d)

mean_velocity=np.mean(v)
stdv_velocity=np.std(v)

mean_length=np.mean(l)
stdv_length=np.std(l)

mean_angle=np.mean(a)
stdv_angle=np.std(a)

#plt.figure()
#plt.hist(a,round(max(a)))
#plt.figure()
#plt.hist(l,round(max(l)))
#plt.figure()
#plt.hist(d,round(max(d)))
#plt.figure()
#plt.hist(v,round(max(v)))


print('Number of Turns = '+str(mean_turns)+' +- '+str(stdv_turns))
print('Duration = '+str(mean_duration)+' +- '+str(stdv_duration))
print('Velocity = '+str(mean_velocity)+' +- '+str(stdv_velocity))
print('Run Length = '+str(mean_length)+' +- '+str(stdv_length))
print('Turn Angle = '+str(mean_angle)+' +- '+str(stdv_angle))


#Plot normalized distance score over time
fig=plt.figure(figsize=[8,8])
plt.rc('xtick', labelsize=18) 
plt.rc('ytick', labelsize=18)
axis=fig.add_axes([.15,.15,.8,.8])
axis.set_xlim(0,simtime/dt)
axis.set_ylim(0,1.2)
axis.set_xticks(np.arange(0,simtime/dt,2000))
axis.set_yticks(np.arange(0.2,1.4,0.2))
axis.set_xlabel('Time (s)',fontsize=20,labelpad=20)
axis.set_ylabel('Normalized distance from source',fontsize=20,labelpad=20)
axis.plot(distance_score,linewidth=2,color='red')


#Save data
#Interpolated tracks are pickled, distance score is not
#Manual manipulation of the distance score data is possible
savetracks=path+filename+'_interpolated'    
with open(savetracks, 'wb') as f:
    pickle.dump(tracks, f)
    
savescores=path+filename+'_distancescore.csv'    
with open(savescores,'w') as f:
    writer=csv.writer(f)
    writer.writerow(distance_score)    
       
fig.savefig(path+filename+'_distance'+'.tiff')    

plt.show()