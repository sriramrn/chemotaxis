# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 15:21:45 2015

@author: Sriram
"""
import chemotaxis as ct
import numpy as np
import matplotlib.pyplot as plt


size=200

fig=plt.figure(figsize=[12,10])
plt.rc('xtick', labelsize=18) 
plt.rc('ytick', labelsize=18)
axis=fig.add_axes([.1,.1,.8,.8])
axis.set_xlim(0,size)
axis.set_ylim(0,size)
axis.set_xticks([])
axis.set_yticks([])

gradient=np.zeros((size,size))
i=0
while i<size:
    ii=0
    while ii<size:
        gradient[ii,i]=ct.gradient_equation([size/2,size/2],800,50,[ii,i])
        ii+=1
    i+=1


plt.pcolor(gradient,vmin=0,vmax=800,cmap='Greys')
#plt.colorbar()

plt.show()