# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 11:17:50 2015

@author: Sriram
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def fit_func(x,a,b,c,d,e,f,g):
    return a*x**6+b*x**5+c*x**4+d*x**3+e*x**2+f*x+g

def fit_func2(x,a,b,c,d,e):
    return a*x**4+b*x**3+c*x**2+d*x+e

def fit_func3(x,a,b,c,d):
    return a*x**3+b*x**2+c*x+d

conc=np.arange(0,960,160)
duration=np.arange(0,3.6,0.6)

runduration=np.zeros(6)
for i in np.arange(0,6,1):
    runduration[i]=np.random.choice(duration,size=None,replace=True,p=None)
    

points_to_interpolate=np.arange(0,800,0.01)
concentration=np.arange(0,800,0.01)
interpolated_runduration=np.interp(points_to_interpolate,conc,runduration,left=None,right=None)


popt,pcov=curve_fit(fit_func,concentration,interpolated_runduration)
fit=fit_func(concentration,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5],popt[6])

popt2,pcov2=curve_fit(fit_func2,concentration,interpolated_runduration)
fit2=fit_func2(concentration,popt2[0],popt2[1],popt2[2],popt2[3],popt2[4])

popt3,pcov3=curve_fit(fit_func3,concentration,interpolated_runduration)
fit3=fit_func3(concentration,popt3[0],popt3[1],popt3[2],popt3[3])

print(len(concentration))

plt.plot(concentration,interpolated_runduration)
plt.plot(concentration,fit)
plt.plot(concentration,fit2)
plt.plot(concentration,fit3)
plt.show()