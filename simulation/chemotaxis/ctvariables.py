# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:37:15 2015

@author: Sriram
"""

import numpy as np

ncells=50
size=2000
simtime=5000       #Seconds to simulate for
runduration=1.5    #Maximum mean duration of a run in Seconds
runvelocity=20.    #Maximum mean velocity of a run in Micrometers per second

nominal_d=0.5
nominal_v=10.
min_d=0.1
min_v=2.
max_d=8.
max_v=50.

memory_decay=0.1  #Memory timecourse in units of maximum run duration
mtau=memory_decay*runduration #Memory timecourse in seconds
mscale_d=0.5
mscale_v=5.
gradient_memory=0

#Attractant and sensor parameters
attractant_source=np.array([size/2,size/2])
attractant_concentration=800
gtau=200
sensor_max=800