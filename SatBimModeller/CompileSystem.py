import sys
import os
import math
from ModelComponent import *

class CompileSystem(ModelComponent):

	# Constructor
	def __init__(self, global_params, working_dir):
		self.global_params = global_params
		#ModelComponent.__init__(self, global_params, working_dir)
		#print("initialized")
		
		# Define name
		self.component_name = "main_model"
		
		
	def CompileSystem( self ):
		#open batch file
		ifile = open( self.working_dir+self.params['model_name']+"_system.bch", 'w' )
		
		
		ifile.write("Files Read "+self.working_dir+self.params['model_name']+"_system.gid\n")
		ifile.write("mescape\n")
		
		# import submodels
		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_ground_model.gid\n")
		ifile.write("mescape\n")
		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_excavation_model.gid\n")
		ifile.write("mescape\n")
		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_building_model.gid\n")
		ifile.write("mescape\n")
		ifile.write("Meshing CancelMesh PreserveFrozen Yes\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Repair Yes\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Collapse Model Yes\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		
		
		ifile.write("Utilities Variables ImportTolerance 50 AutoImportTolerance 0\n")
		ifile.write("mescape\n")
		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_lining_model.gid\n")
		ifile.write("mescape\n")
		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_grouting_model.gid\n")
		ifile.write("mescape\n")
		ifile.write("Meshing CancelMesh PreserveFrozen Yes\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Repair Yes\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Collapse Model Yes\n")
		ifile.write("mescape\n")
		# # Define problem type
		ifile.write("mescape\n")
		ifile.write("Data Defaults ProblemType Yes ekate ")
		ifile.write("mescape\n")
		ifile.write("mescape\n")


		ifile.write("Files SaveAs "+self.working_dir+self.params['model_name']+"_system.gid\n")
		ifile.write("mescape\n")




		#assign boundary conditions
		ifile.write("*****TCL GetBoundary \n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond IsTop\n")
		ifile.write("UnAssign InvertSelection\n")
		ifile.write("mescape\n")


		ifile.write("Data Conditions AssignCond Surface_Group_Membership\n")
		ifile.write("Change shield_fixed_displacement\n")
		ifile.write("layer:shield_wall_back\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Group_Membership\n")
		ifile.write("Change surface\n")
		ifile.write("layer:surface\n")
		ifile.write("mescape\n")
		##########################################
		
		#CHANGE THIS TO BE WRITTEN IN ALINIG AND GROUTING!!!!!!
		#assign activation levels
		number_of_steps=self.global_params['TBM_offset']+self.global_params['grouting_offset']
		reactivation_index_stressfree = (-2*number_of_steps)*6-10
		self.initial_reactivation_index_stressfree = reactivation_index_stressfree
		reactivation_index = (-2*number_of_steps)*6-9
		self.initial_reactivation_index = reactivation_index
		self.initial_face_index = self.global_params['TBM_offset']
		self.initial_trailer_load_index = self.global_params['lining_offset']-2
		self.initial_grouting_surface_index = self.global_params['grouting_offset']
		###########################################
		deactivation_index = 1
		reactivation_index = (-2*self.global_params['number_of_slices'])*2-6
		reactivation_index_stressfree=(-2*self.global_params['number_of_slices'])*2-2

		for step in range(self.global_params['TBM_offset'], self.global_params['number_of_slices']+1):

	#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
			ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
			ifile.write("Change "+str(deactivation_index)+"\n")
			ifile.write("layer:excavation_"+str(step+self.global_params['TBM_offset'])+"\n")
			ifile.write("mescape\n")
			deactivation_index = deactivation_index + 1

	#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		for step in range(self.params['TBM_offset'], self.params['number_of_slices']+1):
			ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
			ifile.write("Change "+str(reactivation_index)+"\n")
			ifile.write("layer:lining_"+str(step+self.params['TBM_offset'])+"\n")
			ifile.write("mescape\n")
			reactivation_index = reactivation_index - 2
		for step in range(self.params['TBM_offset'], self.params['number_of_slices']+1):
			ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
			ifile.write("Change "+str(reactivation_index_stressfree)+"\n")
			ifile.write("layer:grouting_"+str(step+self.params['TBM_offset'])+"\n")
			ifile.write("mescape\n")
			reactivation_index_stressfree = reactivation_index_stressfree - 2




		#assign element types
		ifile.write("Data Conditions AssignCond VolumeElementType\n")
		if( self.params['account_for_water'] == "True" ):
			ifile.write("Change UnsaturatedSoil_2Phase\n")
			ifile.write("1000.0kg/m^3\n")
			ifile.write("1.295kg/m^3\n")
			ifile.write("0.2\n")
			ifile.write("0.001m/s\n")
			ifile.write("0.00000032m/s\n")
			ifile.write("0.00000044m/s\n")
			ifile.write("0.0001m/s\n")
			ifile.write("0.0535\n")
		else:
			ifile.write("Change Kinematic_Linear\n")
			ifile.write("1000.0kg/m^3\n")
			ifile.write("1.295kg/m^3\n")
			ifile.write("0.2\n")
			ifile.write("0.001m/s\n")
			ifile.write("0.00000032m/s\n")
			ifile.write("0.00000044m/s\n")
			ifile.write("0.0001m/s\n")
			ifile.write("0.0535\n")
		ifile.write("layer:ground\n")
		ifile.write("mescape\n")

		for step in range(1, (self.params['number_of_slices']- self.params['TBM_offset'])+1):
			ifile.write("Data Conditions AssignCond VolumeElementType\n")
			if( self.params['account_for_water'] == "True" ):
				ifile.write("Change UnsaturatedSoil_2Phase\n")
				ifile.write("1000.0kg/m^3\n")
				ifile.write("1.295kg/m^3\n")
				ifile.write("0.2\n")
				ifile.write("0.001m/s\n")
				ifile.write("0.00000032m/s\n")
				ifile.write("0.00000044m/s\n")
				ifile.write("0.0001m/s\n")
				ifile.write("0.0535\n")
			else:
				ifile.write("Change Kinematic_Linear\n")
				ifile.write("1000.0kg/m^3\n")
				ifile.write("1.295kg/m^3\n")
				ifile.write("0.2\n")
				ifile.write("0.001m/s\n")
				ifile.write("0.00000032m/s\n")
				ifile.write("0.00000044m/s\n")
				ifile.write("0.0001m/s\n")
				ifile.write("0.0535\n")
			ifile.write("layer:excavation_"+str(step)+"\n")
			ifile.write("mescape\n")

		ifile.write("Files Save\n")
		ifile.write("mescape\n")        
		
	#        create materials for system
	#        Remarks: the material properties of TBM_Steel, Lining, Grouting is fixed (TBD: change through input mat file)
		ifile.write("Data Materials NewMaterial UserDefined Excavation UserDefined\n")
		ifile.write("mescape\n")
		ifile.write("Data Materials NewMaterial UserDefined Soil UserDefined\n")
		ifile.write("mescape\n")

		

		for step in range(1, (self.params['number_of_slices']- self.params['TBM_offset'])+1):

			ifile.write("mescape\n")
			ifile.write("Data Materials AssignMaterial Excavation Volumes\n")
			ifile.write("layer:excavation_"+str(step)+"\n")
			ifile.write("mescape\n")
		ifile.write("Data Materials AssignMaterial Soil Volumes\n")
		ifile.write("layer:ground\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Files Save\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond IsTop\n")
		ifile.write("UnAssign InvertSelection\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		ifile.write("Change 0 0 0 0 0 0 0 0 0 0 0 0\n")
		ifile.write("layer:Top\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		ifile.write("Change 0 0 0 0 1 0 0 0 0 0 0 0\n")
		ifile.write("layer:Bottom\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		ifile.write("Change 0 0 1 0 0 0 0 0 0 0 0 0\n")
		ifile.write("layer:Side_y \n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		ifile.write("Change 1 0 0 0 0 0 0 0 0 0 0 0\n")
		ifile.write("layer:Side_x\n")
		ifile.write("mescape\n")		
		ifile.write("Data Conditions AssignCond IsTop\n")
		ifile.write("layer:Top\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Water_Pressure\n")
		ifile.write("UnAssign layer:Top\n")
		ifile.write("mescape\n")        
		ifile.write("mescape\n")
		ifile.write("Files Save\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Files Save\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Group_Membership\n")
		ifile.write("Change Top\n")
		ifile.write("layer:Top\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Distributed_Surface_Load\n")
		ifile.write("layer:Top\n")
		ifile.write("mescape\n")
		#create material building
		ifile.write("mescape\n")
		ifile.write("Data Materials NewMaterial Isotropic3D Building Isotropic3D "+str(self.params['ro_build'])+"kg/m^3 "+ str(self.params['E_build'])+"/mm^2 "+str(self.params['nu_build'])+"\n")
		ifile.write("mescape\n")
		ifile.write("Data Materials AssignMaterial Building Volumes\n")
		ifile.write("layer:building\n")
		ifile.write("mescape\n")
		ifile.write("Data Materials AssignMaterial Building Volumes\n")
		ifile.write("layer:foundation\n")
		ifile.write("mescape\n")
		#create material lining
		ifile.write("mescape\n")
		ifile.write("Data Materials NewMaterial Isotropic3D Lining Isotropic3D "+str(self.params['ro_build'])+"kg/m^3 "+ str(self.params['E_build'])+"/mm^2 "+str(self.params['nu_build'])+"\n")
		ifile.write("mescape\n")
		for i in range (1, self.params['number_of_slices']+1):
		
			ifile.write("Data Materials AssignMaterial Lining Volumes\n")
			ifile.write("layer:lining_"+str(i)+"\n")
			ifile.write("mescape\n")
		ifile.write("Data Materials NewMaterial Isotropic3D Grouting Isotropic3D "+str(self.params['ro_build'])+"kg/m^3 "+ str(self.params['E_build'])+"/mm^2 "+str(self.params['nu_build'])+"\n")
		ifile.write("mescape\n")
		for i in range (1, self.params['number_of_slices']+1):
		
			ifile.write("Data Materials AssignMaterial Grouting Volumes\n")
			ifile.write("layer:grouting_"+str(i)+"\n")
			ifile.write("mescape\n")
			
		#repair geometry
		ifile.write("mescape\n")
		ifile.write("Utilities Repair Yes\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")

		#create mesh
		ifile.write("Meshing Quadratic Quadratic9\n")
		#ifile.write("Utilities Variables Model(QuadraticType) 1\n")
		ifile.write("mescape\n")
		ifile.write("Meshing Generate\n")
		ifile.write("DefaultSize\n")
		ifile.write("mescape\n")


	
		if( self.params['account_for_water'] == "True" ):
			ifile.write("Data ProblemData -SingleField-\n")
			ifile.write("Perform_MultiFlow_Analysis 1\n")
			ifile.write("mescape\n")
			ifile.write("Data ProblemData -SingleField-\n")
			ifile.write("Water_Pressure 1\n")
			ifile.write("mescape\n")
			ifile.write("Data ProblemData -SingleField-\n")
			ifile.write("Saturation 1\n")
			ifile.write("mescape\n")
		if( self.params['linear_elastic_material'] == "False" ):
			ifile.write("Data ProblemData -SingleField-\n")
			ifile.write("Plastic_strains 1\n")
			ifile.write("mescape\n")
		#Problemtype
		ifile.write("Files Save\n")
		ifile.write("mescape\n")
		ifile.write("Data ProblemData -SingleField-\n")
		ifile.write("Enable_Gravity 1 \n")
		ifile.write("mescape\n")
		ifile.write("Data ProblemData -SingleField-\n")
		ifile.write("Solver\n")
		ifile.write("Pardiso\n")
		ifile.write("mescape\n")

		
		#write calculation file
		ifile.write("mescape\n")
		ifile.write("Utilities Calculate \n")	
		ifile.write("mescape\n")
		ifile.write("Files WriteCalcFile\n")	
		ifile.write("mescape\n")
		ifile.write("mescape\n")	
		#ifile.write("Files WriteCalcFile "+str(self.working_dir+self.params['model_name'])+"_system.gid/"+str(self.params['model_name'])+"_system.dat\n")
		ifile.write("mescape\n")
		ifile.write("Files Save\n")
		ifile.write("mescape\n")
		ifile.write("Quit\n")
		ifile.close()
		subprocess.check_output([self.gid_path+'gid_offscreen.bat', '-offscreen', '-b', self.params['model_name'] + "_system.bch", self.params['model_name']], cwd=self.working_dir) # +self.working_dir )