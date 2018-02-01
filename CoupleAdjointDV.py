"""
CoupleAdjointDV is used to link the calculated design velocities and link them with adjoint sensitivities

Author: DAgarwal
Last Modified: 23/02/2015
"""
from numpy import *
import ast
from ParametricSensitivityVW import ParametricSensitivityVW
from ParametricSensitivityNodeRR import ParametricSensitivityNodeRR
from FMEReaderGMSH import FMEReaderGMSH
from GeometricFunctions import ComputeFacetNormals
#from RRSensitivityReader import RRSensitivityReader
#from RRadjointReader import RRadjointReader
from RRadjointReaderNodesTurb import RRadjointReaderNodesTurb
from RRadjointReaderNodesNGV import RRadjointReaderNodesNGV
from VWadjointReader import VWadjointReader
from AbaqusAdjointReaderQuadTet import AbaqusAdjointReader
from ParametricSensitivityAbaqus import ParametricSensitivityAbaqus
from parametric_effectiveness import ParametricEffectiveness
from FMEReader import FMEReader
from parametric_effectiveness_powerset import ParametricEffectivenessPowerSet
from datetime import datetime
from time import sleep
#from parametric_effectiveness import ParametricEffectivenessSelected
#from parametric_effectiveness import dJdVmax


def CoupleAdjointDV(adj_type,adjoint_data_path,directory_path,local_dir,file_type):
    local_path = directory_path+ local_dir   
    centroid_vn_data_file = open(str(local_path) + "centroid_vn_data" + ".dat", 'r')
    data_files = centroid_vn_data_file.readlines()
    perturbation_values = ast.literal_eval(data_files[0])
    for n,i in enumerate(perturbation_values):
        if i==0.0:
            perturbation_values[n]=1.0
    #parameter_names = ast.literal_eval(data_files[1])
    parameter_numbers = ast.literal_eval(data_files[1])
    centroids_Vn={}
    for i in range(len(perturbation_values)):
        centroids_Vn[i] = ast.literal_eval(data_files[2+i])
    if file_type == "fme":
        unperturbed_geometry = FMEReader(local_path+"\\0.fme")
    elif file_type == "msh":
        unperturbed_geometry = FMEReaderGMSH(local_path+"0.msh")
                    
    point_number_to_coords_unperturbed = unperturbed_geometry[0] # coordinates of points in unpurturbed geometry
    facet_number_to_point_numbers_unperturbed = unperturbed_geometry[2]
    facet_normals_unperturbed = ComputeFacetNormals(point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed)     
    senstivity_data_file = open(str(directory_path) + str(local_dir) + "senstivity_data" + ".dat", 'w')   
    if adj_type == 1:                      
        #adjoint_data = RRadjointReaderNodesTurb(adjoint_data_path,directory_path,local_dir) # Reading directly from sensitivity file to get nodal normal, sens, and coordinates
        adjoint_data = RRadjointReaderNodesNGV(adjoint_data_path,directory_path,local_dir)
        adjoint_node_coord = adjoint_data[0]                
        adjoint_node_sens = adjoint_data[1]
        adjoint_node_normal = adjoint_data[2]
        [parametric_sensitivities,element_data] = ParametricSensitivityNodeRR(point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed, directory_path, centroids_Vn, parameter_numbers,local_dir,facet_normals_unperturbed,adjoint_node_coord,adjoint_node_sens,adjoint_node_normal)
    elif adj_type == 2:
        adjoint_data = VWadjointReader(adjoint_data_path,directory_path + local_dir)                                             
        adjoint_element_centroids = adjoint_data[0]
        adjoint_element_area = adjoint_data[1]
        adjoint_element_normals = adjoint_data[2]
        adjoint_element_sens = multiply(adjoint_data[3],1)
        
        [parametric_sensitivities,element_data,element_data1,element_data_dv] = ParametricSensitivityVW(point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed, adjoint_element_centroids, adjoint_element_normals, adjoint_element_sens, directory_path, centroids_Vn, parameter_numbers,local_dir,facet_normals_unperturbed,adjoint_element_area,perturbation_values)
        #dJdV_max=dJdVmax(adjoint_element_area,adjoint_element_sens)
        #parameter_numbers=[0,1,5,7,9,15,16,17,19]
        [dJdV_parametric,Parametric_Effectiveness_full,dJdV_max,SteepestDecentStep]=ParametricEffectiveness(adjoint_element_area, adjoint_element_sens, parameter_numbers,element_data,parametric_sensitivities,element_data_dv)
        maxsensparam=max(dJdV_parametric.values())        
        senstivity_data_file.write("parameteric Effectiveness of Complete Model is" + " " + str(Parametric_Effectiveness_full) + "\n")
        senstivity_data_file.write("Max. parameteric Effectiveness of variables in Model is" + " " + str(maxsensparam) +" " + "for parameter" + str(dJdV_parametric.values().index(maxsensparam)+1)+ "\n")
        senstivity_data_file.write("Steepest Decent Step for the parameter space is" + " " + str(SteepestDecentStep)+ "\n")
        start_time1 = datetime.now()        
#        [parametric_effectiveness,parameter_comb_list]=ParametricEffectivenessPowerSet(adjoint_element_area, adjoint_element_sens, parameter_numbers,element_data_dv,parametric_sensitivities,directory_path,local_dir,element_data_dv)
#        end_time1 = datetime.now()   
#        delta_t = end_time1 - start_time1
#        senstivity_data_file. write("Time taken for PowerSet Calculation" + " " + str(delta_t)+ "\n")
#        MaxEffectiveness=max(parametric_effectiveness.values())
#        ind = parametric_effectiveness.values().index(MaxEffectiveness)
#        senstivity_data_file. write("Maximum achievable parametric effectiveness is" + " " + str(MaxEffectiveness)+ " for parametric combination of " +str(parameter_comb_list[ind]) + "\n")
#        print parameter_comb_list[ind], MaxEffectiveness
    elif adj_type == 3:
        adjoint_data = AbaqusAdjointReader(adjoint_data_path,directory_path,local_dir)                       
        adjoint_element_centroids = adjoint_data[0]
        adjoint_element_area = adjoint_data[1]
        adjoint_element_normals = adjoint_data[2]
        adjoint_element_sens = adjoint_data[3]
        [parametric_sensitivities,element_data,Element_sens,intphida,intda] = ParametricSensitivityAbaqus(point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed, adjoint_element_centroids, adjoint_element_normals, adjoint_element_sens, directory_path, centroids_Vn, parameter_numbers,local_dir,facet_normals_unperturbed,adjoint_element_area)                    
    
    #sumSi2=sum(square(array(parametric_sensitivities.values())))        
    #senstivity_data_file. write("Sum Si^2 is " + " " + str(sumSi2) + "\n")
        
    for parameter_number in parameter_numbers[1:]:
        senstivity_data_file. write("parameteric Sensitivity of parameter" + " " + str(parameter_number) + "  " + str(parametric_sensitivities[parameter_number]) + "\n")
        if adj_type == 2:
            senstivity_data_file. write("parameteric Effectiveness of parameter" + " " + str(parameter_number) + "  " + str(dJdV_parametric[parameter_number]) + "\n")            
        #if node_normal == 1:
        #    RRTecplot_sens_dv_node(adjoint_sens_path,directory_path  + local_dir + str(current_part_name) + str(parameter_number) + ".dat" ,element_data[parameter_number])
        #else:
        #    RRTecplot_sens_dv(adjoint_sens_path,directory_path  + local_dir + str(current_part_name) + str(parameter_number) + ".dat" ,element_data[parameter_number],adjoint_element_sens)        
                   
    senstivity_data_file.close()    
if __name__ == "__main__":
        
    #adjoint_data_path = "None"
    RR = 0 # 0 or 1 based on which sensitivity input to be used
    VW = 0 
    Abaqus =1
    if RR == 1:
        #adjoint_data_path = "F:/Rolls-Royce/RR_Data_TurbineBlade/Sensitivity/"
        adjoint_data_path = "F:/Rolls-Royce/RR_Data_NGV/Sensitivity/"
        #adjoint_data_path = "None"
        directory_path="F:/Rolls-Royce/"
        current_min_separation = 0.001 # Max design velocity expected based on perturbation
        adj_type = 1
        node_normal = 1
    elif VW == 1:
        adjoint_data_path = "F:/Volkswagen/SensInput/0sensitivitiesBaseParam/"
        #adjoint_data_path = "C:/Users/3050094/Documents/Queen1/VW-Design-Velocity/SensInput/structFineSensBase/"
        directory_path="F:/Volkswagen/"
        adj_type = 2
    elif Abaqus == 1:
        adjoint_data_path = "F:/Abaqus-Design-Velocity/PlateAutomation/Sensitivity/"
        directory_path="F:/Abaqus-Design-Velocity/PlateAutomation/"
        current_min_separation = 0.2 # Max design velocity expected based on perturbation
        adj_type = 3
        node_normal = 0
    else:
        adjoint_data_path = "None"
        directory_path="C:/Users/3050094/Documents/Queen1/VW-Design-Velocity/"
        adj_type = 0 
    adjoint_sens_path = "C:/Users/3050094/Documents/Queen1/RR-Design-Velocity/SensInput/sensitivity_map.dat"    
    # File format for the mesh 
    #file_type = "fme"      # for CADFix Mesher
    file_type = "msh"     # for GMSH mesher

    #local_dir="DesignSBendBaseSketch1a/"
    #local_dir="DesignSBendBaseInsert/"
    #local_dir="DesignSBendBaseProfileInsert/"
    #local_dir="RR_Data_TurbineBlade/"
    #local_dir="RR_Data_NGV_DV/"
    #local_dir="MurrayExample/"
    local_dir = "Step0/"
    overallBoundaryMovement = 0.00012
    
    ResultMainAdjoint=CoupleAdjointDV(adj_type,adjoint_data_path,directory_path,local_dir,file_type)
   