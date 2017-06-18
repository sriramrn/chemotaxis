# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 14:00:28 2015

@author: Sriram
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:58:48 2015

@author: Sriram
"""


import numpy as np
import matplotlib.pyplot as plt


source=[1000,1000]
ncells=50
simtime=5000
dt=1

r=[1,3,4,5,9,10,11,15,16,17,21,22,23,27,28,29,33,34,35,39,40,41,45,46,47,51,52,53,57,58,59]
s=[2,6,7,8,12,13,14,18,19,20,24,25,26,30,31,32,36,37,38,42,43,44,48,49,50,54,55,56,60,61,62]

v=[3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60]
d=[4,7,10,13,16,19,22,25,28,31,34,37,40,43,46,49,52,58,61]
vd=[5,8,11,14,17,20,23,26,29,32,35,38,41,44,47,50,53,59,62]

rw=[1,2]

c=[3,4,5,6,7,8]

me=[9,10,11,12,13,14]
mi=[15,16,17,18,19,20]
mei=[21,22,23,24,25,26]

cme=[27,28,29,30,31,32]
cmi=[33,34,35,36,37,38]
cmei=[39,40,41,42,43,44]

c2me=[45,46,47,48,49,50]
c2mi=[51,52,53,54,55,56]
c2mei=[57,58,59,60,61,62]

m=me+mi+mei
    
    
path='E:/Work/Rotation/Strategy_Comparison_23_09_2015/Consolidated_Scores/'


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


filename=3
color='red'
while filename<63:
    if filename in c and filename in d:
        color='black'
        readscores=path+str(filename)+'.csv'    
        data = np.genfromtxt(readscores,delimiter=',', dtype=float)
        plt.plot(data,color=color,linewidth=2)
        
    if filename in c and filename in v:
        color='red'
        readscores=path+str(filename)+'.csv'    
        data = np.genfromtxt(readscores,delimiter=',', dtype=float)
        plt.plot(data,color=color,linewidth=2)
        
    filename+=1 



plt.show()