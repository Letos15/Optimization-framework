'''
Created on 5 Mar 2018
This module is simply used to compute the wing area and the reference chord.
For the sake of simplicity the reference chord will be computed as the ratio 
between S and b.
@author: Fabio C.
'''

def ref_values(design_vec):
    p = design_vec
    S = (((p[0]+p[1])*p[5])+((p[1]+p[2])*(p[6]-p[5])))/2
    cm = S/p[6]
    return S/1e6, cm/1e3