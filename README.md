# Wing-optimisation
Wing planform aerodynamic optimisation
This optimization couples aerodynamics and topology optimization.
The following file are included:

1) main_opt.py : it is the main file used to run the optimizaion. At the bottom there is the minimize function
                 where it is possible to change the initial design vector.

2) avl_prova.py : this is the script used to produce the input file for AVL.

3) airfoil.txt : is the taxt file containing the airfoil coordinates. It is used by avl_prova.py .

4) avl_output.py : this script reads the results from AVL and extract: CL, CD and write the pressure.txt file for HM.

5) ref_area.py : produces the reference values (S, mean chord) to be used by avl_prova.py.

6) tcl_writer.py : this scripts writes the macro for HM, which in turns generates the files *.hm and .*fem.

7) read_mass.py : this file extract the value of the mass from the *.out file produced by OptiStruct.


USING THIS OPTIMIZATION FRAMEWORK:
##################################

In the main_opt.py the optimization can be adjusted changing some inputs in the minimize function.
Once the optimization is started, all the temporary files are stored in a folder called OS, which is 
refreshed at each function evaluation.

OptiStruct (FreeCAD as a consequence) is not called at each iteration but every two iterations.
Precisely, it is called at the first iteration and at all the even itertions. The mass value is then
updated only every two iterations.
