#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import os
import sys

# Global parameters
REFDIR        = 1
REFNEU        = 2
MESHSIZ       = 0.02
HMIN          = 0.02
HMAX          = 0.02
HAUSD         = 0.001
HGRAD         = 1.3
EPSOT         = 0.01  # Entropic regularization parameter
EPS           = 1e-10 # Precision parameter
EPSP          = 1e-20 # Precision parameter for packing
ALPHA         = 0.03 # Regularization parameter for velocity extension / regularization
MAXIT         = 200
OTMAXIT       = 50   # Maximum number of iterations for the Sinkhorn algorithm
MAXCOEF       = 0.2
MINCOEF       = 0.005
TOL           = 0.005
VTARG         = 0.7
HEAVREG       = 3.0 # 3.0
BETA          = 0.98   # Objective function = BETA*W(\Om) + (1-BETA)*C(\Om)

# Parameters for the null space optimization algorithm
AJ            = 1.0
AG            = 0.6
ITMAXNORMXIJ  = 200

# Paths to folders
RES = "./res/"
SCRIPT = "./sources/"

# Call for the executables of external codes
FREEFEM = "FreeFem++"
MSHDIST = "/Users/dapogny/Mshdist/build/mshdist"
ADVECT  = "/Users/dapogny/Advection/build/advect"
MMG2D   = "/Users/dapogny/mmg/build/bin/mmg2d_O3"

# Path to FreeFem scripts
FFINIMSH     = SCRIPT + "inimsh.edp"
FFINIDENS    = SCRIPT + "inidens.edp"
FFELAS       = SCRIPT + "elasticity.edp"
FFCPLY       = SCRIPT + "compliance.edp"
FFVOL        = SCRIPT + "volume.edp"
FFDESCENTNS  = SCRIPT + "descentNS.edp"
FFDESCENTAL  = SCRIPT + "descentAL.edp"
FFUPDENS     = SCRIPT + "updens.edp"
FFREGFILTER  = SCRIPT + "regfilter.edp"

# Names of output and exchange files
EXCHFILE = RES + "exch.data"
LOGFILE  = RES + "log.data"
STEP     = RES + "step"
TMPSOL   = "./res/temp.sol"
MESH     = RES + "box.mesh"

# Step files
def step(n,typ) :
  if typ == 'm' :
    return STEP + "." + str(n) + ".mesh"
  elif typ == 's' :
    return STEP + "." + str(n) + ".sol"
  elif typ == 'gs' :
    return STEP + "." + str(n) + ".grad.sol"
  elif typ == 'ps' :
    return STEP + "." + str(n) + ".phi.sol"
  elif typ == 'prs' :
    return STEP + "." + str(n) + ".phiR.sol"
  elif typ == 'us' :
    return STEP + "." + str(n) + ".u.sol"
  elif typ == 'otgs' :
    return STEP + "." + str(n) + ".OT.grad.sol"
  elif typ == 'cpgs' :
    return STEP + "." + str(n) + ".CP.grad.sol"
  elif typ == 'vgs' :
    return STEP + "." + str(n) + ".vol.grad.sol"

