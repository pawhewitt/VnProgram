from TestPointTriangle import TestPointTriangle
from scipy.spatial import ckdtree
#from scipy.spatial inport *
from BruteForceNearestNormal import BruteForceNearestNormal
from math import *

##############################################################################################

def BruteForceProjection(point_p, point_p_normal, point_number_to_coords_perturbed, facet_number_to_point_numbers_perturbed, angle_tolerance, tree, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,facet_number_to_centroid_coords,angthreshold):
    '''
    BruteForceProjection uses a brute force method to search for nearest 200 elements 
    to find a successful projection from unperturbed geometry to perturbed geometry. In
    case of no successful projection it calls BruteForceNearestNormal
    
    BruteForceProjection is called from Projection.py file

    '''     
    # n is the number of neighbouring elements to return. Check the lit on python kdtree

    n = 200
    #radius = current_min_separation
    if len(facet_number_to_point_numbers_perturbed.keys()) > n:
        #successful_projections = []
        nearest_facets = tree.query(point_p,n)
        nearest_facet_numbers = nearest_facets[1]                      
                
        #nearest_facets = tree.query_ball_point(point_p, radius,p=2)#editing
        #nearest_facet_numbers = nearest_facets    
        for current_facet_number in nearest_facet_numbers:           
            current_facet_point_numbers = facet_number_to_point_numbers_perturbed[current_facet_number]
            
            facet_coords = [point_number_to_coords_perturbed[point_number] for point_number in current_facet_point_numbers]
            facet_normal = facet_normals_perturbed[current_facet_number]
            
            projection_test = TestPointTriangle(point_p, point_p_normal, facet_coords, facet_normal)
            
            #nearest_point = facet_number_to_centroid_coords[current_facet_number]
            #separation = sqrt((point_p[0] - nearest_point[0])**2 + (point_p[1] - nearest_point[1])**2 + (point_p[2] - nearest_point[2])**2)
            if projection_test[0] == 1:
                if projection_test[2] <= angle_tolerance:            
                    if projection_test[3] <= current_min_separation:
                        point_details = projection_test[4]
                        current_best_projection =  ("point",point_details,current_facet_number)
                        return current_best_projection

        #return ("No projection possible",facet_number_unperturbed)        
        return BruteForceNearestNormal(point_p, point_p_normal, tree, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,facet_number_to_centroid_coords,angthreshold)