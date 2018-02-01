
def VectorPlaneIntersection(point_p, point_normal, plane_point, plane_normal):
    
    '''   
    VectorPlaneIntersection calulcates the intersection point between a plane and a vector from a point P
    
    Inputs:
    
    point_p 
    
      
    Created on 29 Nov 2010
    @author: pthompson
    '''   
    # Called by TestPointTriangle
     
    #Calculate numerator and denominator for calculation separately to check if intersection exists
    numerator = (plane_point[0] - point_p[0])* plane_normal[0] + (plane_point[1] - point_p[1])* plane_normal[1] + (plane_point[2] - point_p[2])* plane_normal[2]
    
    denominator = point_normal[0]*plane_normal[0] + point_normal[1]*plane_normal[1] + point_normal[2]*plane_normal[2]
    
    try:
        distance_to_plane = numerator/denominator
        intersection_point = [point_p[0] + (distance_to_plane * point_normal[0]) , point_p[1] + (distance_to_plane * point_normal[1]) , point_p[2] + (distance_to_plane * point_normal[2])]
        return intersection_point
    
    except ZeroDivisionError:
        return "No intersection exists"