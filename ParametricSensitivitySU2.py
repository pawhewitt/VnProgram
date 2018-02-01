from GeometricFunctions import ComputeFacetCentroids
from scipy.spatial.ckdtree import *
import os


def ParametricSensitivitySU2(point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed, adjoint_data_path, centroids_Vn, parameter_numbers,local_dir,perturbation_values,facet_normals_unperturbed):
    '''
    ParametricSensitivitySU2 is used to calculate the parametric sensitivities
    customized for Test Cases run by SU2
    
    Created on 4 Oct 2016
    
    @author: DAgarwal
    '''
    #sens_dv_data = adjoint_data_path + "surface_adjoint_dvs.csv"
    sens_data = adjoint_data_path + "surface_adjoint.csv"
       
#####################################################################     
    #Open DAT file. If file doesn not exist print error message and exit function
    if os.path.exists(sens_data):
        sens_data_points = open(sens_data, "r")
    else:
        print ("SU2toDAT Error: Sensitivity Input files does not exist.")
        return
    
    #Read in points file using readlines()  
    SU2_lines_points = sens_data_points.readlines()
    
    for i in range(len(SU2_lines_points)):
        SU2_lines_points[i] = SU2_lines_points[i].strip()
    
    #Close opened input file
    sens_data_points.close()
    adjoint_point_coordinates = {}
    adjoint_point_sens={}
    element_data_dv_adj = {}  
    point_number = 0
    
    for i in range(1,len(SU2_lines_points)):        
        #Split current line
        split_line_points = SU2_lines_points[i].split(",")        
        if split_line_points[0].strip() is not "":
            try:                                   
                adjoint_point_coordinates[point_number] = (float(split_line_points[7]), float(split_line_points[8]), float(split_line_points[9]))
                adjoint_point_sens[point_number] = (float(split_line_points[1]))
                element_data_dv_adj[point_number]=[]            
                point_number += 1
            except:                                    
                adjoint_point_coordinates[point_number] = (float(split_line_points[6]), float(split_line_points[7]), 0.0)
                adjoint_point_sens[point_number] = (float(split_line_points[1]))
                element_data_dv_adj[point_number]=[]            
                point_number += 1
    
    adjoint_point_coordinates=list(adjoint_point_coordinates.values())
    adjoint_point_sens=list(adjoint_point_sens.values())
    len_adjoint_points=len(adjoint_point_sens)
###############################################################################################################       
    facet_number_to_centroid_coords = ComputeFacetCentroids(point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed)
    
    #Create list of points from dictionary of coord values and create kd-tree from list
    points_list = []    
    [points_list.append(x) for x in facet_number_to_centroid_coords.values()]            
    tree = cKDTree(points_list)

    current_parameter_element_vn_sens = {}
    element_data_dv = {}
    
    near_point={}
    element_data = {}
    near_point = tree.query(adjoint_point_coordinates,2)[1]

    delta_J = {}
    #sens_dv_data = open(sens_dv_data, "w")        
    for parameter_number in range(1,len(parameter_numbers)):        
        current_parameter_element_vn_sens = {}
        current_parameter_element_vn_sens.clear()
        element_data_parameter = []
        element_data_current_parameter = []        
        current_perturbation_centroids_Vn = centroids_Vn[parameter_number]
        delta_J_current_parameter = 0.0        
        for k2 in range(len_adjoint_points):
            current_point_Vn = current_perturbation_centroids_Vn[near_point[k2][0]]
            current_point_normal=facet_normals_unperturbed[near_point[k2][0]]
#            if abs(current_point_Vn)<1E-7:
#                sens_dv_data.write("0.0,"+str(current_point_normal[0])+","+str(current_point_normal[1])+","+str(current_point_normal[0])+"\n")
#                 #element_data_dv_adj[k2].append(0.0)
#            else:
#                #element_data_dv_adj[k2].append(current_point_Vn)
#                sens_dv_data.write(str(current_point_Vn)+","+str(current_point_normal[0])+","+str(current_point_normal[1])+","+str(current_point_normal[0])+"\n")
            delta_J_current_parameter += -current_point_Vn * adjoint_point_sens[k2]
            element_data_parameter.append(current_point_Vn)
            element_data_current_parameter.append([k2, adjoint_point_sens[k2], current_point_Vn])
                      
        delta_J[parameter_number] = delta_J_current_parameter
        element_data_dv[parameter_number] = element_data_parameter
        element_data[parameter_number] = element_data_current_parameter
   
#    for i in range(len_adjoint_points):      
#        sens_dv_data.write(",".join(map(str, element_data_dv_adj[i]))+"\n")
    #sens_dv_data.close()     
    return (delta_J,element_data,element_data_dv)
    

