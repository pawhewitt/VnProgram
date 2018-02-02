

import numpy as np


def Print_Disp():
	ipf1=open("/home/phewitt/Dropbox/Opt_Sync/Initial_Design.txt")
	Coords=np.loadtxt(ipf1)
	# Scale Coord values m->mm
	Coords=Coords*1000
	return  

if __name__=="__main__":
	Print_Disp()