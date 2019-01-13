import sys
import os
import math
from ModelComponent import *

class BoltsComponent(ModelComponent):

	# Constructor
	def __init__(self, global_params, working_dir):
		ModelComponent.__init__(self, global_params, working_dir)
		
		# Setup LOD handlers
		self.lod_prepare_handlers = [self.PrepareModel_Lod1 ]
		self.lod_script_handlers = [self.AddToSimScript_Lod1]
		
		# Define name
		self.component_name = "bolts"
		
		# Dependencies
		self.lining = None
		self.soil = None
		

		
	def PrepareModel_Lod1(self, ostream):
		# Write model to .bch output file
		print 'bolts LOD = 1'
		
		if (self.lining.lod==1) or (self.soil.lod==1):
			return
		
		# ostream.write("Files Read "+self.modeller_path+"excavation_base_old_2_nonsym.gid\n")
		#ostream.write("mescape\n")		
		#ostream.write("Utilities Variables ImportTolerance 5 AutoImportTolerance 0\n")
		#ostream.write("mescape\n")
		
		ostream.write("mescape\n")
		ostream.write("Files SaveAs "+self.working_dir+self.global_params['model_name']+"_bolts_model.gid\n")

		sizeRatio = self.params['linig_outer_radius']/self.global_params['excavation_radius']
		#open batch file


		ostream.write("Files Read "+self.modeller_path+"bolts3.gid\n")
		ostream.write("mescape\n")
		ostream.write("Files SaveAs "+self.working_dir+self.params['name']+"_bolts_model.gid\n")
		ostream.write("mescape\n")
		#scale outer surface
		ostream.write("Utilities Move Lines Scale\n")
		ostream.write("0,0,0\n")
		ostream.write(str(self.global_params['round_length'])+","+str((self.params['linig_outer_radius']+self.params['lining_inner_radius'])/2)+","+str((self.params['linig_outer_radius']+self.params['lining_inner_radius'])/2)+"\n")
		ostream.write(" 1 2 3 4 5 6 7 8 9 10 11 12 13\n")
		ostream.write("mescape\n")
		#move bolts
		ostream.write("Utilities Move Lines Translation\n")
		ostream.write("0,0,0\n")
		ostream.write(str(self.global_params['round_length']/2)+",0,0\n")
		ostream.write(" 1 2 3 4 5 6\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Move Lines Translation\n")
		ostream.write("0,0,0\n")
		ostream.write(str(self.global_params['round_length'])+",0,0\n")
		ostream.write(" 7 8 9 10 11 12 13\n")
		ostream.write("mescape\n")
		#coppy first line
		ostream.write("Utilities Copy lines Translation\n")
		ostream.write("0,0,0\n")
		ostream.write(str(self.params['round_length'])+",0,0\n")
		ostream.write(" 1 2 3 4 5 6\n")
		ostream.write("mescape\n")        
		###################################################################################
		ostream.write("view layers ToUse\n")
		ostream.write("bolts_2_2\n escape escape\n")
		ostream.write("view layers entities\n")
		ostream.write("bolts_2_2\n")
		ostream.write("LowerEntities Lines\n")
		ostream.write("\n17\n")
		ostream.write("mescape\n")
		###################################################################################        
		ostream.write("view layers ToUse\n")
		ostream.write("bolts_2_3\n escape escape\n")
		ostream.write("view layers entities\n")
		ostream.write("bolts_2_3\n")
		ostream.write("LowerEntities Lines\n")
		#ostream.write("surfaces\n 21 24\n")
		ostream.write("\n18\n")
		ostream.write("mescape\n")
		###################################################################################    
		ostream.write("view layers ToUse\n")
		ostream.write("bolts_2_4\n escape escape\n")
		ostream.write("view layers entities\n")
		ostream.write("bolts_2_4\n")
		ostream.write("LowerEntities Lines\n")
		#ostream.write("surfaces\n 21 24\n")
		ostream.write("\n16\n")
		ostream.write("mescape\n")
		###################################################################################    
		ostream.write("view layers ToUse\n")
		ostream.write("bolts_2_5\n escape escape\n")
		ostream.write("view layers entities\n")
		ostream.write("bolts_2_5\n")
		ostream.write("LowerEntities Lines\n")
		#ostream.write("surfaces\n 21 24\n")
		ostream.write("\n19\n")
		ostream.write("mescape\n")
		###################################################################################    
		ostream.write("view layers ToUse\n")
		ostream.write("bolts_2_6\n escape escape\n")
		ostream.write("view layers entities\n")
		ostream.write("bolts_2_6\n")
		ostream.write("LowerEntities Lines\n")
		#ostream.write("surfaces\n 21 24\n")
		ostream.write("\n14 15\n")
		ostream.write("mescape\n")
		###################################################################################    

		for step in range(1,(self.params['number_of_steps']-1)):
			ostream.write("view layers new\n")
			ostream.write("bolts_"+str(step+2)+"_1"+"\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("bolts_"+str(step+2)+"_1"+"\n escape escape\n")
			xOffset = step*self.params['round_length']
			ostream.write("Utilities Copy lines Translation\n")
			ostream.write("0,0,0\n")
			ostream.write(str(xOffset)+",0,0\n")
			ostream.write(" 10 13\n")
			ostream.write("mescape\n")
		#------------------------------------------------------------------------
			ostream.write("view layers new\n")
			ostream.write("bolts_"+str(step+2)+"_2"+"\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("bolts_"+str(step+2)+"_2"+"\n escape escape\n")
			xOffset = step*self.params['round_length']
			ostream.write("Utilities Copy lines Translation\n")
			ostream.write("0,0,0\n")
			ostream.write(str(xOffset)+",0,0\n")
			ostream.write(" 17 9\n")
			ostream.write("mescape\n")
		#------------------------------------------------------------------------
			ostream.write("view layers new\n")
			ostream.write("bolts_"+str(step+2)+"_3"+"\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("bolts_"+str(step+2)+"_3"+"\n escape escape\n")
			xOffset = step*self.params['round_length']
			ostream.write("Utilities Copy lines Translation\n")
			ostream.write("0,0,0\n")
			ostream.write(str(xOffset)+",0,0\n")
			ostream.write(" 18 11\n")
			ostream.write("mescape\n")
		#------------------------------------------------------------------------
			ostream.write("view layers new\n")
			ostream.write("bolts_"+str(step+2)+"_4"+"\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("bolts_"+str(step+2)+"_4"+"\n escape escape\n")
			xOffset = step*self.params['round_length']
			ostream.write("Utilities Copy lines Translation\n")
			ostream.write("0,0,0\n")
			ostream.write(str(xOffset)+",0,0\n")
			ostream.write(" 16 8\n")
			ostream.write("mescape\n")
		#------------------------------------------------------------------------
			ostream.write("view layers new\n")
			ostream.write("bolts_"+str(step+2)+"_5"+"\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("bolts_"+str(step+2)+"_5"+"\n escape escape\n")
			xOffset = step*self.params['round_length']
			ostream.write("Utilities Copy lines Translation\n")
			ostream.write("0,0,0\n")
			ostream.write(str(xOffset)+",0,0\n")
			ostream.write(" 19 12\n")
			ostream.write("mescape\n")
		#------------------------------------------------------------------------
			ostream.write("view layers new\n")
			ostream.write("bolts_"+str(step+2)+"_6"+"\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("bolts_"+str(step+2)+"_6"+"\n escape escape\n")
			xOffset = step*self.params['round_length']
			ostream.write("Utilities Copy lines Translation\n")
			ostream.write("0,0,0\n")
			ostream.write(str(xOffset)+",0,0\n")
			ostream.write(" 7 14 15\n")
			ostream.write("mescape\n")
			#convert all lines to NURBS
		ostream.write("Geometry Edit ConvToNurbsL\n")
		ostream.write("InvertSelection\n escape\n Yes\n")
		ostream.write("mescape\n") 
		ostream.write("Files Save\n")
		ostream.write("Quit\n")
		ostream.close()		
		
		
		
		#########CREATE BACH FILE FOR MATERIAL PARAMETERS####		
		ifile = open(self.working_dir+'material_condition_bolts.bch','w')
		#print("elastic_grouting")
		
		if self.params['elastic_grouting']== 'True':

			ifile.write("mescape\n")
			ifile.write("Data Materials NewMaterial Isotropic3D Grouting Isotropic3D Isotropic3D 2500.0kg/m^3 20000N/mm^2 0.3\n")
			ifile.write("mescape\n")
		else:
		
			ifile.write("mescape\n")
			ifile.write("Data Materials NewMaterial GroutingMortar Grouting Isotropic3D GroutingMortar 2000.0kg/m^3 5000N/mm^2 0.3 8.0h 6.0h 0.6\n")
			#ifile.write("Data Materials NewMaterial GroutingMortar Grouting GroutingMortar GroutingMortar 2000.0kg/m^3 5000N/mm^2 0.3 8.0h 6.0h 0.6\n")
			ifile.write("mescape\n")

		for step in range(1, self.global_params['number_of_slices']+1):	

			ifile.write("Data Materials AssignMaterial Grouting Volumes\n")
			ifile.write("layer:grouting_"+str(step)+"\n")
			ifile.write("mescape\n")
			
		for step in range(1, self.global_params['number_of_slices']):
			ifile.write("Data Conditions AssignCond Distributed_Surface_Load\n")
			ifile.write("layer:grouting_surface_"+str(step)+"\n")
			ifile.write("mescape\n")
		############ ASSIGNING SURFACE GROUP MEMBERSHIP#######
			ifile.write("Data Conditions AssignCond Surface_Group_Membership\n")
			ifile.write("Change grouting_surface_"+str(step)+"\n")
			ifile.write("layer:grouting_surface_"+str(step)+"\n")
			ifile.write("mescape\n")
			
		ifile.write("mescape\n")
		
		###################ASIGN ELEMENT TYPE TO GROUTING########################
		for step in range(1, self.global_params['number_of_slices']+1):
			ifile.write("Data Conditions AssignCond VolumeElementType\n")			
			if( self.global_params['account_for_water'] == "True" ):
		##                ifile.write("Change Grouting_Element\n")
				ifile.write("Change UnsaturatedSoil_2Phase\n")
				ifile.write("1000.0kg/m^3\n")
				ifile.write("1.295kg/m^3\n")
				ifile.write("0.2\n")
				ifile.write("0.001m/s\n")
				ifile.write("0.00000001m/s\n")
				ifile.write("0.00000001m/s\n")
				ifile.write("0.0001m/s\n")
				ifile.write("0.0535\n")
			else:
				ifile.write("Change Kinematic_Linear\n")
				ifile.write("1000.0kg/m^3\n")
				ifile.write("1.295kg/m^3\n")
				ifile.write("0.2\n")
				ifile.write("0.001m/s\n")
				ifile.write("0.000001m/s\n")
				ifile.write("0.000001m/s\n")
				ifile.write("0.0001m/s\n")
				ifile.write("0.0535\n")
			ifile.write("layer:grouting_"+str(step)+"\n")
			ifile.write("mescape\n")
		ifile.close()			
			
		return
		
	def AddToSimScript_Lod1(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Grouting SimScript LOD = 1'
		if (self.lining.lod==1) or (self.soil.lod==2):
			return
		
		return
		
		
		return