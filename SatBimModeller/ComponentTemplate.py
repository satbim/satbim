import sys
import os
import math
from ModelComponent import *

class SoilComponent(ModelComponent):

	# Constructor
	def __init__(self, global_params, working_dir):
		ModelComponent.__init__(self, global_params, working_dir)
		
		# Setup LOD handlers
		self.lod_prepare_handlers = [self.PrepareModel_Lod1, self.PrepareModel_Lod2, self.PrepareModel_Lod3]
		self.lod_script_handlers = [self.AddToSimScript_Lod1, self.AddToSimScript_Lod2, self.AddToSimScript_Lod3]
		
		# Define name
		self.component_name = "soil"
		
	def PrepareModel_Lod1(self, ostream):
		# Write model to .bch output file
		print 'Soil LOD = 1'
		
		return
	
	def PrepareModel_Lod2(self, ostream):
		# Write model to .bch output file
		print 'Soil LOD = 2'
		
		
		return
		
	def PrepareModel_Lod3(self, ostream):
		# Write model to .bch output file
		print 'Soil LOD = 3'
		
		return
		
	def AddToSimScript_Lod1(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Soil SimScript LOD = 1'
		
		return
		
	def AddToSimScript_Lod2(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Soil SimScript LOD = 2'
		
		return
		
	def AddToSimScript_Lod3(self, ostream):
		# Write the appropriate entries to the stream for the simulation script
		print 'Soil SimScript LOD = 3'
		
		return