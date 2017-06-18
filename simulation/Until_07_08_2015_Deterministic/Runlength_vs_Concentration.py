# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 21:51:12 2015

@author: Sriram
"""

import numpy as np
import matplotlib.pyplot as plt


def runlength_v(max_concentration,max_velocity,max_duration):
    concentration=np.arange(0,max_concentration,1)
    scaling=max_velocity/max_concentration
    velocity_range=max_velocity-concentration*scaling
    runlength=velocity_range*max_duration
    
    return runlength


def runlength_d(max_concentration,max_velocity,max_duration):
    concentration=np.arange(0,max_concentration,1)
    scaling=max_duration/max_concentration
    duration_range=max_duration-concentration*scaling
    runlength=duration_range*max_velocity
    
    return runlength


def runlength_vd(max_concentration,max_velocity,max_duration):
    concentration=np.arange(0,max_concentration,1)
    scaling_v=max_velocity/max_concentration
    scaling_d=max_duration/max_concentration
    velocity_range=max_velocity-concentration*scaling_v
    duration_range=max_duration-concentration*scaling_d
    runlength=velocity_range*duration_range
    
    return runlength    


max_concentration=800
runduration=6
runvelocity=30

v=runlength_v(max_concentration,runvelocity,runduration)
d=runlength_d(max_concentration,runvelocity,runduration)
vd=runlength_vd(max_concentration,runvelocity,runduration)

plt.plot(v)
plt.plot(d)
plt.plot(vd)

plt.show()