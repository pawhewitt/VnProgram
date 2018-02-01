from TestPointTriangle import TestPointTriangle
from BruteForceProjection import BruteForceProjection
from BruteForceNearestNormal import BruteForceNearestNormal
from math import *

#################################################################################################################################

def Projection(point_p, point_p_normal, nearest_facet_number, tree,point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed, angle_tolerance, facet_number_to_centroid_coords, point_number_to_facet_numbers, centroid_coords_to_facet_number, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,angthreshold):
    '''
    Projection computes the projection of a point and normal onto a perturbed faceting.
    
    Inputs:
    
    point_p
    point_p_normal
    point_number_to_coords_perturbed
    coords_to_point_number
    facet_number_to_point_numbers_perturbed
    angle_tolerance
    
    Outputs:
    
    entity_type
    entity_details
       
    Created on 3 Dec 2010
    @author: pthompson
    
    Modified by DAgarwal on 15 Oct 2015
    '''
    
    # Called by DesignVelocityField Computation()
    # Calls TestPointTriangle(),BruteForceProjection() 
   
    #Find nearest neighbour point
    #nearest_point_data = tree.query(point_p, 1)

    #nearest_facet_number = tree.query(point_p, 1)[1]
    nearest_point = facet_number_to_centroid_coords[nearest_facet_number]
         
    separation = sqrt((point_p[0] - nearest_point[0])**2 + (point_p[1] - nearest_point[1])**2 + (point_p[2] - nearest_point[2])**2) 
        
    if separation < 1e-10: #numpy.allclose(point_p, nearest_point):
        projection_details = ("identical_centroid_point", (nearest_facet_number))
        return projection_details, "IdenticalPoint"
        
    current_facet_point_numbers = facet_number_to_point_numbers_perturbed[nearest_facet_number]
    facet_coords = [point_number_to_coords_perturbed[point_number] for point_number in current_facet_point_numbers]
    facet_normal = facet_normals_perturbed[nearest_facet_number]
        
    projection_test = TestPointTriangle(point_p, point_p_normal, facet_coords, facet_normal)
        
    if projection_test[0] == 1:
        if projection_test[2] <= angle_tolerance:
            if projection_test[3] <= current_min_separation:                                                                  
                point_details = projection_test[4]
                projection_details =  ("point",point_details,nearest_facet_number)                       
                return projection_details, "point"    
        #elif projection_test[0] == 2:
        #    edge_details = (facet_number_to_point_numbers_perturbed[nearest_facet_number][0], facet_number_to_point_numbers_perturbed[nearest_facet_number][2])                     
        #    projection_details =  ("edge",edge_details)                   
        #elif projection_test[0] == 3:
        #    edge_details = (facet_number_to_point_numbers_perturbed[nearest_facet_number][0], facet_number_to_point_numbers_perturbed[nearest_facet_number][1])
        #    projection_details =  ("edge",edge_details)
        #elif projection_test[0] == 4:
        #    edge_details = (facet_number_to_point_numbers_perturbed[nearest_facet_number][1], facet_number_to_point_numbers_perturbed[nearest_facet_number][2])
        #    projection_details =  ("edge",edge_details)
        #elif projection_test[0] == 5:
        #    point_details = (facet_number_to_point_numbers_perturbed[nearest_facet_number][0])
        #    projection_details =  ("point",point_details)
        #elif projection_test[0] == 6:
        #    point_details = (facet_number_to_point_numbers_perturbed[nearest_facet_number][1])
        #    projection_details =  ("point",point_details)
        #elif projection_test[0] == 7:
        #    point_details = (facet_number_to_point_numbers_perturbed[nearest_facet_number][2])
        #    projection_details =  ("point",point_details)
        
    #return projection_details, "InitialFacets"                                                                                    
    #Begin testing different facets, given initial test unsuccessful
    #Use first nearest_neighbour facet as initial facet to start procedure
    current_facet_number = nearest_facet_number
    previously_tested_facets = []    
    counter = 0
    #BruteForceNearestNormal(point_p, point_p_normal, tree, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,facet_number_to_centroid_coords,angthreshold)
    while True:        
        counter += 1        
        if counter > 300:
            
            return BruteForceProjection(point_p, point_p_normal, point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed, angle_tolerance, tree, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,facet_number_to_centroid_coords,angthreshold), "BruteForce"
          
        if current_facet_number in previously_tested_facets:
            
            if previously_tested_facets[-2] is current_facet_number:
                
                return BruteForceProjection(point_p, point_p_normal, point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed, angle_tolerance, tree, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,facet_number_to_centroid_coords,angthreshold), "BruteForce"
                
        #Test current facet
        current_facet_point_numbers = facet_number_to_point_numbers_perturbed[current_facet_number]
        facet_coords = [point_number_to_coords_perturbed[point_number] for point_number in current_facet_point_numbers]
        previously_tested_facets.append(current_facet_number)
        
        facet_normal = facet_normals_perturbed[current_facet_number]
        
        projection_test = TestPointTriangle(point_p, point_p_normal, facet_coords, facet_normal) 
        
        nearest_point = facet_number_to_centroid_coords[current_facet_number]
        separation = sqrt((point_p[0] - nearest_point[0])**2 + (point_p[1] - nearest_point[1])**2 + (point_p[2] - nearest_point[2])**2)    
         
        if projection_test[0] == 1:
            if projection_test[3] <= current_min_separation:
                if projection_test[2] <= angle_tolerance:
                    point_details = projection_test[4]
                    projection_details =  ("point",point_details,current_facet_number)                                                 
                    return projection_details, "ProjectionAlgorithm"                                
                else:
                #Has nowhere to go - BruteForceSearch
                    return BruteForceProjection(point_p, point_p_normal, point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed, angle_tolerance, tree, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,facet_number_to_centroid_coords,angthreshold), "BruteForce"
            else:
                #Has nowhere to go - BruteForceSearch
                return BruteForceProjection(point_p, point_p_normal, point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed, angle_tolerance, tree, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,facet_number_to_centroid_coords,angthreshold), "BruteForce"
        
################################################################################################################                
        elif projection_test[0] is 8:#Return value 8 indicates point projects outside triangle and facet sharing edge AC should be tested next
            
            edge_AC_point_numbers = (facet_number_to_point_numbers_perturbed[current_facet_number][0], facet_number_to_point_numbers_perturbed[current_facet_number][2])
            
            point_A_facets = point_number_to_facet_numbers[edge_AC_point_numbers[0]]   #FindFacetsSharingPoint(edge_AC_point_numbers[0], facet_number_to_point_numbers_perturbed)
            point_C_facets = point_number_to_facet_numbers[edge_AC_point_numbers[1]]   #FindFacetsSharingPoint(edge_AC_point_numbers[1], facet_number_to_point_numbers_perturbed)
            
            point_A_facets = set(point_A_facets)
            point_C_facets = set(point_C_facets)
            
            common_facets = point_A_facets.intersection(point_C_facets)
            common_facets.remove(current_facet_number)
                        
            if len(list(common_facets)) is 0:
                     
                #edge_details = (edge_AC_point_numbers[0], edge_AC_point_numbers[1])
                #projection_details =  ("edge",edge_details)
                #return projection_details, "ProjectionAlgorithm - Geometric edge"                        
                return BruteForceProjection(point_p, point_p_normal, point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed, angle_tolerance, tree, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,facet_number_to_centroid_coords,angthreshold), "BruteForce"
            else:              
                next_facet_to_test = list(common_facets)[0]
            
        elif projection_test[0] is 9:#Return value 9 indicates point projects outside triangle and facet sharing edge AB should be tested next
            
            edge_AB_point_numbers = (facet_number_to_point_numbers_perturbed[current_facet_number][0], facet_number_to_point_numbers_perturbed[current_facet_number][1])
            
            point_A_facets = point_number_to_facet_numbers[edge_AB_point_numbers[0]]  #FindFacetsSharingPoint(edge_AB_point_numbers[0], facet_number_to_point_numbers_perturbed)
            point_B_facets = point_number_to_facet_numbers[edge_AB_point_numbers[1]]   #FindFacetsSharingPoint(edge_AB_point_numbers[1], facet_number_to_point_numbers_perturbed)
            
            point_A_facets = set(point_A_facets)
            point_B_facets = set(point_B_facets)
            
            common_facets = point_A_facets.intersection(point_B_facets)
            common_facets.remove(current_facet_number)
    
            if len(list(common_facets)) is 0:
                #edge_details = (edge_AB_point_numbers[0], edge_AB_point_numbers[1])
                #projection_details =  ("edge",edge_details)
                #return projection_details, "ProjectionAlgorithm-Geometric edge"
                return BruteForceProjection(point_p, point_p_normal, point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed, angle_tolerance, tree, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,facet_number_to_centroid_coords,angthreshold), "BruteForce"               
            else:              
                next_facet_to_test = list(common_facets)[0]
            
        elif projection_test[0] is 10:#Return value 10 indicates point projects outside triangle and facet sharing edge BC should be tested next
            
            edge_BC_point_numbers = (facet_number_to_point_numbers_perturbed[current_facet_number][1], facet_number_to_point_numbers_perturbed[current_facet_number][2])
            
            point_B_facets = point_number_to_facet_numbers[edge_BC_point_numbers[0]]   #FindFacetsSharingPoint(edge_BC_point_numbers[0], facet_number_to_point_numbers_perturbed)
            point_C_facets = point_number_to_facet_numbers[edge_BC_point_numbers[1]]   #FindFacetsSharingPoint(edge_BC_point_numbers[1], facet_number_to_point_numbers_perturbed)
            
            point_B_facets = set(point_B_facets)
            point_C_facets = set(point_C_facets)
            
            common_facets = point_B_facets.intersection(point_C_facets)
            common_facets.remove(current_facet_number)
    
            if len(list(common_facets)) is 0:
                #edge_details = (edge_BC_point_numbers[0], edge_BC_point_numbers[1])
                #projection_details =  ("edge",edge_details)
                #return projection_details, "ProjectionAlgorithm-Geometric edge"  
                return BruteForceProjection(point_p, point_p_normal, point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed, angle_tolerance, tree, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,facet_number_to_centroid_coords,angthreshold), "BruteForce"              
            else:              
                next_facet_to_test = list(common_facets)[0]
        
        elif projection_test[0] is -1: #Return value -1 indicates no projection possible (point normal parallel to plane of facet)
            return BruteForceProjection(point_p, point_p_normal, point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed, angle_tolerance, tree, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,facet_number_to_centroid_coords,angthreshold), "BruteForce"
            
        current_facet_number = next_facet_to_test