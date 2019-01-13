import sys
import os
import math
from ModelComponent import *
from HelperMethods import *

class ExcavationComponent(ModelComponent):

	# Constructor
	def __init__(self, global_params, working_dir):
		ModelComponent.__init__(self, global_params, working_dir)
		
		# Setup LOD handlers
		self.lod_prepare_handlers = [self.PrepareModel_Lod1 ]
		self.lod_script_handlers = [self.AddToSimScript_Lod1]
		
		# Define name
		self.component_name = "excavation"
		# Dependencies
		self.lining = None
		self.building = None
		self.tbm = None
		self.soil = None		

		
	def PrepareModel_Lod1(self, ostream):
		# Write model to .bch output file
		print 'Excavation LOD = 1'
		if self.soil.lod==1:
			return
		ostream.write("mescape\n")
		ostream.write("Files SaveAs "+self.working_dir+self.global_params['model_name']+"_excavation_model.gid\n")
		ostream.write("mescape\n")
		for step in range(1,self.global_params['number_of_slices']+1):
			ostream.write("view layers new\n")
			ostream.write("excavation_"+str(step)+"\n escape escape\n")
			ostream.write("view layers ToUse\n")
			ostream.write("excavation_"+str(step)+"\n escape escape\n")

			ostream.write("Files AcisRead " +str(self.global_params['model_path'])+ "sat_files\excavation\excavation_volume_" +str(step)+".sat"+"\n ")
			ostream.write("mescape\n")
	
	
		
		
		#convert all lines to NURBS
		ostream.write("Geometry Edit ConvToNurbsL\n")
		ostream.write("InvertSelection\n escape\n Yes\n")
		ostream.write("mescape\n")
		list_hf=[2, 1]
		k=2
		for i in range(0, self.global_params['number_of_slices']-1):
			k=k+2
			list_hf.append(k)
		
		for step in range(0,len(list_hf)):
			ostream.write("view layers new\n")
			ostream.write("heading_face_" + str(step) + "\n escape escape\n")
			ostream.write("view layers entities\n")
			ostream.write("heading_face_" + str(step) + "\n")
			ostream.write("surfaces\n"+str(list_hf[step])+"\n")
			ostream.write("mescape\n")

		# set meshing information
		# ostream.write("Meshing Structured Volumes\n")
		# ostream.write("InvertSelection\n escape\n 1\n")
		# ostream.write("InvertSelection\n escape\n escape\n")
		# ostream.write("mescape\n")
		ostream.write("mescape\n")
		ostream.write("Meshing\n Generate\n"+str(self.global_params['excavation_radius'])+" escape\n escape\n")

		ostream.write("Files Save\n")
		ostream.write("Quit\n")
		ostream.close()
		
		
		####CREATE BACH FILE FOR ACTIVATION LEVELS####
		ifile = open(self.working_dir+'set_activation_excavation.bch','w')
		deactivation_index = 1
		if (self.lining.lod)>1:
			for step in range(1, self.global_params['number_of_slices']+1):
				#if( step < self.global_params['TBM_offset']+1 ):
				#####THIS IS CHANGED!!!!!!! CHECK THE EFFECT
				if( step < self.global_params['TBM_offset']+1):
					ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
					ifile.write("Change -1\n")
					ifile.write("layer:excavation_"+str(step)+"\n")
					ifile.write("mescape\n")
				else:
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
					ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
					ifile.write("Change "+str(deactivation_index)+"\n")
					ifile.write("layer:excavation_"+str(step)+"\n")
					ifile.write("mescape\n")
					deactivation_index = deactivation_index + 1
		else:
			for step in range(1, self.global_params['number_of_slices']+1):

				ifile.write("Data Conditions AssignCond Volume_Activation_Level\n")
				ifile.write("Change "+str(deactivation_index)+"\n")
				ifile.write("layer:excavation_"+str(step)+"\n")
				ifile.write("mescape\n")
				deactivation_index = deactivation_index + 1
		
		ifile.close()			
	#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-	
		#########CREATE BACH FILE FOR MATERIAL PARAMETERS####		
		ifile = open(self.working_dir+'material_condition_excavation.bch','w')
		ifile.write("mescape\n")  
		ifile.write("Data Materials NewMaterial UserDefined Excavation UserDefined UserDefined\n")
		ifile.write("mescape\n")
		ifile.write("mescape\n")   

		for step in range(1, self.global_params['number_of_slices']+1):	

			ifile.write("Data Materials AssignMaterial Excavation Volumes\n")
			ifile.write("layer:excavation_"+str(step)+"\n")
			ifile.write("mescape\n")
		ifile.write("mescape\n")
			
		#assign element type excavation
		for step in range(1, (self.global_params['number_of_slices'])+1):
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
			ifile.write("layer:excavation_"+str(step)+"\n")
			ifile.write("mescape\n")
			
		############ ASSIGNING SURFACE GROUP MEMBERSHIP######			
		for step in range(1, self.global_params['number_of_slices']):
		############ ASSIGNING SURFACE GROUP MEMBERSHIP#######
			ifile.write("Data Conditions AssignCond Surface_Group_Membership\n")
			ifile.write("Change heading_face_"+str(step)+"\n")
			ifile.write("layer:heading_face_"+str(step)+"\n")
			ifile.write("mescape\n")
			ifile.write("Data Conditions AssignCond Distributed_Surface_Load\n")
			ifile.write("layer:heading_face_"+str(step)+"\n")
			ifile.write("mescape\n")

				
		ifile.close()				
		return
		
	def AddToSimScript_Lod1(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Excavation SimScript LOD = 1'
		
		if self.soil.lod==1:
			ostream.write("time=1.0\n")
			ostream.write("model1.Solve( time, 0, 0, 0, 0 )\n")
			ostream.write("model1.WriteOutput( time )\n")
			return

		if self.lining.lod==1:					
			ostream.write("radius=[0.0,0.0,0.0] \n")
			ostream.write("for step in range (1, number_of_slices+1):\n")
			ostream.write("	time=time+move_delta_time\n")
			ostream.write("	disp_x=(float(alignment[step][0]))\n")
			ostream.write("	disp_y=(float(alignment[step][1]))	\n")
			ostream.write("	delta_x=(disp_x-float(alignment[step-1][0]))\n")
			ostream.write("	delta_y=(disp_y-float(alignment[step-1][1]))\n")
			ostream.write("	alpha=math.atan(delta_y/delta_x)\n")
			ostream.write("	for node_id in model1.layer_nodes_sets['excavation_surface_'+str(step)]:\n")
			ostream.write("		node = model1.model_part.Nodes[node_id]\n")
			ostream.write("		x=node.X0\n")
			ostream.write("		y=node.Y0\n")
			ostream.write("		z=node.Z0\n")
			ostream.write("		point=[x,y,z]\n")
			ostream.write("		for i in range (0,3):\n")
			ostream.write("			radius[i]=float(alignment[step][i])-point[i]\n")
			ostream.write("		theta=math.atan2( radius[1], radius[2] )\n")
			ostream.write("		delta_rz=delta_r*math.cos(theta)\n")
			#ostream.write("		delta_ry_1=-delta_r*math.sin(theta)\n")
			ostream.write("		delta_ry_1=delta_r*math.sin(theta)\n")
			ostream.write("		delta_rx=delta_ry_1*math.sin(alpha)\n")
			ostream.write("		delta_ry=delta_ry_1*math.cos(alpha)\n")
			ostream.write("\n")
			ostream.write("		node.Fix(DISPLACEMENT_X)\n")
			ostream.write("		node.Fix(DISPLACEMENT_Y)\n")
			ostream.write("		node.Fix(DISPLACEMENT_Z)\n")
			ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_X, delta_rx)\n")
			ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_EINS_X, delta_rx)\n")
			ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_NULL_X, delta_rx)\n")
			ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_Y, delta_ry)\n")
			ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_EINS_Y, delta_ry)\n")
			ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_NULL_Y, delta_ry)\n")
			ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_Z, delta_rz)\n")
			ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_EINS_Z, delta_rz)\n")
			ostream.write("		node.SetSolutionStepValue(DISPLACEMENT_NULL_Z, delta_rz)\n")

				#model.Solve(time, 0, 0, 0, 0)
				#model.WriteOutput(time)
		elif self.lining.lod>1:	
			ostream.write("init=TBM_offset \n")	
			ostream.write("disp_vector=[]\n")
			if self.tbm.lod==1:
				ostream.write("radius=[0.0,0.0,0.0]	\n")
				ostream.write("delta_r_tbm=[0]*tbm_rings\n")
				#for midpoint deformation of TBM
				ostream.write("for i in range (0,tbm_rings):\n")
				ostream.write("	delta_r_tbm[i]=excavation_radius-(tbm_r-round_length*(tbm_rings-i-0.5)*tbm_conicity/100.0)\n")
				ostream.write("print(delta_r_tbm)				\n")		
				ostream.write("for i in range (TBM_offset-tbm_rings, len(alignment)):\n")
				ostream.write("	disp_vector.append(alignment[i])				\n")	


			elif self.tbm.lod==2:
				ostream.write("insert_tbm=[]\n")
				ostream.write("for j in range (0,3):\n")
				ostream.write("	insert_tbm.append(alignment[TBM_offset-1][j])\n")
				ostream.write("for i in range (TBM_offset-2, len(alignment)):\n")
				ostream.write("	disp_vector.append(alignment[i])\n")
				ostream.write("for i in range (1, len(disp_vector)):\n")
				ostream.write("	for j in range (0,3):\n")
				ostream.write("		disp_vector[i][j]= (float(disp_vector[i][j])-float(disp_vector[0][j]))\n")
				ostream.write("for j in range (0,3):\n")
				ostream.write("	disp_vector[0][j]= 0.0\n")
			
			ostream.write("disp_x=0.0\n")			
			ostream.write("disp_y=0.0\n")		
			ostream.write("\n")
			if self.tbm.lod==2:
				ostream.write("delta_x=(float(disp_vector[1][0])-float(disp_vector[0][0]))\n")
				ostream.write("delta_y=(float(disp_vector[1][1])-float(disp_vector[0][1]))\n")
				ostream.write("alpha_last=math.atan(delta_y/delta_x)		\n")
				ostream.write("beta=0\n")
			ostream.write("for step in range(1,number_of_excavation_steps+1):\n")
			ostream.write("	#move\n")
			ostream.write("	print('ready for next step')\n")
			ostream.write("	print '#########################################'\n")
			ostream.write("	print '############# MOVE MACHINE  #############'\n")
			ostream.write("	print '#########################################'\n")
			if self.tbm.lod==1:
				ostream.write("	delta_x=(float(disp_vector[step+tbm_rings][0])-float(disp_vector[step+tbm_rings-1][0]))\n")		
				ostream.write("	delta_y=(float(disp_vector[step+tbm_rings][1])-float(disp_vector[step+tbm_rings-1][1]))\n")
				ostream.write("	alpha=math.atan(delta_y/delta_x)\n")
							
			elif self.tbm.lod==2:
				ostream.write("	delta_x=(float(disp_vector[step+1][0])-float(disp_vector[step][0]))\n")		
				ostream.write("	delta_y=(float(disp_vector[step+1][1])-float(disp_vector[step][1]))\n")
				ostream.write("	alpha=math.atan(delta_y/delta_x)\n")
				ostream.write("	delta_alpha=alpha-alpha_last\n")
				ostream.write("	alpha_last=alpha\n")
				ostream.write("	beta=beta+delta_alpha\n")
		
			ostream.write("\n")
			ostream.write("\n")
		if self.lining.lod==3:
		#CHANGE FOR ACTIVE BOLT NODES!!!
			ostream.write("	for nodes in beams_node_list:\n")
			#ostream.write("	for nodes in bolt_nodes:\n")
			ostream.write("		model1.model_part.Nodes[nodes].Fix(ROTATION_X)\n")
			ostream.write("		model1.model_part.Nodes[nodes].Fix(ROTATION_Y)\n")
			ostream.write("		model1.model_part.Nodes[nodes].Fix(ROTATION_Z)\n")
			ostream.write("		model1.model_part.Nodes[nodes].SetSolutionStepValue(ROTATION_X, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[nodes].SetSolutionStepValue(ROTATION_Y, 0.0)\n")
			ostream.write("		model1.model_part.Nodes[nodes].SetSolutionStepValue(ROTATION_Z, 0.0)\n")
			ostream.write("\n")
			
		if self.tbm.lod==1 and self.lining.lod>1:			
			ostream.write("	for moving_step in range (0,move_steps):\n")
			ostream.write("		time = time + move_delta_time\n")
			ostream.write("		tbm_index=step+TBM_offset-tbm_rings\n")
			ostream.write("		for ring in range(0, tbm_rings):\n")
			ostream.write("			for node_id in model1.layer_nodes_sets['excavation_surface_'+str(tbm_index+ring)]:\n")
			ostream.write("				node = model1.model_part.Nodes[node_id]\n")
			ostream.write("				x=node.X0\n")
			ostream.write("				y=node.Y0\n")
			ostream.write("				z=node.Z0\n")
			ostream.write("				point=[x,y,z]\n")
			ostream.write("				for i in range (0,3):\n")
			ostream.write("					radius[i]=float(disp_vector[step+ring][i])-point[i]\n")

			ostream.write("				theta=math.atan2( radius[1], radius[2] )\n")
			ostream.write("				delta_rz=delta_r_tbm[ring]*math.cos(theta)\n")
			ostream.write("				delta_ry_1=delta_r_tbm[ring]*math.sin(theta)\n")
			ostream.write("				delta_rx=delta_ry_1*math.sin(alpha)\n")
			ostream.write("				delta_ry=delta_ry_1*math.cos(alpha)\n")
			ostream.write("				node.Fix(DISPLACEMENT_X)\n")
			ostream.write("				node.Fix(DISPLACEMENT_Y)\n")
			ostream.write("				node.Fix(DISPLACEMENT_Z)\n")
			ostream.write("				node.SetSolutionStepValue(DISPLACEMENT_X, delta_rx)\n")
			ostream.write("				node.SetSolutionStepValue(DISPLACEMENT_EINS_X, delta_rx)\n")
			ostream.write("				node.SetSolutionStepValue(DISPLACEMENT_NULL_X, delta_rx)\n")
			ostream.write("				node.SetSolutionStepValue(DISPLACEMENT_Y, delta_ry)\n")
			ostream.write("				node.SetSolutionStepValue(DISPLACEMENT_EINS_Y, delta_ry)\n")
			ostream.write("				node.SetSolutionStepValue(DISPLACEMENT_NULL_Y, delta_ry)\n")
			ostream.write("				node.SetSolutionStepValue(DISPLACEMENT_Z, delta_rz)\n")
			ostream.write("				node.SetSolutionStepValue(DISPLACEMENT_EINS_Z, delta_rz)\n")
			ostream.write("				node.SetSolutionStepValue(DISPLACEMENT_NULL_Z, delta_rz)\n")
							
			ostream.write("		for node_id in model1.layer_nodes_sets['excavation_surface_'+str(tbm_index-1)]:\n")
			ostream.write("			node = model1.model_part.Nodes[node_id]\n")
			ostream.write("			node.Free(DISPLACEMENT_X)\n")
			#ostream.write("			node.Free(DISPLACEMENT_EINS_X)\n")
			#ostream.write("			node.Free(DISPLACEMENT_NULL_X)\n")
			ostream.write("			node.Free(DISPLACEMENT_Y)\n")
			#ostream.write("			node.Free(DISPLACEMENT_EINS_Y)\n")
			#ostream.write("			node.Free(DISPLACEMENT_NULL_Y)\n")
			ostream.write("			node.Free(DISPLACEMENT_Z)\n")
			#ostream.write("			node.Free(DISPLACEMENT_EINS_Z)\n")
			#ostream.write("			node.Free(DISPLACEMENT_NULL_Z)\n")
			
		elif (self.tbm.lod==2 and self.lining.lod>1):			
			ostream.write("	for moving_step in range (0,move_steps):\n")
			ostream.write("		time = time + move_delta_time\n")
			ostream.write("		advance = advance +  one_ring/float(move_steps)\n")
			ostream.write("		disp_x = disp_x +  delta_x/float(move_steps)\n")
			ostream.write("		disp_y = disp_y +  delta_y/float(move_steps)\n")

			ostream.write("		print('--- moving to ' +str(disp_x)+' ---') \n")
			ostream.write("\n")
			ostream.write("\n")
			ostream.write("		##for node in model1.node_groups['shield_advance']:\n")
			ostream.write("		for node_id in shield_nodes:\n")
			ostream.write("			node = model1.model_part.Nodes[node_id]\n")
			ostream.write("			x=node.X0-float(insert_tbm[0])\n")
			ostream.write("			y=node.Y0-float(insert_tbm[1])\n")
			ostream.write("			x1=x*math.cos(beta)-y*math.sin(beta)+float(insert_tbm[0])-node.X0\n")
			ostream.write("			y1=x*math.sin(beta)+y*math.cos(beta)+float(insert_tbm[1])-node.Y0\n")
			ostream.write("			dx=disp_x+x1\n")
			ostream.write("			dy=disp_y+y1\n")					
			ostream.write("			node.SetSolutionStepValue(DISPLACEMENT_Y, dy)\n")
			ostream.write("			node.SetSolutionStepValue(DISPLACEMENT_EINS_Y, dy)\n")
			ostream.write("			node.SetSolutionStepValue(DISPLACEMENT_NULL_Y, dy)\n")
			ostream.write("			node.SetSolutionStepValue(DISPLACEMENT_X, dx)\n")
			ostream.write("			node.SetSolutionStepValue(DISPLACEMENT_EINS_X, dx)\n")
			ostream.write("			node.SetSolutionStepValue(DISPLACEMENT_NULL_X, dx)\n")
			ostream.write("\n")
			
		elif self.tbm.lod==3:	
			#ADD STEERING HERE!!!!!!!!!!!!! NOT DOEN JET
			ostream.write("		steering_utility.Move( advance, model1.model_part,with_diagonals)\n")
			
		#correct this part here!!!!
		if self.lining.lod>1:
			ostream.write("\n")
			ostream.write("\n")
			#if self.tbm.lod==2:				
			ostream.write("		model1.model_part.CloneTimeStep( time )\n")
			ostream.write("		model1.solver.Solve()\n")
			ostream.write("		model1.WriteOutput( time )\n")
		
		if self.lining.lod==3:		
			ostream.write("\n")
			ostream.write("	active_bolt_index= active_bolt_index+1\n")
		ostream.write("\n")
		ostream.write("\n")
		ostream.write("	print('--- moving step done ['+str(time)+'] ---') \n") 
		ostream.write("	print '#########################################'\n")
		ostream.write("	print '############# MACHINE MOVED  ############'\n")
		ostream.write("	print '#########################################'\n")        
		ostream.write("\n")
		ostream.write("	print('#############')\n")
		ostream.write("	print(' excavating...')\n")
		ostream.write("	print('#############')\n")
		ostream.write("	#excavate\n")
		ostream.write("	print('deactivating and reactivating ...')\n")

		ostream.write("	deactivation_index = deactivation_index + 1\n")
		ostream.write("\n")
		if self.lining.lod>1:			
		
			ostream.write("	if(grouting_surface_index>=3):\n")
			ostream.write("			for node in model1.layer_nodes_sets[grouting_face_layer]:\n")
			ostream.write("				if( account_for_water == True ):\n")
			ostream.write("					model1.model_part.Nodes[node].Free(WATER_PRESSURE)\n")
			ostream.write("				model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,0.0)\n")
			ostream.write("	if(lining_face_index>=3):\n")
			ostream.write("			for node in model1.layer_nodes_sets['lining_surface_'+str(lining_face_index)]:\n")
			ostream.write("				model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,0.0)\n")
			ostream.write("\n")
			ostream.write("	lining_face_index= lining_face_index+1    \n")
			ostream.write("	grouting_surface_index= grouting_surface_index+1\n")
			ostream.write("	face_index = face_index+1\n")
			ostream.write("\n")
			ostream.write("	grouting_face_layer = 'grouting_surface_'+str(grouting_surface_index)\n")
			ostream.write("	for node in model1.layer_nodes_sets[grouting_face_layer]:\n")
			ostream.write("			pressure = grouting_pressure-(model1.model_part.Nodes[node].Z)*grouting_gradient\n")
			ostream.write("			if( account_for_water == True ):\n")
			ostream.write("				model1.model_part.Nodes[node].Fix(WATER_PRESSURE)\n")
			ostream.write("				model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE,pressure)\n")
			ostream.write("				model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_EINS,pressure)\n")
			ostream.write("				model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_NULL,pressure)\n")
			ostream.write("			model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,-pressure)\n")
			ostream.write("			\n")
			ostream.write("	for node in model1.layer_nodes_sets['lining_surface_'+str(lining_face_index)]:\n")
			ostream.write("		initial_pressure = heading_face_pressure\n")
			ostream.write("		depth = model1.model_part.Nodes[node].Z\n")			
			#ostream.write("		depth = model1.model_part.Nodes[node].Z\n")
			ostream.write("		pressure = initial_pressure-depth*heading_face_gradient\n")
			ostream.write("		model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,-pressure)    \n")                
			ostream.write("\n")
		if self.lining.lod==1:	
			ostream.write("	face_index = face_index+1\n")
		ostream.write("	if face_index>1:\n")
		ostream.write("		old_face_layer = 'heading_face_'+str(face_index-1)\n")
		ostream.write("		for node in model1.node_groups[old_face_layer]:\n")
		ostream.write("				model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,0.0)\n")
		ostream.write("				if( account_for_water == True ):\n")
		ostream.write("					model1.model_part.Nodes[node].Free( WATER_PRESSURE )\n")
		ostream.write("	current_face_layer = 'heading_face_'+str(face_index)\n")
		ostream.write("	for node in model1.node_groups[current_face_layer]:\n")
		ostream.write("			pressure = heading_face_pressure-(model1.model_part.Nodes[node].Z)*heading_face_gradient\n")
		ostream.write("			model1.model_part.Nodes[node].SetSolutionStepValue(FACE_LOAD_X,pressure)\n")
		ostream.write("			if( account_for_water == True ):\n")
		ostream.write("				model1.model_part.Nodes[node].Fix( WATER_PRESSURE )\n")
		ostream.write("				model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE,pressure)\n")
		ostream.write("				model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_NULL,pressure)\n")
		ostream.write("				model1.model_part.Nodes[node].SetSolutionStepValue(WATER_PRESSURE_EINS,pressure)\n")
		
		if self.lining.lod==1:	
			ostream.write("	#cloning time step\n")
			ostream.write("	time = time + exc_delta_time\n")
			ostream.write("	model1.model_part.CloneTimeStep( time )\n")	
			#ostream.write("	model1.deac.ReactivateStressFree( model1.model_part, initial_reactivation_index, reactivation_index )\n")
			ostream.write("	model1.deac.Deactivate( model1.model_part, 0, deactivation_index )    \n")	
			#ostream.write("	model1.model_part.CloneTimeStep( time )\n")
			ostream.write("	print('solving...')\n")
			ostream.write("	model1.solver.Solve()\n")
			ostream.write("	model1.WriteOutput( time )\n")
			ostream.write("	print('#############')\n")
			if self.global_params["write_to_databese"]==True:
				ostream.write("	if step!=(number_of_slices-1):\n")
				ostream.write("		ifile = open('settlments.dat', 'a' )\n")
				ostream.write("		for node_id in top_nodes_print:\n")
				ostream.write("			if node_id!=0:\n")
				ostream.write("				node=model1.model_part.Nodes[node_id]\n")
				ostream.write("				x = node.GetSolutionStepValue(DISPLACEMENT_X)\n")
				ostream.write("				y = node.GetSolutionStepValue(DISPLACEMENT_Y)\n")
				ostream.write("				z = node.GetSolutionStepValue(DISPLACEMENT_Z)\n")
				ostream.write("				ifile.write(str(time)+' '+str(node_id)+' '+str(node.X)+' '+str(node.Y)+' '+str(node.Z)+' '+str(x)+' '+str(y)+' '+str(z)+'\\n')\n")
				ostream.write("		ifile.close()\n")
	#			if self.building.lod>1:	
				ostream.write("		ifile = open('building.dat', 'a' )\n")
				ostream.write("		i=0\n")
				ostream.write("		for node_id in building_print:\n")
				ostream.write("			if node_id!=0:\n")
				ostream.write("				node=model1.model_part.Nodes[node_id]\n")
				ostream.write("				x = -builidng_init[i][0]+node.GetSolutionStepValue(DISPLACEMENT_X)\n")
				ostream.write("				y = -builidng_init[i][1]+node.GetSolutionStepValue(DISPLACEMENT_Y)\n")
				ostream.write("				z = -builidng_init[i][2]+node.GetSolutionStepValue(DISPLACEMENT_Z)\n")
				ostream.write("				ifile.write(str(time)+' '+str(node_id)+' '+str(node.X)+' '+str(node.Y)+' '+str(node.Z)+' '+str(x)+' '+str(y)+' '+str(z)+'\\n')\n")
				ostream.write("			i=i+1\n")	
				ostream.write("		ifile.close()\n")	

			
			ostream.write("print('ALL DONE.')\n")			
		
		if self.lining.lod==2:	


			ostream.write("	#cloning time step\n")
			ostream.write("	time = time + exc_delta_time\n")
			#ostream.write("	model1.model_part.CloneTimeStep( time )\n")
			#change!!!!!

			ostream.write("	reactivation_index_stressfree = reactivation_index_stressfree + 2*segment_number \n")
			ostream.write("	reactivation_index = reactivation_index + 2*7\n")
			ostream.write("	#model1.deac.ReactivateStressFree( model1.model_part,initial_reactivation_index , reactivation_index_stressfree )\n") 
			ostream.write("	model1.deac.ReactivateStressFree( model1.model_part, initial_reactivation_index, reactivation_index )\n")
			ostream.write("	model1.deac.Deactivate( model1.model_part, 0, deactivation_index )    \n")
			ostream.write("	print('done...')\n")
			ostream.write("	print '##### APPLYING FACE PRESSURE #####'\n")
			ostream.write("	print '##### FREE OLD PRESSURE FACES #####'\n")
			ostream.write("\n")
			ostream.write("	print '##### APPLY BOUNDARY CONDITIONS AT HEADING FACE #####'\n")
			ostream.write("\n")
			ostream.write("	#solve and consolidate results\n")
			ostream.write("	for moving_step in range (0,exc_steps):\n")
			ostream.write("		time = time + exc_delta_time\n")
			ostream.write("		model1.model_part.CloneTimeStep( time )\n")
			ostream.write("		print('solving...')\n")
			ostream.write("		model1.solver.Solve()\n")
			ostream.write("		model1.WriteOutput( time )\n")
			ostream.write("		print('#############')\n")
			ostream.write("	print('step '+str(step)+' done.')\n")
			ostream.write("\n")
			if self.global_params["write_to_databese"]==True:
				ostream.write("	print('#############')\n")
				ostream.write("	if step==(number_of_excavation_steps-2):\n")
				ostream.write("		ifile = open('settlments.dat', 'a' )\n")
				ostream.write("		for node_id in top_nodes_print:\n")
				ostream.write("			if node_id!=0:\n")
				ostream.write("				node=model1.model_part.Nodes[node_id]\n")
				ostream.write("				x = node.GetSolutionStepValue(DISPLACEMENT_X)\n")
				ostream.write("				y = node.GetSolutionStepValue(DISPLACEMENT_Y)\n")
				ostream.write("				z = node.GetSolutionStepValue(DISPLACEMENT_Z)\n")
				ostream.write("				ifile.write(str(node_id)+' '+str(node.X)+' '+str(node.Y)+' '+str(node.Z)+' '+str(x)+' '+str(y)+' '+str(z)+'\\n')\n")
				ostream.write("		ifile.close()\n")
				if self.building.lod>1:	
					ostream.write("		ifile = open('building.dat', 'a' )\n")
					ostream.write("		i=0\n")
					ostream.write("		for node_id in building_print:\n")
					ostream.write("			if node_id!=0:\n")
					ostream.write("				node=model1.model_part.Nodes[node_id]\n")
					ostream.write("				x = -builidng_init[i][0]+node.GetSolutionStepValue(DISPLACEMENT_X)\n")
					ostream.write("				y = -builidng_init[i][1]+node.GetSolutionStepValue(DISPLACEMENT_Y)\n")
					ostream.write("				z = -builidng_init[i][2]+node.GetSolutionStepValue(DISPLACEMENT_Z)\n")
					ostream.write("				ifile.write(str(node_id)+' '+str(node.X)+' '+str(node.Y)+' '+str(node.Z)+' '+str(x)+' '+str(y)+' '+str(z)+'\\n')\n")
					ostream.write("			i=i+1\n")
					ostream.write("		ifile.close()\n")
			ostream.write("print('ALL DONE.')\n")
		
		
		elif self.lining.lod==3:			
			ostream.write("	for i in range (1,segment_number+1):\n")
			ostream.write("		#cloning time step\n")
			ostream.write("		time = time + exc_delta_time/segment_number\n")
			#ostream.write("		model1.model_part.CloneTimeStep( time )\n")
			ostream.write("		#set bolt index\n")
			ostream.write("		for node in model1.layer_nodes_sets['bolts_'+str(active_bolt_index)+'_'+str(i)]:\n")
			ostream.write("			beams_node_list.append(node)\n")
			ostream.write("		Epltu = EmbeddedNodePenaltyTyingUtility()\n")
			ostream.write("		links1 = Epltu.SetUpTyingLinks( model1.model_part, beams_node_list, segment_elements )\n")
			ostream.write("		for cond in links1:\n")
			ostream.write("			cond.SetValue(INITIAL_PENALTY, 1.0e12)\n")
			ostream.write("		######################################################\n")
			ostream.write("		#reactivate grouting\n")
			ostream.write("\n")
			ostream.write("		reactivation_index_stressfree = reactivation_index_stressfree + 2\n")
			ostream.write("		reactivation_index = reactivation_index + 2\n")
			ostream.write("		#model1.deac.ReactivateStressFree( model1.model_part,initial_reactivation_index , reactivation_index_stressfree )\n") 
			ostream.write("		model1.deac.ReactivateStressFree( model1.model_part, initial_reactivation_index, reactivation_index )\n")
			ostream.write("		model1.deac.Deactivate( model1.model_part, 0, deactivation_index )    \n")
			ostream.write("		print('done...')\n")
			ostream.write("		print '##### APPLYING FACE PRESSURE #####'\n")
			ostream.write("		print '##### FREE OLD PRESSURE FACES #####'\n")
			ostream.write("\n")
			ostream.write("		print '##### APPLY BOUNDARY CONDITIONS AT HEADING FACE #####'\n")
			ostream.write("\n")
			ostream.write("	#solve and consolidate results\n")
			ostream.write("		time = time + exc_delta_time\n")
			ostream.write("		model1.model_part.CloneTimeStep( time )\n")
			ostream.write("		print('solving...')\n")
			ostream.write("		model1.solver.Solve()\n")
			ostream.write("		model1.WriteOutput( time )\n")
			ostream.write("		print('#############')\n")
			ostream.write("		print('step '+str(step)+' done.')\n")
			ostream.write("\n")
			ostream.write("	print('#############')\n")
			if self.global_params["write_to_databese"]==True:
				ostream.write("	print('######ONLY OF OUTPUT IS REQUIRED FOR VISUALISATION #######')\n")			
				ostream.write("	if step==(number_of_excavation_steps-2):\n")
				ostream.write("		ifile = open('settlments.dat', 'a' )\n")
				ostream.write("		for node_id in top_nodes_print:\n")
				ostream.write("			if node_id!=0:\n")
				ostream.write("				node=model1.model_part.Nodes[node_id]\n")
				ostream.write("				x = node.GetSolutionStepValue(DISPLACEMENT_X)\n")
				ostream.write("				y = node.GetSolutionStepValue(DISPLACEMENT_Y)\n")
				ostream.write("				z = node.GetSolutionStepValue(DISPLACEMENT_Z)\n")
				ostream.write("				ifile.write(str(node_id)+' '+str(node.X)+' '+str(node.Y)+' '+str(node.Z)+' '+str(x)+' '+str(y)+' '+str(z)+'\\n')\n")
				#ostream.write("				ifile.write(str(node_id)+' '+str(node.X)+' '+str(node.Y)+' '+str(node.Z)+' '+str(node.X0-node.X)+' '+str(node.Y0-node.Y)+' '+str(node.Z0-node.Z)+'\n')\n")
				ostream.write("		ifile.close()\n")
			#change if write to file yes
			if self.global_params["write_to_databese"]==True:
				if self.building.lod>1:	
					ostream.write("		ifile = open('building.dat', 'a' )\n")
					ostream.write("		i=0\n")
					ostream.write("		for node_id in building_print:\n")
					ostream.write("			if node_id!=0:\n")
					ostream.write("				node=model1.model_part.Nodes[node_id]\n")
					ostream.write("				x = -builidng_init[i][0]+node.GetSolutionStepValue(DISPLACEMENT_X)\n")
					ostream.write("				y = -builidng_init[i][1]+node.GetSolutionStepValue(DISPLACEMENT_Y)\n")
					ostream.write("				z = -builidng_init[i][2]+node.GetSolutionStepValue(DISPLACEMENT_Z)\n")
					ostream.write("				ifile.write(str(node_id)+' '+str(node.X)+' '+str(node.Y)+' '+str(node.Z)+' '+str(x)+' '+str(y)+' '+str(z)+'\\n')\n")
					ostream.write("			i=i+1\n")
					ostream.write("		ifile.close()\n")
			ostream.write("print('ALL DONE.')\n")
		ostream.write("\n")			
#		ostream.write("ifile = open('settlments.dat', 'a' )\n")	
#		ostream.write("for node_id in top_nodes:\n")	
#		ostream.write("	node=model1.model_part.Nodes[node_id]\n")	
#		ostream.write("	ifile.write(str(node_id)+' '+str(node.X)+' '+str(node.Y)+' '+str(node.Z)+'\'+'n')\n")	

		#ostream.write("ifile.close()\n")	
		
		
		return