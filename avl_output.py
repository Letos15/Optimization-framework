'''
Created on 6 Mar 2018
This is the module that reads the results from file and produces the two output
'pressure.txt' and 'efficiency.txt'.
@author: Fabio C.
'''

import os
import numpy as np
#import re
#from numpy import loadtxt

from isa_atmosphere import IsaAtmosphere


output_dir = os.path.join(os.getcwd(), 'OS')

def get_efficiency(results, output_dir):
    '''
    This function reads the results.txt file generated by AVL and gives back
    the efficiency and the pressure distribution over the wing.

    Parameters
    ----------
    results :      in the results.txt generated by AVL.
    out_dir:       is the output directory to save the files containing the 
                   pressure and the efficiency.

    Returns
    -------
    pressure.txt :    is the file containing the pressure values in a row.
    efficiency.txt :  is the file containing just the efficiency value.
    '''
    
    path_res = os.path.join(output_dir, results)
    path_eff = os.path.join(output_dir,'efficiency.txt')
    
    f = open(path_res)
    content = f.readlines()
    content = [x.split() for x in content]
     
    Eff = []
    file_path = os.path.join(output_dir, results)
    f = open(file_path)
    for i, line in enumerate(f):
        if line.startswith('  Forces referred to Ssurf, Cave about'):
            Eff = content[i+1]
            break
    CL = float(Eff[2])
    CD = float(Eff[5])       
    eff = open(path_eff,'w')
    eff.write('{:6.5f}  {:6.5f}\n'.format(CL/2, CD/2))
    eff.close()

    
#     path_res = os.path.join(results, output_dir)
#     path_eff = os.path.join(output_dir,'efficiency.txt')
#     eff = None
#     regexp = re.compile(r'     CLsurf  =   0.45000     CDsurf  =   .*?([0-9E.-]+)')
#     for line in list(open(path_res)):
#         #print(line)
#         match = regexp.match(line)
#         #print(match)
#         if match:
#             eff = open(path_eff,'w')
#             eff.write(match.group(1))
#             eff.close()
#             break   
#     return match.group(1)


def get_pressure(results, output_dir, Mach, z):
    """
    This function reads the data from a lattice-beta output file and
    puts them in a numpy array
    
    Args:
    filename(string):    the name of the file to read
    
    
    Returns:
    ndarray:             all the data in a single numpy array structure
    """
    
    path_res = os.path.join(output_dir, results)
    
    flight_conditions = IsaAtmosphere(z)
    rho = flight_conditions.compute_density()
    c = flight_conditions.compute_sound_speed()
    p_dyn = 0.5 * rho * (Mach*c)**2
    #b = np.sqrt(1-Mach**2)
    
    
    y = np.zeros((40))
    dy = np.zeros((40))
    A = np.zeros((40))
    ccl = np.zeros((40))
    file = open(path_res)
    lines = file.readlines()
    for j in range(40):
        riga = lines[j+20]
        l = riga.split('  ')
        y[j]= l[3]
        A[j]= l[5]
        ccl[j] = l[6]
    
    dy[0] = y[0]
    for k in range(39):
        dy[k+1] = y[k+1]-y[k]
    As = np.array([sum(A[0:10]), sum(A[11:20]), sum(A[21:30]), sum(A[31:40])])
    ccldy = ccl * dy
    Clocal = np.array([sum(ccldy[0:10]), sum(ccldy[11:20]), sum(ccldy[21:30]), sum(ccldy[31:40])])
    Cl = Clocal / (2*As)
    p = (Cl * p_dyn)/10e5
    p = np.around(p,4)
    #print(np.around(p,4))
    pres = open('OS\\pressures.txt', 'w')
    pres.write('{:5.4f} {:5.4f} {:5.4f} {:5.4f}'.format(p[0], p[1], p[2], p[3]))
    pres.close()


