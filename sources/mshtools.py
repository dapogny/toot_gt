#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import path
import subprocess
import os
import inout
import sys
import numpy as np

#########################################################################
#############  Call to mmg2d for remeshing or LS discretization  ########
#########################################################################

def mmg2d(smesh,ls,ssol,hmin,hmax,hausd,hgrad,nr,out) :
  
  log = open(path.LOGFILE,'a')
  
  if  ls :
    if nr :
      proc = subprocess.Popen(["{mmg} {mesh} -ls -sol {sol} -hmin {hmin} -hmax {hmax} -hausd {hausd} -hgrad {hgrad} -nr {res} -rmc".format(mmg=path.MMG2D,mesh=smesh,sol=ssol,hmin=hmin,hmax=hmax,hausd=hausd,hgrad=hgrad,res=out)],shell=True,stdout=log)
      proc.wait()
    else :
      proc = subprocess.Popen(["{mmg} {mesh} -ls -sol {sol} -hmin {hmin} -hmax {hmax} -hausd {hausd} -hgrad {hgrad} {res} -rmc".format(mmg=path.MMG2D,mesh=smesh,sol=ssol,hmin=hmin,hmax=hmax,hausd=hausd,hgrad=hgrad,res=out)],shell=True,stdout=log)
      proc.wait()
  else :
    if nr :
      proc = subprocess.Popen(["{mmg} {mesh} -hmin {hmin} -hmax {hmax} -hausd {hausd} -hgrad {hgrad} -nr {res} -rmc".format(mmg=path.MMG2D,mesh=smesh,sol=ssol,hmin=hmin,hmax=hmax,hausd=hausd,hgrad=hgrad,res=out)],shell=True,stdout=log)
      proc.wait()
    else :
      proc = subprocess.Popen(["{mmg} {mesh} -hmin {hmin} -hmax {hmax} -hausd {hausd} -hgrad {hgrad} {res} -rmc".format(mmg=path.MMG2D,mesh=smesh,sol=ssol,hmin=hmin,hmax=hmax,hausd=hausd,hgrad=hgrad,res=out)],shell=True,stdout=log)
      proc.wait()
  
  log.close()

#########################################################################
#########################################################################
