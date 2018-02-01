import math

#########################################################################################################

def CreateTecplotDAT(point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed, Vn_centroids, parameter_names, part_name, time_stamp, local_path, point_number_to_facet_numbers_unperturbed,facet_normals_unperturbed,point_number_ind):
    
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
        
    #Open file to write to
    # Windows Path
    tecplot_output_file = open(str(local_path) + "Tecplot_Results.tec", 'w')
    # Ubuntu path
    # tecplot_output_file = open(str(directory_path) + "/" + "Results" + "/" + str(part_name) + "_"+str(time_stamp) + ".dat", 'w')
    
    #Write file header material
    
    tecplot_output_file. write("TITLE    = \"Grid:" + str(part_name) + ", Pointdata: Vn\"" + "\n")
    tecplot_output_file.write("VARIABLES = \"x\" \"y\" \"z\" ")
    for parameter_number, parameter_name in parameter_names.items():
        tecplot_output_file.write("\"Vn_" + str(parameter_number) + "_" + str(parameter_name) + "\" ")
        # Include Facet normals and dp  ######
#    for parameter_number, parameter_name in parameter_names.items():
#        tecplot_output_file.write("\"Dp_" + str(parameter_number) + "_" + str(parameter_name) + "\" ")
#    
#    for parameter_number, parameter_name in parameter_names.items():
#        tecplot_output_file.write("\"Projected_id's_" + str(parameter_number) + "_" + str(parameter_name) + "\" ")
#   
#    for parameter_number, parameter_name in parameter_names.items():
#        tecplot_output_file.write("\"Nearest_Points_" + str(parameter_number) + "_" + str(parameter_name) + "\" ")
   
    tecplot_output_file.write("\"Normal_x\"")
    tecplot_output_file.write("\"Normal_y\"")
    tecplot_output_file.write("\"Normal_z\"")
   
   ##########
    tecplot_output_file.write("\n")
    tecplot_output_file.write("ZONE T=\"SURFACE\"" + "\n")
    tecplot_output_file.write(" NODES=" + str(len(x_points)) + ", ELEMENTS=" + str(len(facet_number_to_point_numbers_unperturbed)) + ", DATAPACKING=BLOCK, ZONETYPE=FEQUADRILATERAL, VARLOCATION=([1-3]=NODAL, ")
    for parameter_number_1 in list(parameter_names.keys()):
        tecplot_output_file.write("[" + str(parameter_number_1 + 4) + "]=CELLCENTERED, ")
    # Include disp
#    for parameter_number_2 in list(parameter_names.keys()):
#        num1=parameter_number_1+parameter_number_2+5
#        tecplot_output_file.write("[" + str(num1) + "]=CELLCENTERED, ")
#    # Include Perturbed Facet Id's
#    for parameter_number_2 in list(parameter_names.keys()):
#        num2=num1+parameter_number_2+1
#        tecplot_output_file.write("[" + str(num2) + "]=CELLCENTERED, ")
#    # Include Nearest Points
#    for parameter_number_2 in list(parameter_names.keys()):
#        num3=num2+parameter_number_2+1
#        tecplot_output_file.write("[" + str(num3) + "]=CELLCENTERED, ")
    # Include facet normals ######
    tecplot_output_file.write("[" + str(parameter_number_1 + 5) + "]=CELLCENTERED,")
    tecplot_output_file.write("[" + str(parameter_number_1 + 6) + "]=CELLCENTERED, ")
    tecplot_output_file.write("[" + str(parameter_number_1 + 7) + "]=CELLCENTERED, ")
   
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
        x_coord[0] = point_number_to_coords_unperturbed[(5 * i) + 0][0]
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
        y_coord[0] = point_number_to_coords_unperturbed[(5 * i) + 0][1]
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
            
    #Write Vn data
   
    for parameter_number,parameter_name in parameter_names.items():      
        current_perturbation_Vn_centroids = Vn_centroids[parameter_number]
                  
        Vn_data = [0,0,0,0,0]
        for i in range(number_of_element_rows):
            Vn_data[0] = current_perturbation_Vn_centroids[5 * i]
            Vn_data[1] = current_perturbation_Vn_centroids[(5 * i) + 1]
            Vn_data[2] = current_perturbation_Vn_centroids[(5 * i) + 2]
            Vn_data[3] = current_perturbation_Vn_centroids[(5 * i) + 3]
            Vn_data[4] = current_perturbation_Vn_centroids[(5 * i) + 4]
            
            tecplot_output_file.write(" " + "%.9E"%Vn_data[0] + " " + "%.9E"%Vn_data[1] + " " + "%.9E"%Vn_data[2] + " " + "%.9E"%Vn_data[3] + " " + "%.9E"%Vn_data[4] + "\n")
            
        Vn_data = Vn_data[:element_remainder]
        
        for i in range(element_remainder):
            Vn_data[i] = current_perturbation_Vn_centroids[(number_of_element_rows * 5) + i]
        if element_remainder == 1:
            tecplot_output_file.write(" " + "%.9E"%Vn_data[0] + "\n")
        elif element_remainder == 2:
            tecplot_output_file.write(" " + "%.9E"%Vn_data[0] + " " + "%.9E"%Vn_data[1] + "\n")
        elif element_remainder == 3:
            tecplot_output_file.write(" " + "%.9E"%Vn_data[0] + " " + "%.9E"%Vn_data[1] + " " + "%.9E"%Vn_data[2] +"\n")
        elif element_remainder ==4:
            tecplot_output_file.write(" " + "%.9E"%Vn_data[0] + " " + "%.9E"%Vn_data[1] + " " + "%.9E"%Vn_data[2] + " " + "%.9E"%Vn_data[3] +"\n")   
 
    ##########################
    # Write Dp Data
#    for parameter_number, parameter_name in parameter_names.items():
#        para_dp=dp[parameter_number]
#        disp = [0,0,0,0,0]
#        for i in range(number_of_element_rows):
#            disp[0] = para_dp[5 * i]
#            disp[1] = para_dp[(5 * i) + 1]
#            disp[2] = para_dp[(5 * i) + 2]
#            disp[3] = para_dp[(5 * i) + 3]
#            disp[4] = para_dp[(5 * i) + 4] 
#        
#            tecplot_output_file.write(" " + "%.9E"%disp[0] + " " + "%.9E"%disp[1] + " " + "%.9E"%disp[2] + " " + "%.9E"%disp[3] + " " + "%.9E"%disp[4] + "\n")
#        
#        disp= disp[:element_remainder]
#        
#        for i in range(element_remainder):
#            disp[i] = para_dp[(5 * number_of_element_rows) + i]
#        if element_remainder == 1:
#            tecplot_output_file.write(" " + "%.9E"%disp[0] + "\n")
#        elif element_remainder == 2:
#            tecplot_output_file.write(" " + "%.9E"%disp[0] + " " + "%.9E"%disp[1] + "\n")
#        elif element_remainder== 3:
#            tecplot_output_file.write(" " + "%.9E"%disp[0] + " " + "%.9E"%disp[1] + " " + "%.9E"%disp[2] +"\n")
#        elif element_remainder ==4:
#            tecplot_output_file.write(" " + "%.9E"%disp[0] + " " + "%.9E"%disp[1] + " " + "%.9E"%disp[2] + " " + "%.9E"%disp[3] +"\n")
#    ###############################      
#    # Write Perturbed Facet Id's
#    # Note due to differences in the counting starting point the value of the index has been increased by 1 
#    for parameter_number in parameter_names.keys():
#        para_id=projected_ids[parameter_number]
#        
#        ids = [0,0,0,0,0]
#        for i in range(number_of_element_rows):
#            ids[0] = para_id[5 * i]+1
#            ids[1] = para_id[(5 * i) + 1]+1
#            ids[2] = para_id[(5 * i) + 2]+1
#            ids[3] = para_id[(5 * i) + 3]+1
#            ids[4] = para_id[(5 * i) + 4]+1
#            
#            tecplot_output_file.write(" " + "%.9E"%ids[0] + " " + "%.9E"%ids[1] + " " + "%.9E"%ids[2] + " " + "%.9E"%ids[3] + " " + "%.9E"%ids[4] + "\n")    
#        
#        ids= ids[:element_remainder]
#            
#        for i in range(element_remainder):
#            ids[i] = para_id[(5 * number_of_element_rows) + i]+1
#        if element_remainder == 1:
#            tecplot_output_file.write(" " + "%.9E"%ids[0] + "\n")
#        elif element_remainder == 2:
#            tecplot_output_file.write(" " + "%.9E"%ids[0] + " " + "%.9E"%ids[1] + "\n")
#        elif element_remainder== 3:
#            tecplot_output_file.write(" " + "%.9E"%ids[0] + " " + "%.9E"%ids[1] + " " + "%.9E"%ids[2] +"\n")
#        elif element_remainder ==4:
#            tecplot_output_file.write(" " + "%.9E"%ids[0] + " " + "%.9E"%ids[1] + " " + "%.9E"%ids[2] + " " + "%.9E"%ids[3] +"\n")          
#   # Write Nearest Points
#
#    for parameter_number, parameter_name in parameter_names.items():
#        near_id=near_points[parameter_number]
#        ids = [0,0,0,0,0]
#        for i in range(number_of_element_rows):
#            ids[0] = near_id[5 * i]+1
#            ids[1] = near_id[(5 * i) + 1]+1
#            ids[2] = near_id[(5 * i) + 2]+1
#            ids[3] = near_id[(5 * i) + 3]+1
#            ids[4] = near_id[(5 * i) + 4]+1
#            tecplot_output_file.write(" " + "%.9E"%ids[0] + " " + "%.9E"%ids[1] + " " + "%.9E"%ids[2] + " " + "%.9E"%ids[3] + " " + "%.9E"%ids[4] + "\n")	    
#
#        ids= ids[:element_remainder]
#        
#        for i in range(element_remainder):
#            ids[i] = near_id[(5 * number_of_element_rows) + i]+1
#        if element_remainder == 1:
#            tecplot_output_file.write(" " + "%.9E"%ids[0] + "\n")
#        elif element_remainder == 2:
#            tecplot_output_file.write(" " + "%.9E"%ids[0] + " " + "%.9E"%ids[1] + "\n")
#        elif element_remainder== 3:
#            tecplot_output_file.write(" " + "%.9E"%ids[0] + " " + "%.9E"%ids[1] + " " + "%.9E"%ids[2] +"\n")
#        elif element_remainder ==4:
#            tecplot_output_file.write(" " + "%.9E"%ids[0] + " " + "%.9E"%ids[1] + " " + "%.9E"%ids[2] + " " + "%.9E"%ids[3] +"\n")        
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
        normal_x[i] = facet_normals_unperturbed[(5 * number_of_element_rows) + i][0]
             
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
        normal_y[i] = facet_normals_unperturbed[(5 * number_of_element_rows) + i][1]
         
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
        normal_z[i] = facet_normals_unperturbed[(5 * number_of_element_rows) + i][2]
         
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
        
        if  len(facet_number_to_point_numbers_unperturbed[i]) == 3:
            tecplot_output_file.write(" " + str(facet_number_to_point_numbers_unperturbed[i][0] + 1) + " " + str(facet_number_to_point_numbers_unperturbed[i][1] + 1) + " " + str(facet_number_to_point_numbers_unperturbed[i][2] + 1) + " " + str(facet_number_to_point_numbers_unperturbed[i][2] + 1) + "\n")
        elif len(facet_number_to_point_numbers_unperturbed[i]) == 4:
            tecplot_output_file.write(" " + str(facet_number_to_point_numbers_unperturbed[i][0] + 1) + " " + str(facet_number_to_point_numbers_unperturbed[i][1] + 1) + " " + str(facet_number_to_point_numbers_unperturbed[i][2]+1)  + " " + str(facet_number_to_point_numbers_unperturbed[i][3] + 1)+ "\n")
        
    tecplot_output_file.close()