# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 09:50:48 2016

@author: WAM
"""
import numpy as np
import matplotlib.pylab as plt
from matplotlib.widgets import Slider

def interactiveModel(mat,vectors,singularValues,sens,xnodes,znodes,dataLocations,errors):
    numCells=mat.size
    rank=len(singularValues)
    numVectors=len(vectors)
    sliderAxisHeight=0.8/(numVectors+1)
    sliderHeight=0.6*sliderAxisHeight
    sliderWidth=0.25
    
    #Calculate Data
    model=np.reshape(mat.T,(numCells))
    data=sens.dot(model)
    
    fig = plt.figure()
#    fig.suptitle(title)
    #plot data
    ax = fig.add_subplot(2,2,1)
    plt.errorbar(dataLocations,data,yerr=errors)
    dataplot=plt.plot(dataLocations,data)
#    plt.axis('off')
    
    #plot model
    ax = fig.add_subplot(2,2,3)
#    plt.subplots_adjust(right=sliderWidth+.05) #top=sliderHeight*(numVectors+2))
#    ax.set_aspect('equal')
    modelplot=plt.imshow(mat,aspect='auto',interpolation='nearest',vmin=-4,vmax=4)#,cmap=plt.cm.Blues)
#    modelplot=plt.pcolormesh(X,Y,C,vmin=-4,vmax=4)
#    plt.colorbar()
    plt.axis('off')
    #initial slider values and list of sliders
    c=[0]*numVectors
    sliders=[None]*numVectors
    
    #executes when a slider value changes
    def update(val):
        pltmat=np.copy(mat)
        for i in range(0,numVectors):
            pltmat+=sliders[i].val*vectors[i]
        modelplot.set_data(pltmat)
        model=np.reshape(pltmat.T,(numCells))
        data=sens.dot(model)
        plt.setp(dataplot,'ydata',data)
        plt.draw()
    
    #set sliders in figure
    for i in range(0,rank):
        ax0 = plt.axes([0.9-sliderWidth, sliderAxisHeight*(numVectors-i+2), sliderWidth, sliderHeight], axisbg='lightgoldenrodyellow')
#        sliders[i]=Slider(ax0,'Vector '+str(i+1),-6,6,valinit=c[i])
        labelstr='s={0:.2g}'.format(singularValues[i])
        sliders[i]=Slider(ax0,labelstr,-6,6,valinit=c[i])
        sliders[i].on_changed(update)
    for i in range(rank,numVectors):
        ax0 = plt.axes([0.9-sliderWidth, sliderAxisHeight*(numVectors-i+1), sliderWidth, sliderHeight], axisbg='lightgray')
#        sliders[i]=Slider(ax0,'Vector '+str(i+1),-6,6,valinit=c[i])
        sliders[i]=Slider(ax0,'s=0',-6,6,valinit=c[i])
        sliders[i].on_changed(update)
        
    plt.show()
    
