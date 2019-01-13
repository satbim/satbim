###SATBIM - 
##################################################################
## This is a Simulation sctipt for SATBIM tunnel submodel    #####
###For calulation KRATOS FE framework                        #####
##################################################################
###							                                 #####
## ATTENTION: before running simulation script  	         #####
## make sure that yopur geometry and FE mesh is regular      #####
##################################################################
import sys
import os
import math
kratos_root_path = os.environ['KRATOS_ROOT_PATH']


#importing Kratos main library
from KratosMultiphysics import *
from KratosMultiphysics.StructuralApplication import *
from KratosMultiphysics.EkateAuxiliaryApplication import *
from KratosMultiphysics.ExternalSolversApplication import *
from KratosMultiphysics.MKLSolversApplication import *
from KratosMultiphysics.MortarApplication import *

kernel = Kernel()   #defining kernel