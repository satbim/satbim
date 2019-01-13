import sys
import os
import math
from ModelComponent import *

class GroutingComponent(ModelComponent):

	# Constructor
	def __init__(self, global_params, working_dir):
		ModelComponent.__init__(self, global_params, working_dir)
		
		# Setup LOD handlers
		self.lod_prepare_handlers = [self.PrepareModel_Lod1 ]
		self.lod_script_handlers = [self.AddToSimScript_Lod1]
		
		# Define name
		self.component_name = "grouting"
		
		# Dependencies
		self.lining = None
		self.soil = None
		

		
	def PrepareModel_Lod1(self, ostream):
		# Write model to .bch output file
		print 'Grouting LOD = 1'
		
		if (self.lining.lod==1) or (self.soil.lod==1):
			return
		
		# ostream.write("Files Read "+self.modeller_path+"excavation_base_old_2_nonsym.gid\n")
		ostream.write("mescape\n")		
		ostream.write("Utilities Variables ImportTolerance 5 AutoImportTolerance 0\n")
		ostream.write("mescape\n")
		
		ostream.write("mescape\n")
		ostream.write("Files SaveAs "+self.working_dir+self.global_params['model_name']+"_grouting_model.gid\n")
		ostream.write("mescape\n")
		for step in range(1,self.global_params['number_of_slices']+1):
			ostream.write("view layers new\n")
			ostream.write("grouting_"+str(step)+"\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("grouting_"+str(step)+"\n escape escape\n")

			ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files\grouting\grouting_volume_" +str(step)+".sat"+"\n ")
			ostream.write("mescape\n")
			

			
		list_surf_grout_out=[1,5]
		k=5
		for a in range (1,self.global_params['number_of_slices']-1):
			k=k+3
			list_surf_grout_out.append(k)
		ostream.write("view layers new\n")
		ostream.write("grouting_surface_inside \n escape escape\n")
		ostream.write("view layers entities\n")
		ostream.write("grouting_surface_inside \n")
		ostream.write("surfaces\n")	
		for i in range(0, len(list_surf_grout_out)):			
			ostream.write(str(list_surf_grout_out[i])+" ")			
		ostream.write("\n")
		ostream.write("mescape\n")
		
		list_surf_grout=[2,6]
		k=6
		for a in range (1,self.global_params['number_of_slices']-1):
			k=k+3
			list_surf_grout.append(k)
			
		for i in range(0, len(list_surf_grout)):	
			ostream.write("view layers new\n")
			ostream.write("grouting_surface_"+str(i+1)+" \n escape escape\n")
			ostream.write("view layers entities\n")
			ostream.write("grouting_surface_"+str(i+1)+" \n")
			ostream.write("surfaces\n")	
		
			ostream.write(str(list_surf_grout[i])+" ")			
			ostream.write("\n")
			ostream.write("mescape\n")	
##### new aproach

		#set delite volumes
		ostream.write("Geometry Delete Volume\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")
		#asigbn layer to all surfaces 
		ostream.write("view layers new\n")
		ostream.write("point \n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("point \n escape escape\n")
		
		nos=self.global_params['number_of_slices']
		
		#coppy first points
		ostream.write("Utilities Copy points Translation\n")
		ostream.write("0,0,0\n")
		ostream.write("-2000,10000,0\n")
		ostream.write("4 \n")
		ostream.write("mescape\n")
		ostream.write("Utilities Copy points Translation\n")
		ostream.write("0,0,0\n")
		ostream.write("2000,10000,0\n")
		ostream.write(str(self.global_params['number_of_slices']*2+2)+" \n")
		ostream.write("mescape\n")
		ostream.write("Utilities Copy points Translation\n")
		ostream.write("0,0,0\n")
		ostream.write("0,-20000,0\n")
		ostream.write(str(self.global_params['number_of_slices']*2+3)+" "+ str(self.global_params['number_of_slices']*2+4) +" \n")		
		ostream.write("mescape\n")
		ostream.write("Geometry Create Line Join\n")	
		ostream.write(str(nos*2+3)+" "+ str(self.global_params['number_of_slices']*2+4) +" \n escape\n")	
		ostream.write(str(nos*2+4)+" "+ str(nos*2+6) +" \n escape\n")		
		ostream.write(str(nos*2+5)+" "+ str(nos*2+6) +" \n escape\n")		
		ostream.write(str(nos*2+5)+" "+ str(nos*2+3) +" \n escape\n")
		ostream.write("mescape\n")		
		ostream.write("Geometry Create NurbsSurface\n")
		ostream.write(str(nos*4+3)+" "+ str(nos*4+4)+" "+str(nos*4+5)+" "+ str(nos*4+6) +" \n escape\n")	
		ostream.write("mescape\n")			
		ostream.write("Geometry Create IntMultSurfs\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")		
		ostream.write("Geometry Delete Surface\n")
		ostream.write(str(nos*10+4)+" \n")	
		ostream.write("mescape\n")
		ostream.write("Geometry Delete Line\n")	
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")	
		ostream.write("Geometry Delete Point\n")	
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")	
		ostream.write("Geometry Create Volume AutomaticStruct\n")	
		ostream.write("mescape\n")
		ostream.write("mescape\n")	
		
		ostream.write("mescape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("grouting_1 \n escape escape\n")
		ostream.write("view layers entities\n")
		ostream.write("grouting_1\n")
		ostream.write("Volumes\n")
		ostream.write("1 3 \n")
		ostream.write("mescape\n")	
		ostream.write("view layers ToUse\n")
		ostream.write("grouting_2 \n escape escape\n")
		ostream.write("view layers entities\n")
		ostream.write("grouting_2\n")
		ostream.write("Volumes\n")
		ostream.write("2 4 \n")
		ostream.write("mescape\n")	

		for step in range(2,self.global_params['number_of_slices']):
			ostream.write("mescape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("grouting_" + str(step+1)  + "\n escape escape\n")
			ostream.write("view layers entities\n")
			ostream.write("grouting_" + str(step+1) + "\n")
			ostream.write("Volumes\n")
			#ostream.write("Entities Volumes\n")
			ostream.write(str(step*2+1)+" "+str(step*2+2)+" \n")
			ostream.write("mescape\n")
			
		#Repair model		
		ostream.write("Utilities Repair Yes\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Repair Yes\n")
		ostream.write("mescape\n")

		
		
		#convert all lines to NURBS
		ostream.write("Geometry Edit ConvToNurbsL\n")
		ostream.write("InvertSelection\n escape\n Yes\n")
		ostream.write("mescape\n")
		
		#set meshing information
		ostream.write("mescape\n")
		ostream.write("Meshing Structured Volumes\n")
		ostream.write("InvertSelection\n escape\n 1\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		
		
		#asigbn layer to all surfaces 
		# list_surf_grout=[nos*3+10,nos*4+12]
		# k=nos*4+12
		# for a in range (1,self.global_params['number_of_slices']):
			# k=k+5
			# list_surf_grout.append(k)
			# k=k+2
			
			# list_surf_grout.append(k)
			
		# ostream.write("view layers new\n")
		# ostream.write("surf \n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("point \n escape escape\n")
		ostream.write("view layers entities\n")
		ostream.write("point \n")
		ostream.write("LowerEntities Surfaces\n")
		ostream.write("layer:point\n")
		ostream.write("mescape\n")
		
		ostream.write("Layers Off point \n")
		ostream.write("mescape\n")		
		
		ostream.write("mescape\n")
		ostream.write("Meshing Structured Lines 6\n")
		ostream.write("InvertSelection\n escape\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		# ostream.write("Meshing Structured Lines 1\n")
		# for i in range (0, len(list_lines_grout)):
			# ostream.write(str(list_lines_grout[i])+" ")
		# ostream.write("\n")
		# ostream.write("mescape\n")				
		# ostream.write("mescape\n")
		ostream.write("Utilities Variables Model(QuadraticType) 1\n")
		ostream.write("mescape\n")
		ostream.write("Meshing Generate\n")
		ostream.write("DefaultSize\n")
		ostream.write("mescape\n")
			
		ostream.write("Files Save\n")
		ostream.write("Quit\n")
		ostream.close()
		
		
		# ####CREATE BACH FILE FOR ACTIVATION LEVELS####
		# ifile = open(self.working_dir+'set_activation_grouting.bch','w')

		# number_of_steps=self.global_params['number_of_slices']-self.global_params['TBM_offset']+(self.global_params['lining_offset'])
		# reactivation_index_stressfree = (-2*number_of_steps)*7-10
		# self.initial_reactivation_index_stressfree = reactivation_index_stressfree
		# reactivation_index = (-2*number_of_steps)*7-9
		# self.initial_reactivation_index = reactivation_index
		# self.initial_face_index = self.global_params['TBM_offset']
		# self.initial_trailer_load_index = self.global_params['lining_offset']-2
		# self.initial_grouting_surface_index = self.global_params['grouting_offset']		
		
		# for step in range(number_of_steps+1, self.global_params['number_of_slices']+1):
		
			# ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
			# ifile.write("Change -1\n")
			# ifile.write("layer:grouting_"+str(step)+"\n")
			# ifile.write("mescape\n")
			
		# for step in range(self.global_params['grouting_offset'],number_of_steps+1):		
			# ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
			# ifile.write("Change "+str(reactivation_index_stressfree)+"\n")
			# ifile.write("layer:grouting_"+str(step)+"\n")
			# ifile.write("mescape\n")

			# for i in range (1,8):
				# reactivation_index = reactivation_index + 2
				# reactivation_index_stressfree = reactivation_index_stressfree + 2		
		
		# ifile.close()	
		#########CREATE BACH FILE FOR MATERIAL PARAMETERS####		
		ifile = open(self.working_dir+'material_condition_grouting.bch','w')
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
		if (self.lining.lod==1) or (self.soil.lod==1):
			return
		
		return
		
		
		return