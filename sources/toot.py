#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import os
import sys
sys.path.append('/Users/dapogny/libkeops')

import path
import inout
import mshtools
import mechtools
import totools
import inigeom
import subprocess
import numpy as np

########################################################
##################   START PROGRAM   ###################
########################################################
print("**********************************************")
print("********************* Toot *******************")
print("**********************************************")

# Initialize folders and files
inout.iniWF()

# Create computational mesh and initial density function
inigeom.iniGeom(path.MESH,path.step(0,"ps"))

# Regularization filter
totools.regulFilter(path.MESH,path.step(0,"ps"),path.step(0,"prs"))

# Resolution of the linear elasticity system
mechtools.elasticity(path.MESH,path.step(0,"prs"),path.step(0,"us"))

# Evaluate initial objective and constraint functions
newCp  = mechtools.complianceGrad(path.step(0,"m"),path.step(0,"prs"),path.step(0,"us"),path.step(0,"cpgs"))
newvol = mechtools.volumeGrad(path.step(0,"m"),path.step(0,"prs"),path.step(0,"vgs"))

# Initial values for the parameters of the augmented Lagrangian
lmo = 0.01*(newvol-path.VTARG)/path.VTARG;
muo = 0.2*(newvol/path.VTARG)*abs(lmo);

# Main loop
coef = 0.1 # Maximum change in the values of the density within 1 iteration
for n in range(0,path.MAXIT) :

  print("Iteration {}".format(n))
  scurphi       = path.step(n,"ps")
  snewphi       = path.step(n+1,"ps")
  scurphiR      = path.step(n,"prs")
  snewphiR      = path.step(n+1,"prs")
  scuru         = path.step(n,"us")
  snewu         = path.step(n+1,"us")
  scurgrad      = path.step(n,"gs")
  scurCPgrad    = path.step(n,"cpgs")
  snewCPgrad    = path.step(n+1,"cpgs")
  scurvolgrad   = path.step(n,"vgs")
  snewvolgrad   = path.step(n+1,"vgs")
  Cp = newCp
  vol = newvol
  
  # Set parameters of the Augmented Lagrangian
  inout.setAtt(file=path.EXCHFILE,attname="lmAL",attval=lmo)
  inout.setAtt(file=path.EXCHFILE,attname="penAL",attval=muo)
    
  # Update Heaviside filter parameter
  if 0 and n == 30 :
    path.HEAVREG = path.HEAVREG + 2.0
    inout.setAtt(file=path.EXCHFILE,attname="HeavisideRegularization",attval=path.HEAVREG)
    mechtools.elasticity(path.MESH,scurphiR,scuru)
    Cp  = mechtools.complianceGrad(path.MESH,scurphiR,scuru,scurCPgrad)
    vol = mechtools.volumeGrad(path.MESH,scurphiR,scurvolgrad)

  # Calculation of the descent direction
  mechtools.descentNS(path.MESH,scurCPgrad,scurvolgrad,scurgrad)
  # mechtools.descentAL(path.MESH,scurCPgrad,scurvolgrad,scurgrad)

  # Evaluation of initial merit
  # merit = mechtools.evalObjAL(path.MESH,Cp,vol)
  merit = mechtools.evalObjNS(path.MESH,Cp,vol)
  print("Merit {}, CP value {} and volume {}".format(merit,Cp,vol))
  
  # Line search procedure
  print("  Line search procedure")
  for k in range(0,10) :
    print("  k = {}".format(k))
    
    # Update of the design
    totools.updens(path.MESH,scurgrad,scurphi,snewphi,coef)
    
    # Regularization filter
    totools.regulFilter(path.MESH,snewphi,snewphiR)
  
    # Resolution of the linear elasticity system
    mechtools.elasticity(path.MESH,snewphiR,snewu)

    # Evaluation of the new merit
    newCp    = mechtools.complianceGrad(path.MESH,snewphiR,snewu,snewCPgrad)
    newvol   = mechtools.volumeGrad(path.MESH,snewphiR,snewvolgrad)
    # newmerit = mechtools.evalObjAL(path.MESH,newCp,newvol)
    newmerit = mechtools.evalObjNS(path.MESH,newCp,newvol)

    # Decision
    # Iteration accepted
    if ( ( newmerit < merit + path.TOL*abs(merit) ) or ( k == 2 ) or ( coef < path.MINCOEF) ) :
      coef = min(path.MAXCOEF,1.1*coef)
      print("New merit {}, CP value {} and volume {}".format(newmerit,newCp,newvol))
      break
    # Iteration rejected
    else :
      coef = max(path.MINCOEF,0.6*coef)
    
  # Update of the coefficients of the Augmented Lagrangian
  lmo = lmo - muo*(newvol-path.VTARG);
  if  ( n != 0 ) and ( n%3 == 0 ) and ( n <= 70 ) :
    muo = muo*1.4


########################################################
####################   END PROGRAM   ###################
########################################################

print("**********************************************")
print("****************** End of Toot ***************")
print("**********************************************")
