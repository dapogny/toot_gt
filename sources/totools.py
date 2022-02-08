#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import subprocess
import inout
import os
import path
import sys
import numpy as np

#####################################################################################
#######   Regularization filter for the density function                      #######
#######       inputs: smesh (string): mesh of the computational domain        #######
#######               sphi (string): density function for design              #######
#######               snphi (string): returned density function               #######
#####################################################################################

def regulFilter(smesh,sphi,snphi) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=smesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiName",attval=sphi)
  inout.setAtt(file=path.EXCHFILE,attname="SolName",attval=snphi)
  
  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {elasticity} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,elasticity=path.FFREGFILTER)],shell=True)
  proc.wait()

#####################################################################################
#####################################################################################

#####################################################################################
#######   Update of the density function                                      #######
#######       inputs: smesh (string): mesh of the computational domain        #######
#######               sg (string): descent direction                          #######
#######               sphi (string): density function for design              #######
#######               snphi (string): returned density function               #######
#######               dt (double): time step                                  #######
#####################################################################################

def updens(smesh,sg,sphi,snphi,dt) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=smesh)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=sg)
  inout.setAtt(file=path.EXCHFILE,attname="PhiName",attval=sphi)
  inout.setAtt(file=path.EXCHFILE,attname="SolName",attval=snphi)
  inout.setAtt(file=path.EXCHFILE,attname="TimeStep",attval=dt)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {elasticity} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,elasticity=path.FFUPDENS)],shell=True)
  proc.wait()

#####################################################################################
#####################################################################################
