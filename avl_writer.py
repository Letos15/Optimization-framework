'''
Created on 5 Mar 2018
This is the module used to write the file *.avl which produces the geometry in
AVL.
@author: Fabio C.
'''

import os

from ref_values import ref_values

def avl_writer(des_vec, Mach, out_dir, output_file):
    """
    This function reads the airfoil coordinates from the airfoil_file, 
    splits them into upper and lower edge and returns a single array 
    'airfoil' having four columns. Columns 1 and 3 contain the x coordinate 
    from 0 to 1, the 2nd and 4th columns the upper and lower coordinates 
    respectively. 
        
    Args:
    des_vec :             is the design vector.
    Mach number :         Mach number.
    out_dir :             output directory.
    output_file :         name of the file produced in output.
      
    Returns:
    
    """
    p = des_vec/1000
    S, c = ref_values(des_vec)
    
    path = os.path.join(out_dir, output_file)
    file_avl = open(path, 'w')
    
    file_avl.write('AeroVLM\n')
    file_avl.write('#Mach\n')
    file_avl.write(' {:3.2f}'.format(Mach) + '\n')   
    file_avl.write('#IYsym   IZsym   Zsym\n')   
    file_avl.write(' 0 0 0.0\n')
    file_avl.write('#Sref    Cref    Bref\n')
    file_avl.write(' {:5.2f} {:5.2f} {:5.2f}\n'.format(2*S, c, 2*p[6]))
    file_avl.write('#Xref    Yref    Zref\n')
    file_avl.write(' {:3.1f}'.format(0.25*p[0]) + ' ' + str(0.0)+ ' '  + str(0.0) +'\n\n')
    file_avl.write('SURFACE\n')
    file_avl.write('wing\n')
    file_avl.write('#Nchordwise  Cspace   Nspanwise   Sspace\n')
    file_avl.write(' 20 1.0 40 3.0\n')
    file_avl.write('YDUPLICATE\n')
    file_avl.write(' 0.0\n')
    file_avl.write('ANGLE\n')
    file_avl.write(' 0.0\n\n')
    file_avl.write('SECTION\n')
    file_avl.write('#Xle    Yle    Zle      Chord        Ainc  Nspanwise  Sspace\n')
    file_avl.write('0.00 0.00 0.00 ' + str(p[0]) + ' 0.0 0 0\n')
    file_avl.write('AFILE\n')
    file_avl.write('crm.txt\n')
#     file_avl.write('NACA\n')
#     file_avl.write(' 0012\n\n')
    file_avl.write('SECTION\n')
    file_avl.write('#Xle    Yle    Zle      Chord        Ainc  Nspanwise  Sspace\n')
    file_avl.write(str(p[3]) + ' ' + str(p[5]) + ' 0.00 ' + str(p[1]) + ' 0.0 0 0\n')
    file_avl.write('AFILE\n')
    file_avl.write('crm.txt\n')
    file_avl.write('SECTION\n')
    file_avl.write('#Xle    Yle    Zle      Chord        Ainc  Nspanwise  Sspace\n')
    file_avl.write(str(p[4]) + ' ' + str(p[6]) + ' 0.00 ' + str(p[2]) + ' 0.0 0 0\n')
    file_avl.write('AFILE\n')
    file_avl.write('crm.txt\n')

    file_avl.close    
    