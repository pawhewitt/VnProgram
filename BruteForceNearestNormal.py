from GeometricFunctions import CompareNormals
##############################################################################################

def BruteForceNearestNormal(point_p, point_p_normal, tree, facet_normals_perturbed,facet_number_unperturbed,current_min_separation,facet_number_to_centroid_coords,angthreshold):
    '''
    BruteForceProjectionnew uses a brute force method to find the nearest facet with similar surface normal
    It is called from Projection.py and BruteForceProjection.py files
    '''
    n = 200

    nearest_facets = tree.query(point_p, n)#editing
    nearest_facet_numbers = nearest_facets[1]
    nearest_facet_distance = nearest_facets[0]

    for i in range(len(nearest_facet_numbers)):
        current_facet_number = nearest_facet_numbers[i]        
        facet_normal = facet_normals_perturbed[current_facet_number]
        normal_test = CompareNormals(point_p_normal,facet_normal)      
        if normal_test < angthreshold:
            if nearest_facet_distance[i] <= current_min_separation:
                current_best_projection = ("point", facet_number_to_centroid_coords[current_facet_number],current_facet_number) 
                return current_best_projection
    return ("No projection possible",facet_number_unperturbed)          