#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 16:18:33 2018

@author: nick
"""

import cv2
import matplotlib.pyplot as plt

'''
User options: 
    Masked  = True 
        returns masked images in directory
    Masked = False 
        returns 'pretty' images
    
    Directory = 'string' 
        please modify this string to the parent directory of the videos
        
    Name = 'string'
        Modify to correspond to the name of the dataset
    Time = int
        Simulation time of the image (hours please)
'''

Masked = False
Directory = '/home/nick/Desktop/Renders/wrf_microhh/20160611_old/28800/OLD/'
#Name = 'LASSO 20160611 '
#Time = 28800/3600



'''
Source
 |
 |
 V
'''
xcoords = [6400, 9600, 12800, 16000]

if Masked == False:
    name_0 = 'TSI_R '
else:
    name_0 = 'TSI_R '

for xcoord in xcoords:
    name_1 = '(along x = '+str(xcoord)+').avi'
    video = cv2.VideoCapture(Directory+name_0+name_1)

    
    i = -1# framenumber
    success = True
    while success == True:
        i += 1
        print('Frame number = ', i)
        ycoord = i * 150 #m 
        plt.figure()
        success, img = video.read()
        if type(img) == None:
            raise NameError('Files are not in Directory, rename directory to reflect correct directory')
        '''
        Several options may exist at this point, simply saving the data or 
        utilizing some sort of unwrapping algorithm. Or, at this point, the 
        image may be fed to the machine learning algorithm
        '''
        
        plt.title('TSI_Render at: x,y = '+str(xcoord)+', '+str(ycoord)+'(m)')
        plt.imshow(np.array(img))
        plt.show()
        