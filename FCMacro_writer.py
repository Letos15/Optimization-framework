'''
Created on 14 Jan 2018
Last change on 28 Feb 2018

This module contains the FreeCAD_writer class.
This class is used to generate the macro for FreeCAD. It takes the aerofoil
points and other planform input and produces the corresponding macro which once
in FreeCAD will generate the external shape.
@author: Fabio C.
'''

import os

import numpy as np
from numpy import loadtxt



class FCMacro_writer:

    
    def __init__ (self, pars, airfoil_file):
        
        self.parameters = pars
        self.airfoil_file = airfoil_file
        self.macro = None
        
        """
        FreeCAD_writer is a class, whose purpose is the generation of the macro
        for FreeCAD. The macro is intended for the automatic generation of the
        wing 3D parametric model of the external surface and the crresponding 
        internal structure.
        """
        

    def read_airfoil(self):
        """
        This function reads the airfoil coordinates from the airfoil_file, 
        splits them into upper and lower edge and returns a single array 
        'airfoil' having four columns. Columns 1 and 3 contain the x coordinate 
        from 0 to 1, the 2nd and 4th columns the upper and lower coordinates 
        respectively. 
            
        Args:
            
        Returns:
        airfoil:              n_points x 4 array.
        """
        
        airfoil_path = os.path.join(os.getcwd(), 'Inputs', self.airfoil_file)
        airfoil = loadtxt(airfoil_path)
        length = len(airfoil)
        upper = airfoil[0:(length//2+1)]
        lower = airfoil[(length//2):length]
        '''
        The following line reverses the order of the elements in 'upper' and
        makes it consistent with 'lower'.
        '''
        upper = upper[::-1]
        airfoil = np.concatenate((upper, lower), axis=1)

        return airfoil
    
    def split_points(self):
        """
        This function take the upper and lower points from 'read_airfoil()' and
        splits each one in three parts: leading edge, central part (box) and 
        trailing edge.
            
        Args:
            
        Returns:
        le, box, te:        arrays of 4 columns. Parts of the airfoil array.
        """
        airfoil = self.read_airfoil()
        length = len(airfoil)
        le = airfoil[0:round(0.3*length), :]
        box = airfoil[round(0.3*length)-1:round(0.8*length), :]
        #te = airfoil[round(0.8*length)-1:length, :]
        return le, box
    
    
    def make_sections(self):
        """
        This function takes a number of evenly spaced sections along the span 
        and for each one computes the chord.It is desirable to have an odd 
        number of sections.
        Then the function estimates the area of each wing block.
             
        Args:
         
        Returns:
        chords:             chords values [mm] in a numpy array structure.
        areas:              area values [mm2] in a numpy array.
        """
        params = self.parameters
        sections = ([0, params[5]/2, params[5], (params[6]+params[5])/2, params[6]])
        num = len(sections)
        chords = np.zeros(num)
        xle = np.zeros(num)
        j = 0
        '''
        I define the four sweep angles: 2 for the LE and for the TE.
        '''
        Sweep_le1 = (params[3])/(params[5])
        Sweep_le2 = (params[4]-params[3])/(params[6]-params[5])
        Sweep_te1 = ((params[1]+params[3])-params[0])/(params[5])
        Sweep_te2 = ((params[2]+params[4])-(params[1]+params[3]))/(params[6]-params[5])
         
        for sec in sections:            
            if sec <= params[5]:
                xle[j] =  (Sweep_le1*sec)
                chords[j] = (params[0]+(Sweep_te1*sec))-(Sweep_le1*sec)
            else:
                xle[j] = params[3]+(Sweep_le2*(sec-params[5]))
                chords[j] = ((params[1]+params[3])+(Sweep_te2*(sec-params[5])))-(params[3]+(Sweep_le2*(sec-params[5])))
            j += 1
         
        '''
        Now I compute the value of the area between two adjacent sections.
        '''
        areas = np.zeros(num-1)
        for k in range(num-1):
            height = sections[k+1]-sections[k]
            areas[k] = ((chords[k+1]+chords[k])*height)/2
             
        return sections, xle, chords
     
    
    def block_import(self):
        """
        This function writes the first block for the FreeCAD macro. This block
        is intended to add all the required modules used in FreeCAD.
        First, it creates the 'geom.py' file then write the block.
        
        Args:
        
        Returns:
        
        """
        #Here, I write the importing sequence.
        self.macro.write("import FreeCAD\n")
        self.macro.write("from FreeCAD import Base\n")
        self.macro.write("import PartDesignGui\n")
        self.macro.write("import DraftTools\n")
        self.macro.write("import PartDesign\n")
        self.macro.write("import Part\n")
        self.macro.write("import Draft\n")
        self.macro.write("import PartDesignGui\n\n")
        self.macro.write("docName = 'MyDoc'\n")
        self.macro.write("FreeCAD.newDocument(docName)\n\n")


    def airfoil_points(self):
        '''
        I use a 'for' loop to create the block corresponding to the aerofoil
        points. The nested 'if' condition is used only to avoid to write the
        comma in the final line.
        '''
#       params = self.parameters()
#       le, box, te = self.split_points()
        box = self.split_points()[1]
        yle, xle, chords = self.make_sections()
        k = 0       
        self.macro.write("#Splines from points. Six splines per section.\n\n")
        for j in range(len(yle)):
            
#             self.macro.write("points = [\n")
#             for l in range(len(le)):
#                 if l < (len(le)-1):
#                     self.macro.write('    FreeCAD.Vector('+str(params[j]*le[l,0]) + ',' +   \
#                                         str(params[j]*le[l,1]) + ',' + str(0.0) +'),\n')
#                 else:
#                     self.macro.write('    FreeCAD.Vector('+str(params[j]*le[l,0]) + ',' +   \
#                                          str(params[j]*le[l,1]) + ',' + str(0.0) +')\n')
#             self.macro.write("]\n")
#             self.macro.write('spline = Draft.makeBSpline(points,closed=False,face=False,support=None)\n')
#             self.macro.write('Draft.autogroup(spline)\n')
#             if k == 0:      
#                 self.macro.write('FreeCAD.getDocument("MyDoc").getObject("BSpline").Placement = App.Placement(App.Vector(' + str(xle[j]) + ', 0,' + str(yle[j]) + '),App.Rotation(App.Vector(0,0,1),0))\n\n')
#             else:
#                 self.macro.write('FreeCAD.getDocument("MyDoc").getObject("BSpline' + str(k).zfill(3) + '").Placement = App.Placement(App.Vector(' + str(xle[j]) + ', 0,' + str(yle[j]) + '),App.Rotation(App.Vector(0,0,1),0))\n\n')
#             k +=1 
            
            '''
            With the following block I write the upper and lower splines only 
            corresponding to the box. So the 'for' loop on 'l' is for the upper 
            spline, while the 'for' loop on 'm' draws the lower spline.
            This block is inside the 'for' loop in 'j', which means it is 
            repeated for each section.
            '''
            
            self.macro.write("points = [\n")
            for l in range(len(box)):
                if l < (len(box)-1):
                    self.macro.write('    FreeCAD.Vector('+str(chords[j]*box[l,0]) + ',' + \
                                     str(0.0) + ',' + str(chords[j]*box[l,1]) +'),\n')
                else:
                    self.macro.write('    FreeCAD.Vector('+str(chords[j]*box[l,0]) + ',' + \
                                     str(0.0) + ',' + str(chords[j]*box[l,1]) +')\n')
            self.macro.write("]\n")
            self.macro.write('spline = Draft.makeBSpline(points,closed=False,face=False,support=None)\n')
            self.macro.write('Draft.autogroup(spline)\n')
            if k == 0:      
                self.macro.write('FreeCAD.getDocument("MyDoc").getObject("BSpline").Placement = App.Placement(App.Vector(' + str(xle[j]) + ',' + str(yle[j]) + ', 0),App.Rotation(App.Vector(0,0,1),0))\n\n')
            else:
                self.macro.write('FreeCAD.getDocument("MyDoc").getObject("BSpline' + str(k).zfill(3) + '").Placement = App.Placement(App.Vector(' + str(xle[j]) + ',' + str(yle[j]) + ', 0),App.Rotation(App.Vector(0,0,1),0))\n\n')
            k +=1 
    
            self.macro.write("points = [\n")    
            for m in range(len(box)):
                if m < (len(box)-1):
                    self.macro.write('    FreeCAD.Vector('+str(chords[j]*box[m,0]) + ',' + \
                                     str(0.0) + ',' + str(chords[j]*box[m,3]) +'),\n')
                else:
                    self.macro.write('    FreeCAD.Vector('+str(chords[j]*box[m,0]) + ',' + \
                                     str(0.0) + ',' + str(chords[j]*box[m,3]) +')\n')
            self.macro.write("]\n")
            self.macro.write('spline = Draft.makeBSpline(points,closed=False,face=False,support=None)\n')
            self.macro.write('Draft.autogroup(spline)\n')
            self.macro.write('FreeCAD.getDocument("MyDoc").getObject("BSpline' + str(k).zfill(3) + '").Placement = App.Placement(App.Vector(' + str(xle[j]) + ',' + str(yle[j]) + ', 0),App.Rotation(App.Vector(0,0,1),0))\n\n')
            k +=1
#             
#             self.macro.write("points = [\n")
#             for n in range(len(te)):
#                 if n < (len(te)-1):
#                     self.macro.write('    FreeCAD.Vector('+str(params[j]*te[n,0]) + ',' +   \
#                                         str(params[j]*te[n,1]) + ',' + str(0.0) +'),\n')
#                 else:
#                     self.macro.write('    FreeCAD.Vector('+str(params[j]*te[n,0]) + ',' +   \
#                                          str(params[j]*te[n,1]) + ',' + str(0.0) +')\n')
#             self.macro.write("]\n")
#             self.macro.write('spline = Draft.makeBSpline(points,closed=False,face=False,support=None)\n')
#             self.macro.write('Draft.autogroup(spline)\n')
#             self.macro.write('FreeCAD.getDocument("MyDoc").getObject("BSpline' + str(k).zfill(3) + '").Placement = App.Placement(App.Vector(' + str(xle[j]) + ', 0,' + str(yle[j]) + '),App.Rotation(App.Vector(0,0,1),0))\n\n')
#             k += 1
            
            ####################################################################
            
#             self.macro.write("points = [\n")
#             for l in range(len(le)):
#                 if l < (len(le)-1):
#                     self.macro.write('    FreeCAD.Vector('+str(params[j]*le[l,0]) + ',' +   \
#                                         str(params[j]*le[l,3]) + ',' + str(0.0) +'),\n')
#                 else:
#                     self.macro.write('    FreeCAD.Vector('+str(params[j]*le[l,0]) + ',' +   \
#                                          str(params[j]*le[l,3]) + ',' + str(0.0) +')\n')
#             self.macro.write("]\n")
#             self.macro.write('spline = Draft.makeBSpline(points,closed=False,face=False,support=None)\n')
#             self.macro.write('Draft.autogroup(spline)\n')
#             self.macro.write('FreeCAD.getDocument("MyDoc").getObject("BSpline' + str(k).zfill(3) + '").Placement = App.Placement(App.Vector(' + str(xle[j]) + ', 0,' + str(yle[j]) + '),App.Rotation(App.Vector(0,0,1),0))\n\n')
#             k +=1 
#             
#     
#             self.macro.write("points = [\n")    
#             for m in range(len(box)):
#                 if m < (len(box)-1):
#                     self.macro.write('    FreeCAD.Vector('+str(params[j]*box[m,0]) + ',' +   \
#                                         str(params[j]*box[m,3]) + ',' + str(0.0) +'),\n')
#                 else:
#                     self.macro.write('    FreeCAD.Vector('+str(params[j]*box[m,0]) + ',' +   \
#                                          str(params[j]*box[m,3]) + ',' + str(0.0) +')\n')
#             self.macro.write("]\n")
#             self.macro.write('spline = Draft.makeBSpline(points,closed=False,face=False,support=None)\n')
#             self.macro.write('Draft.autogroup(spline)\n')
#             self.macro.write('FreeCAD.getDocument("MyDoc").getObject("BSpline' + str(k).zfill(3) + '").Placement = App.Placement(App.Vector(' + str(xle[j]) + ', 0,' + str(yle[j]) + '),App.Rotation(App.Vector(0,0,1),0))\n\n')
#             k +=1
#             
#             self.macro.write("points = [\n")
#             for n in range(len(te)):
#                 if n < (len(te)-1):
#                     self.macro.write('    FreeCAD.Vector('+str(params[j]*te[n,0]) + ',' +   \
#                                         str(params[j]*te[n,3]) + ',' + str(0.0) +'),\n')
#                 else:
#                     self.macro.write('    FreeCAD.Vector('+str(params[j]*te[n,0]) + ',' +   \
#                                          str(params[j]*te[n,3]) + ',' + str(0.0) +')\n')
#             self.macro.write("]\n")
#             self.macro.write('spline = Draft.makeBSpline(points,closed=False,face=False,support=None)\n')
#             self.macro.write('Draft.autogroup(spline)\n')
#             self.macro.write('FreeCAD.getDocument("MyDoc").getObject("BSpline' + str(k).zfill(3) + '").Placement = App.Placement(App.Vector(' + str(xle[j]) + ', 0,' + str(yle[j]) + '),App.Rotation(App.Vector(0,0,1),0))\n\n')
#             k += 1

    def make_skin(self):
        sections = self.make_sections()[0]
        num = len(sections)
        for k in range(2*(num-1)):
            if k == 0:
                self.macro.write("FreeCAD.ActiveDocument.addObject('Part::RuledSurface', 'Ruled Surface')\n")
                self.macro.write("FreeCAD.ActiveDocument.ActiveObject.Curve1=(FreeCAD.ActiveDocument.BSpline,['Edge1'])\n")
                self.macro.write("FreeCAD.ActiveDocument.ActiveObject.Curve2=(FreeCAD.ActiveDocument.BSpline002,['Edge1'])\n")
                self.macro.write("App.ActiveDocument.recompute()\n\n")
            else:
                self.macro.write("FreeCAD.ActiveDocument.addObject('Part::RuledSurface', 'Ruled Surface')\n")
                self.macro.write("FreeCAD.ActiveDocument.ActiveObject.Curve1=(FreeCAD.ActiveDocument.BSpline" + str(k).zfill(3) + ",['Edge1'])\n")
                self.macro.write("FreeCAD.ActiveDocument.ActiveObject.Curve2=(FreeCAD.ActiveDocument.BSpline" + str(k+2).zfill(3) + ",['Edge1'])\n")
                self.macro.write("App.ActiveDocument.recompute()\n\n")       
               
    def make_spar(self):
        sections = self.make_sections()[0]
        num = len(sections)
        for k in range(num-1):
            if k == 0:
                self.macro.write("FreeCAD.ActiveDocument.addObject('Part::RuledSurface', 'Ruled Surface')\n")
                self.macro.write("FreeCAD.ActiveDocument.ActiveObject.Curve1=(FreeCAD.ActiveDocument.Ruled_Surface,['Edge4'])\n")
                self.macro.write("FreeCAD.ActiveDocument.ActiveObject.Curve2=(FreeCAD.ActiveDocument.Ruled_Surface001,['Edge4'])\n")
                self.macro.write("App.ActiveDocument.recompute()\n\n")
            else:
                self.macro.write("FreeCAD.ActiveDocument.addObject('Part::RuledSurface', 'Ruled Surface')\n")
                self.macro.write("FreeCAD.ActiveDocument.ActiveObject.Curve1=(FreeCAD.ActiveDocument.Ruled_Surface" + str(2*k).zfill(3) + ",['Edge4'])\n")
                self.macro.write("FreeCAD.ActiveDocument.ActiveObject.Curve2=(FreeCAD.ActiveDocument.Ruled_Surface" + str(2*k+1).zfill(3) + ",['Edge4'])\n")
                self.macro.write("App.ActiveDocument.recompute()\n\n")
            
            if k == 0:
                self.macro.write("FreeCAD.ActiveDocument.addObject('Part::RuledSurface', 'Ruled Surface')\n")
                self.macro.write("FreeCAD.ActiveDocument.ActiveObject.Curve1=(FreeCAD.ActiveDocument.Ruled_Surface,['Edge2'])\n")
                self.macro.write("FreeCAD.ActiveDocument.ActiveObject.Curve2=(FreeCAD.ActiveDocument.Ruled_Surface001,['Edge2'])\n")
                self.macro.write("App.ActiveDocument.recompute()\n\n")
            else:
                self.macro.write("FreeCAD.ActiveDocument.addObject('Part::RuledSurface', 'Ruled Surface')\n")
                self.macro.write("FreeCAD.ActiveDocument.ActiveObject.Curve1=(FreeCAD.ActiveDocument.Ruled_Surface" + str(2*k).zfill(3) + ",['Edge2'])\n")
                self.macro.write("FreeCAD.ActiveDocument.ActiveObject.Curve2=(FreeCAD.ActiveDocument.Ruled_Surface" + str(2*k+1).zfill(3) + ",['Edge2'])\n")
                self.macro.write("App.ActiveDocument.recompute()\n\n")  
        
    
    def export_iges(self, out_dir):
        self.macro.write("__objs__=[]\n")
        for k in range(16):
            if k == 0:
                self.macro.write("__objs__.append(FreeCAD.getDocument('MyDoc').getObject('Ruled_Surface'))\n")
            else:
                self.macro.write("__objs__.append(FreeCAD.getDocument('MyDoc').getObject('Ruled_Surface" + str(k).zfill(3) + "'))\n")
        
        local_path = os.path.join(out_dir,'box.iges')
        self.macro.write("Part.export(__objs__,r'" +local_path+"')\n")
        self.macro.write("del __objs__\n")
        self.macro.write("exit()\n")

    
    def write_macro(self, out_dir, output_file):
        """
        This function finally write the macro in a file. It uses all the other
        methods in the class to accomplish each operation.
            
        Args:
        output_file :     this is the name of the file containing the macro for
                          FreeCAD
        
        Returns:
        ndarray:          all the coordinates in a single numpy array structure.
        """
        path = os.path.join(out_dir, output_file)
        self.macro = open(path,'w')
        self.block_import()
        self.airfoil_points()
        self.make_skin()
        self.make_spar()
        self.export_iges(out_dir)
        
        self.macro.close()        