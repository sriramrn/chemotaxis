# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 11:53:10 2015

@author: Sriram
"""
import numpy as np
import matplotlib.pyplot as plt

mu,sigma = 62.,28. # mean and standard deviation
#s = np.random.laplace(mu, sigma, 10000)
#s = np.random.normal(mu, sigma, 10000)

s=np.arange(0,10000,1)
i=0
while i<10000:
    s[i]=np.random.normal(mu, sigma)
    while s[i]<0:
        s[i]=np.random.normal(mu, sigma)
    i+=1
      
mean=np.mean(s)
std=np.std(s)
print(mean,std)

count, bins = np.histogram(s, 20, normed=True)

fig=plt.figure(figsize=[12,8])
plt.rc('xtick', labelsize=18) 
plt.rc('ytick', labelsize=18)
axis=fig.add_axes([.15,.15,.8,.8])
axis.plot(bins,1/(sigma*np.sqrt(2 * np.pi))*np.exp(-(bins-mu)**2/(2*sigma**2)),
              linewidth=2,color='green')
              
axis.set_xlim(0,180)
axis.set_ylim(0,0.018)
axis.set_xticks(np.arange(0,200,40))
axis.set_yticks(np.arange(0.004,0.020,0.004))
axis.set_xlabel('Turn Angle (degrees)',fontsize=20,labelpad=20)
axis.set_ylabel('Probability Density',fontsize=20,labelpad=20)

plt.show()