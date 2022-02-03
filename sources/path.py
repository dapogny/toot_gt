#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import os
import sys

# Global parameters
REFDIR        = 1
REFNEU        = 2
MESHSIZ       = 0.05
HMIN          = 0.001
HMAX          = 0.03
HAUSD         = 0.001
HGRAD         = 1.3
EPSOT         = 0.01  # Entropic regularization parameter
EPS           = 1e-10 # Precision parameter
EPSP          = 1e-20 # Precision parameter for packing
ALPHA         = 0.001 # Regularization parameter for velocity extension / regularization
MAXIT         = 200
OTMAXIT       = 50   # Maximum number of iterations for the Sinkhorn algorithm
MAXCOEF       = 2.0
MINCOEF       = 0.02
TOL           = 0.02
AJ            = 1.0
AG            = 0.3
ITMAXNORMXIJ  = 200
VTARG         = 0.5  # 1.0
BETA          = 0.98   # Objective function = BETA*W(\Om) + (1-BETA)*C(\Om)

# Paths to folders
RES = "./res/"
SCRIPT = "./sources/"

# Call for the executables of external codes
FREEFEM = "FreeFem++"
MSHDIST = "/Users/dapogny/Mshdist/build/mshdist"
ADVECT  = "/Users/dapogny/Advection/build/advect"
MMG2D   = "/Users/dapogny/mmg/build/bin/mmg2d_O3"

# Path to FreeFem scripts


# Names of output and exchange files
EXCHFILE = RES + "exch.data"
LOGFILE  = RES + "log.data"
STEP     = RES + "step"
TMPSOL   = "./res/temp.sol"
