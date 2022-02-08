#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import path
import subprocess
import os
import inout
import sys
import mshtools
import numpy as np

###################################################################################
#######         Create computational mesh and initial density Function      #######
#######         Inputs: smesh = (string) path to mesh;                      #######
#######                   ssol = (string) path to ls function               #######
###################################################################################
def iniGeom(smesh,ssol) :
  
  # Fill in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=smesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiName",attval=ssol)

  # Call to FreeFem for creating the background mesh
  log = open(path.LOGFILE,'a')
  proc = subprocess.Popen(["{FreeFem} {file} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,file=path.FFINIMSH)],shell=True,stdout=log)
  proc.wait()
  log.close()
  
  # Call to mmg2d for remeshing the background mesh
  mshtools.mmg2d(smesh,0,ssol,path.HMIN,path.HMAX,path.HAUSD,path.HGRAD,0,smesh)
  
  # Call to FreeFem for creating the initial density function
  log = open(path.LOGFILE,'a')
  proc = subprocess.Popen(["{FreeFem} {file} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,file=path.FFINIDENS)],shell=True,stdout=log)
  proc.wait()
  log.close()

###################################################################################
###################################################################################
