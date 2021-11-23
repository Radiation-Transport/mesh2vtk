import os
import re
from sys import path
import pytest 

dep_path='./../' # adjust this path to the location of the meshtal_mod.py module 
path.append(dep_path)  
from  meshtal_mod import *


@pytest.mark.parametrize("input_meshtal",['meshtal_cuv',
                                          'meshtal_cyl',
                                          'meshtal_d1s_CSimpactStudy'
                                          ])
def test_mesh_print_tally_info(input_meshtal):
  #To check if the meshtal can be read without any problem"
  filetype='MCNP'
  meshtally = Meshtal(input_meshtal,filetype)
  
  for i in meshtally.mesh.items():
    meshtally.mesh[i[0]].print_info()
  assert True

@pytest.mark.parametrize("input_meshtal",['meshtal_cuv',
                                          'meshtal_cyl',
                                          'meshtal_d1s_CSimpactStudy'
                                          ])
def test_mesh_print_info(input_meshtal):
  #To check if the meshtal can be read without any problem"
  filetype='MCNP'
  meshtally = Meshtal(input_meshtal,filetype)
  
  for i in meshtally.mesh.items():
    meshtally.print_info()
  assert True
  
  