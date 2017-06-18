# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 10:45:58 2015

@author: Sriram
"""

import numpy as np
import matplotlib.pyplot as plt

ncells=10
size=500

fig=plt.figure(figsize=[10,10])
axis=fig.add_axes([.1,.1,.8,.8])
axis.set_xlim(0,size)
axis.set_ylim(0,size)


i=0
xpos=np.zeros(ncells)
ypos=np.zeros(ncells)

plt.ion()
plt.show()

while i<ncells:
    xpos[i]=np.random.randint(size)
    ypos[i]=np.random.randint(size)
    plt.scatter(xpos[i],ypos[i],color='red')
    plt.draw()
    i+=1

plt.ioff()
plt.show()