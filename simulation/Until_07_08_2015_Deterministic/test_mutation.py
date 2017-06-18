# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 00:01:27 2015

@author: Sriram
"""
import numpy as np
import matplotlib.pyplot as plt
import csv
import os




def get_next_index_range(current_index,index_range,window):
    
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
        next_range=get_next_index_range(selector,k,2)
        
    
    points_to_interpolate_duration=np.arange(0,source_concentration,dint)
    points_to_interpolate_velocity=np.arange(0,source_concentration,dint)
    interpolated_duration_profile=np.interp(points_to_interpolate_duration,conc,duration_profile,
                                       left=None,right=None)
    interpolated_velocity_profile=np.interp(points_to_interpolate_velocity,conc,velocity_profile,
                                       left=None,right=None)
                                       
    return (interpolated_duration_profile,interpolated_velocity_profile)
    
#Path and filename to save data
datapath='E:/Work/Rotation/06_09_2015/'
filename='random_mutations_velocity'
repeat='0'

newpath = datapath+filename+repeat
if not os.path.exists(newpath): os.makedirs(newpath)
path=newpath+'/'


mutation_list_velocity=[]
p=0
while p<31:
    mutation=mutate_now(800,3,30)
    duration_profile=np.array(mutation[0])
    velocity_profile=np.array(mutation[1])
    concentration=np.arange(0,800,1)
    mutation_list_velocity.append(velocity_profile)
    #plt.plot(concentration,velocity_profile)
    p+=1
#plt.show()


writedata_random= open(path+filename+repeat+'.csv', 'w')
writer=csv.writer(writedata_random,lineterminator = '\n')
for data in mutation_list_velocity:
    writer.writerow(data)
    
writedata_random.flush()    
writedata_random.close
