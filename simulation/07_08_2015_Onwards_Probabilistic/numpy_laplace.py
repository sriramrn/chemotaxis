# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 18:37:09 2015

@author: Sriram
"""

import numpy as np
import matplotlib.pyplot as plt


ma=0
sa=1

mb=0
sb=2

mc=0
sc=3

nsamples=1000000
sone=np.zeros(nsamples)
stwo=np.zeros(nsamples)
sthree=np.zeros(nsamples)
i=0
while i<nsamples:
    
    sone[i]=np.random.laplace(ma,sa)
    stwo[i]=np.random.laplace(mb,sb)
    sthree[i]=np.random.laplace(mc,sc)

    while sone[i]<0 or sone[i]>8:
        sone[i]=np.random.laplace(ma,sa)
    while stwo[i]<0 or stwo[i]>8:
        stwo[i]=np.random.laplace(mb,sb)
    while sthree[i]<0 or sthree[i]>8:
        sthree[i]=np.random.laplace(mc,sc)

    i+=1
    
hista,counta=np.histogram(sone,bins=50,range=[0,9])
histb,countb=np.histogram(stwo,bins=50,range=[0,9])
histc,countc=np.histogram(sthree,bins=50,range=[0,9])

pdf_a=hista/sum(hista)
pdf_b=histb/sum(histb)
pdf_c=histc/sum(histc)

x=np.arange(0,9,0.18)


fig=plt.figure(figsize=[12,8])
plt.rc('xtick', labelsize=18) 
plt.rc('ytick', labelsize=18)

axis=fig.add_axes([.15,.15,.8,.8])
axis.set_xlim(0,8)
axis.set_ylim(0,0.15)
axis.set_xticks(np.arange(0,10,2))
axis.set_yticks(np.arange(0.05,0.20,0.05))
axis.set_xlabel('Run Duration (s)',fontsize=20,labelpad=20)
axis.set_ylabel('Probability Density',fontsize=20,labelpad=20)

plt.plot(x,pdf_a,linewidth=2,color='blue',label='Tau = 1s')
plt.plot(x,pdf_b,linewidth=2,color='green',label='Tau = 2s')
plt.plot(x,pdf_c,linewidth=2,color='red',label='Tau = 3s')

plt.legend(loc=[0.65,0.75],fontsize=18,frameon=False)

plt.show()