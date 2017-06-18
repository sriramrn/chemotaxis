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

r=[1,3,4,5,9,10,11,15,16,17,21,22,23]
s=[2,6,7,8,12,13,14,18,19,20,24,25,26]

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
    
    
path='E:/Work/Rotation/Strategy_Comparison_23_09_2015/Consolidated_Scores/'

readscores=path+'1.csv'  
data = np.genfromtxt(readscores,delimiter=',', dtype=float)
RWR=1-np.mean(data)
      
readscores=path+'2.csv'  
data = np.genfromtxt(readscores,delimiter=',', dtype=float)
RWS=1-np.mean(data)

random_walk=np.hstack((RWR,RWR,RWR,RWS,RWS,RWS))
    
filename=3
D=np.zeros(60)
color='red'
while filename<63:
    readscores=path+str(filename)+'.csv'    
    data = np.genfromtxt(readscores,delimiter=',', dtype=float)  
    D[filename-3]=1-np.mean(data)
    filename+=1 

D=np.hstack((random_walk,D))    
matrix_all=np.flipud(np.reshape(D,[11,6])) 
matrix=matrix_all[0:matrix_all.shape[0]-1]



normdiff_dvr=matrix[:,1]-matrix[:,0]
normdiff_dvs=matrix[:,4]-matrix[:,3]
normdiff_mplusc=matrix[8,:]-matrix[9,:]
normdiff_mminusc=matrix[7,:]-matrix[9,:]
normdiff_mplusminusc=matrix[6,:]-matrix[9,:]



mean_random=np.mean(matrix[:,0:3])
ste_random=np.std(matrix[:,0:3])/np.sqrt(30)
print(mean_random,ste_random)

mean_skewed=np.mean(matrix[:,3:6])
ste_skewed=np.std(matrix[:,3:6])/np.sqrt(30)
print(mean_skewed,ste_skewed)



fig1=plt.figure(figsize=[8.2,8.2])
plt.rc('xtick', labelsize=18) 
plt.rc('ytick', labelsize=18)
ax1=fig1.add_axes([.15,.1,.8,.8])
ax1.set_xlim(0,11)
ax1.set_ylim(-0.4,0.4)
ax1.set_xticks(np.arange(1,11,1))
ax1.set_yticks(np.arange(-0.4,0.6,0.2))
ax1.set_ylabel('Mean Score of D - Mean Score of V',fontsize=20,labelpad=20)
ax1.set_xlabel('Strategy',fontsize=20,labelpad=18)

plt.plot(np.arange(len(normdiff_dvs),0,-1),normdiff_dvs,color='green',marker='o',
         markersize=10,linewidth=2,label='Skewed Turns')
plt.plot(np.arange(len(normdiff_dvr),0,-1),normdiff_dvr,color='blue',marker='o',
         markersize=10,linewidth=2,label='Random Turns')
plt.plot(np.arange(11,-1,-1),np.zeros(12),'--',linewidth=2,color='black')

plt.legend(loc=[0.1,0.80],fontsize=18,frameon=False)
 
 
fig2=plt.figure(figsize=[12,10])
ax2=fig2.add_axes([.15,.1,.8,.8])
ax2.set_xlim(0,6)
ax2.set_ylim(0,11)
ax2.set_xticks([])
ax2.set_yticks([])

plt.pcolor(matrix_all,vmin=min(D),vmax=1.0,cmap='hot')
plt.colorbar()   


fig3=plt.figure(figsize=[8.2,8.2])
ax3=fig3.add_axes([.15,.1,.8,.8])
ax3.set_xlim(0,7)
ax3.set_ylim(-1,1)
ax3.set_xticks(np.arange(1,7,1))
ax3.set_yticks(np.arange(-1,1.2,0.2))
ax3.set_ylabel('Mean Score of M - Mean Score of C',fontsize=20,labelpad=20)
ax3.set_xlabel('Sub strategy',fontsize=20,labelpad=18)

plt.plot(np.arange(1,len(normdiff_mplusc)+1,1),normdiff_mplusc,color='black',marker='o',
         markersize=10,linewidth=2,label='M+')
plt.plot(np.arange(1,len(normdiff_mminusc)+1,1),normdiff_mminusc,color='darkviolet',marker='o',
         markersize=10,linewidth=2,label='M-')
plt.plot(np.arange(1,len(normdiff_mplusminusc)+1,1),normdiff_mplusminusc,color='red',marker='o',
         markersize=10,linewidth=2,label='M+-')
plt.plot(np.arange(0,8,1),np.zeros(8),'--',linewidth=2,color='black')

plt.legend(loc=[0.1,0.8],fontsize=18,frameon=False)


fig4=plt.figure(figsize=[8,8])
ax4=fig4.add_axes([.15,.1,.8,.8])
ax4.set_xlim(0,4)
ax4.set_ylim(0,1)
ax4.set_xticks([])
ax4.set_yticks(np.arange(0,1.2,0.2))
ax4.set_ylabel('Mean of Mean Score',fontsize=20,labelpad=20)

ax4.bar(0.5,mean_random,1,yerr=ste_random,color='blue',
        error_kw=dict(elinewidth=4,ecolor='black'),label='Random Turns')
ax4.bar(2.5,mean_skewed,1,yerr=ste_skewed,color='green',
        error_kw=dict(elinewidth=4,ecolor='black'),label='Skewed Turns')

plt.legend(loc=[0.1,0.8],fontsize=18,frameon=False)


plt.show()