from FMEReader import FMEReader
from FMEReaderGMSH import FMEReaderGMSH
from GeometricFunctions import ComputeFacetNormals
from GeometricFunctions import ComputeFacetCentroids
from GeometricFunctions import CompareNormals
from Projection import Projection
from VnComputation import VnComputation
from scipy.spatial.ckdtree import *
from MeshElementArea import MeshElementArea
#import sys
from numpy import *
from CreateTecplotDATP import CreateTecplotDATP

################################################################################################################################################

def DesignVelocityFieldComputation(local_path, parameter_names, file_type, length_perturbation_size_mm, angle_perturbation_size_deg,local_dir,current_min_separation,angle_tolerance,angthreshold,perturbation_values):
    '''
    DesignVelocityFieldComputation returns a series of design velocity fields
    
    Created on 15 Dec 2010

    @author: PThompson
    
    Modified by DAgarwal on 22/10/2015
    '''
    
    # Called by Main()
    # Calls FMEReader(),ComputeFacetNormals(),ComputeFacetCentroids(),Projection(),CreateTecplotDAT(),VnComputation()
    
    centroids_Vn = {}
    # create array to store displacements, nearest elements and perturbed facet id's
    parameter_dp={}
    parameter_facet_id={}
    parameter_near_point={}
        
    # Read in the unpertubed mesh
    
    if file_type == "fme":
        unperturbed_geometry = FMEReader(local_path+"\\0.fme")
    elif file_type == "msh":
        unperturbed_geometry = FMEReaderGMSH(local_path+"0.msh")
                    
    point_number_to_coords_unperturbed = unperturbed_geometry[0] # coordinates of points in unpurturbed geometry
    facet_number_to_point_numbers_unperturbed = unperturbed_geometry[1] # vertex numbers associated with unpurturbed facet
    point_number_to_facet_numbers_unperturbed = unperturbed_geometry[2] # point on which facets
    point_number_ind_unperturbed= unperturbed_geometry[3]
    element_area=MeshElementArea(point_number_to_coords_unperturbed,facet_number_to_point_numbers_unperturbed)    
    facet_normals_unperturbed = ComputeFacetNormals(point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed) 
    facet_centroids_unperturbed = ComputeFacetCentroids(point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed)
    CreateTecplotDATP(point_number_to_coords_unperturbed,facet_number_to_point_numbers_unperturbed, local_path,facet_normals_unperturbed,0,point_number_ind_unperturbed)
    # Read in geometry for perturbed designs
    
    centroids_Vn[0] = [0]*len(list(facet_centroids_unperturbed.keys()))    
    centroid_vn_data_file = open(str(local_path) + "centroid_vn_data" + ".dat", 'w')
    centroid_vn_data_file.write(str(perturbation_values[1:])+ "\n")
    centroid_vn_data_file.write(str(list(parameter_names.keys()))+ "\n")
    centroid_vn_data_file.write(str(list(parameter_names.values()))+ "\n")
    centroid_vn_data_file.write(str(centroids_Vn[0])+ "\n")
    
    for parameter_number in list(parameter_names.keys())[1:]:
           
        if file_type == "fme":
            current_perturbed_geometry = FMEReader(local_path + str(parameter_number) + ".fme")
        elif file_type == "msh":
            current_perturbed_geometry = FMEReaderGMSH(local_path + str(parameter_number) + ".msh")
            
        point_number_to_coords_perturbed = current_perturbed_geometry[0]
        facet_number_to_point_numbers_perturbed = current_perturbed_geometry[1]
        point_number_to_facet_numbers = current_perturbed_geometry[2]
        point_number_ind= current_perturbed_geometry[3]
                              
        current_perturbation_centroid_Vn = {}
        current_perturbation_centroid_Vn.clear()
        points_list = []
        No_projection_facets=[]        
        # Get the centroid coords for all elements                        
        facet_number_to_centroid_coords = ComputeFacetCentroids(point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed)
        
        # Get the unit normal vector for all elements
        facet_normals_perturbed = ComputeFacetNormals(point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed) 
        
        # Write the deformed mesh to tecplot output file
        CreateTecplotDATP(point_number_to_coords_perturbed,facet_number_to_point_numbers_perturbed, local_path,facet_normals_perturbed,parameter_number,point_number_ind)
    
        centroid_coords_to_facet_number = dict([[facet_number_to_centroid_coords[k],k] for k in list(facet_number_to_centroid_coords.keys())])
        
        for centroid_coords in list(facet_number_to_centroid_coords.values()):   
            points_list.append(centroid_coords)
           
        tree = cKDTree(points_list)        
        nearest_facets = tree.query(list(facet_centroids_unperturbed.values()), 1)[1]
        # create arrays to store displacements and perturbed facet id's
        dp={}
        perturbed_facet_id={}
        near_point={}
        current_Vn={}#[0]*len(list(parameter_names.keys()))
        
        for facet_number_unperturbed in facet_centroids_unperturbed.keys():
            facet_centroid_unperturbed = facet_centroids_unperturbed[facet_number_unperturbed] 
            near_facet = nearest_facets[facet_number_unperturbed]           
            near_point[facet_number_unperturbed]=near_facet                               
            current_projection = Projection(facet_centroid_unperturbed, facet_normals_unperturbed[facet_number_unperturbed], near_facet,tree, point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed, angle_tolerance, facet_number_to_centroid_coords, point_number_to_facet_numbers, centroid_coords_to_facet_number, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,angthreshold)
            if current_projection[0][0] =="No Intersection exist":
                current_Vn[0] = 0.0
                current_Vn[1] = 0.0
                current_Vn[2] = array([0.0,0.0,0.0])
                perturbed_facet_id[facet_number_unperturbed]=1
                No_projection_facets.append(facet_number_unperturbed)
            elif current_projection[0][0] == "No projection possible":
                current_Vn[0] = 0.0
                current_Vn[1] = 0.0
                current_Vn[2] = array([0.0,0.0,0.0])
##########################################################################################
                perturbed_facet_id[facet_number_unperturbed]=1
                No_projection_facets.append(facet_number_unperturbed)#addition
##########################################################################################                
            else:
                if current_projection[0][0] == "identical_centroid_point":                    
                    current_Vn[0] = 0.0
                    current_Vn[1] = 0.0
                    current_Vn[2] = array([0.0,0.0,0.0])
                    perturbed_facet_id[facet_number_unperturbed]=current_projection[0][1]
                else:                   
                    if current_projection[0][0] == "point":                            
                        perturbed_entity_coords = current_projection[0][1]
                        perturbed_facet_id[facet_number_unperturbed]=current_projection[0][2]
                    else:                    
                        perturbed_entity_coords = [point_number_to_coords_perturbed[point_number] for point_number in current_projection[0][1]]
                        perturbed_facet_id[facet_number_unperturbed]=3                                          
                    current_Vn = VnComputation(facet_centroid_unperturbed, facet_normals_unperturbed[facet_number_unperturbed], current_projection[0][0], perturbed_entity_coords,local_path,perturbation_values[parameter_number])
                current_Vn=list(current_Vn)                  
            current_perturbation_centroid_Vn[facet_number_unperturbed] = current_Vn[0]
            #Store the displacment information
            dp[facet_number_unperturbed]=current_Vn[2]
            
###############################################################################################################
        iteration=0
        ang=30
        No_projection_facets=[]
        while len(No_projection_facets) != 0:
            No_projection_facets_update=[]              
            for j in range(len(No_projection_facets)):
                i=0
                k=0
                k1=0
                edge_point_numbers = (facet_number_to_point_numbers_unperturbed[No_projection_facets[j]])            
                point_A_facets = point_number_to_facet_numbers_unperturbed[edge_point_numbers[0]]   
                point_C_facets = point_number_to_facet_numbers_unperturbed[edge_point_numbers[1]]   
                point_B_facets = point_number_to_facet_numbers_unperturbed[edge_point_numbers[2]]
#
                point_A_facets = set(point_A_facets)
                point_B_facets = set(point_B_facets)
                point_C_facets = set(point_C_facets)
                common_facets_1 = point_A_facets.union(point_C_facets)
                nearby_facets = list(common_facets_1.union(point_B_facets))
                nearby_facets.remove(No_projection_facets[j])     
                while i<len(nearby_facets):
                    angle_between_normals=CompareNormals(facet_normals_unperturbed[No_projection_facets[j]],facet_normals_unperturbed[nearby_facets[i]])                
                    if angle_between_normals < ang:
                        if perturbed_facet_id[nearby_facets[i]] != 1:                    
                            current_perturbation_centroid_Vn[No_projection_facets[j]] += current_perturbation_centroid_Vn[nearby_facets[i]]
                            dp[No_projection_facets[j]] += dp[nearby_facets[i]]
                            k=k+1
                        else:
                            k1 = k1+1
                    else:
                        k1 = k1+1
                    i=i+1
                if k>0:
                    perturbed_facet_id[No_projection_facets[j]]=4
                    current_perturbation_centroid_Vn[No_projection_facets[j]]=current_perturbation_centroid_Vn[No_projection_facets[j]]/k
                    dp[No_projection_facets[j]]=dp[No_projection_facets[j]]/k
                else:
                    No_projection_facets_update.append(No_projection_facets[j])
            if No_projection_facets_update == No_projection_facets:
                break
            No_projection_facets=No_projection_facets_update
            iteration += 1                        
######################################################################################################################################################
        centroids_Vn[parameter_number] = list(current_perturbation_centroid_Vn.values())
        centroid_vn_data_file.write(str(list(current_perturbation_centroid_Vn.values()))+ "\n")

    centroid_vn_data_file.close()    
    return (point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed, facet_normals_unperturbed, centroids_Vn, point_number_to_facet_numbers_unperturbed,element_area,point_number_ind_unperturbed,dp)
    