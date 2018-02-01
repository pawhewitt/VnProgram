# -*- coding: utf-8 -*-
"""
@author: DAgarwal
Created on: 26/02/2016
"""
from math import sqrt
from numpy import *

def MeshElementArea(point_number_to_coords,facet_number_to_point_numbers):
    
    element_area = {}
    element_number = 0
    for vertex in list(facet_number_to_point_numbers.values()):
        a_b = [point_number_to_coords[vertex[1]][0]-point_number_to_coords[vertex[0]][0],point_number_to_coords[vertex[1]][1]-point_number_to_coords[vertex[0]][1],point_number_to_coords[vertex[1]][2]-point_number_to_coords[vertex[0]][2]]
        a_c = [point_number_to_coords[vertex[2]][0]-point_number_to_coords[vertex[0]][0],point_number_to_coords[vertex[2]][1]-point_number_to_coords[vertex[0]][1],point_number_to_coords[vertex[2]][2]-point_number_to_coords[vertex[0]][2]]                    
    #Compute cross product AB x AC and compute modulus of resulting vector
        ab_x_ac = [a_b[1] * a_c[2] - a_b[2] * a_c[1], a_b[2] * a_c[0] - a_b[0] * a_c[2], a_b[0] * a_c[1] - a_b[1] * a_c[0]]
        mod_ab_x_ac = sqrt(ab_x_ac[0] * ab_x_ac[0] + ab_x_ac[1] * ab_x_ac[1] + ab_x_ac[2] * ab_x_ac[2])                   
    #Compute current triangular element area as half the modulus of the cross product of two edge vectors
        element_area[element_number] = 0.5 * mod_ab_x_ac
        element_number += 1
    return element_area