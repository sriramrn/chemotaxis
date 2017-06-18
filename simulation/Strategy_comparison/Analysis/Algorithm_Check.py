# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:21:08 2015

@author: Sriram
"""

import numpy as np
import pickle
from scipy.spatial import distance
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def displacement(init_position,position_list):
    p=len(position_list[0][:])-1
    disp=np.zeros(p)
    i=0
    while i<p:
        disp[i]=distance.euclidean(init_position,[position_list[0][i],position_list[1][i]])
        i+=1
        
    return disp
    
    
def fitFunc(t,d):
    return np.sqrt(d*t)



ncells=50    
simtime=5000
dt=1

path1='E:/Work/Rotation/AlgorithmTest/Conc250/CVR/CVR_interpolated'
path2='E:/Work/Rotation/AlgorithmTest/Conc500/CVR/CVR_interpolated'
path3='E:/Work/Rotation/AlgorithmTest/Conc750/CVR/CVR_interpolated'

with open(path1, 'rb') as f:
    group_tracks = pickle.load(f)


D=np.zeros(simtime/dt-1)
i=0
while i<ncells:
    d=displacement([group_tracks[2*i,0],group_tracks[2*i+1,0]],
                   [group_tracks[2*i,:],group_tracks[2*i+1,:]])
    D=np.vstack((D,d))
    i+=1
D=D[1::,:]


md1=np.mean(D,axis=0)
x=np.arange(0,simtime/dt-1,1)

md1=md1[0:200]
x=x[0:200]

fitParams, fitCovariances = curve_fit(fitFunc,x,md1)
print(fitParams)

y1=fitFunc(x,fitParams[0])

rsquared=1-sum((md1-fitFunc(x,fitParams[0]))**2)/sum((md1-np.mean(md1))**2)
print(rsquared)


with open(path2, 'rb') as f:
    group_tracks = pickle.load(f)


D=np.zeros(simtime/dt-1)
i=0
while i<ncells:
    d=displacement([group_tracks[2*i,0],group_tracks[2*i+1,0]],
                   [group_tracks[2*i,:],group_tracks[2*i+1,:]])
    D=np.vstack((D,d))
    i+=1
D=D[1::,:]

md2=np.mean(D,axis=0)
x=np.arange(0,simtime/dt-1,1)

md2=md2[0:200]
x=x[0:200]

fitParams, fitCovariances = curve_fit(fitFunc,x,md2)
print(fitParams)

y2=fitFunc(x,fitParams[0])


with open(path3, 'rb') as f:
    group_tracks = pickle.load(f)


D=np.zeros(simtime/dt-1)
i=0
while i<ncells:
    d=displacement([group_tracks[2*i,0],group_tracks[2*i+1,0]],
                   [group_tracks[2*i,:],group_tracks[2*i+1,:]])
    D=np.vstack((D,d))
    i+=1
D=D[1::,:]

md3=np.mean(D,axis=0)
x=np.arange(0,simtime/dt-1,1)

md3=md3[0:200]
x=x[0:200]

fitParams, fitCovariances = curve_fit(fitFunc,x,md3)
print(fitParams)

y3=fitFunc(x,fitParams[0])



fig=plt.figure(figsize=[8,8])
plt.rc('xtick', labelsize=18) 
plt.rc('ytick', labelsize=18)
ax=fig.add_axes([.15,.1,.8,.8])
ax.set_xlim(0,200)
ax.set_ylim(0,500)
ax.set_xticks(np.arange(0,250,50))
ax.set_yticks(np.arange(100,600,100))
ax.set_ylabel('Mean Displacement (um)',fontsize=20,labelpad=20)
ax.set_xlabel('Time (s)',fontsize=20,labelpad=18)
#ax.text(44,380,'R^2= '+str(round(rsquared,3)), fontsize=18)


plt.plot(x,md1,color='black',linewidth=2, label='C=250')
plt.plot(x,y1,color='red',linewidth=2)
plt.plot(x,md2,color='green',linewidth=2, label='C=500')
plt.plot(x,y2,color='red',linewidth=2)
plt.plot(x,md3,color='navy',linewidth=2, label='C=750')
plt.plot(x,y3,color='red',linewidth=2)
                                   
plt.legend(loc=[0.1,0.75],fontsize=18,frameon=False)


plt.show()