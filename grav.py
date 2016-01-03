# -*- coding: utf-8 -*-
"""
Spyder Editor

Tools to form sensitivity matrices for 2D and 3D gravity problems.
"""

import math
import scipy as sc
import scipy.sparse as sparse
import numpy as np

#output in microGals
#NIST
#gamma=6.67408e-3 # +/- 0.00031
#CGEM
gamma=6.67384e-3

def gc3d( x,y,z ):
   "function_docstring"
   #geometric factor for obs point at origin
   #multiply by gamma*rho for g
   #from Blakely
   
   r=math.sqrt(x**2 + y**2 + z**2)

   result=0 
   if z!=0:
       #Blakely
       #result+=z*math.atan2(x*y,z*r)
       #Okabe
       result+=-2*z*math.atan2(x+y+r,z)
   if x!=0:
       result-=x*math.log(r+y)
   if y!=0:
       result-=y*math.log(r+x)
   return result

def g_3drect( xlims,ylims,zlims ):
   "function_docstring"
   #geometric factor for obs point at origin
   #multiply by gamma*rho for gz
   #from Blakely
   
   sum = 0
   for ii in range(1,3):
       for jj in range(1,3):
           for kk in range(1,3):
               mu = (-1)**ii*(-1)**jj*(-1)**kk
               sum = sum + mu*gc3d(xlims[ii-1],ylims[jj-1],zlims[kk-1])
   return sum*gamma

def gc2d( x,z ):
    #A corner of a 2D rectangle (infinite extent in y)
    result=0
    if z!=0:
        result+=2*z*math.atan2(x,z)
    if x!=0:
        result+=x*math.log(x**2+z**2)
    return result

def g_2drect( xlims,zlims ):
    #geometric factor for a rectangle (infinite extent in y)
    #obs point at origin
    #multiply by gamma*rho for gz
    
    sum=0
    for ii in range(1,3):
        for jj in range(1,3):
            mu=(-1)**ii*(-1)**jj
            sum=sum+mu*gc2d(xlims[ii-1],zlims[jj-1])
    return sum*gamma

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
    corners=np.zeros(nx*nz)
    i=0
    for x in xnodes:
        for z in znodes:
            corners[i]=gc2d( x,z )
            i+=1
    factors=corners2factors.dot(corners)
    return factors*gamma

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
    rho=1
    xx=(50,250)
    yy=(-10000,10000)
    zz=(50,250)
    answer=g_3drect(xx,yy,zz)*rho
    print(answer)
    answer=g_2drect(xx,zz)*rho
    print(answer)

if __name__=='__main__':
    main()
