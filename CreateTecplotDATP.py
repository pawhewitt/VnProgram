import math

########################################################################################################

def CreateTecplotDATP(point_number_to_coords_unperturbed,facet_number_to_point_numbers_unperturbed, local_path,facet_normals_unperturbed,parameter_number,point_number_ind_unperturbed):
    
    '''   
    CreateTecplotDAT outputs a Tecplot .dat file of the computed design velocity field data
    
    Created on 05 Jul 2011
    @author: pthompson
    '''  
    
    #print("Create TecPlot")
    
    #Prepare x-, y- and z-data
    
    x_points = []
    y_points = []
    z_points = []
        
    for point_number, point_coords in point_number_to_coords_unperturbed.items():
        
        x_points.append(point_coords[0])
        y_points.append(point_coords[1])
        z_points.append(point_coords[2])
        
    #print("facet_normals_perturbed ={}").format(len(facet_normals_unperturbed))
    #print ("facet_normals_"+str(parameter_number) + " is " + str(len(facet_normals_unperturbed)))
    #Open file to write to
    # Windows Path
    tecplot_output_file = open(str(local_path)+ "Perturbed_mesh_"+str(parameter_number)+".dat", 'w')
    # Ubuntu path
    #tecplot_output_file = open(str(directory_path) + "/" + "Results" + "/" + "Perturbed_mesh.dat", 'w')
    
    #Write file header material
    
    tecplot_output_file. write("TITLE    = \"Perturbed Mesh\"" + "\n")
    tecplot_output_file.write("VARIABLES = \"x\" \"y\" \"z\" ")
    # Include Facet normals ######
    tecplot_output_file.write("\"Normal_x\"")
    tecplot_output_file.write("\"Normal_y\"")
    tecplot_output_file.write("\"Normal_z\"")
    ##########
    tecplot_output_file.write("\n")
    tecplot_output_file.write("ZONE T=\"SURFACE\"" + "\n")
    tecplot_output_file.write(" NODES=" + str(len(x_points)) + ", ELEMENTS=" + str(len(facet_number_to_point_numbers_unperturbed)) + ", DATAPACKING=BLOCK, ZONETYPE=FETRIANGLE, VARLOCATION=([1-3]=NODAL, ")
    
    # Include facet normals ######
    tecplot_output_file.write("[4]=CELLCENTERED,")
    tecplot_output_file.write("[5]=CELLCENTERED, ")
    tecplot_output_file.write("[6]=CELLCENTERED, ")
    ####
    tecplot_output_file.write(")" + "\n")
    tecplot_output_file.write("\n")
    
    #Compute number of rows per variable
    number_of_rows = int(math.floor((len(point_number_to_coords_unperturbed))/5))
    remainder = int((len(point_number_to_coords_unperturbed)) - (number_of_rows * 5))
    
    number_of_element_rows = int(math.floor((len(facet_number_to_point_numbers_unperturbed))/5))
    element_remainder = int((len(facet_number_to_point_numbers_unperturbed)) - (number_of_element_rows * 5))
        
    
    #Write x point data
    x_coord = [0,0,0,0,0]
    
    for i in range(number_of_rows):
        x_coord[0] = point_number_to_coords_unperturbed[5 * i][0]
        x_coord[1] = point_number_to_coords_unperturbed[(5 * i) + 1][0]
        x_coord[2] = point_number_to_coords_unperturbed[(5 * i) + 2][0]
        x_coord[3] = point_number_to_coords_unperturbed[(5 * i) + 3][0]
        x_coord[4] = point_number_to_coords_unperturbed[(5 * i) + 4][0]
         
        tecplot_output_file.write(" " + "%.9E"%x_coord[0] + " " + "%.9E"%x_coord[1] + " " + "%.9E"%x_coord[2] + " " + "%.9E"%x_coord[3] + " " + "%.9E"%x_coord[4] + "\n")
         
    x_coord = x_coord[:remainder]
    
    for i in range(remainder):
        x_coord[i] = point_number_to_coords_unperturbed[(5 * number_of_rows) + i][0]
         
    if remainder == 1:
        tecplot_output_file.write(" " + "%.9E"%x_coord[0] + "\n")
    elif remainder == 2:
        tecplot_output_file.write(" " + "%.9E"%x_coord[0] + " " + "%.9E"%x_coord[1] + "\n")
    elif remainder == 3:
        tecplot_output_file.write(" " + "%.9E"%x_coord[0] + " " + "%.9E"%x_coord[1] + " " + "%.9E"%x_coord[2] +"\n")
    elif remainder ==4:
        tecplot_output_file.write(" " + "%.9E"%x_coord[0] + " " + "%.9E"%x_coord[1] + " " + "%.9E"%x_coord[2] + " " + "%.9E"%x_coord[3] +"\n")
        
    #Write y point data
    y_coord = [0,0,0,0,0]
    
    for i in range(number_of_rows):
        y_coord[0] = point_number_to_coords_unperturbed[5 * i][1]
        y_coord[1] = point_number_to_coords_unperturbed[(5 * i) + 1][1]
        y_coord[2] = point_number_to_coords_unperturbed[(5 * i) + 2][1]
        y_coord[3] = point_number_to_coords_unperturbed[(5 * i) + 3][1]
        y_coord[4] = point_number_to_coords_unperturbed[(5 * i) + 4][1]
         
        tecplot_output_file.write(" " + "%.9E"%y_coord[0] + " " + "%.9E"%y_coord[1] + " " + "%.9E"%y_coord[2] + " " + "%.9E"%y_coord[3] + " " + "%.9E"%y_coord[4] + "\n")
         
    y_coord = y_coord[:remainder]
    
    for i in range(remainder):
        y_coord[i] = point_number_to_coords_unperturbed[(5 * number_of_rows) + i][1]
         
    if remainder == 1:
        tecplot_output_file.write(" " + "%.9E"%y_coord[0] + "\n")
    elif remainder == 2:
        tecplot_output_file.write(" " + "%.9E"%y_coord[0] + " " + "%.9E"%y_coord[1] + "\n")
    elif remainder == 3:
        tecplot_output_file.write(" " + "%.9E"%y_coord[0] + " " + "%.9E"%y_coord[1] + " " + "%.9E"%y_coord[2] +"\n")
    elif remainder ==4:
        tecplot_output_file.write(" " + "%.9E"%y_coord[0] + " " + "%.9E"%y_coord[1] + " " + "%.9E"%y_coord[2] + " " + "%.9E"%y_coord[3] +"\n")
        

    #Write z point data
    z_coord = [0,0,0,0,0]
    
    for i in range(number_of_rows):
        z_coord[0] = point_number_to_coords_unperturbed[5 * i][2]
        z_coord[1] = point_number_to_coords_unperturbed[(5 * i) + 1][2]
        z_coord[2] = point_number_to_coords_unperturbed[(5 * i) + 2][2]
        z_coord[3] = point_number_to_coords_unperturbed[(5 * i) + 3][2]
        z_coord[4] = point_number_to_coords_unperturbed[(5 * i) + 4][2]
         
        tecplot_output_file.write(" " + "%.9E"%z_coord[0] + " " + "%.9E"%z_coord[1] + " " + "%.9E"%z_coord[2] + " " + "%.9E"%z_coord[3] + " " + "%.9E"%z_coord[4] + "\n")
         
    z_coord = z_coord[:remainder]
    
    for i in range(remainder):
        z_coord[i] = point_number_to_coords_unperturbed[(5 * number_of_rows) + i][2]
         
    if remainder == 1:
        tecplot_output_file.write(" " + "%.9E"%z_coord[0] + "\n")
    elif remainder == 2:
        tecplot_output_file.write(" " + "%.9E"%z_coord[0] + " " + "%.9E"%z_coord[1] + "\n")
    elif remainder == 3:
        tecplot_output_file.write(" " + "%.9E"%z_coord[0] + " " + "%.9E"%z_coord[1] + " " + "%.9E"%z_coord[2] +"\n")
    elif remainder ==4:
        tecplot_output_file.write(" " + "%.9E"%z_coord[0] + " " + "%.9E"%z_coord[1] + " " + "%.9E"%z_coord[2] + " " + "%.9E"%z_coord[3] +"\n")
    
 
    ##########################
    # Write Normal Data
    normal_x = [0,0,0,0,0]
    
    for i in range(number_of_element_rows):
        normal_x[0] = facet_normals_unperturbed[5 * i][0]
        normal_x[1] = facet_normals_unperturbed[(5 * i) + 1][0]
        normal_x[2] = facet_normals_unperturbed[(5 * i) + 2][0]
        normal_x[3] = facet_normals_unperturbed[(5 * i) + 3][0]
        normal_x[4] = facet_normals_unperturbed[(5 * i) + 4][0]
         
        tecplot_output_file.write(" " + "%.9E"%normal_x[0] + " " + "%.9E"%normal_x[1] + " " + "%.9E"%normal_x[2] + " " + "%.9E"%normal_x[3] + " " + "%.9E"%normal_x[4] + "\n")
         
    normal_x = normal_x[:element_remainder]
    
    for i in range(element_remainder):
        normal_x[i] = facet_normals_unperturbed[(5 * number_of_rows) + i][0]
         
    if element_remainder == 1:
        tecplot_output_file.write(" " + "%.9E"%normal_x[0] + "\n")
    elif element_remainder == 2:
        tecplot_output_file.write(" " + "%.9E"%normal_x[0] + " " + "%.9E"%normal_x[1] + "\n")
    elif element_remainder== 3:
        tecplot_output_file.write(" " + "%.9E"%normal_x[0] + " " + "%.9E"%normal_x[1] + " " + "%.9E"%normal_x[2] +"\n")
    elif element_remainder ==4:
        tecplot_output_file.write(" " + "%.9E"%normal_x[0] + " " + "%.9E"%normal_x[1] + " " + "%.9E"%normal_x[2] + " " + "%.9E"%normal_x[3] +"\n")
   
    normal_y = [0,0,0,0,0]
    
    for i in range(number_of_element_rows):
        normal_y[0] = facet_normals_unperturbed[5 * i][1]
        normal_y[1] = facet_normals_unperturbed[(5 * i) + 1][1]
        normal_y[2] = facet_normals_unperturbed[(5 * i) + 2][1]
        normal_y[3] = facet_normals_unperturbed[(5 * i) + 3][1]
        normal_y[4] = facet_normals_unperturbed[(5 * i) + 4][1]
         
        tecplot_output_file.write(" " + "%.9E"%normal_y[0] + " " + "%.9E"%normal_y[1] + " " + "%.9E"%normal_y[2] + " " + "%.9E"%normal_y[3] + " " + "%.9E"%normal_y[4] + "\n")
         
    normal_y = normal_y[:element_remainder]
    
    for i in range(element_remainder):
        normal_y[i] = facet_normals_unperturbed[(5 * number_of_rows) + i][1]
         
    if element_remainder == 1:
        tecplot_output_file.write(" " + "%.9E"%normal_y[0] + "\n")
    elif element_remainder == 2:
        tecplot_output_file.write(" " + "%.9E"%normal_y[0] + " " + "%.9E"%normal_y[1] + "\n")
    elif element_remainder== 3:
        tecplot_output_file.write(" " + "%.9E"%normal_y[0] + " " + "%.9E"%normal_y[1] + " " + "%.9E"%normal_y[2] +"\n")
    elif element_remainder ==4:
        tecplot_output_file.write(" " + "%.9E"%normal_y[0] + " " + "%.9E"%normal_y[1] + " " + "%.9E"%normal_y[2] + " " + "%.9E"%normal_y[3] +"\n")
        
    normal_z = [0,0,0,0,0]
    
    for i in range(number_of_element_rows):
        normal_z[0] = facet_normals_unperturbed[5 * i][2]
        normal_z[1] = facet_normals_unperturbed[(5 * i) + 1][2]
        normal_z[2] = facet_normals_unperturbed[(5 * i) + 2][2]
        normal_z[3] = facet_normals_unperturbed[(5 * i) + 3][2]
        normal_z[4] = facet_normals_unperturbed[(5 * i) + 4][2]
         
        tecplot_output_file.write(" " + "%.9E"%normal_z[0] + " " + "%.9E"%normal_z[1] + " " + "%.9E"%normal_z[2] + " " + "%.9E"%normal_z[3] + " " + "%.9E"%normal_z[4] + "\n")
         
    normal_z = normal_z[:element_remainder]
    
    for i in range(element_remainder):
        normal_z[i] = facet_normals_unperturbed[(5 * number_of_rows) + i][2]
         
    if element_remainder == 1:
        tecplot_output_file.write(" " + "%.9E"%normal_z[0] + "\n")
    elif element_remainder == 2:
        tecplot_output_file.write(" " + "%.9E"%normal_z[0] + " " + "%.9E"%normal_z[1] + "\n")
    elif element_remainder== 3:
        tecplot_output_file.write(" " + "%.9E"%normal_z[0] + " " + "%.9E"%normal_z[1] + " " + "%.9E"%normal_z[2] +"\n")
    elif element_remainder ==4:
        tecplot_output_file.write(" " + "%.9E"%normal_z[0] + " " + "%.9E"%normal_z[1] + " " + "%.9E"%normal_z[2] + " " + "%.9E"%normal_z[3] +"\n")
    
   
    ###############
    
    #Write connectivity data
    
    for i in range(len(facet_number_to_point_numbers_unperturbed)):  
        tecplot_output_file.write(" " + str(facet_number_to_point_numbers_unperturbed[i][0] + 1) + " " + str(facet_number_to_point_numbers_unperturbed[i][1] + 1) + " " + str(facet_number_to_point_numbers_unperturbed[i][2] + 1) + "\n")
        
     
    tecplot_output_file.close()