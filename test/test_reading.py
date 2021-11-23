import os
import re
from sys import path
import pytest 

dep_path='./../' # adjust this path to the location of the meshtal_mod.py module 
path.append(dep_path)  
from  meshtal_mod import *


@pytest.mark.parametrize("input_meshtal",['meshtal_cuv',
                                          'meshtal_cyl',
                                          'meshtal_d1s_CSimpactStudy',
										  'meshtal_d1s_IVVS_FDR',
										  'meshtal_rect_VV'])
def test_reading(input_meshtal):
  #To check if the meshtal can be read without any problem"
  filetype='MCNP'
  Meshtal(input_meshtal,filetype)
  
  assert True