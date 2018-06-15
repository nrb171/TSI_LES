#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 16:56:11 2018

@author: cls0208
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:59:40 2018

@author: Nick B
"""

import netCDF4 as nc
import numpy as np
from trackpull import trackpull
from cloudsort import cloudsort
#from fractalgen import alpha_shape3d, cloudfieldplot
import bpy
import bmesh
import os
#import matplotlib.pyplot as plt
dset = '/data/wrf_microhh/20160611/' # setting the directory containing ql.nc

timeindex = 8 # setting index time
timesim = timeindex * 3600 # setting simulation time

#path = '/users/PFS0220/cls0208/work/workshop/TSI Renders/'+dset_0+sets[index][3:9]+'/'
fname = dset+'/'


f=nc.Dataset(fname,'r')

varname = "nrcloud" 
idx2 = cloudsort(f)     
num = int(np.max(idx2[:, 3]))
rr=idx2

nrcloud = f.variables['nrcloud'][:]

merged_nrcloud = nrcloud.sum(axis = 1).sum(axis = 1)
CBH = 25 * np.where(merged_nrcloud == merged_nrcloud[merged_nrcloud>0][0])[0]
CBH =  int(CBH)

'''
-----
'''
bpy.ops.mesh.primitive_cube_add(radius=8*0.999/1024);
orig_cube = bpy.context.active_object;
#mat = bpy.data.materials.get('CloudMatv0.1')
mat = bpy.data.materials.get('BaseMask')

#print(mat)

orig_cube.data.materials.append(mat)
orig_cube.name = 'Cloud Base'
'''
-----
'''
bpy.ops.mesh.primitive_cube_add(radius=8*0.999/1024);
orig_cube_sides = bpy.context.active_object;
#mat = bpy.data.materials.get('CloudMatv0.1')
mat = bpy.data.materials.get('CloudMask')

#print(mat)

orig_cube_sides.data.materials.append(mat)
orig_cube_sides.name = 'Cloud Side'
'''
------
desired camera location
'''
ycoordstoloop = np.arange(0,25600,150)/ 25 /1024 * 16 - 8
xcoordstoloop = np.arange(4,12,2) - 8

bpy.ops.mesh.primitive_plane_add();
o = bpy.context.active_object;
me = o.data;
bm = bmesh.new();
o.name = 'Cloud Sides'

bpy.ops.mesh.primitive_plane_add();
osides = bpy.context.active_object;
mesides = osides.data;
bmsides = bmesh.new();
osides.name = 'Cloud Base'

o.name = 'Cloud Field'
k = 0
meancloudbase = 0
print('-----Placing Cloud Particles-----')
for i in range(num): #number of clouds to loop over set to 'num' if you want to loop over all
    #print(i)
    indcloud = rr[rr[:,3]==i+1]
    xs = indcloud[:,2]*16/1024 -8 
    ys = indcloud[:,1]*16/1024 -8
    zs = indcloud[:,0]*16/1024
    zsmin = np.min(zs)
    zslim = CBH + 150/1600
    k += 1
    meancloudbase = (meancloudbase*(k-1)+min(zs))/k
    #rendercount += 1
    for i in range(len(xs)):
        
#        print(meancloudbase)
        x = xs[i]
        y = ys[i]
        z = zs[i]
        if z < zslim:    
            bm.verts.new().co= [x, y, z]
        else:
            bmsides.verts.new().co= [x, y, z]
    bm.to_mesh(me);
    o.dupli_type = 'VERTS';
    orig_cube.parent = o;  


    bmsides.to_mesh(mesides);
    osides.dupli_type = 'VERTS';
    orig_cube_sides.parent = osides;  
    

#text = open(path+'Cloud Base.txt','w')
#text.write('Mean cloud base: '+str(meancloudbase*1024/16*25)+' m')
#text.close()   
#linenum = -1    

'''
This node is for the camera positioning and rendering 
'''

print('----- Rendering -----')

ycoords = np.arange(0,25600,150)/ 25 /1024 * 16 - 8 # every 150m (30s x 5m/s) step size
xcoords = np.arange(4,12,2) - 8
scene = bpy.context.scene
frame = 1

for ob in bpy.data.objects:
    ob.select = False
    
bpy.data.objects['TSI'].select = True # putting the TSI as the acitve object so we only animate it.

for l in xcoords:
    frame = 0
    for m in ycoords:
        camera_loc = np.array([l,m,0.001])
        camera = bpy.data.objects['TSI']
        scene.frame_set(frame) # updating the fram
        camera.location.x = camera_loc[0] # move the camera to appropriate x,y,z locs
        camera.location.y = camera_loc[1]
        camera.location.z = camera_loc[2]
        
        bpy.ops.anim.keyframe_insert(type = 'Location') # Creating keyframe

        
        print(frame, camera_loc)
        
        frame += 1
        
    
        
    bpy.data.scenes['Scene'].render.filepath = '/home/nick/Desktop/Renders/wrf_microhh/20160611_old/'+str(timesim)+'/TSI_R (along x = '+str((l + 8) * 1600)+').avi' # setting save location
    bpy.ops.render.render( write_still=True, animation = True ) # initializing rendering

        