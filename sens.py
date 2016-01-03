# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 16:43:28 2016

@author: WAM
"""

import math
import scipy as sc
import scipy.sparse as sparse
import numpy as np
import grav

#mesh
xnodes=np.arange(0,801,200)
znodes=np.arange(0,801,200)
nxcells=len(xnodes)-1
nzcells=len(znodes)-1
#data locations
xlocs=[250,350,450,550]
zlocs=[-50]

#get number of data and model cells
n=len(xlocs)*len(zlocs)
m=(len(xnodes)-1)*(len(znodes)-1)
#initialize sensitivity matrix
sens2D=np.zeros((n,m))
#sens3D=np.zeros((n,m))
#for sens3D, to approximate infinite dimension
yn=[-10000,10000]
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

