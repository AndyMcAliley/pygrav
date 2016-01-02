# -*- coding: utf-8 -*-
"""
Spyder Editor

Tools to form sensitivity matrices for 2D and 3D gravity problems.
"""

import math
import scipy as sc
import scipy.sparse as sparse
import numpy as np

def gc3d( x,y,z ):
   "function_docstring"
   #geometric factor for obs point at origin
   #multiply by gamma*rho for g
   #from Blakely
   
   r=math.sqrt(x**2 + y**2 + z**2)
   #Blakely
   result=z*math.atan2(x*y,z*r) - x*math.log(r+y) - y*math.log(r+x)
   #Okabe
   #result=2*z*math.atan2(x+y+r,z) + x*math.log(r+y) + y*math.log(r+x)
   return result

def g_3drect( xlims,ylims,zlims ):
   "function_docstring"
   #geometric factor for obs point at origin
   #multiply by gamma*rho for gz
   #from Blakely
   
   sum = 0
   for ii in range(1,2):
       for jj in range(1,2):
           for kk in range(1,2):
               mu = (-1)**ii*(-1)**jj*(-1)**kk
               sum = sum + mu*gc3d(xlims[ii-1],ylims[jj-1],zlims[kk-1])
   return sum

def gc2d( x,z ):
    #A corner of a 2D rectangle (infinite extent in y)
    
    result=x*math.log(x**2+z**2)+2*z*math.atan2(x,z)
    return result

def g_2drect( xlims,zlims ):
    #geometric factor for a rectangle (infinite extent in y)
    #obs point at origin
    #multiply by gamma*rho for gz
    
#    import math
#    
#    return (xlims[1]*math.log((xlims[1]**2+zlims[1]**2)/(xlims[1]**2+zlims[0]**2))+
#           xlims[0]*math.log((xlims[0]**2+zlims[0]**2)/(xlims[0]**2+zlims[1]**2))+
#           2*zlims[1]*(math.atan2(xlims[1],zlims[1])-math.atan2(xlims[0],zlims[1]))+
#           2*zlims[0]*(math.atan2(xlims[0],zlims[0])-math.atan2(xlims[1],zlims[0])))
    sum=0
    for ii in range(1,2):
        for jj in range(1,2):
            mu=(-1)**ii*(-1)**jj
            sum=sum+mu*gc2d(xlims[ii-1],zlims[jj-1])
    return sum

def g_2dmesh( xnodes,znodes ):
    #geometric factors for a 2D mesh
    #obs point at origin
    #multiply by gamma*rho for gz
    
    #get dimensions
    nx=len(xnodes)
    nz=len(znodes)
    #construct matrix to calculate factors from corners
    corners2factors=sparse.kron(spFD1D(nx),spFD1D(nz))
    #initialize corners vector
    corners=np.zeros((1,nx*nz))
    i=0
    for x in xnodes:
        for z in znodes:
            corners[i]=gc2d( x,z )
            i+=1
    factors=corners2factors.dot(corners)
    return factors

def spFD1D(n):
    #Construct sparse 1D finite difference matrix
    #n elements; n-1 differences
    #Result is n-1 rows by n columns
    e=np.ones((2,n-1))
    e[0]=-e[0]
    mat=sparse.diags(e,[0,1],shape=[n-1,n])
    return mat

def main():
    #test
    xx=(1,3)
    yy=(1,2)
    zz=(105,120)
    answer=g_3drect(xx,yy,zz)
    print(answer)

if __name__=='__main__':
    main()
