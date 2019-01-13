### This is SATBIM modeller for scaled standard models

import sys
import os
import time
import subprocess
import math
import shutil
from HelperMethods import *
from LiningComponent import *
from SoilComponent import *
from BuildingComponent import *
from ExcavationComponent import *
from InsituComponent import *
from GroutingComponent import *
from TBMComponent import *
#from CompileSystem import *
print("inside")

class SatBimModeller:
	def __init__(self, args):
		try:
			self.modeller_path = str(args[1])
			self.problem_path = args[2]
			self.gid_path = args[3]

			self.job_id = args[4]
		except:
			print "Error: Invalid command line"
			sys.exit(0)
		
		# Read parameters for main model
		self.ReadParams()
		self.params['gid_path'] = self.gid_path
		
		# Working dir
		self.working_dir = self.problem_path + self.params['model_name'] + "/"
		print "Run: working dir is: " + self.working_dir
		try:
			if os.path.exists(self.working_dir) and os.path.isdir(self.working_dir):
				print "Run: path " + self.working_dir + " exists and is a directory"
			elif os.path.exists(self.working_dir) and os.path.isfile(self.working_dir):
				self.Error("Run: trying to overwrite existing file")
			else:
				try:
					os.mkdir(self.working_dir)
				except:
					self.Error("Run: failed creating directory")
		except:
			self.Error("Run: failed determining working directory")
		
		# Add all model components to list 
		#print(self.params['TBM_offset'])

		insitu = InsituComponent(self.params, self.working_dir)
		soil = SoilComponent(self.params, self.working_dir)
		lining = LiningComponent(self.params, self.working_dir)
		building = BuildingComponent(self.params, self.working_dir)
		grouting = GroutingComponent(self.params, self.working_dir)
		tbm = TBMComponent(self.params, self.working_dir)
		excavation = ExcavationComponent(self.params, self.working_dir)
		
		# Setup dependencies
		# Insitu
		insitu.soil = soil
		insitu.building = building
		insitu.lining = lining
		insitu.tbm = tbm
		# Soil
		soil.lining = lining
		soil.building = building
		soil.tbm = tbm

		# Lining
		lining.soil = soil
		lining.excavation = excavation
		lining.tbm = tbm
		# Building
		building.soil = soil
		# TBM
		tbm.soil = soil
		tbm.lining = lining

		
		# Excavation
		excavation.soil = soil
		excavation.building = building
		excavation.tbm = tbm
		excavation.lining = lining
		# Grouting
		grouting.soil = soil
		grouting.lining = lining
			
		self.model_components = [
			insitu,
#			building,
			lining,
			soil, 
			building, 
			grouting,
			tbm,
			excavation
		]
#		if lining.lod==3:
#		
#			self.model_components.append(bolts)
		
		
		#self.CompileSystem(self.params, self.working_dir)
	def ReadParams(self):
		inputPath = self.problem_path + "/input_files/main_model.dat"
		self.params = HelperMethods.ReadParamFile(inputPath)
		print("ReadParams: Model name: " + self.params['model_name'])
		print(self.params)


	def Error( self, error_msg ):
		sys.exit(error_msg)

	def InvokeGID(self, component_name):
		subprocess.check_output([self.gid_path+'gid_offscreen.bat', '-offscreen', '-b', component_name, self.params['model_name']], cwd=self.working_dir) # +self.working_dir )
	
	def Run( self ):
		# Main function
		
		# Read parameters for all model components
		print "Run: Reading params for all components ..."
		
		for component in self.model_components:
			# Read param file for component
			param_file = self.problem_path + "/input_files/" + component.component_name + ".dat"
			component.ReadParams(param_file)
			



		# Prepare models for all model components
		print "Run: Preparing model components ..."
		for component in self.model_components:
			# Prepare model
			output_path = self.working_dir + self.params['model_name'] + "_" + component.component_name + ".bch"
			
			# Open file
			bch_handle = open(output_path, 'w' )
			
			# Prepare component
			component.PrepareModel(bch_handle)
			
			# Close file
			bch_handle.close()
			
			# invoke GID

			self.InvokeGID(output_path)
		
#		sys.exit()
		
		self.coords = HelperMethods.ReadAlignmentFile(self.params['model_path']+'/input_files/')
			
		# Compile all model Components into simulation model			
		self.CompileSystem()
		print 'CompileSystem completed'
			
		self.CreateSimulationScript()
		
		for component in self.model_components:
			# Write simulation script model
			output_path = self.working_dir + self.params['model_name'] + "_simulation.py"
			
			# Open file
			bch_handle = open(output_path, 'a' )
			
			# Prepare component
			component.AddToSimScript(bch_handle)
			
			# Close file
			bch_handle.close()
			
		#self.CreateInsituIdentical()
		#coppy spoil_propertis utility and material file
		shutil.copy(self.problem_path+self.params['matfile']+".dat", self.working_dir)
		shutil.copy('soil_properties_utility.py', self.working_dir)
        print("modeller done ... ready for simulation")

		
		# Prepare simulation model	

 

	def CompileSystem( self ):
		#open batch file
		ifile = open( self.working_dir+self.params['model_name']+"_system.bch", 'w' )
		ifile.write("mescape\n")		
		ifile.write("Files SaveAs "+self.working_dir+self.params['model_name']+"_system.gid\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Variables ImportTolerance 5.0 AutoImportTolerance 0 \n")		
		
		ifile.write("mescape\n")
		ifile.write("Data Defaults ProblemType Yes ekate ")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		
		
		# import submodels
		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_ground_model.gid\n")
		ifile.write("mescape\n")

		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_grouting_model.gid\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Meshing CancelMesh PreserveFrozen Yes\n")
		ifile.write("mescape\n")		
		# ifile.write("mescape\n")			
		# ifile.write("Geometry Create IntMultSurfs\n")
		# ifile.write("InvertSelection\n escape\n escape\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Collapse Model Yes\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Repair Yes\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Collapse Model Yes\n")
		ifile.write("mescape\n")
		
		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_excavation_model.gid\n")
		ifile.write("mescape\n")
		

		ifile.write("mescape\n")		
		ifile.write("mescape\n")
		ifile.write("Meshing CancelMesh PreserveFrozen Yes\n")
		ifile.write("mescape\n")

		ifile.write("Utilities Collapse Model Yes\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")

		
		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_building_model.gid\n")
		ifile.write("mescape\n")
		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_bolts_model.gid\n")
		ifile.write("mescape\n")
		
		ifile.write("mescape\n")
		ifile.write("Meshing CancelMesh PreserveFrozen Yes\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Collapse Model Yes\n")
		ifile.write("mescape\n")

		ifile.write("Utilities Repair Yes\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Variables ImportTolerance 1.0 AutoImportTolerance 0 \n")		
		#ifile.write("Utilities Variables ImportTolerance "+str(self.params['round_length']/15)+" AutoImportTolerance 0\n")
		ifile.write("mescape\n")

		ifile.write("mescape\n")		
		
		#ifile.write("Utilities Variables ImportTolerance 10 AutoImportTolerance 0 \n")
		ifile.write("mescape\n")
		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_lining_model.gid\n")		
		ifile.write("mescape\n")
		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_tbm_model.gid\n")
		ifile.write("mescape\n")
		ifile.write("Meshing CancelMesh PreserveFrozen Yes\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Repair Yes\n")
		# ifile.write("mescape\n")
		# ifile.write("Utilities Collapse Model Yes\n")
		# ifile.write("mescape\n")
		# # Define problem type
		
		
		#scale complete_model_to meters		
		ifile.write("Utilities Move All Duplicate MaintainLayers Scale\n")
		ifile.write(str(self.coords[0][0])+" "+str(self.coords[0][1])+" "+str(self.coords[0][2])+"\n")
		ifile.write("0.01 0.01 0.01\n")
		ifile.write("InvertSelection\n")
		ifile.write("mescape\n")
		#move complete_model_to position 0,0,0
		ifile.write("Utilities Move All Duplicate MaintainLayers Translation\n")
		ifile.write(str(self.coords[0][0])+" "+str(self.coords[0][1])+" "+str(self.coords[0][2])+"\n")
		ifile.write("0.0 0.0 0.0\n")
		ifile.write("InvertSelection\n")
		ifile.write("mescape\n")
		
		#assign contact conditions to shield surface outside
		ifile.write("Data Conditions AssignCond Surface_Mortar Change "+str(1)+" Slave Option_automatic_axes\n")
		ifile.write("layer:shield_outter_surface\n")
		ifile.write("mescape\n")
		
		#assign contact conditions to excavation boundary
		for i in range (1, self.params['number_of_slices']+1):
			ifile.write("Data Conditions AssignCond Surface_Mortar Change "+str(1)+" Master Option_automatic_axes\n")
			ifile.write("layer:excavation_surface_"+str(i)+"\n")
			ifile.write("mescape\n")
		#### ATTENTION: I SWITCHED THIS BECAUSE IT GIVES BETTER RESULTS (10 MASTER-SLAVED SWITCHED) #I switched back
		#assign tying conditions to grouting surface outside
		ifile.write("Data Conditions AssignCond Surface_Mortar Change "+str(10)+" Master Option_automatic_axes\n")
		ifile.write("layer:grouting_surface_inside\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		#assign tying conditions to grouting surface outside#
		
		for step in range (1, self.params['number_of_slices']+1):
			ifile.write("Data Conditions AssignCond Surface_Mortar Change "+str(10)+" Slave Option_automatic_axes\n")
			ifile.write("layer:lining_outer_surface_"+str(step)+"\n")
			ifile.write("mescape\n")
		ifile.write("mescape\n")

		ifile.write("Files SaveAs "+self.working_dir+self.params['model_name']+"_system.gid\n")
		ifile.write("mescape\n")

		##########################################
		
		ifile.write("mescape\n")
		ifile.write("Files BatchFile\n")
		ifile.write( self.working_dir + "set_activation_grouting.bch"+"\n")
		ifile.write("mescape\n")		
		ifile.write("Files BatchFile\n")
		ifile.write( self.working_dir + "set_activation_lining.bch"+"\n")
		ifile.write("mescape\n")		
		ifile.write("Files BatchFile\n")
		ifile.write( self.working_dir + "set_activation_excavation.bch"+"\n")
		ifile.write("mescape\n")		
		ifile.write("Files Save\n")
		ifile.write("mescape\n")        
		
		#        assign materials and conditions
		for i in range(1, len(self.model_components)):
			
			ifile.write("mescape\n")
			ifile.write("Files BatchFile\n")
			ifile.write( self.working_dir + "material_condition_"+str(self.model_components[i].component_name)+".bch"+"\n")
			ifile.write("mescape\n")			
	
		ifile.write("mescape\n")
		ifile.write("Files Save\n")
		
		#repair geometry
		ifile.write("mescape\n")
		ifile.write("Utilities Repair Yes\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")

		#create mesh
		ifile.write("Utilities Variables Model(QuadraticType) 1\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
#		ifile.write("Meshing Generate\n")
#		ifile.write("DefaultSize\n")
		ifile.write("Meshing\n Generate\n"+str(int(self.params['excavation_radius']/100*1.7))+" escape\n escape\n")
		ifile.write("mescape\n")


		#asign calculation parameters####
		ifile.write("Data ProblemData -SingleField-\n")
		ifile.write("Stresses 1\n")
		ifile.write("mescape\n")
		ifile.write("Data ProblemData -SingleField-\n")
		ifile.write("Insitu_Stress 1\n")
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
		ifile.write("Data ProblemData -SingleField-\n")
		ifile.write("analysis_type\n")
		ifile.write("quasi-static\n")
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
		#subprocess.check_output([self.gid_path+'gid_offscreen.bat', '-offscreen', '-b', self.params['model_name'] + "_system.bch", self.params['model_name']], cwd=self.working_dir) # +self.working_dir )
		self.InvokeGID(self.params['model_name'] + "_system.bch")


	def CreateSimulationScript( self ):
		
		
		#print("generating simulation script...")
		#open script file
		tempfile=open('Simulation_template.py', 'r')
		ifile = open( self.working_dir+self.params['model_name']+"_simulation.py",'a' )
		ifile.seek(0)
		ifile.truncate()
		ifile.write("#simulation script for "+str(self.params['model_name'])+"\n")

		ifile.write(tempfile.read())
		
		ifile.write("params = {}\n")
	#        ifile.write("params['path'] = '"+str(self.working_dir)+"'\n")
		ifile.write("path = os.getcwd() + '/'\n")
		ifile.write("model_name = '"+str(self.params['model_name'])+"'\n")
		ifile.write("matfile = '"+str(self.params['matfile'])+".dat'\n")
		ifile.write("linear_elastic_material = "+str(self.params['linear_elastic_material'])+"\n")
		ifile.write("time_advance = "+str(self.params['time_advance'])+"\n")
		ifile.write("time_ring_construction = "+str(self.params['time_ring_construction'])+"\n")
		ifile.write("excavation_radius = "+str(float(self.params['excavation_radius'])/100.0)+"\n")
		ifile.write("account_for_water = "+str(self.params['account_for_water'])+"\n")
		ifile.write("ground_water_table = "+str(float(self.params['overburden'])/100.0)+"\n")
#		ifile.write("params['surface_pressure'] = "+str(self.params['surface_pressure'])+"\n")
		ifile.write("grouting_pressure = "+str(self.params['grouting_pressure'])+"\n")
		ifile.write("grouting_gradient = "+str(self.params['grouting_gradient'])+"\n")
		ifile.write("support_pressure = "+str(self.params['support_pressure'])+"\n")
		ifile.write("support_gradient = "+str(self.params['support_gradient'])+"\n")
#		ifile.write("params['number_of_loading_steps'] = "+str(self.params['number_of_loading_steps'])+"\n")
		ifile.write("number_of_slices = "+str(self.params['number_of_slices'])+"\n")
		ifile.write("number_of_excavation_steps = "+str(self.params['number_of_slices']-self.params['TBM_offset'])+"\n")
		ifile.write("initial_grouting_surface_index = "+str(self.params['grouting_offset'])+"\n")		
		ifile.write("round_length = "+str(float(self.params['round_length'])/100.0)+"\n")
		ifile.write("TBM_offset = "+str(self.params['TBM_offset'])+"\n")
		ifile.write("lining_offset = "+str(self.params['lining_offset'])+"\n")
		ifile.write("grouting_offset = "+str(self.params['grouting_offset'])+"\n")
#		ifile.write("params['machine_weight_pressure'] = "+str(self.params['machine_weight_pressure'])+"\n")
#		ifile.write("params['trailer_pressure'] = "+str(self.params['trailer_pressure'])+"\n")
#		ifile.write("params['initial_trailer_load_index'] = "+str(self.initial_trailer_load_index)+"\n")
#		ifile.write("params['number_of_loading_steps'] = "+str(self.params['number_of_loading_steps'])+"\n")
#		ifile.write("params['number_of_loading_steps_insitu'] = "+str(self.params['number_of_loading_steps_insitu'])+"\n")
		ifile.write("move_steps_per_round_length = "+str(self.params['move_steps_per_round_length'])+"\n")
		ifile.write("steps_per_down_time = "+str(self.params['steps_per_down_time'])+"\n")
		if self.params['segment_type']==61:
			ifile.write("segment_number = 7\n")
		elif self.params['segment_type']==71:
			ifile.write("segment_number = 8\n")
		else:
			ifile.write("segment_number = 1\n")			
#		ifile.write("params['OCR'] = "+str(self.params['OCR'])+"\n")
		ifile.write("write_to_database = "+str(self.params['write_to_databese'])+"\n")
#		ifile.write("params['write_pod_information'] = "+str(self.params['write_pod_information'])+"\n")
#		ifile.write("params['job_id'] = "+str(self.job_id)+"\n")
		ifile.write("\n")
		ifile.write("\n")
#		ifile.write("simulator = EkateSimulator(params)\n")
#		ifile.write("simulator.Run()\n")
		ifile.close()
		
#	def CreateInsituIdentical( self ):
#		print("Prepare Identical Inisty for Model - longer computation but reduced eror")
#		#open batch file
#		ifile = open( self.working_dir+self.params['model_name']+"_insitu_1.bch", 'w' )
#		ifile.write("mescape\n")		
#		ifile.write("Files SaveAs "+self.working_dir+self.params['model_name']+"_insitu_1_model.gid\n")
#		ifile.write("mescape\n")
#		ifile.write("mescape\n")
#		ifile.write("Utilities Variables ImportTolerance 5.0 AutoImportTolerance 0 \n")		
#		
#		ifile.write("mescape\n")
#		ifile.write("Data Defaults ProblemType Yes ekate ")
#		ifile.write("mescape\n")
#		ifile.write("mescape\n")
#		
#		
		# import submodels
#		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_ground_model.gid\n")
#		ifile.write("mescape\n")
#		ifile.write("Files InsertGeom "+self.working_dir+self.params['model_name']+"_excavation_model.gid\n")
##		ifile.write("mescape\n")
	#	
		
#		ifile.write("mescape\n")
#		ifile.write("Meshing CancelMesh PreserveFrozen Yes\n")
#		ifile.write("mescape\n")
#		ifile.write("Utilities Collapse Model Yes\n")
#		ifile.write("mescape\n")			
#
#		#assign lines to outer surface	
#		ifile.write("view layers ToUse\n")
#		ifile.write("ground \n escape escape\n")
#		ifile.write("view layers entities\n")
#		ifile.write("ground \n")
#		ifile.write("LowerEntities Volumes\n")
#		ifile.write("InvertSelection\n escape\n escape\n")
##		
	
#		ifile.write("mescape\n")
#		ifile.write("Utilities Collapse Model Yes\n")
#		ifile.write("mescape\n")
#
#		ifile.write("mescape\n")
#		ifile.write("Files BatchFile\n")
#		ifile.write( self.working_dir + "material_condition_insitu.bch"+"\n")
#		ifile.write("mescape\n")
		
#		#write calculation file
#		ifile.write("Files WriteCalcFile "+str(self.working_dir+self.params['model_name'])+"_insitu_1_model.gid/"+str(self.params['model_name'])+"_insitu_1_model.dat\n")
#		ifile.write("mescape\n")
#		ifile.write("mescape\n")
#		ifile.write("Files Save\n")
#		ifile.write("mescape\n")
#		ifile.write("Quit\n")
#		ifile.close()		
#		
#		self.InvokeGID(self.params['model_name'] + "_insitu_1.bch")

modeller = SatBimModeller( sys.argv )
modeller.Run()
