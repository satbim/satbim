import sys
import os
import math
import numbers
from HelperMethods import *

class ModelComponent:
	# Variables
	DISABLE_COMPONENT = 0
	
	# Constructor
	def __init__(self, global_params, working_dir):
		self.params = []
		self.lod_prepare_handlers = []
		self.lod_script_handlers = []
		self.global_params = global_params
		self.component_name = ""
		self.working_dir = working_dir
		self.is_collapsable = False
		
	def ReadParams(self, pathToParamFile):
		# Read parameters from file
		self.params = HelperMethods.ReadParamFile(pathToParamFile)
		
		# Read LOD from param file
		self.lod = self.params['lod']
		
		# debug output
		print "Params for " + self.component_name + ": "
		print self.params
		
		return
		
	def PrepareModel(self, ostream):
		# Prepare model batch file

		#check how many elements:
		if isinstance(self.lod, numbers.Integral)==True:
			# LOD 0 means component is disabled
			if self.lod == ModelComponent.DISABLE_COMPONENT:
				print 'PrepareModel: Component ' + self.component_name + ' is deactivated (LOD = 0)'
			# Else: self.lod - 1 is correct index, since lod starts at 1 but array at 0
			elif (self.lod - 1) >= len(self.lod_prepare_handlers):
				print 'PrepareModel: Error, lod = ' + str(self.lod) + ' invalid'
			# Else: call correct handler
			else:
				lod_handler = self.lod_prepare_handlers[self.lod - 1]
				lod_handler(ostream)
		else:

			lod_handler = self.lod_prepare_handlers[2]
			lod_handler(ostream)
	def AddToSimScript(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		if isinstance(self.lod, numbers.Integral)==True:		
			# LOD 0 means component is disabled
			if self.lod == ModelComponent.DISABLE_COMPONENT:
				print 'AddToSimScript: Component ' + self.component_name + ' is deactivated (LOD = 0)'
			# Else: self.lod - 1 is correct index, since lod starts at 1 but array at 0
			elif (self.lod - 1) >= len(self.lod_script_handlers):
				print 'AddToSimScript: Error, lod = ' + str(self.lod) + ' invalid'
			# Else: call correct handler
			else:
				lod_handler = self.lod_script_handlers[self.lod - 1]
				lod_handler(ostream)
		else:
			lod_handler = self.lod_script_handlers[2]
			lod_handler(ostream)		
		
		return
	