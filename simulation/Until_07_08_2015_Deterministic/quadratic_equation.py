# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 19:20:50 2015

@author: Sriram
"""

import numpy as np
import matplotlib.pyplot as plt

x=np.arange(0,800,1)
a=-0.000006
c=3
s=-450
w=1.5

fx=a*((w*x)+s)**2+c
gx=a*x**2+c


plt.plot(fx)
plt.plot(gx)
plt.show()