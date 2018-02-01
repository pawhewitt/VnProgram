import os
import numpy

def FMEReaderGMSH(file_path):
    '''
    FMEReaderGMSH reads data from a GMSH mesh file located at file_path.
    
    Reads the GMSH file and converts the coordinates from mm to m to use 
    for design velocity calculation
        
    Created on 30 July 2015
    
    @author: DAgarwal
    '''
    #print("FMEReaderGMSH")
    #print(file_path)
    if os.path.exists(file_path):
        FME_file = open(file_path, "r")
    else:
        print ("FMEReaderGMSH Error: Input file does not exist.")
        return
    
    #Read in file using readlines()  
    FME_lines = FME_file.readlines()
    
    for i in range(len(FME_lines)):
        FME_lines[i] = FME_lines[i].strip()
    
    #Close opened input file
    FME_file.close()
    
    #Initialise empty lists for point and facet data
    point_number_to_coords = {}
    #coords_to_point_number = {}
    element_number_to_point_numbers = {}
    point_number_to_element_numbers = {}
    element_number_to_surface_number = {}
          
    NODE = 0
    ELEMENT = 0
    kn=0
    ke=0
    point_number_ind={}    
    for i in range(len(FME_lines)):                
        split_line = FME_lines[i].split(" ")       
        split_line[:] = [x for x in split_line if len(x) != 0]
        if NODE == 1:
            if len(split_line) > 1:                
                point_number = int(split_line[0].strip()) - 1
                point_number_ind[point_number]=kn
                x_coord = float(split_line[1].strip())/1000    # divided by 1000 in order to convert coordinate values in mm
                y_coord = float(split_line[2].strip())/1000
                z_coord = float(split_line[3].strip())/1000                
                point_coords = (x_coord, y_coord, z_coord)                
                point_number_to_coords[point_number] = point_coords
                #coords_to_point_number[point_coords] = point_number
                kn=kn+1
        else:
            if ELEMENT == 1:                
                if len(split_line) > 1:
                    if split_line[1].strip() == "2":
                        surface_number = int(split_line[4].strip()) 
                        element_number = ke
                        element_point_1 = int(split_line[5].strip()) - 1
                        element_point_2 = int(split_line[6].strip()) - 1
                        element_point_3 = int(split_line[7].strip()) - 1
                        element_point_numbers = (element_point_1, element_point_2, element_point_3)
                
                        element_number_to_point_numbers[element_number] = element_point_numbers
                        element_number_to_surface_number[element_number] = surface_number
                        
                        for point_number in element_point_numbers:                        
                            if point_number in point_number_to_element_numbers:                            
                                point_number_to_element_numbers[point_number].append(element_number)                        
                            else:
                                point_number_to_element_numbers[point_number] = [element_number]
                        ke=ke+1
        if split_line != []:
            if split_line[0].strip()=="$Nodes":
                NODE = 1
            elif split_line[0].strip()=="$EndNodes":
                NODE = 0
            elif split_line[0].strip()=="$Elements":
                ELEMENT = 1
            else:
                if split_line[0].strip()=="$EndElements":
                    ELEMENT = 0
      
    return [point_number_to_coords, element_number_to_point_numbers, point_number_to_element_numbers,element_number_to_surface_number,point_number_ind]     

if __name__ == "__main__":    
    file_path = 'F:/Volkswagen/test.msh'   
    data =  FMEReaderGMSH(file_path)

    


    
    
    