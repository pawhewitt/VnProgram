from math import sqrt
from numpy import *

def VnComputation(unperturbed_point, unperturbed_normal, perturbed_entity_type, perturbed_entity_coordinates,local_path,perturbation_value):
    '''
    VnComputation returns a single scalar value for design velocity
    
    unperturbed_point is an xyz coordinate
    unperturbed normal is and xyz normal direction
    perturbed_entity_type is "point" which defines the projected point in perturbed geometry
    perturbed_entity_coordinates contains 1,2,or 3 xyz coordinates (depending on entity type)
    
    Created on 15 Dec 2010

    @author: Peter
    
    Modified by DAgarwal on 22/10/2015

    '''
   # Called by DesignVelocityFieldComputation()
     
    #opf1=open(str(local_path)+"VnComputation.txt","a")
    
    if perturbed_entity_type == "point":
        
        perturbed_point = perturbed_entity_coordinates
        dp = [perturbed_point[0] - unperturbed_point[0], perturbed_point[1] - unperturbed_point[1], perturbed_point[2] - unperturbed_point[2]]
        if perturbation_value == 0.0:
            Vn=0.0
        else:
            Vn = (dp[0] * unperturbed_normal[0] + dp[1] * unperturbed_normal[1] + dp[2] * unperturbed_normal[2])/perturbation_value
        dp1=array(dp)
        dp=sqrt(dp[0]*dp[0]+dp[1]*dp[1]+dp[2]*dp[2])
        #opf1.write("{}\t{}\n".format(Vn,"point"))
             
        return Vn,dp,dp1
    elif perturbed_entity_type == "edge":
        
        perturbed_point_a = perturbed_entity_coordinates[0]
        perturbed_point_b = perturbed_entity_coordinates[1]
    
        ab = [perturbed_point_b[0] - perturbed_point_a[0], perturbed_point_b[1] - perturbed_point_a[1], perturbed_point_b[2] - perturbed_point_a[2]]
        
        ac = [unperturbed_point[0] - perturbed_point_a[0], unperturbed_point[1] - perturbed_point_a[1], unperturbed_point[2] - perturbed_point_a[2]]
        
        t = (ac[0]*ab[0] + ac[1]*ab[1] + ac[2]*ab[2]) / (ab[0]*ab[0] + ab[1]*ab[1] + ab[2]*ab[2])
        
        point_d = [perturbed_point_a[0] + (t * ab[0]), perturbed_point_a[1] + (t * ab[1]), perturbed_point_a[2] + (t * ab[2])]
        
        dp = [point_d[0] - unperturbed_point[0], point_d[1] - unperturbed_point[1], point_d[2] - unperturbed_point[2]]
        
        Vn = (dp[0] * unperturbed_normal[0] + dp[1] * unperturbed_normal[1] + dp[2] * unperturbed_normal[2])
        dp1=dp
        dp=sqrt(dp[0]*dp[0]+dp[1]*dp[1]+dp[2]*dp[2])
	
        #opf1.write("{}\t{}\n".format(Vn,"edge"))
                   
        return Vn,array(dp),dp1

    else:
        
        return "VnComputation Error: entity_type must be 'point'"
    
    
if __name__ == "__main__":
    
    unperturbed_point = (0,0,0)
    unperturbed_normal = (1,0,0)
    perturbed_entity_type = "point"
    perturbed_entity_coordinates = (1.0,1,1)   

