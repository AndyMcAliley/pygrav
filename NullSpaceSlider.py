# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 09:50:48 2016

@author: WAM
"""
import numpy as np
import matplotlib.spines as sp
import matplotlib.pylab as plt
from matplotlib.widgets import Slider
from matplotlib.widgets import Button

def interactiveModel(mat,vectors,singularValues,sens,xnodes,znodes,dataLocations,noise,sd,modelmin):
    (numData,numCells)=sens.shape
    rank=len(singularValues)
    numVectors=len(vectors)
    sliderAxisHeight=.9/(numVectors+1)
    sliderHeight=0.6*sliderAxisHeight
    sliderWidth=0.25
    buttonWidth=0.15
    sliderMax=15
    sliderMin=-15
    colorbarMax=6
    colorbarMin=-6
    
    #Calculate Data
    model=np.reshape(mat.T,(numCells))
    truedata=sens.dot(model)
    noisydata=truedata+noise
    
    fig = plt.figure()
#    fig.suptitle(title)
    #plot data
    dataSubplot = fig.add_subplot(2,2,1)
    plt.errorbar(dataLocations,noisydata,yerr=sd*2)#*numData**(0.5))
    data=np.copy(truedata)
    dataplot=plt.plot(dataLocations,data)
#    plt.axis('off')
    
    #plot model
    modelSubplot = fig.add_subplot(2,2,3)
#    plt.subplots_adjust(right=sliderWidth+.05) #top=sliderHeight*(numVectors+2))
#    ax.set_aspect('equal')
    modelplot=plt.imshow(mat,aspect='auto',interpolation='nearest',vmin=colorbarMin,vmax=colorbarMax)#,cmap=plt.cm.Blues)
#    modelplot=plt.pcolormesh(X,Y,C,vmin=-4,vmax=4)
#    plt.colorbar()
#    plt.axis('off')
    modelplot.axes.get_xaxis().set_ticks([])
    modelplot.axes.get_yaxis().set_ticks([])
    
    #initial slider values and list of sliders
    c=[0]*numVectors
    for i in range(0,numVectors):
        c[i]=np.tensordot(mat,vectors[i],axes=2)
    sliders=[None]*numVectors
    
    #executes when a slider value changes
    def update(val):
#        pltmat=np.copy(mat)
        #plot new model
        pltmat=np.zeros(mat.shape)
        for i in range(0,numVectors):
            pltmat+=sliders[i].val*vectors[i]
        modelplot.set_data(pltmat)
        #change border if any model cell is less than modelmin
        if (pltmat>=modelmin).all():
            modelbordercolor='black'
            modelborderwidth=1
        else:
            modelbordercolor='red'
            modelborderwidth=4
        for child in modelSubplot.get_children():
            if isinstance(child,sp.Spine):
                child.set_color(modelbordercolor)
                child.set_linewidth(modelborderwidth)
        #calculate data
        model=np.reshape(pltmat.T,(numCells))
        data=sens.dot(model)
        #plot data
        plt.setp(dataplot,'ydata',data)
        #calculate data misfit
        phid=np.linalg.norm((data-truedata)/sd)**2
        #change border if data misfit is greater than expected
        if phid > numData:
            databordercolor='red'
            databorderwidth=4
        else:
            databordercolor='black'
            databorderwidth=1
        for child in dataSubplot.get_children():
            if isinstance(child,sp.Spine):
                child.set_color(databordercolor)
                child.set_linewidth(databorderwidth)
        plt.draw()
    
    #set sliders in figure
    for i in range(0,rank):
        ax0 = plt.axes([0.9-sliderWidth, sliderAxisHeight*(numVectors-i+2), sliderWidth, sliderHeight], axisbg='lightgoldenrodyellow')
#        sliders[i]=Slider(ax0,'Vector '+str(i+1),-6,6,valinit=c[i])
        labelstr='s={0:.2g}'.format(singularValues[i])
        sliders[i]=Slider(ax0,labelstr,sliderMin,sliderMax,valinit=c[i])
        sliders[i].on_changed(update)
    for i in range(rank,numVectors):
        ax0 = plt.axes([0.9-sliderWidth, sliderAxisHeight*(numVectors-i+1), sliderWidth, sliderHeight], axisbg='lightgray')
#        sliders[i]=Slider(ax0,'Vector '+str(i+1),-6,6,valinit=c[i])
        sliders[i]=Slider(ax0,'s=0',sliderMin,sliderMax,valinit=c[i])
        sliders[i].on_changed(update)
        
    def resetSliders(self):
        for sl in sliders:
            sl.reset()
    #set reset button
    ax0=plt.axes([0.9-buttonWidth,sliderAxisHeight,buttonWidth,sliderHeight])
    reset=Button(ax0,'True model')
    reset.on_clicked(resetSliders)
        
    plt.show()
    
