# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 10:45:39 2015

@author: Sriram
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import csv


def mean_distance_from_source(source_coordinates,cells,tracks):
    distance_measure=np.zeros(cells)
    for i in np.arange(4,ncells-5,1):
        distance_measure[i]=distance.euclidean(source_coordinates,[tracks[2*i],tracks[2*i+1]])
    mean_distance=np.mean(distance_measure)
        
    return mean_distance
    
    
def normalized_mean_distance(mean_distance_from_source):
    init_mean_distance=mean_distance_from_source[0]
    normalized=mean_distance_from_source/init_mean_distance
    
    return normalized


#Path and filename to save data
datapath='E:/Work/Rotation/07_09_2015/'
filename='test_timestep'
repeat='5'
path=datapath+filename+repeat+'/'

#Simulation parameters
simtime=20000
dt=1
ncells=10
attractant_source=np.array([1000,1000])


#Load tracks
group_pos = np.genfromtxt (path+filename+repeat+'_tracks.csv', delimiter=',')

#Load turns
with open(path+filename+repeat+'_turns.csv', 'r') as f:
    reader = csv.reader(f)
    group_turn = list(reader)

turn1=np.array(group_turn[1])


#Calculate mean distance from attractant source over each timestep
mean_distance=0

for i in np.arange(0,simtime/dt,1):
    md=mean_distance_from_source(attractant_source,ncells,group_pos[i,:])
    mean_distance=np.vstack((mean_distance,md))
mean_distance=mean_distance[1::]

distance_score=normalized_mean_distance(mean_distance)


#Save data in a csv file
writedata= open(path+filename+repeat+'_DistanceScore.csv', 'w')
writer=csv.writer(writedata,lineterminator = '\n')
for data in distance_score:
    writer.writerow(data)
    
writedata.flush()    
writedata.close

fig=plt.figure(figsize=[10,10])
axis=fig.add_axes([.1,.1,.8,.8])
axis.set_xlim(0,simtime/dt)
axis.set_ylim(0,1.1)

plt.plot(distance_score)

fig.savefig(path+filename+repeat+'_DistanceScore'+'.png')

plt.show()