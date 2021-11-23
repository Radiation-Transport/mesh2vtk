import os
import re
from sys import path
import pytest 

dep_path='./../' # adjust this path to the location of the meshtal_mod.py module 
path.append(dep_path)  
from  meshtal_mod import *

@pytest.mark.parametrize("input_meshtal",['meshtal_rect_VV',
                                          'meshtal_cyl',
                                          'meshtal_d1s_CSimpactStudy',
#                                          'meshtal_cuv',
                                          ])
def test_mesh_vtkwrite(input_meshtal):  
	filetype='MCNP'
	meshtally = Meshtal(input_meshtal,filetype)
	
	for i in meshtally.mesh.items():
		meshtally.mesh[i[0]].print_info()
		meshtally.readMesh([i[0]])

		meshname  = meshtally
		meshobj   = meshtally.mesh[i[0]]
		if meshobj.cart:
			name = 'test_.vtr'
		else:
			name = 'test_.vts'

		meshobj.writeVTK(name)
		assert True