import numpy

def CreateAbaqusODB(point_number_to_coords_unperturbed, facet_number_to_point_numbers_unperturbed, facet_normals_unperturbed, Vn_centroids, parameter_names, file_name, time_stamp, local_path):
    
    '''   
    CreateAbaqusODB outputs a Python script file which can be run in Abaqus to generate an ODB of the computed design velocity field data
    
    Created on 29 Nov 2010
    @author: pthompson
    '''   

    odb_file = open(str(local_path) + "Abaqus_Results_File.py", 'w')
    
    #Write header material
    odb_file.write("from odbAccess import *" + "\n")
    odb_file.write("from odbMaterial import *" + "\n")
    odb_file.write("from odbSection import *" + "\n")
    odb_file.write("from abaqusConstants import *" + "\n")
    odb_file.write("" + "\n")
    odb_file.write("def createODB():" + "\n")
    odb_file.write("  odb = Odb(name='DesignVelocity" + str(file_name) + " " + str(time_stamp) + "'," + "\n")
    odb_file.write("      analysisTitle='Design Velocity Visualisation'," + "\n")
    odb_file.write("      description='ODB file displaying computed Design Velocity values'," + "\n")
    odb_file.write("      path='odbDesignVelocity" + str(file_name) + " " + str(time_stamp) + ".odb')" + "\n")
    
    #Write point coordinates header
    odb_file.write("  part1 = odb.Part(name='part-1', embeddedSpace=THREE_D," + "\n")
    odb_file.write("      type=DEFORMABLE_BODY)" + "\n")
    odb_file.write("  nodeData = (" + "\n")
    
    
    #Write point coordinate data
    for point_number, point_coords in point_number_to_coords_unperturbed.items():
        
        odb_file.write("      (" + str(point_number) + "," + str(point_coords[0]) + "," + str(point_coords[1]) + "," + str(point_coords[2]) + "), # Point " + str(point_number) + "\n")
    
    #Write facets header   
    odb_file.write("      )" + "\n")
    odb_file.write("  part1.addNodes(nodeData=nodeData," + "\n")
    odb_file.write("      nodeSetName='nset-1')" + "\n")
    odb_file.write("  elementData = (" + "\n")
    
    #Write facet data
    for facet_number, facet_points in facet_number_to_point_numbers_unperturbed.items():
        
        odb_file.write("      (" + str(facet_number) + "," + str(facet_points[0]) + "," + str(facet_points[1]) + "," + str(facet_points[2]) + "), #Facet " + str(facet_number) + "\n")
    
        
    odb_file.write("      )" + "\n")
    odb_file.write("  part1.addElements(elementData=elementData, type='S3'," + "\n")
    odb_file.write("      elementSetName='eset-1')" + "\n")
    odb_file.write("  instance1 = odb.rootAssembly.Instance(name='part-1-1'," + "\n")
    odb_file.write("      object=part1)" + "\n")
    odb_file.write("  step1 = odb.Step(name='step-1'," + "\n")
    odb_file.write("      description='analysis step'," + "\n")
    odb_file.write("      domain=TIME, timePeriod=1.0)" + "\n")
    odb_file.write("  analysisTime=0.1" + "\n")
     
    # for Base Parameter i.e. 0
    
    for parameter_number, parameter_name in list(parameter_names.items()):
        
        current_perturbation_Vn_centroids = Vn_centroids[parameter_number]       
        
        if parameter_number == 0:
            odb_file.write("  frame" + str(parameter_number) + " = step1.Frame(incrementNumber=" + str(parameter_number) + "," + "\n")
            odb_file.write("      frameValue=analysisTime," + "\n")
            odb_file.write("      description=\\" + "\n")
            odb_file.write("          'Original model (No perturbation)')" + "\n")
            
        else:
            odb_file.write("  frame" + str(parameter_number) + " = step1.Frame(incrementNumber=" + str(parameter_number) + "," + "\n")
            odb_file.write("      frameValue=analysisTime," + "\n")
            odb_file.write("      description=\\" + "\n")
            odb_file.write("          'Vn for parameter " + str(parameter_name) + "')" + "\n")
          
        odb_file.write("  uField = frame" + str(parameter_number) + ".FieldOutput(name='Vn'," + "\n")
        odb_file.write("      description='Design Velocities', type=VECTOR, validInvariants = (MAGNITUDE,))" + "\n")
        
        if parameter_number == 0:
            odb_file.write("  elementLabelData = (" + "\n")
            
            for facet_number in facet_number_to_point_numbers_unperturbed.keys():
                
                if facet_number == (len(facet_number_to_point_numbers_unperturbed)-1):
                    odb_file.write("      " + str(facet_number) + ")" + "\n")
                else:
                    odb_file.write("      " + str(facet_number) + "," + "\n")
        
        odb_file.write("  dispData = (" + "\n")
        
        if parameter_number == 0:
            facet_number=0
            for facet_centroid_Vn in current_perturbation_Vn_centroids:                        
                current_facet_normal = numpy.array(facet_normals_unperturbed[facet_number])
                current_facet_centroid_Vn_vector = facet_centroid_Vn * current_facet_normal
            
                if facet_number == (len(facet_number_to_point_numbers_unperturbed)-1):
                    odb_file.write("      (" + str(current_facet_centroid_Vn_vector[0]) + "," + str(current_facet_centroid_Vn_vector[1]) + "," + str(current_facet_centroid_Vn_vector[2]) + ") #Vn vector at centroid " + str(facet_number) + "\n")
                else:
                    odb_file.write("      (" + str(current_facet_centroid_Vn_vector[0]) + "," + str(current_facet_centroid_Vn_vector[1]) + "," + str(current_facet_centroid_Vn_vector[2]) + "), #Vn vector at centroid " + str(facet_number) + "\n")
                facet_number+=1
        else:    
            for facet_number, facet_centroid_Vn in current_perturbation_Vn_centroids.items():
                current_facet_normal = numpy.array(facet_normals_unperturbed[facet_number])
                current_facet_centroid_Vn_vector = facet_centroid_Vn * current_facet_normal
            
                if facet_number == (len(facet_number_to_point_numbers_unperturbed)-1):
                    odb_file.write("      (" + str(current_facet_centroid_Vn_vector[0]) + "," + str(current_facet_centroid_Vn_vector[1]) + "," + str(current_facet_centroid_Vn_vector[2]) + ") #Vn vector at centroid " + str(facet_number) + "\n")
                else:
                    odb_file.write("      (" + str(current_facet_centroid_Vn_vector[0]) + "," + str(current_facet_centroid_Vn_vector[1]) + "," + str(current_facet_centroid_Vn_vector[2]) + "), #Vn vector at centroid " + str(facet_number) + "\n")
        
        odb_file.write("      )" + "\n")
        odb_file.write("  uField.addData(position=CENTROID, instance=instance1," + "\n")
        odb_file.write("      labels=elementLabelData," + "\n")
        odb_file.write("      data=dispData)" + "\n")
    
    
    #Write closing material   
    odb_file.write("  odb.save()" + "\n")
    odb_file.write("  odb.close()" + "\n")
    odb_file.write("if __name__ == " + "\"" + "__main__" + "\"" + ":" + "\n")
    odb_file.write("  createODB()" + "\n")
    
    return
  

#if __name__ == "__main__":