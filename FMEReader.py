import os
import numpy

def FMEReader(file_path):

    '''
    FMEReader reads data from a CADfix FME mesh file located at file_path.
        
    Created on 19 Nov 2011
    @author: pthompson
    '''    
    #print("FMEReader")
    #print(file_path)

    if os.path.exists(file_path):
        FME_file = open(file_path, "r")
    else:
        print ("FMEReader Error: Input file does not exist.")
        return
    
    #Read in file using readlines()  
    FME_lines = FME_file.readlines()
    
    for i in range(len(FME_lines)):
        FME_lines[i] = FME_lines[i].strip()
    
    #Close opened input file
    FME_file.close()
    
    #Initialise empty lists for point and facet data
    point_number_to_coords = {}
    coords_to_point_number = {}
    element_number_to_point_numbers = {}
    point_number_to_element_numbers = {}
          
    
    for i in range(len(FME_lines)):
        split_line = FME_lines[i].split(" ")
        
        split_line[:] = [x for x in split_line if len(x) != 0]

        if len(split_line) != 0:
        
            if split_line[0].strip() == "NODE":
                
                point_number = int(split_line[1].strip()) - 1
                x_coord = float(split_line[2].strip())/1000
                y_coord = float(split_line[3].strip())/1000
                z_coord = float(split_line[4].strip())/1000
                
                point_coords = (x_coord, y_coord, z_coord)
                
                point_number_to_coords[point_number] = point_coords
                coords_to_point_number[point_coords] = point_number
                
            elif split_line[0].strip() == "ELEM":
                
                if split_line[2].strip() != "TR3":
                    
                    print ("FMEReader Error: Elements must be of type TR3")
                    return
                                
                element_number = int(split_line[1].strip()) - 1
                element_point_1 = int(split_line[3].strip()) - 1
                element_point_2 = int(split_line[4].strip()) - 1
                element_point_3 = int(split_line[5].strip()) - 1
                element_point_numbers = (element_point_1, element_point_2, element_point_3)
                
                element_number_to_point_numbers[element_number] = element_point_numbers
                
        
                for point_number in element_point_numbers:
                        
                    if point_number in point_number_to_element_numbers:
                            
                        point_number_to_element_numbers[point_number].append(element_number)
                        
                    else:
                        point_number_to_element_numbers[point_number] = [element_number]
               
    return [point_number_to_coords, element_number_to_point_numbers, point_number_to_element_numbers] 

if __name__ == "__main__":    
    file_path = 'F:/Volkswagen/test.fme'   
    data =  FMEReader(file_path)    


    
    
    