##################################################################
##### ekate - Enhanced KRATOS for Advanced Tunnel Enineering #####
##### copyright by CIMNE, Barcelona, Spain                   #####
#####          and Janosch Stascheit for TUNCONSTRUCT        #####
##### all rights reserved                                    #####
##################################################################
#setting the domain size for the problem to be solved
domain_size = 3
##################################################################
##################################################################
## ATTENTION: here the order is important                    #####
##################################################################
## including kratos path                                     #####
## ATTENTION: the following lines have to be adapted to      #####
##            match your acrtual configuration               #####
##################################################################
import sys
import os
kratos_root_path=os.environ['KRATOS_ROOT_PATH']
##setting up paths
kratos_libs_path = kratos_root_path+'libs' ##kratos_root/libs
kratos_applications_path = kratos_root_path+'applications' ##kratos_root/applications
##################################################################
##################################################################
sys.path.append(kratos_libs_path)
sys.path.append(kratos_applications_path)

##################################################################
##################################################################
sys.path.append('./rEpLaCeMeNtStRiNg.gid')
import rEpLaCeMeNtStRiNg_include
from rEpLaCeMeNtStRiNg_include import **
# calculate insitu-stress for geology_virgin.gid
model = rEpLaCeMeNtStRiNg_include.Model('rEpLaCeMeNtStRiNg',os.getcwd()+"/")
model.InitializeModel()

##################################################################
###  SIMULATION  #################################################
##################################################################
*if(strcmp(GenData(Simulation_Script),"standard")==0)
time = 0.0
delta_time = *GenData(time_step_length)

for step in range( 0, *GenData(time_steps) ):
    time = time + delta_time
    model.Solve( time, 0, 0, 0, 0 )
    model.WriteOutput( time )
    print("###################")
    print("step "+str(time)+" done.")
    print("###################")
print "Calculation done"
sys.exit(0)
*else
*# user-defined script is used (will be appended automatically)
# =====================
# | USER SCRIPT FOR CALCULATION OF AUSBLAS.GID |
# vvvvvvvvvvvvvvvvvvvvv
*endif
