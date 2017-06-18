# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 19:01:07 2015

@author: Sriram
"""

import numpy as np
import matplotlib.pyplot as plt
import math

tau=1
    
time=np.arange(0,10,0.1)
memory=np.zeros(100)
t=0
while t<100:
    memory[t]=math.exp(-time[t]/tau)
    t+=1
    
flank1=np.zeros(10)
flank2=np.zeros(5)
memory1=np.hstack((flank1,memory,flank1))
memory2=np.hstack((flank1,flank2,memory,flank2))
memory3=np.hstack((flank1,flank1,memory))
T=np.arange(0,12,0.1)

fig = plt.figure(figsize = [12,8])
plt.rc('xtick', labelsize=18) 
plt.rc('ytick', labelsize=18)

ax1=plt.subplot(4,2,1)
ax1.plot(T,memory1,linewidth=2,color='green')
ax1.set_xlim(0,4)
ax1.set_ylim(-2.2,2.2)
ax1.set_xticks(())
ax1.set_yticks((-2,0,2))

ax2=plt.subplot(4,2,3)
ax2.plot(T,memory2,linewidth=2,color='green')
ax2.set_xlim(0,4)
ax2.set_ylim(-2.2,2.2)
ax2.set_xticks(())
ax2.set_yticks((-2,0,2))

ax3=plt.subplot(4,2,5)
ax3.plot(T,memory3,linewidth=2,color='green')
ax3.set_xlim(0,4)
ax3.set_ylim(-2.2,2.2)
ax3.set_xticks(())
ax3.set_yticks((-2,0,2))

ax4=plt.subplot(4,2,7)
ax4.plot(T,memory1+memory2+memory3,linewidth=2,color='green')
ax4.set_xlim(0,4)
ax4.set_ylim(-2.2,2.2)
ax4.set_xticks((0,2,4))
ax4.set_yticks((-2,0,2))

ax5=plt.subplot(4,2,2)
ax5.plot(T,-memory1,linewidth=2,color='green')
ax5.set_xlim(0,4)
ax5.set_ylim(-2.2,2.2)
ax5.set_xticks(())
ax5.set_yticks((-2,0,2))

ax6=plt.subplot(4,2,4)
ax6.plot(T,-memory2,linewidth=2,color='green')
ax6.set_xlim(0,4)
ax6.set_ylim(-2.2,2.2)
ax6.set_xticks(())
ax6.set_yticks((-2,0,2))

ax7=plt.subplot(4,2,6)
ax7.plot(T,-memory3,linewidth=2,color='green')
ax7.set_xlim(0,4)
ax7.set_ylim(-2.2,2.2)
ax7.set_xticks(())
ax7.set_yticks((-2,0,2))

ax8=plt.subplot(4,2,8)
ax8.plot(T,-(memory1+memory2+memory3),linewidth=2,color='green')
ax8.set_xlim(0,4)
ax8.set_ylim(-2.2,2.2)
ax8.set_xticks((0,2,4))
ax8.set_yticks((-2,0,2))

ax8.set_xlabel('Time(s)',fontsize=20,labelpad=20)
ax4.set_xlabel('Time (s)',fontsize=20,labelpad=20)
ax1.set_title('M+',fontsize=20)
ax5.set_title('M-',fontsize=20)
fig.suptitle('Gradient Memory',fontsize=20)

plt.show()