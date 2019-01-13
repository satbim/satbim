import sys
import os
import fnmatch
import math
import subprocess
from ModelComponent import *
from HelperMethods import *

class BuildingComponent(ModelComponent):

	# Constructor
	def __init__(self, global_params, working_dir):
		ModelComponent.__init__(self, global_params, working_dir)
		
		# Setup LOD handlers
		self.lod_prepare_handlers = [self.PrepareModel_Lod1, self.PrepareModel_Lod2, self.PrepareModel_Lod3]
		self.lod_script_handlers = [self.AddToSimScript_Lod1, self.AddToSimScript_Lod2, self.AddToSimScript_Lod3]
		
		# Define name
		self.component_name = "building"
		# Dependencies
		self.soil = None
		
	
	def ReadParams(self, pathToParamFile):	
		ModelComponent.ReadParams(self, pathToParamFile)
		
		if self.lod <= 2:
			self.is_collapsable = True
		else:
			self.is_collapsable = False
	
	def PrepareModel_Lod1(self, ostream):
		# Write model to .bch output file
		print 'Building LOD = 1'
		

		
		return
	
	def PrepareModel_Lod2(self, ostream):
		# Write model to .bch output file
		print 'Building LOD = 2'
		# Write model to .bch output file

		ostream.write("mescape\n")
		ostream.write("Files SaveAs "+self.working_dir+self.global_params['model_name']+"_building_model.gid\n")
		ostream.write("mescape\n")
		n_col_x=self.params['n_col_x']
		n_col_y=self.params['n_col_y']
		n_floors=self.params['n_floors']
		dirpath= str(self.global_params['model_path'])+ "sat_files/buildings/"
		no_build= len(fnmatch.filter(os.listdir(dirpath), '*.sat'))	
		print(no_build)
		ostream.write("mescape\n")
		ostream.write("view layers new\n")
		ostream.write("building \n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("building \n escape escape\n")
		for step in range(1,no_build+1):
			ostream.write("mescape\n")    
			ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/buildings/building_volume" +str(step)+".sat"+"\n ")
			
			

		ostream.write("mescape\n")
		ostream.write("view layers new\n")
		ostream.write("foundation \n escape escape\n")
		ostream.write("view layers ToUse\n")
		ostream.write("foundation \n escape escape\n")
		for i in range (0,no_build):
			ostream.write("view layers entities\n")
			ostream.write("foundation \n")
			ostream.write("LowerEntities Surfaces\n")
			#ostream.write("surfaces\n 21 24\n")
			ostream.write(str(i*6+1)+"\n")
			ostream.write("mescape\n")
			
			
			
		ostream.write("mescape\n")
		ostream.write("Meshing ElemType Hexahedra\n")
		ostream.write("InvertSelection\n escape \n escape \n")
		ostream.write("mescape\n")
		ostream.write("Meshing Structured Volumes\n")
		ostream.write("InvertSelection\n escape \n 1\n")
		ostream.write("InvertSelection\n escape\n escape\n")
			
		ostream.write("mescape\n")
		ostream.write("Meshing Structured Lines 4\n")
		ostream.write("InvertSelection\n escape\n")
		ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Utilities Variables Model(QuadraticType) 1\n")
		ostream.write("mescape\n")
		ostream.write("Meshing Generate\n")
		ostream.write("DefaultSize\n")
		ostream.write("mescape\n")
		
		
		ostream.write("Files Save\n")
		ostream.write("Quit\n")
		ostream.close()		

		#########CREATE BACH FILE FOR MATERIAL PARAMETERS####		
		ifile = open(self.working_dir+'material_condition_building.bch','w')
		#create material building
		ifile.write("mescape\n")
		#ifile.write("Data Materials NewMaterial Isotropic3D Building Isotropic3D Isotropic3D "+str(0.0)+"kg/m^3 "+ str(self.params['E_build'])+"N/mm^2 "+str(self.params['nu_build'])+"\n")
		ifile.write("Data Materials NewMaterial Isotropic3D Building Isotropic3D Isotropic3D "+str(self.params['ro_build']/4.0)+"kg/m^3 "+ str(self.params['E_build']*1000000)+"N/mm^2 "+str(self.params['nu_build'])+"\n")
		ifile.write("mescape\n")
		ifile.write("Data Materials AssignMaterial Building Volumes\n")
		ifile.write("layer:building\n")
		ifile.write("mescape\n")
		if self.soil.lod ==1:
			ifile.write("mescape\n")
			ifile.write("Data Conditions AssignCond Surface_Bedding Change\n 1 0.0N/m^3\n 1 0.0N/m^3\n 1 0.0N/m^3\n")
			ifile.write("layer:foundation\n")
			ifile.write("mescape\n")
			
		#asign kinematic linear element type to building

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
		ifile.write("layer:building \n")
		ifile.write("mescape\n")


		ifile.close()			

		
		return
		
	def PrepareModel_Lod3(self, ostream):
		# Write model to .bch output file
		if isinstance(self.lod, numbers.Integral)==True:
			print 'Building LOD = 3'
			ostream.write("mescape\n")		
			ostream.write("Utilities Variables ImportTolerance 5 AutoImportTolerance 0\n")
			ostream.write("mescape\n")

			ostream.write("mescape\n")
			ostream.write("Files SaveAs "+self.working_dir+self.global_params['model_name']+"_building_model.gid\n")
			ostream.write("mescape\n")
			n_col_x=self.params['n_col_x']
			n_col_y=self.params['n_col_y']
			n_floors=self.params['n_floors']
			start_0= n_col_x*n_col_y*n_floors*2+n_col_x*n_col_y+(n_col_x-1)*(n_col_y-1)*5*(n_floors+1)
			ostream.write("mescape\n")
			ostream.write("view layers new\n")
			ostream.write("building \n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("building \n escape escape\n")
			for step in range(1,start_0+1):
				ostream.write("mescape\n")    
				ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files/buildings/building_volume" +str(step)+".sat"+"\n ")
				
				

			ostream.write("mescape\n")
			ostream.write("view layers new\n")
			ostream.write("foundation \n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("foundation \n escape escape\n")
			for i in range (0,(n_col_x*n_col_y)):
				ostream.write("view layers entities\n")
				ostream.write("foundation \n")
				ostream.write("LowerEntities Volumes\n")
				#ostream.write("surfaces\n 21 24\n")
				ostream.write(str(i*2+1)+"\n")
				ostream.write("mescape\n")
			start_1= (n_col_x*n_col_y*n_floors*2+n_col_x*n_col_y)
			start_2=(n_col_x-1)*n_col_y+(n_col_y-1)*n_col_x+(n_col_x-1)*(n_col_y-1)
			for i in range (0,start_2):
				ostream.write("view layers entities\n")
				ostream.write("foundation \n")
				ostream.write("LowerEntities Volumes\n")
				#ostream.write("surfaces\n 21 24\n")
				ostream.write(str(start_1+i+1)+"\n")
				ostream.write("mescape\n")
				
				
				
			ostream.write("mescape\n")
			ostream.write("Meshing ElemType Hexahedra\n")
			ostream.write("InvertSelection\n escape\n escape\n")
			ostream.write("mescape\n")
			ostream.write("Meshing Structured Volumes\n")
			ostream.write("InvertSelection\n escape\n 1\n")
			ostream.write("InvertSelection\n escape\n")
			ostream.write("mescape\n")
			ostream.write("Utilities Variables Model(QuadraticType) 1\n")
			ostream.write("mescape\n")
			ostream.write("Meshing Generate\n")
			ostream.write("DefaultSize\n")
			ostream.write("mescape\n")
			
			
			ostream.write("Files Save\n")
			ostream.write("Quit\n")
			ostream.close()		
			

			
			#########CREATE BACH FILE FOR MATERIAL PARAMETERS ANS CONDITIONS####	

			ifile = open(self.working_dir+'material_condition_building.bch','w')		
			#create material building
			ifile.write("mescape\n")
			#ifile.write("Data Materials NewMaterial Isotropic3D Building Isotropic3D Isotropic3D "+str(0.0)+"kg/m^3 "+ str(self.params['E_build'])+"N/mm^2 "+str(self.params['nu_build'])+"\n")
			ifile.write("Data Materials NewMaterial Isotropic3D Building Isotropic3D Isotropic3D "+str(self.params['ro_build'])+"kg/m^3 "+ str(self.params['E_build']*1000000)+"N/mm^2 "+str(self.params['nu_build'])+"\n")
			ifile.write("mescape\n")
			ifile.write("Data Materials AssignMaterial Building Volumes\n")
			ifile.write("layer:building\n")
			ifile.write("mescape\n")
			ifile.write("Data Materials AssignMaterial Building Volumes\n")
			ifile.write("layer:foundation\n")
			ifile.write("mescape\n")
			ifile.write("mescape\n")
			
			
			#asign kinematic linear element type to building

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
			ifile.write("layer:building \n")
			ifile.write("mescape\n")
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
			ifile.write("layer:foundation \n")
			ifile.write("mescape\n")
		
			if self.soil.lod ==1:
				ifile.write("mescape\n")
				ifile.write("Data Conditions AssignCond Surface_Bedding Change\n 1 0.0N/m^3\n 1 0.0N/m^3\n 1 0.0N/m^3\n")
				ifile.write("layer:foundation\n")
				ifile.write("mescape\n")
			ifile.close()
		else:
			index=0
			for i in range(0, len(self.params['lod'])):
				index=index+1
				#print(index)
				#print(self.params['lod'])
				if int(self.params['lod'][i])==1:
					#print("lod1")
					self.PrepareSubModel_Lod1(self.params['lod'][i], index)
				if int(self.params['lod'][i])==2:
					#print("lod2")
					self.PrepareSubModel_Lod2(self.params['lod'][i], index)
				if int(self.params['lod'][i])==3:
					#print("lod3")
					self.PrepareSubModel_Lod3(self.params['lod'][i], index)
					
			print 'Building LOD = 3'
			ostream.write("mescape\n")		
			ostream.write("Utilities Variables ImportTolerance 5 AutoImportTolerance 0\n")
			ostream.write("mescape\n")

			ostream.write("mescape\n")
			ostream.write("Files SaveAs "+self.working_dir+self.global_params['model_name']+"_building_model.gid\n")
			ostream.write("mescape\n")
			for i in range(0, len(self.params['lod'])):
				ostream.write("mescape\n")	
				ostream.write("mescape\n")
				ostream.write("Files InsertGeom "+self.working_dir+self.global_params['model_name']+'_building_help_'+str(i+1)+'.gid\n')
				ostream.write("mescape\n")
				ostream.write("mescape\n")
				
			ostream.write("Meshing CancelMesh PreserveFrozen Yes\n")
			ostream.write("mescape\n")
			ostream.write("mescape\n")
			ostream.write("Utilities Variables Model(QuadraticType) 1\n")
			ostream.write("mescape\n")
			ostream.write("Meshing Generate\n")
			ostream.write("DefaultSize\n")
			ostream.write("mescape\n")
			
			
			ostream.write("Files Save\n")
			ostream.write("Quit\n")
#			ostream.close()	

			#########CREATE BACH FILE FOR MATERIAL PARAMETERS ANS CONDITIONS####	

			ifile = open(self.working_dir+'material_condition_building.bch','w')		
			#create material building
			index=0
			for i in range(0, len(self.params['lod'])):
				index=index+1
				ifile.write("mescape\n")
				ifile.write("Data Materials NewMaterial Isotropic3D Building_" +str(index)+" Isotropic3D Isotropic3D "+str(self.params['ro_build'][index-1])+"kg/m^3 "+ str(self.params['E_build'][index-1]*1000000)+"N/mm^2 "+str(self.params['nu_build'][index-1])+"\n")
				ifile.write("mescape\n")
				ifile.write("Data Materials AssignMaterial Building_" +str(index)+" Volumes\n")
				ifile.write('layer:building_'+str(index)+'\n')
				ifile.write("mescape\n")
				ifile.write("Data Materials AssignMaterial Building_" +str(index)+" Volumes\n")
				ifile.write('layer:foundation_'+str(index)+'\n')
				ifile.write("mescape\n")
				ifile.write("mescape\n")
			
			
				#asign kinematic linear element type to building

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
				ifile.write('layer:building_'+str(index)+'\n')
				ifile.write("mescape\n")
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
				ifile.write('layer:foundation_'+str(index)+'\n')
				ifile.write("mescape\n")
			
				if self.soil.lod ==1:
					ifile.write("mescape\n")
					ifile.write("Data Conditions AssignCond Surface_Bedding Change\n 1 0.0N/m^3\n 1 0.0N/m^3\n 1 0.0N/m^3\n")
					ifile.write('layer:foundation_'+str(index)+'\n')
					ifile.write("mescape\n")
			ifile.close()	
			
		return
		
	def AddToSimScript_Lod1(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Building SimScript LOD = 1'
		
		# ostream.write("def InsidePointolygon(Point, Polygon):\n")
		# ostream.write("	cn = 0    # the crossing number counter\n")

		# ostream.write("	Polygon = tuple(Polygon[:])+(Polygon[0],)\n")

		# ostream.write("	# loop through all edges of the Polygon\n")
		# ostream.write("	for i in range(len(Polygon)-1):   # edge from V[i] to V[i+1]\n")
		# ostream.write("		if ((Polygon[i][1] <= Point[1] and Polygon[i+1][1] > Point[1])   # an upward crossing\n")
		# ostream.write("			or (Polygon[i][1] > Point[1] and Polygon[i+1][1] <= Point[1])):  # a downward crossing\n")
		# ostream.write("			# comPointute the actual edge-ray intersect x-coordinate\n")
		# ostream.write("			vt = (Point[1] - Polygon[i][1]) / float(Polygon[i+1][1] - Polygon[i][1])\n")
		# ostream.write("			if Point[0] < Polygon[i][0] + vt * (Polygon[i+1][0] - Polygon[i][0]): # Point[0] < intersect\n")
		# ostream.write("				cn += 1  # a valid crossing of y=Point[1] right of Point[0]\n")

		# ostream.write("	return cn % 2   # 0 if even (out), and 1 if odd (in)\n")

		
		# self.coords = HelperMethods.ReadAlignmentFile(self.global_params['model_path']+'/input_files/')	
		# b_coords = HelperMethods.ReadBuildingFile(self.global_params['model_path']+'/sat_files/buildings/')
		#print(b_coords)
		# for i in range (0,len(b_coords)):
			# b_coords[i][0]=b_coords[i][0]/100.0-self.coords[0][0]
			# b_coords[i][1]=b_coords[i][1]/100.0-self.coords[0][1]
		# print(b_coords)
		
		# ostream.write("building_load=[]	\n")
		# ostream.write("for node_id in top_nodes:\n")
		# ostream.write("	node = model1.model_part.Nodes[node_id]\n")
		# ostream.write("	point[0]=node.X\n")
		# ostream.write("	point[1]=node.Y\n")
		# ostream.write("	if (InsidePointolygon(point, b_coord)=True)\n")
		# ostream.write("		building_load.append(node_id)\n")
		
		
		
		# n_col_x=self.params['n_col_x']
		# n_col_y=self.params['n_col_y']
		# n_floors=self.params['n_floors']
		# ro_build=self.params['ro_build']
		# x_span=self.params['x_span']/100.0
		# y_span=self.params['y_span']/100.0
		# h_floor=self.params['h_floor']/100.0
		
		#####FINISH WAHAT
		# print("do x_span. y_span_f_span")
		
		# pressure=(n_col_x-1)*x_span*(n_col_y-1)*y_span*(n_floors-1)*h_floor*ro_build*9.81
		# ostream.write("	for node in building_load:\n")
		# ostream.write("			pressure = "+str(pressure)+"\n")
		# ostream.write("			model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_Z,-pressure)\n")
		
		return
		
	def AddToSimScript_Lod2(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Building SimScript LOD = 2'
		
		params_soil = HelperMethods.ReadMaterialFile(self.global_params['model_path']+'/'+self.global_params['matfile']+'.dat')
		if self.soil.lod==1:
			ostream.write("z0=10000000\n")
			ostream.write("for node in model.layer_nodes_sets['building']:\n")
			ostream.write("	if node.Z0<z0:\n")
			ostream.write("		z0=node.Z0\n")
			ostream.write("tol=0.1\n")
			ostream.write("foundation_nodes=[]\n")
			ostream.write("for node in model.layer_nodes_sets['building']:\n")
			ostream.write("	if node.Z0<(z0+tol):\n")
			ostream.write("		foundation_nodes.append(node)\n")
			ostream.write("\n")		
			E_soil_1=params_soil['E_soil_1']
			nu_soil_1=params_soil['nu_soil_1']
			k_spring=E_soil_1/(self.global_params['excavation_radius']/100)*((1-nu_soil_1)/((1+nu_soil_1)*(1-2*nu_soil_1)))

			ostream.write("for node_id in foundation_nodes:\n")
			ostream.write("	node = model.model_part.Nodes[node_id]\n")
			ostream.write("	node.SetSolutionStepValue(ELASTIC_BEDDING_STIFFNESS_X, "+ str(k_spring)+")\n")
			ostream.write("	node.SetSolutionStepValue(ELASTIC_BEDDING_STIFFNESS_Y, "+ str(k_spring)+")\n")
			ostream.write("	node.SetSolutionStepValue(ELASTIC_BEDDING_STIFFNESS_Z, "+ str(k_spring)+")\n")
			
			ostream.write("Epltu = EmbeddedNodePenaltyTyingUtility()\n")
			ostream.write("links1 = Epltu.SetUpTyingLinks( model.model_part, foundation_nodes, model.layer_sets['ground'] )\n")
			ostream.write("for cond in links1:\n")
			ostream.write("	cond.SetValue(INITIAL_PENALTY, 1.0e10)\n")
		return
		
	def AddToSimScript_Lod3(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Building SimScript LOD = 3'

			
		params_soil = HelperMethods.ReadMaterialFile(self.global_params['model_path']+'/'+self.global_params['matfile']+'.dat')
		if self.soil.lod==1:
			if isinstance(self.lod, numbers.Integral)==True:		
				ostream.write("z0=10000000\n")
				ostream.write("for node in model.layer_nodes_sets['foundation']:\n")
				ostream.write("	if node.Z0<z0:\n")
				ostream.write("		z0=node.Z0\n")
				ostream.write("tol=0.1\n")
				ostream.write("foundation_nodes=[]\n")
				ostream.write("for node in model.layer_nodes_sets['foundation']:\n")
				ostream.write("	if node.Z0<(z0+tol):\n")
				ostream.write("		foundation_nodes.append(node)\n")
			else:
				n_buildings=len(self.params['lod'])
				ostream.write("z0=10000000\n")
				ostream.write('for i in range(0,'+str(n_buildings)+'):\n')				
				ostream.write("	for node in model.layer_nodes_sets['foundation_'+str(i)]:\n")
				ostream.write("		if node.Z0<z0:\n")
				ostream.write("			z0=node.Z0\n")
				ostream.write("	tol=0.1\n")
				ostream.write("	foundation_nodes=[]\n")
				
				ostream.write('for i in range(0,'+str(n_buildings)+'):\n')				
				ostream.write("	for node in model.layer_nodes_sets['foundation_'+str(i)]:\n")
				ostream.write("		if node.Z0<(z0+tol):\n")
				ostream.write("			foundation_nodes.append(node)\n")
			ostream.write("\n")		
			E_soil_1=params_soil['E_soil_1']
			nu_soil_1=params_soil['nu_soil_1']
			k_spring=E_soil_1/(self.global_params['excavation_radius']/100)*((1-nu_soil_1)/((1+nu_soil_1)*(1-2*nu_soil_1)))

			ostream.write("for node_id in foundation_nodes:\n")
			ostream.write("	node = model.model_part.Nodes[node_id]\n")
			ostream.write("	node.SetSolutionStepValue(ELASTIC_BEDDING_STIFFNESS_X, "+ str(k_spring)+")\n")
			ostream.write("	node.SetSolutionStepValue(ELASTIC_BEDDING_STIFFNESS_Y, "+ str(k_spring)+")\n")
			ostream.write("	node.SetSolutionStepValue(ELASTIC_BEDDING_STIFFNESS_Z, "+ str(k_spring)+")\n")
			
			ostream.write("Epltu = EmbeddedNodePenaltyTyingUtility()\n")
			ostream.write("links1 = Epltu.SetUpTyingLinks( model.model_part, foundation_nodes, model.layer_sets['ground'] )\n")
			ostream.write("for cond in links1:\n")
			ostream.write("	cond.SetValue(INITIAL_PENALTY, 1.0e10)\n")
			
		return
		
	def PrepareSubModel_Lod2(self, sub_lod, index):
	
		ifile=open( self.working_dir+self.global_params['model_name']+'_building_help_'+str(index)+'.bch','w')
		ifile.write("mescape\n")
		
		ifile.write("mescape\n")		
		ifile.write("Utilities Variables ImportTolerance 5 AutoImportTolerance 0\n")
		ifile.write("mescape\n")

		ifile.write("mescape\n")
		ifile.write("Files SaveAs "+self.working_dir+self.global_params['model_name']+'_building_help_'+str(index)+'.gid\n')
		ifile.write("mescape\n")
		n_col_x=int(self.params['n_col_x'][index-1])
		n_col_y=int(self.params['n_col_y'][index-1])
		n_floors=int(self.params['n_floors'][index-1])
		dirpath= str(self.global_params['model_path'])+ 'sat_files/buildings/building_'+str(index)
		no_build= len(fnmatch.filter(os.listdir(dirpath), '*.sat'))	
#		print(no_build)
		ifile.write("mescape\n")
		ifile.write("view layers new\n")
		ifile.write('building_'+str(index)+' \n escape escape\n')
		ifile.write("view layers ToUse\n")
		ifile.write('building_'+str(index)+' \n escape escape\n')
		for step in range(1,no_build+1):
			ifile.write("mescape\n")    
			ifile.write("Files AcisRead " +str(self.global_params['model_path'])+ 'sat_files/buildings/building_'+str(index)+'/building_volume' +str(step)+".sat"+"\n ")
			
			

		ifile.write("mescape\n")
		ifile.write("view layers new\n")
		ifile.write('foundation \n escape escape\n')
		ifile.write("view layers ToUse\n")
		ifile.write('foundation \n escape escape\n')
		for i in range (0,no_build):
			ifile.write("view layers entities\n")
			ifile.write('foundation \n')
			ifile.write("LowerEntities Surfaces\n")
			#ostream.write("surfaces\n 21 24\n")
			ifile.write(str(i*6+2)+"\n")
			ifile.write("mescape\n")
			
			
			
		ifile.write("mescape\n")
		ifile.write("Meshing ElemType Hexahedra\n")
		ifile.write("InvertSelection\n escape\n")
		ifile.write("mescape\n")
		ifile.write("Meshing Structured Volumes\n")
		ifile.write("InvertSelection\n escape\n 1\n")
		ifile.write("InvertSelection\n escape\n escape\n")
			
		ifile.write("mescape\n")
		ifile.write("Meshing Structured Lines 8\n")
		ifile.write("InvertSelection\n escape\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Variables Model(QuadraticType) 1\n")
		ifile.write("mescape\n")
		ifile.write("Meshing Generate\n")
		ifile.write("DefaultSize\n")
		ifile.write("mescape\n")
		
		
		ifile.write("Files Save\n")
		ifile.write("Quit\n")
		ifile.close()		



#		self.gid_path='C:/Program Files/GiD/GiD 12.0.10/'
#		subprocess.check_output([self.gid_path+'gid_offscreen.bat', '-offscreen', '-b', self.global_params['model_name'] + '_builiding_'+str(index)+'.bch', self.global_params['model_name']], cwd=self.working_dir) # +self.working_dir )
		subprocess.check_output([self.global_params['gid_path']+'gid_offscreen.bat', '-offscreen', '-b', self.global_params['model_name'] + '_building_help_'+str(index)+'.bch', self.global_params['model_name']], cwd=self.working_dir)
				
	
	def PrepareSubModel_Lod3(self, sub_lod, index):
	
		ifile=open( self.working_dir+self.global_params['model_name']+'_building_help_'+str(index)+'.bch','w')
		ifile.write("mescape\n")
	
		# Write model to .bch output file
#		print 'Building LOD = 3'
		ifile.write("mescape\n")		
		ifile.write("Utilities Variables ImportTolerance 5 AutoImportTolerance 0\n")
		ifile.write("mescape\n")

		ifile.write("mescape\n")
		ifile.write("Files SaveAs "+self.working_dir+self.global_params['model_name']+'_building_help_'+str(index)+'.gid\n')
		ifile.write("mescape\n")
		n_col_x=int(self.params['n_col_x'][index-1])
		n_col_y=int(self.params['n_col_y'][index-1])
		n_floors=int(self.params['n_floors'][index-1])
		start_0= n_col_x*n_col_y*n_floors*2+n_col_x*n_col_y+(n_col_x-1)*(n_col_y-1)*5*(n_floors+1)
		ifile.write("mescape\n")
		ifile.write("view layers new\n")
		ifile.write('building_'+str(index)+' \n escape escape\n')
		ifile.write("view layers ToUse\n")
		ifile.write('building_'+str(index)+' \n escape escape\n')
		for step in range(1,start_0+1):
			ifile.write("mescape\n")    
			ifile.write("Files AcisRead " +str(self.global_params['model_path'])+ 'sat_files/buildings/building_'+str(index)+'/building_volume' +str(step)+".sat"+"\n ")
			
			

		ifile.write("mescape\n")
		ifile.write("view layers new\n")
		ifile.write('foundation_'+str(index)+' \n escape escape\n')
		ifile.write("view layers ToUse\n")
		ifile.write('foundation_'+str(index)+' \n escape escape\n')
		for i in range (0,(n_col_x*n_col_y)):
			ifile.write("view layers entities\n")
			ifile.write('foundation_'+str(index)+' \n')
			ifile.write("LowerEntities Volumes\n")
			#ostream.write("surfaces\n 21 24\n")
			ifile.write(str(i*2+1)+"\n")
			ifile.write("mescape\n")
		start_1= (n_col_x*n_col_y*n_floors*2+n_col_x*n_col_y)
		start_2=(n_col_x-1)*n_col_y+(n_col_y-1)*n_col_x+(n_col_x-1)*(n_col_y-1)
		for i in range (0,start_2):
			ifile.write("view layers entities\n")
			ifile.write('foundation_'+str(index)+' \n')
			ifile.write("LowerEntities Volumes\n")
			#ostream.write("surfaces\n 21 24\n")
			ifile.write(str(start_1+i+1)+"\n")
			ifile.write("mescape\n")
			

		ifile.write("mescape\n")	
		ifile.write('Layers off building_'+str(index)+' \n')		
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("view layers new\n")
		ifile.write('foundation \n escape escape\n')
		ifile.write("view layers ToUse\n")
		ifile.write('foundation \n escape escape\n')	
		ifile.write("view layers entities\n")
		ifile.write("foundation \n")
		ifile.write("LowerEntities Surfaces\n")
		ifile.write("InvertSelection\n")
		ifile.write("mescape\n")


		ifile.write("mescape\n")	
		ifile.write('Layers on building_'+str(index)+' \n')		
		ifile.write("mescape\n")		
			
		ifile.write("mescape\n")
		ifile.write("Meshing ElemType Hexahedra\n")
		ifile.write("InvertSelection\n escape\n")
		ifile.write("mescape\n")
		ifile.write("Meshing Structured Volumes\n")
		ifile.write("InvertSelection\n escape\n 1\n")
		ifile.write("InvertSelection\n escape\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		#print("I am here and I do: Meshing Structured Lines 1")
		ifile.write("Meshing Structured Lines 1\n")
		ifile.write("InvertSelection\n escape\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")
		ifile.write("Utilities Variables Model(QuadraticType) 1\n")
		ifile.write("mescape\n")
		ifile.write("Meshing Generate\n")
		ifile.write("DefaultSize\n")
		ifile.write("mescape\n")
		
		
		ifile.write("Files Save\n")
		ifile.write("Quit\n")
		ifile.close()		
		

		

		
		#self.gid_path='C:/Program Files/GiD/GiD 12.0.10/'
		#subprocess.check_output([self.gid_path+'gid_offscreen.bat', '-offscreen', '-b', self.global_params['model_name'] + '_builiding_'+str(index)+'.bch', self.global_params['model_name']], cwd=self.working_dir) # +self.working_dir )
		subprocess.check_output([self.global_params['gid_path']+'gid_offscreen.bat', '-offscreen', '-b', self.global_params['model_name'] + '_building_help_'+str(index)+'.bch', self.global_params['model_name']], cwd=self.working_dir)
				