# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 15:16:20 2015

@author: Sriram
"""

import numpy as np
import matplotlib.pyplot as plt


plt.rc('xtick', labelsize=18) 
plt.rc('ytick', labelsize=18)
fig = plt.figure(figsize = [12,8])
axis = fig.add_axes([.15,.15,.8,.8])
axis.set_xlim(0,20)
mylegend=['5','10','15']

i=5
p=0
while i<20:
    s = np.random.normal(i,1,100000)
    edges,hist=np.histogram(s,bins=100,range=(0,20),density=True)
    edges=edges/5
    x=np.arange(0,20,0.2)   
    print(np.sum(edges))
    plt.plot(x,edges,linewidth=2,label='Mean Velocity = '+str(mylegend[p]))
    plt.legend(loc=[0.65,0.75],fontsize=18,frameon=False)        
    i+=5
    p+=1

axis.set_xlabel('Velocity (um/s)',fontsize=20,labelpad=20)
axis.set_ylabel('Probability Density',fontsize=20,labelpad=20)
axis.set_yticks(np.arange(0.02,0.14,0.02))

plt.show()