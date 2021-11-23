import os
import re
from sys import path
import pytest 
import pyvista as pv

dep_path='./../' # adjust this path to the location of the meshtal_mod.py module 
path.append(dep_path)  
from  meshtal_mod import *

# ************** STATUS OF TESTING *****************
# Mesh scale               (scale)      ---> DONE
# Mesh sum                 (sum)        ---> DONE
# Mesh difference          (diff)       ---> DONE
# Energy bin sum           (binsum)     ---> PENDING
# Check identical mesh     (identical)  ---> DONE
# Change correlation       (corr)       ---> DONE
# CuV testing                           ---> PENDING

# 'meshtal_CUBE_SQUARE'
#  ^
#  |   9  16
#  |   1  4
#  Y
#     X --->

# 'meshtal_CUBE_ONES'
#  ^
#  |   1  1
#  |   1  1
#  Y
#     X --->
 
@pytest.mark.parametrize("input_meshtal",['meshtal_CUBE_SQUARE',
                                          'meshtal_CUBE_ONES'])
def test_reading(input_meshtal):
  #To check if the meshtal can be read without any problem"
  filetype='MCNP'
  Meshtal(input_meshtal,filetype)
  
  assert True
  
  
@pytest.mark.parametrize("input_meshtal",['meshtal_CUBE_SQUARE'])
def test_mesh_VTKwrite(input_meshtal):  
	filetype='MCNP'
	meshtally = Meshtal(input_meshtal,filetype)
	
	meshtally.mesh[124].print_info()
	meshtally.readMesh([124])

	meshname  = meshtally
	meshobj   = meshtally.mesh[124]

	name = 'test_VTK_CUBE_SQUARE.vtr'
	
	meshobj.writeVTK(name)
	assert True
	
@pytest.mark.parametrize("filename",['test_VTK_CUBE_SQUARE.vtr'])
def test_mesh_VTKcheck(filename):  

	mesh = pv.read(filename)
	
	assert mesh['Value - Total'][0]	== 1
	assert mesh['Value - Total'][1]	== 9
	assert mesh['Value - Total'][2]	== 4
	assert mesh['Value - Total'][3]	== 16
	
@pytest.mark.parametrize("sfactor",[1,2,3,10,20])
def test_mesh_scale(sfactor):  

	input_meshtal = 'meshtal_CUBE_SQUARE'
	filetype='MCNP'
	
	meshtally = Meshtal(input_meshtal,filetype)
	meshtally.readMesh([124])
	meshobj   = meshtally.mesh[124]
	
	smesh = scalemesh(meshobj,sfactor)

	assert smesh.dat[0][0][0][0]	== 1 * sfactor
	assert smesh.dat[0][0][0][1]	== 9 * sfactor
	assert smesh.dat[0][0][1][0]	== 4 * sfactor
	assert smesh.dat[0][0][1][1]	== 16* sfactor	
	
	
def test_mesh_sum(): 
	input_meshtal = 'meshtal_CUBE_SQUARE'

	filetype='MCNP'
	meshtally = Meshtal(input_meshtal,filetype)

	meshtally.readMesh([124])
	meshobj   = meshtally.mesh[124]

	smesh = addmesh(meshobj,meshobj,f1=1.,f2=1.,corr=False)
	
	assert smesh.dat[0][0][0][0]	== 1 * 2
	assert smesh.dat[0][0][0][1]	== 9 * 2
	assert smesh.dat[0][0][1][0]	== 4 * 2
	assert smesh.dat[0][0][1][1]	== 16* 2

def test_mesh_corr(): 
	input_meshtal = 'meshtal_CUBE_ONES'

	filetype='MCNP'
	meshtally = Meshtal(input_meshtal,filetype)

	meshtally.readMesh([124])
	meshobj   = meshtally.mesh[124]
	
	smesh = addmesh(meshobj,meshobj,f1=1.,f2=1.,corr=True)
	
	assert smesh.err[0][0][0][0]	== 1
	assert smesh.err[0][0][0][1]	== 1
	assert smesh.err[0][0][1][0]	== 1
	assert smesh.err[0][0][1][1]	== 1	
	
	smesh = addmesh(meshobj,meshobj,f1=1.,f2=1.,corr=False)
	
	assert smesh.err[0][0][0][0]	== ((1+1)**0.5)/2
	assert smesh.err[0][0][0][1]	== ((1+1)**0.5)/2
	assert smesh.err[0][0][1][0]	== ((1+1)**0.5)/2
	assert smesh.err[0][0][1][1]	== ((1+1)**0.5)/2

def test_mesh_diff(): 
	input_meshtal = 'meshtal_CUBE_SQUARE'

	filetype='MCNP'
	meshtally = Meshtal(input_meshtal,filetype)

	meshtally.readMesh([124])
	meshobj   = meshtally.mesh[124]

	smesh = diffmesh(meshobj,meshobj)
	
	assert smesh.dat[0][0][0][0]	== 0
	assert smesh.dat[0][0][0][1]	== 0
	assert smesh.dat[0][0][1][0]	== 0
	assert smesh.dat[0][0][1][1]	== 0
	
	
def test_mesh_identical(): 
	input_meshtal = 'meshtal_CUBE_SQUARE'

	filetype='MCNP'
	meshtally = Meshtal(input_meshtal,filetype)

	meshtally.readMesh([124])
	meshobj   = meshtally.mesh[124]

	part,mesh,mtype = identical_mesh(meshobj,meshobj)
	
	assert part	 == True
	assert mesh	 == True
	assert mtype == True
	
	
	