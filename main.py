'''
Created on 15 Jan 2018
Last change on 07 Mar 2018

This module, called 'main.py', is the top module for the optimisation.
It calls the other modules and drives the optimisation loop.
Scrolling down through this file it is possible to change all the inputs for the
optimisation. Each stage is fully explained in the comments.

@author: Fabio C.

IMPORTANT NOTE: The paths to the software (FreeCAD, OptiStruct) called from this
                module MUST be defined in the batch file 'optimisation.bat' used
                to launch this module. For this reason they are omitted here.
                This choice derives by the need to define/modify the path easily
                on different machines.
                Alternatively, it is possible to give the full path where the 
                software are called, in the following lines.
'''

import os
import subprocess
from subprocess import PIPE, STDOUT
from numpy import loadtxt
import shutil


from avl_writer import avl_writer
from FCMacro_writer import FCMacro_writer
# from tcl_writer import tcl_writer
# from avl_output import get_efficiency, get_pressure
from tcl_writer_p import tcl_writer
from avl_output_p import get_efficiency, get_pressure
from read_mass import read_mass
 
'''
This module 'main.py' is the top module for the optimisation loop and will be 
launched from a prompt that at least will have the directory to Python.
'''
os.environ['RADFLEX_PATH'] = r'C:\Program Files\Altair\14.0\hwsolvers\common\bin\win64'
avl_exe = r'C:\Users\NG6A38A\Downloads\AeroSuite\AVL\avl.exe'
freecad_exe = r'C:\Users\NG6A38A\Downloads\FreeCAD_0.17.12940_x64_dev_win\bin\FreeCAD.exe'
hypermesh_exe = r'C:\Program Files\Altair\14.0\hm\bin\win64\hmbatch.exe'
#hypermesh_exe = r'C:\Program Files\Altair\14.0\hm\bin\win64\hmopengl.exe'
optistruct_exe = r'C:\Program Files\Altair\14.0\hwsolvers\optistruct\bin\win64\optistruct_14.0_win64.exe'

'''
Defining the output directory where all the output files will be saved.
This directory is the current working directory plus a new folder (here called 
'OS').  
'''

'''
In the following lines I assign the working directory in the folder 'OS'.
Then I delete any pre-existent folder with the same name and I create it again
to store the new files. 
'''
output_dir = os.path.join(os.getcwd(), 'OS')
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
      
os.makedirs(output_dir)




'''
This function reads the design vector from 'desvec.txt'. 
'''
def read_desvec(desvec_file):
    """
    This function reads the design vectors from the desvec_file.txt and returns
    them into a numpy array format.
           
    Args:
    desvec_file:        is the name of the file where the design vector is.
                    
    Returns:
    vector:             an array of 7 numbers.
    """
     
    file_path = os.path.join(os.getcwd(), 'Inputs', desvec_file)
    des_vec = loadtxt(file_path)
    return des_vec
 
 
    
'''
Passing the design vector from the read_desvec function.
SET HERE THE NAME OF THE FILE CONTAINING THE DESING VECTOR.
________________________________________________________________________________
'''
desvec = read_desvec('desvec.txt')


'''
AERODYNAMIC ANALYSIS
Call here the function to do the aerodynamic analysis.
________________________________________________________________________________
'''

'''
First the file *.avl containing the geometry is generated.
'''
Mach_number = 0.85
avl_writer(desvec, Mach_number, output_dir, 'wing.avl')

'''
Then the file is read by avl.exe and the analysis completed.
'''
subP = subprocess.Popen([avl_exe], stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=output_dir)
#subP.communicate(input=b'load wing.avl\n oper \n a c 0.45\n x\n fs results.txt')
subP.communicate(input=b'load wing.avl\n oper \n a c 0.5\n x\n fe results.txt')



'''
The results are post-processed and two new text files are produced:
efficiency.txt and pressures.txt .
'''
get_efficiency('results.txt', output_dir)

'''
z is the flight heigth.
'''
z = 10000
get_pressure('results.txt', output_dir, Mach_number, z)


'''
GEOMETRY FOR THE IGES FILE.
Passing the input to the FCMacro_writer class and writing the macro for FreeCAD.
SET HERE THE NAME OF THE FILE CONTAINIG THE AIRFOIL COORDINATES.
________________________________________________________________________________
'''
wing = FCMacro_writer(desvec, 'airfoil.txt')
file = wing.write_macro(output_dir, 'box.FCmacro')

'''
Executing FreeCAD to generate the box.iges file.
'''
subprocess.run([freecad_exe, 'box.FCmacro'], cwd=output_dir)


'''
FE ANALYSIS: PRE-PROCESSING IN HYPERMESH AND OPTIMISATION IN OPTISTRUCT.
Execute tcl_macro.py to generate the hmbox.tcl macro for HyperMesh.
SET HERE THE NAME OF THE FILE CONTAINIG THE PRESSURE VALUES.
________________________________________________________________________________
'''
tcl_file_path = os.path.join(output_dir,'hmbox.tcl')
#tcl_writer(desvec, 0.3, 'pressures.txt', tcl_file_path, output_dir, compliance=True)
tcl_writer(desvec, 0.3, tcl_file_path, output_dir, compliance=True)


'''
The following command if I use hypermesh.exe
'''
subprocess.run([hypermesh_exe,'-b', '-tcl', 'hmbox.tcl'], cwd=output_dir)
'''
The following command if I use hmopengl.exe
'''
#subprocess.run([hypermesh_exe, '-noconsole', '-tcl', 'prova.tcl'], cwd=output_dir)

exit()

subprocess.run([optistruct_exe, 'box.fem', '-analysis'], cwd=output_dir)
#subprocess.run([optistruct_exe, 'box.fem', '-license=OPT'], cwd=output_dir)


'''
Execute read_mass.py to generate the mass.txt file containing the mass value.
'''
file_path = os.path.join(output_dir, 'box.out')
read_mass(file_path, output_dir)  