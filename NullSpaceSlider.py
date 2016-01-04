# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 09:50:48 2016

@author: WAM
"""
import matplotlib.pylab as plt
from matplotlib.widgets import Slider

def nsslider(mat,nullspace):
    fig = plt.figure()
#    fig.suptitle(title)
    ax = fig.add_subplot(1,1,1)
    plt.subplots_adjust(left=0.25, bottom=0.25)
    ax.set_aspect('equal')
    image=plt.imshow(mat,interpolation='nearest',vmin=-3,vmax=3)#,cmap=plt.cm.Blues)
    plt.colorbar()
    
    #initial slider value
    c0=0
    
    ax0 = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg='lightgoldenrodyellow')
    s0=Slider(ax0,'Null space singular vector 1',-2,2,valinit=c0)
    
    def update(val):
        pltmat=mat+s0.val*nullspace
        image.set_data(pltmat)
        plt.draw()
    s0.on_changed(update)
        
    plt.show()
        
