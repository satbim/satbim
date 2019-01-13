import sys
import os
import math
from HelperMethods import *
from ModelComponent import *

class InsituComponent(ModelComponent):

	# Constructor
	def __init__(self, global_params, working_dir):
		ModelComponent.__init__(self, global_params, working_dir)
		
		# Setup LOD handlers
		self.lod_prepare_handlers = [self.PrepareModel_Lod1]
		self.lod_script_handlers = [self.AddToSimScript_Lod1]
		
		# Define name
		self.component_name = "insitu"
		
		# Dependencies
		self.soil = None
		self.building = None
		self.lining = None
		self.tbm = None
		
	
	def ReadParams(self, pathToParamFile):	
		ModelComponent.ReadParams(self, pathToParamFile)
		
		if self.lod <= 2:
			self.is_collapsable = True
		else:
			self.is_collapsable = False
	
	def PrepareModel_Lod1(self, ostream):
		# # Write model to .bch output file
		# print 'Insitu LOD = 1'
		
		# if self.soil.lod ==1:
			# return
		# ostream.write("mescape\n")
		# #Define problem type
		# #import Insitu Model
		
		# ostream.write("mescape\n")
		# ostream.write("Files SaveAs " + self.working_dir + self.global_params['model_name'] + "_insitu_model.gid\n")
		# ostream.write("mescape\n")


		# ostream.write("mescape\n")
		# ostream.write("Utilities Variables ImportTolerance "+str(self.global_params['excavation_radius']/10)+" AutoImportTolerance 0\n")
		# ostream.write("mescape\n")
		# ostream.write("view layers new\n")
		# ostream.write("ground"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("ground"+"\n escape escape\n")
		# ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files\soil_insitu\soil_insitu_volume.sat"+"\n ")

		# ostream.write("mescape\n")
		# ostream.write("Utilities Variables ImportTolerance "+str(self.global_params['excavation_radius']/10)+" AutoImportTolerance 0\n")
		# ostream.write("mescape\n")
		# # # Define problem type
		# ostream.write("mescape\n")
		# ostream.write("Data Defaults ProblemType Yes ekate ")
		# ostream.write("mescape\n")
		# ostream.write("mescape\n")

		
		# ###ASIGN LAYERS FOR BOUNDARY CONDITIONS
		# ostream.write("mescape\n")
		# ostream.write("view layers new\n")
		# ostream.write("Top"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("Top\n escape escape\n")
		# ostream.write("Layers Entities\n")
		# ostream.write("Top\n")
		# ostream.write("LowerEntities Surfaces\n")
		# ostream.write("1 \n")
		# ostream.write("mescape\n")
		# ostream.write("view layers new\n")
		# ostream.write("Bottom"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("Bottom\n escape escape\n")
		# ostream.write("Layers Entities\n")
		# ostream.write("Bottom\n")
		# ostream.write("LowerEntities Surfaces\n")
		# ostream.write("2 \n")
		# ostream.write("mescape\n") 
		# ostream.write("view layers new\n")
		# ostream.write("Side_x"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("Side_x"+"\n escape escape\n")
		# ostream.write("Layers Entities\n")
		# ostream.write("Side_x\n")
		# ostream.write("LowerEntities Surfaces\n")
		# ostream.write("4 6 \n")
		# ostream.write("mescape\n") 
		# ostream.write("view layers new\n")
		# ostream.write("Side_y"+"\n escape escape\n")
		# ostream.write("view layers ToUse\n")
		# ostream.write("Side_y"+"\n escape escape\n")
		# ostream.write("Layers Entities\n")
		# ostream.write("Side_y\n")
		# ostream.write("LowerEntities Surfaces\n")
		# ostream.write("3 5 \n")
		# ostream.write("mescape\n") 
		# ostream.write("mescape\n")
		# ostream.write("Data Conditions AssignCond IsTop\n")
		# ostream.write("UnAssign InvertSelection\n")
		# ostream.write("mescape\n")

		# #ASIGN CONDITIONS DISPLACEMENTS

		# #########CREATE BACH FILE FOR MATERIAL PARAMETERS AND CONDITIONS####		
		# ifile = open(self.working_dir+'material_condition_insitu.bch','w')
		# ifile.write("mescape\n")
		
		# #assign boundary conditions
		# ifile.write("*****TCL GetBoundary \n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond VolumeElementType\n")
		# if( self.global_params['account_for_water'] == "True" ):
			# ifile.write("Change UnsaturatedSoil_2Phase\n")
			# ifile.write("1000.0kg/m^3\n")
			# ifile.write("1.295kg/m^3\n")
			# ifile.write("0.2\n")
			# ifile.write("0.001m/s\n")
			# ifile.write("0.00000032m/s\n")
			# ifile.write("0.00000044m/s\n")
			# ifile.write("0.0001m/s\n")
			# ifile.write("0.0535\n")
		# else:
			# ifile.write("Change Kinematic_Linear\n")
			# ifile.write("1000.0kg/m^3\n")
			# ifile.write("1.295kg/m^3\n")
			# ifile.write("0.2\n")
			# ifile.write("0.001m/s\n")
			# ifile.write("0.00000032m/s\n")
			# ifile.write("0.00000044m/s\n")
			# ifile.write("0.0001m/s\n")
			# ifile.write("0.0535\n")
		# ifile.write("layer:ground\n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond IsTop\n")
		# ifile.write("UnAssign InvertSelection\n")
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
		# ifile.write("mescape\n")		
		# ifile.write("Data Conditions AssignCond IsTop\n")
		# ifile.write("layer:Top\n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond Surface_Water_Pressure\n")
		# ifile.write("UnAssign layer:Top\n")
		# ifile.write("mescape\n")        
		# ifile.write("mescape\n")
		# ifile.write("Files Save\n")
		# ifile.write("mescape\n")
		# ifile.write("mescape\n")
		# ifile.write("Files Save\n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond Surface_Group_Membership\n")
		# ifile.write("Change Top\n")
		# ifile.write("layer:Top\n")
		# ifile.write("mescape\n")
		# ifile.write("Data Conditions AssignCond Distributed_Surface_Load\n")
		# ifile.write("layer:Top\n")
		# ifile.write("mescape\n")

		
		# #create material for insitu
		# ifile.write("mescape\n")  
		# ifile.write("Data Materials NewMaterial UserDefined Soil UserDefined UserDefined\n")
		# ifile.write("mescape\n")
		
		# #assign materials
		# ifile.write("Data Materials AssignMaterial Soil Volumes\n")
		# ifile.write("layer:ground\n")
		# ifile.write("mescape\n")
		
		# #scale complete_model_to meters
		# self.coords = HelperMethods.ReadAlignmentFile(self.global_params['model_path']+'/input_files/')
		
		# ifile.write("Utilities Move All Duplicate MaintainLayers Scale\n")
		# ifile.write(str(self.coords[0][0])+" "+str(self.coords[0][1])+" "+str(self.coords[0][2])+"\n")
		# ifile.write("0.01 0.01 0.01\n")
		# ifile.write("InvertSelection\n")
		# ifile.write("mescape\n")
		
		# #move complete_model_to position 0,0,0
		# ifile.write("Utilities Move All Duplicate MaintainLayers Translation\n")
		# ifile.write(str(self.coords[0][0])+" "+str(self.coords[0][1])+" "+str(self.coords[0][2])+"\n")
		# ifile.write("0.0 0.0 0.0\n")
		# ifile.write("InvertSelection\n")
		# ifile.write("mescape\n")

		
		# #create mesh
		# #ifile.write("Meshing Quadratic Quadratic9\n")
		# ifile.write("Utilities Variables Model(QuadraticType) 1\n")
		# ifile.write("mescape\n")
		# ifile.write("Meshing Generate Yes\n")
		# ifile.write(str(self.global_params['excavation_radius']/100*2)+"\n")
		# ifile.write("mescape\n")

		# ifile.write("Data ProblemData -SingleField-\n")
		# ifile.write("Stresses 1\n")
		# ifile.write("mescape\n")
		# ifile.write("Data ProblemData -SingleField-\n")
		# ifile.write("Insitu_Stress 1\n")
		# ifile.write("mescape\n")
		# if( self.global_params['account_for_water'] == "True" ):
			# ifile.write("Data ProblemData -SingleField-\n")
			# ifile.write("Perform_MultiFlow_Analysis 1\n")
			# ifile.write("mescape\n")
			# ifile.write("Data ProblemData -SingleField-\n")
			# ifile.write("Water_Pressure 1\n")
			# ifile.write("mescape\n")
			# ifile.write("Data ProblemData -SingleField-\n")
			# ifile.write("Saturation 1\n")
			# ifile.write("mescape\n")
		# if( self.global_params['linear_elastic_material'] == "False" ):
			# ifile.write("Data ProblemData -SingleField-\n")
			# ifile.write("Plastic_strains 1\n")
			# ifile.write("mescape\n")
		# #Problemtype
		# ifile.write("Files Save\n")
		# ifile.write("mescape\n")
		# ifile.write("Data ProblemData -SingleField-\n")
		# ifile.write("Enable_Gravity 1 \n")
		# ifile.write("mescape\n")
		# ifile.write("Data ProblemData -SingleField-\n")
		# ifile.write("Solver\n")
		# ifile.write("Pardiso\n")
		# ifile.write("mescape\n")
		# ifile.write("mescape\n")
		# ifile.write("Data ProblemData -SingleField-\n")
		# ifile.write("analysis_type\n")
		# ifile.write("quasi-static\n")
		# ifile.write("mescape\n")
		# ifile.write("mescape\n")
		# ifile.write("Utilities Calculate \n")	
		# ifile.write("mescape\n")
		# ifile.write("Files WriteCalcFile\n")	
		# ifile.write("mescape\n")
		# ifile.write("mescape\n")		
		# ifile.write("Files Save\n")
		# ifile.write("mescape\n")
		# ifile.close()

		
		# ostream.write("mescape\n")
		# ostream.write("Files BatchFile\n")
		# ostream.write( self.working_dir + "material_condition_insitu.bch"+"\n")
		# ostream.write("mescape\n")		
		
		# #write calculation file
		# ostream.write("Files WriteCalcFile "+str(self.working_dir+self.global_params['model_name'])+"_insitu_model.gid/"+str(self.global_params['model_name'])+"_insitu_model.dat\n")
		# ostream.write("mescape\n")
		# ostream.write("Quit\n")
		

		# ostream.close()		
		return
	

		
	def AddToSimScript_Lod1(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Insitu SimScript LOD = 1'
		
		ostream.write("##### COORDINATES OF TUNNEL ALIGMNET	#####\n")
		self.coords = HelperMethods.ReadAlignmentFile(self.global_params['model_path']+'/input_files/')
		ostream.write("alignment="+str(self.coords)+"\n")
		ostream.write("for i in range (1, len(alignment)):\n")
		ostream.write("	for j in range (0,3):\n")
		ostream.write("		alignment[i][j]= (float(alignment[i][j])-float(alignment[0][j]))/100.0\n")
		ostream.write("for j in range (0,3):\n")
		ostream.write("	alignment[0][j]= 0.0\n")
		
		if self.soil.lod ==1:
		
			ostream.write("time = 1.0\n")
			ostream.write("delta_time = 100.0\n")
			#sys.path.append(path+model_name+'_insitu_model.gid')
			ostream.write("sys.path.append(path+model_name+'_system.gid')\n")

			return
		ostream.write("time = 1.0\n")

		ostream.write("delta_time = 100.0\n")
		
		
#### OLD APROACH - SIMPLIFIED GEOMETRY OF THE INSITY MODEL
		#ostream.write("sys.path.append(path+model_name+'_insitu_model.gid')\n")
		#ostream.write("sys.path.append(path+model_name+'_system.gid')\n")
		#ostream.write("geology_insitu_include = __import__(model_name+'_insitu_model_include')\n")
		#ostream.write("model_insitu = geology_insitu_include.Model(model_name+'_insitu_model',path+'/'+model_name+'_insitu_model.gid/')\n")

		
#### OLD APROACH - IDENTICAL GEOMETRY OF THE INSITY MODEL		
		# ostream.write("sys.path.append(path+model_name+'_insitu_1_model.gid')\n")
		# ostream.write("sys.path.append(path+model_name+'_system.gid')\n")
		# ostream.write("geology_insitu_include = __import__(model_name+'_insitu_1_model_include')\n")
		# ostream.write("model_insitu = geology_insitu_include.Model(model_name+'_insitu_1_model',path+'/'+model_name+'_insitu_1_model.gid/')\n")

		
#### NEW APROACH - SYSTEM MODEL IS THE INSITY MODEL		
		#ostream.write("sys.path.append(path+model_name+'_insitu_1_model.gid')\n")
		ostream.write("sys.path.append(path+model_name+'_system.gid')\n")
		ostream.write("geology_insitu_include = __import__(model_name+'_system_include')\n")
		ostream.write("model_insitu = geology_insitu_include.Model(model_name+'_system',path+'/'+model_name+'_system.gid/')\n")
		
		ostream.write("model_insitu.InitializeModel()\n")
#		ostream.write("if( write_to_database == False ):\n")
#		ostream.write("	import output_utility_2\n")

		ostream.write("from soil_properties_utility import *\n")
		ostream.write("spu = SoilPropertiesUtility(matfile)\n")
		ostream.write("for element in model_insitu.layer_sets['ground']:\n")
		ostream.write("	if element in model_insitu.model_part.Elements:\n")
		ostream.write("		spu.SetMaterialProperties( model_insitu.model_part, model_insitu.model_part.Elements[element] )\n")
		ostream.write("for layer, layer_set in model_insitu.layer_sets.iteritems():\n")
		ostream.write("	if 'excavation' in layer:\n")
		ostream.write("		for element in layer_set:\n")
		ostream.write("			if element in model_insitu.model_part.Elements:\n")
		ostream.write("				spu.SetMaterialProperties( model_insitu.model_part, model_insitu.model_part.Elements[element] )\n")
		
		
				

		#ostream.write("x0=0.0\n")
		#ostream.write("y0=0.0\n")
		#ostream.write("z0=0.0\n")
		m=self.global_params['TBM_offset']
		ostream.write("x0_min=float(alignment["+str(m)+"][0])\n")
		ostream.write("x0_max=float(alignment["+str(m)+"][0])\n")
		ostream.write("y0_min=float(alignment["+str(m)+"][1])\n")
		ostream.write("y0_max=float(alignment["+str(m)+"][1])\n")
		ostream.write("z0=float(alignment["+str(m)+"][2])\n")
		ostream.write("\n")		
		ostream.write("for node in model_insitu.model_part.Nodes:\n")
		ostream.write("	if node.Z0<z0:\n")
		ostream.write("		z0=node.Z0\n")
		ostream.write("	if node.X0>x0_max:\n")
		ostream.write("		x0_max=node.X0\n")
		ostream.write("	elif node.X0<x0_min:\n")
		ostream.write("		x0_min=node.X0\n")
		ostream.write("	if node.Y0>y0_max:\n")
		ostream.write("		y0_max=node.Y0\n")
		ostream.write("	elif node.Y0<y0_min:\n")
		ostream.write("		y0_min=node.Y0\n")
		
#### NEW APROACH - SYSTEM MODEL IS THE INSITY MODEL	
		if self.building.lod>1:
			ostream.write("#turn off the building and foundation layer\n")
			ostream.write("for e in model_insitu.layer_sets['building']:\n")
			ostream.write("	if e in model_insitu.model_part.Elements:\n")
			ostream.write("		model_insitu.model_part.Elements[e].SetValue(ACTIVATION_LEVEL, -1)\n")
			ostream.write("for e in model_insitu.layer_sets['foundation']:\n")
			ostream.write("	if e in model_insitu.model_part.Elements:\n")
			ostream.write("		model_insitu.model_part.Elements[e].SetValue(ACTIVATION_LEVEL, -1)\n")
		if self.lining.lod>1:
			ostream.write("#turn off the grouting and lining\n")
			ostream.write("for layer, elem_set in model_insitu.layer_sets.iteritems():\n")
			ostream.write("	if 'grouting' in layer:\n")
			ostream.write("		for e in elem_set:\n")
			ostream.write("			 if e in model_insitu.model_part.Elements:\n")
			ostream.write("				model_insitu.model_part.Elements[e].SetValue(ACTIVATION_LEVEL, -1)\n")
			ostream.write("for layer, elem_set in model_insitu.layer_sets.iteritems():\n")
			ostream.write("	if 'lining' in layer:\n")
			ostream.write("		for e in elem_set:\n")
			ostream.write("			 if e in model_insitu.model_part.Elements:\n")
			ostream.write("				 model_insitu.model_part.Elements[e].SetValue(ACTIVATION_LEVEL, -1)\n")
		if self.tbm.lod>1 and self.lining.lod>1:
			ostream.write("#turn off the TBM and foundation layer\n")
			ostream.write("for e in model_insitu.layer_sets['shield']:\n")
			ostream.write("	if e in model_insitu.model_part.Elements:\n")
			ostream.write("		model_insitu.model_part.Elements[e].SetValue(ACTIVATION_LEVEL, -1)\n")

		ostream.write("#turn on all the excavation\n")
		ostream.write("for layer, layer_set in model_insitu.layer_sets.iteritems():\n")
		ostream.write("	if 'excavation' in layer:\n")
		ostream.write("		for element in layer_set:\n")
		ostream.write("			if element in model_insitu.model_part.Elements:\n")
		ostream.write("				model_insitu.model_part.Elements[element].SetValue(ACTIVATION_LEVEL, 0)\n")

				
		ostream.write("tol = 1.0e-1\n")
		
		ostream.write("for node in model_insitu.model_part.Nodes:\n")
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
		
		# if self.building.lod>1:
			# ostream.write("foundation_nodes=[]\n")
			# ostream.write("for node_id in model_insitu.layer_nodes_sets['foundation']:\n")
			# ostream.write("	node = model_insitu.model_part.Nodes[node_id]\n")	
			# ostream.write("	foundation_nodes.append(node_id)\n")
			# ostream.write("\n")		
			# ostream.write("Epltu = EmbeddedNodePenaltyTyingUtility()\n")
			# ostream.write("links1 = Epltu.SetUpTyingLinks( model_insitu.model_part, foundation_nodes, model_insitu.layer_sets['ground'] )\n")
			# ostream.write("for cond in links1:\n")
			# ostream.write("	cond.SetValue(INITIAL_PENALTY, 1.0e10)\n")
		
		ostream.write("#Prescribe Hydrostratic Pressure\n")
		ostream.write("free_node_list_water_insitu = []\n")
		ostream.write("free_node_list_air_insitu = []\n")
		ostream.write("if( account_for_water == True ):\n")
		ostream.write("	z_coord_of_groundwater_table= ground_water_table\n")
		#ostream.write("	z_coord_of_groundwater_table= z0_max\n")
		ostream.write("	for node in model_insitu.model_part.Nodes:\n")
		ostream.write("		if( node.Z > z_coord_of_groundwater_table ):\n")
		ostream.write("			node.Fix( WATER_PRESSURE )\n")
		ostream.write("	model_insitu.FixPressureNodes(free_node_list_water_insitu, free_node_list_air_insitu)\n")
		ostream.write("	model_insitu.ApplyInsituWaterPressure(free_node_list_water_insitu, free_node_list_air_insitu, z_coord_of_groundwater_table, 9.81)\n")
		
		if self.building.lod ==1:		
			ostream.write("def InsidePointolygon(Point, Polygon):\n")
			ostream.write("	cn = 0    # the crossing number counter\n")

			ostream.write("	Polygon = tuple(Polygon[:])+(Polygon[0],)\n")

			ostream.write("	# loop through all edges of the Polygon\n")
			ostream.write("	for i in range(len(Polygon)-1):   # edge from V[i] to V[i+1]\n")
			ostream.write("		if ((Polygon[i][1] <= Point[1] and Polygon[i+1][1] > Point[1])   # an upward crossing\n")
			ostream.write("			or (Polygon[i][1] > Point[1] and Polygon[i+1][1] <= Point[1])):  # a downward crossing\n")
			ostream.write("			# comPointute the actual edge-ray intersect x-coordinate\n")
			ostream.write("			vt = (Point[1] - Polygon[i][1]) / float(Polygon[i+1][1] - Polygon[i][1])\n")
			ostream.write("			if Point[0] < Polygon[i][0] + vt * (Polygon[i+1][0] - Polygon[i][0]): # Point[0] < intersect\n")
			ostream.write("				cn += 1  # a valid crossing of y=Point[1] right of Point[0]\n")

			ostream.write("	return cn % 2   # 0 if even (out), and 1 if odd (in)\n")
			
			####add top nodes for the output
			ostream.write("tol=0.1	\n")
			ostream.write("top_nodes_insitu=[]\n")
			ostream.write("for node_id in model_insitu.layer_nodes_sets['ground']:\n")
			ostream.write("	node = model_insitu.model_part.Nodes[node_id]\n")
			ostream.write("	if node.Z0>(ground_water_table-tol):\n")
			ostream.write("		top_nodes_insitu.append(node_id)\n")
			ostream.write("for node_id in model_insitu.layer_nodes_sets['surface']:\n")
			ostream.write("	node = model_insitu.model_part.Nodes[node_id]\n")
			ostream.write("	if node.Z0>(ground_water_table-tol):\n")
			ostream.write("		top_nodes_insitu.append(node_id)\n")		


			self.params=HelperMethods.ReadParamFile (self.global_params['model_path']+'/input_files/building.dat')
			#self.coords = HelperMethods.ReadAlignmentFile(self.global_params['model_path']+'/input_files/')	
			b_coords = HelperMethods.ReadBuildingFile(self.global_params['model_path']+'/sat_files/buildings/')
			#print(b_coords)
			for i in range (0,len(b_coords)):
				b_coords[i][0]=(b_coords[i][0]-self.coords[0][0])/100.0
				b_coords[i][1]=(b_coords[i][1]-self.coords[0][1])/100.0
#			print(b_coords)
			
			ostream.write("b_coords="+str(b_coords)+"	\n")		
			ostream.write("building_load_insitu=[]	\n")
			ostream.write("point=[0.0,0.0]	\n")
			ostream.write("for node_id in top_nodes_insitu:\n")
			ostream.write("	node = model_insitu.model_part.Nodes[node_id]\n")
			ostream.write("	point[0]=node.X\n")
			ostream.write("	point[1]=node.Y\n")
			ostream.write("	if (InsidePointolygon(point, b_coords)==1):\n")
			ostream.write("		building_load_insitu.append(node_id)\n")
			
			
			
			n_col_x=self.params['n_col_x']
			n_col_y=self.params['n_col_y']
			n_floors=self.params['n_floors']
			#THIS IS CORRECTED TO MAKE DIFFERENCE BETWEEN LOD1 LOD2 AND LOD3
			ro_build=self.params['ro_build']/4.0
			x_span=self.params['x_span']/100.0
			y_span=self.params['y_span']/100.0
			h_floor=self.params['h_floor']/100.0
			

			#print("do x_span. y_span_f_span")
			
			#pressure=(n_col_x-1)*x_span*(n_col_y-1)*y_span*(n_floors-1)*h_floor*ro_build*9.81

			pressure=(n_floors-1)*h_floor*ro_build*9.81
			ostream.write("building_pressure="+str(pressure)+"\n")
			ostream.write("for node in building_load_insitu:\n")
			#ostream.write("	pressure = "+str(pressure)+"\n")
			ostream.write("	model_insitu.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_Z,-building_pressure)\n")

		ostream.write("print '##### Solve model without prestress #####'\n")
		#ostream.write("for node in model_insitu.top_surface_nodes:\n")
		#ostream.write("	pressure = surface_pressure\n")
		#ostream.write("	model_insitu.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_Z,pressure)\n")
		ostream.write("time = time+delta_time\n")
		ostream.write("model_insitu.Solve( time, 0, 0, 0, 0 )\n")
		ostream.write("model_insitu.WriteOutput( time )\n")

		ostream.write("##Set InSitu Stress in one Step (Attention model must behave kinematic linear [no dependencie on deformations])\n")
		ostream.write("time = time+delta_time\n")
		ostream.write("isu = InSituStressUtility()\n")
		ostream.write("isu.SetInSituStressFromCurrentStress( model_insitu.model_part, model_insitu.model_part.ProcessInfo )\n")
		ostream.write("model_insitu.Solve( time, 0, 0, 0, 0 )        \n")
		ostream.write("model_insitu.WriteOutput(time)    \n")
		ostream.write("print ('~~~~~~~~~~~~~~ STEP DONE: APPLICATION OF INSITU STRESS ~~~~~~~~~~~~~~\')\n")
	
		ostream.write("##Model is initialized with InSitu Stress, the next step is only to check the residual displacements\n")
		ostream.write("time = time+delta_time\n")
		ostream.write("model_insitu.Solve( time, 0, 0, 0, 0 )      \n")
		ostream.write("model_insitu.WriteOutput(time)    \n")

		ostream.write("max_disp = 0.0\n")
		ostream.write("for node in model_insitu.model_part.Nodes:\n")
		ostream.write("	for direction in range(0,3):\n")
		ostream.write("		if( abs(float(node.GetSolutionStepValue(DISPLACEMENT)[direction])) > max_disp ):\n")
		ostream.write("			max_disp = abs(float(node.GetSolutionStepValue(DISPLACEMENT)[direction])) \n")
		return

		
		return