#simulation script for multi_build_lod_optim
###SATBIM - 
##################################################################
## This is a Simulation sctipt for SATBIM tunnel submodel    #####
###For calulation KRATOS FE framework                        #####
##################################################################
###							                                 #####
## ATTENTION: before running simulation script  	         #####
## make sure that yopur geometry and FE mesh is regular      #####
##################################################################
import sys
import os
import math
kratos_root_path = os.environ['KRATOS_ROOT_PATH']


#importing Kratos main library
from KratosMultiphysics import *
from KratosMultiphysics.StructuralApplication import *
from KratosMultiphysics.EkateAuxiliaryApplication import *
from KratosMultiphysics.ExternalSolversApplication import *
from KratosMultiphysics.MKLSolversApplication import *
from KratosMultiphysics.MortarApplication import *

kernel = Kernel()   #defining kernelparams = {}
path = os.getcwd() + '/'
model_name = 'multi_build_lod_optim'
matfile = 'matfile.dat'
linear_elastic_material = False
time_advance = 1000
time_ring_construction = 1200
excavation_radius = 5.0
account_for_water = True
ground_water_table = 17.5
grouting_pressure = 200000
grouting_gradient = 10000
support_pressure = 180000
support_gradient = 15000
number_of_slices = 78
number_of_excavation_steps = 73
initial_grouting_surface_index = 2
round_length = 2.5
TBM_offset = 5
lining_offset = 3
grouting_offset = 2
move_steps_per_round_length = 1
steps_per_down_time = 1
segment_number = 8
write_to_database = True


##### COORDINATES OF TUNNEL ALIGMNET	#####
alignment=[[-2093.20242808, 3935.25216918, 14000.0], [-1843.20242808, 3936.0334268, 14000.0], [-1593.20242808, 3935.25216918, 14000.0], [-1343.20242808, 3936.0334268, 14000.0], [-1093.20242808, 3935.25216918, 14000.0], [-843.202428085, 3936.0334268, 14000.0], [-593.202428085, 3935.25216918, 14000.0], [-343.202428085, 3936.0334268, 14000.0], [-93.2024280846, 3935.25216918, 14000.0], [156.797571915, 3936.0334268, 14000.0], [406.797571915, 3935.25216918, 14000.0], [656.797571915, 3936.0334268, 14000.0], [906.797571915, 3935.25216918, 14000.0], [1156.79757192, 3936.0334268, 14000.0], [1406.79757192, 3935.25216918, 14000.0], [1656.79757192, 3936.0334268, 14000.0], [1906.79757192, 3935.25216918, 14000.0], [2156.79757192, 3936.0334268, 14000.0], [2406.79757192, 3935.25216918, 14000.0], [2656.79757192, 3936.0334268, 14000.0], [2906.79757192, 3935.25216918, 14000.0], [3156.79757192, 3936.0334268, 14000.0], [3406.79757192, 3935.25216918, 14000.0], [3656.79757192, 3936.0334268, 14000.0], [3906.79757192, 3935.25216918, 14000.0], [4156.79757192, 3936.0334268, 14000.0], [4406.79757192, 3935.25216918, 14000.0], [4656.79757192, 3936.0334268, 14000.0], [4906.79757192, 3935.25216918, 14000.0], [5156.79757192, 3936.0334268, 14000.0], [5406.79757192, 3935.25216918, 14000.0], [5656.79757192, 3936.0334268, 14000.0], [5906.79757192, 3935.25216918, 14000.0], [6156.79757192, 3936.0334268, 14000.0], [6406.79757192, 3935.25216918, 14000.0], [6656.79757192, 3936.0334268, 14000.0], [6906.79757192, 3935.25216918, 14000.0], [7156.79757192, 3936.0334268, 14000.0], [7406.79757192, 3935.25216918, 14000.0], [7656.79757192, 3936.0334268, 14000.0], [7906.79757192, 3935.25216918, 14000.0], [8156.79757192, 3936.0334268, 14000.0], [8406.79757192, 3935.25216918, 14000.0], [8656.79757192, 3936.0334268, 14000.0], [8906.79757192, 3935.25216918, 14000.0], [9156.79757192, 3936.0334268, 14000.0], [9406.79757192, 3935.25216918, 14000.0], [9656.79757192, 3936.0334268, 14000.0], [9906.79757192, 3935.25216918, 14000.0], [10156.7975719, 3936.0334268, 14000.0], [10406.7975719, 3935.25216918, 14000.0], [10656.7975719, 3936.0334268, 14000.0], [10906.7975719, 3935.25216918, 14000.0], [11156.7975719, 3936.0334268, 14000.0], [11406.7975719, 3935.25216918, 14000.0], [11656.7975719, 3936.0334268, 14000.0], [11906.7975719, 3935.25216918, 14000.0], [12156.7975719, 3936.0334268, 14000.0], [12406.7975719, 3935.25216918, 14000.0], [12656.7975719, 3936.0334268, 14000.0], [12906.7975719, 3935.25216918, 14000.0], [13156.7975719, 3936.0334268, 14000.0], [13406.7975719, 3935.25216918, 14000.0], [13656.7975719, 3936.0334268, 14000.0], [13906.7975719, 3935.25216918, 14000.0], [14156.7975719, 3936.0334268, 14000.0], [14406.7975719, 3935.25216917, 14000.0], [14656.7975719, 3936.0334268, 14000.0], [14906.7975719, 3935.25216917, 14000.0], [15156.7975719, 3936.0334268, 14000.0], [15406.7975719, 3935.25216917, 14000.0], [15656.7975719, 3936.0334268, 14000.0], [15906.7975719, 3935.25216917, 14000.0], [16156.7975719, 3936.0334268, 14000.0], [16406.7975719, 3935.25216917, 14000.0], [16656.7975719, 3936.0334268, 14000.0], [16906.7975719, 3935.25216917, 14000.0], [17156.7975719, 3936.0334268, 14000.0], [17406.7975719, 3935.25216917, 14000.0]]
for i in range (1, len(alignment)):
	for j in range (0,3):
		alignment[i][j]= (float(alignment[i][j])-float(alignment[0][j]))/100.0
for j in range (0,3):
	alignment[0][j]= 0.0
time = 1.0
delta_time = 100.0
sys.path.append(path+model_name+'_system.gid')
geology_insitu_include = __import__(model_name+'_system_include')
model_insitu = geology_insitu_include.Model(model_name+'_system',path+'/'+model_name+'_system.gid/')
model_insitu.InitializeModel()
from soil_properties_utility import *
spu = SoilPropertiesUtility(matfile)
for element in model_insitu.layer_sets['ground']:
	if element in model_insitu.model_part.Elements:
		spu.SetMaterialProperties( model_insitu.model_part, model_insitu.model_part.Elements[element] )
for layer, layer_set in model_insitu.layer_sets.iteritems():
	if 'excavation' in layer:
		for element in layer_set:
			if element in model_insitu.model_part.Elements:
				spu.SetMaterialProperties( model_insitu.model_part, model_insitu.model_part.Elements[element] )
x0_min=float(alignment[5][0])
x0_max=float(alignment[5][0])
y0_min=float(alignment[5][1])
y0_max=float(alignment[5][1])
z0=float(alignment[5][2])

for node in model_insitu.model_part.Nodes:
	if node.Z0<z0:
		z0=node.Z0
	if node.X0>x0_max:
		x0_max=node.X0
	elif node.X0<x0_min:
		x0_min=node.X0
	if node.Y0>y0_max:
		y0_max=node.Y0
	elif node.Y0<y0_min:
		y0_min=node.Y0
#turn off the building and foundation layer
for e in model_insitu.layer_sets['building']:
	if e in model_insitu.model_part.Elements:
		model_insitu.model_part.Elements[e].SetValue(ACTIVATION_LEVEL, -1)
for e in model_insitu.layer_sets['foundation']:
	if e in model_insitu.model_part.Elements:
		model_insitu.model_part.Elements[e].SetValue(ACTIVATION_LEVEL, -1)
#turn off the grouting and lining
for layer, elem_set in model_insitu.layer_sets.iteritems():
	if 'grouting' in layer:
		for e in elem_set:
			 if e in model_insitu.model_part.Elements:
				model_insitu.model_part.Elements[e].SetValue(ACTIVATION_LEVEL, -1)
for layer, elem_set in model_insitu.layer_sets.iteritems():
	if 'lining' in layer:
		for e in elem_set:
			 if e in model_insitu.model_part.Elements:
				 model_insitu.model_part.Elements[e].SetValue(ACTIVATION_LEVEL, -1)
#turn off the TBM and foundation layer
for e in model_insitu.layer_sets['shield']:
	if e in model_insitu.model_part.Elements:
		model_insitu.model_part.Elements[e].SetValue(ACTIVATION_LEVEL, -1)
#turn on all the excavation
for layer, layer_set in model_insitu.layer_sets.iteritems():
	if 'excavation' in layer:
		for element in layer_set:
			if element in model_insitu.model_part.Elements:
				model_insitu.model_part.Elements[element].SetValue(ACTIVATION_LEVEL, 0)
tol = 1.0e-1
for node in model_insitu.model_part.Nodes:
	if node.Z0  < z0 +tol:
		node.Fix(DISPLACEMENT_Z)
		node.SetSolutionStepValue(DISPLACEMENT_Z, 0.0)
		node.SetSolutionStepValue(DISPLACEMENT_EINS_Z, 0.0)
		node.SetSolutionStepValue(DISPLACEMENT_NULL_Z, 0.0)
	if (node.X0> (x0_max-tol)) or (node.X0< (x0_min+tol)):
		node.Fix(DISPLACEMENT_X)
		node.SetSolutionStepValue(DISPLACEMENT_X, 0.0)
		node.SetSolutionStepValue(DISPLACEMENT_EINS_X, 0.0)
		node.SetSolutionStepValue(DISPLACEMENT_NULL_X, 0.0)
	if (node.Y0> (y0_max-tol)) or (node.Y0< (y0_min+tol)):
		node.Fix(DISPLACEMENT_Y)
		node.SetSolutionStepValue(DISPLACEMENT_Y, 0.0)
		node.SetSolutionStepValue(DISPLACEMENT_EINS_Y, 0.0)
		node.SetSolutionStepValue(DISPLACEMENT_NULL_Y, 0.0)
#Prescribe Hydrostratic Pressure
free_node_list_water_insitu = []
free_node_list_air_insitu = []
if( account_for_water == True ):
	z_coord_of_groundwater_table= ground_water_table
	for node in model_insitu.model_part.Nodes:
		if( node.Z > z_coord_of_groundwater_table ):
			node.Fix( WATER_PRESSURE )
	model_insitu.FixPressureNodes(free_node_list_water_insitu, free_node_list_air_insitu)
	model_insitu.ApplyInsituWaterPressure(free_node_list_water_insitu, free_node_list_air_insitu, z_coord_of_groundwater_table, 9.81)
print '##### Solve model without prestress #####'
time = time+delta_time
model_insitu.Solve( time, 0, 0, 0, 0 )
model_insitu.WriteOutput( time )
##Set InSitu Stress in one Step (Attention model must behave kinematic linear [no dependencie on deformations])
time = time+delta_time
isu = InSituStressUtility()
isu.SetInSituStressFromCurrentStress( model_insitu.model_part, model_insitu.model_part.ProcessInfo )
model_insitu.Solve( time, 0, 0, 0, 0 )        
model_insitu.WriteOutput(time)    
print ('~~~~~~~~~~~~~~ STEP DONE: APPLICATION OF INSITU STRESS ~~~~~~~~~~~~~~')
##Model is initialized with InSitu Stress, the next step is only to check the residual displacements
time = time+delta_time
model_insitu.Solve( time, 0, 0, 0, 0 )      
model_insitu.WriteOutput(time)    
max_disp = 0.0
for node in model_insitu.model_part.Nodes:
	for direction in range(0,3):
		if( abs(float(node.GetSolutionStepValue(DISPLACEMENT)[direction])) > max_disp ):
			max_disp = abs(float(node.GetSolutionStepValue(DISPLACEMENT)[direction])) 
##### INITIALIZE MODEL	#####
system_include = __import__(model_name+'_system_include')
model1 = system_include.Model(model_name+'_system',path+'/'+model_name+'_system.gid/')
model1.InitializeModel()
initial_reactivation_index = -1235
reactivation_index = -1224
reactivation_index_stressfree = -1225
initial_face_index = 5
########################################################################################
#############	SETUP TYING LINKS PENALTY BETWEEN LINIG AND GROUTING	################
tying_util = MortarTyingUtility
util = MortarTyingUtility()
mortar_links = util.SetupTyingLinkElementBased(model1.model_part, 10, 'tying_link_geometrical_linear_penalty', 'surface tying')
for cond in mortar_links:
	cond.SetValue(INITIAL_PENALTY, 1.0e11)

########################################################################################
#############	SETUP CONTACT LINKS PENALTY BETWEEN SHIELD AND SOIL	##################
model1.solver.solver.contact_tying_indices = {}
model1.solver.solver.Parameters['penalty'] = {}
model1.solver.solver.Parameters['friction_coefficient'] = {}
model1.solver.solver.contact_tying_indices[1] = 'contact_link_kinematic_linear_penalty_no_linearized'
#model1.solver.solver.contact_tying_indices[1] = 'contact_link_kinematic_linear_penalty'
model1.solver.solver.mortar_contact_utility.SetValue(MAXIMAL_DETECTION_DISTANCE, 0.1)
model1.solver.solver.mortar_contact_utility.SetValue(GAP_TOLERANCE, 1.0e-10)
model1.solver.solver.Parameters['penalty'][1] = 1.0e9
model1.solver.solver.Parameters['friction_coefficient'][1] = 0.0
model1.solver.solver.Parameters['max_active_set_iter'] = 1
model1.solver.solver.Parameters['predict_local_point_method'] = 2
model1.solver.solver.Parameters['solution_strategy'] = 'solve active-set penalty'
model1.solver.solver.Parameters['integration_type'] = 'element based'
model1.solver.solver.Parameters['test_linearization'] = False
model1.solver.solver.Parameters['test_linearization_disp'] = 1.0e-7
model1.solver.solver.Parameters['test_linearization_tol'] = 1.0e-6
##### VOLUME LOSS #####
volume_loss =0.5

##### SET UP SOIL PROPERTIES #####
for element in model1.layer_sets['ground']:
	spu.SetMaterialProperties( model1.model_part, model1.model_part.Elements[element] )
for step in range(1,number_of_slices+1):
	excavation_layer = 'excavation_'+str(step)
	for element in model1.layer_sets[excavation_layer]:
		spu.SetMaterialProperties( model1.model_part, model1.model_part.Elements[element] )
print('##### TRANSFERRING INSITU STRESS #####')
vtu = VariableTransferUtility(MKLPardisoSolver())
vtu.TransferPrestressIdentically( model_insitu.model_part, model1.model_part )

if( account_for_water == True ):
	for node in model1.model_part.Nodes:
		if( node.Z > z_coord_of_groundwater_table ):
			node.Fix( WATER_PRESSURE )

##reset to Zero in-situ stress in shield, lining and grouting
element_list = []
for element in model1.layer_sets['shield']:
	if element in model1.model_part.Elements:
		element_list.append( element )
for element in model1.layer_sets['building']:
	if element in model1.model_part.Elements:
		element_list.append( element )
for step in range(1,number_of_slices+1):
	for element in model1.layer_sets['lining_'+str(step)]:
		if element in model1.model_part.Elements:
			element_list.append( element )
	for element in model1.layer_sets['grouting_'+str(step)]:
		if element in model1.model_part.Elements:
			element_list.append( element )
isu.ScalePrestress( model1.model_part, element_list, len(element_list), 0.0 )
z0_f=10000000
for node_id in model1.layer_nodes_sets['foundation']:
	node = model1.model_part.Nodes[node_id]
	if node.Z0<z0_f:
		z0_f=node.Z0
tol=0.1
foundation_nodes=[]
for node_id in model1.layer_nodes_sets['foundation']:
	node = model1.model_part.Nodes[node_id]
	if node.Z0<(z0_f+tol):
		foundation_nodes.append(node_id)

Epltu = EmbeddedNodePenaltyTyingUtility()
links1 = Epltu.SetUpTyingLinks( model1.model_part, foundation_nodes, model1.layer_sets['ground'] )
for cond in links1:
	cond.SetValue(INITIAL_PENALTY, 1.0e10)
shield_nodes=[]
for node in model1.layer_nodes_sets['shield']:
	if node in model1.model_part.Nodes:
		shield_nodes.append(node)
for node in model1.layer_nodes_sets['shield_outter_surface']:
	if node in model1.model_part.Nodes:
		shield_nodes.append(node)

print('##### ASSIGN HYDROSTATIC PORE PRESSURE #####')
#Prescribe Hydrostratic Pressure
free_node_list_water1 = []
free_node_list_air1 = []
model1.FixPressureNodes(free_node_list_water1, free_node_list_air1)

print('##### APPLY INSITU STRESS INCREMENTAL #####')
time = 100.0
delta_time = 180.0

if( account_for_water == True ):
	model1.ApplyInsituWaterPressure(free_node_list_water1, free_node_list_air1, z_coord_of_groundwater_table, 9.81)
	model1.SetReferenceWaterPressure()
print '######## DO THE FIRST STEP #############'
heading_face_pressure = support_pressure
heading_face_gradient = support_gradient
for node in model1.node_groups['heading_face_'+str(initial_face_index)]:
	initial_pressure = heading_face_pressure
	depth = model1.model_part.Nodes[node].Z
	pressure = initial_pressure-depth*heading_face_gradient
	model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,pressure)
lining_face_index= 3
for node in model1.layer_nodes_sets['lining_surface_'+str(lining_face_index)]:
	initial_pressure = heading_face_pressure
	depth = model1.model_part.Nodes[node].Z
	pressure = initial_pressure-depth*heading_face_gradient
	model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,-pressure)     	
	if( account_for_water == True ):
		model1.model_part.Nodes[node].Fix(WATER_PRESSURE)
		model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE,pressure)
		model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_NULL,pressure)
		model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_EINS,pressure)
for node in shield_nodes:
	if node in model1.model_part.Nodes:
		model1.model_part.Nodes[node].Fix(DISPLACEMENT_X)
		model1.model_part.Nodes[node].Fix(DISPLACEMENT_Y)
		model1.model_part.Nodes[node].Fix(DISPLACEMENT_Z)
		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_X, 0.0)
		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_EINS_X, 0.0)
		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_NULL_X, 0.0)
		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_Y, 0.0)
		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_EINS_Y, 0.0)
		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_NULL_Y, 0.0)
		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_Z, 0.0)
		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_EINS_Z, 0.0)
		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_NULL_Z, 0.0)
tol = 0.1
for node in model1.model_part.Nodes:
	if node.Z0  < z0 +tol:
		node.Fix(DISPLACEMENT_Z)
		node.SetSolutionStepValue(DISPLACEMENT_Z, 0.0)
		node.SetSolutionStepValue(DISPLACEMENT_EINS_Z, 0.0)
		node.SetSolutionStepValue(DISPLACEMENT_NULL_Z, 0.0)
	if (node.X0> (x0_max-tol)) or (node.X0< (x0_min+tol)):
		node.Fix(DISPLACEMENT_X)
		node.SetSolutionStepValue(DISPLACEMENT_X, 0.0)
		node.SetSolutionStepValue(DISPLACEMENT_EINS_X, 0.0)
		node.SetSolutionStepValue(DISPLACEMENT_NULL_X, 0.0)
	if (node.Y0> (y0_max-tol)) or (node.Y0< (y0_min+tol)):
		node.Fix(DISPLACEMENT_Y)
		node.SetSolutionStepValue(DISPLACEMENT_Y, 0.0)
		node.SetSolutionStepValue(DISPLACEMENT_EINS_Y, 0.0)
		node.SetSolutionStepValue(DISPLACEMENT_NULL_Y, 0.0)
###########################################SOLVE FOR THE FORST TIME################################
###################################################################################################
deactivation_index=0
model1.Solve( time, 0, deactivation_index, initial_reactivation_index, reactivation_index)
model1.WriteOutput( time )		

if( account_for_water == True ):
	model1.FreePressureNodes( free_node_list_water1, free_node_list_air1) 

time=time+delta_time
model1.Solve( time, 0, deactivation_index, initial_reactivation_index, reactivation_index)
model1.WriteOutput( time )		
delta_time_advance = time_advance
delta_time_downtime = time_ring_construction
one_ring= round_length
move_steps= move_steps_per_round_length
exc_steps= steps_per_down_time
move_delta_time= delta_time_advance/float(move_steps)
exc_delta_time= delta_time_downtime/float(exc_steps)
face_index = initial_face_index
grouting_surface_index = initial_grouting_surface_index

advance = 0.0
#print '######## DO THE FIRST STEP WITH FIXED MACHINE  #############'
for node in model1.node_groups['shield']:
	if node in model1.model_part.Nodes:
		model1.model_part.Nodes[node].Fix(DISPLACEMENT_Z)
		model1.model_part.Nodes[node].SetSolutionStepValue(DISPLACEMENT_Z, 0.0)
init=TBM_offset 
disp_vector=[]
insert_tbm=[]
for j in range (0,3):
	insert_tbm.append(alignment[TBM_offset-1][j])
for i in range (TBM_offset-2, len(alignment)):
	disp_vector.append(alignment[i])
for i in range (1, len(disp_vector)):
	for j in range (0,3):
		disp_vector[i][j]= (float(disp_vector[i][j])-float(disp_vector[0][j]))
for j in range (0,3):
	disp_vector[0][j]= 0.0
disp_x=0.0
disp_y=0.0

delta_x=(float(disp_vector[1][0])-float(disp_vector[0][0]))
delta_y=(float(disp_vector[1][1])-float(disp_vector[0][1]))
alpha_last=math.atan(delta_y/delta_x)		
beta=0
for step in range(1,number_of_excavation_steps+1):
	#move
	print('ready for next step')
	print '#########################################'
	print '############# MOVE MACHINE  #############'
	print '#########################################'
	delta_x=(float(disp_vector[step+1][0])-float(disp_vector[step][0]))
	delta_y=(float(disp_vector[step+1][1])-float(disp_vector[step][1]))
	alpha=math.atan(delta_y/delta_x)
	delta_alpha=alpha-alpha_last
	alpha_last=alpha
	beta=beta+delta_alpha


	for moving_step in range (0,move_steps):
		time = time + move_delta_time
		advance = advance +  one_ring/float(move_steps)
		disp_x = disp_x +  delta_x/float(move_steps)
		disp_y = disp_y +  delta_y/float(move_steps)
		print('--- moving to ' +str(disp_x)+' ---') 


		##for node in model1.node_groups['shield_advance']:
		for node_id in shield_nodes:
			node = model1.model_part.Nodes[node_id]
			x=node.X0-float(insert_tbm[0])
			y=node.Y0-float(insert_tbm[1])
			x1=x*math.cos(beta)-y*math.sin(beta)+float(insert_tbm[0])-node.X0
			y1=x*math.sin(beta)+y*math.cos(beta)+float(insert_tbm[1])-node.Y0
			dx=disp_x+x1
			dy=disp_y+y1
			node.SetSolutionStepValue(DISPLACEMENT_Y, dy)
			node.SetSolutionStepValue(DISPLACEMENT_EINS_Y, dy)
			node.SetSolutionStepValue(DISPLACEMENT_NULL_Y, dy)
			node.SetSolutionStepValue(DISPLACEMENT_X, dx)
			node.SetSolutionStepValue(DISPLACEMENT_EINS_X, dx)
			node.SetSolutionStepValue(DISPLACEMENT_NULL_X, dx)



		model1.model_part.CloneTimeStep( time )
		model1.solver.Solve()
		model1.WriteOutput( time )


	print('--- moving step done ['+str(time)+'] ---') 
	print '#########################################'
	print '############# MACHINE MOVED  ############'
	print '#########################################'

	print('#############')
	print(' excavating...')
	print('#############')
	#excavate
	print('deactivating and reactivating ...')
	deactivation_index = deactivation_index + 1

	if(grouting_surface_index>=3):
			for node in model1.layer_nodes_sets[grouting_face_layer]:
				if( account_for_water == True ):
					model1.model_part.Nodes[node].Free(WATER_PRESSURE)
				model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,0.0)
	if(lining_face_index>=3):
			for node in model1.layer_nodes_sets['lining_surface_'+str(lining_face_index)]:
				model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,0.0)

	lining_face_index= lining_face_index+1    
	grouting_surface_index= grouting_surface_index+1
	face_index = face_index+1

	grouting_face_layer = 'grouting_surface_'+str(grouting_surface_index)
	for node in model1.layer_nodes_sets[grouting_face_layer]:
			pressure = grouting_pressure-(model1.model_part.Nodes[node].Z)*grouting_gradient
			if( account_for_water == True ):
				model1.model_part.Nodes[node].Fix(WATER_PRESSURE)
				model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE,pressure)
				model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_EINS,pressure)
				model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_NULL,pressure)
			model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,-pressure)
			
	for node in model1.layer_nodes_sets['lining_surface_'+str(lining_face_index)]:
		initial_pressure = heading_face_pressure
		depth = model1.model_part.Nodes[node].Z
		pressure = initial_pressure-depth*heading_face_gradient
		model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,-pressure)    

	if face_index>1:
		old_face_layer = 'heading_face_'+str(face_index-1)
		for node in model1.node_groups[old_face_layer]:
				model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,0.0)
				if( account_for_water == True ):
					model1.model_part.Nodes[node].Free( WATER_PRESSURE )
	current_face_layer = 'heading_face_'+str(face_index)
	for node in model1.node_groups[current_face_layer]:
			pressure = heading_face_pressure-(model1.model_part.Nodes[node].Z)*heading_face_gradient
			model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,pressure)
			if( account_for_water == True ):
				model1.model_part.Nodes[node].Fix( WATER_PRESSURE )
				model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE,pressure)
				model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_NULL,pressure)
				model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_EINS,pressure)
	#cloning time step
	time = time + exc_delta_time
	reactivation_index_stressfree = reactivation_index_stressfree + 2*segment_number 
	reactivation_index = reactivation_index + 2*7
	#model1.deac.ReactivateStressFree( model1.model_part,initial_reactivation_index , reactivation_index_stressfree )
	model1.deac.ReactivateStressFree( model1.model_part, initial_reactivation_index, reactivation_index )
	model1.deac.Deactivate( model1.model_part, 0, deactivation_index )    
	print('done...')
	print '##### APPLYING FACE PRESSURE #####'
	print '##### FREE OLD PRESSURE FACES #####'

	print '##### APPLY BOUNDARY CONDITIONS AT HEADING FACE #####'

	#solve and consolidate results
	for moving_step in range (0,exc_steps):
		time = time + exc_delta_time
		model1.model_part.CloneTimeStep( time )
		print('solving...')
		model1.solver.Solve()
		model1.WriteOutput( time )
		print('#############')
	print('step '+str(step)+' done.')

print('ALL DONE.')

