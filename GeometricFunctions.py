import numpy
from math import sqrt, acos, pi

def distance(point1,point2):
    separation = sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2+(point1[2]-point2[2])**2)
    return separation
    
def ComputeFacetAreas(point_number_to_coords, facet_number_to_point_numbers):
    '''
    ComputeFacetAreas returns a dictionary of facet areas calculated from dictionaries of point coordinates and facet points
       
    Created on 3 Dec 2010
    @author: pthompson
    '''
    
    facet_areas = {}
    
    for facet_number, point_numbers in facet_number_to_point_numbers.items():
          
        point_a = numpy.array(point_number_to_coords[point_numbers[0]])
        point_b = numpy.array(point_number_to_coords[point_numbers[1]])
        point_c = numpy.array(point_number_to_coords[point_numbers[2]])
          
        a_b = point_b - point_a
        a_c = point_c - point_a
        ab_x_ac = numpy.cross(a_b, a_c)
          
        facet_areas[facet_number] = 0.5*sqrt(numpy.dot(ab_x_ac, ab_x_ac.conj()))
          
    return facet_areas 
   
def ComputeFacetCentroids(point_number_to_coords, facet_number_to_point_numbers):
    '''
    ComputeFacetCentroids returns a dictionary of facet centroids calculated from dictionaries of point coordinates and facet points
       
    Created on 3 Dec 2010
    @author: pthompson
    '''
    
    facet_centroids = {}
    
    for facet_number, point_numbers in facet_number_to_point_numbers.items():
          
        point_a = point_number_to_coords[point_numbers[0]]
        point_b = point_number_to_coords[point_numbers[1]]
        point_c = point_number_to_coords[point_numbers[2]]
          
        facet_centroids[facet_number] = tuple([(point_a[0] + point_b[0] + point_c[0]) / 3, (point_a[1] + point_b[1] + point_c[1]) / 3, (point_a[2] + point_b[2] + point_c[2]) / 3])
          
    return facet_centroids

    
def ComputeFacetNormals(point_number_to_coords, facet_number_to_point_numbers):
    '''
    ComputeFacetNormals returns a dictionary of facet unit normals calculated from dictionaries of point coordinates and facet points
       
    Created on 3 Dec 2010
    @author: pthompson
    '''        
    facet_normals = {}
    
    for facet_number, point_numbers in facet_number_to_point_numbers.items():
        a = point_number_to_coords[point_numbers[0]]
        b = point_number_to_coords[point_numbers[1]]
        c = point_number_to_coords[point_numbers[2]]
        
        a_b = [b[0] - a[0], b[1] - a[1], b[2] - a[2]]
            
        a_c = [c[0] - a[0], c[1] - a[1], c[2] - a[2]]
        
        # Compute normal
        ab_x_ac = [a_b[1] * a_c[2] - a_b[2] * a_c[1], a_b[2] * a_c[0] - a_b[0] * a_c[2], a_b[0] * a_c[1] - a_b[1] * a_c[0]]
        #ab_x_ac = [a_b[1] * a_c[2] - a_b[2] * a_c[1], 0.0, a_b[0] * a_c[1] - a_b[1] * a_c[0]]
        # Compute magnitude
        mod_ab_x_ac = sqrt(ab_x_ac[0] * ab_x_ac[0] + ab_x_ac[1] * ab_x_ac[1] + ab_x_ac[2] * ab_x_ac[2])

       # if the mod_ab_x_ac variable is 0 then the current facet is given the normal of the previous facet 
        if mod_ab_x_ac == 0.0:
            
            facet_normals[facet_number] = facet_normals[facet_number -1]
        
        else:  
            # Get unit normal; 
            facet_normals[facet_number] = [ab_x_ac[0] / mod_ab_x_ac, ab_x_ac[1] / mod_ab_x_ac, ab_x_ac[2] / mod_ab_x_ac]  
    return facet_normals
    

def CompareNormals(normal_a, normal_b):   
    dot = round(normal_a[0]*normal_b[0] + normal_a[1]*normal_b[1] + normal_a[2]*normal_b[2], 6)    
    return ((acos(dot)) * (180 / pi))
    
def ComputeReverseFacetNormals(point_number_to_coords, facet_number_to_point_numbers):
    '''
    ComputeFacetNormals returns a dictionary of facet unit normals calculated from dictionaries of point coordinates and facet points
       
    Created on 3 Dec 2010
    @author: pthompson
    '''        
    facet_normals = {}
    
    for facet_number, point_numbers in facet_number_to_point_numbers.items():
        
        a = point_number_to_coords[point_numbers[0]]
        b = point_number_to_coords[point_numbers[1]]
        c = point_number_to_coords[point_numbers[2]]        
        a_b = [b[0] - a[0], b[1] - a[1], b[2] - a[2]]
            
        a_c = [c[0] - a[0], c[1] - a[1], c[2] - a[2]]
        # Compute normal
        ab_x_ac = [a_b[1] * a_c[2] - a_b[2] * a_c[1], a_b[2] * a_c[0] - a_b[0] * a_c[2], a_b[0] * a_c[1] - a_b[1] * a_c[0]]        
        # Compute magnitude
        mod_ab_x_ac = sqrt(ab_x_ac[0] * ab_x_ac[0] + ab_x_ac[1] * ab_x_ac[1] + ab_x_ac[2] * ab_x_ac[2])
       # if the mod_ab_x_ac variable is 0 then the current facet is given the normal of the previous facet 
        if mod_ab_x_ac == 0.0:            
            facet_normals[facet_number] = facet_normals[facet_number -1]        
        else:  
            # Get unit normal; 
            facet_normals[facet_number] = [-1*ab_x_ac[0] / mod_ab_x_ac, -1*ab_x_ac[1] / mod_ab_x_ac, -1*ab_x_ac[2] / mod_ab_x_ac]       
    return facet_normals
    