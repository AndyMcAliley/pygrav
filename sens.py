# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 16:43:28 2016

@author: WAM
"""

#import math
#import scipy as sc
#import scipy.sparse as sparse
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
    
def plotmat(mat,title,fignum):
    fig = plt.figure(fignum)
    fig.suptitle(title)
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    #TODO: try using pcolormesh
#    plt.imshow(mat,interpolation='nearest',vmin=-1,vmax=1)#,cmap=plt.cm.Blues)
    plt.imshow(mat,interpolation='nearest',vmin=0,vmax=1)
    plt.colorbar()
    plt.savefig(title+'.png',bbox_inches='tight')

#def main():
#mesh
xnodes=np.arange(0,801,200)
znodes=np.arange(0,801,200)
nxcells=len(xnodes)-1
nzcells=len(znodes)-1
dims=(nxcells,nzcells)

#data locations
#xlocs=[290,390,490,590]
n=10
xlocs=np.linspace(0,800,num=n)
zlocs=[-50]
n=len(xlocs)*len(zlocs)

G=sens2d(xnodes,znodes,xlocs,zlocs)

#plot sensitivity of model to each datum

#for row in G:
#    plotmat(row)

#include noise
sd=0.5
WD=np.identity(n)/sd
G=np.dot(WD,G)
    
#Perform SVD
U,s,V = np.linalg.svd(G,full_matrices=True)
rank=len(s) #maybe this should be len(s!=0)
degFreedom=nxcells*nzcells-rank
Vecon=V[:rank,:]

#plot diagonal of V*V.T (econ version of V)
#measure of how much each model cell is controlled by 
#G's row space (1 minus measure of same for null space)
res=np.dot(Vecon.T,Vecon)
res=np.diag(res)
res=np.reshape(res,dims).T
plotmat(res,'Diagonal of Resolution Matrix',98)

#plot complement of the above plot
#measure of how much each model cell is controlled by 
#G's null space (1 minus measure of same for row space)
Vnull=V[-degFreedom:,:]
nullres=np.dot(Vnull.T,Vnull)
nullres=np.diag(nullres)
nullres=np.reshape(nullres,dims).T
plotmat(nullres,'Complement of Diagonal of Resolution Matrix',97)

#plot diagonal of smallest model Tikhonov resolution matrix
#for beta=1
#Don't need full SVD to do this
ssquared=s*s
beta=1
butterworth=ssquared/(ssquared+beta)
butterworth=np.append(butterworth,[0]*degFreedom)
tikres=V*V
tikres=(tikres.T*butterworth).T
tikres=np.sum(tikres,0)
tikres=np.reshape(tikres,dims).T
plotmat(tikres,'Min Norm Tik Resolution Matrix',99)

#form list of matrices shaped appropriately
#All right singular vectors
rSpace=[]
for row in V:
    rMat=np.reshape(row,dims).T
    rSpace.append(rMat)

##Plot all singular vectors
#irow=1
#for rMat in rSpace:
#    title="".join(('Vector ',str(irow),' of ',str(n)))
#    plotmat( rMat,title,irow )
#    irow+=1

#form list of matrices shaped appropriately
nullVectors=V[-degFreedom:]
nullSpace=[]
for row in nullVectors:
    nullMat=np.reshape(row,dims).T
    nullSpace.append(nullMat)

##Plot null vectors only
#irow=1
#for mat in nullSpace:
#    title="".join(('Vector ',str(irow),' of ',str(degFreedom)))
#    plotmat( mat,title,irow )
#    irow+=1    
    
#Test sliders
#test model
model=np.zeros(dims)
model[1,1]=2
model[2,1]=0.5
#null0=np.reshape(V[13],dims).T
#bad place for an import!
import NullSpaceSlider as ns
ns.interactiveModel(model,rSpace,s,G,xnodes,znodes,xlocs,sd)

#if __name__=='__main__':
#    main()