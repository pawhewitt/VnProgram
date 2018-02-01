import win32com.client
import os
import math
from datetime import datetime

def IncrementParameters(parameter_type = "User", length_perturbation_size_mm = 1.0, angle_perturbation_size_deg = 1.0,dir_path="/Design_0/sens",local_dir="/Design_0/sens"):
    '''   
    IncrementParameters perturbs parameters of currently active Catia part document and outputs perturbed geometries as a series of STEP files.
    
    parameter_type set to "User" or "All". Default = "User"
    perturbation_size_length_mm set to desired finite-differencing step size for lengths in mm. Default = 1
    perturbation_size_angle_deg set to desired finite-differencing step size for angles in degrees. Default = 1
    
    Created on 29 Nov 2010
    @author: pthompson
    Modified by DAgarwal 19022016
    '''   

    catia_application =  win32com.client.dynamic.Dispatch('CATIA.Application')

    current_part_doc = catia_application.ActiveDocument
    current_part = current_part_doc.Part
    current_part_parameters = current_part.Parameters
    current_part_doc_path = current_part_doc.Path
    current_part_name = current_part.Name
        
    #Create directory within current active part directory to save exported models
    directory_path = dir_path+local_dir
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
        
    #Define function to export current part as STEP file
    def ExportCurrentPartAsSTP(name):
        '''
        Function to export currently active part as numbered VRML file if file does not already exist.
        n = name of file to export part as
        '''       
        if os.path.exists(directory_path + str(name) + ".stp"):
            os.remove(directory_path + str(name) + ".stp")
        current_part_doc.ExportData(directory_path +str(name) + ".stp", "stp")    
    
    def CloseCADCatia():
        """
        CloseCADCatia closes the currently active CATIA V5 document"

        @author: DAgarwal
        @created on: 23/03/2016
        """
        catia_application =  win32com.client.dynamic.Dispatch('CATIA.Application')
        current_part_doc = catia_application.ActiveDocument
        current_part_doc.Close()
        
    def OpenCADCatia(dir_path,Model_name):
        """
        OpenCADCatia opens a Catia V5 cad model with named Model_name at dir_path
        
        @author: DAgarwal
        @created on: 23/03/2016
        """
        catia_application =  win32com.client.dynamic.Dispatch('CATIA.Application')
        catia_application.Documents.Open(str(dir_path) +"\\"+str(Model_name))
    
    ExportCurrentPartAsSTP(0)
    
    #Initialise dictionary of parameter names
    parameter_names = {0:"Original Geometry"}
    
    #Set user_access_mode parameter to perturb all parameters or user parameters only 
    if parameter_type == "User":
        user_access_mode = 2
    elif parameter_type == "All":
        user_access_mode = 1
    
    #Loop through model parameter (all or user only depending on input) and perturb length and angle parameters according to perturbation inputs
    perturbation_number = 0
    PerturbationValue={0:0.0}
    parameter_values={0:0.0}

    for i in range(len(current_part_parameters)):
        current_parameter=current_part_parameters[i]
        #For user_access_mode = 1, all write-able parameters may be perturbed. For user_access_mode = 2 only user defined parameters can be perturbed.
        if current_parameter.UserAccessMode >= user_access_mode:            
            try:
                relation = current_parameter.OptionalRelation()
            except:
                relation = None              
            if relation is None:                
                #Obtain value of parameter. Returned as string with units attached.
                current_parameter_value_string = current_parameter.ValueAsString()
                current_parameter_value_string_list = list(str(current_parameter_value_string))
                #Length or angle parameter must be at least 3 characters (e.g. "1mm")          
                if len(current_parameter_value_string_list) >= 2:                    
                    #Check for parameters with units "mm" (lengths)                                              
                    if current_parameter_value_string_list[-2:] == ['m', 'm']:
                        original_current_parameter_value = float(current_parameter_value_string.replace("mm", ""))
                        try:
                            current_parameter.ValuateFromString(str(original_current_parameter_value/1000))                       
                            perturbation_number += 1
                            PerturbationValue[perturbation_number] = length_perturbation_size_mm  
                            #Add perturbed parameter name to dictionary or perturbed parameters
                            parameter_names[perturbation_number]=str(current_parameter.Name.split("\\")[1:])#[-1:][0])
                            parameter_values[perturbation_number]=original_current_parameter_value
                            perturbed_current_parameter_value = original_current_parameter_value + PerturbationValue[perturbation_number]
                            current_parameter.ValuateFromString(str(perturbed_current_parameter_value/1000))                        
                            successful_update = 0
                            update_failed = 0
                            x_org = 1.0
                            test = 0
                            while successful_update == 0:                                                     
                                #Update part to reflect parameter change
                                try:
                                    current_part.Update()                                 
                                    successful_update = 1                          
                                    update_failed = 0
                                    ExportCurrentPartAsSTP(perturbation_number)
                                    current_parameter.ValuateFromString(str(original_current_parameter_value/1000))
                                    current_part.Update() 
                                except:                                
                                    test += 1                               
                                    current_parameter.ValuateFromString(str(original_current_parameter_value/1000))
                                    try:
                                        current_part.Update()
                                        successful_update = 0
                                        update_failed = 1 
                                    except:                            
                                        CloseCADCatia()
                                        OpenCADCatia(current_part_doc_path,current_part_doc.Name)
                                        current_part_doc = catia_application.ActiveDocument
                                        current_part = current_part_doc.Part
                                        current_part_parameters = current_part.Parameters
                                        current_parameter=current_part_parameters[i]
                                        successful_update = 0
                                        update_failed = 1                           
                                if update_failed == 1:
                                    if test == 1:
                                        x = -x_org#/4.0
                                        PerturbationValue[perturbation_number] = length_perturbation_size_mm*x 
                                        #Add length perturbation to original length value
                                        perturbed_current_parameter_value = original_current_parameter_value + PerturbationValue[perturbation_number]
                                        #Update parameter in Catia to new perturbed value. ValuateFromString method takes units m for lengths(i.e. mm/1000)
                                        current_parameter.ValuateFromString(str(perturbed_current_parameter_value/1000))
                                    elif test > 1 and test < 6:
                                        x = x_org/2
                                        PerturbationValue[perturbation_number] = length_perturbation_size_mm*x 
                                        #Add length perturbation to original length value
                                        perturbed_current_parameter_value = original_current_parameter_value + PerturbationValue[perturbation_number]
                                        #Update parameter in Catia to new perturbed value. ValuateFromString method takes units m for lengths(i.e. mm/1000)
                                        current_parameter.ValuateFromString(str(perturbed_current_parameter_value/1000))
                                    elif test>6:
                                        CloseCADCatia()
                                        OpenCADCatia(current_part_doc_path,current_part_doc.Name)
                                        current_part_doc = catia_application.ActiveDocument
                                        current_part = current_part_doc.Part
                                        current_part_parameters = current_part.Parameters
                                        current_parameter=current_part_parameters[i]
                                        successful_update = 1                                        
                        except:
                            pass
                    #Check for parameters with units "deg" (angles)
                    elif  current_parameter_value_string_list[-3:] == ["d", "e", "g"]:
                        original_current_parameter_value = float(current_parameter_value_string.replace("deg", ""))
                        try:
                            current_parameter.ValuateFromString(str(math.radians(original_current_parameter_value)))
                            perturbation_number += 1
                            PerturbationValue[perturbation_number] = angle_perturbation_size_deg
                            #Add perturbed parameter name to dictionary or perturbed parameters
                            parameter_names[perturbation_number]=str(current_parameter.Name.split("\\")[1:])#[-1:][0])
                            parameter_values[perturbation_number]=original_current_parameter_value
                            #Add angle perturbation value to original angle parameter
                            perturbed_current_parameter_value = original_current_parameter_value + PerturbationValue[perturbation_number]
                            #Update parameter in Catia to new perturbed value. ValuateFromString method takes units radians for angles
                            current_parameter.ValuateFromString(str(math.radians(perturbed_current_parameter_value)))
                            
                            successful_update = 0
                            update_failed = 0
                            x_org = 1.0
                            test = 0                        
                            while successful_update == 0:                                                     
                                #Update part to reflect parameter change
                                try:
                                    current_part.Update()                                 
                                    successful_update = 1                          
                                    update_failed = 0
                                    #PerturbationValue[perturbation_number]=PerturbationValue[perturbation_number]
                                    ExportCurrentPartAsSTP(perturbation_number)
                                    current_parameter.ValuateFromString(str(math.radians(original_current_parameter_value)))
                                    current_part.Update() 
                                except:                                
                                    test += 1                               
                                    current_parameter.ValuateFromString(str(math.radians(original_current_parameter_value)))
                                    try:
                                        current_part.Update()
                                        successful_update = 0
                                        update_failed = 1
                                    except:                            
                                        CloseCADCatia()
                                        OpenCADCatia(current_part_doc_path,current_part_doc.Name)
                                        current_part_doc = catia_application.ActiveDocument
                                        current_part = current_part_doc.Part
                                        current_part_parameters = current_part.Parameters
                                        current_parameter=current_part_parameters[i]
                                        successful_update = 0
                                        update_failed = 1                           
                                if update_failed == 1:
                                    if test == 1:
                                        x = -x_org#/4.0
                                        PerturbationValue[perturbation_number] = angle_perturbation_size_deg*x 
                                        #Add length perturbation to original length value
                                        perturbed_current_parameter_value = original_current_parameter_value + PerturbationValue[perturbation_number]
                                        #Update parameter in Catia to new perturbed value. ValuateFromString method takes units m for lengths(i.e. mm/1000)
                                        current_parameter.ValuateFromString(str(math.radians(perturbed_current_parameter_value)))
                                    elif test > 1 and test < 6:
                                        x = x_org/2
                                        PerturbationValue[perturbation_number] = angle_perturbation_size_deg*x 
                                        #Add length perturbation to original length value
                                        perturbed_current_parameter_value = original_current_parameter_value + PerturbationValue[perturbation_number]
                                        #Update parameter in Catia to new perturbed value. ValuateFromString method takes units m for lengths(i.e. mm/1000)
                                        current_parameter.ValuateFromString(str(math.radians(perturbed_current_parameter_value))) 
                                    elif test>6:
                                        CloseCADCatia()
                                        OpenCADCatia(current_part_doc_path,current_part_doc.Name)
                                        current_part_doc = catia_application.ActiveDocument
                                        current_part = current_part_doc.Part
                                        current_part_parameters = current_part.Parameters
                                        current_parameter=current_part_parameters[i]
                                        successful_update = 1
                                        update_failed = 0
                        except:
                            pass
    current_part.Update()
    print (list(PerturbationValue.values()))

    ############################################################################
    output = (parameter_names, current_part_name, directory_path,list(PerturbationValue.values()),list(parameter_values.values()))
    return output    
    
if __name__ == "__main__":
    parameter_type = "All"
    length_perturbation_size_mm =0.5
    angle_perturbation_size_deg =0.5
    dir_path="F:/Volkswagen/VW Data Exchange/Optimization/NewParamOrigFeatureShell/Optimization_Stage2_Full1/"
    local_path="StepFiles/"
    output=IncrementParameters(parameter_type, length_perturbation_size_mm, angle_perturbation_size_deg,dir_path,local_path)

