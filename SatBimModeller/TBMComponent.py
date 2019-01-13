import sys
import os
import math
from ModelComponent import *

class TBMComponent(ModelComponent):

	# Constructor
	def __init__(self, global_params, working_dir):
		ModelComponent.__init__(self, global_params, working_dir)
		
		# Setup LOD handlers
		self.lod_prepare_handlers = [self.PrepareModel_Lod1, self.PrepareModel_Lod2, self.PrepareModel_Lod3]
		self.lod_script_handlers = [self.AddToSimScript_Lod1, self.AddToSimScript_Lod2, self.AddToSimScript_Lod3]
		
		# Define name
		self.component_name = "tbm"
		
		# Dependencies
		self.soil = None
		self.lining = None
		
	
	def ReadParams(self, pathToParamFile):	
		ModelComponent.ReadParams(self, pathToParamFile)
		
		if self.lod <= 2:
			self.is_collapsable = True
		else:
			self.is_collapsable = False
	
	def PrepareModel_Lod1(self, ostream):
		# Write model to .bch output file
		print 'TBM LOD = 1'
		
		return
	
	def PrepareModel_Lod2(self, ostream):
		# Write model to .bch output file
		print 'TBM LOD = 2'
		if self.soil.lod ==1 or self.lining.lod ==1:
			return
		ostream.write("mescape\n")
		ostream.write("Files SaveAs " + self.working_dir + self.global_params['model_name'] + "_tbm_model.gid\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Variables ImportTolerance 10 AutoImportTolerance 0 \n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("view layers new\n")
		ostream.write("shield"+"\n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("shield"+"\n escape escape\n")		
		
		ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/tbm/TBM_0.sat"+"\n ")
		ostream.write("mescape\n")

		
		#convert all lines to NURBS
		ostream.write("Geometry Edit ConvToNurbsL\n")
		ostream.write("InvertSelection\n escape\n Yes\n")
		ostream.write("mescape\n")

		
		#set delite volumes
		ostream.write("Geometry Delete Volume\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")
		#set delete outer surfaces
		ostream.write("Geometry Delete Surface\n")
		ostream.write("3 5 \n")
		ostream.write("mescape\n")
		#set create lines
		ostream.write("Geometry Create Line Join\n")	
		ostream.write("1 8 \n escape\n")	
		ostream.write("2 5 \n escape\n")		
		ostream.write("3 6 \n escape\n")		
		ostream.write("4 7 \n escape\n")	

		ostream.write("mescape\n")
		ostream.write("Geometry Create NurbsSurface Automatic 4\n")		
		ostream.write("mescape\n")

		ostream.write("view layers ToUse\n")
		ostream.write("shield"+"\n escape escape\n")			
		
		ostream.write("mescape\n")
		ostream.write("Geometry Create Volume AutomaticStruct\n")	
		ostream.write("mescape\n")
		ostream.write("mescape\n")	
	

		ostream.write("mescape\n")
		ostream.write("view layers new\n")
		ostream.write("shield_outter_surface"+"\n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("shield_outter_surface\n escape escape\n")
		ostream.write("Layers Entities\n")
		ostream.write("shield_outter_surface\n")
		ostream.write("LowerEntities Surfaces\n")
		ostream.write("1 6")
		ostream.write("mescape\n") 		
		
		ostream.write("mescape\n")		
		#ostream.write("Meshing ElemType Hexahedra\n")
		ostream.write("Meshing ElemType Tetrahedra\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")
		
		#set meshing information
		ostream.write("Meshing Structured Volumes\n")
		ostream.write("InvertSelection\n escape\n 1\n")
		ostream.write("InvertSelection\n escape\n escape\n")
			
		ostream.write("mescape\n")
		ostream.write("Meshing Structured Lines 8\n")
		ostream.write("InvertSelection\n escape\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		
		ostream.write("mescape\n")
		ostream.write("Meshing Structured Lines 1\n")
		ostream.write("13 14 15 16\n")
		ostream.write("mescape\n")

		
		
				
		ostream.write("mescape\n")
		ostream.write("Utilities Variables Model(QuadraticType) 1\n")
		ostream.write("mescape\n")
		ostream.write("Meshing Generate\n")
		ostream.write("DefaultSize\n")
		ostream.write("mescape\n")
			
		ostream.write("Files Save\n")
		ostream.write("Quit\n")
		
		
		#########CREATE BACH FILE FOR MATERIAL PARAMETERS AND CONDITIONS####		
		ifile = open(self.working_dir+'material_condition_tbm.bch','w')
		ifile.write("mescape\n")
		ifile.write("Data Materials NewMaterial Isotropic3D TBM_Steel Isotropic3D Isotropic3D 7620.0kg/m^3 210000000000N/mm^2 0.3\n")
		ifile.write("mescape\n")

		ifile.write("Data Materials AssignMaterial TBM_Steel Volumes\n")
		ifile.write("layer:shield \n")
		ifile.write("mescape\n")
		#TOTAL LAGRANGIEN VOLUME ELEMENT
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond VolumeElementType\n")
		ifile.write("Change TotalLagrangian\n")
		ifile.write("1000.0kg/m^3\n")
		ifile.write("1.295kg/m^3\n")
		ifile.write("0.2\n")
		ifile.write("0.001m/s\n")
		ifile.write("0.00000032m/s\n")
		ifile.write("0.00000044m/s\n")
		ifile.write("0.0001m/s\n")
		ifile.write("0.0535\n")
		ifile.write("layer:shield\n")
		ifile.write("mescape\n")
		
		ifile.write("Data Conditions AssignCond Surface_Group_Membership\n")
		ifile.write("Change shield\n")
		ifile.write("layer:shield\n")
		ifile.write("mescape\n")
		
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		ifile.write("Change 1 0 1 0 1 0 0 0 0 0 0 0\n")
		ifile.write("layer:shield\n")
		ifile.write("mescape\n")
		ifile.close()	
		
		return
		
	def PrepareModel_Lod3(self, ostream):
		# Write model to .bch output file
		print 'TBM LOD = 3'
		ostream.write("mescape\n")
		ostream.write("Files SaveAs " + self.working_dir + self.global_params['model_name'] + "_tbm_model.gid\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		#stream.write("mescape\n")
		#ostream.write("Utilities Variables ImportTolerance 10 AutoImportTolerance 0 \n")
		#ostream.write("mescape\n")		
		ostream.write("mescape\n")
		ostream.write("view layers new\n")
		ostream.write("jacks"+"\n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("jacks"+"\n escape escape\n")

		ostream.write("mescape\n")
		ostream.write("Utilities Variables ImportTolerance "+str(self.params['jack_radius']*5)+" AutoImportTolerance 0\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		lines_select=[4]
		for i in range(1,13):
			lines_select.append(4+6*i)
			
		for i in range (5,25):
			ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/tbm/TBM_"+str(i)+".sat"+"\n ")
			ostream.write("mescape\n")
		#set delite surfaces
		ostream.write("Geometry Delete Volumes\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")
		ostream.write("Geometry Delete Surface\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")
		ostream.write("Geometry Delete Lines\n")
		for i in range(1,73):
			if i not in lines_select:
				ostream.write(str(i)+" ")
		ostream.write("\n")						
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Geometry Delete Points\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")

		ostream.write("mescape\n")
		ostream.write("Utilities Variables ImportTolerance 1 AutoImportTolerance 0\n")
		ostream.write("mescape\n")
		ostream.write("view layers new\n")
		ostream.write("shield"+"\n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("shield"+"\n escape escape\n")		
		for i in range (0,5):
			ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/tbm/TBM_"+str(i)+".sat"+"\n ")
			ostream.write("mescape\n")
		
		ostream.write("mescape\n")

	
		#convert all lines to NURBS
		ostream.write("Geometry Edit ConvToNurbsL\n")
		ostream.write("InvertSelection\n escape\n Yes\n")
		ostream.write("mescape\n")
		ostream.write("view layers new\n")
		ostream.write("shield_outter_surface"+"\n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("shield_outter_surface\n escape escape\n")
		ostream.write("Layers Entities\n")
		ostream.write("shield_outter_surface\n")
		ostream.write("LowerEntities Surfaces\n")
		ostream.write("1 6 7 11 20 21 22")
		ostream.write("mescape\n") 
			
		ostream.write("mescape\n")
		ostream.write("Meshing Structured Lines 4\n")
		ostream.write("InvertSelection\n escape\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		
		ostream.write("mescape\n")
		ostream.write("Meshing Structured Lines 1\n")
		ostream.write(" 2 3 4 5 11 12 13 14 23 24 26 27\n")
		ostream.write("mescape\n")
		
		
		ostream.write("mescape\n")
###FIX MESH - STILL WRONG				
		ostream.write("mescape\n")
		ostream.write("Utilities Variables Model(QuadraticType) 1\n")
		ostream.write("mescape\n")
		ostream.write("Meshing Generate\n")
		ostream.write("DefaultSize\n")
		ostream.write("mescape\n")
			
		ostream.write("Files Save\n")
		ostream.write("Quit\n")		
		
		#####FIX THIS FOR LOD !!!!!!!!!!!!!!!!####################
		#########CREATE BACH FILE FOR MATERIAL PARAMETERS AND CONDITIONS####		
		ifile = open(self.working_dir+'material_condition_tbm.bch','w')
		ifile.write("mescape\n")
		ifile.write("Data Materials NewMaterial Isotropic3D TBM_Steel Isotropic3D Isotropic3D 7620.0kg/m^3 210000N/mm^2 0.3\n")
		ifile.write("mescape\n")

		ifile.write("Data Materials AssignMaterial TBM_Steel Volumes\n")
		ifile.write("layer:shield \n")
		ifile.write("mescape\n")
		#TOTAL LAGRANGIEN VOLUME ELEMENT
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond VolumeElementType\n")
		ifile.write("Change TotalLagrangian\n")
		ifile.write("1000.0kg/m^3\n")
		ifile.write("1.295kg/m^3\n")
		ifile.write("0.2\n")
		ifile.write("0.001m/s\n")
		ifile.write("0.00000032m/s\n")
		ifile.write("0.00000044m/s\n")
		ifile.write("0.0001m/s\n")
		ifile.write("0.0535\n")
		ifile.write("layer:shield\n")
		ifile.write("mescape\n")
		ifile.close()	
		
		
		return
		
	def AddToSimScript_Lod1(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'TBM SimScript LOD = 1'
		ostream.write("advance = 0.0\n")
		ostream.write("tbm_lenght="+str(self.params['tbm_lenght']/100.0)+"\n")
		ostream.write("tbm_conicity= "+str(self.params['tbm_conicity'])+"\n")
		ostream.write("tbm_r= "+str(self.params['tbm_r']/100.0)+"\n")
		ostream.write("tbm_rings=int(tbm_lenght/round_length)\n")
		
		return
		
	def AddToSimScript_Lod2(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'TBM SimScript LOD = 2'
		
		ostream.write("advance = 0.0\n")
		if self.lining.lod>1:
			ostream.write("#print '######## DO THE FIRST STEP WITH FIXED MACHINE  #############'\n")
			ostream.write("for node in model1.node_groups['shield']:\n")
			ostream.write("	if node in model1.model_part.Nodes:\n")
			ostream.write("		model1.model_part.Nodes[node].Fix(DISPLACEMENT_Z)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_Z, 0.0)\n")
		
		return
		
	def AddToSimScript_Lod3(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'TBM SimScript LOD = 3'

		ostream.write("print '######## JACKS SETUP #############'\n")
		ostream.write("#setting up steering utility\n")
		ostream.write("steering_utility = SteeringUtility()\n")
		ostream.write("with_diagonals= False\n")
		ostream.write("jacks = __import__( self.name+'_jacks' )\n")
		ostream.write("jacks_obj = jacks.HydraulicJacksPositions()\n")
		ostream.write("jack_locations= jacks_obj.coords\n")

		ostream.write("##### SOLVE MODEL #####\n")
		ostream.write("face_index = initial_face_index\n")

		ostream.write("steering_utility.InitializeSteeringUtility(model1.model_part, jack_locations, len(jack_locations),with_diagonals)\n")
		ostream.write("print('steering_utility.InitializeSteeringUtility(...)')\n")
		ostream.write("steering_utility.ResetHydraulicJacks(model1.model_part,with_diagonals)\n")
		ostream.write("steering_utility.SetHydraulicJacks(model1.model_part,with_diagonals)\n")
		ostream.write("print('steering_utility.SetHydraulicJacks(...)')\n")

		ostream.write("model1.deac.Reactivate( model1.model_part, 0, 0 )\n")
		ostream.write("model1.deac.Deactivate( model1.model_part, 0, 0 )\n")

		ostream.write("advance = 0.0\n")
		if self.lining.lod>1:
			ostream.write("#print '######## DO THE FIRST STEP WITH FIXED MACHINE  #############'\n")
			ostream.write("for node in model1.node_groups['shield_fixed_displacement']:\n")
			ostream.write("	if node in model1.model_part.Nodes:\n")
			ostream.write("		model1.model_part.Nodes[node].Fix(DISPLACEMENT_Z)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_Z, 0.0)\n")
		
		return