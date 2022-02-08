#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import subprocess
import inout
import os
import path
import sys
import numpy as np

#####################################################################################
#######   Numerical solver for elasticity                                     #######
#######       inputs: smesh (string): mesh of the computational domain        #######
#######       inputs: sphir (string): regularized density function            #######
#######               su (string): output elastic displacement                #######
#####################################################################################

def elasticity(smesh,sphir,su) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=smesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiRName",attval=sphir)
  inout.setAtt(file=path.EXCHFILE,attname="SolName",attval=su)
  
  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {elasticity} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,elasticity=path.FFELAS)],shell=True)
  proc.wait()

#####################################################################################
#####################################################################################

#####################################################################################
#######   Evaluation of the elastic compliance and its gradient               #######
#######       inputs: smesh (string): mesh of the computational domain        #######
#######       inputs: sphir (string): regularized density function            #######
#######               su (string): elastic displacement                       #######
#######               sg (string): gradient of elastic compliance             #######
#####################################################################################

def complianceGrad(smesh,sphir,su,sg) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=path.MESH)
  inout.setAtt(file=path.EXCHFILE,attname="PhiRName",attval=sphir)
  inout.setAtt(file=path.EXCHFILE,attname="SolName",attval=su)
  inout.setAtt(file=path.EXCHFILE,attname="CpGradName",attval=sg)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {compliance} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,compliance=path.FFCPLY)],shell=True)
  proc.wait()
  
  # Return compliance
  [cply] = inout.getrAtt(file=path.EXCHFILE,attname="Compliance")
  
  return cply

#####################################################################################
#####################################################################################

#####################################################################################
#######   Evaluation of the volume and its gradient                           #######
#######       inputs: smesh (string): mesh of the computational domain        #######
#######       inputs: sphir (string): regularized density function            #######
#######               sg (string): gradient of volume                         #######
#####################################################################################

def volumeGrad(smesh,sphir,sg) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=path.MESH)
  inout.setAtt(file=path.EXCHFILE,attname="PhiRName",attval=sphir)
  inout.setAtt(file=path.EXCHFILE,attname="VolGradName",attval=sg)
    
  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {compliance} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,compliance=path.FFVOL)],shell=True)
  proc.wait()
  
  # Return volume
  [vol] = inout.getrAtt(file=path.EXCHFILE,attname="Volume")
  
  return vol

#####################################################################################
#####################################################################################

#######################################################################################
#####             Calculation of the (normalized) descent direction               #####
#####                     via the Null Space optimization algorithm               #####
#####      inputs : smesh: (string for) mesh ;                                    #####
#####                 sgCp: (string for) gradient of Compliance                   #####
#####                 sgV:  (string for) gradient of Volume                       #####
#####                 sg: (string for) output total gradient                      #####
#######################################################################################

def descentNS(smesh,sgCp,sgV,sg) :

  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=smesh)
  inout.setAtt(file=path.EXCHFILE,attname="CpGradName",attval=sgCp)
  inout.setAtt(file=path.EXCHFILE,attname="volGradName",attval=sgV)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=sg)
  
  # Velocity extension - regularization via FreeFem
  proc = subprocess.Popen(["{FreeFem} {ffdescent} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,ffdescent=path.FFDESCENTNS)],shell=True)
  proc.wait()

#######################################################################################
#######################################################################################

#######################################################################################
#####             Calculation of the (normalized) descent direction               #####
#####                        via the Augmented Lagrangian algorithm               #####
#####      inputs : smesh: (string for) mesh ;                                    #####
#####                 sgCp: (string for) gradient of Compliance                   #####
#####                 sgV:  (string for) gradient of Volume                       #####
#####                 sg: (string for) output total gradient                      #####
#######################################################################################

def descentAL(smesh,sgCp,sgV,sg) :

  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=smesh)
  inout.setAtt(file=path.EXCHFILE,attname="CpGradName",attval=sgCp)
  inout.setAtt(file=path.EXCHFILE,attname="volGradName",attval=sgV)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=sg)
  
  # Velocity extension - regularization via FreeFem
  proc = subprocess.Popen(["{FreeFem} {ffdescent} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,ffdescent=path.FFDESCENTAL)],shell=True)
  proc.wait()

#######################################################################################
#######################################################################################

#######################################################################################
#####                         Evaluation of the merit function                    #####
#####                     in the Null Space optimization algorithm                #####
#####      inputs : smesh: (string for) mesh                                      #####
#####               W: (real) value of the OT functional                          #####
#####      outputs : merit: (real) value of the merit of shape                    #####
#####                vol: (real) volume of shape                                  #####
#######################################################################################

def evalObjNS(smesh,Cp,vol) :

  # Read parameters in the exchange file
  [alphaJ] = inout.getrAtt(file=path.EXCHFILE,attname="alphaJ")
  [alphaG] = inout.getrAtt(file=path.EXCHFILE,attname="alphaG")
  [ell] = inout.getrAtt(file=path.EXCHFILE,attname="Lagrange")
  [m] = inout.getrAtt(file=path.EXCHFILE,attname="Penalty")
  [vtarg] = inout.getrAtt(file=path.EXCHFILE,attname="VolumeTarget")

  merit = alphaJ*(Cp - ell*(vol-vtarg)) + 0.5*alphaG/m*(vol-vtarg)**2

  return merit

#######################################################################################
#######################################################################################

#######################################################################################
#####                         Evaluation of the merit function                    #####
#####                     in the Augmented Lagrangian algorithm                   #####
#####      inputs : smesh: (string for) mesh                                      #####
#####               W: (real) value of the OT functional                          #####
#####      outputs : merit: (real) value of the merit of shape                    #####
#####                vol: (real) volume of shape                                  #####
#######################################################################################

def evalObjAL(smesh,Cp,vol) :

  # Read parameters in the exchange file
  [lmo] = inout.getrAtt(file=path.EXCHFILE,attname="lmAL")
  [muo] = inout.getrAtt(file=path.EXCHFILE,attname="penAL")
  [vtarg] = inout.getrAtt(file=path.EXCHFILE,attname="VolumeTarget")

  merit = Cp - lmo*(vol-vtarg) + 0.5*muo*(vol-vtarg)**2

  return merit

#######################################################################################
#######################################################################################
