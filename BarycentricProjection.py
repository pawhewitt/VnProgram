
def TriangleArea2D(x1,y1,x2,y2,x3,y3):
    
    '''   
    TriangleArea2D computes twice the 2D projected area from  3 x-y points
    
    Created on 29 Nov 2010
    @author: pthompson
    '''   
    
    return (x1-x2)*(y2-y3) - (x2-x3)*(y1-y2)
    


def BarycentricProjection(point_p, facet_points_abc):
    
    '''   
    BarycentricProjection computes the u,v,w barycentric coordinates of an xyz point P with respect to a triangular facet defined by 3 xyz points(A,B,C)
    
    Follows method from "Real-time Collision Detection" by Ericson (Section 3.4)
    
    Created on 29 Nov 2010
    @author: pthompson
    '''   
     
    facet_point_a = facet_points_abc[0]
    facet_point_b = facet_points_abc[1]
    facet_point_c = facet_points_abc[2]
          
    a_b = [facet_points_abc[1][0] - facet_points_abc[0][0], facet_points_abc[1][1] - facet_points_abc[0][1], facet_points_abc[1][2] - facet_points_abc[0][2]]       
    a_c = [facet_points_abc[2][0] - facet_points_abc[0][0], facet_points_abc[2][1] - facet_points_abc[0][1], facet_points_abc[2][2] - facet_points_abc[0][2]]    
    facet_normal = [a_b[1] * a_c[2] - a_b[2] * a_c[1] , a_b[2] * a_c[0] - a_b[0] * a_c[2] , a_b[0] * a_c[1] - a_b[1] * a_c[0] ]
    
    
    #Compute areas in plane of largest projection
    
    if abs(facet_normal[1]) <= abs(facet_normal[0]) >= abs(facet_normal[2]):        
        #x is largest, therefore project to yz plane
        nominator_u = TriangleArea2D(point_p[1],point_p[2], facet_point_b[1],facet_point_b[2], facet_point_c[1],facet_point_c[2]) #Area of PBC in yz plane
        nominator_v = TriangleArea2D(point_p[1],point_p[2], facet_point_c[1],facet_point_c[2], facet_point_a[1],facet_point_a[2]) #Area of PCA in yz plane
        inverse_denominator = 1.0 / facet_normal[0]
        
    
    elif abs(facet_normal[0]) <= abs(facet_normal[1]) >= abs(facet_normal[2]):        
        #y is largest, therefore project to xz plane
        nominator_u = TriangleArea2D(point_p[0],point_p[2], facet_point_b[0],facet_point_b[2], facet_point_c[0],facet_point_c[2]) #Area of PBC in xz plane
        nominator_v = TriangleArea2D(point_p[0],point_p[2], facet_point_c[0],facet_point_c[2], facet_point_a[0],facet_point_a[2]) #Area of PCA in xz plane
        inverse_denominator = -1.0 / facet_normal[1]
            
    else:
        #z is largest, therefore project to xy plane
        nominator_u = TriangleArea2D(point_p[0],point_p[1], facet_point_b[0],facet_point_b[1], facet_point_c[0],facet_point_c[1]) #Area of PBC in xy plane
        nominator_v = TriangleArea2D(point_p[0],point_p[1], facet_point_c[0],facet_point_c[1], facet_point_a[0],facet_point_a[1]) #Area of PCA in xy plane
        inverse_denominator = 1.0 / facet_normal[2]
    
    #Compute u,v,w barycentric coordinates and return result

    u = nominator_u * inverse_denominator
    v = nominator_v * inverse_denominator
    w = 1.0 - u - v
    
    barycentric = [u,v,w]
    return barycentric
    
    
