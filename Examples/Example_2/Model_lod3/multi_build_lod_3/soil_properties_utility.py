import sys
import os
kratos_root_path = os.environ['KRATOS_ROOT_PATH']
##setting up paths
kratos_libs_path = kratos_root_path+'libs' ##kratos_root/libs
kratos_applications_path = kratos_root_path+'applications' ##kratos_root/applications
kratos_applications_path_nonfree = kratos_root_path+'applications_nonfree' ##kratos_root/applications_nonfree
ekate_auxiliary_path = kratos_root_path+'applications_nonfree/ekate_auxiliary_application/python_scripts'
##################################################################
##################################################################
sys.path.append(kratos_libs_path)
sys.path.append(kratos_applications_path)
sys.path.append(kratos_applications_path_nonfree)
sys.path.append(ekate_auxiliary_path)

#importing Kratos main library
from Kratos import *
#kernel = Kernel()   #defining kernel

from KratosStructuralApplication import *
# from KratosExternalSolversApplication import *
# from KratosEkateAuxiliaryApplication import *
# from KratosExternalConstitutiveLawsApplication import *
# from KratosMKLSolversApplication import *

class Material:
    def __init__( self, Id, polygon, params ):
        self.Id = Id
        self.polygon = polygon
        self.params = params

    # note: polygons are defined in x-z plane
    def IsInside( self, point ):
        n = len(self.polygon)
        inside = False
        p1x,p1y = self.polygon[0]
        for i in range(n+1):
            p2x,p2y = self.polygon[i % n]
            if point[2] > min(p1y,p2y):
                if point[2] <= max(p1y,p2y):
                    if point[0] <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (point[2]-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or point[0] <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y
        return inside

class SoilPropertiesUtility:
    def __init__( self, matfile ):
        print("initialized SoilPropertiesUtility")
        self.ReadMaterials( matfile )

    def ReadMaterials( self, matfile ):
        self.materials = {}
        print("reading materials from file: "+str(matfile))
        matdata = open( matfile, 'r' ).readlines()
        matblock = False
        polygonblock = False
        parametersblock = False
        matname = ""
        coords = []
        parameters = {}
        for line in matdata:
            if "begin material" in line:
                matblock = True
                matname = line.split()[2]
            elif "end material" in line:
                self.materials[matname] = Material(matname, coords, parameters)
                coords = []
                parameters = {}
                matblock = False
            elif "begin polygon" in line and matblock:
                polygonblock = True
            elif "end polygon" in line and matblock:
                polygonblock = False
            elif polygonblock and matblock:
                point_data = line.split()
                coords.append( (float(point_data[0]),float(point_data[2])) )
            elif "begin parameters" in line and matblock and not polygonblock:
                parametersblock = True
            elif "end parameters" in line:
                parametersblock = False
            elif parametersblock and matblock and not polygonblock:
                param = line.split()
                parameters[param[0]] = param[1]

    def SetMaterialProperties( self, model_part, element ):
        integration_points = element.GetIntegrationPoints()
        isotropic3dpointer = Isotropic3D()
        druckerpragerpointer = DruckerPrager()
        mohrcoulombpointer = MohrCoulomb3dImplicit()
        cl_pointers = []
        youngs_moduli = []
        poisson_ratios = []
        densities = []
        cohesions = []
        hardening_moduli = []
        K0_values = []
        internal_friction_angles = []
        dilatancy_angles = []
        density = 0.0
        for counter in range(0, len(integration_points) ):
            mat = self.GetMaterialID(integration_points[counter])
            if( mat != "dummy" ):
                material = self.materials[mat]
                if( material.params['model_type'] == "isotropic3d" ):
                    cl_pointers.append( isotropic3dpointer.Clone() )
                    youngs_moduli.append( float(self.materials[mat].params['youngs_modulus']) )
                    poisson_ratios.append( float(self.materials[mat].params['poisson_ratio']) ) 
                    K0_values.append( float(self.materials[mat].params['K0']) )
                    cohesions.append( 0.0 )
                    hardening_moduli.append( 0.0 )
                    internal_friction_angles.append( 0.0 )
                    dilatancy_angles.append( 0.0 )
                    densities.append( float(self.materials[mat].params['density']) )
                elif( material.params['model_type'] == "drucker_prager" ):
                    cl_pointers.append( druckerpragerpointer.Clone() )
                    youngs_moduli.append( float(self.materials[mat].params['youngs_modulus']) )
                    poisson_ratios.append( float(self.materials[mat].params['poisson_ratio']) )
                    K0_values.append( float(self.materials[mat].params['K0']) )
                    cohesions.append( float(self.materials[mat].params['cohesion']) )
                    hardening_moduli.append( float(self.materials[mat].params['hardening_modulus']) )
                    internal_friction_angles.append( float(self.materials[mat].params['internal_friction_angle']) )
                    dilatancy_angles.append( float(self.materials[mat].params['internal_friction_angle']) ) # by default, only associative plasticity is supported
                    densities.append( float(self.materials[mat].params['density']) )
                elif( material.params['model_type'] == "mohr_coulomb" ):
                    cl_pointers.append( mohrcoulombpointer.Clone() )
                    youngs_moduli.append( float(self.materials[mat].params['youngs_modulus']) )
                    poisson_ratios.append( float(self.materials[mat].params['poisson_ratio']) )
                    K0_values.append( float(self.materials[mat].params['K0']) )
                    cohesions.append( float(self.materials[mat].params['cohesion']) )
                    hardening_moduli.append( float(self.materials[mat].params['hardening_modulus']) )
                    internal_friction_angles.append( float(self.materials[mat].params['internal_friction_angle']) )    
                    dilatancy_angles.append( float(self.materials[mat].params['dilatancy_angle']) )    
                    densities.append( float(self.materials[mat].params['density']) )
                else:
                    print("ERROR: Material not defined")
                    sys.exit(0)
            density = float(self.materials[mat].params['density'])
            porosity = float(self.materials[mat].params['porosity'])                                  
            permeability = float(self.materials[mat].params['permeability'])
        if( len(cl_pointers) != len(integration_points) ):
            print("ERROR: not all points are defined")
            sys.exit(0)
        element.SetValuesOnIntegrationPoints( CONSTITUTIVE_LAW, cl_pointers, model_part.ProcessInfo )
        element.SetValuesOnIntegrationPoints( K0, K0_values, model_part.ProcessInfo )
        element.SetValue( DENSITY, float(density) )
        element.SetValue( POROSITY, float(porosity) )
        element.SetValue( PERMEABILITY_WATER, float(permeability) )
        element.SetValuesOnIntegrationPoints( YOUNG_MODULUS, youngs_moduli, model_part.ProcessInfo )
        element.SetValuesOnIntegrationPoints( POISSON_RATIO, poisson_ratios, model_part.ProcessInfo )
        element.SetValuesOnIntegrationPoints( COHESION, cohesions, model_part.ProcessInfo )
        element.SetValuesOnIntegrationPoints( ISOTROPIC_HARDENING_MODULUS, hardening_moduli, model_part.ProcessInfo )
        element.SetValuesOnIntegrationPoints( INTERNAL_FRICTION_ANGLE, internal_friction_angles, model_part.ProcessInfo )
        element.SetValuesOnIntegrationPoints( DILATANCY_ANGLE, dilatancy_angles, model_part.ProcessInfo )
        element.ResetConstitutiveLaw()

    def GetMaterialID( self, point ):
        for material in self.materials:
            if self.materials[material].IsInside( point ):
                return material
        print("XXXXXXXXX")
        print(point)
        return("dummy")
