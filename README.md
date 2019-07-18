# mesh2vtk
Mesh2Vtk converts the meshes produced by MCNP and D1S-UNED into a VTK format.
The tool is a python based script able to read any mesh format 
in meshtally files produced by D1SUNED, MCNP5 or MCNP6. 
Mesh format includes usual MCNP column or matrix format and also specific D1SUNED format 
including cell or isotope contribution binning and source mesh importance format. 
Both Cartesian and cylindrical meshes can be read. The tool incorporates also simple 
functions to operate with meshes (add, scale, compare).
The tool is used through a text based interactive menu, and it can be run under 
Windows or Linus systems. 

Detailed information and documentation is available on request contacting marco.fabbri@f4e.europa.eu

## How to use it
> python -m mesh2vtk.py

## What you need
- Python 2.7
- numpy,https://www.scipy.org/scipylib/download.html
- vtkpython, https://www.vtk.org/download/