#simulation script for Tunnel
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
model_name = 'Tunnel'
matfile = 'matfile.dat'
linear_elastic_material = True
time_advance = 1000
time_ring_construction = 1200
excavation_radius = 5.0
account_for_water = True
ground_water_table = 15.0
grouting_pressure = 200000
grouting_gradient = 10000
support_pressure = 180000
support_gradient = 15000
number_of_slices = 30
number_of_excavation_steps = 26
initial_grouting_surface_index = 2
round_length = 3.5
TBM_offset = 4
lining_offset = 3
grouting_offset = 2
move_steps_per_round_length = 1
steps_per_down_time = 1
segment_number = 7
write_to_database = True


##### COORDINATES OF TUNNEL ALIGMNET	#####
alignment=[[133.360790896, 3091.26210065, 14000.0], [483.36093891, 3100.01165715, 14000.0], [833.360790784, 3091.25026246, 14000.0], [1183.3609388, 3099.99981897, 14000.0], [1533.36079067, 3091.23842428, 14000.0], [1883.36093869, 3099.98798078, 14000.0], [2233.36079056, 3091.22658609, 14000.0], [2583.36093858, 3099.9761426, 14000.0], [2933.36079045, 3091.21474791, 14000.0], [3283.36093846, 3099.96430441, 14000.0], [3632.92286867, 3082.45839273, 14000.0], [3980.29767768, 3038.78459719, 14000.0], [4329.85960789, 3021.2786855, 14000.0], [4679.8597559, 3030.028242, 14000.0], [5029.42168611, 3012.52233032, 14000.0], [5376.79649512, 2968.84853477, 14000.0], [5725.92050367, 2942.59810609, 14000.0], [6071.98622266, 2890.26725353, 14000.0], [6411.09507326, 2803.63476861, 14000.0], [6739.85596695, 2683.56697619, 14000.0], [7058.79123805, 2539.14761739, 14000.0], [7384.54855852, 2410.85565931, 14000.0], [7699.67388637, 2258.55323731, 14000.0], [7998.01239509, 2075.53920996, 14000.0], [8276.58069961, 1863.64371752, 14000.0], [8532.59311686, 1624.98571492, 14000.0], [8763.4895227, 1361.95178218, 14000.0], [8966.96095304, 1077.17225864, 14000.0], [9148.56937747, 777.847955375, 14000.0], [9352.04080782, 493.068431832, 14000.0], [9582.93721365, 230.034499096, 14000.0]]
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
x0_min=float(alignment[4][0])
x0_max=float(alignment[4][0])
y0_min=float(alignment[4][1])
y0_max=float(alignment[4][1])
z0=float(alignment[4][2])

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
initial_reactivation_index = 0 
reactivation_index =0
reactivation_index_stressfree= 0
initial_face_index = 1
##### VOLUME LOSS #####
volume_loss =2.0

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
for element in model1.layer_sets['building']:
	if element in model1.model_part.Elements:
		element_list.append( element )
for element in model1.layer_sets['foundation']:
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
delta_r=excavation_radius-excavation_radius*math.sqrt(1-volume_loss/100.0)
excavation_nodes=[]
for i in range (1, number_of_slices+1):
	for node in model1.layer_nodes_sets['excavation_surface_'+str(i)]:
		if node in model1.model_part.Nodes:
			excavation_nodes.append(node)
for node_id in excavation_nodes:
	node = model1.model_part.Nodes[node_id]
	node.Fix(DISPLACEMENT_Z)
	node.SetSolutionStepValue(DISPLACEMENT_Z, 0.0)
	node.SetSolutionStepValue(DISPLACEMENT_EINS_Z, 0.0)
	node.SetSolutionStepValue(DISPLACEMENT_NULL_Z, 0.0)
	node.Fix(DISPLACEMENT_X)
	node.SetSolutionStepValue(DISPLACEMENT_X, 0.0)
	node.SetSolutionStepValue(DISPLACEMENT_EINS_X, 0.0)
	node.SetSolutionStepValue(DISPLACEMENT_NULL_X, 0.0)
	node.Fix(DISPLACEMENT_Y)
	node.SetSolutionStepValue(DISPLACEMENT_Y, 0.0)
	node.SetSolutionStepValue(DISPLACEMENT_EINS_Y, 0.0)
	node.SetSolutionStepValue(DISPLACEMENT_NULL_Y, 0.0)
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

for node_id in excavation_nodes:
	node = model1.model_part.Nodes[node_id]
	node.Free(DISPLACEMENT_Z)
	node.Free(DISPLACEMENT_X)
	node.Free(DISPLACEMENT_Y)
advance = 0.0
tbm_lenght=7.5
tbm_conicity= 0.5
tbm_r= 4.94
tbm_rings=int(tbm_lenght/round_length)
radius=[0.0,0.0,0.0] 
for step in range (1, number_of_slices+1):
	time=time+move_delta_time
	disp_x=(float(alignment[step][0]))
	disp_y=(float(alignment[step][1]))	
	delta_x=(disp_x-float(alignment[step-1][0]))
	delta_y=(disp_y-float(alignment[step-1][1]))
	alpha=math.atan(delta_y/delta_x)
	for node_id in model1.layer_nodes_sets['excavation_surface_'+str(step)]:
		node = model1.model_part.Nodes[node_id]
		x=node.X0
		y=node.Y0
		z=node.Z0
		point=[x,y,z]
		for i in range (0,3):
			radius[i]=float(alignment[step][i])-point[i]
		theta=math.atan2( radius[1], radius[2] )
		delta_rz=delta_r*math.cos(theta)
		delta_ry_1=delta_r*math.sin(theta)
		delta_rx=delta_ry_1*math.sin(alpha)
		delta_ry=delta_ry_1*math.cos(alpha)

		node.Fix(DISPLACEMENT_X)
		node.Fix(DISPLACEMENT_Y)
		node.Fix(DISPLACEMENT_Z)
		node.SetSolutionStepValue(DISPLACEMENT_X, delta_rx)
		node.SetSolutionStepValue(DISPLACEMENT_EINS_X, delta_rx)
		node.SetSolutionStepValue(DISPLACEMENT_NULL_X, delta_rx)
		node.SetSolutionStepValue(DISPLACEMENT_Y, delta_ry)
		node.SetSolutionStepValue(DISPLACEMENT_EINS_Y, delta_ry)
		node.SetSolutionStepValue(DISPLACEMENT_NULL_Y, delta_ry)
		node.SetSolutionStepValue(DISPLACEMENT_Z, delta_rz)
		node.SetSolutionStepValue(DISPLACEMENT_EINS_Z, delta_rz)
		node.SetSolutionStepValue(DISPLACEMENT_NULL_Z, delta_rz)


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

	face_index = face_index+1
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
	model1.model_part.CloneTimeStep( time )
	model1.deac.Deactivate( model1.model_part, 0, deactivation_index )    
	print('solving...')
	model1.solver.Solve()
	model1.WriteOutput( time )
	print('#############')
print('ALL DONE.')

