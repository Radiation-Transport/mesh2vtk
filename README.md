![GitHub last commit](https://img.shields.io/github/last-commit/Radiation-Transport/iWW-GVR)
![GitHub issues](https://img.shields.io/github/issues/Radiation-Transport/iWW-GVR)
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/Radiation-Transport/iWW-GVR)
![GitHub top language](https://img.shields.io/github/languages/top/Radiation-Transport/iWW-GVR)
![](https://img.shields.io/badge/license-EU%20PL-blue)

# mesh2vtk
Mesh2Vtk converts the meshes produced by MCNP and D1S-UNED into a VTK format. The tool is a python based script able to read any mesh format in meshtally files produced by D1SUNED, MCNP5 or MCNP6. Mesh format includes usual MCNP column or matrix format and also specific D1SUNED format including cell or isotope contribution binning and source mesh importance format. Both Cartesian and cylindrical meshes can be read. The tool incorporates also simple functions to operate with meshes (add, scale, compare). The tool is used through a text based interactive menu, and it can be run under Windows or Linus systems. 


## How to use it

    >  python -m mesh2vtk.py


## What you need
- Python 3.7, https://www.python.org/download/releases
- numpy, https://www.scipy.org/scipylib/download.html
- vtkpython, https://www.vtk.org/download/

## License
Copyright 2019 F4E | European Joint Undertaking for ITER and the Development of Fusion Energy (‘Fusion for Energy’). Licensed under the EUPL, Version 1.1 or - as soon they will be approved by the European Commission - subsequent versions of the EUPL (the “Licence”). You may not use this work except in compliance with the Licence. You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl.html   
Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an “AS IS” basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the Licence permissions and limitations under the Licence.
