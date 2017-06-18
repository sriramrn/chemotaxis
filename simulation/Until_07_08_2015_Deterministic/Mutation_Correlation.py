# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 00:06:16 2015

@author: Sriram
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import patches
import csv

#Path and filename to save data
datapath='E:/Work/Rotation/06_09_2015/'
filename='evolution_velocity'
repeat='0'
path=datapath+filename+repeat+'/'

filename2='random_mutations_velocity'
repeat2='0'
path2=datapath+filename2+repeat2+'/'

#Load mutations
mutations=np.genfromtxt(path+filename+repeat+'_accepted.csv', delimiter=',')
random_mutations=np.genfromtxt(path2+filename2+repeat2+'.csv', delimiter=',')

avg_mutations=np.mean(mutations,0)
stdv_mutations=np.std(mutations,0)
ste_mutations=stdv_mutations/math.sqrt(mutations.shape[0])


fig1=plt.figure('Average Velocity Profile',figsize=[12,10])
plt.rc('xtick', labelsize=18) 
plt.rc('ytick', labelsize=18)
axis1=fig1.add_axes([.1,.1,.8,.8])
axis1.set_xlabel('Concentration',fontsize=20,labelpad=20)
axis1.set_ylabel('Velocity (um/s)',fontsize=20, labelpad=20)

i=0
while i<len(ste_mutations):
    axis1.add_patch(patches.Rectangle((i,avg_mutations[i]-stdv_mutations[i]),1,
                    stdv_mutations[i]*2,facecolor='crimson',alpha=0.025,edgecolor=None))
    i+=1
        
plt.plot(avg_mutations,color='crimson',linewidth=2)

corr=np.corrcoef(mutations)
random_corr=np.corrcoef(random_mutations)

fig2=plt.figure('Selected Mutations',figsize=[12,10])
axis2=fig2.add_axes([.1,.1,.8,.8])
axis2.set_xlim(0,mutations.shape[0])
axis2.set_ylim(0,mutations.shape[0])

plt.pcolor(corr,vmin=-1,vmax=1)
plt.colorbar()


fig3=plt.figure('Random Mutations',figsize=[12,10])
axis3=fig3.add_axes([.1,.1,.8,.8])
axis3.set_xlim(0,mutations.shape[0])
axis3.set_ylim(0,mutations.shape[0])

plt.pcolor(random_corr,vmin=-1,vmax=1)
plt.colorbar()


writedata_average= open(path+filename+repeat+'_average.csv', 'w')
writer=csv.writer(writedata_average,lineterminator = '\n')
writer.writerow(avg_mutations)
    
writedata_average.flush()    
writedata_average.close

plt.show()