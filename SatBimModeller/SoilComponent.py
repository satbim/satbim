import sys
import os
import math
import os.path
from ModelComponent import *
from LiningComponent import *

class SoilComponent(ModelComponent):
	
	# Constructor
	def __init__(self, global_params, working_dir):
		ModelComponent.__init__(self, global_params, working_dir)
		
		# Setup LOD handlers
		self.lod_prepare_handlers = [self.PrepareModel_Lod1, self.PrepareModel_Lod2, self.PrepareModel_Lod3]
		self.lod_script_handlers = [self.AddToSimScript_Lod1, self.AddToSimScript_Lod2, self.AddToSimScript_Lod3]
		
		# Define name
		self.component_name = "soil"
		
		# Dependencies
		self.lining = None
		self.building = None
		self.tbm = None
		
	def PrepareModel_Lod1(self, ostream):
		# Write model to .bch output file
		print 'Soil LOD = 1'
		
		return
	
	def PrepareModel_Lod2(self, ostream):
		# Write model to .bch output file
		print 'Soil LOD = 2'
		
		ostream.write("mescape\n")

		ostream.write("mescape\n")
		ostream.write("Files SaveAs " + self.working_dir+self.global_params['model_name'] + "_ground_model.gid\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Variables ImportTolerance "+str(self.global_params['round_length']/5.0)+" AutoImportTolerance 0\n")
		ostream.write("mescape\n")
		ostream.write("view layers new\n")
		ostream.write("ground"+"\n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("ground"+"\n escape escape\n")
		ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/excavation_soil/excavation_soil_volume.sat"+"\n ")
		ostream.write("mescape\n")
		# ostream.write("view layers new\n")
		# ostream.write("Top"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("Top\n escape escape\n")
		# ostream.write("Layers Entities\n")
		# ostream.write("Top\n")
		# ostream.write("LowerEntities Surfaces\n")
		# ostream.write(str(self.global_params['number_of_slices']+3)+"\n")
		# ostream.write("mescape\n")
		
		# ostream.write("view layers new\n")
		# ostream.write("Bottom"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("Bottom\n escape escape\n")
		# ostream.write("Layers Entities\n")
		# ostream.write("Bottom\n")
		# ostream.write("LowerEntities Surfaces\n")
		# ostream.write(str(self.global_params['number_of_slices']+4)+"\n")
		# ostream.write("mescape\n") 
		# ostream.write("view layers new\n")
		# ostream.write("Side_x"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("Side_x\n escape escape\n")
		# ostream.write("Layers Entities\n")
		# ostream.write("Side_x\n")
		# ostream.write("LowerEntities Surfaces\n")
		# ostream.write(str(self.global_params['number_of_slices']+6)+" "+str(self.global_params['number_of_slices']+8)+"\n")
		# ostream.write("mescape\n") 
		# ostream.write("view layers new\n")
		# ostream.write("Side_y"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("Side_y\n escape escape\n")
		# ostream.write("Layers Entities\n")
		# ostream.write("Side_y\n")
		# ostream.write("LowerEntities Surfaces\n")
		# ostream.write((str(self.global_params['number_of_slices']+5))+" "+str(self.global_params['number_of_slices']+7)+"\n")
		# ostream.write("mescape\n") 
		
		
		ostream.write("mescape\n") 
		ostream.write("view layers new\n")
		ostream.write("Excavation_surface"+"\n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("Excavation_surface\n escape escape\n")
		ostream.write("Layers Entities\n")
		ostream.write("Excavation_surface\n")
		ostream.write("LowerEntities Surfaces\n")
		
		
		ostream.write("mescape\n") 
		ostream.write("view layers new\n")
		ostream.write("surface \n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("surface \n escape escape\n")
		ostream.write("Layers Entities\n")
		ostream.write("surface \n")
		ostream.write("LowerEntities Surfaces\n")
		ostream.write(str(self.global_params['number_of_slices']+2)+" ")
		
		for i in range (1, self.global_params['number_of_slices']+1):
			ostream.write("mescape\n") 
			ostream.write("view layers new\n")
			ostream.write("excavation_surface_"+str(i)+"\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("excavation_surface_"+str(i)+"\n escape escape\n")
			ostream.write("Layers Entities\n")
			ostream.write("excavation_surface_"+str(i)+"\n")
			ostream.write("LowerEntities Surfaces\n")
			ostream.write(str(self.global_params['number_of_slices']+2-i)+" ")
		ostream.write("\n mescape\n") 

		ostream.write("mescape\n")
		ostream.write("Utilities Variables ImportTolerance "+str(self.global_params['round_length']/2.0)+" AutoImportTolerance 0\n")
		ostream.write("mescape\n")
		# ostream.write("mescape\n")
		# ostream.write("Layers ")	
		# ostream.write("Off Side_y ")	
		# ostream.write("Off Side_x ")	
		# ostream.write("Off Top ")	
		# ostream.write("Off Bottom \n")
		# ostream.write("mescape\n")
		#ostream.write("Meshing Structured Lines 4\n")
		#ostream.write("InvertSelection\n escape\n escape\n")
		#ostream.write("mescape\n")
		ostream.write("mescape\n")
######

		# ostream.write("Layers Off ground \n")
		# ostream.write("mescape\n")	
		
		##asigbn layer to all surfaces 
		# ostream.write("view layers new\n")
		# ostream.write("surf \n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("surf \n escape escape\n")
		
		
		##coppy first points
		# nos=self.global_params['number_of_slices']
		# ostream.write("Utilities Copy points Translation\n")
		# ostream.write("0,0,0\n")
		# ostream.write("5000,20000,0\n")
		# ostream.write("1 \n")
		# ostream.write("mescape\n")
		# ostream.write("Utilities Copy points Translation\n")
		# ostream.write("0,0,0\n")
		# ostream.write("-5000,20000,0\n")
		# ostream.write(str(nos+2)+" \n")
		# ostream.write("mescape\n")
		# ostream.write("Utilities Copy points Translation\n")
		# ostream.write("0,0,0\n")
		# ostream.write("0,-40000,0\n")
		# ostream.write(str(nos+2+8+1)+" "+ str(nos+2+8+2) +" \n")		
		# ostream.write("mescape\n")
		# ostream.write("Geometry Create Line Join\n")	
		# ostream.write(str(nos+2+8+1)+" "+ str(nos+2+8+2) +" \n escape\n")	
		# ostream.write(str(nos+2+8+1)+" "+ str(nos+2+8+3) +" \n escape\n")		
		# ostream.write(str(nos+2+8+3)+" "+ str(nos+2+8+4) +" \n escape\n")		
		# ostream.write(str(nos+2+8+2)+" "+ str(nos+2+8+4) +" \n escape\n")

		# ostream.write("mescape\n")
		# ostream.write("Geometry Create NurbsSurface Automatic 4\n")		
		# ostream.write("mescape\n")		
		# ostream.write("Geometry Create IntMultSurfs\n")
		# ostream.write("InvertSelection\n escape\n escape\n")
		# ostream.write("mescape\n")		
		# ostream.write("Geometry Delete Surface\n")
		# ostream.write("layer:surf \n")	
		# ostream.write("mescape\n")
		# ostream.write("Geometry Delete Line\n")	
		# ostream.write("InvertSelection\n escape\n escape\n")
		# ostream.write("mescape\n")	
		# ostream.write("Geometry Delete Point\n")	
		# ostream.write("InvertSelection\n escape\n escape\n")
		# ostream.write("mescape\n")	
		# ostream.write("mescape\n")	
		
		ostream.write("mescape\n")
		nos=self.global_params['number_of_slices']
		list_1=[]
		for i in range(1,nos+1):
			list_1.append(i*2+1)
		#list_1.append(nos+2)
		#list_1.append(nos+3)
		list_12=[]
		list_12.append(1)
		#list_12.append(nos+1)
		for i in range(1,nos+1):
			list_12.append(i*2)
			
		ostream.write("Meshing Structured Lines 1\n")
		nos=self.global_params['number_of_slices']
		for i in range (0,len(list_1)):
			ostream.write(str(list_1[i])+" ")
		ostream.write("\n")
		ostream.write("mescape\n")
		ostream.write("Meshing Structured Lines 12\n")

		for i in range (0,len(list_12)):
			ostream.write(str(list_12[i])+" ")
		ostream.write("\n")
		ostream.write("mescape\n")				



		ostream.write("mescape\n")
		ostream.write("Utilities Repair Yes\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Collapse Model Yes\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Repair Yes\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Collapse Model Yes\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		
		# ostream.write("mescape\n")
		# ostream.write("Layers ")	
		# ostream.write("On Side_y ")	
		# ostream.write("On Side_x ")	
		# ostream.write("On Top ")	
		# ostream.write("On Bottom \n")
		# ostream.write("mescape\n")
		ostream.write("Meshing\n Generate\n"+str(self.global_params['excavation_radius']*2)+" escape\n escape\n")		

		ostream.write("Files Save\n")
		ostream.write("Quit\n")	

		#########CREATE BACH FILE FOR MATERIAL PARAMETERS####		
		ifile = open(self.working_dir+'material_condition_soil.bch','w')
		ifile.write("mescape\n")  
		ifile.write("Data Materials NewMaterial UserDefined Soil UserDefined UserDefined\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")   


		ifile.write("Data Materials AssignMaterial Soil Volumes\n")
		ifile.write("layer:ground\n")
		ifile.write("mescape\n")
		
		
		#assign element types
		ifile.write("Data Conditions AssignCond VolumeElementType\n")
		if( self.global_params['account_for_water'] == "True" ):
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
		
		####asign boundary vonditions#######
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Group_Membership\n")
		ifile.write("Change Top\n")
		ifile.write("layer:Top\n")
		ifile.write("mescape\n")		
		ifile.write("mescape\n")
		ifile.write("Files Save\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond IsTop\n")
		ifile.write("UnAssign InvertSelection\n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		# ifile.write("Change 0 0 0 0 0 0 0 0 0 0 0 0\n")
		# ifile.write("layer:Top\n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		# ifile.write("Change 0 0 0 0 1 0 0 0 0 0 0 0\n")
		# ifile.write("layer:Bottom\n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		# ifile.write("Change 0 0 1 0 0 0 0 0 0 0 0 0\n")
		# ifile.write("layer:Side_y \n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		# ifile.write("Change 1 0 0 0 0 0 0 0 0 0 0 0\n")
		# ifile.write("layer:Side_x\n")
		ifile.write("mescape\n")		
		ifile.write("Data Conditions AssignCond IsTop\n")
		ifile.write("layer:surface\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Water_Pressure\n")
		ifile.write("UnAssign layer:surface\n")
		ifile.write("mescape\n")        

		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Files Save\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Group_Membership\n")
		ifile.write("Change surface\n")
		ifile.write("layer:surface\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Distributed_Surface_Load\n")
		ifile.write("layer:surface\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Files Save\n")
		
		#assign side boundary conditions
		ifile.write("*****TCL GetBoundary \n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond IsTop\n")
		ifile.write("UnAssign InvertSelection\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond IsTop\n")
		ifile.write("layer:surface\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Water_Pressure\n")
		ifile.write("Change 1 1.0\n")
		ifile.write("layer:surface\n")
		ifile.write("mescape\n")
		ifile.close()		
		return
		
	def PrepareModel_Lod3(self, ostream):
		# Write model to .bch output file
		#CHANGE OR CHECK HERE! NOT CONSISTANT FOR ALL GEOMTRIES
		print 'Soil LOD = 3'
		DIR= str(self.global_params['model_path'])+ "sat_files/excavation_soil"
		n_volumes=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
		
		ostream.write("mescape\n")

		ostream.write("mescape\n")
		ostream.write("Files SaveAs " + self.working_dir+self.global_params['model_name'] + "_ground_model.gid\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Variables ImportTolerance "+str(self.global_params['round_length']/5.0)+" AutoImportTolerance 0\n")
		for i in range (0, n_volumes):
			ostream.write("mescape\n")
			ostream.write("view layers new\n")
			ostream.write("ground_"+str(i)+"\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("ground_"+str(i)+"\n escape escape\n")
			ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/excavation_soil/excavation_soil_volume_"+str(i)+".sat"+"\n ")
			ostream.write("mescape\n")
		# ostream.write("view layers new\n")
		# ostream.write("Top"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("Top\n escape escape\n")
		# ostream.write("Layers Entities\n")
		# ostream.write("Top\n")
		# ostream.write("LowerEntities Surfaces\n")
		# ostream.write(str(self.global_params['number_of_slices']+3)+"\n")
		# ostream.write("mescape\n")
		
		# ostream.write("view layers new\n")
		# ostream.write("Bottom"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("Bottom\n escape escape\n")
		# ostream.write("Layers Entities\n")
		# ostream.write("Bottom\n")
		# ostream.write("LowerEntities Surfaces\n")
		# ostream.write(str(self.global_params['number_of_slices']+4)+"\n")
		# ostream.write("mescape\n") 
		# ostream.write("view layers new\n")
		# ostream.write("Side_x"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("Side_x\n escape escape\n")
		# ostream.write("Layers Entities\n")
		# ostream.write("Side_x\n")
		# ostream.write("LowerEntities Surfaces\n")
		# ostream.write(str(self.global_params['number_of_slices']+6)+" "+str(self.global_params['number_of_slices']+8)+"\n")
		# ostream.write("mescape\n") 
		# ostream.write("view layers new\n")
		# ostream.write("Side_y"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("Side_y\n escape escape\n")
		# ostream.write("Layers Entities\n")
		# ostream.write("Side_y\n")
		# ostream.write("LowerEntities Surfaces\n")
		# ostream.write((str(self.global_params['number_of_slices']+5))+" "+str(self.global_params['number_of_slices']+7)+"\n")
		# ostream.write("mescape\n") 
		
		
		ostream.write("mescape\n") 
		ostream.write("view layers new\n")
		ostream.write("Excavation_surface"+"\n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("Excavation_surface\n escape escape\n")
		ostream.write("Layers Entities\n")
		ostream.write("Excavation_surface\n")
		ostream.write("LowerEntities Surfaces\n")
		for i in range (0, self.global_params['number_of_slices']+1):
			ostream.write("mescape\n") 
			ostream.write("view layers new\n")
			ostream.write("excavation_surface_"+str(i)+"\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("excavation_surface_"+str(i)+"\n escape escape\n")
			ostream.write("Layers Entities\n")
			ostream.write("excavation_surface_"+str(i)+"\n")
			ostream.write("LowerEntities Surfaces\n")
			ostream.write(str(self.global_params['number_of_slices']+2-i)+" ")
		ostream.write("\n mescape\n") 

		ostream.write("mescape\n")
		ostream.write("Utilities Variables ImportTolerance "+str(self.global_params['round_length']/2.0)+" AutoImportTolerance 0\n")
		ostream.write("mescape\n")
		# ostream.write("mescape\n")
		# ostream.write("Layers ")	
		# ostream.write("Off Side_y ")	
		# ostream.write("Off Side_x ")	
		# ostream.write("Off Top ")	
		# ostream.write("Off Bottom \n")
		# ostream.write("mescape\n")
		#ostream.write("Meshing Structured Lines 4\n")
		#ostream.write("InvertSelection\n escape\n escape\n")
		#ostream.write("mescape\n")
		ostream.write("mescape\n")
######

		# ostream.write("Layers Off ground \n")
		# ostream.write("mescape\n")	
		
		##asigbn layer to all surfaces 
		# ostream.write("view layers new\n")
		# ostream.write("surf \n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("surf \n escape escape\n")
		
		
		##coppy first points
		# nos=self.global_params['number_of_slices']
		# ostream.write("Utilities Copy points Translation\n")
		# ostream.write("0,0,0\n")
		# ostream.write("5000,20000,0\n")
		# ostream.write("1 \n")
		# ostream.write("mescape\n")
		# ostream.write("Utilities Copy points Translation\n")
		# ostream.write("0,0,0\n")
		# ostream.write("-5000,20000,0\n")
		# ostream.write(str(nos+2)+" \n")
		# ostream.write("mescape\n")
		# ostream.write("Utilities Copy points Translation\n")
		# ostream.write("0,0,0\n")
		# ostream.write("0,-40000,0\n")
		# ostream.write(str(nos+2+8+1)+" "+ str(nos+2+8+2) +" \n")		
		# ostream.write("mescape\n")
		# ostream.write("Geometry Create Line Join\n")	
		# ostream.write(str(nos+2+8+1)+" "+ str(nos+2+8+2) +" \n escape\n")	
		# ostream.write(str(nos+2+8+1)+" "+ str(nos+2+8+3) +" \n escape\n")		
		# ostream.write(str(nos+2+8+3)+" "+ str(nos+2+8+4) +" \n escape\n")		
		# ostream.write(str(nos+2+8+2)+" "+ str(nos+2+8+4) +" \n escape\n")

		# ostream.write("mescape\n")
		# ostream.write("Geometry Create NurbsSurface Automatic 4\n")		
		# ostream.write("mescape\n")		
		# ostream.write("Geometry Create IntMultSurfs\n")
		# ostream.write("InvertSelection\n escape\n escape\n")
		# ostream.write("mescape\n")		
		# ostream.write("Geometry Delete Surface\n")
		# ostream.write("layer:surf \n")	
		# ostream.write("mescape\n")
		# ostream.write("Geometry Delete Line\n")	
		# ostream.write("InvertSelection\n escape\n escape\n")
		# ostream.write("mescape\n")	
		# ostream.write("Geometry Delete Point\n")	
		# ostream.write("InvertSelection\n escape\n escape\n")
		# ostream.write("mescape\n")	
		# ostream.write("mescape\n")	
		
		ostream.write("mescape\n")
		nos=self.global_params['number_of_slices']
		list_1=[]
		for i in range(2,nos+1):
			list_1.append(i)
		list_1.append(nos+2)
		list_1.append(nos+3)
		list_12=[]
		list_12.append(1)
		list_12.append(nos+1)
		for i in range(0,nos):
			list_12.append(nos+17+i)
			
		ostream.write("Meshing Structured Lines 1\n")
		nos=self.global_params['number_of_slices']
		for i in range (0,len(list_1)):
			ostream.write(str(list_1[i])+" ")
		ostream.write("\n")
		ostream.write("mescape\n")
		ostream.write("Meshing Structured Lines 12\n")

		for i in range (0,len(list_12)):
			ostream.write(str(list_12[i])+" ")
		ostream.write("\n")
		ostream.write("mescape\n")				



		ostream.write("mescape\n")
		ostream.write("Utilities Repair Yes\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Collapse Model Yes\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Repair Yes\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Collapse Model Yes\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		
		# ostream.write("mescape\n")
		# ostream.write("Layers ")	
		# ostream.write("On Side_y ")	
		# ostream.write("On Side_x ")	
		# ostream.write("On Top ")	
		# ostream.write("On Bottom \n")
		# ostream.write("mescape\n")
		ostream.write("Meshing\n Generate\n"+str(self.global_params['excavation_radius']*2)+" escape\n escape\n")		

		ostream.write("Files Save\n")
		ostream.write("Quit\n")	

		#########CREATE BACH FILE FOR MATERIAL PARAMETERS####
		ifile = open(self.working_dir+'material_condition_soil.bch','w')
		for i in range (0, n_volumes):		
			ifile.write("mescape\n")  
			ifile.write("Data Materials NewMaterial UserDefined Soil_"+str(i)+" UserDefined UserDefined\n")
			ifile.write("mescape\n")

			ifile.write("Data Materials AssignMaterial Soil_"+str(i)+" Volumes\n")
			ifile.write("layer:ground_"+str(i)+"\n")
			ifile.write("mescape\n")
		
		
		#assign element types
		for i in range (0, n_volumes):
			ifile.write("Data Conditions AssignCond VolumeElementType\n")
			if( self.global_params['account_for_water'] == "True" ):
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
			ifile.write("layer:ground_"+str(i)+"\n")
			ifile.write("mescape\n")
			
#		for i in range (0, self.global_params['number_of_slices']+1):
			
#			ifile.write("mescape\n")
#			ifile.write("View Layers Freeze\n")
#			ifile.write("excavation_surface_"+str(i)+"\n")
#			ifile.write("mescape\n")

			
		ifile.write("mescape\n")
		ifile.write("view layers new\n")
		ifile.write("ground \n escape escape\n")
		ifile.write("view layers ToUse\n")
		ifile.write("ground \n escape escape\n")
		for i in range (0, n_volumes):
			ifile.write("Layers Entities\n")
			ifile.write("ground\n")
			ifile.write("Volumes\n")
			ifile.write("layer:ground_"+str(i)+" ")
			#ifile.write("\n")		
			ifile.write("mescape\n")
		for i in range (0, n_volumes):
			ifile.write("Layers Entities\n")
			ifile.write("ground\n")
			ifile.write("LowerEntities Surfaces\n")
			ifile.write("layer:ground_"+str(i)+" ")
			#ifile.write("\n")		
			ifile.write("mescape\n")
		
#		for i in range (0, self.global_params['number_of_slices']+1):
#			ifile.write("mescape\n")
#			ifile.write("View Layers Unfreeze\n")
#			ifile.write("excavation_surface_"+str(i)+"\n")
#			ifile.write("mescape\n")
			
		
		####asign boundary vonditions#######
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Group_Membership\n")
		ifile.write("Change Top\n")
		ifile.write("layer:Top\n")
		ifile.write("mescape\n")		
		ifile.write("mescape\n")
		ifile.write("Files Save\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond IsTop\n")
		ifile.write("UnAssign InvertSelection\n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		# ifile.write("Change 0 0 0 0 0 0 0 0 0 0 0 0\n")
		# ifile.write("layer:Top\n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		# ifile.write("Change 0 0 0 0 1 0 0 0 0 0 0 0\n")
		# ifile.write("layer:Bottom\n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		# ifile.write("Change 0 0 1 0 0 0 0 0 0 0 0 0\n")
		# ifile.write("layer:Side_y \n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond Surface_Displacement\n")
		# ifile.write("Change 1 0 0 0 0 0 0 0 0 0 0 0\n")
		# ifile.write("layer:Side_x\n")
		ifile.write("mescape\n")		
		ifile.write("Data Conditions AssignCond IsTop\n")
		ifile.write("layer:Top\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Water_Pressure\n")
		ifile.write("UnAssign layer:Top\n")
		ifile.write("mescape\n")        

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
		ifile.write("mescape\n")
		ifile.write("Files Save\n")
		
		#assign side boundary conditions
		ifile.write("*****TCL GetBoundary \n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond IsTop\n")
		ifile.write("UnAssign InvertSelection\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond IsTop\n")
		ifile.write("layer:Top\n")
		ifile.write("mescape\n")
		ifile.write("Data Conditions AssignCond Surface_Water_Pressure\n")
		ifile.write("Change 1 1.0\n")
		ifile.write("layer:Top\n")
		ifile.write("mescape\n")
		ifile.close()	
		return
		
	def AddToSimScript_Lod1(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Soil SimScript LOD = 1'
		# ostream.write("##### INITIALIZE MODEL	#####\n")
		# ostream.write("system_include = __import__(model_name+'_system_include')\n")
		# ostream.write("model1 = system_include.Model(model_name+'_system',path+'/'+model_name+'_system.gid/')\n")

		# ostream.write("model1.InitializeModel()\n")
		
		return
		
	def AddToSimScript_Lod2(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Soil SimScript LOD = 2'
		# ostream.write("##### INITIALIZE MODEL	#####\n")
		# ostream.write("system_include = __import__(model_name+'_system_include')\n")
		# ostream.write("model1 = system_include.Model(model_name+'_system',path+'/'+model_name+'_system.gid/')\n")

		# ostream.write("model1.InitializeModel()\n")

		
		#ostream.write("##### COORDINATES OF TUNNEL ALIGMNET	#####\n")
		#self.coords = HelperMethods.ReadAlignmentFile(self.global_params['model_path']+'/input_files/')
		#ostream.write("disp_vector="+str(self.coords)+"\n")
		ostream.write("##### VOLUME LOSS #####\n")
		ostream.write("volume_loss ="+str(float(self.params['volume_loss']))+"\n")
		ostream.write("\n")		
		ostream.write("##### SET UP SOIL PROPERTIES #####\n")
		ostream.write("for element in model1.layer_sets['ground']:\n")
		ostream.write("	spu.SetMaterialProperties( model1.model_part, model1.model_part.Elements[element] )\n")
		ostream.write("for step in range(1,number_of_slices+1):\n")
		ostream.write("	excavation_layer = 'excavation_'+str(step)\n")
		ostream.write("	for element in model1.layer_sets[excavation_layer]:\n")
		ostream.write("		spu.SetMaterialProperties( model1.model_part, model1.model_part.Elements[element] )\n")

		ostream.write("print('##### TRANSFERRING INSITU STRESS #####')\n")
		ostream.write("vtu = VariableTransferUtility(MKLPardisoSolver())\n")
		#ostream.write("vtu.TransferPrestress( model_insitu.model_part, model1.model_part )\n")
		ostream.write("vtu.TransferPrestressIdentically( model_insitu.model_part, model1.model_part )\n")
		ostream.write("\n")
		ostream.write("if( account_for_water == True ):\n")
		ostream.write("	for node in model1.model_part.Nodes:\n")
		ostream.write("		if( node.Z > z_coord_of_groundwater_table ):\n")
		ostream.write("			node.Fix( WATER_PRESSURE )\n")
		ostream.write("\n")
		ostream.write("##reset to Zero in-situ stress in shield, lining and grouting\n")
		# if self.global_params['lod_tbm']>1:
		
	#	if self.global_params["write_to_databese"]==True:
		if self.building.lod==1:
			####add top nodes for the output
			ostream.write("tol=0.1	\n")
			ostream.write("top_nodes=[]\n")
			ostream.write("for node_id in model1.layer_nodes_sets['ground']:\n")
			#ostream.write("for node_id in model1.layer_nodes_sets['Top']:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			#CCHANGED recently this has to be checked!
			ostream.write("	if node.Z0>(ground_water_table-tol):\n")
			ostream.write("		top_nodes.append(node_id)\n")
			ostream.write("for node_id in model1.layer_nodes_sets['surface']:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")		
			ostream.write("	if node.Z0>(ground_water_table-tol):\n")
			ostream.write("		top_nodes.append(node_id)\n")
			####add top nodes for the builidng output	
			if self.building.lod>1:	
		
				ostream.write("x0b_min=10000000.0\n")
				ostream.write("x0b_max=-10000000.0\n")
				ostream.write("y0b_min=10000000.0\n")
				ostream.write("y0b_max=-10000000.0\n")
				ostream.write("z0b_max=-10000000.0\n")
				ostream.write("for node_id in model1.layer_nodes_sets['building']:\n")
				ostream.write("	node = model1.model_part.Nodes[node_id]\n")
				ostream.write("	if node.Z0>z0b_max:\n")
				ostream.write("		z0b_max=node.Z0\n")
				ostream.write("	if node.X0>x0b_max:\n")
				ostream.write("		x0b_max=node.X0\n")
				ostream.write("	elif node.X0<x0b_min:\n")
				ostream.write("		x0b_min=node.X0\n")
				ostream.write("	if node.Y0>y0b_max:\n")
				ostream.write("		y0b_max=node.Y0\n")
				ostream.write("	elif node.Y0<y0b_min:\n")
				ostream.write("		y0b_min=node.Y0\n")
				ostream.write("building_print=[]\n")
				ostream.write("for node_id in model1.layer_nodes_sets['building']:\n")
				ostream.write("	node = model1.model_part.Nodes[node_id]\n")
				ostream.write("	if node.Z0==z0b_max:\n")
				ostream.write("		if node.X0==x0b_max or  node.X0==x0b_min:\n")
				ostream.write("			if node.Y0==y0b_max or  node.Y0==y0b_min:\n")
				ostream.write("				building_print.append(node_id)\n")

			####add top nodes for the output for metamodel						
			ostream.write("x_r=5\n")
			ostream.write("y_r=5\n")
			ostream.write("del_x=(x0_max-x0_min)/float(x_r-1)\n")
			ostream.write("del_y=(y0_max-y0_min)/float(y_r-1)\n")
			ostream.write("points= [[[0 for i in xrange(2)] for i in xrange(y_r)] for i in xrange(x_r)]\n")
			ostream.write("for i in range (0,x_r):\n")
			ostream.write("	for j in range (0,y_r):\n")
			ostream.write("		points[i][j][0]=x0_min+i*del_x\n")
			ostream.write("		points[i][j][1]=y0_min+j*del_y\n")
			ostream.write("print_nodes=[[0 for i in xrange(y_r)]for i in xrange(x_r)]\n")
			#toleranc depends on mesh size
			ostream.write("tol_node=4.0\n")
			ostream.write("for node_id in top_nodes:\n")
			#ostream.write("for node_id in model1.layer_nodes_sets['Top']:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			ostream.write("	for i in range (0,x_r):\n")
			ostream.write("		if node.X0<(points[i][j][0]+tol_node) and node.X0>(points[i][j][0]-tol_node):\n")
			ostream.write("			for j in range (0,y_r):\n")
			ostream.write("				if node.Y0<(points[i][j][1]+tol_node) and node.Y0>(points[i][j][1]-tol_node):\n")
			ostream.write("					print_nodes[i][j]=node_id\n")
			ostream.write("top_nodes_print=[]\n")
			ostream.write("for i in range (0,x_r):\n")
			ostream.write("	for j in range (0,y_r):\n")
			ostream.write("		top_nodes_print.append(print_nodes[i][j])\n")		
			ostream.write("\n")					
			ostream.write("print(print_nodes)\n")
		
		
		ostream.write("element_list = []\n")
		if (self.tbm.lod > 1 and self.lining.lod > 1):
			ostream.write("for element in model1.layer_sets['shield']:\n")
			ostream.write("	if element in model1.model_part.Elements:\n")
			ostream.write("		element_list.append( element )\n")
		if self.building.lod > 1:
			ostream.write("for element in model1.layer_sets['building']:\n")
			ostream.write("	if element in model1.model_part.Elements:\n")
			ostream.write("		element_list.append( element )\n")
		if self.building.lod == 3:
			ostream.write("for element in model1.layer_sets['foundation']:\n")
			ostream.write("	if element in model1.model_part.Elements:\n")
			ostream.write("		element_list.append( element )\n")

		if self.lining.lod == 2:
			ostream.write("for step in range(1,number_of_slices+1):\n")
			ostream.write("	for element in model1.layer_sets['lining_'+str(step)]:\n")
			ostream.write("		if element in model1.model_part.Elements:\n")
			ostream.write("			element_list.append( element )\n")
			ostream.write("	for element in model1.layer_sets['grouting_'+str(step)]:\n")
			ostream.write("		if element in model1.model_part.Elements:\n")
			ostream.write("			element_list.append( element )\n")

		elif self.lining.lod == 3:	
			ostream.write("for step in range(1,number_of_slices+1):\n")
			ostream.write("	for j in range(1,(segment_number+1)):\n")				
			ostream.write("		for element in  model1.layer_sets['lining_'+str(step)+'_'+str(j)]:\n")
			ostream.write("			if element in model1.model_part.Elements:\n")
			ostream.write("				element_list.append( element )\n")		
			ostream.write("	for element in model1.layer_sets['grouting_'+str(step)]:\n")
			ostream.write("		if element in model1.model_part.Elements:\n")
			ostream.write("			element_list.append( element )\n")
		ostream.write("isu.ScalePrestress( model1.model_part, element_list, len(element_list), 0.0 )\n")
		
		#LOOK ABOVE IN NEW WAY OF SCALING PRESTRESSES
		# if self.tbm.lod > 1:
			# ostream.write("isu.ScalePrestress( model1.model_part, model1.layer_sets['shield'], len(model1.layer_sets['shield']), 0.0 )\n")

		# if self.lining.lod == 2:
			# ostream.write("for step in range(1,number_of_slices+1):\n")
			# ostream.write("	isu.ScalePrestress( model1.model_part, model1.layer_sets['lining_'+str(step)], len(model1.layer_sets['lining_'+str(step)]), 0.0 )\n")
			# ostream.write("	isu.ScalePrestress( model1.model_part, model1.layer_sets['grouting_'+str(step)], len(model1.layer_sets['grouting_'+str(step)]), 0.0 )\n")

		# if self.lining.lod == 3:
			# ostream.write("for step in range(1,number_of_slices+1):\n")
			# ostream.write("	for j in range(1,(segment_number+1)):\n")			
			# ostream.write("		isu.ScalePrestress( model1.model_part, model1.layer_sets['lining_'+str(step)+'_'+str(j)], len(model1.layer_sets['lining_'+str(step)+'_'+str(j)]), 0.0 )\n")
			# ostream.write("	isu.ScalePrestress( model1.model_part, model1.layer_sets['grouting_'+str(step)], len(model1.layer_sets['grouting_'+str(step)]), 0.0 )\n")

		# if self.building.lod > 1:
			# ostream.write("isu.ScalePrestress( model1.model_part, model1.layer_sets['building'], len(model1.layer_sets['building']), 0.0 )\n")

		# if self.building.lod == 3:
			# ostream.write("isu.ScalePrestress( model1.model_part, model1.layer_sets['foundation'], len(model1.layer_sets['foundation']), 0.0 )\n")
		# ostream.write("\n")
			
		if self.building.lod==1:	

			ostream.write("building_load=[]	\n")
			ostream.write("for node_id in top_nodes:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			ostream.write("	point[0]=node.X\n")
			ostream.write("	point[1]=node.Y\n")
			ostream.write("	if (InsidePointolygon(point, b_coords)==1):\n")
			ostream.write("		building_load.append(node_id)\n")		
			
			ostream.write("for node in building_load:\n")
			#ostream.write("	pressure = "+str(pressure)+"\n")
			ostream.write("	model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_Z,-building_pressure)\n")

			ostream.write("x0b_min=10000000.0\n")
			ostream.write("x0b_max=-10000000.0\n")
			ostream.write("y0b_min=10000000.0\n")
			ostream.write("y0b_max=-10000000.0\n")
			ostream.write("z0b_max=-10000000.0\n")
			ostream.write("for node_id in building_load:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			ostream.write("	if node.Z0>z0b_max:\n")
			ostream.write("		z0b_max=node.Z0\n")
			ostream.write("	if node.X0>x0b_max:\n")
			ostream.write("		x0b_max=node.X0\n")
			ostream.write("	elif node.X0<x0b_min:\n")
			ostream.write("		x0b_min=node.X0\n")
			ostream.write("	if node.Y0>y0b_max:\n")
			ostream.write("		y0b_max=node.Y0\n")
			ostream.write("	elif node.Y0<y0b_min:\n")
			ostream.write("		y0b_min=node.Y0\n")
			ostream.write("building_print=[]\n")
			ostream.write("for node_id in building_load:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			#ostream.write("	if node.Z0==z0b_max:\n")
			ostream.write("	if (node.X0==x0b_max) or  (node.X0==x0b_min) or (node.Y0==y0b_max) or  (node.Y0==y0b_min):\n")
			#ostream.write("			if node.Y0==y0b_max or  node.Y0==y0b_min:\n")
			ostream.write("				building_print.append(node_id)\n")
				
				
		if self.building.lod>1:
			ostream.write("z0_f=10000000\n")
			ostream.write("for node_id in model1.layer_nodes_sets['foundation']:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")				
			ostream.write("	if node.Z0<z0_f:\n")
			ostream.write("		z0_f=node.Z0\n")
			ostream.write("tol=0.1\n")
			ostream.write("foundation_nodes=[]\n")
			ostream.write("for node_id in model1.layer_nodes_sets['foundation']:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")	
			ostream.write("	if node.Z0<(z0_f+tol):\n")
			ostream.write("		foundation_nodes.append(node_id)\n")
			ostream.write("\n")		
			ostream.write("Epltu = EmbeddedNodePenaltyTyingUtility()\n")
			ostream.write("links1 = Epltu.SetUpTyingLinks( model1.model_part, foundation_nodes, model1.layer_sets['ground'] )\n")
			ostream.write("for cond in links1:\n")
			ostream.write("	cond.SetValue(INITIAL_PENALTY, 1.0e10)\n")
		if (self.tbm.lod>1 and self.lining.lod>1):
			ostream.write("shield_nodes=[]\n")
			ostream.write("for node in model1.layer_nodes_sets['shield']:\n")
			ostream.write("	if node in model1.model_part.Nodes:\n")
			ostream.write("		shield_nodes.append(node)\n")
			ostream.write("for node in model1.layer_nodes_sets['shield_outter_surface']:\n")
			ostream.write("	if node in model1.model_part.Nodes:\n")
			ostream.write("		shield_nodes.append(node)\n")
			
			ostream.write("\n")
		
		if self.lining.lod==1:
	
			ostream.write("delta_r=excavation_radius-excavation_radius*math.sqrt(1-volume_loss/100.0)\n")
			ostream.write("excavation_nodes=[]\n")

			ostream.write("for i in range (1, number_of_slices+1):\n")
			ostream.write("	for node in model1.layer_nodes_sets['excavation_surface_'+str(i)]:\n")
			ostream.write("		if node in model1.model_part.Nodes:\n")
			ostream.write("			excavation_nodes.append(node)\n")
						
			ostream.write("for node_id in excavation_nodes:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			ostream.write("	node.Fix(DISPLACEMENT_Z)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_Z, 0.0)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_EINS_Z, 0.0)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_NULL_Z, 0.0)\n")
			ostream.write("	node.Fix(DISPLACEMENT_X)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_X, 0.0)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_EINS_X, 0.0)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_NULL_X, 0.0)\n")
			ostream.write("	node.Fix(DISPLACEMENT_Y)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_Y, 0.0)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_EINS_Y, 0.0)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_NULL_Y, 0.0)\n")



			
		ostream.write("print('##### ASSIGN HYDROSTATIC PORE PRESSURE #####')\n")
		ostream.write("#Prescribe Hydrostratic Pressure\n")
		ostream.write("free_node_list_water1 = []\n")
		ostream.write("free_node_list_air1 = []\n")
		ostream.write("model1.FixPressureNodes(free_node_list_water1, free_node_list_air1)\n")
		ostream.write("\n")

		ostream.write("print('##### APPLY INSITU STRESS INCREMENTAL #####')\n")
		ostream.write("time = 100.0\n")
		ostream.write("delta_time = 180.0\n")
		ostream.write("\n")

		ostream.write("if( account_for_water == True ):\n")
		ostream.write("	model1.ApplyInsituWaterPressure(free_node_list_water1, free_node_list_air1, z_coord_of_groundwater_table, 9.81)\n")
		ostream.write("	model1.SetReferenceWaterPressure()\n")
		
		ostream.write("print '######## DO THE FIRST STEP #############'\n")
		ostream.write("heading_face_pressure = support_pressure\n")
		ostream.write("heading_face_gradient = support_gradient\n")
		ostream.write("for node in model1.node_groups['heading_face_'+str(initial_face_index)]:\n")
		ostream.write("	initial_pressure = heading_face_pressure\n")
		#ostream.write("	depth = model1.model_part.Nodes[node].Z\n")
		ostream.write("	depth = model1.model_part.Nodes[node].Z\n")
		ostream.write("	pressure = initial_pressure-depth*heading_face_gradient\n")
		ostream.write("	model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,pressure)\n")
		ostream.write("lining_face_index= "+str(self.global_params['lining_offset'])+"\n")
		if self.lining.lod>1: 
			ostream.write("for node in model1.layer_nodes_sets['lining_surface_'+str(lining_face_index)]:\n")
			ostream.write("	initial_pressure = heading_face_pressure\n")
			ostream.write("	depth = model1.model_part.Nodes[node].Z\n")
			ostream.write("	pressure = initial_pressure-depth*heading_face_gradient\n")
			ostream.write("	model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,-pressure)     	\n")
			ostream.write("	if( account_for_water == True ):\n")
			ostream.write("		model1.model_part.Nodes[node].Fix(WATER_PRESSURE)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE,pressure)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_NULL,pressure)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_EINS,pressure)\n")
		
		if (self.tbm.lod>1 and self.lining.lod>1):
			ostream.write("for node in shield_nodes:\n")
			ostream.write("	if node in model1.model_part.Nodes:\n")
			ostream.write("		model1.model_part.Nodes[node].Fix(DISPLACEMENT_X)\n")
			ostream.write("		model1.model_part.Nodes[node].Fix(DISPLACEMENT_Y)\n")
			ostream.write("		model1.model_part.Nodes[node].Fix(DISPLACEMENT_Z)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_X, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_EINS_X, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_NULL_X, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_Y, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_EINS_Y, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_NULL_Y, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_Z, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_EINS_Z, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_NULL_Z, 0.0)\n")
		ostream.write("tol = 0.1\n")
		ostream.write("for node in model1.model_part.Nodes:\n")
		ostream.write("	if node.Z0  < z0 +tol:\n")
		ostream.write("		node.Fix(DISPLACEMENT_Z)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_Z, 0.0)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_EINS_Z, 0.0)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_NULL_Z, 0.0)\n")
		#ostream.write("	if abs(node.X0)> x0-tol:\n")
		ostream.write("	if (node.X0> (x0_max-tol)) or (node.X0< (x0_min+tol)):\n")
		ostream.write("		node.Fix(DISPLACEMENT_X)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_X, 0.0)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_EINS_X, 0.0)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_NULL_X, 0.0)\n")
		#ostream.write("	if abs(node.Y0)>y0-tol:\n")
		ostream.write("	if (node.Y0> (y0_max-tol)) or (node.Y0< (y0_min+tol)):\n")
		ostream.write("		node.Fix(DISPLACEMENT_Y)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_Y, 0.0)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_EINS_Y, 0.0)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_NULL_Y, 0.0)\n")
		
				
		ostream.write("###########################################SOLVE FOR THE FORST TIME################################\n")
		ostream.write("###################################################################################################\n")
		ostream.write("deactivation_index=0\n")
		ostream.write("model1.Solve( time, 0, deactivation_index, initial_reactivation_index, reactivation_index)\n")
		ostream.write("model1.WriteOutput( time )		\n")
		ostream.write("\n")
		
		ostream.write("if( account_for_water == True ):\n")
		ostream.write("	model1.FreePressureNodes( free_node_list_water1, free_node_list_air1) \n") 
		ostream.write("\n")
		ostream.write("time=time+delta_time\n")
		ostream.write("model1.Solve( time, 0, deactivation_index, initial_reactivation_index, reactivation_index)\n")
		ostream.write("model1.WriteOutput( time )		\n")
		
		#this is only for print
		if self.global_params["write_to_databese"]==True:
			ostream.write("#INITIAL BUILDING DISPLACEMENT\n")
			ostream.write("builidng_init=[[0,0,0]]*len(building_print)	\n")
			ostream.write("i=0\n")
			ostream.write("for node_id in building_print:\n")
			ostream.write("	node=model1.model_part.Nodes[node_id]\n")
			ostream.write("	builidng_init[i][0] = node.GetSolutionStepValue(DISPLACEMENT_X)\n")
			ostream.write("	builidng_init[i][1] = node.GetSolutionStepValue(DISPLACEMENT_Y)\n")
			ostream.write("	builidng_init[i][2] = node.GetSolutionStepValue(DISPLACEMENT_Z)\n")
			ostream.write("	i=i+1\n")
		ostream.write("delta_time_advance = time_advance\n")
		ostream.write("delta_time_downtime = time_ring_construction\n")
		ostream.write("one_ring= round_length\n")
		ostream.write("move_steps= move_steps_per_round_length\n")
		ostream.write("exc_steps= steps_per_down_time\n")
		ostream.write("move_delta_time= delta_time_advance/float(move_steps)\n")
		ostream.write("exc_delta_time= delta_time_downtime/float(exc_steps)\n")
		ostream.write("face_index = initial_face_index\n")
		ostream.write("grouting_surface_index = initial_grouting_surface_index\n")
		ostream.write("\n")		
		if self.lining.lod==1:			
			ostream.write("for node_id in excavation_nodes:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			ostream.write("	node.Free(DISPLACEMENT_Z)\n")
			ostream.write("	node.Free(DISPLACEMENT_X)\n")
			ostream.write("	node.Free(DISPLACEMENT_Y)\n")

		


		return
		
	def AddToSimScript_Lod3(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Soil SimScript LOD = 3'


		
		#ostream.write("##### COORDINATES OF TUNNEL ALIGMNET	#####\n")
		#self.coords = HelperMethods.ReadAlignmentFile(self.global_params['model_path']+'/input_files/')
		#ostream.write("disp_vector="+str(self.coords)+"\n")
		ostream.write("##### VOLUME LOSS #####\n")
		ostream.write("volume_loss ="+str(float(self.params['volume_loss']))+"\n")
		ostream.write("\n")		
		ostream.write("##### SET UP SOIL PROPERTIES #####\n")
		ostream.write("for element in model1.layer_sets['ground']:\n")
		ostream.write("	spu.SetMaterialProperties( model1.model_part, model1.model_part.Elements[element] )\n")
		ostream.write("for step in range(1,number_of_slices+1):\n")
		ostream.write("	excavation_layer = 'excavation_'+str(step)\n")
		ostream.write("	for element in model1.layer_sets[excavation_layer]:\n")
		ostream.write("		spu.SetMaterialProperties( model1.model_part, model1.model_part.Elements[element] )\n")

		ostream.write("print('##### TRANSFERRING INSITU STRESS #####')\n")
		ostream.write("vtu = VariableTransferUtility(MKLPardisoSolver())\n")
		#ostream.write("vtu.TransferPrestress( model_insitu.model_part, model1.model_part )\n")
		ostream.write("vtu.TransferPrestressIdentically( model_insitu.model_part, model1.model_part )\n")
		ostream.write("\n")
		ostream.write("if( account_for_water == True ):\n")
		ostream.write("	for node in model1.model_part.Nodes:\n")
		ostream.write("		if( node.Z > z_coord_of_groundwater_table ):\n")
		ostream.write("			node.Fix( WATER_PRESSURE )\n")
		ostream.write("\n")
		ostream.write("##reset to Zero in-situ stress in shield, lining and grouting\n")
		# if self.global_params['lod_tbm']>1:
		
		####add top nodes for the output
		ostream.write("tol=0.1	\n")
		ostream.write("top_nodes=[]\n")
		ostream.write("for node_id in model1.layer_nodes_sets['ground']:\n")
		#ostream.write("for node_id in model1.layer_nodes_sets['Top']:\n")
		ostream.write("	node = model1.model_part.Nodes[node_id]\n")
		ostream.write("	if node.Z0>(ground_water_table-tol):\n")
		ostream.write("		top_nodes.append(node_id)\n")
		
		####add top nodes for the builidng output	
		if self.building.lod>2:	
	
			ostream.write("x0b_min=10000000.0\n")
			ostream.write("x0b_max=-10000000.0\n")
			ostream.write("y0b_min=10000000.0\n")
			ostream.write("y0b_max=-10000000.0\n")
			ostream.write("z0b_max=-10000000.0\n")
			ostream.write("for node_id in model1.layer_nodes_sets['building']:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			ostream.write("	if node.Z0>z0b_max:\n")
			ostream.write("		z0b_max=node.Z0\n")
			ostream.write("	if node.X0>x0b_max:\n")
			ostream.write("		x0b_max=node.X0\n")
			ostream.write("	elif node.X0<x0b_min:\n")
			ostream.write("		x0b_min=node.X0\n")
			ostream.write("	if node.Y0>y0b_max:\n")
			ostream.write("		y0b_max=node.Y0\n")
			ostream.write("	elif node.Y0<y0b_min:\n")
			ostream.write("		y0b_min=node.Y0\n")
			ostream.write("building_print=[]\n")
			ostream.write("for node_id in model1.layer_nodes_sets['building']:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			ostream.write("	if node.Z0==z0b_max:\n")
			ostream.write("		if node.X0==x0b_max or  node.X0==x0b_min:\n")
			ostream.write("			if node.Y0==y0b_max or  node.Y0==y0b_min:\n")
			ostream.write("				building_print.append(node_id)\n")

		

		####add top nodes for the output for metamodel						
		ostream.write("x_r=5\n")
		ostream.write("y_r=5\n")
		ostream.write("del_x=(x0_max-x0_min)/float(x_r-1)\n")
		ostream.write("del_y=(y0_max-y0_min)/float(y_r-1)\n")
		ostream.write("points= [[[0 for i in xrange(2)] for i in xrange(y_r)] for i in xrange(x_r)]\n")
		ostream.write("for i in range (0,x_r):\n")
		ostream.write("	for j in range (0,y_r):\n")
		ostream.write("		points[i][j][0]=x0_min+i*del_x\n")
		ostream.write("		points[i][j][1]=y0_min+j*del_y\n")
		ostream.write("print_nodes=[[0 for i in xrange(y_r)]for i in xrange(x_r)]\n")
		#toleranc depends on mesh size
		ostream.write("tol_node=4.0\n")
		ostream.write("for node_id in top_nodes:\n")
		#ostream.write("for node_id in model1.layer_nodes_sets['Top']:\n")
		ostream.write("	node = model1.model_part.Nodes[node_id]\n")
		ostream.write("	for i in range (0,x_r):\n")
		ostream.write("		if node.X0<(points[i][j][0]+tol_node) and node.X0>(points[i][j][0]-tol_node):\n")
		ostream.write("			for j in range (0,y_r):\n")
		ostream.write("				if node.Y0<(points[i][j][1]+tol_node) and node.Y0>(points[i][j][1]-tol_node):\n")
		ostream.write("					print_nodes[i][j]=node_id\n")
		ostream.write("top_nodes_print=[]\n")
		ostream.write("for i in range (0,x_r):\n")
		ostream.write("	for j in range (0,y_r):\n")
		ostream.write("		top_nodes_print.append(print_nodes[i][j])\n")		
		ostream.write("\n")					
		ostream.write("print(print_nodes)\n")
		
		
		ostream.write("element_list = []\n")
		if (self.tbm.lod > 1 and self.lining.lod > 1):
			ostream.write("for element in model1.layer_sets['shield']:\n")
			ostream.write("	if element in model1.model_part.Elements:\n")
			ostream.write("		element_list.append( element )\n")
		if self.building.lod > 1:
			ostream.write("for element in model1.layer_sets['building']:\n")
			ostream.write("	if element in model1.model_part.Elements:\n")
			ostream.write("		element_list.append( element )\n")
		if self.building.lod == 3:
			ostream.write("for element in model1.layer_sets['foundation']:\n")
			ostream.write("	if element in model1.model_part.Elements:\n")
			ostream.write("		element_list.append( element )\n")

		if self.lining.lod == 2:
			ostream.write("for step in range(1,number_of_slices+1):\n")
			ostream.write("	for element in model1.layer_sets['lining_'+str(step)]:\n")
			ostream.write("		if element in model1.model_part.Elements:\n")
			ostream.write("			element_list.append( element )\n")
			ostream.write("	for element in model1.layer_sets['grouting_'+str(step)]:\n")
			ostream.write("		if element in model1.model_part.Elements:\n")
			ostream.write("			element_list.append( element )\n")

		elif self.lining.lod == 3:	
			ostream.write("for step in range(1,number_of_slices+1):\n")
			ostream.write("	for j in range(1,(segment_number+1)):\n")				
			ostream.write("		for element in  model1.layer_sets['lining_'+str(step)+'_'+str(j)]:\n")
			ostream.write("			if element in model1.model_part.Elements:\n")
			ostream.write("				element_list.append( element )\n")		
			ostream.write("	for element in model1.layer_sets['grouting_'+str(step)]:\n")
			ostream.write("		if element in model1.model_part.Elements:\n")
			ostream.write("			element_list.append( element )\n")
		ostream.write("isu.ScalePrestress( model1.model_part, element_list, len(element_list), 0.0 )\n")
		
		#LOOK ABOVE IN NEW WAY OF SCALING PRESTRESSES
		# if self.tbm.lod > 1:
			# ostream.write("isu.ScalePrestress( model1.model_part, model1.layer_sets['shield'], len(model1.layer_sets['shield']), 0.0 )\n")

		# if self.lining.lod == 2:
			# ostream.write("for step in range(1,number_of_slices+1):\n")
			# ostream.write("	isu.ScalePrestress( model1.model_part, model1.layer_sets['lining_'+str(step)], len(model1.layer_sets['lining_'+str(step)]), 0.0 )\n")
			# ostream.write("	isu.ScalePrestress( model1.model_part, model1.layer_sets['grouting_'+str(step)], len(model1.layer_sets['grouting_'+str(step)]), 0.0 )\n")

		# if self.lining.lod == 3:
			# ostream.write("for step in range(1,number_of_slices+1):\n")
			# ostream.write("	for j in range(1,(segment_number+1)):\n")			
			# ostream.write("		isu.ScalePrestress( model1.model_part, model1.layer_sets['lining_'+str(step)+'_'+str(j)], len(model1.layer_sets['lining_'+str(step)+'_'+str(j)]), 0.0 )\n")
			# ostream.write("	isu.ScalePrestress( model1.model_part, model1.layer_sets['grouting_'+str(step)], len(model1.layer_sets['grouting_'+str(step)]), 0.0 )\n")

		# if self.building.lod > 1:
			# ostream.write("isu.ScalePrestress( model1.model_part, model1.layer_sets['building'], len(model1.layer_sets['building']), 0.0 )\n")

		# if self.building.lod == 3:
			# ostream.write("isu.ScalePrestress( model1.model_part, model1.layer_sets['foundation'], len(model1.layer_sets['foundation']), 0.0 )\n")
		# ostream.write("\n")
			
		if self.building.lod==1:	

			ostream.write("building_load=[]	\n")
			ostream.write("for node_id in top_nodes:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			ostream.write("	point[0]=node.X\n")
			ostream.write("	point[1]=node.Y\n")
			ostream.write("	if (InsidePointolygon(point, b_coords)==1):\n")
			ostream.write("		building_load.append(node_id)\n")		
			
			ostream.write("for node in building_load:\n")
			#ostream.write("	pressure = "+str(pressure)+"\n")
			ostream.write("	model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_Z,-building_pressure)\n")

			ostream.write("x0b_min=10000000.0\n")
			ostream.write("x0b_max=-10000000.0\n")
			ostream.write("y0b_min=10000000.0\n")
			ostream.write("y0b_max=-10000000.0\n")
			ostream.write("z0b_max=-10000000.0\n")
			ostream.write("for node_id in building_load:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			ostream.write("	if node.Z0>z0b_max:\n")
			ostream.write("		z0b_max=node.Z0\n")
			ostream.write("	if node.X0>x0b_max:\n")
			ostream.write("		x0b_max=node.X0\n")
			ostream.write("	elif node.X0<x0b_min:\n")
			ostream.write("		x0b_min=node.X0\n")
			ostream.write("	if node.Y0>y0b_max:\n")
			ostream.write("		y0b_max=node.Y0\n")
			ostream.write("	elif node.Y0<y0b_min:\n")
			ostream.write("		y0b_min=node.Y0\n")
			ostream.write("building_print=[]\n")
			ostream.write("for node_id in building_load:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			#ostream.write("	if node.Z0==z0b_max:\n")
			ostream.write("	if (node.X0==x0b_max) or  (node.X0==x0b_min) or (node.Y0==y0b_max) or  (node.Y0==y0b_min):\n")
			#ostream.write("			if node.Y0==y0b_max or  node.Y0==y0b_min:\n")
			ostream.write("				building_print.append(node_id)\n")
				
		if self.building.lod>1:
			# ostream.write("z0_f=10000000\n")
			# ostream.write("for node_id in model1.layer_nodes_sets['foundation']:\n")
			# ostream.write("	node = model1.model_part.Nodes[node_id]\n")				
			# ostream.write("	if node.Z0<z0_f:\n")
			# ostream.write("		z0_f=node.Z0\n")
			# ostream.write("tol=0.1\n")
			ostream.write("foundation_nodes=[]\n")
			ostream.write("for node_id in model1.layer_nodes_sets['foundation']:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")	
			# ostream.write("	if node.Z0<(z0_f+tol):\n")
			ostream.write("	foundation_nodes.append(node_id)\n")
			ostream.write("\n")		
			ostream.write("Epltu = EmbeddedNodePenaltyTyingUtility()\n")
			ostream.write("links1 = Epltu.SetUpTyingLinks( model1.model_part, foundation_nodes, model1.layer_sets['ground'] )\n")
			ostream.write("for cond in links1:\n")
			ostream.write("	cond.SetValue(INITIAL_PENALTY, 1.0e10)\n")
		if (self.tbm.lod>1 and self.lining.lod>1):
			ostream.write("shield_nodes=[]\n")
			ostream.write("for node in model1.layer_nodes_sets['shield']:\n")
			ostream.write("	if node in model1.model_part.Nodes:\n")
			ostream.write("		shield_nodes.append(node)\n")
			ostream.write("for node in model1.layer_nodes_sets['shield_outter_surface']:\n")
			ostream.write("	if node in model1.model_part.Nodes:\n")
			ostream.write("		shield_nodes.append(node)\n")
			
			ostream.write("\n")
		
		if self.lining.lod==1:
	
			ostream.write("delta_r=excavation_radius-excavation_radius*math.sqrt(1-volume_loss/100.0)\n")
			ostream.write("excavation_nodes=[]\n")

			ostream.write("for i in range (1, number_of_slices+1):\n")
			ostream.write("	for node in model1.layer_nodes_sets['excavation_surface_'+str(i)]:\n")
			ostream.write("		if node in model1.model_part.Nodes:\n")
			ostream.write("			excavation_nodes.append(node)\n")
						
			ostream.write("for node_id in excavation_nodes:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			ostream.write("	node.Fix(DISPLACEMENT_Z)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_Z, 0.0)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_EINS_Z, 0.0)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_NULL_Z, 0.0)\n")
			ostream.write("	node.Fix(DISPLACEMENT_X)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_X, 0.0)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_EINS_X, 0.0)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_NULL_X, 0.0)\n")
			ostream.write("	node.Fix(DISPLACEMENT_Y)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_Y, 0.0)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_EINS_Y, 0.0)\n")
			ostream.write("	node.SetSolutionStepValue(DISPLACEMENT_NULL_Y, 0.0)\n")



			
		ostream.write("print('##### ASSIGN HYDROSTATIC PORE PRESSURE #####')\n")
		ostream.write("#Prescribe Hydrostratic Pressure\n")
		ostream.write("free_node_list_water1 = []\n")
		ostream.write("free_node_list_air1 = []\n")
		ostream.write("model1.FixPressureNodes(free_node_list_water1, free_node_list_air1)\n")
		ostream.write("\n")

		ostream.write("print('##### APPLY INSITU STRESS INCREMENTAL #####')\n")
		ostream.write("time = 100.0\n")
		ostream.write("delta_time = 180.0\n")
		ostream.write("\n")

		ostream.write("if( account_for_water == True ):\n")
		ostream.write("	model1.ApplyInsituWaterPressure(free_node_list_water1, free_node_list_air1, z_coord_of_groundwater_table, 9.81)\n")
		ostream.write("	model1.SetReferenceWaterPressure()\n")
		
		ostream.write("print '######## DO THE FIRST STEP #############'\n")
		ostream.write("heading_face_pressure = support_pressure\n")
		ostream.write("heading_face_gradient = support_gradient\n")
		ostream.write("for node in model1.node_groups['heading_face_'+str(initial_face_index)]:\n")
		ostream.write("	initial_pressure = heading_face_pressure\n")
		#ostream.write("	depth = model1.model_part.Nodes[node].Z\n")
		ostream.write("	depth = model1.model_part.Nodes[node].Z\n")
		ostream.write("	pressure = initial_pressure-depth*heading_face_gradient\n")
		ostream.write("	model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,pressure)\n")
		ostream.write("lining_face_index= "+str(self.global_params['lining_offset'])+"\n")
		if self.lining.lod>1: 
			ostream.write("for node in model1.layer_nodes_sets['lining_surface_'+str(lining_face_index)]:\n")
			ostream.write("	initial_pressure = heading_face_pressure\n")
			ostream.write("	depth = model1.model_part.Nodes[node].Z\n")
			ostream.write("	pressure = initial_pressure-depth*heading_face_gradient\n")
			ostream.write("	model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,-pressure)     	\n")
			ostream.write("	if( account_for_water == True ):\n")
			ostream.write("		model1.model_part.Nodes[node].Fix(WATER_PRESSURE)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE,pressure)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_NULL,pressure)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_EINS,pressure)\n")
		
		if (self.tbm.lod>1 and self.lining.lod>1):
			ostream.write("for node in shield_nodes:\n")
			ostream.write("	if node in model1.model_part.Nodes:\n")
			ostream.write("		model1.model_part.Nodes[node].Fix(DISPLACEMENT_X)\n")
			ostream.write("		model1.model_part.Nodes[node].Fix(DISPLACEMENT_Y)\n")
			ostream.write("		model1.model_part.Nodes[node].Fix(DISPLACEMENT_Z)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_X, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_EINS_X, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_NULL_X, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_Y, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_EINS_Y, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_NULL_Y, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_Z, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_EINS_Z, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_NULL_Z, 0.0)\n")

		
		ostream.write("tol = 0.1\n")
		ostream.write("for node in model1.model_part.Nodes:\n")
		ostream.write("	if node.Z0 +tol < z0:\n")
		ostream.write("		node.Fix(DISPLACEMENT_Z)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_Z, 0.0)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_EINS_Z, 0.0)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_NULL_Z, 0.0)\n")
		ostream.write("	if (node.X0> (x0_max-tol)) or (node.X0< (x0_min+tol)):\n")
		ostream.write("		node.Fix(DISPLACEMENT_X)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_X, 0.0)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_EINS_X, 0.0)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_NULL_X, 0.0)\n")
		ostream.write("	if (node.Y0> (y0_max-tol)) or (node.Y0< (y0_min+tol)):\n")
		ostream.write("		node.Fix(DISPLACEMENT_Y)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_Y, 0.0)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_EINS_Y, 0.0)\n")
		ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_NULL_Y, 0.0)\n")
				
		ostream.write("###########################################SOLVE FOR THE FORST TIME################################\n")
		ostream.write("###################################################################################################\n")
		ostream.write("deactivation_index=0\n")
		ostream.write("model1.Solve( time, 0, deactivation_index, initial_reactivation_index, reactivation_index)\n")
		ostream.write("model1.WriteOutput( time )		\n")
		ostream.write("\n")
		
		ostream.write("if( account_for_water == True ):\n")
		ostream.write("	model1.FreePressureNodes( free_node_list_water1, free_node_list_air1) \n") 
		ostream.write("\n")
		ostream.write("time=time+delta_time\n")
		ostream.write("model1.Solve( time, 0, deactivation_index, initial_reactivation_index, reactivation_index)\n")
		ostream.write("model1.WriteOutput( time )		\n")
		
		#this is only for print
		if self.global_params["write_to_databese"]==True:
			ostream.write("#INITIAL BUILDING DISPLACEMENT\n")
			ostream.write("builidng_init=[[0,0,0]]*len(building_print)	\n")
			ostream.write("i=0\n")
			ostream.write("for node_id in building_print:\n")
			ostream.write("	node=model1.model_part.Nodes[node_id]\n")
			ostream.write("	builidng_init[i][0] = node.GetSolutionStepValue(DISPLACEMENT_X)\n")
			ostream.write("	builidng_init[i][1] = node.GetSolutionStepValue(DISPLACEMENT_Y)\n")
			ostream.write("	builidng_init[i][2] = node.GetSolutionStepValue(DISPLACEMENT_Z)\n")
			ostream.write("	i=i+1\n")
		
		ostream.write("delta_time_advance = time_advance\n")
		ostream.write("delta_time_downtime = time_ring_construction\n")
		ostream.write("one_ring= round_length\n")
		ostream.write("move_steps= move_steps_per_round_length\n")
		ostream.write("exc_steps= steps_per_down_time\n")
		ostream.write("move_delta_time= delta_time_advance/float(move_steps)\n")
		ostream.write("exc_delta_time= delta_time_downtime/float(exc_steps)\n")
		ostream.write("face_index = initial_face_index\n")
		ostream.write("grouting_surface_index = initial_grouting_surface_index\n")
		ostream.write("\n")		
		if self.lining.lod==1:			
			ostream.write("for node_id in excavation_nodes:\n")
			ostream.write("	node = model1.model_part.Nodes[node_id]\n")
			ostream.write("	node.Free(DISPLACEMENT_Z)\n")
			ostream.write("	node.Free(DISPLACEMENT_X)\n")
			ostream.write("	node.Free(DISPLACEMENT_Y)\n")

		

		
		return