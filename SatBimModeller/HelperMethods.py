import sys
import os
import math

class HelperMethods:

	# Convert integer
	@staticmethod
	def DetectAndConvert2Integer(s):
		if( s - int(s) == 0):
			return int(s)
		else:
			return s
	
	# Read a parameter file
	@staticmethod	
	def ReadParamFile(pathToFile):
		file = open(pathToFile,'r')
		input = file.readlines()
		params = {}

		
		for line in input:
			values = line.split()
			if len(values)==2:
				try:
					params[values[0]] = HelperMethods.DetectAndConvert2Integer(float(values[1]))
				except:
					params[values[0]] = values[1]
			else:
				params[values[0]] =[]
				for i in range(1, len(values)):
					params[values[0]].append (values[i])
				
		return params
	# Read a parameter file
	@staticmethod	
	def ReadAlignmentFile(pathToFile):
		file = open(pathToFile+'alignment.dat','r')
		lines = file.readlines()
		n_points = len(lines)
		coords=[[0 for x in xrange(3)] for x in xrange(n_points)]
		i=0
		for line in lines:
			columns = line.split()
			point_id=int(columns[0])
			coords[point_id][0]=float(columns[1])
			coords[point_id][1]=float(columns[2])
			coords[point_id][2]=float(columns[3])
		#tranform coordinates to meters
		#for i in range (1, len(coords)):
		#	for j in range (0,3):
		#		coords[i][j]= coords[0][j]+(coords[i][j]-coords[0][j])/100.0
			
		return coords
		
		
	@staticmethod			
	def ReadBuildingFile(pathToFile):
		file = open(pathToFile+'building.dat','r')
		lines = file.readlines()
		n_points = len(lines)
		coords=[[0 for x in xrange(2)] for x in xrange(n_points)]
		i=0
		for line in lines:
			columns = line.split()
			coords[i][0]=float(columns[0])
			coords[i][1]=float(columns[1])
			i=i+1
		return coords
		
	@staticmethod			
	def ReadRingRotationFile(pathToFile):
		file = open(pathToFile+'lining_ring_rotations.dat','r')
		lines = file.readlines()
#		print(lines)
		n_points = len(lines)
		rotations=[0 for x in xrange(n_points)]

		for i in range(0,len(lines)):
			columns = lines[i].split()
			#print(columns[0])
			#rotations[i]=columns[0]*math.pi()/180.0
			#rotations[i]=float(columns[0]) -1.0
			rotations[i]=float(columns[0])

			rotations[i]=rotations[i]*180+180.0
			#rotations[i]=rotations[i]*60.0+180.0
		#print(rotations)
			
		return rotations
		
	@staticmethod	
	def ReadMaterialFile(pathToFile):
		file = open(pathToFile,'r')
		lines = file.readlines()
		n_points = len(lines)
		params={}
		for line in lines:
			columns = line.split()
			i=1
			j=1
			k=1
			if columns[0]=='youngs_modulus':
				params[str('E_soil_'+str(i))] = float(columns[1])
				i=i+1
			if columns[0]=='density':
				params[str('ro_soil_'+str(j))] = float(columns[1])
				j=j+1
			if columns[0]=='poisson_ratio':
				params[str('nu_soil_'+str(j))] = float(columns[1])
				j=j+1
			if columns[0]=='K0':
				params[str('K0_'+str(j))] = float(columns[1])
				j=j+1
				
#		print params
		return params
		#def InvokeGID(self, component_name):
		#	subprocess.check_output([self.gid_path+'gid_offscreen.bat', '-offscreen', '-b', component_name, self.params['model_name']], cwd=self.working_dir) # +self.working_dir )
		
		
