# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 09:50:48 2016

@author: WAM
"""
import numpy as np
import matplotlib.pylab as plt
from matplotlib.widgets import Slider

def nsslider(mat,nullspace):
    numVectors=len(nullspace)
    sliderHeight=0.05
    
    
    fig = plt.figure()
#    fig.suptitle(title)
    ax = fig.add_subplot(1,1,1)
    plt.subplots_adjust(left=0.25, bottom=sliderHeight*(numVectors+2))
    ax.set_aspect('equal')
    image=plt.imshow(mat,interpolation='nearest',vmin=-4,vmax=4)#,cmap=plt.cm.Blues)
    plt.colorbar()
    
    #initial slider values and list of sliders
    c=[0]*numVectors
    s=[None]*numVectors
    
    def update(val):
        pltmat=np.copy(mat)
        for i in range(0,numVectors):
#            print(" ".join([str(i),str(s[i].val)]))
            pltmat+=s[i].val*nullspace[i]
        image.set_data(pltmat)
        plt.draw()    
    
    for i in range(0,numVectors):
        ax0 = plt.axes([0.25, sliderHeight*(numVectors-i), 0.65, 0.03], axisbg='lightgoldenrodyellow')
        s[i]=Slider(ax0,'Vector '+str(i+1),-6,6,valinit=c[i])
        s[i].on_changed(update)
        
    plt.show()
    
