
'''
The Main file is used to run the QUB design velocity calculation module and
is linked with adjoint sensitivities to calculate the gradients.It can be run
individually or with optimization modules. Further it can be used to perturb 
parameters in CATIA V5 or can be executed on already existing .STEP files.
The required sub-modules for this tool are as stated below
1) Numpy
2) Scipy
3) sys
4) datatime and time
5) OS
6) DesignVelocityFieldComputation
7) CreateTecplotDAT
8) CreateCWC (used with CADfix)
9) RRadjointReaderNodesNGV (RRD Specific)
10) RRadjointReaderNodesTurb (RRD Specific)
11) ParametricSensitivityNodeRR (RRD specific)
12) CreateAbaqusODB (To create Visualization plot in Abaqus)
13) ParametricSensitivityVW (VW specific)
14) VWadjointReader (VW specific)
15) GeometricFunctions
16) parametric_effectiveness
17) parametric_effectiveness_powerset
18) AbaqusAdjointReader (Abaqus Specific)
19) ParametricSensitivityAbaqus (Abaqus Specific)
20) parametric_effectiveness_Abaqus (Abaqus Specific)
21) CreateTecplotDAT (To create DV plot in Tecplot)

@author: DAgarwal
@created on: 23/03/2016
'''

####General python modules###############################
from datetime import datetime
from time import sleep
import os
import subprocess
import sys
from numpy import *
import numpy
from Write_Disp import Write_Disp
#####################################################################################
######Catia Perturbation Script##################

# Temp 1 Feb 2018 Philp Hewitt -----Commented for standalone 
#from increment_parameters1 import IncrementParameters

#################################################
######Display Module############
from CreateAbaqusODB import CreateAbaqusODB
from CreateTecplotDAT import CreateTecplotDAT
######################################################
######Design Velocity Modules######
from DesignVelocityFieldComputation import DesignVelocityFieldComputation

#################################################################
from ParametricSensitivitySU2 import ParametricSensitivitySU2

#============================================================================================

def Main(adjoint_data_path = "None", directory_path = "None", file_type = "VRML", length_perturbation_size_mm = 1.0, angle_perturbation_size_deg = 1.0,local_dir="/Design_0/sens/",data="sens",current_min_separation = 0.001,angle_tolerance = 60,angthreshold = 5,node_normal = 1,adj_type=0):#,GMSH_path = "None",CADFix_path = "None",Abaqus='1',VW='1'):

	start_time = datetime.now()
	time_stamp_string = start_time.strftime("%d-%m-%y_%H%M%S")
	start_time_string = start_time.strftime("%d-%m-%y %H:%M:%S.%f")

	local_path=directory_path+local_dir

	if data =="sens":
		#parameter type User is used to perturb only user defines parameters while All is used to perturb all the defined parameters                
		parameter_type = "User"
		#parameter_type = "All"
		increment_parameters_output = IncrementParameters(parameter_type, length_perturbation_size_mm, angle_perturbation_size_deg,directory_path,local_dir)

		parameter_names = increment_parameters_output[0]
		current_part_name = increment_parameters_output[1]
		perturbation_values = increment_parameters_output[3]
		parameter_values = increment_parameters_output[4]

		end_time = datetime.now()
		end_time_string = end_time.strftime("%d-%m-%y_%H:%M:%S.%f")    
		delta_t = end_time - start_time
		senstivity_data_file = open(str(directory_path) + str(local_dir) + "senstivity_data" + ".dat", 'a')
		senstivity_data_file.write("StepFiles creation completed in "+str(delta_t)+"\n")
		senstivity_data_file.close()

	elif data=="disp":
		parameter_number = 0
		while True:
			if os.path.exists(local_path+ str(parameter_number+1) + ".stp"):
				parameter_number +=1
			else:
				break        
		number_of_parameters = parameter_number
		           
		current_part_name = "Part_1"

		parameter_names = {}
		parameter_names[0] = "DatumModel"
		perturbation_values=[0]*(number_of_parameters+1)
		parameter_values=[0]*(number_of_parameters+1)
		for i in range(1, number_of_parameters + 1):
			parameter_names[i] = str(i)
			perturbation_values[i] = length_perturbation_size_mm
		end_time = datetime.now()
		end_time_string = end_time.strftime("%d-%m-%y_%H:%M:%S.%f") 
		delta_t = end_time - start_time
		print ("StepFiles creation completed in "+str(delta_t))

	parameter_numbers = list(parameter_names.keys())
# file type msh specifies GMSH to be used as surface meshing tool                              
	if file_type == "msh":
		GMSH={}
		for parameter_number in list(parameter_names.keys()):
			GMSH[parameter_number] = subprocess.Popen("gmsh" + " " + "-2" +" -clmax 4.0 " + " " + str(parameter_number) + ".stp", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE,cwd = local_path)
			GMSH[parameter_number].communicate()                  

	Vn_field_data = DesignVelocityFieldComputation(local_path, parameter_names, file_type, length_perturbation_size_mm, angle_perturbation_size_deg,local_dir,current_min_separation,angle_tolerance,angthreshold,perturbation_values)    
	point_number_to_coords_unperturbed = Vn_field_data[0]
	facet_number_to_point_numbers_unperturbed = Vn_field_data[1]
	facet_normals_unperturbed = Vn_field_data[2]                                                       
	centroids_Vn = Vn_field_data[3]
	point_number_ind= Vn_field_data[6]    
	point_number_to_facet_numbers_unperturbed = Vn_field_data[4]
	element_area = Vn_field_data[5]
	CreateTecplotDAT(point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed, centroids_Vn, parameter_names, current_part_name, time_stamp_string, local_path, point_number_to_facet_numbers_unperturbed,facet_normals_unperturbed,point_number_ind)

######### Displacement data print out #########
	Write_Disp(Vn_field_data)	

###############################################################################################################    
	if adjoint_data_path is not "None":
		senstivity_data_file = open(str(directory_path) + str(local_dir) + "senstivity_data" + ".dat", 'a')
		if adj_type == 4:
			[parametric_sensitivities,element_data,element_data_dv] = ParametricSensitivitySU2(point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed, adjoint_data_path, centroids_Vn, parameter_numbers,local_dir,perturbation_values,facet_normals_unperturbed)
			for parameter_number in list(parameter_names.keys())[1:]:
				senstivity_data_file.write("parameteric Sensitivity of parameter" + " " + str(parameter_number) + "  " + str(parametric_sensitivities[parameter_number]) + "\n")
			
		senstivity_data_file.close()
      ###########################################################################          

  #print ("run_time = " + str(delta_t2-delta_t1))
	return (list(parameter_names.values())[1:],parameter_values[1:],perturbation_values[1:],list(centroids_Vn.values())[1:],list(element_area.values()))
#==================================================================================================================================


#===================================================================================================================================
if __name__ == "__main__":
    
    # Get path for Step Files
    import os
    Vn_Run= os.environ['Vn_Run']



    #Provide the details of test case as below by using 0 or 1

    SU2=1

    if SU2 == 1:
        adjoint_data_path = "None"#"F:/WingTestCase/Optimization/NACA2D/Thickness-18-Drag-Zeroalpha/SensDataFiles/"
        directory_path=Vn_Run
        current_min_separation = 1 # Max design velocity expected based on perturbation
        adj_type = 4

    file_type = "msh"     # for GMSH mesher
    angle_tolerance = 30 # used to compare two face normals for projection validation
    angthreshold = 2    # used to verify the orientation of nearby cells for averaging
    data = "disp"      # to use parameters in opened CATIA V5 model
    local_dir ="Onera/"
    
    ResultMain=Main(adjoint_data_path, directory_path, file_type,0.5,0.5,local_dir,data,current_min_separation,angle_tolerance,angthreshold,adj_type)
    
    
    
    