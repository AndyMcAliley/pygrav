# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 16:43:28 2016

@author: WAM
"""

import math
import scipy as sc
import scipy.sparse as sparse
import numpy as np
import matplotlib.pylab as plt
import grav

def sens2d( xnodes,znodes,xlocs,zlocs ):
    #get number of data and model cells
    n=len(xlocs)*len(zlocs)
    nxcells=len(xnodes)-1
    nzcells=len(znodes)-1
    m=(nxcells)*(nzcells)
    #initialize sensitivity matrix
    sens2D=np.zeros((n,m))
    #sens3D=np.zeros((n,m))
    #for sens3D, to approximate infinite dimension
    #yn=[-10000,10000]
    irow=0
    #for xloc in np.nditer(xlocs):
    for xloc in xlocs:
        xnodesshifted=xnodes-xloc
        for zloc in zlocs:
            znodesshifted=znodes-zloc
            sens2D[irow]=grav.g_2dmesh( xnodesshifted,znodesshifted )
    #        for ix in range(0,nxcells):
    #            xn=xnodesshifted[ix:ix+2]
    #            for iz in range(0,nzcells):
    #                zn=znodesshifted[iz:iz+2]
    #                sens3D[irow,iz+ix*nzcells]=grav.g_3drect( xn,yn,zn )
            irow+=1
    return sens2D
    
def plotmat(mat):
    mat=np.reshape(mat,(4,4)).T
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    plt.imshow(mat,interpolation='nearest',vmin=-1,vmax=1)#,cmap=plt.cm.Blues)
    plt.colorbar()
    plt.show()

#def main():
#mesh
xnodes=np.arange(0,801,200)
znodes=np.arange(0,801,200)

#data locations
#xlocs=[290,390,490,590]
xlocs=np.arange(0,801,100)
zlocs=[-50]

G=sens2d(xnodes,znodes,xlocs,zlocs)

#plot sensitivity of model to each datum

#for row in G:
#    plotmat(row)
    
#Perform SVD
U,s,V = np.linalg.svd(G,full_matrices=True)

irow=0
for row in V:
    print(irow)
    plotmat(row)
    irow+=1

#if __name__=='__main__':
#    main()