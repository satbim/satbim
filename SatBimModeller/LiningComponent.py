import sys
import os
import math
import subprocess
from HelperMethods import *
from ModelComponent import *

class LiningComponent(ModelComponent):

	# Constructor
	def __init__(self, global_params, working_dir):
		ModelComponent.__init__(self, global_params, working_dir)
		
		# Setup LOD handlers
		self.lod_prepare_handlers = [self.PrepareModel_Lod1, self.PrepareModel_Lod2, self.PrepareModel_Lod3]
		self.lod_script_handlers = [self.AddToSimScript_Lod1, self.AddToSimScript_Lod2, self.AddToSimScript_Lod3]
		
		# Define name
		self.component_name = "lining"
		
		# Dependencies
		self.excavation = None
		self.tbm = None
		self.soil = None
		#
		self.coords = HelperMethods.ReadAlignmentFile(self.global_params['model_path']+'/input_files/')		
		print(self.coords)
		print(len(self.coords))
		self.rotations = HelperMethods.ReadRingRotationFile(self.global_params['model_path']+'/input_files/')		
		print(self.rotations)
		
	
	def ReadParams(self, pathToParamFile):	
		ModelComponent.ReadParams(self, pathToParamFile)
		
		if self.lod <= 2:
			self.is_collapsable = True
		else:
			self.is_collapsable = False
	
	def PrepareModel_Lod1(self, ostream):
		# Write model to .bch output file
		print 'Lining LOD = 1'
		
		return
	
	def PrepareModel_Lod2(self, ostream):
		# Write model to .bch output file
		print 'Lining LOD = 2'
		
		ostream.write("mescape\n")
		ostream.write("Files SaveAs " + self.working_dir + self.global_params['model_name'] + "_lining_model.gid\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")		
		ostream.write("Utilities Variables ImportTolerance 5 AutoImportTolerance 0\n")
		ostream.write("mescape\n")
		
		for step in range(1,self.global_params['number_of_slices']+1):
			ostream.write("view layers new\n")
			ostream.write("lining_" + str(step) + "\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("lining_" + str(step) + "\n escape escape\n")
			ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
			ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Collapse Model Yes\n")
		ostream.write("mescape\n")
			
		#set delite volumes
		ostream.write("Geometry Delete Volume\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")
		#asigbn layer to all surfaces 
		ostream.write("view layers new\n")
		ostream.write("surf \n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("surf \n escape escape\n")
		ostream.write("view layers entities\n")
		ostream.write("surf \n")
		ostream.write("LowerEntities Surfaces\n")
		ostream.write("InvertSelection\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")

		#set cretate lines
		ostream.write("view layers new\n")
		ostream.write("lines \n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("lines \n escape escape\n")
		ostream.write("mescape\n")
		list_lines = [1,3, 9, 10]
		k = 10
		
		for a in range (1,self.global_params['number_of_slices']):
			k=k+3
			list_lines.append(k)
			k=k+2
			list_lines.append(k)
			k=k+2
			list_lines.append(k)
			k=k+1
			list_lines.append(k)
		ostream.write("view layers entities\n")
		ostream.write("lines \n")		
		ostream.write("LowerEntities Lines\n")
		#ostream.write("lines \n")
		for i in range (0, len(list_lines)):
			ostream.write(str(list_lines[i])+" ")
		ostream.write("\n")
		ostream.write("mescape\n")
		
		
		ostream.write("Geometry Create Line Join\n")	
		ostream.write("1 8 \n escape\n")	
		ostream.write("2 6 \n escape\n")		
		ostream.write("4 5 \n escape\n")		
		ostream.write("3 7 \n escape\n")	
		for step in range(1,self.global_params['number_of_slices']):
			ostream.write(str(4*step+5)+" "+str(4*step+8)+" "+"\n escape\n")		
			ostream.write(str(4*step+6)+" "+str(4*step+7)+" "+"\n escape\n")	
		nos=self.global_params['number_of_slices']
		ostream.write("mescape\n")	
		ostream.write("mescape\n")
		
		ostream.write("View Layers Freeze\n")
		ostream.write("surf \n")
		ostream.write("mescape\n")

		ostream.write("mescape\n")
		ostream.write("Geometry Create NurbsSurface Automatic 4\n")		
		ostream.write("mescape\n")
		ostream.write("mescape\n")

		ostream.write("View Layers UnFreeze\n")
		ostream.write("surf \n")
		ostream.write("mescape\n")
	
		ostream.write("view layers new\n")
		ostream.write("lining_surface_0\n escape escape\n")
		ostream.write("view layers entities\n")
		ostream.write("lining_surface_0\n")
		ostream.write("LowerEntities surfaces\n")
		ostream.write("3 ")
		ostream.write("mescape\n")

		for step in range(1,self.global_params['number_of_slices']+1):
			ostream.write("view layers new\n")
			ostream.write("lining_surface_" + str(step) + "\n escape escape\n")
			ostream.write("view layers entities\n")
			ostream.write("lining_surface_" + str(step) + "\n")
			ostream.write("LowerEntities surfaces\n"+str(5+(step-1)*5)+"\n")
			ostream.write("mescape\n")


		#ostream.write("view layers new\n")
		#ostream.write("lining_surface_outter\n escape escape\n")
		#ostream.write("view layers entities\n")
		#ostream.write("lining_surface_outter\n")
		#ostream.write("LowerEntities surfaces\n")
		#ostream.write(" 1 2 ")
		lin_orf_out=[1,2]
		for step in range(0,self.global_params['number_of_slices']-1):		
			#ostream.write(str(5*step+7)+" "+str(5*step+8)+" ")
			lin_orf_out.append(5*step+7)
			lin_orf_out.append(5*step+8)
		i=0
		for step in range(1,self.global_params['number_of_slices']+1):	
			ostream.write("view layers new\n")
			ostream.write("lining_outer_surface_"+str(step)+"\n escape escape\n")
			ostream.write("view layers entities\n")
			ostream.write("lining_outer_surface_"+str(step)+"\n")
			ostream.write("LowerEntities surfaces\n")
			ostream.write(str(lin_orf_out[i])+" "+str(lin_orf_out[i+1])+"\n")
			i=i+2
			ostream.write("mescape\n")
			
		ostream.write("\n")
		ostream.write("mescape\n")
		
		ostream.write("mescape\n")			
		ostream.write("Geometry Create IntMultSurfs\n")		
		ostream.write("InvertSelection\n")
		ostream.write("mescape\n")
		
		ostream.write("mescape\n")
		ostream.write("Utilities Collapse Model Yes\n")
		ostream.write("mescape\n")
		
		ostream.write("Geometry Create Volume AutomaticStruct\n")	
		ostream.write("mescape\n")
		ostream.write("mescape\n")	

		ostream.write("mescape\n")
			
		ostream.write("Files Save\n")

		for step in range(0,self.global_params['number_of_slices']):
			ostream.write("mescape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("lining_" + str(step+1)  + "\n escape escape\n")
			ostream.write("view layers entities\n")
			ostream.write("lining_" + str(step+1) + "\n")
			ostream.write("Volumes\n")
			#ostream.write("Entities Volumes\n")
			ostream.write(str(step*2+1)+" "+str(step*2+2)+" \n")
			ostream.write("mescape\n")
			
		#assign lines to outer surface	
		ostream.write("view layers ToUse\n")
		ostream.write("lining_surface_outside \n escape escape\n")
		ostream.write("view layers entities\n")
		ostream.write("lining_surface_outside \n")
		ostream.write("LowerEntities Surfaces\n")
		ostream.write("layer:lining_surface_outside\n")
		ostream.write("mescape\n")
		
		#convert all lines to NURBS
		ostream.write("Geometry Edit ConvToNurbsL\n")
		ostream.write("InvertSelection\n escape\n Yes\n")
		ostream.write("mescape\n")
		
		ostream.write("mescape\n")		
		ostream.write("Meshing ElemType Hexahedra\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")
		
		#set meshing information
		ostream.write("Meshing Structured Volumes\n")
		ostream.write("InvertSelection\n escape\n 1\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		

		ostream.write("mescape\n")
		if self.soil.lod>1:	
			ostream.write("Meshing Structured Lines 6\n")
		else:
			ostream.write("Meshing Structured Lines 12\n")		
		ostream.write("InvertSelection\n escape\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		
		ostream.write("Meshing Structured Lines 1\n")
		b=nos*8+4
		
		for a in range (1,(self.global_params['number_of_slices']+1)*2+1):
			b=b+1		
			list_lines.append(b)
		#print(nos)
		
		for i in range (0, len(list_lines)):
			ostream.write(str(list_lines[i])+" ")
		ostream.write("\n")
		
		ostream.write("mescape\n")
				
		ostream.write("mescape\n")
		ostream.write("Utilities Variables Model(QuadraticType) 1\n")
		ostream.write("mescape\n")
		ostream.write("Meshing Generate\n")
		ostream.write("DefaultSize\n")
		ostream.write("mescape\n")
			
		ostream.write("Files Save\n")
		ostream.write("Quit\n")
		
		#####CREATE BACH FILE FOR ACTIVATION LEVELS####	
		if self.soil.lod>1 and self.params['lod']>1 :			
			ifile = open(self.working_dir+'set_activation_lining.bch','w')
			ifile_g =  open(self.working_dir+'set_activation_grouting.bch','w')
			no_segments= int(self.global_params['segment_type'])

			number_of_steps=self.global_params['number_of_slices']-self.global_params['TBM_offset']+(self.global_params['lining_offset'])
			if no_segments==61:
				reactivation_index_stressfree = (-2*number_of_steps)*7-10
				reactivation_index_stressfree_g = (-2*number_of_steps)*7-10
			elif no_segments==71:
				reactivation_index_stressfree = (-2*number_of_steps)*8-10
				reactivation_index_stressfree_g = (-2*number_of_steps)*8-10
			else:
				print("Error:segments")
			self.initial_reactivation_index_stressfree = reactivation_index_stressfree
			if no_segments==61:
				reactivation_index = (-2*number_of_steps)*7-9
				reactivation_index_g = (-2*number_of_steps)*7-9
			elif no_segments==71:
				reactivation_index = (-2*number_of_steps)*8-9
				reactivation_index_g = (-2*number_of_steps)*8-9
			else:
				print("Error:segments")
			self.initial_reactivation_index = reactivation_index
			self.initial_face_index = self.global_params['TBM_offset']
			self.initial_trailer_load_index = self.global_params['lining_offset']-2
			self.initial_grouting_surface_index = self.global_params['grouting_offset']	
			#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
			for step in range(number_of_steps+1, self.global_params['number_of_slices']+1):
			

				ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
				ifile.write("Change -1\n")
				ifile.write("layer:lining_"+str(step)+"\n")
				ifile.write("mescape\n")
			for step in range(number_of_steps+1, self.global_params['number_of_slices']+1):
			

				ifile_g.write("Data Conditions AssignCond Volume_Activation_Level\n")
				ifile_g.write("Change -1\n")
				ifile_g.write("layer:grouting_"+str(step)+"\n")
				ifile_g.write("mescape\n")
				
			for step in range(self.global_params['lining_offset'], number_of_steps+1):		
				ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
				ifile.write("Change "+str(reactivation_index)+"\n")
				ifile.write("layer:lining_"+str(step)+"\n")
				ifile.write("mescape\n")
				for i in range (1,8):
					reactivation_index = reactivation_index + 2
					reactivation_index_stressfree = reactivation_index_stressfree + 2
					
			for step in range(self.global_params['grouting_offset'], number_of_steps+1):		
				ifile_g.write("Data Conditions AssignCond Volume_Activation_Level\n")
				ifile_g.write("Change "+str(reactivation_index_g)+"\n")
				ifile_g.write("layer:grouting_"+str(step)+"\n")
				ifile_g.write("mescape\n")
				for i in range (1,8):
					reactivation_index_g = reactivation_index_g + 2
					reactivation_index_stressfree_g = reactivation_index_stressfree_g + 2
			#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
			#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
			ifile.close()
			ifile_g.close()
			
		
		#########CREATE BACH FILE FOR MATERIAL PARAMETERS AND CONDITIONS####		
		ifile = open(self.working_dir+'material_condition_lining.bch','w')
		ifile.write("mescape\n")
		ifile.write("Data Materials NewMaterial Isotropic3D Lining_Concrete Isotropic3D Isotropic3D 2500.0kg/m^3 20000000000N/mm^2 0.3\n")
		ifile.write("mescape\n")


		for step in range(1, self.global_params['number_of_slices']+1):	

			ifile.write("Data Materials AssignMaterial Lining_Concrete Volumes\n")
			ifile.write("layer:lining_"+str(step)+"\n")
			ifile.write("mescape\n")
			
		#asign kinematic linear element type to linig
		for step in range(1, self.global_params['number_of_slices']+1):
			ifile.write("Data Conditions AssignCond VolumeElementType\n")
			ifile.write("Change Kinematic_Linear\n")
			ifile.write("1000.0kg/m^3\n")
			ifile.write("1.295kg/m^3\n")
			ifile.write("0.2\n")
			ifile.write("0.001m/s\n")
			ifile.write("0.00000032m/s\n")
			ifile.write("0.00000044m/s\n")
			ifile.write("0.0001m/s\n")
			ifile.write("0.0535\n")
			ifile.write("layer:lining_"+str(step)+"\n")
			ifile.write("mescape\n")
			
			
		if self.soil.lod==1:
			for i in range(1,self.global_params['number_of_slices']+1):	
				ifile.write("mescape\n")
				ifile.write("Data Conditions AssignCond Distributed_Surface_Load\n")
				ifile.write("layer:lining_outer_surface_"+str(i)+"\n")
				ifile.write("mescape\n")
			for i in range(1,self.global_params['number_of_slices']+1):	
				ifile.write("mescape\n")
				ifile.write("Data Conditions AssignCond Surface_Bedding Change\n 1 0.0N/m^3\n 1 0.0N/m^3\n 1 0.0N/m^3\n")
				ifile.write("layer:lining_outer_surface_"+str(i)+"\n")
				ifile.write("mescape\n")


		
			
		#self.coords = HelperMethods.ReadAlignmentFile(self.global_params['model_path']+'/input_files/')		
		#print(self.coords)
		
		return
		
	def PrepareModel_Lod3(self, ostream):
		# Write model to .bch output file
		
		print 'Lining LOD = 3'
		self.PrepareBoltModel()
		#TESTING_NEW_BOTS
		#self.PrepareBoltModel1()
		
	#	sys.exit()	
		ifile = open( self.working_dir+self.global_params['model_name']+"_lining_help.bch", 'w' )
		no_segments= int(self.global_params['segment_type'])
		ifile.write("mescape\n")
		ifile.write("Files SaveAs " + self.working_dir + self.global_params['model_name'] + "_lining_help.gid\n")
		# ifile.write("mescape\n")
		# ifile.write("mescape Utilities Variables AutoCollapseAfterImport 0\n")
		# ifile.write("mescape\n")

		
		ifile.write("mescape\n")		
		ifile.write("Utilities Variables ImportTolerance 5 AutoImportTolerance 0\n")
		ifile.write("mescape\n")
		nos=self.global_params['number_of_slices']
		#print(self.params['segment_type'])
		if no_segments==61:
			i=0
			lin_volume=1
			for step in range(nos*3+1,nos*4+1):

				ifile.write("view layers new\n")
				ifile.write("lining_" + str(i+1) +"_4" + "\n escape escape\n")
				ifile.write("view layers ToUse\n")
				ifile.write("lining_" + str(i+1) +"_4" + "\n escape escape\n")
				ifile.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
				ifile.write("mescape\n")
				ifile.write("Utilities Move Volumes Translation\n")
				ifile.write("0,0,0\n")
				ifile.write(str(self.global_params['round_length']*i)+" 0 "+str(self.global_params['excavation_radius']*2)+"\n")
				ifile.write(str(lin_volume)+"\n")
				ifile.write("mescape\n")	
				i=i+1
				lin_volume=lin_volume+1
			i=0
			for step in range(nos*4+1,nos*5+1):
				ifile.write("view layers new\n")
				ifile.write("lining_" + str(i+1) +"_5" + "\n escape escape\n")
				ifile.write("view layers ToUse\n")
				ifile.write("lining_" + str(i+1) +"_5" + "\n escape escape\n")
				ifile.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
				ifile.write("mescape\n")
				ifile.write("Utilities Move Volumes Translation\n")
				ifile.write("0,0,0\n")
				ifile.write(str(self.global_params['round_length']*i)+" 0 "+str(self.global_params['excavation_radius']*2)+"\n")
				ifile.write(str(lin_volume)+"\n")
				ifile.write("mescape\n")
				lin_volume=lin_volume+1
				i=i+1
		elif no_segments==71:
			i=0
			lin_volume=1
			for step in range(nos*3+1,nos*4+1):
			#for step in range(nos*4+1,nos*5+1):

				ifile.write("view layers new\n")
				#ifile.write("lining_" + str(i+1) +"_5" + "\n escape escape\n")
				ifile.write("lining_" + str(i+1) +"_4" + "\n escape escape\n")
				ifile.write("view layers ToUse\n")
				#ifile.write("lining_" + str(i+1) +"_5" + "\n escape escape\n")
				ifile.write("lining_" + str(i+1) +"_4" + "\n escape escape\n")
				ifile.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
				ifile.write("mescape\n")
				ifile.write("Utilities Move Volumes Translation\n")
				ifile.write("0,0,0\n")
				ifile.write(str(self.global_params['round_length']*i)+" 0 "+str(self.global_params['excavation_radius']*2)+"\n")
				ifile.write(str(lin_volume)+"\n")
				ifile.write("mescape\n")	
				i=i+1
				lin_volume=lin_volume+1
			i=0
			#for step in range(nos*5+1,nos*6+1):
			for step in range(nos*6+1,nos*7+1):
				ifile.write("view layers new\n")
				#ifile.write("lining_" + str(i+1) +"_6" + "\n escape escape\n")
				ifile.write("lining_" + str(i+1) +"_7" + "\n escape escape\n")
				ifile.write("view layers ToUse\n")
				#ifile.write("lining_" + str(i+1) +"_6" + "\n escape escape\n")
				ifile.write("lining_" + str(i+1) +"_7" + "\n escape escape\n")
				ifile.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
				ifile.write("mescape\n")
				ifile.write("Utilities Move Volumes Translation\n")
				ifile.write("0,0,0\n")
				ifile.write(str(self.global_params['round_length']*i)+" 0 "+str(self.global_params['excavation_radius']*2)+"\n")
				ifile.write(str(lin_volume)+"\n")
				ifile.write("mescape\n")
				lin_volume=lin_volume+1
				i=i+1
		else:
			print("ERROR: the sugestid number of segments not jet implemented")

			
		ifile.write("Utilities Repair Yes\n")
		ifile.write("mescape\n")
		list_del = []
		k = 0
		print (self.params['rs'])
		if self.params['rs'] == 'True':
			k=nos*12
		#	print("here")
			for a in range (1,nos+1):
				k=k+13
				list_del.append(k)
				k=k+5
				list_del.append(k)
			
		else:
			for a in range (1,nos+1):
				k=k+15
				list_del.append(k)
			for a in range (1,nos+1):
				k=k+13
				list_del.append(k)
				k=k+5
				list_del.append(k)

		# set delite volumes
		ifile.write("Geometry Delete Volume\n")
		ifile.write("InvertSelection\n escape\n escape\n")
		ifile.write("mescape\n")
		#set delite surfaces
		ifile.write("Geometry Delete Surface\n")
		ifile.write("InvertSelection\n escape\n escape\n")
		ifile.write("mescape\n")
		#set delite surfaces
		ifile.write("Geometry Delete Line\n")
		for i in range(0,len(list_del)):
			ifile.write(str(list_del[i])+" ")
		ifile.write("\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Collapse Model Yes\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Geometry Create NurbsSurface Automatic 4\n")		
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Geometry Create Volume AutomaticStruct\n")	
		ifile.write("mescape\n")
		ifile.write("mescape\n")

		if no_segments==61:		
			for step in range(1,self.global_params['number_of_slices']+1):
				ifile.write("mescape\n")
				ifile.write("view layers ToUse\n")
				ifile.write("lining_" + str(step) +"_4" + "\n escape escape\n")
				ifile.write("view layers entities\n")
				ifile.write("lining_" + str(step) +"_4" + "\n")
				ifile.write("LowerEntities Volumes\n")
				ifile.write(str(step)+"\n")
				ifile.write("mescape\n")
				ifile.write("view layers ToUse\n")
				ifile.write("lining_" + str(step) +"_5" + "\n escape escape\n")
				ifile.write("view layers entities\n")
				ifile.write("lining_" + str(step) +"_5" + "\n")
				ifile.write("LowerEntities Volumes\n")
				ifile.write(str(step+nos)+"\n")
				ifile.write("mescape\n")
		elif no_segments==71:
			for step in range(1,self.global_params['number_of_slices']+1):
				ifile.write("mescape\n")
				ifile.write("view layers ToUse\n")
				# ifile.write("lining_" + str(step) +"_5" + "\n escape escape\n")
				# ifile.write("view layers entities\n")
				# ifile.write("lining_" + str(step) +"_5" + "\n")
				ifile.write("lining_" + str(step) +"_4" + "\n escape escape\n")
				ifile.write("view layers entities\n")
				ifile.write("lining_" + str(step) +"_4" + "\n")
				ifile.write("LowerEntities Volumes\n")
				ifile.write(str(step)+"\n")
				ifile.write("mescape\n")
				ifile.write("view layers ToUse\n")
				# ifile.write("lining_" + str(step) +"_6" + "\n escape escape\n")
				# ifile.write("view layers entities\n")
				# ifile.write("lining_" + str(step) +"_6" + "\n")
				ifile.write("lining_" + str(step) +"_7" + "\n escape escape\n")
				ifile.write("view layers entities\n")
				ifile.write("lining_" + str(step) +"_7" + "\n")
				ifile.write("LowerEntities Volumes\n")
				ifile.write(str(step+nos)+"\n")
				ifile.write("mescape\n")
		else:
			print("ERROR: number of segments")
			
		for step in range(1,self.global_params['number_of_slices']+1):
			ifile.write("view layers new\n")
			ifile.write("lining_surface_" + str(step)+ "\n escape escape\n")
			ifile.write("view layers entities\n")
			ifile.write("lining_surface_" + str(step)+ "\n")
			ifile.write("LowerEntities surfaces\n")
			x=(step-1)*6
			ifile.write(str(4+x)+" "+str(nos*6+6+x))			
			ifile.write("\n")
			ifile.write("mescape\n")
		# for step in range(1,self.global_params['number_of_slices']+1):
			ifile.write("view layers new\n")
			ifile.write("lining_surface_back_" + str(step)+ "\n escape escape\n")
			ifile.write("view layers entities\n")
			ifile.write("lining_surface_back_" + str(step)+ "\n")
			ifile.write("LowerEntities surfaces\n")
			# x=(step-1)*6
			ifile.write(str(2+x)+" "+str(nos*6+4+x))			
			ifile.write("\n")
			ifile.write("mescape\n")
		
		ifile.write("view layers new\n")
		if no_segments==61:	
			ifile.write("lining_joint_master_4\n escape escape\n")
			ifile.write("view layers entities\n")
			ifile.write("lining_joint_master_4\n")	
		elif no_segments==71:	
			ifile.write("lining_joint_master_4\n escape escape\n")
			#ifile.write("lining_joint_master_5\n escape escape\n")
			ifile.write("view layers entities\n")
			#ifile.write("lining_joint_master_5\n")	
			ifile.write("lining_joint_master_4\n")	
		else:
			print("ERROR: segments")
		ifile.write("LowerEntities surfaces\n")		
		for step in range(1,self.global_params['number_of_slices']+1):
			###############################
			x=(step-1)*6
			ifile.write(str(5+x)+" ")			
		ifile.write("\n")
		ifile.write("mescape\n")
		ifile.write("view layers new\n")
		if no_segments==61:
			ifile.write("lining_joint_master_5\n escape escape\n")
			ifile.write("view layers entities\n")
			ifile.write("lining_joint_master_5\n")
		elif no_segments==71:
			#ifile.write("lining_joint_master_6\n escape escape\n")
			ifile.write("lining_joint_master_7\n escape escape\n")
			ifile.write("view layers entities\n")
			#ifile.write("lining_joint_master_6\n")
			ifile.write("lining_joint_master_7\n")
		else:
			print("ERROR: segments")
		ifile.write("LowerEntities surfaces\n")				
		for step in range(1,self.global_params['number_of_slices']+1):
			x=(step-1)*6
			ifile.write(str(nos*6+3+x)+" ")			
		ifile.write("\n")
		ifile.write("mescape\n")

		
			###############################
		ifile.write("view layers new\n")
		if no_segments==61:
			ifile.write("lining_joint_slave_4\n escape escape\n")
			ifile.write("view layers entities\n")
			ifile.write("lining_joint_slave_4 \n")
		elif no_segments==71:
			# ifile.write("lining_joint_slave_5\n escape escape\n")
			# ifile.write("view layers entities\n")
			# ifile.write("lining_joint_slave_5 \n")
			ifile.write("lining_joint_slave_4\n escape escape\n")
			ifile.write("view layers entities\n")
			ifile.write("lining_joint_slave_4 \n")
		else:
			print("ERROR: segments")
		ifile.write("LowerEntities surfaces\n")
		for step in range(1,self.global_params['number_of_slices']+1):
			x=(step-1)*6
			ifile.write(str(3+x)+" ")			
		ifile.write("\n")
		ifile.write("mescape\n")
		ifile.write("view layers new\n")
		if no_segments==61:
			ifile.write("lining_joint_slave_5\n escape escape\n")
			ifile.write("view layers entities\n")
			ifile.write("lining_joint_slave_5 \n")
		elif no_segments==71:
			# ifile.write("lining_joint_slave_6\n escape escape\n")
			# ifile.write("view layers entities\n")
			# ifile.write("lining_joint_slave_6 \n")
			ifile.write("lining_joint_slave_7\n escape escape\n")
			ifile.write("view layers entities\n")
			ifile.write("lining_joint_slave_7 \n")
		else:
			print("ERROR:segments")
		ifile.write("LowerEntities surfaces\n")
		for step in range(1,self.global_params['number_of_slices']+1):
			x=(step-1)*6
			ifile.write(str(nos*6+1+x)+" ")			
		ifile.write("\n")
		ifile.write("mescape\n")
		#CORRECTION HERE
		#lin_surf_out_1=[]
		#for step in range(1,self.global_params['number_of_slices']+1):	
		#	x=(step-1)*6		
		#	ifile.write(str(1+x)+" "+str(nos*6+2+x)+" ")	
			
		for step in range(1,self.global_params['number_of_slices']+1):	
			ifile.write("view layers new\n")
			ifile.write("lining_outer_surface_"+str(step)+" \n escape escape\n")
			ifile.write("view layers entities\n")
			ifile.write("lining_outer_surface_"+str(step)+" \n")
			ifile.write("LowerEntities surfaces\n")	
			x=(step-1)*6		
			ifile.write(str(1+x)+" "+str(nos*6+2+x)+" ")			
			ifile.write("\n")
			ifile.write("mescape\n")
		i=0
		for step in range(1,nos+1):
			ifile.write("mescape\n")
			ifile.write("Utilities Move Volumes Duplicate MaintainLayers Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(-self.global_params['round_length']*(i))+" 0 "+str(-self.global_params['excavation_radius']*2)+"\n")
			ifile.write(str(step)+"\n")
			ifile.write("mescape\n")
			i=i+1
		i=0
		for step in range(nos+1,nos*2+1):
			ifile.write("mescape\n")
			ifile.write("Utilities Move Volumes Duplicate MaintainLayers Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(-self.global_params['round_length']*(i))+" 0 "+str(-self.global_params['excavation_radius']*2)+"\n")
			ifile.write(str(step)+"\n")
			ifile.write("mescape\n")
			i=i+1

		
		ifile.write("Files Save\n")
		ifile.write("Quit\n")
		ifile.close()
		subprocess.check_output([self.global_params['gid_path']+'gid_offscreen.bat', '-offscreen', '-b', self.global_params['model_name'] + "_lining_help.bch", self.global_params['model_name']], cwd=self.working_dir)

		
		

		####################################################################################		
		
		
		
		ostream.write("mescape\n")
		ostream.write("Files SaveAs " + self.working_dir + self.global_params['model_name'] + "_lining_model.gid\n")
		ostream.write("mescape\n")
		
		ostream.write("mescape\n")		
		ostream.write("Utilities Variables ImportTolerance 5 AutoImportTolerance 0\n")
		ostream.write("mescape\n")		
		
		ostream.write("mescape\n")
		ostream.write("mescape Utilities Variables AutoCollapseAfterImport 0\n")
		ostream.write("mescape\n")
		
		
		i=0
		
		for step in range(1,nos+1):
			
			ostream.write("view layers new\n")
			ostream.write("lining_" + str(i+1) +"_1"+ "\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("lining_" + str(i+1) +"_1"+ "\n escape escape\n")
			ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
			ostream.write("mescape\n")

			i=i+1
		####################################################################################
		i=0
		for step in range(nos+1,nos*2+1):
	
			ostream.write("view layers new\n")
			ostream.write("lining_" + str(i+1) +"_2"+ "\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("lining_" + str(i+1) +"_2" + "\n escape escape\n")
			ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
			ostream.write("mescape\n")

			i=i+1
		i=0
		for step in range(nos*2+1,nos*3+1):
			ostream.write("view layers new\n")
			ostream.write("lining_" + str(i+1) +"_3"+ "\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("lining_" + str(i+1) +"_3"+ "\n escape escape\n")
			ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
			ostream.write("mescape\n")

			i=i+1
		if no_segments== 71:
			i=0
			for step in range(nos*4+1,nos*5+1):

				ostream.write("view layers new\n")
				ostream.write("lining_" + str(i+1) +"_5" + "\n escape escape\n")
				ostream.write("view layers ToUse\n")
				ostream.write("lining_" + str(i+1) +"_5" + "\n escape escape\n")
				ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
				ostream.write("mescape\n")
				i=i+1
			
		
		ostream.write("mescape\n")				
		ostream.write("Files InsertGeom " + self.working_dir + self.global_params['model_name'] + "_lining_help.gid\n")
		ostream.write("mescape\n")
		
		if no_segments== 61:
			i=0
			for step in range(nos*5+1,nos*6+1):

				ostream.write("view layers new\n")
				ostream.write("lining_" + str(i+1) +"_6" + "\n escape escape\n")
				ostream.write("view layers ToUse\n")
				ostream.write("lining_" + str(i+1) +"_6" + "\n escape escape\n")
				ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
				ostream.write("mescape\n")
				i=i+1
			i=0
			for step in range(nos*6+1,nos*7+1):
				ostream.write("view layers new\n")
				ostream.write("lining_" + str(i+1) +"_7" + "\n escape escape\n")
				ostream.write("view layers ToUse\n")
				ostream.write("lining_" + str(i+1) +"_7" + "\n escape escape\n")
				ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
				ostream.write("mescape\n")

				i=i+1
				
		if no_segments== 71:
			i=0			
			for step in range(nos*5+1,nos*6+1):
				ostream.write("view layers new\n")
				ostream.write("lining_" + str(i+1) +"_6" + "\n escape escape\n")
				ostream.write("view layers ToUse\n")
				ostream.write("lining_" + str(i+1) +"_6" + "\n escape escape\n")
				ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
				ostream.write("mescape\n")

				i=i+1
			i=0
			for step in range(nos*7+1,nos*8+1):

				ostream.write("view layers new\n")
				ostream.write("lining_" + str(i+1) +"_8" + "\n escape escape\n")
				ostream.write("view layers ToUse\n")
				ostream.write("lining_" + str(i+1) +"_8" + "\n escape escape\n")
				ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/lining/lining_volume_" +str(step)+".sat"+"\n ")
				ostream.write("mescape\n")
				i=i+1
				
				
		nos=self.global_params['number_of_slices']

		ostream.write("Utilities Repair Yes\n")
		ostream.write("mescape\n")
		list_del = []

		for step in range(1,self.global_params['number_of_slices']+1):
			ostream.write("view layers ToUse\n")
			ostream.write("lining_surface_" + str(step)+ "\n escape escape\n")
			ostream.write("view layers entities\n")
			ostream.write("lining_surface_" + str(step)+ "\n")
			ostream.write("LowerEntities surfaces\n")
			x=(step-1)*6
			if no_segments==61:
				ostream.write(str(4+x)+" "+str(nos*6+4+x)+" "+str(nos*6*2+4+x)+" "+str(nos*6*5+4+x)+" "+str(nos*6*6+4+x))
			elif no_segments==71:
				ostream.write(str(4+x)+" "+str(nos*6+4+x)+" "+str(nos*6*2+4+x)+" "+str(nos*6*3+4+x)+" "+str(nos*6*6+4+x)+" "+str(nos*6*7+4+x))	
			else:
				print("ERROR")				
			ostream.write("\n")
			ostream.write("mescape\n")
		#for step in range(1,self.global_params['number_of_slices']+1):
			ostream.write("view layers ToUse\n")
			ostream.write("lining_surface_back_" + str(step)+ "\n escape escape\n")
			ostream.write("view layers entities\n")
			ostream.write("lining_surface_back_" + str(step)+ "\n")
			ostream.write("LowerEntities surfaces\n")
			#x=(step-1)*6
			if no_segments==61:
				ostream.write(str(3+x)+" "+str(nos*6+3+x)+" "+str(nos*6*2+3+x)+" "+str(nos*6*5+3+x)+" "+str(nos*6*6+3+x))
			elif no_segments==71:
				ostream.write(str(3+x)+" "+str(nos*6+3+x)+" "+str(nos*6*2+3+x)+" "+str(nos*6*3+3+x)+" "+str(nos*6*6+3+x)+" "+str(nos*6*7+3+x))
			else:
				print("ERROR")				

			ostream.write("\n")
			ostream.write("mescape\n")
			
		print(self.global_params['segment_type'])	
		if no_segments==61:		
			list_jl=[1,2,3,6,7]
		elif no_segments==71:
			list_jl=[1,2,3,4,7,8]

		
		else:
			print("ERROR")
			###############################
		for j in list_jl:
		
			if no_segments==71:	
				if j==4:
					k=5
				elif j==7:
					k=6
				else:
					k=j
			else:
				k=j
			ostream.write("view layers new\n")
			ostream.write("lining_joint_slave_"+str(k)+"\n escape escape\n")
			ostream.write("view layers entities\n")
			ostream.write("lining_joint_slave_"+str(k)+" \n")
			ostream.write("LowerEntities surfaces\n")
			for step in range(1,self.global_params['number_of_slices']+1):
				x=(step-1)*6
#				if self.params['segment_type']== '61':
				ostream.write(str(2+x+(j-1)*nos*6)+" ")			
			ostream.write("\n")
			ostream.write("mescape\n")
			
			ostream.write("view layers new\n")
			ostream.write("lining_joint_master_"+str(k)+"\n escape escape\n")
			ostream.write("view layers entities\n")
			ostream.write("lining_joint_master_"+str(k)+" \n")
			ostream.write("LowerEntities surfaces\n")
			for step in range(1,self.global_params['number_of_slices']+1):
				x=(step-1)*6
#				if self.params['segment_type']== '61':
				ostream.write(str(5+x+(j-1)*nos*6)+" ")			
			ostream.write("\n")
			ostream.write("mescape\n")


		#correction_here
		

		#ostream.write("surfaces\n")	
		for step in range(1,self.global_params['number_of_slices']+1):	
			ostream.write("view layers ToUse\n")
			ostream.write("lining_outer_surface_"+str(step)+" \n escape escape\n")
			ostream.write("view layers entities\n")
			ostream.write("lining_outer_surface_"+str(step)+ "\n")
			ostream.write("LowerEntities Surfaces\n")
			x=(step-1)*6
			if no_segments== 61:
				ostream.write(str(1+x)+" "+str(nos*6+1+x)+" "+str(nos*6*2+1+x)+" "+str(nos*6*5+1+x)+" "+str(nos*6*6+1+x)+" ")		
			elif no_segments== 71:
				#ostream.write(str(1+x)+" "+str(nos*6+1+x)+" "+str(nos*6*2+1+x)+" "+str(nos*6*3+1+x)+" "+str(nos*6*6+1+x)+" "+str(nos*6*7+1+x)+" ")	
				ostream.write(str(1+x)+" "+str(nos*6+1+x)+" "+str(nos*6*2+1+x)+" "+str(nos*6*3+1+x)+" "+str(nos*6*6+1+x)+" "+str(nos*6*7+1+x)+" ")	
			ostream.write("\n")
			ostream.write("mescape\n")
		
		ostream.write("mescape\n")		
		ostream.write("Meshing ElemType Hexahedra\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")
		ostream.write("Meshing Structured Volumes\n")
		ostream.write("InvertSelection\n escape\n 1\n")
		ostream.write("InvertSelection\n escape\n escape\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		if self.soil.lod==1:
			ostream.write("Meshing Structured Lines 1\n")
		else:
			ostream.write("Meshing Structured Lines 1\n")
		ostream.write("InvertSelection\n escape\n")
		ostream.write("mescape\n")
		
		#Switch off all layers except Lining_surface_outter and apply discretozation for better result
		ostream.write("mescape\n")
		for step in range(1,self.global_params['number_of_slices']+1):
		
			ostream.write("Layers off lining_surface_"+str(step)+ "\n")
			ostream.write("mescape\n")
			ostream.write("Layers off lining_surface_back_"+str(step)+ "\n")
			ostream.write("mescape\n")
		if no_segments== 61:
			for step in range(1,8):
				ostream.write("Layers off lining_joint_master_"+str(step)+ "\n")
				ostream.write("mescape\n")
				ostream.write("Layers off lining_joint_slave_"+str(step)+ "\n")
				ostream.write("mescape\n")
		elif no_segments== 71:
			for step in range(1,9):
				ostream.write("Layers off lining_joint_master_"+str(step)+ "\n")
				ostream.write("mescape\n")
				ostream.write("Layers off lining_joint_slave_"+str(step)+ "\n")
				ostream.write("mescape\n")
		else:
			print("ERROR")	
				
		if no_segments==61:
			for step in range(1, self.global_params['number_of_slices']+1):
				for i in range (1,8):
					ostream.write("Layers off lining_"+str(step)+"_"+str(i)+ "\n")
					ostream.write("mescape\n")
		elif no_segments==71:
			for step in range(1, self.global_params['number_of_slices']+1):
				for i in range (1,9):
					ostream.write("Layers off lining_"+str(step)+"_"+str(i)+ "\n")
					ostream.write("mescape\n")
		else:
			print("ERROR")	
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Meshing Structured Lines 3\n")
		ostream.write("InvertSelection\n escape\n")
		ostream.write("mescape\n")
		
		for step in range(1,self.global_params['number_of_slices']+1):
		
			ostream.write("Layers on lining_surface_"+str(step)+ "\n")
			ostream.write("mescape\n")
			ostream.write("Layers on lining_surface_back_"+str(step)+ "\n")
			ostream.write("mescape\n")
		if no_segments== 61:
			for step in range(1,8):
				ostream.write("Layers on lining_joint_master_"+str(step)+ "\n")
				ostream.write("mescape\n")
				ostream.write("Layers on lining_joint_slave_"+str(step)+ "\n")
				ostream.write("mescape\n")
		elif no_segments== 71:
			for step in range(1,9):
				ostream.write("Layers on lining_joint_master_"+str(step)+ "\n")
				ostream.write("mescape\n")
				ostream.write("Layers on lining_joint_slave_"+str(step)+ "\n")
				ostream.write("mescape\n")
		else:
			print("ERROR")	
				
		if no_segments==61:
			for step in range(1, self.global_params['number_of_slices']+1):
				for i in range (1,8):
					ostream.write("Layers on lining_"+str(step)+"_"+str(i)+ "\n")
					ostream.write("mescape\n")
		elif no_segments==71:
			for step in range(1, self.global_params['number_of_slices']+1):
				for i in range (1,9):
					ostream.write("Layers on lining_"+str(step)+"_"+str(i)+ "\n")
					ostream.write("mescape\n")
		else:
			print("ERROR")	

		# ostream.write("mescape\n")
				
		ostream.write("mescape\n")
		ostream.write("Utilities Variables Model(QuadraticType) 1\n")
		ostream.write("mescape\n")
		ostream.write("Meshing Generate\n")
		ostream.write("DefaultSize\n")
		ostream.write("mescape\n")
			
		ostream.write("Files Save\n")
			
		
		ostream.write("Quit\n")		
		
		
		#####CREATE BACH FILE FOR ACTIVATION LEVELS####		
		ifile = open(self.working_dir+'set_activation_lining.bch','w')
		ifile_g =  open(self.working_dir+'set_activation_grouting.bch','w')
		if no_segments==61:
			number_of_steps=self.global_params['number_of_slices']-self.global_params['TBM_offset']+(self.global_params['lining_offset'])
			reactivation_index_stressfree = (-2*number_of_steps)*7-10
			self.initial_reactivation_index_stressfree = reactivation_index_stressfree
			reactivation_index = (-2*number_of_steps)*7-9
		elif no_segments==71:
			number_of_steps=self.global_params['number_of_slices']-self.global_params['TBM_offset']+(self.global_params['lining_offset'])
			reactivation_index_stressfree = (-2*number_of_steps)*8-10

			self.initial_reactivation_index_stressfree = reactivation_index_stressfree
			reactivation_index = (-2*number_of_steps)*8-9			
			print (reactivation_index)			
			
		self.initial_reactivation_index = reactivation_index
		self.initial_face_index = self.global_params['TBM_offset']
		self.initial_trailer_load_index = self.global_params['lining_offset']-2
		self.initial_grouting_surface_index = self.global_params['grouting_offset']	
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		if self.params['lod']>1 and self.soil.lod!=1:

			if no_segments==61:
				for step in range(number_of_steps+1, self.global_params['number_of_slices']+1):
					for i in range (1,8):
						ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
						ifile.write("Change -1\n")
						ifile.write("layer:lining_"+str(step)+"_"+str(i)+"\n")
						ifile.write("mescape\n")
						ifile.write("mescape\n")
						ifile.write("Data Conditions AssignCond Line_Activation_Level\n")
						ifile.write("Change -1\n")
						ifile.write("layer:bolts_"+str(step)+"_"+str(i)+"\n")
						ifile.write("mescape\n")
						ifile_g.write("Data Conditions AssignCond Volume_Activation_Level\n")
						ifile_g.write("Change -1\n")
						ifile_g.write("layer:grouting_"+str(step)+"\n")
						ifile_g.write("mescape\n")
					#here remains the question of syarting index
				for step in range(self.global_params['lining_offset']+1, number_of_steps+1):	
				#for step in range(self.global_params['lining_offset'], number_of_steps+1):				
					for i in range (1,8):
						ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
						ifile.write("Change "+str(reactivation_index)+"\n")
						ifile.write("layer:lining_"+str(step)+"_"+str(8-i)+"\n")
						ifile.write("mescape\n")
						ifile.write("Data Conditions AssignCond Line_Activation_Level\n")
						ifile.write("Change "+str(reactivation_index)+"\n")
						ifile.write("layer:bolts_"+str(step)+"_"+str(i)+"\n")
						ifile.write("mescape\n")
						reactivation_index = reactivation_index + 2
						reactivation_index_stressfree = reactivation_index_stressfree + 2
				reactivation_index_stressfree=reactivation_index_stressfree -2*(number_of_steps-self.global_params['lining_offset'])*7
				for step in range(self.global_params['grouting_offset']+1,number_of_steps+1):		
					ifile_g.write("Data Conditions AssignCond Volume_Activation_Level\n")
					ifile_g.write("Change "+str(reactivation_index_stressfree)+"\n")
					ifile_g.write("layer:grouting_"+str(step)+"\n")
					ifile_g.write("mescape\n")
					for i in range (1,8):
						reactivation_index = reactivation_index + 2
						reactivation_index_stressfree = reactivation_index_stressfree + 2		
		
					
			elif no_segments==71:
				for step in range(number_of_steps+1, self.global_params['number_of_slices']+1):
					for i in range (1,9):
						ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
						ifile.write("Change -1\n")
						ifile.write("layer:lining_"+str(step)+"_"+str(i)+"\n")
						ifile.write("mescape\n")
						ifile.write("mescape\n")
						ifile.write("Data Conditions AssignCond Line_Activation_Level\n")
						ifile.write("Change -1\n")
						ifile.write("layer:bolts_"+str(step)+"_"+str(i)+"\n")
						ifile.write("mescape\n")
						ifile_g.write("Data Conditions AssignCond Volume_Activation_Level\n")
						ifile_g.write("Change -1\n")
						ifile_g.write("layer:grouting_"+str(step)+"\n")
						ifile_g.write("mescape\n")
				#here remains the question of syarting index
				for step in range(self.global_params['lining_offset'], number_of_steps+1):	
				#for step in range(self.global_params['lining_offset'], number_of_steps+1):				
					for i in range (1,9):
						ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
						ifile.write("Change "+str(reactivation_index)+"\n")
						ifile.write("layer:lining_"+str(step)+"_"+str(9-i)+"\n")
						ifile.write("mescape\n")
						ifile.write("Data Conditions AssignCond Line_Activation_Level\n")
						ifile.write("Change "+str(reactivation_index)+"\n")
						ifile.write("layer:bolts_"+str(step)+"_"+str(i)+"\n")
						ifile.write("mescape\n")
						reactivation_index = reactivation_index + 2
						reactivation_index_stressfree = reactivation_index_stressfree + 2
				reactivation_index_stressfree=reactivation_index_stressfree -2*(number_of_steps-self.global_params['lining_offset'])*8
				for step in range(self.global_params['grouting_offset'],number_of_steps+1):	
					
					ifile_g.write("Data Conditions AssignCond Volume_Activation_Level\n")
					ifile_g.write("Change "+str(reactivation_index_stressfree)+"\n")
					ifile_g.write("layer:grouting_"+str(step)+"\n")
					ifile_g.write("mescape\n")
					for i in range (1,9):
						reactivation_index = reactivation_index + 2
						reactivation_index_stressfree = reactivation_index_stressfree + 2		


			else:
				print("ERROR: wrong number of segments")
				
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		ifile.close()
		ifile_g.close()
		ifile = open(self.working_dir+'material_condition_lining.bch','w')
		ifile.write("mescape\n")
		ifile.write("Data Materials NewMaterial Isotropic3D Lining_Concrete Isotropic3D Isotropic3D 2500.0kg/m^3 20000000000N/mm^2 0.3\n")
		ifile.write("mescape\n")

#		if self.params['lod']==1:
		ifile.write("mescape\n")
		ifile.write("Data Materials NewMaterial Isotropic3D Bolts Isotropic3D Isotropic3D 300.0kg/m^3 210000000000N/mm^2 0.3\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")

		for step in range(1, self.global_params['number_of_slices']+1):
			if no_segments==61:
				for i in range (1,8):
					ifile.write("Data Materials AssignMaterial Lining_Concrete Volumes\n")
					ifile.write("layer:lining_"+str(step)+"_"+str(i)+"\n")
					ifile.write("mescape\n")
				for i in range (1,8):
					ifile.write("Data Materials AssignMaterial Bolts Lines\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(i)+"\n")
					ifile.write("mescape\n")
			elif no_segments==71:
				for i in range (1,9):
					ifile.write("Data Materials AssignMaterial Lining_Concrete Volumes\n")
					ifile.write("layer:lining_"+str(step)+"_"+str(i)+"\n")
					ifile.write("mescape\n")
				for i in range (1,9):
					ifile.write("Data Materials AssignMaterial Bolts Lines\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(i)+"\n")
					ifile.write("mescape\n")
			else:
				print("ERROR: wrong number of segments")
				
			ifile.write("mescape\n")
			
		########ASIGN ELEMENT TYPE KINEMATIC LINEAR######################

		for step in range(1, self.global_params['number_of_slices']+1):
			if no_segments==61:
			##################*********LINING*********##################################
				for i in range (1,8):
					ifile.write("Data Conditions AssignCond VolumeElementType\n")
					ifile.write("Change Kinematic_Linear\n")
					ifile.write("1000.0kg/m^3\n")
					ifile.write("1.295kg/m^3\n")
					ifile.write("0.2\n")
					ifile.write("0.001m/s\n")
					ifile.write("0.00000032m/s\n")
					ifile.write("0.00000044m/s\n")
					ifile.write("0.0001m/s\n")
					ifile.write("0.0535\n")
					ifile.write("layer:lining_"+str(step)+"_"+str(i)+"\n")
					ifile.write("mescape\n")
			##################*********BOLTS*********##################################?????????????????????
				for i in range (1,8):
					ifile.write("Data Conditions AssignCond LineElementType\n")
					ifile.write("Change Beam\n")
					ifile.write("0.01m^2\n")
					ifile.write("0.00001m^4\n")
					ifile.write("0.00001m^4\n")
					ifile.write("0.00001m^4\n")
	#CHECK CoRRECT!				
					#ifile.write("0.0005m^4\n")
					#ifile.write("0.0005m^4\n")
					#ifile.write("0.0005m^4\n")				
					ifile.write("layer:bolts_"+str(step)+"_"+str(i)+"\n")
					ifile.write("mescape\n")
			elif no_segments==71:	
			##################*********LINING*********##################################
				for i in range (1,9):
					ifile.write("Data Conditions AssignCond VolumeElementType\n")
					ifile.write("Change Kinematic_Linear\n")
					ifile.write("1000.0kg/m^3\n")
					ifile.write("1.295kg/m^3\n")
					ifile.write("0.2\n")
					ifile.write("0.001m/s\n")
					ifile.write("0.00000032m/s\n")
					ifile.write("0.00000044m/s\n")
					ifile.write("0.0001m/s\n")
					ifile.write("0.0535\n")
					ifile.write("layer:lining_"+str(step)+"_"+str(i)+"\n")
					ifile.write("mescape\n")
			##################*********BOLTS*********##################################?????????????????????
				for i in range (1,9):
					ifile.write("Data Conditions AssignCond LineElementType\n")
					ifile.write("Change Beam\n")
					ifile.write("0.01m^2\n")
					ifile.write("0.00001m^4\n")
					ifile.write("0.00001m^4\n")
					ifile.write("0.00001m^4\n")
	#CHECK CoRRECT!				
					#ifile.write("0.0005m^4\n")
					#ifile.write("0.0005m^4\n")
					#ifile.write("0.0005m^4\n")				
					ifile.write("layer:bolts_"+str(step)+"_"+str(i)+"\n")
					ifile.write("mescape\n")
			else:
				print("ERROR: wrong number of segments")					
		#ASIGN MORTAR INDECIS
		if no_segments==61:
			if self.params['rs']=='True':
				slave_master_pairs=[[1,3],[2,1],[3,5],[4,2],[5,7],[6,4], [7,6]]
			else:
				slave_master_pairs=[[1,2],[2,4],[3,1],[4,6],[5,3],[6,7], [7,5]]
		elif no_segments==71:	
			slave_master_pairs=[[1,2],[2,4],[3,1],[4,6],[5,3],[6,8], [7,5], [8,7]]

		for i in range (0,len(slave_master_pairs)):
			ifile.write("Data Conditions AssignCond Surface_Mortar Change "+str(100+i+1)+" Master Option_automatic_axes\n")
			if no_segments==61:
				ifile.write("layer:lining_joint_master_"+str(slave_master_pairs[i][0])+"\n")
			elif no_segments==71:
				ifile.write("layer:lining_joint_master_"+str(slave_master_pairs[i][1])+"\n")
			ifile.write("mescape\n")
			ifile.write("Data Conditions AssignCond Surface_Mortar Change "+str(100+i+1)+" Slave Option_automatic_axes\n")
			if no_segments==61:
				ifile.write("layer:lining_joint_slave_"+str(slave_master_pairs[i][1])+"\n")
			elif no_segments==71:
				ifile.write("layer:lining_joint_slave_"+str(slave_master_pairs[i][0])+"\n")
			ifile.write("mescape\n")				
		for i in range(1, self.global_params['number_of_slices']):
			ifile.write("Data Conditions AssignCond Surface_Mortar Change "+str(1000+i)+" Master Option_automatic_axes\n")
			ifile.write("layer:lining_surface_"+str(i)+"\n")
			ifile.write("mescape\n")
			ifile.write("Data Conditions AssignCond Surface_Mortar Change "+str(1000+i)+" Slave Option_automatic_axes\n")
			ifile.write("layer:lining_surface_back_"+str(i+1)+"\n")
			ifile.write("mescape\n")			

		if self.soil.lod==1:
			for i in range(1,self.global_params['number_of_slices']+1):	
				ifile.write("mescape\n")
				ifile.write("Data Conditions AssignCond Distributed_Surface_Load\n")
				ifile.write("layer:lining_outer_surface_"+str(i)+"\n")
				ifile.write("mescape\n")
			for i in range(1,self.global_params['number_of_slices']+1):	
				ifile.write("mescape\n")
				ifile.write("Data Conditions AssignCond Surface_Bedding Change\n 1 0.0N/m^3\n 1 0.0N/m^3\n 1 0.0N/m^3\n")
				ifile.write("layer:lining_outer_surface_"+str(i)+"\n")
				ifile.write("mescape\n")
				

		ifile.close()		
		
		
		return
		

	def AddToSimScript_Lod1(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Lining SimScript LOD = 1'
		#initialize model
		ostream.write("##### INITIALIZE MODEL	#####\n")
		ostream.write("system_include = __import__(model_name+'_system_include')\n")
		ostream.write("model1 = system_include.Model(model_name+'_system',path+'/'+model_name+'_system.gid/')\n")
		ostream.write("model1.InitializeModel()\n")
		
		ostream.write("initial_reactivation_index = 0 \n")
		ostream.write("reactivation_index =0\n")
		ostream.write("reactivation_index_stressfree= 0\n")
		ostream.write("initial_face_index = 1\n")



		return
		
	def AddToSimScript_Lod2(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Lining SimScript LOD = 2'
		
		#initialize model
		ostream.write("##### INITIALIZE MODEL	#####\n")
		ostream.write("system_include = __import__(model_name+'_system_include')\n")
		ostream.write("model1 = system_include.Model(model_name+'_system',path+'/'+model_name+'_system.gid/')\n")
		ostream.write("model1.InitializeModel()\n")


		if self.soil.lod==1:
		
			params_soil = HelperMethods.ReadMaterialFile(self.global_params['model_path']+'/'+self.global_params['matfile']+'.dat')
			
			print(params_soil)
			ostream.write("import math\n")
			#ostream.write("time=1.0\n")
			E_soil_1=params_soil['E_soil_1']
			nu_soil_1=params_soil['nu_soil_1']
			ostream.write("K0="+str(params_soil['K0_1'])+"\n")
			ostream.write("ro="+str(params_soil['ro_soil_1'])+"\n")
			ostream.write("overburden="+str(self.global_params['overburden']/100.0)+"\n")
			ostream.write("k_spring="+str(E_soil_1/(self.global_params['excavation_radius']/100)*((1-nu_soil_1)/((1+nu_soil_1)*(1-2*nu_soil_1))))+"\n")
			ostream.write("radius=[0.0,0.0,0.0] \n")
			


			ostream.write("for step in range (1, number_of_slices+1):\n")
				
			ostream.write("	disp_x=(float(alignment[step][0]))\n")
			ostream.write("	disp_y=(float(alignment[step][1]))	\n")
			ostream.write("	delta_x=(disp_x-float(alignment[step-1][0]))\n")
			ostream.write("	delta_y=(disp_y-float(alignment[step-1][1]))\n")
			ostream.write("	alpha=math.atan(delta_y/delta_x)\n")
			ostream.write("	for node_id in model1.layer_nodes_sets['lining_outer_surface_'+str(step)]:\n")
			ostream.write("		node = model1.model_part.Nodes[node_id]\n")
			ostream.write("		x=node.X0\n")
			ostream.write("		y=node.Y0\n")
			ostream.write("		z=node.Z0\n")
			ostream.write("\n")		
							
			ostream.write("		point=[x,y,z]\n")
			ostream.write("		for i in range (0,3):\n")
			ostream.write("			radius[i]=float(alignment[step][i])-point[i]\n")

			ostream.write("		theta=math.atan2( radius[1], radius[2] )\n")

			ostream.write("		depth = node.Z\n")

			ostream.write("		pressure = -(overburden*9.81*ro- depth*9.81*ro)\n")
			ostream.write("		pressure_z=pressure *math.cos(-theta)\n")
			ostream.write("		pressure_y_1=pressure *math.sin(-theta)\n")
			ostream.write("		pressure_x=pressure_y_1*math.sin(alpha)\n")
			ostream.write("		pressure_y=pressure_y_1*math.cos(alpha)\n")
			ostream.write("\n")		
			ostream.write("		node.SetSolutionStepValue( FACE_LOAD_Z, -pressure_z )\n")
			ostream.write("		node.SetSolutionStepValue( FACE_LOAD_Y, 0.5*pressure_y )\n")
			ostream.write("		node.SetSolutionStepValue( FACE_LOAD_X, 0.5*pressure_x )\n")
					
			ostream.write("		eb_z=k_spring*math.cos(-theta)\n")
			ostream.write("		eb_y_1=k_spring*math.sin(-theta)\n")
			ostream.write("		eb_x=eb_y_1*math.sin(alpha)\n")
			ostream.write("		eb_y=eb_y_1*math.cos(alpha)\n")
					
			ostream.write("		node.SetSolutionStepValue(ELASTIC_BEDDING_STIFFNESS_X, abs(eb_x))\n")
			ostream.write("		node.SetSolutionStepValue(ELASTIC_BEDDING_STIFFNESS_Y, abs(eb_y))\n")
			ostream.write("		node.SetSolutionStepValue(ELASTIC_BEDDING_STIFFNESS_Z, abs(eb_z))\n")

		else:
		#ATTENTION: I ADDED +1 IN NEXT THREE LINES BEACUSE IN THE MAIN SCREEPT REACTIVATIN INDEX INSTEAD OF REACTIVATIN INDEX STRESSFREE IS USED!!!!
			ostream.write("initial_reactivation_index = "+str(self.initial_reactivation_index_stressfree-10+1)+"\n")
			ostream.write("reactivation_index = "+str(self.initial_reactivation_index+1)+"\n")
			ostream.write("reactivation_index_stressfree = "+str(self.initial_reactivation_index_stressfree+1)+"\n")
			ostream.write("initial_face_index = "+str(self.initial_face_index)+"\n")
			
	
			ostream.write("########################################################################################\n")
			ostream.write("#############	SETUP TYING LINKS PENALTY BETWEEN LINIG AND GROUTING	################\n")		
			ostream.write("tying_util = MortarTyingUtility\n")
			ostream.write("util = MortarTyingUtility()\n")
			ostream.write("mortar_links = util.SetupTyingLinkElementBased(model1.model_part, 10, 'tying_link_geometrical_linear_penalty', 'surface tying')\n")
			ostream.write("for cond in mortar_links:\n")
			ostream.write("	cond.SetValue(INITIAL_PENALTY, 1.0e11)\n")
			ostream.write("\n")	
			if self.tbm.lod>1:
				ostream.write("########################################################################################\n")
				ostream.write("#############	SETUP CONTACT LINKS PENALTY BETWEEN SHIELD AND SOIL	##################\n")		
				ostream.write("model1.solver.solver.contact_tying_indices = {}\n")
				ostream.write("model1.solver.solver.Parameters['penalty'] = {}\n")
				ostream.write("model1.solver.solver.Parameters['friction_coefficient'] = {}\n")
				ostream.write("model1.solver.solver.contact_tying_indices[1] = 'contact_link_kinematic_linear_penalty_no_linearized'\n")
				ostream.write("#model1.solver.solver.contact_tying_indices[1] = 'contact_link_kinematic_linear_penalty'\n")
				ostream.write("model1.solver.solver.mortar_contact_utility.SetValue(MAXIMAL_DETECTION_DISTANCE, 0.1)\n")
				ostream.write("model1.solver.solver.mortar_contact_utility.SetValue(GAP_TOLERANCE, 1.0e-10)\n")
				ostream.write("model1.solver.solver.Parameters['penalty'][1] = 1.0e9\n") #TODO: it would be more accurate if its 1.0e12
				ostream.write("model1.solver.solver.Parameters['friction_coefficient'][1] = 0.0\n")
				ostream.write("model1.solver.solver.Parameters['max_active_set_iter'] = 1\n")
			
				ostream.write("model1.solver.solver.Parameters['predict_local_point_method'] = 2\n")
				ostream.write("model1.solver.solver.Parameters['solution_strategy'] = 'solve active-set penalty'\n")
				ostream.write("model1.solver.solver.Parameters['integration_type'] = 'element based'\n")
				ostream.write("model1.solver.solver.Parameters['test_linearization'] = False\n")
				ostream.write("model1.solver.solver.Parameters['test_linearization_disp'] = 1.0e-7\n")
				ostream.write("model1.solver.solver.Parameters['test_linearization_tol'] = 1.0e-6\n")
		return
		
	def AddToSimScript_Lod3(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Lining SimScript LOD = 3'
		no_segments=int(self.global_params['segment_type'])
		#initialize model
		ostream.write("##### INITIALIZE MODEL	#####\n")
		ostream.write("system_include = __import__(model_name+'_system_include')\n")
		ostream.write("model1 = system_include.Model(model_name+'_system',path+'/'+model_name+'_system.gid/')\n")
		ostream.write("model1.InitializeModel()\n")
		ostream.write("\n")	
		ostream.write("segment_elements=[]\n")
		ostream.write("for i in range (1,number_of_slices+1):\n")
		if no_segments==61:
			ostream.write("	for j in range (1,8):\n")
		elif no_segments==71:
			ostream.write("	for j in range (1,9):\n")
		else:
			print("ERROR: segments number")
		#ostream.write("	for j in range (1,8):\n")
		ostream.write("		for element in model1.layer_sets['lining_'+str(i)+'_'+str(j)]:\n")
		ostream.write("			segment_elements.append(element)\n")
		ostream.write("\n")
		if self.soil.lod==1:
			ostream.write("beams_node_list=[]\n")
			ostream.write("for i in range (1,number_of_slices+1):\n")
			if no_segments==61:
				ostream.write("	for j in range (1,8):\n")
			elif no_segments==71:
				ostream.write("	for j in range (1,9):\n")
			else:
				print("ERROR: segments number")
			ostream.write("		for node in model1.layer_nodes_sets['bolts_'+str(i)+'_'+str(j)]:\n")
			ostream.write("			beams_node_list.append(node)\n")
			ostream.write("###############TYING BETWEEN BOLTS AND SEGMENTS#######################################\n")
			ostream.write("Epltu = EmbeddedNodePenaltyTyingUtility()\n")
			ostream.write("links1 = Epltu.SetUpTyingLinks( model1.model_part, beams_node_list, segment_elements )\n")
			ostream.write("for cond in links1:\n")
			ostream.write("	cond.SetValue(INITIAL_PENALTY, 1.0e11)\n")
			ostream.write("\n")	

		ostream.write("###################SETUP CONTACT LINKS PENALTY##########################################	\n")			
		ostream.write("model1.solver.solver.contact_tying_indices = {}\n")
		ostream.write("model1.solver.solver.Parameters['penalty'] = {}\n")
		ostream.write("model1.solver.solver.Parameters['friction_coefficient'] = {}\n")
		if no_segments==61:
			ostream.write("for i in range (1,8):\n")
		elif no_segments==71:
			ostream.write("for i in range (1,9):\n")
		else:
			print("ERROR: segments number")
		ostream.write("	model1.solver.solver.contact_tying_indices[100+i] = 'contact_link_kinematic_linear_penalty'\n")
		ostream.write("	model1.solver.solver.mortar_contact_utility.SetValue(MAXIMAL_DETECTION_DISTANCE, 0.1)\n")
		ostream.write("	model1.solver.solver.mortar_contact_utility.SetValue(GAP_TOLERANCE, 1.0e-10)\n")
		ostream.write("	model1.solver.solver.Parameters['penalty'][100+i] = 1.0e10\n")
		ostream.write("	model1.solver.solver.Parameters['friction_coefficient'][100+i] =0.0\n")
		ostream.write("\n")
		ostream.write("\n")

		ostream.write("for i in range (1,number_of_slices+1):\n")
		ostream.write("	model1.solver.solver.contact_tying_indices[1000+i] = 'contact_link_kinematic_linear_penalty'\n")
		ostream.write("	model1.solver.solver.mortar_contact_utility.SetValue(MAXIMAL_DETECTION_DISTANCE, 0.1)\n")
		ostream.write("	model1.solver.solver.mortar_contact_utility.SetValue(GAP_TOLERANCE, 1.0e-10)		\n")	
		ostream.write("	model1.solver.solver.Parameters['penalty'][1000+i] = 1.0e10\n")
		ostream.write("	model1.solver.solver.Parameters['friction_coefficient'][1000+i] =0.0\n")
		ostream.write("model1.solver.solver.Parameters['predict_local_point_method'] = 2\n")
		ostream.write("model1.solver.solver.Parameters['solution_strategy'] = 'solve active-set penalty'\n")
		ostream.write("model1.solver.solver.Parameters['integration_type'] = 'element based'\n")
		ostream.write("model1.solver.solver.Parameters['test_linearization'] = False\n")
		ostream.write("model1.solver.solver.Parameters['test_linearization_disp'] = 1.0e-7\n")
		ostream.write("model1.solver.solver.Parameters['test_linearization_tol'] = 1.0e-6\n")
		if self.soil.lod==1:
			ostream.write("model1.solver.solver.Parameters['max_active_set_iter'] = 10\n")
		else:
			ostream.write("model1.solver.solver.Parameters['max_active_set_iter'] = 1\n")
		ostream.write("\n")

		if self.soil.lod==1:
			###do something
			params_soil = HelperMethods.ReadMaterialFile(self.global_params['model_path']+'/'+self.global_params['matfile']+'.dat')
			
			print(params_soil)
			ostream.write("import math\n")
			#ostream.write("time=1.0\n")
			E_soil_1=params_soil['E_soil_1']
			nu_soil_1=params_soil['nu_soil_1']
			ostream.write("K0="+str(params_soil['K0_1'])+"\n")
			ostream.write("ro="+str(params_soil['ro_soil_1'])+"\n")
			ostream.write("overburden="+str(self.global_params['overburden']/100.0)+"\n")
			ostream.write("k_spring="+str(E_soil_1/(self.global_params['excavation_radius']/100)*((1-nu_soil_1)/((1+nu_soil_1)*(1-2*nu_soil_1))))+"\n")
			ostream.write("radius=[0.0,0.0,0.0]\n")
			ostream.write("for step in range (1, number_of_slices+1):\n")
			ostream.write("	disp_x=(float(alignment[step][0]))\n")
			ostream.write("	disp_y=(float(alignment[step][1]))	\n")
			ostream.write("	disp_z=(float(alignment[step][2]))	\n")
			ostream.write("	delta_x=(disp_x-float(alignment[step-1][0]))\n")
			ostream.write("	delta_y=(disp_y-float(alignment[step-1][1]))\n")
			ostream.write("	delta_z=(disp_z-float(alignment[step-1][2]))\n")
			ostream.write("	alpha=math.atan(delta_y/delta_x)\n")
			ostream.write("	gamma=math.atan(delta_z/delta_x)\n")
			ostream.write("	for node_id in model1.layer_nodes_sets['lining_outer_surface_'+str(step)]:\n")
			ostream.write("		node = model1.model_part.Nodes[node_id]\n")
			ostream.write("		x=node.X0\n")
			ostream.write("		y=node.Y0\n")
			ostream.write("		z=node.Z0\n")
			ostream.write("\n")		
							
			ostream.write("		point=[x,y,z]\n")
			ostream.write("		for i in range (0,3):\n")
			ostream.write("			radius[i]=float(alignment[step][i])-point[i]\n")

			ostream.write("		theta=math.atan2( radius[1], radius[2] )\n")

			ostream.write("		depth = node.Z\n")

			ostream.write("		pressure = -(overburden*9.81*ro- depth*9.81*ro)\n")
			ostream.write("		pressure_z=pressure *math.cos(-theta)\n")
			ostream.write("		pressure_y_1=pressure *math.sin(-theta)\n")
			ostream.write("		pressure_x=pressure_y_1*math.sin(alpha)\n")
			ostream.write("		pressure_y=pressure_y_1*math.cos(alpha)\n")
			ostream.write("\n")		
			ostream.write("		node.SetSolutionStepValue( FACE_LOAD_Z, -pressure_z )\n")
			ostream.write("		node.SetSolutionStepValue( FACE_LOAD_Y, 0.5*pressure_y )\n")
			ostream.write("		node.SetSolutionStepValue( FACE_LOAD_X, 0.5*pressure_x )\n")

			ostream.write("		eb_z_1=k_spring*math.cos(-theta)\n")			
			ostream.write("		eb_z=eb_z_1*math.cos(gamma)\n")
			ostream.write("		eb_y_1=k_spring*math.sin(-theta)\n")
			ostream.write("		eb_x=eb_y_1*math.sin(alpha) +eb_z_1*math.sin(gamma)\n")
			ostream.write("		eb_y=eb_y_1*math.cos(alpha)\n")
					
			ostream.write("		node.SetSolutionStepValue(ELASTIC_BEDDING_STIFFNESS_X, abs(eb_x))\n")
			ostream.write("		node.SetSolutionStepValue(ELASTIC_BEDDING_STIFFNESS_Y, abs(eb_y))\n")
			ostream.write("		node.SetSolutionStepValue(ELASTIC_BEDDING_STIFFNESS_Z, abs(eb_z))\n")		


		else:		
			ostream.write("initial_reactivation_index = "+str(self.initial_reactivation_index_stressfree-12)+"\n")
			ostream.write("reactivation_index = "+str(self.initial_reactivation_index-2)+"\n")
			ostream.write("reactivation_index_stressfree = "+str(self.initial_reactivation_index_stressfree-2)+"\n")
			ostream.write("initial_face_index = "+str(self.initial_face_index)+"\n")	
			#setup active bolt indices for bolt node list
			ostream.write("active_bolt_index=lining_offset\n")
			ostream.write("beams_node_list= []\n")
			ostream.write("for l in range (1,active_bolt_index+1):\n")
			#ostream.write("	for j in range (1,8):\n")
			if no_segments==61:
				ostream.write("	for j in range (1,8):\n")
			elif no_segments==71:
				ostream.write("	for j in range (1,9):\n")
			else:
				print("ERROR: segments number")
			ostream.write("		for node in model1.layer_nodes_sets['bolts_'+str(l)+'_'+str(j)]:\n")
			ostream.write("			beams_node_list.append(node)\n")
			#beam elements
			ostream.write("is_beam_elem=[]\n")                    
			ostream.write("for element in model1.model_part.Elements:\n")
			ostream.write("\n")
			ostream.write("	list_nodes_in = element.GetNodes()\n")
			ostream.write("	for nod in list_nodes_in:\n")
			ostream.write("		x= nod.Id\n")
			ostream.write("		if x in beams_node_list:\n")
			ostream.write("			is_beam_elem.append(element.Id)\n")
			ostream.write("\n")	
			ostream.write("	\n")
			ostream.write("###############TYING BETWEEN BOLTS AND SEGMENTS#######################################\n")
			ostream.write("Epltu = EmbeddedNodePenaltyTyingUtility()\n")
			ostream.write("links1 = Epltu.SetUpTyingLinks( model1.model_part, beams_node_list, segment_elements )\n")
			ostream.write("for cond in links1:\n")
			ostream.write("	cond.SetValue(INITIAL_PENALTY, 1.0e12)\n")
			ostream.write("\n")			
			
			###setup contact link tbm-soil
			ostream.write("model1.solver.solver.contact_tying_indices[1] = 'contact_link_kinematic_linear_penalty_no_linearized'\n")
			ostream.write("#model1.solver.solver.contact_tying_indices[1] = 'contact_link_kinematic_linear_penalty'\n")
			ostream.write("model1.solver.solver.mortar_contact_utility.SetValue(MAXIMAL_DETECTION_DISTANCE, 0.1)\n")
			ostream.write("model1.solver.solver.mortar_contact_utility.SetValue(GAP_TOLERANCE, 1.0e-10)\n")
			ostream.write("model1.solver.solver.Parameters['penalty'][1] = 1.0e9\n")	#TODO: it would be more accurate if its 1.0e12
			ostream.write("model1.solver.solver.Parameters['friction_coefficient'][1] = 0.0\n")
			ostream.write("########################################################################################\n")
			ostream.write("###################SETUP TYING LINKS PENALTY##########################################	\n")		
			ostream.write("tying_util = MortarTyingUtility\n")
			ostream.write("util = MortarTyingUtility()\n")
			ostream.write("mortar_links = util.SetupTyingLinkElementBased(model1.model_part, 10, 'tying_link_geometrical_linear_penalty', 'surface tying')\n")
			ostream.write("for cond in mortar_links:\n")
			ostream.write("	cond.SetValue(INITIAL_PENALTY, 1.0e11)\n")
			ostream.write("########################################################################################\n")			
		return
		
		
	def PrepareBoltModel( self ):
		sizeRatio = self.params['lining_outer_radius']/self.global_params['excavation_radius']
		#open batch file
		ifile = open( self.working_dir+self.global_params['model_name']+"_bolts.bch", 'w' )
		str1=os.getcwd()
		str2=str1.split('/')
		#print(str2)
		str1=str(str2[2].upper()+":/")
		for i in range (3, len(str2)):
			str1=str1+'/'+str(str2[i])
		#print(str1)

		angles_alpha=[]
		for i in range(1, len(self.coords)):
			delta_x=self.coords[i][0]-self.coords[i-1][0]
			delta_y=self.coords[i][1]-self.coords[i-1][1]
			alpha=math.atan(delta_y/delta_x)*180/math.pi
			angles_alpha.append(alpha)
#		angles_alpha_long=[]
#		for i in range(0, len(angles_alpha)):
#			angles_alpha_long.append((angles_alpha[i]+angles_alpha[i+1])/2.0)
		#print(angles_alpha)
		#print(angles_alpha*180/math.pi)
			
		no_segments= int(self.global_params['segment_type'])	
		
		ifile.write("mescape\n")
		if no_segments==61:
			ifile.write("Files Read "+str(str1)+"/gid_geometries/bolts_61.gid\n")
		elif no_segments==71:
			ifile.write("Files Read "+str(str1)+"/gid_geometries/bolts_71.gid\n")
		else:
			print("Error:segments")
		ifile.write("mescape\n")
		ifile.write("Files SaveAs "+self.working_dir+self.global_params['model_name']+"_bolts_model.gid\n")
		ifile.write("mescape\n")
		#scale outer surface
		ifile.write("Utilities Move Lines Scale\n")
		ifile.write("0,0,0\n")
		ifile.write(str(self.global_params['round_length'])+","+str((self.params['lining_outer_radius']+self.params['lining_inner_radius'])/2)+","+str((self.params['lining_outer_radius']+self.params['lining_inner_radius'])/2)+"\n")
		if no_segments==61:
			ifile.write(" 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\n")
		elif no_segments==71:
			ifile.write(" 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17\n")
		else:
			print("Error:segments")
		
		ifile.write("mescape\n")
		#move bolts
		ifile.write("Utilities Move Lines Translation\n")
		ifile.write("0,0,0\n")
		#I HAVE TO CORRECT THIS!!!
		ifile.write(str((self.coords[1][0]-self.coords[0][0]))+","+str(str((self.coords[1][1]-self.coords[0][1])))+","+str(str(self.coords[1][2]-self.coords[0][2]))+"\n")
		#ifile.write(str(self.global_params['round_length']/2)+",0,0\n")
		if no_segments==61:
			ifile.write(" 1 2 3 4 5 6 14\n")
		elif no_segments==71:
			ifile.write(" 1 2 3 4 5 6 14 16\n")
		else:
			print("Error:segments")
		
		ifile.write("mescape\n")
		ifile.write("Utilities Move Lines Translation\n")
		ifile.write("0,0,0\n")
		
		#ifile.write(str(self.global_params['round_length'])+",0,0\n")
		#I HAVE TO CORRECT THIS!!!
		delta_x0=self.coords[1][0]-self.coords[0][0]
		delta_y0=self.coords[1][1]-self.coords[0][1]
		delta_z0=self.coords[1][2]-self.coords[0][2]
		
		ifile.write(str((self.coords[2][0]-self.coords[1][0])/2+delta_x0)+","+str(str((self.coords[2][1]-self.coords[1][1])/2+delta_y0))+","+str(str((self.coords[2][2]-self.coords[1][2])/2+delta_z0))+"\n")
		if no_segments==61:
			ifile.write(" 7 8 9 10 11 12 13 15\n")
		elif no_segments==71:
			ifile.write(" 7 8 9 10 11 12 13 15 17\n")
		else:
			print("Error:segments")
		
		ifile.write("mescape\n")
		#coppy first line
		ifile.write("Utilities Copy lines Translation\n")
		ifile.write("0,0,0\n")
		#coords
		#ifile.write(str(self.global_params['round_length'])+",0,0\n")
		ifile.write(str(self.coords[1][0]-self.coords[0][0])+","+str(str(self.coords[1][1]-self.coords[0][1]))+","+str(str(self.coords[1][2]-self.coords[0][2]))+"\n")
		if no_segments==61:
			ifile.write("1 2 3 4 5 6 14\n")
		elif no_segments==71:
			ifile.write("1 2 3 4 5 6 14 16\n")
		else:
			print("Error:segments")
		ifile.write("mescape\n")        
		###################################################################################
		ifile.write("view layers ToUse\n")
		ifile.write("bolts_2_2\n escape escape\n")
		ifile.write("view layers entities\n")
		ifile.write("bolts_2_2\n")
		ifile.write("LowerEntities Lines\n")
		if no_segments==61:
			ifile.write("\n19\n")
		elif no_segments==71:
			# ifile.write("\n25\n")
			ifile.write("\n21\n")
		else:
			print("Error:segments")
		#ifile.write("\n19\n")
		ifile.write("mescape\n")
		###################################################################################        
		ifile.write("view layers ToUse\n")
		ifile.write("bolts_2_3\n escape escape\n")
		ifile.write("view layers entities\n")
		ifile.write("bolts_2_3\n")
		ifile.write("LowerEntities Lines\n")
		#ifile.write("surfaces\n 21 24\n")
		if no_segments==61:
			ifile.write("\n20\n")
		elif no_segments==71:
			# ifile.write("\n21\n")
			ifile.write("\n25\n")
		else:
			print("Error:segments")
		#ifile.write("\n20\n")
		ifile.write("mescape\n")
		###################################################################################    
		ifile.write("view layers ToUse\n")
		ifile.write("bolts_2_4\n escape escape\n")
		ifile.write("view layers entities\n")
		ifile.write("bolts_2_4\n")
		ifile.write("LowerEntities Lines\n")
		#ifile.write("surfaces\n 21 24\n")
		if no_segments==61:
			ifile.write("\n18\n")
		elif no_segments==71:
			# ifile.write("\n22\n")
			ifile.write("\n20\n")
		else:
			print("Error:segments")
		#ifile.write("\n18\n")
		ifile.write("mescape\n")
		###################################################################################    
		ifile.write("view layers ToUse\n")
		ifile.write("bolts_2_5\n escape escape\n")
		ifile.write("view layers entities\n")
		ifile.write("bolts_2_5\n")
		ifile.write("LowerEntities Lines\n")
		#ifile.write("surfaces\n 21 24\n")
		if no_segments==61:
			ifile.write("\n21\n")
		elif no_segments==71:
			# ifile.write("\n20\n")
			ifile.write("\n22\n")
		else:
			print("Error:segments")
		#ifile.write("\n21\n")
		ifile.write("mescape\n")
		###################################################################################    
		ifile.write("view layers ToUse\n")
		ifile.write("bolts_2_6\n escape escape\n")
		ifile.write("view layers entities\n")
		ifile.write("bolts_2_6\n")
		ifile.write("LowerEntities Lines\n")
		#ifile.write("surfaces\n 21 24\n")
		if no_segments==61:
			ifile.write("\n17\n")
		elif no_segments==71:
			# ifile.write("\n23\n")
			ifile.write("\n19\n")
		else:
			print("Error:segments")
		#ifile.write("\n17\n")
		ifile.write("mescape\n")
		###################################################################################  
		ifile.write("view layers ToUse\n")
		ifile.write("bolts_2_7\n escape escape\n")
		ifile.write("view layers entities\n")
		ifile.write("bolts_2_6\n")
		ifile.write("LowerEntities Lines\n")
		#ifile.write("surfaces\n 21 24\n")
		if no_segments==61:
			ifile.write("\n16 22\n")
		elif no_segments==71:
			# ifile.write("\n19\n")
			ifile.write("\n23\n")
		else:
			print("Error:segments")
		#ifile.write("\n16 22\n")
		ifile.write("mescape\n")
		###################################################################################  	
		if no_segments==71:
			###################################################################################    
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_2_8\n escape escape\n")
			ifile.write("view layers entities\n")
			ifile.write("bolts_2_8\n")
			ifile.write("LowerEntities Lines\n")
			ifile.write("\n18 24\n")
			ifile.write("mescape\n")
		###################################################################################  


		for step in range(1,(self.global_params['number_of_slices']-1)):
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_1"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_1"+"\n escape escape\n")
			#xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")

			if no_segments==61:
				ifile.write(" 10 13\n")
			elif no_segments==71:
				ifile.write(" 10 13\n")
			else:
				print("Error:segments")

			#ifile.write(" 10 13\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_2"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_2"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")

			if no_segments==61:
				ifile.write("19 9\n")
			elif no_segments==71:
#				ifile.write("17 25\n")
				ifile.write("21 9\n")
			else:
				print("Error:segments")
			#ifile.write(" 19 9\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_3"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_3"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
			if no_segments==61:
				ifile.write("20 11\n")
			elif no_segments==71:
				# ifile.write("21 9\n")
				ifile.write("17 25\n")
			else:
				print("Error:segments")
			#ifile.write(" 20 11\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_4"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_4"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
			if no_segments==61:
				ifile.write("18 8\n")
			elif no_segments==71:
				# ifile.write("11 22\n")
				ifile.write("8 20\n")
			else:
				print("Error:segments")
			#ifile.write(" 18 8\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_5"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_5"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
			if no_segments==61:
				ifile.write("21 12\n")
			elif no_segments==71:
				# ifile.write("8 20\n")
				ifile.write("11 22\n")
			else:
				print("Error:segments")
			#ifile.write(" 21 12\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_6"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_6"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
			if no_segments==61:
				ifile.write("7 17\n")
			elif no_segments==71:
				# ifile.write("23 12\n")
				ifile.write("7 19\n")
			else:
				print("Error:segments")
			#ifile.write(" 7 17\n")
			ifile.write("mescape\n")
			
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_7"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_7"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
			if no_segments==61:
				ifile.write("22 16 15\n")
			elif no_segments==71:
				# ifile.write("7 19\n")
				ifile.write("23 12\n")
			else:
				print("Error:segments")
			#ifile.write(" 22 16 15\n")
			ifile.write("mescape\n")
			
			
			if no_segments==71:		
				ifile.write("view layers new\n")
				ifile.write("bolts_"+str(step+2)+"_8"+"\n escape escape\n")
				ifile.write("view layers ToUse\n")
				ifile.write("bolts_"+str(step+2)+"_8"+"\n escape escape\n")
				xOffset = step*self.global_params['round_length']
				ifile.write("Utilities Copy lines Translation\n")
				ifile.write("0,0,0\n")
				ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
				ifile.write(" 15 18 24\n")
				ifile.write("mescape\n")			
			
		#convert all lines to NURBS
		ifile.write("Geometry Edit ConvToNurbsL\n")
		ifile.write("InvertSelection\n escape\n Yes\n")
		ifile.write("mescape\n") 
		#move complete_model_to position 0,0,0
		ifile.write("Utilities Move All Duplicate MaintainLayers Translation\n")
		ifile.write("0.0 0.0 0.0\n")
		ifile.write(str(self.coords[0][0])+" "+str(self.coords[0][1])+" "+str(self.coords[0][2])+"\n")
		ifile.write("InvertSelection\n")
		ifile.write("mescape\n")
		
		# rotate all based on alignment
		for step in range(1,(self.global_params['number_of_slices']+1)):
			if no_segments==61:
				for j in range (1,8):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]))+"\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]+1000.0))+"\n")
					ifile.write(str(angles_alpha[step-1])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")	
			elif no_segments==71:
				for j in range (1,9):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]))+"\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]+1000.0))+"\n")
					ifile.write(str(angles_alpha[step-1])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")	
			else:
				print("Error:segments")
		for step in range(1,(self.global_params['number_of_slices']+1)):
			if no_segments==61:
				for j in range (1,8):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str(self.coords[step-1][0])+","+str(str(self.coords[step-1][1]))+","+str(str(self.coords[step-1][2]))+"\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]))+"\n")
					ifile.write(str(self.rotations[step-1])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")
			elif no_segments==71:		
				for j in range (1,9):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str(self.coords[step-1][0])+","+str(str(self.coords[step-1][1]))+","+str(str(self.coords[step-1][2]))+"\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]))+"\n")
					ifile.write(str(self.rotations[step-1])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")	
			else:
				print("Error:segments")					
		ifile.write("Files Save\n")
		ifile.write("Quit\n")
		ifile.close()
			#shell.execute(self.modeller_path+'run_gid '+self.gid_path+" "+self.working_dir+self.params['name']+"_bolts.bch " +self.working_dir )
		self.gid_path='C:/Program Files/GiD/GiD 12.0.10/'
		subprocess.check_output([self.gid_path+'gid_offscreen.bat', '-offscreen', '-b', self.global_params['model_name'] + "_bolts.bch", self.global_params['model_name']], cwd=self.working_dir) # +self.working_dir )
		#self.InvokeGID(self.global_params['model_name'] + "_bolts.bch")
		
	def PrepareBoltModel1( self ):
		sizeRatio = self.params['lining_outer_radius']/self.global_params['excavation_radius']
		#open batch file
		ifile = open( self.working_dir+self.global_params['model_name']+"_bolts_trans.bch", 'w' )
		str1=os.getcwd()
		str2=str1.split('/')
		#print(str2)
		str1=str(str2[2].upper()+":/")
		for i in range (3, len(str2)):
			str1=str1+'/'+str(str2[i])
		#print(str1)

		angles_alpha=[]
		angles_gamma=[]
		for i in range(1, len(self.coords)):
			delta_x=self.coords[i][0]-self.coords[i-1][0]
			delta_y=self.coords[i][1]-self.coords[i-1][1]
			delta_z=self.coords[i][2]-self.coords[i-1][2]
			alpha=math.atan(delta_y/delta_x)*180/math.pi
			gamma=math.atan(delta_z/delta_x)*180/math.pi
			angles_alpha.append(alpha)
			angles_gamma.append(gamma)
		angles_alpha_long=[]
		angles_gamma_long=[]
		for i in range(0, len(angles_alpha)-1):
			angles_alpha_long.append((angles_alpha[i]+angles_alpha[i+1])/2.0)
			angles_gamma_long.append((angles_alpha[i]+angles_alpha[i+1])/2.0)
			
		no_segments= int(self.global_params['segment_type'])	
		
		ifile.write("mescape\n")
		if no_segments==61:
			if self.params['rs']== 'True':
				ifile.write("Files Read "+str(str1)+"/gid_geometries/bolts_61_rs_trans.gid\n")
			else:
				ifile.write("Files Read "+str(str1)+"/gid_geometries/bolts_61_trans.gid\n")
		elif no_segments==71:
			ifile.write("Files Read "+str(str1)+"/gid_geometries/bolts_71_trans.gid\n")
		else:
			print("Error:segments")
		ifile.write("mescape\n")
		ifile.write("Files SaveAs "+self.working_dir+self.global_params['model_name']+"_bolts_model_trans.gid\n")
		ifile.write("mescape\n")
		#scale outer surface
		ifile.write("Utilities Move Lines Scale\n")
		ifile.write("0,0,0\n")
		ifile.write(str(self.global_params['round_length'])+","+str((self.params['lining_outer_radius']+self.params['lining_inner_radius'])/2)+","+str((self.params['lining_outer_radius']+self.params['lining_inner_radius'])/2)+"\n")
		if no_segments==61:
			ifile.write(" 1 2 3 4 5 6 14\n")
		elif no_segments==71:
			ifile.write(" 1 2 3 4 5 6 14 16\n")
		else:
			print("Error:segments")
		
		ifile.write("mescape\n")
		#move bolts
		ifile.write("Utilities Move Lines Translation\n")
		ifile.write("0,0,0\n")
		#I HAVE TO CORRECT THIS!!!
		ifile.write(str((self.coords[1][0]-self.coords[0][0]))+","+str(str((self.coords[1][1]-self.coords[0][1])))+","+str(str(self.coords[1][2]-self.coords[0][2]))+"\n")
		#ifile.write(str(self.global_params['round_length']/2)+",0,0\n")
		if no_segments==61:
			ifile.write(" 1 2 3 4 5 6 14\n")
		elif no_segments==71:
			ifile.write(" 1 2 3 4 5 6 14 16\n")
		else:
			print("Error:segments")
		
		ifile.write("mescape\n")
		ifile.write("Utilities Move Lines Translation\n")
		ifile.write("0,0,0\n")
		
		#ifile.write(str(self.global_params['round_length'])+",0,0\n")
		
		ifile.write("mescape\n")


		for step in range(1,(self.global_params['number_of_slices'])):
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+1)+"_2"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+1)+"_2"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+1][0]-self.coords[1][0])+","+str(str(self.coords[step+1][1]-self.coords[1][1]))+","+str(str(self.coords[step+1][2]-self.coords[1][2]))+"\n")

			if no_segments==61:
				ifile.write("4\n")
			elif no_segments==71:
				ifile.write("4\n")
			else:
				print("Error:segments")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+1)+"_3"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+1)+"_3"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+1][0]-self.coords[1][0])+","+str(str(self.coords[step+1][1]-self.coords[1][1]))+","+str(str(self.coords[step+1][2]-self.coords[1][2]))+"\n")
			if no_segments==61:
				ifile.write("5\n")
			elif no_segments==71:
				ifile.write("16\n")
			else:
				print("Error:segments")
			#ifile.write(" 20 11\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+1)+"_4"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+1)+"_4"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+1][0]-self.coords[1][0])+","+str(str(self.coords[step+1][1]-self.coords[1][1]))+","+str(str(self.coords[step+1][2]-self.coords[1][2]))+"\n")
			if no_segments==61:
				ifile.write("3\n")
			elif no_segments==71:
				ifile.write("3\n")
			else:
				print("Error:segments")
			#ifile.write(" 18 8\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+1)+"_5"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+1)+"_5"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+1][0]-self.coords[1][0])+","+str(str(self.coords[step+1][1]-self.coords[1][1]))+","+str(str(self.coords[step+1][2]-self.coords[1][2]))+"\n")
			if no_segments==61:
				ifile.write("6\n")
			elif no_segments==71:
				ifile.write("5\n")
			else:
				print("Error:segments")
			#ifile.write(" 21 12\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+1)+"_6"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+1)+"_6"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+1][0]-self.coords[1][0])+","+str(str(self.coords[step+1][1]-self.coords[1][1]))+","+str(str(self.coords[step+1][2]-self.coords[1][2]))+"\n")
			if no_segments==61:
				ifile.write("2\n")
			elif no_segments==71:
				ifile.write("2\n")
			else:
				print("Error:segments")
			#ifile.write(" 7 17\n")
			ifile.write("mescape\n")
			
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+1)+"_7"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+1)+"_7"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			ifile.write(str(self.coords[step+1][0]-self.coords[1][0])+","+str(str(self.coords[step+1][1]-self.coords[1][1]))+","+str(str(self.coords[step+1][2]-self.coords[1][2]))+"\n")
			if no_segments==61:
				ifile.write("1 14\n")
			elif no_segments==71:
				ifile.write("6\n")
			else:
				print("Error:segments")
			#ifile.write(" 22 16 15\n")
			ifile.write("mescape\n")
			
			
			if no_segments==71:		
				ifile.write("view layers new\n")
				ifile.write("bolts_"+str(step+1)+"_8"+"\n escape escape\n")
				ifile.write("view layers ToUse\n")
				ifile.write("bolts_"+str(step+1)+"_8"+"\n escape escape\n")
				xOffset = step*self.global_params['round_length']
				ifile.write("Utilities Copy lines Translation\n")
				ifile.write("0,0,0\n")
				ifile.write(str(self.coords[step+1][0]-self.coords[1][0])+","+str(str(self.coords[step+1][1]-self.coords[1][1]))+","+str(str(self.coords[step+1][2]-self.coords[1][2]))+"\n")
				ifile.write(" 1 14\n")
				ifile.write("mescape\n")			
			
		#convert all lines to NURBS
		ifile.write("Geometry Edit ConvToNurbsL\n")
		ifile.write("InvertSelection\n escape\n Yes\n")
		ifile.write("mescape\n") 
		#move complete_model_to position 0,0,0
		ifile.write("Utilities Move All Duplicate MaintainLayers Translation\n")
		ifile.write("0.0 0.0 0.0\n")
		ifile.write(str(self.coords[0][0])+" "+str(self.coords[0][1])+" "+str(self.coords[0][2])+"\n")
		ifile.write("InvertSelection\n")
		ifile.write("mescape\n")
		
		# rotate all based on alignment
		for step in range(1,(self.global_params['number_of_slices']+1)):
			if no_segments==61:
				for j in range (1,8):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]))+"\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]+1000.0))+"\n")
					ifile.write(str(angles_alpha[step-1])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")	
				for j in range (1,8):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]))+"\n")
					ifile.write(str(self.coords[step][0]+1000.0)+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]))+"\n")
					ifile.write(str(angles_gamma[step-1])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")	
			elif no_segments==71:
				for j in range (1,9):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]))+"\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]+1000.0))+"\n")
					ifile.write(str(angles_alpha[step-1])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")	
			else:
				print("Error:segments")
		for step in range(1,(self.global_params['number_of_slices']+1)):
			if no_segments==61:
				for j in range (1,8):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str(self.coords[step-1][0])+","+str(str(self.coords[step-1][1]))+","+str(str(self.coords[step-1][2]))+"\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]))+"\n")
					ifile.write(str(self.rotations[step-1])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")
			elif no_segments==71:		
				for j in range (1,9):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str(self.coords[step-1][0])+","+str(str(self.coords[step-1][1]))+","+str(str(self.coords[step-1][2]))+"\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]))+"\n")
					ifile.write(str(self.rotations[step-1])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")	
			else:
				print("Error:segments")					
		ifile.write("Files Save\n")
		ifile.write("Quit\n")
		ifile.close()
			#shell.execute(self.modeller_path+'run_gid '+self.gid_path+" "+self.working_dir+self.params['name']+"_bolts.bch " +self.working_dir )
		self.gid_path='C:/Program Files/GiD/GiD 12.0.10/'
		subprocess.check_output([self.gid_path+'gid_offscreen.bat', '-offscreen', '-b', self.global_params['model_name'] + "_bolts_trans.bch", self.global_params['model_name']], cwd=self.working_dir) # +self.working_dir )
		
		
	################################
############################
############################	
		
		
		
		
		
		ifile = open( self.working_dir+self.global_params['model_name']+"_bolts_long.bch", 'w' )
		str1=os.getcwd()
		str2=str1.split('/')
		#print(str2)
		str1=str(str2[2].upper()+":/")
		for i in range (3, len(str2)):
			str1=str1+'/'+str(str2[i])
		#print(str1)

			
		no_segments= int(self.global_params['segment_type'])	
		
		ifile.write("mescape\n")
		if no_segments==61:
			if self.params['rs']== 'True':
				ifile.write("Files Read "+str(str1)+"/gid_geometries/bolts_61_rs_long.gid\n")
			else:
				ifile.write("Files Read "+str(str1)+"/gid_geometries/bolts_61_long.gid\n")
		elif no_segments==71:
			ifile.write("Files Read "+str(str1)+"/gid_geometries/bolts_71_long.gid\n")
		else:
			print("Error:segments")
		ifile.write("mescape\n")
		ifile.write("Files SaveAs "+self.working_dir+self.global_params['model_name']+"_bolts_model_long.gid\n")
		ifile.write("mescape\n")
		#scale outer surface
		ifile.write("Utilities Move Lines Scale\n")
		ifile.write("0,0,0\n")
		ifile.write(str(self.global_params['round_length'])+","+str((self.params['lining_outer_radius']+self.params['lining_inner_radius'])/2)+","+str((self.params['lining_outer_radius']+self.params['lining_inner_radius'])/2)+"\n")
		if no_segments==61:
			ifile.write(" 7 8 9 10 11 12 13 15\n")
		elif no_segments==71:
			ifile.write(" 7 8 9 10 11 12 13 15 17\n")
		else:
			print("Error:segments")
		
		ifile.write("mescape\n")
		#move bolts
		#ifile.write(str(self.global_params['round_length'])+",0,0\n")
		#move bolts
		ifile.write("Utilities Move Lines Translation\n")
		ifile.write("0,0,0\n")
		#I HAVE TO CORRECT THIS!!!
		
		
		
		
		delta_x0=self.coords[1][0]-self.coords[0][0]
		delta_y0=self.coords[1][1]-self.coords[0][1]
		delta_z0=self.coords[1][2]-self.coords[0][2]
		
		ifile.write(str((self.coords[2][0]-self.coords[1][0])/2.0+delta_x0)+","+str(str((self.coords[2][1]-self.coords[1][1])/2.0+delta_y0))+","+str(str((self.coords[2][2]-self.coords[1][2])/2.0+delta_z0))+"\n")
		if no_segments==61:
			ifile.write(" 7 8 9 10 11 12 13 15\n")
		elif no_segments==71:
			ifile.write(" 7 8 9 10 11 12 13 15 17\n")
		else:
			print("Error:segments")
		
		ifile.write("mescape\n")
		

		
		delta_x1=(self.coords[2][0]-self.coords[1][0])/2.0
		delta_y1=(self.coords[2][1]-self.coords[1][1])/2.0 
		delta_z1=(self.coords[2][2]-self.coords[1][2])/2.0


		for step in range(1,(self.global_params['number_of_slices']-1)):
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_1"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_1"+"\n escape escape\n")
			#xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			#ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
			#ifile.write(str((self.coords[step+1][0]-self.coords[1][0])+(self.coords[step+2][0]-self.coords[step+1][0])/2.0)+","+str(str(self.coords[step+1][1]-self.coords[1][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0))+","+str(str(self.coords[step+1][2]-self.coords[1][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0))+"\n")
			#ifile.write(str((self.coords[step+2][0]-self.coords[step+1][0])/2.0)+","+str(str((self.coords[step+2][1]-delta_y1)/2.0+(self.coords[step+1][1]-delta_y1)/2.0))+","+str(str((self.coords[step+2][2]-delta_z1)/2.0+(self.coords[step+1][2]-delta_z1)/2.0))+"\n")
			ifile.write(str(delta_x1+ self.coords[step+1][0]-self.coords[2][0]+(self.coords[step+2][0]-self.coords[step+1][0])/2.0) + "," + str(delta_y1 + self.coords[step+1][1]-self.coords[2][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0) + "," + str(delta_z1 + self.coords[step+1][2]-self.coords[2][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0)+"\n")

			
			if no_segments==61:
				ifile.write(" 10 13\n")
			elif no_segments==71:
				ifile.write(" 10 13\n")
			else:
				print("Error:segments")

			#ifile.write(" 10 13\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_2"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_2"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			#ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
			#ifile.write(str((self.coords[step+2][0]-delta_x1)/2.0+(self.coords[step+1][0]-delta_x0)/2.0)+","+str(str((self.coords[step+2][1]-delta_y1)/2.0+(self.coords[step+1][1]-delta_y0)/2.0))+","+str(str((self.coords[step+2][2]-delta_z1)/2.0+(self.coords[step+1][2]-delta_z0)/2.0))+"\n")
			#ifile.write(str((self.coords[step+1][0]-self.coords[1][0])+(self.coords[step+2][0]-self.coords[step+1][0])/2.0)+","+str(str(self.coords[step+1][1]-self.coords[1][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0))+","+str(str(self.coords[step+1][2]-self.coords[1][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0))+"\n")
			ifile.write(str(delta_x1+ self.coords[step+1][0]-self.coords[2][0]+(self.coords[step+2][0]-self.coords[step+1][0])/2.0) + "," + str(delta_y1 + self.coords[step+1][1]-self.coords[2][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0) + "," + str(delta_z1 + self.coords[step+1][2]-self.coords[2][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0)+"\n")

			
			if no_segments==61:
				ifile.write("9 \n")
			elif no_segments==71:
				ifile.write("9 \n")
			else:
				print("Error:segments")
			#ifile.write(" 19 9\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_3"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_3"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			#ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
			#ifile.write(str((self.coords[step+2][0]-delta_x1)/2.0+(self.coords[step+1][0]-delta_x0)/2.0)+","+str(str((self.coords[step+2][1]-delta_y1)/2.0+(self.coords[step+1][1]-delta_y0)/2.0))+","+str(str((self.coords[step+2][2]-delta_z1)/2.0+(self.coords[step+1][2]-delta_z0)/2.0))+"\n")
			#ifile.write(str((self.coords[step+1][0]-self.coords[1][0])+(self.coords[step+2][0]-self.coords[step+1][0])/2.0)+","+str(str(self.coords[step+1][1]-self.coords[1][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0))+","+str(str(self.coords[step+1][2]-self.coords[1][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0))+"\n")
			ifile.write(str(delta_x1+ self.coords[step+1][0]-self.coords[2][0]+(self.coords[step+2][0]-self.coords[step+1][0])/2.0) + "," + str(delta_y1 + self.coords[step+1][1]-self.coords[2][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0) + "," + str(delta_z1 + self.coords[step+1][2]-self.coords[2][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0)+"\n")

			
			if no_segments==61:
				ifile.write("11\n")
			elif no_segments==71:
				ifile.write(" 17\n")
			else:
				print("Error:segments")
			#ifile.write(" 20 11\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_4"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_4"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			#ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
			#ifile.write(str((self.coords[step+2][0]-delta_x1)/2.0+(self.coords[step+1][0]-delta_x0)/2.0)+","+str(str((self.coords[step+2][1]-delta_y1)/2.0+(self.coords[step+1][1]-delta_y0)/2.0))+","+str(str((self.coords[step+2][2]-delta_z1)/2.0+(self.coords[step+1][2]-delta_z0)/2.0))+"\n")
			#ifile.write(str((self.coords[step+1][0]-self.coords[1][0])+(self.coords[step+2][0]-self.coords[step+1][0])/2.0)+","+str(str(self.coords[step+1][1]-self.coords[1][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0))+","+str(str(self.coords[step+1][2]-self.coords[1][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0))+"\n")
			ifile.write(str(delta_x1+ self.coords[step+1][0]-self.coords[2][0]+(self.coords[step+2][0]-self.coords[step+1][0])/2.0) + "," + str(delta_y1 + self.coords[step+1][1]-self.coords[2][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0) + "," + str(delta_z1 + self.coords[step+1][2]-self.coords[2][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0)+"\n")

			
			if no_segments==61:
				ifile.write("8\n")
			elif no_segments==71:
				ifile.write("8 \n")
			else:
				print("Error:segments")
			#ifile.write(" 18 8\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_5"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_5"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			#ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
			#ifile.write(str((self.coords[step+2][0]-delta_x1)/2.0+(self.coords[step+1][0]-delta_x0)/2.0)+","+str(str((self.coords[step+2][1]-delta_y1)/2.0+(self.coords[step+1][1]-delta_y0)/2.0))+","+str(str((self.coords[step+2][2]-delta_z1)/2.0+(self.coords[step+1][2]-delta_z0)/2.0))+"\n")
			#ifile.write(str((self.coords[step+1][0]-self.coords[1][0])+(self.coords[step+2][0]-self.coords[step+1][0])/2.0)+","+str(str(self.coords[step+1][1]-self.coords[1][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0))+","+str(str(self.coords[step+1][2]-self.coords[1][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0))+"\n")
			ifile.write(str(delta_x1+ self.coords[step+1][0]-self.coords[2][0]+(self.coords[step+2][0]-self.coords[step+1][0])/2.0) + "," + str(delta_y1 + self.coords[step+1][1]-self.coords[2][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0) + "," + str(delta_z1 + self.coords[step+1][2]-self.coords[2][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0)+"\n")

			if no_segments==61:
				ifile.write("12\n")
			elif no_segments==71:
				ifile.write("11 \n")
			else:
				print("Error:segments")
			#ifile.write(" 21 12\n")
			ifile.write("mescape\n")
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_6"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_6"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			#ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
			#ifile.write(str((self.coords[step+2][0]-delta_x1)/2.0+(self.coords[step+1][0]-delta_x0)/2.0)+","+str(str((self.coords[step+2][1]-delta_y1)/2.0+(self.coords[step+1][1]-delta_y0)/2.0))+","+str(str((self.coords[step+2][2]-delta_z1)/2.0+(self.coords[step+1][2]-delta_z0)/2.0))+"\n")
			#ifile.write(str((self.coords[step+1][0]-self.coords[1][0])+(self.coords[step+2][0]-self.coords[step+1][0])/2.0)+","+str(str(self.coords[step+1][1]-self.coords[1][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0))+","+str(str(self.coords[step+1][2]-self.coords[1][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0))+"\n")
			ifile.write(str(delta_x1+ self.coords[step+1][0]-self.coords[2][0]+(self.coords[step+2][0]-self.coords[step+1][0])/2.0) + "," + str(delta_y1 + self.coords[step+1][1]-self.coords[2][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0) + "," + str(delta_z1 + self.coords[step+1][2]-self.coords[2][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0)+"\n")

			if no_segments==61:
				ifile.write("7\n")
			elif no_segments==71:
				ifile.write(" 7\n")
			else:
				print("Error:segments")
			#ifile.write(" 7 17\n")
			ifile.write("mescape\n")
			
		#------------------------------------------------------------------------
			ifile.write("view layers new\n")
			ifile.write("bolts_"+str(step+2)+"_7"+"\n escape escape\n")
			ifile.write("view layers ToUse\n")
			ifile.write("bolts_"+str(step+2)+"_7"+"\n escape escape\n")
			xOffset = step*self.global_params['round_length']
			ifile.write("Utilities Copy lines Translation\n")
			ifile.write("0,0,0\n")
			#ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
			#ifile.write(str((self.coords[step+2][0]-delta_x1)/2.0+(self.coords[step+1][0]-delta_x0)/2.0)+","+str(str((self.coords[step+2][1]-delta_y1)/2.0+(self.coords[step+1][1]-delta_y0)/2.0))+","+str(str((self.coords[step+2][2]-delta_z1)/2.0+(self.coords[step+1][2]-delta_z0)/2.0))+"\n")
			#ifile.write(str((self.coords[step+1][0]-self.coords[1][0])+(self.coords[step+2][0]-self.coords[step+1][0])/2.0)+","+str(str(self.coords[step+1][1]-self.coords[1][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0))+","+str(str(self.coords[step+1][2]-self.coords[1][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0))+"\n")
			ifile.write(str(delta_x1+ self.coords[step+1][0]-self.coords[2][0]+(self.coords[step+2][0]-self.coords[step+1][0])/2.0) + "," + str(delta_y1 + self.coords[step+1][1]-self.coords[2][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0) + "," + str(delta_z1 + self.coords[step+1][2]-self.coords[2][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0)+"\n")


			if no_segments==61:
				ifile.write("15 \n")
			elif no_segments==71:
				ifile.write(" 12 \n")
			else:
				print("Error:segments")
			#ifile.write(" 22 16 15\n")
			ifile.write("mescape\n")
			
			
			if no_segments==71:		
				ifile.write("view layers new\n")
				ifile.write("bolts_"+str(step+2)+"_8"+"\n escape escape\n")
				ifile.write("view layers ToUse\n")
				ifile.write("bolts_"+str(step+2)+"_8"+"\n escape escape\n")
				xOffset = step*self.global_params['round_length']
				ifile.write("Utilities Copy lines Translation\n")
				ifile.write("0,0,0\n")
				#ifile.write(str(self.coords[step+2][0]-self.coords[2][0])+","+str(str(self.coords[step+2][1]-self.coords[2][1]))+","+str(str(self.coords[step+2][2]-self.coords[2][2]))+"\n")
				#ifile.write(str((self.coords[step+2][0]-delta_x1)/2.0+(self.coords[step+1][0]-delta_x0)/2.0)+","+str(str((self.coords[step+2][1]-delta_y1)/2.0+(self.coords[step+1][1]-delta_y0)/2.0))+","+str(str((self.coords[step+2][2]-delta_z1)/2.0+(self.coords[step+1][2]-delta_z0)/2.0))+"\n")
				#ifile.write(str((self.coords[step+1][0]-self.coords[1][0])+(self.coords[step+2][0]-self.coords[step+1][0])/2.0)+","+str(str(self.coords[step+1][1]-self.coords[1][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0))+","+str(str(self.coords[step+1][2]-self.coords[1][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0))+"\n")
				ifile.write(str(delta_x1+ self.coords[step+1][0]-self.coords[2][0]+(self.coords[step+2][0]-self.coords[step+1][0])/2.0) + "," + str(delta_y1 + self.coords[step+1][1]-self.coords[2][1]+(self.coords[step+2][1]-self.coords[step+1][1])/2.0) + "," + str(delta_z1 + self.coords[step+1][2]-self.coords[2][2]+(self.coords[step+2][2]-self.coords[step+1][2])/2.0)+"\n")

				ifile.write(" 15 \n")
				ifile.write("mescape\n")			
			
			
			
		#convert all lines to NURBS
		ifile.write("Geometry Edit ConvToNurbsL\n")
		ifile.write("InvertSelection\n escape\n Yes\n")
		ifile.write("mescape\n") 
		#move complete_model_to position 0,0,0
		ifile.write("Utilities Move All Duplicate MaintainLayers Translation\n")
		ifile.write("0.0 0.0 0.0\n")
		ifile.write(str(self.coords[0][0])+" "+str(self.coords[0][1])+" "+str(self.coords[0][2])+"\n")
		ifile.write("InvertSelection\n")
		ifile.write("mescape\n")
		
		# rotate all based on alignment
		for step in range(2,(self.global_params['number_of_slices']+1)):
			if no_segments==61:
				for j in range (1,8):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str((self.coords[step-1][0]+self.coords[step][0])/2.0)+","+str(str((self.coords[step-1][1]+self.coords[step][1])/2.0))+","+str(str((self.coords[step-1][2]+self.coords[step][2])/2.0))+"\n")
					ifile.write(str((self.coords[step-1][0]+self.coords[step][0])/2.0)+","+str(str((self.coords[step-1][1]+self.coords[step][1])/2.0))+","+str(str((self.coords[step-1][2]+self.coords[step][2])/2.0+1000.0))+"\n")
					ifile.write(str(angles_alpha_long[step-2])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")	
				for j in range (1,8):
					ifile.write("mescape\n")
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str((self.coords[step-1][0]+self.coords[step][0])/2.0)+","+str(str((self.coords[step-1][1]+self.coords[step][1])/2.0))+","+str(str((self.coords[step-1][2]+self.coords[step][2])/2.0))+"\n")
					ifile.write(str((self.coords[step-1][0]+self.coords[step][0])/2.0+1000.0)+","+str(str((self.coords[step-1][1]+self.coords[step][1])/2.0))+","+str(str((self.coords[step-1][2]+self.coords[step][2])/2.0))+"\n")
					#print(angles_gamma_long[step-2])
					ifile.write(str(angles_gamma_long[step-2])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")	
			elif no_segments==71:
				for j in range (1,9):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str((self.coords[step-1][0]+self.coords[step][0])/2.0)+","+str(str((self.coords[step-1][1]+self.coords[step][1])/2.0))+","+str(str((self.coords[step-1][2]+self.coords[step][2])/2.0))+"\n")
					ifile.write(str((self.coords[step-1][0]+self.coords[step][0])/2.0)+","+str(str((self.coords[step-1][1]+self.coords[step][1])/2.0))+","+str(str((self.coords[step-1][2]+self.coords[step][2])/2.0+1000.0))+"\n")
					ifile.write(str(angles_alpha_long[step-2])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")					
			else:
				print("Error:segments")
		for step in range(2,(self.global_params['number_of_slices']+1)):
			if no_segments==61:
				for j in range (1,8):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str((self.coords[step-1][0]+self.coords[step][0])/2.0)+","+str(str((self.coords[step-1][1]+self.coords[step][1])/2.0))+","+str(str((self.coords[step-1][2]+self.coords[step][2])/2.0))+"\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]))+"\n")
					ifile.write(str(self.rotations[step-1])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")
			elif no_segments==71:		
				for j in range (1,9):
					ifile.write("mescape\n")		
					ifile.write("Utilities Move Lines MaintainLayers Rotation\n")
					ifile.write(str((self.coords[step-1][0]+self.coords[step][0])/2.0)+","+str(str((self.coords[step-1][1]+self.coords[step][1])/2.0))+","+str(str((self.coords[step-1][2]+self.coords[step][2])/2.0))+"\n")
					ifile.write(str(self.coords[step][0])+","+str(str(self.coords[step][1]))+","+str(str(self.coords[step][2]))+"\n")
					ifile.write(str(self.rotations[step-1])+"\n")
					ifile.write("layer:bolts_"+str(step)+"_"+str(j)+"\n")
					ifile.write("mescape\n")	
			else:
				print("Error:segments")					
		ifile.write("Files Save\n")
		ifile.write("Quit\n")
		ifile.close()
			#shell.execute(self.modeller_path+'run_gid '+self.gid_path+" "+self.working_dir+self.params['name']+"_bolts.bch " +self.working_dir )
		self.gid_path='C:/Program Files/GiD/GiD 12.0.10/'
		subprocess.check_output([self.gid_path+'gid_offscreen.bat', '-offscreen', '-b', self.global_params['model_name'] + "_bolts_long.bch", self.global_params['model_name']], cwd=self.working_dir) # +self.working_dir )
		
		
		ifile = open( self.working_dir+self.global_params['model_name']+"_bolts.bch", 'w' )
		str1=os.getcwd()
		str2=str1.split('/')
		#print(str2)
		str1=str(str2[2].upper()+":/")
		for i in range (3, len(str2)):
			str1=str1+'/'+str(str2[i])
			
		ifile.write("mescape\n")

		ifile.write("mescape\n")
		ifile.write("Files InsertGeom "+self.working_dir+self.global_params['model_name']+"_bolts_model_trans.gid\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Files InsertGeom "+self.working_dir+self.global_params['model_name']+"_bolts_model_long.gid\n")
		ifile.write("mescape\n")

		ifile.write("mescape\n")
		ifile.write("Files SaveAs "+self.working_dir+self.global_params['model_name']+"_bolts_model.gid\n")
		ifile.write("mescape\n")

		
		ifile.write("Files Save\n")
		ifile.write("Quit\n")
		ifile.close()
			#shell.execute(self.modeller_path+'run_gid '+self.gid_path+" "+self.working_dir+self.params['name']+"_bolts.bch " +self.working_dir )
		self.gid_path='C:/Program Files/GiD/GiD 12.0.10/'
		subprocess.check_output([self.gid_path+'gid_offscreen.bat', '-offscreen', '-b', self.global_params['model_name'] + "_bolts.bch", self.global_params['model_name']], cwd=self.working_dir) # +self.working_dir )

		

		#self.InvokeGID(self.global_params['model_name'] + "_bolts.bch")