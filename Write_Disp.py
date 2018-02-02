
from GeometricFunctions import *
import numpy as np
from scipy.spatial.ckdtree import *


def Write_Disp(Vn_field_data):
	ipf1=open("/home/phewitt/Dropbox/Opt_Sync/Initial_Design.txt")
	Coords=np.loadtxt(ipf1)
	# Scale Coord values m->mm
	# Coords=Coords*1000
	
	# Assign Vnfield data to variables
	point_number_to_coords = Vn_field_data[0]
	facet_number_to_point_numbers = Vn_field_data[1]
	facet_normals = Vn_field_data[2]                                                         
	centroids_Vn = Vn_field_data[3]
	point_number_to_facet_numbers = Vn_field_data[4]
  
  # Get the Ids for the centroids of all facets used for Vn Computation
	facet_centroids = ComputeFacetCentroids(point_number_to_coords, facet_number_to_point_numbers)    
  
  # Split the facets according to their surface location via normals
	upper_surface_points=[]           
	lower_surface_points=[]
	for facet_number in facet_centroids.keys():
	    facet_centroid_xyz_coords = facet_centroids[facet_number]
	    if facet_normals[facet_number][2] >= 0.0:
	        upper_surface_points.append(facet_centroid_xyz_coords)                
	    elif facet_normals[facet_number][2] < 0.0:           
	        lower_surface_points.append(facet_centroid_xyz_coords)                

	# Create 2 KDtress to store facet coordinates     
	upper_tree = cKDTree(upper_surface_points)
	lower_tree = cKDTree(lower_surface_points)

  
  # Begin mapping elements to nodes

	centroid_coords_to_facet_number = dict([[facet_centroids[k],k] for k in facet_centroids.keys()])
	gid_to_closest_facet_number = {}
	gid_to_separation = {}
  
	# Loop over Coords
	for gid in range(len(Coords)):
		gid_coords=[0,0,0]
		gid_coords[0] = Coords[gid][0]
		gid_coords[1] = Coords[gid][1]
		gid_coords[2] = Coords[gid][2]
		normal=Coords[gid][3] 


	  # Use the Kd tress to find the closest mesh coord to each facet
		if normal >= 0.0:            
			nearest_point_data = upper_tree.query(gid_coords, 1)
			separation = nearest_point_data[0]
			closest_facet_centroid_coords = upper_tree.data[nearest_point_data[1]]   
		elif normal < 0.0:            
			nearest_point_data = lower_tree.query(gid_coords, 1)
			separation = nearest_point_data[0]
			closest_facet_centroid_coords = lower_tree.data[nearest_point_data[1]]
	  
	  # Store the closest facet's coordinates
		facet_centroid_coords = [0.0, 0.0, 0.0]
		facet_centroid_coords[0] = closest_facet_centroid_coords[0]
		facet_centroid_coords[1] = closest_facet_centroid_coords[1]
		facet_centroid_coords[2] = closest_facet_centroid_coords[2]

		print facet_centroid_coords
		facet_centroid_coords = tuple(facet_centroid_coords)
	  
	  # Get the Id of the closet facet
		closest_facet_number = centroid_coords_to_facet_number[facet_centroid_coords]            
		gid_to_closest_facet_number[gid] = closest_facet_number
		gid_to_separation[gid] = separation

	# Get the Vn Data for the mapped coordinates

	gid_to_vn = {}
	gid_to_disp_x = {}
	gid_to_disp_y = {}
	gid_to_disp_z = {}

	for gid in range(len(Coords)):

		# zero displacement at trailing and leading edges
		if Coords[gid][3]==0:
			gid_to_vn[gid] = 0.0
			gid_to_disp_x[gid] = 0.0
			gid_to_disp_y[gid] = 0.0
			gid_to_disp_z[gid] = 0.0
	 
		else:
			closest_facet_number = gid_to_closest_facet_number[gid]
			gid_to_vn[gid] = centroids_Vn[1][closest_facet_number]
			facet_normal = facet_normals[closest_facet_number]
			gid_to_disp_x[gid] = (gid_to_vn[gid] * facet_normal[0])
			gid_to_disp_y[gid] = (gid_to_vn[gid] * facet_normal[1])
			gid_to_disp_z[gid] = (gid_to_vn[gid] * facet_normal[2])
		     
	gid_list = []
	for gid in range(len(Coords)):      
		gid_list.append(gid)  
	gid_list.sort()
	        
	disp_x = []
	disp_y = []
	disp_z = []

	# for gid in gid_list:
	# 	disp_x.append(gid_to_disp_x[gid]/1000.0)
	# 	disp_y.append(gid_to_disp_y[gid]/1000.0)
	# 	disp_z.append(gid_to_disp_z[gid]/1000.0)
	
	for gid in gid_list:
		disp_x.append(gid_to_disp_x[gid])
		disp_y.append(gid_to_disp_y[gid])
		disp_z.append(gid_to_disp_z[gid])

	# Export displacements to file
	opf1=open("/home/phewitt/Dropbox/Opt_Sync/Disp.txt",'w')

	Disp_X=numpy.squeeze(numpy.asarray(disp_x))
	Disp_Y=numpy.squeeze(numpy.asarray(disp_y))
	Disp_Z=numpy.squeeze(numpy.asarray(disp_z))

	# print("Disp X = \t Disp Y = \t Disp Z \n".format(Disp_X[0],Disp_Y[0],Disp_X[0]))


	# Make the Header
	opf1.write("I.D.,\tDisp_x,\t\tDisp_y,\t\tDisp_z\n")
	
	for i in range(len(Coords)):
		opf1.write("{},\t{:.7E},\t{:.7E},\t{:.7E}\t".format(i,Disp_X[i],Disp_Y[i],Disp_Z[i])) # Write displacements
		if i<(len(Coords)-1):
			opf1.write("\n")
    
	return  

