# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 12:06:49 2016

@author: WAM
"""

import numpy as np
import scipy.sparse as sparse

def invert2D(data,mref,dx,dz,std,beta):
    dobs=data[3]
    Mx=len(dx)
    My=len(dy)
    Mz=len(dz)
    M=Mx*My*Mz
    N=len(data[1])
    
    #simple weighting matrices
    WMTWM=sparse.identity(M)
    WDTWD=1/(std*std)*sparse.identity(N)
    
    
    