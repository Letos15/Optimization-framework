'''
Created on 12 Feb 2018
This module writes the box.tcl file imported in HyperMesh. It mainly opens a file
and writes in it the whole macro in tcl. The only input are the pressure values 
from AVL (missing at the moment. I will use a txt file to test the code) and the
root chord dimension (from par.txt) to adjust the mesh size according to the
model size.
I write the module as a function, not a class.
@author: Fabio C.
'''
import os
from numpy import loadtxt


'''
Setting directory.
'''

def tcl_writer(desvec, vol_frac, file_loads, output_filename, out_dir, compliance=False):
    '''
    This function writes the tcl macro for HM in a file, whose name is given as
    input. It actually only changes the mesh size and the pressure values, while
    all the rest of the script remained unchanged.
    
    Args:
    desvec:             Is the design vector.
    vf:                 Volume fraction used during topology optimisation.
    file_loads:         Is the file containing the aerodynamic loads.
    output_filename:    Is the file containing the tcl macro for HyperMesh.
    '''
            
    volfrac = vol_frac
    params = desvec
    size = int(params[2]/30)
    '''
    Get the path to the aerodynamic loads file.
    '''
    loads_path = os.path.join(out_dir, file_loads)
    loads = loadtxt(loads_path)
    
    
    tclfile = open(output_filename,'w')
    
    #Writing the initial block.
    tclfile.write("# Launching block.\n")
    s_launch = '''
*begin "version 14.0"
*menufilterset "*"
*menufilterdisable 
*settopologydisplaymode 0
*settopologydisplaymode 0
*settopologydisplaymode 0
*ME_CoreBehaviorAdjust "allowable_actions_policy=TC_lite"
*settopologydisplaymode 0
*settopologydisplaymode 0
*ME_CoreBehaviorAdjust "allowable_actions_policy=TC_lite"
*settopologydisplaymode 0
*settopologydisplaymode 0
*elementchecksettings 6 0 0 1 1 6 0 6 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0
*templatefileset "C:/Program Files/Altair/14.0/templates/feoutput/optistruct/optistruct"
*enablemacromenu 1'''
    tclfile.write(s_launch)
    
    #Import the *.iges file.
    s_geom = '''
#Import geometry from *.iges.
*start_batch_import 3
*setgeomrefinelevel 1
*geomimport "auto_detect" "box.iges" "CleanupTol=-0.01" "DoNotMergeEdges=off" "ImportBlanked=off" "ScaleFactor=1.0"
*end_batch_import'''
    tclfile.write(s_geom)
    
    #Making the two extreme surfaces to close the volume.
    s_faces = '''
#Making the two extreme surfaces to close the volume.
*drawlistresetstyle
*surfacemode 4
*createmark lines 1 1 2 12 14
*surfacesplineonlinesloop 1 1 1 3 
*surfacemode 4
*createmark lines 1 8 9 29 35
*surfacesplineonlinesloop 1 1 1 3'''
    tclfile.write(s_faces)
    
    #Create the volume.
    s_volume = '''
*createmark surfaces 1 "all"
*solids_create_from_surfaces 1 4 -1 2'''
    tclfile.write(s_volume)
   
   
    #Collectors management.
    s_colcts = ''' 
#Rename the lvl0 collector...
*retainmarkselections 1
*startnotehistorystate {Renamed component from "lvl0" to "Design"}
*renamecollector components "lvl0" "Design"
*retainmarkselections 0
*endnotehistorystate {Renamed component from "lvl0" to "Design"}
#...create the 'skin' component.
*createentity comps name=component1
*retainmarkselections 1
*startnotehistorystate {Renamed component from "component1" to "skin"}
*renamecollector components "component1" "skin"
*retainmarkselections 0
*endnotehistorystate {Renamed component from "component1" to "skin"}

#...and create the components for the caps.
*createentity comps name=component1
*retainmarkselections 1
*startnotehistorystate {Renamed component from "component1" to "Caps"}
*renamecollector components "component1" "Caps"
*retainmarkselections 0
*endnotehistorystate {Renamed component from "component1" to "Caps"}'''
    tclfile.write(s_colcts)

    s_meshtip = '''
#Create the 2D mesh for the Caps component.
*setedgedensitylinkwithaspectratio -1
*elementorder 1
*startnotehistorystate {Automesh surfaces}
*createmark surfaces 1 17 18
*interactiveremeshsurf 1 ''' + str(size) + ''' 2 2 2 1 1
*set_meshfaceparams 0 2 2 0 0 1 0.5 1 1
*automesh 0 2 2
*set_meshfaceparams 1 2 2 0 0 1 0.5 1 1
*automesh 1 2 2
*storemeshtodatabase 0
*ameshclearsurface 
*endnotehistorystate {Automesh surfaces}'''
    tclfile.write(s_meshtip)   
    
    s_meshsurf = '''
#Make the skin component current.
*retainmarkselections 1
*currentcollector components "skin"
*retainmarkselections 0

#Create the mesh. First the 2D surface mesh. If you see OS uses an iterative command over the 16 surfaces.
#IMPORTANT: The mesh size is the value, '25' in this case, in the line 'interactiveremeshsurf 1 25 2 2 2 1 1'.
*setedgedensitylinkwithaspectratio -1
*elementorder 1
*startnotehistorystate {Automesh surfaces}
*createmark surfaces 1 1-16
*interactiveremeshsurf 1 ''' + str(size) + ''' 2 2 2 1 1
*set_meshfaceparams 0 2 2 0 0 1 0.5 1 1
*automesh 0 2 2
*set_meshfaceparams 1 2 2 0 0 1 0.5 1 1
*automesh 1 2 2
*set_meshfaceparams 2 2 2 0 0 1 0.5 1 1
*automesh 2 2 2
*set_meshfaceparams 3 2 2 0 0 1 0.5 1 1
*automesh 3 2 2
*set_meshfaceparams 4 2 2 0 0 1 0.5 1 1
*automesh 4 2 2
*set_meshfaceparams 5 2 2 0 0 1 0.5 1 1
*automesh 5 2 2
*set_meshfaceparams 6 2 2 0 0 1 0.5 1 1
*automesh 6 2 2
*set_meshfaceparams 7 2 2 0 0 1 0.5 1 1
*automesh 7 2 2
*set_meshfaceparams 8 2 2 0 0 1 0.5 1 1
*automesh 8 2 2
*set_meshfaceparams 9 2 2 0 0 1 0.5 1 1
*automesh 9 2 2
*set_meshfaceparams 10 2 2 0 0 1 0.5 1 1
*automesh 10 2 2
*set_meshfaceparams 11 2 2 0 0 1 0.5 1 1
*automesh 11 2 2
*set_meshfaceparams 12 2 2 0 0 1 0.5 1 1
*automesh 12 2 2
*set_meshfaceparams 13 2 2 0 0 1 0.5 1 1
*automesh 13 2 2
*set_meshfaceparams 14 2 2 0 0 1 0.5 1 1
*automesh 14 2 2
*set_meshfaceparams 15 2 2 0 0 1 0.5 1 1
*automesh 15 2 2
*storemeshtodatabase 0
*ameshclearsurface 
*endnotehistorystate {Automesh surfaces}'''
    tclfile.write(s_meshsurf)  
    
    s_meshsolid = '''
#make current the solid component.
*retainmarkselections 1
*currentcollector components "Design"
*retainmarkselections 0

#Create the solid mesh.
*createstringarray 2 "pars: upd_shell fix_comp_bdr" "tet: 35 1 2 0 0.8 0"
*createmark elements 2 "all"
*tetmesh elements 2 1 elements 0 -1 1 2

#Remove the lateral 2D mesh by deleting the entire 'Caps' component.
*createmark components 1 "Caps"
*deletemark components 1'''
    tclfile.write(s_meshsolid) 
    
    s_mater = '''
#Create the material.
*createentity mats cardimage=MAT1 name=material1
*retainmarkselections 1
*startnotehistorystate {Renamed material from "material1" to "Dural"}
*renamecollector materials "material1" "Dural"
*retainmarkselections 0
*endnotehistorystate {Renamed material from "material1" to "Dural"}
*setvalue mats id=1 STATUS=1 1=73000
*setvalue mats id=1 STATUS=1 3=0.33
*setvalue mats id=1 STATUS=1 4=2.78e-009'''
    tclfile.write(s_mater)
    
    s_props = '''
#Create the properties.

#Thickness property.
*createentity props cardimage=PSHELL name=property1
*retainmarkselections 1
*startnotehistorystate {Renamed property from "property1" to "Thickness"}
*renamecollector properties "property1" "Thickness"
*retainmarkselections 0
*endnotehistorystate {Renamed property from "property1" to "Thickness"}
*setvalue props id=1 STATUS=1 95=0.5
*setvalue props id=1 materialid={mats 1}
#Assign it to the 'Skin' component.
*createmark components 1
*clearmark components 1
*createmark components 1 "skin"
*clearmark components 1
*startnotehistorystate {Assigned "Thickness" to component "skin"}
*createmark components 1 "skin"
*propertyupdate components 1 "Thickness"
*endnotehistorystate {Assigned "Thickness" to component "skin"}
*createmark components 1
*clearmark components 1
*startnotehistorystate {Assigned "Thickness" to component "skin"}
*createmark components 1 "skin"
*propertyupdate components 1 "Thickness"
*endnotehistorystate {Assigned "Thickness" to component "skin"}
*createmark nodes 1
*clearmark nodes 1
*createmark components 1
*clearmark components 1
*createmark properties 1
*clearmark properties 1
*createmark materials 1
*clearmark materials 1
*createmark elements 1
*clearmark elements 1

#Solid property.
*createentity props cardimage=PSHELL name=property1
*retainmarkselections 1
*startnotehistorystate {Renamed property from "property1" to "Solid"}
*renamecollector properties "property1" "Solid"
*retainmarkselections 0
*endnotehistorystate {Renamed property from "property1" to "Solid"}
*setvalue props id=2 cardimage="PSOLID"
*setvalue props id=2 materialid={mats 1}
#Assign the 'Solid' property to the Design component.
*createmark components 1
*clearmark components 1
*createmark components 1 "Design"
*clearmark components 1
*startnotehistorystate {Assigned "Solid" to component "Design"}
*createmark components 1 "Design"
*propertyupdate components 1 "Solid"
*endnotehistorystate {Assigned "Solid" to component "Design"}
*createmark components 1
*clearmark components 1
*startnotehistorystate {Assigned "Solid" to component "Design"}
*createmark components 1 "Design"
*propertyupdate components 1 "Solid"
*endnotehistorystate {Assigned "Solid" to component "Design"}
*createmark nodes 1
*clearmark nodes 1
*createmark components 1
*clearmark components 1
*createmark properties 1
*clearmark properties 1
*createmark materials 1
*clearmark materials 1
*createmark elements 1
*clearmark elements 1'''
    tclfile.write(s_props)
    
    s_constr = '''
#CONSTRAINTS
*createentity loadcols name=loadcol1
*retainmarkselections 1
*startnotehistorystate {Renamed loadcol from "loadcol1" to "Constraints"}
*renamecollector loadcols "loadcol1" "Constraints"
*retainmarkselections 0
*endnotehistorystate {Renamed loadcol from "loadcol1" to "Constraints"}
#Apply the clamped condition to the root surface.
*startnotehistorystate {Show component "Design "}
*createmark components 2 "Design"
*createstringarray 2 "geometry_on" "elements_off"
*showentitybymark 2 1 2
*endnotehistorystate {Show component "Design "}
*startnotehistorystate {Created Constraints}
*createmark surfaces 1 17
*loadcreateonentity_curve surfaces 1 3 1 0 0 0 0 0 0 0 0 0 0 0
*createmark loads 0 1
*loadsupdatefixedvalue 0 0
*endnotehistorystate {Created Constraints}'''
    tclfile.write(s_constr)
    
    s_loads = '''
#LOADS
*createentity loadcols name=loadcol1
*retainmarkselections 1
*startnotehistorystate {Renamed loadcol from "loadcol1" to "Loads"}
*renamecollector loadcols "loadcol1" "Loads"
*retainmarkselections 0
*endnotehistorystate {Renamed loadcol from "loadcol1" to "Loads"}
#Apply the pressure loads on the surfaces.
#Surface 1
*createmark surfaces 1 1
*createmark nodes 1
*pressuresonentity_curve surfaces 1 1 0 0 0 ''' +str(loads[0])+ ''' 30 1 0 0 0 0 0
#Surface 3
*createmark surfaces 1 3
*createmark nodes 1
*pressuresonentity_curve surfaces 1 1 0 0 0 ''' +str(loads[1])+ ''' 30 1 0 0 0 0 0
#Surface 5
*createmark surfaces 1 5
*createmark nodes 1
*pressuresonentity_curve surfaces 1 1 0 0 0 ''' +str(loads[2])+ ''' 30 1 0 0 0 0 0
#Surface 7
*createmark surfaces 1 7
*createmark nodes 1
*pressuresonentity_curve surfaces 1 1 0 0 0 ''' +str(loads[3])+ ''' 30 1 0 0 0 0 0'''
    tclfile.write(s_loads) 
    
    s_loadstep = '''
#Create the LOADSTEP 'Static'
*startnotehistorystate {LoadSteps Creation}
*createmark loadcols 1 "Constraints" "Loads"
*createmark outputblocks 1
*createmark groups 1
*loadstepscreate "static" 1
*attributeupdateint loadsteps 1 4143 1 1 0 1
*attributeupdateint loadsteps 1 4709 1 1 0 1
*attributeupdateentity loadsteps 1 4145 1 1 0 loadcols 1
*attributeupdateentity loadsteps 1 4147 1 1 0 loadcols 2
*attributeupdateint loadsteps 1 9224 1 1 0 0
*attributeupdateint loadsteps 1 3800 1 1 0 0
*attributeupdateint loadsteps 1 707 1 1 0 0
*attributeupdateint loadsteps 1 2396 1 1 0 0
*attributeupdateint loadsteps 1 8134 1 1 0 0
*attributeupdateint loadsteps 1 2160 1 1 0 0
*endnotehistorystate {LoadSteps Creation}'''
    tclfile.write(s_loadstep)
    
    
    
    
    if compliance is True:
        s_responses = '''
#Create the responses.
#COMPLIANCE
*createarray 6 0 0 0 0 0 0
*createdoublearray 6 0 0 0 0 0 0
*optiresponsecreate "compl" 31 0 0 0 0 0 6 0 0 0 1 6 1 6
*optiresponsesetequationdata1 "compl" 0 0 0 0 1 0
*optiresponsesetequationdata2 "compl" 0 0 1 0
*optiresponsesetequationdata3 "compl" 0 0 1 0
*optiresponsesetequationdata4 "compl" 0 0 0 0 1 0 1 0
#VOLUME FRACTION
*createarray 7 2 0 0 0 0 0 0
*createdoublearray 6 0 0 0 0 0 0
*optiresponsecreate "VolFrac" 3 2 0 0 0 1 6 0 0 0 1 7 1 6
*optiresponsesetequationdata1 "VolFrac" 0 0 0 0 1 0
*optiresponsesetequationdata2 "VolFrac" 0 0 1 0
*optiresponsesetequationdata3 "VolFrac" 0 0 1 0
*optiresponsesetequationdata4 "VolFrac" 0 0 0 0 1 0 1 0'''
        tclfile.write(s_responses)    
    
        s_obj = '''
#Design Constraints: DCONSTRAINTS
#Volume Fraction
*createarray 0
*opticonstraintcreate "volume_frac" 2 1 0 ''' +str(volfrac)+ ''' 1 0

#Design Objective
#Compliance
*optiobjectivecreate 1 0 1'''
        tclfile.write(s_obj)
    
    else:        
        s_responses = '''
#Create the responses.
#MASS
*createarray 7 2 0 0 0 0 0 0
*createdoublearray 6 0 0 0 0 0 0
*optiresponsecreate "Mass" 29 2 0 0 0 1 6 0 0 0 1 7 1 6
*optiresponsesetequationdata1 "Mass" 0 0 0 0 1 0
*optiresponsesetequationdata2 "Mass" 0 0 1 0
*optiresponsesetequationdata3 "Mass" 0 0 1 0
*optiresponsesetequationdata4 "Mass" 0 0 0 0 1 0 1 0
#VON MISES STRESS
*createarray 7 2 0 0 0 0 0 0
*createdoublearray 6 0 0 0 0 0 0
*optiresponsecreate "vonMises" 9 2 0 13 0 1 6 0 0 0 1 7 1 6
*createmark elements 0
*optiresponseexcludeelements "vonMises" 0
*optiresponsesetequationdata1 "vonMises" 0 0 0 0 1 0
*optiresponsesetequationdata2 "vonMises" 0 0 1 0
*optiresponsesetequationdata3 "vonMises" 0 0 1 0
*optiresponsesetequationdata4 "vonMises" 0 0 0 0 1 0 1 0
#VOLUME FRACTION
*createarray 7 2 0 0 0 0 0 0
*createdoublearray 6 0 0 0 0 0 0
*optiresponsecreate "VolFrac" 3 2 0 0 0 1 6 0 0 0 1 7 1 6
*optiresponsesetequationdata1 "VolFrac" 0 0 0 0 1 0
*optiresponsesetequationdata2 "VolFrac" 0 0 1 0
*optiresponsesetequationdata3 "VolFrac" 0 0 1 0
*optiresponsesetequationdata4 "VolFrac" 0 0 0 0 1 0 1 0'''
        tclfile.write(s_responses)    
    
        s_obj = '''
#Design Constraints: DCONSTRAINTS
#Stress_von_Mises: -300 and 300 are the lower and upper limit respectively.
*createarray 1 1
*opticonstraintcreate "Stress_vM" 2 2 -400 400 1 1

#Volume Fraction
*createarray 0
*opticonstraintcreate "volume_frac" 3 1 0 ''' +str(volfrac)+ ''' 1 0

#Design Objective
#Mass
*optiobjectivecreate 1 0 0'''
        tclfile.write(s_obj)
        
     
     
     
        
    s_topo = '''
#Create Design Variable (DESVAR): 'Topology'. MINDIM = 100.
*createmark properties 1 "Solid"
*topologydesvarcreate 1 "topology" 0 0 2
*topologyparametersupdatewithmingap "topology" 100 0 0 0 0 0 0

*drawlistresetstyle 
*startnotehistorystate {Modified control Cards}
*cardcreate "ANALYSIS"
*startnotehistorystate {Attached attributes to card}
*attributeupdatestring cards 1 7149 1 2 0 "        "
*endnotehistorystate {Attached attributes to card}
*endnotehistorystate {Modified control Cards}
*startnotehistorystate {Modified control Cards}
*endnotehistorystate {Modified control Cards}


# #opticontrol
# *drawlistresetstyle
# *opticontrolupdate80sr1 1 200 0 0 0 0.6 0 0.01 0 1 0 0 0 0 1 0.01 0 0.5 0 0.2 0 0.5 0 1 0 10 0 0 0 0 0 0 0 0 1 0 1 0
# *opticontrolupdateeslparameters 0 30 0 1 0 0.3
# *opticontrolupdateoptimizationparameters 0 2 0 "MFD" 0 20 0 20 0 1
# *opticontrolupdateremeshparameters 0 0
# *opticontrolupdateapproxparameters 0 "FULL"
# *opticontrolupdatebarconparameters 0 "REQUIRED"
# *opticontrolupdatecontolparameters 0 1
# *opticontrolupdatetopdiscparameters 0 "NO"\n'''
    tclfile.write(s_topo)
   
    hm_file = "box.hm"
    fem_file = "box.fem"
    tclfile.write("#Exporting files HM and FEM.\n")
    tclfile.write("*writefile \""+ hm_file + "\" 1\n")
    tclfile.write("*carddisable \"ANALYSIS\"\n")
    tclfile.write("*createstringarray 1 \"CONNECTORS_SKIP \"\n")
    tclfile.write("*feoutputwithdata \"C:/Program Files/Altair/14.0/templates/feoutput/optistruct/optistruct\" \"" + fem_file + "\" 1 0 2 1 1\n")
    tclfile.write("*cardenable \"ANALYSIS\"\n")

    tclfile.close()







