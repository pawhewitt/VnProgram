from math import sqrt
from VectorPlaneIntersection import VectorPlaneIntersection
from BarycentricProjection import BarycentricProjection
from GeometricFunctions import CompareNormals

#######################################################################################
def TestPointTriangle(point_p, point_normal, perturbed_facet_points, perturbed_facet_normal):
    '''
    TestPointTriangle tests if a point projects within a triangle
    
    Created on 15 Dec 2010

    @author: Peter
    '''
    # Called by Projection
    # Calls VectorPlaneIntersection(), CompareNormals(),BarycentricProjection()
    
    def stage1(perturbed_facet_points):
   
        a_b = [perturbed_facet_points[1][0] - perturbed_facet_points[0][0], perturbed_facet_points[1][1] - perturbed_facet_points[0][1], perturbed_facet_points[1][2] - perturbed_facet_points[0][2]]
            
        a_c = [perturbed_facet_points[2][0] - perturbed_facet_points[0][0], perturbed_facet_points[2][1] - perturbed_facet_points[0][1], perturbed_facet_points[2][2] - perturbed_facet_points[0][2]]
            
        ab_x_ac = [a_b[1] * a_c[2] - a_b[2] * a_c[1], a_b[2] * a_c[0] - a_b[0] * a_c[2], a_b[0] * a_c[1] - a_b[1] * a_c[0]]
                
        return ab_x_ac
        
    def stage2(ab_x_ac):        

        mod_ab_x_ac = sqrt(ab_x_ac[0] * ab_x_ac[0] + ab_x_ac[1] * ab_x_ac[1] + ab_x_ac[2] * ab_x_ac[2])
        # Compute unti normal vector
        if mod_ab_x_ac == 0:
            
            return (-1, "No projection possible")
        else:            
            perturbed_facet_normal = [ab_x_ac[0] / mod_ab_x_ac, ab_x_ac[1] / mod_ab_x_ac, ab_x_ac[2] / mod_ab_x_ac]        
       
        return perturbed_facet_normal
        
    def stage3(perturbed_facet_normal, perturbed_facet_points):
        
        angle_between_normals = CompareNormals(point_normal, perturbed_facet_normal)
        
        perturbed_facet_centroid = [(perturbed_facet_points[0][0] + perturbed_facet_points[1][0] + perturbed_facet_points[2][0]) / 3.0, (perturbed_facet_points[0][1] + perturbed_facet_points[1][1] + perturbed_facet_points[2][1]) / 3.0, (perturbed_facet_points[0][2] + perturbed_facet_points[1][2] + perturbed_facet_points[2][2]) / 3.0]    

        stage3 = [perturbed_facet_centroid, angle_between_normals]
        
        return stage3
    
    def stage4(point_p, point_normal, perturbed_facet_centroid, perturbed_facet_normal):
        projected_point_p = VectorPlaneIntersection(point_p, point_normal, perturbed_facet_centroid, perturbed_facet_normal)
        
        return projected_point_p
          
    # No stage 5?
    
    def stage6(projected_point_p, perturbed_facet_points):    
    
        uvw = BarycentricProjection(projected_point_p, perturbed_facet_points)
        # Note the following modifies the Barycentric coordinates according to certain set tolerances
        
      ##########################
        uvw = [round(x, 6) for x in uvw]
#        #
#        #####
#        ##tol = 0.1
#        #########
#        tol =0.00001
#        #tol = tol*tol
#        ##
#        ##
#        if uvw[0]*uvw[0] <= tol:
#            uvw[0] = 0.0
#        ##    
#        if (1 - (uvw[0]*uvw[0])) <= tol:
#            uvw[0] = 1.0
#        ##    
#        if uvw[1]*uvw[1] <= tol:
#            uvw[1] = 0.0
#        ##    
#        if (1 - (uvw[1]*uvw[1])) <= tol:
#            uvw[1] = 1.0
#        ##    
#        if uvw[2]*uvw[2] <= tol:
#            uvw[2] = 0.0
#        ##    
#        if (1 - (uvw[2]*uvw[2])) <= tol:
#            uvw[2] = 1.0
        #
        #################
        return uvw
        
    # Compute normal
    ab_x_ac = stage1(perturbed_facet_points)

    # Compute unit normal
    perturbed_facet_normal = stage2(ab_x_ac)
    if perturbed_facet_normal[1] == "No projection possible":          
        return (-1, "No projection possible")
    

    # Compute centroid and compare normal angles
    stage3 = stage3(perturbed_facet_normal, perturbed_facet_points)
    perturbed_facet_centroid = stage3[0]
    angle_between_normals = stage3[1]

    # Computed the projected point with vectorplane_intersection()
    projected_point_p = stage4(point_p, point_normal, perturbed_facet_centroid, perturbed_facet_normal)
    
#    separation =sqrt(separation)
    
    if projected_point_p == "No intersection exists":              
        return (-1, "No projection possible")        
            
    separation = sqrt((point_p[0] - projected_point_p[0])**2 + (point_p[1] - projected_point_p[1])**2 + (point_p[2] - projected_point_p[2])**2) 
    # Get the Barycentric coordinates 
    uvw = stage6(projected_point_p, perturbed_facet_points)   
     
    # Determine projected point location relative to element        
    def stage7(uvw):        
        u = uvw[0]
        v = uvw[1]
        w = uvw[2]
    
        return_value = -1 
    
        if v >= 0:
            if w >= 0:
                if (v + w) <= 1:
                    return_value = 1 #Return value 1 indicates point projects within facet
#                if (v + w) == 1:
#                    return_value = 4 #Return value 4 indicates point projects onto edge BC
    
#        if v == 0:
#            if w == 0:
#                return_value = 5 #Return value 5 indicates point projects onto point A
#        
#            if 0 < w < 1:
#                return_value = 2 #Return value 2 indicates point projects onto edge AC
#            
#            if w == 1:
#                return_value = 7 #Return value 7 indicates point projects onto point C
#        
#        if w == 0:
#            if 0 < v < 1:
#                return_value = 3 #Return value 3 indicates point projects onto edge AB
#        
#        if v == 1:
#            if w == 0:
#                return_value = 6 #Return value 6 indicates point projects onto point B
        
        if v < 0:
            return_value = 8 #Return value 8 indicates point projects outside triangle and facet sharing edge AC should be tested next
    
        if w < 0:
            return_value = 9 #Return value 9 indicates point projects outside triangle and facet sharing edge AB should be tested next
    
        if (v + w) > 1:
            return_value = 10 #Return value 10 indicates point projects outside triangle and facet sharing edge BC should be tested next
    
        return return_value
   
    return_value = stage7(uvw)
    
    return (return_value, uvw, angle_between_normals, separation, projected_point_p)   