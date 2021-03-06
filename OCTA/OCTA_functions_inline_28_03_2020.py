# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 12:21:35 2019
OCTA: Order & Complexity Toolbox for Aesthetics
@author: Eline Van Geert
"""

# Import necessary libraries 
#import os
import svgwrite
import numpy as np
import colour
import pandas as pd
#import json
   
### CREATE JSON FILE
def create_pattern_json(template = "grid",
                   shape = ['rectangle'], 
                   image = ["none"], #'../vector_images/hotdog.svg',
                   text = ["none"],
                   nrows = 5, ncols = 5,
                   startx = 30, starty = 30,
                   xdist = 30, ydist = 30,
                   shapemirror = ['none'],
                   orientation = [0],
                   shapecolour = ["blue"],
                   repeateachcolor = 1,
                   colourpattern = 'identity',
                   colourdim = 'element',
                   repeateachshape = 1,
                   shapepattern = 'identity',
                   shapedim = 'element',
                   repeateachshapeorientation = 1,
                   shapeorientationpattern = 'identity',
                   shapeorientationdim = 'element',
                   shapesize = [20],
                   shapexyratio = [1],
                   jitterscale = [0],
                   writedir = "OCTA_stimuli", 
                   output = ['txtinline']): # 'json', 'jsoninline', 'txt' and 'txtinline' possible
     
    # if "json" in output:      
    #     # If folder for .json-files does not exist yet, create folder
    #     if not os.path.exists(writedir + '/json/'):
    #         os.makedirs(writedir + '/json/')
    #             
    #     imgsjson = os.listdir('OCTA_stimuli/json/')
    # 
    # if 'txt' in output:       
    #     if not os.path.exists(writedir + '/txt/'):
    #         os.makedirs(writedir + '/txt/')
    #             
    #     imgstxt = os.listdir('OCTA_stimuli/txt/')
    
    # LOCATIONS
    
    if template == "grid":  
        x = np.tile(np.arange(startx, startx + xdist*ncols, xdist), reps = nrows)
        y = np.repeat(np.arange(starty, starty + ydist*nrows, ydist), repeats = ncols)
    elif template == "sine":
        x = np.tile(np.arange(startx, startx + xdist*ncols, xdist), reps = nrows)
        y = np.repeat(np.arange(starty, starty + ydist*nrows, ydist), repeats = ncols) - np.sin(x)*(shapesize)
    elif template == "cosine":
        x = np.tile(np.arange(startx, startx + xdist*ncols, xdist), reps = nrows)
        y = np.repeat(np.arange(starty, starty + ydist*nrows, ydist), repeats = ncols) - np.cos(x)*(shapesize)
    elif template == "circle":
        x = startx + xdist * np.cos(2*np.pi*np.arange(1, ncols+1, 1)/ncols)
        y = starty + xdist * np.sin(2*np.pi*np.arange(1, ncols+1, 1)/ncols)
    elif template == "unity":
        x = np.repeat(startx, repeats = nrows*ncols)
        y = np.repeat(starty, repeats = nrows*ncols)

    # Calculate dimensions resulting image
    max_x = float(max(x) + xdist)
    max_y = float(max(y) + ydist)
    
    # Naming of output image 
    # if "json" in output: 
    #     jsonfilename = (writedir + '/json/' + str(len(imgsjson)+1).zfill(8) + '.json')
    # if "txt" in output:
    #     txtfilename = (writedir + '/txt/' + str(len(imgstxt)+1).zfill(8) + '.txt')  
    # BACKGROUND COLOR 
#    dwg.add(dwg.rect(insert=(0, 0), size=('1530', '530'), rx=None, ry=None, fill='lightgrey'))
    
    ### COMPLEXITY ###
    
    ## IN LOCATION ##
    
    # ADD JITTER
    xjitter = np.random.normal(loc = 0, scale = jitterscale, size = nrows*ncols)
    x = x + xjitter
    yjitter = np.random.normal(loc = 0, scale = jitterscale, size = nrows*ncols)
    y = y + yjitter
    
    ## IN COLOUR ##
    
    # COLOUR
    if colourpattern == "gradient":
               
        if isinstance(shapecolour, str): 
            startcol = colour.Color(shapecolour)
            endcol = colour.Color(shapecolour)
        else:            
            startcol = colour.Color(shapecolour[0])
            endcol = colour.Color(shapecolour[1]) 
        
        if colourdim == "element":
            gradient = list(startcol.range_to(endcol, int((nrows * ncols))))
            colors = {}
            for i in range(len(gradient)):
                colors[i] = gradient[i].hex
            col = list(colors.values())
            
        elif colourdim == "row":
            gradient = list(startcol.range_to(endcol, int(nrows)))
            colors = {}
            for i in range(len(gradient)):
                colors[i] = gradient[i].hex
            col = np.repeat(list(colors.values()), repeats = ncols)      
            
        elif colourdim == "col":
            gradient = list(startcol.range_to(endcol, int(ncols)))
            colors = {}
            for i in range(len(gradient)):
                colors[i] = gradient[i].hex
            col = np.tile(list(colors.values()), reps = nrows)
            
        elif colourdim == "rightdiag":
            gradient = list(startcol.range_to(endcol, int((nrows+ncols)-1)))
            colors = {}
            for i in range(len(gradient)):
                colors[i] = gradient[i].hex
            
            col = np.array(list(colors.values())[:ncols])
            for i in range(1,nrows):
                col = np.append(col, np.roll(list(colors.values()), -i)[:ncols])
                
        elif colourdim == "leftdiag":
            gradient = list(startcol.range_to(endcol, int((nrows+ncols)-1)))
            colors = {}
            for i in range(len(gradient)):
                colors[i] = gradient[i].hex
            
            col = np.array(list(colors.values())[:ncols])[::-1]
            for i in range(1,nrows):
                col = np.append(col, np.roll(list(colors.values()), -i)[:ncols][::-1])
        
    elif colourpattern == "repeateach":
        shapecolour = list(np.repeat(shapecolour, repeateachcolor))
        
        if colourdim == "element":
            # create list that is as long as number of elements in grid (nrows * ncols)
            col = np.array(shapecolour * int((nrows * ncols) / len(shapecolour)))
            if ((nrows * ncols) % len(shapecolour) != 0):
                col = np.append(col, shapecolour[0:(nrows * ncols) % len(shapecolour)]) 
            
        elif colourdim == "row":
            # create list that is as long as number of elements in grid (nrows * ncols)
            col = np.array(shapecolour * int((ncols) / len(shapecolour)))
            if ((ncols) % len(shapecolour) != 0):
                col = np.append(col, shapecolour[0:(ncols) % len(shapecolour)]) 
                
            col = np.tile(col, reps = nrows)
            
        elif colourdim == "col":
            # create list that is as long as number of elements in grid (nrows * ncols)
            col = np.array(shapecolour * int((nrows) / len(shapecolour)))
            if ((nrows) % len(shapecolour) != 0):
                col = np.append(col, shapecolour[0:(nrows) % len(shapecolour)]) 
                
            col = np.repeat(col, repeats = ncols)

        elif colourdim == "rightdiag":
            colors = np.array(shapecolour * int((nrows+ncols)-1 / len(shapecolour)))
            if (((nrows+ncols)-1) % len(shapecolour) != 0):
                colors = np.append(colors, shapecolour[0:((nrows+ncols)-1) % len(shapecolour)]) 
                     
            col = colors[:ncols]
            for i in range(1,nrows):
                col = np.append(col, np.roll(colors, -i)[:ncols])
                
        elif colourdim == "leftdiag":
            colors = np.array(shapecolour * int((nrows+ncols)-1 / len(shapecolour)))
            if (((nrows+ncols)-1) % len(shapecolour) != 0):
                colors = np.append(colors, shapecolour[0:((nrows+ncols)-1) % len(shapecolour)]) 
                     
            col = colors[:ncols][::-1]
            for i in range(1,nrows):
                col = np.append(col, np.roll(colors, -i)[:ncols][::-1])
                
    elif colourpattern == "symmetric":
        shapecolour = list(np.repeat(shapecolour, repeateachcolor))
        
        if colourdim == "element":
            shapecolour = np.concatenate((shapecolour, shapecolour[:-1][::-1]))
            col = np.array(list(shapecolour) * int((nrows * ncols) / len(shapecolour)))
            if ((nrows * ncols) % len(shapecolour) != 0):
                col = np.append(col, shapecolour[0:(nrows * ncols) % len(shapecolour)]) 
            
        elif colourdim == "row":
            if ncols % 2 != 0:
                shapecolour = list(np.concatenate((
                    shapecolour *int((int(((ncols)/2)+1) / len(shapecolour)) ), 
                    shapecolour[0:int(((ncols)/2)+1) % len(shapecolour)],
                    list(shapecolour[0:int(((ncols)/2)) % len(shapecolour)])[::-1],
                    list(shapecolour * (int(((ncols)/2) / len(shapecolour)) ))[::-1])))
            else:
                shapecolour = list(np.concatenate((
                    shapecolour *(int(((ncols)/2) / len(shapecolour)) ), 
                    shapecolour[0:int(((ncols)/2)) % len(shapecolour)],
                    list(shapecolour[0:int(((ncols)/2)) % len(shapecolour)])[::-1],
                    list(shapecolour * (int(((ncols)/2) / len(shapecolour)) ))[::-1])))
            col = np.array(list(shapecolour) * int((ncols) / len(shapecolour)))
            if ((ncols) % len(shapecolour) != 0):
                col = np.append(col, shapecolour[0:(ncols) % len(shapecolour)]) 
                
            col = np.tile(col, reps = nrows)
            
        elif colourdim == "col":
            if nrows % 2 != 0:
                shapecolour = list(np.concatenate((
                    shapecolour *int((int(((nrows)/2)+1) / len(shapecolour)) ), 
                    shapecolour[0:int(((nrows)/2)+1) % len(shapecolour)],
                    list(shapecolour[0:int(((nrows)/2)) % len(shapecolour)])[::-1],
                    list(shapecolour * (int(((nrows)/2) / len(shapecolour)) ))[::-1])))
            else:
                shapecolour = list(np.concatenate((
                    shapecolour *(int(((nrows)/2) / len(shapecolour)) ), 
                    shapecolour[0:int(((nrows)/2)) % len(shapecolour)],
                    list(shapecolour[0:int(((nrows)/2)) % len(shapecolour)])[::-1],
                    list(shapecolour * (int(((nrows)/2) / len(shapecolour)) ))[::-1])))
                
            col = np.array(list(shapecolour) * int((nrows) / len(shapecolour)))
            if ((nrows) % len(shapecolour) != 0):
                col = np.append(col, shapecolour[0:(nrows) % len(shapecolour)]) 
                
            col = np.repeat(col, repeats = ncols)

        elif colourdim == "rightdiag":
               
            if ((nrows+ncols)-1) % 2 != 0:
                shapecolour = list(np.concatenate((
                        shapecolour *int(int(((nrows+ncols-1)/2)+1) / len(shapecolour) ), 
                        shapecolour[0:int(((nrows+ncols-1)/2)+1) % len(shapecolour)],
                        list(shapecolour[0:int(((nrows+ncols-1)/2)) % len(shapecolour)])[::-1],
                        list(shapecolour * (int(((nrows+ncols-1)/2) / len(shapecolour)) ))[::-1])))
                colors = np.array(shapecolour * int(((nrows+ncols)-1)/ len(shapecolour)))
            else:
                shapecolour = list(np.concatenate((
                        shapecolour *(int(((nrows+ncols-1)/2) / len(shapecolour)) ), 
                        shapecolour[0:int(((nrows+ncols-1)/2)) % len(shapecolour)],
                        list(shapecolour[0:int(((nrows+ncols-1)/2)) % len(shapecolour)])[::-1],
                        list(shapecolour * (int(((nrows+ncols-1)/2) / len(shapecolour)) ))[::-1])))
                colors = np.array(shapecolour * int(((nrows+ncols)-1)/ len(shapecolour)))
                     
            col = colors[:ncols]
            for i in range(1,nrows):
                col = np.append(col, np.roll(colors, -i)[:ncols])
                
        elif colourdim == "leftdiag":
                           
            if ((nrows+ncols)-1) % 2 != 0:
                shapecolour = list(np.concatenate((
                        shapecolour *int(int(((nrows+ncols-1)/2)+1) / len(shapecolour) ), 
                        shapecolour[0:int(((nrows+ncols-1)/2)+1) % len(shapecolour)],
                        list(shapecolour[0:int(((nrows+ncols-1)/2)) % len(shapecolour)])[::-1],
                        list(shapecolour * (int(((nrows+ncols-1)/2) / len(shapecolour)) ))[::-1])))
                colors = np.array(shapecolour * int(((nrows+ncols)-1)/ len(shapecolour)))
            else:
                shapecolour = list(np.concatenate((
                        shapecolour *(int(((nrows+ncols-1)/2) / len(shapecolour)) ), 
                        shapecolour[0:int(((nrows+ncols-1)/2)) % len(shapecolour)],
                        list(shapecolour[0:int(((nrows+ncols-1)/2)) % len(shapecolour)])[::-1],
                        list(shapecolour * (int(((nrows+ncols-1)/2) / len(shapecolour)) ))[::-1])))
                colors = np.array(shapecolour * int(((nrows+ncols)-1)/ len(shapecolour)))
                     
            col = colors[:ncols][::-1]
            for i in range(1,nrows):
                col = np.append(col, np.roll(colors, -i)[:ncols][::-1])
               
    
    elif colourpattern == "identity":
        # create list that is as long as number of elements in grid (nrows * ncols)
        col = np.resize(shapecolour, [nrows*ncols,1]).flatten()
        
    elif colourpattern == "random":
        # create list that is as long as number of elements in grid (nrows * ncols)
        col = np.resize(shapecolour, [nrows*ncols,1]).flatten()
        np.random.shuffle(col)

    ## IN SIZE ##
    
    # SIZE
    # create list that is as long as number of elements in grid (nrows * ncols)
    size = np.resize(shapesize, [nrows*ncols,1]).flatten()
        
    ## IN shapeorientation ##
    
    # shapeorientation
        
    if shapeorientationpattern == "repeateach":
        orientation = list(np.repeat(orientation, repeateachshapeorientation))
        
        if shapeorientationdim == "element":
            # create list that is as long as number of elements in grid (nrows * ncols)
            shapeorientation = np.array(orientation * int((nrows * ncols) / len(orientation)))
            if ((nrows * ncols) % len(orientation) != 0):
                shapeorientation = np.append(shapeorientation, orientation[0:(nrows * ncols) % len(orientation)]) 
            
        elif shapeorientationdim == "row":
            # create list that is as long as number of elements in grid (nrows * ncols)
            shapeorientation = np.array(orientation * int((ncols) / len(orientation)))
            if ((ncols) % len(orientation) != 0):
                shapeorientation = np.append(shapeorientation, orientation[0:(ncols) % len(orientation)]) 
                
            shapeorientation = np.tile(shapeorientation, reps = nrows)
            
        elif shapeorientationdim == "col":
            # create list that is as long as number of elements in grid (nrows * ncols)
            shapeorientation = np.array(orientation * int((nrows) / len(orientation)))
            if ((nrows) % len(orientation) != 0):
                shapeorientation = np.append(shapeorientation, orientation[0:(nrows) % len(orientation)]) 
                
            shapeorientation = np.repeat(shapeorientation, repeats = ncols)

        elif shapeorientationdim == "rightdiag":
            elementshapeorientations = np.array(orientation * int((nrows+ncols)-1 / len(orientation)))
            if (((nrows+ncols)-1) % len(orientation) != 0):
                elementshapeorientations = np.append(elementshapeorientations, orientation[0:((nrows+ncols)-1) % len(orientation)]) 
                     
            shapeorientation = elementshapeorientations[:ncols]
            for i in range(1,nrows):
                shapeorientation = np.append(shapeorientation, np.roll(elementshapeorientations, -i)[:ncols])
                
        elif shapeorientationdim == "leftdiag":
            elementshapeorientations = np.array(orientation * int((nrows+ncols)-1 / len(orientation)))
            if (((nrows+ncols)-1) % len(orientation) != 0):
                elementshapeorientations = np.append(elementshapeorientations, orientation[0:((nrows+ncols)-1) % len(orientation)]) 
                     
            shapeorientation = elementshapeorientations[:ncols][::-1]
            for i in range(1,nrows):
                shapeorientation = np.append(shapeorientation, np.roll(elementshapeorientations, -i)[:ncols][::-1])
                
    elif shapeorientationpattern == "symmetric":
        orientation = list(np.repeat(orientation, repeateachshapeorientation))
        
        if shapeorientationdim == "element":
            orientation = np.concatenate((orientation, orientation[:-1][::-1]))
            shapeorientation = np.array(list(orientation) * int((nrows * ncols) / len(orientation)))
            if ((nrows * ncols) % len(orientation) != 0):
                shapeorientation = np.append(shapeorientation, orientation[0:(nrows * ncols) % len(orientation)]) 
            
        elif shapeorientationdim == "row":
            if ncols % 2 != 0:
                orientation = list(np.concatenate((
                    orientation *int((int(((ncols)/2)+1) / len(orientation)) ), 
                    orientation[0:int(((ncols)/2)+1) % len(orientation)],
                    list(orientation[0:int(((ncols)/2)) % len(orientation)])[::-1],
                    list(orientation * (int(((ncols)/2) / len(orientation)) ))[::-1])))
            else:
                orientation = list(np.concatenate((
                    orientation *(int(((ncols)/2) / len(orientation)) ), 
                    orientation[0:int(((ncols)/2)) % len(orientation)],
                    list(orientation[0:int(((ncols)/2)) % len(orientation)])[::-1],
                    list(orientation * (int(((ncols)/2) / len(orientation)) ))[::-1])))
            shapeorientation = np.array(list(orientation) * int((ncols) / len(orientation)))
            if ((ncols) % len(orientation) != 0):
                shapeorientation = np.append(shapeorientation, orientation[0:(ncols) % len(orientation)]) 
                
            shapeorientation = np.tile(shapeorientation, reps = nrows)
            
        elif shapeorientationdim == "col":
            if nrows % 2 != 0:
                orientation = list(np.concatenate((
                    orientation *int((int(((nrows)/2)+1) / len(orientation)) ), 
                    orientation[0:int(((nrows)/2)+1) % len(orientation)],
                    list(orientation[0:int(((nrows)/2)) % len(orientation)])[::-1],
                    list(orientation * (int(((nrows)/2) / len(orientation)) ))[::-1])))
            else:
                orientation = list(np.concatenate((
                    orientation *(int(((nrows)/2) / len(orientation)) ), 
                    orientation[0:int(((nrows)/2)) % len(orientation)],
                    list(orientation[0:int(((nrows)/2)) % len(orientation)])[::-1],
                    list(orientation * (int(((nrows)/2) / len(orientation)) ))[::-1])))
                
            shapeorientation = np.array(list(orientation) * int((nrows) / len(orientation)))
            if ((nrows) % len(orientation) != 0):
                shapeorientation = np.append(shapeorientation, orientation[0:(nrows) % len(orientation)]) 
                
            shapeorientation = np.repeat(shapeorientation, repeats = ncols)

        elif shapeorientationdim == "rightdiag":
               
            if ((nrows+ncols)-1) % 2 != 0:
                orientation = list(np.concatenate((
                        orientation *int(int(((nrows+ncols-1)/2)+1) / len(orientation) ), 
                        orientation[0:int(((nrows+ncols-1)/2)+1) % len(orientation)],
                        list(orientation[0:int(((nrows+ncols-1)/2)) % len(orientation)])[::-1],
                        list(orientation * (int(((nrows+ncols-1)/2) / len(orientation)) ))[::-1])))
                elementshapeorientations = np.array(orientation * int(((nrows+ncols)-1)/ len(orientation)))
            else:
                orientation = list(np.concatenate((
                        orientation *(int(((nrows+ncols-1)/2) / len(orientation)) ), 
                        orientation[0:int(((nrows+ncols-1)/2)) % len(orientation)],
                        list(orientation[0:int(((nrows+ncols-1)/2)) % len(orientation)])[::-1],
                        list(orientation * (int(((nrows+ncols-1)/2) / len(orientation)) ))[::-1])))
                elementshapeorientations = np.array(orientation * int(((nrows+ncols)-1)/ len(orientation)))
                     
            shapeorientation = elementshapeorientations[:ncols]
            for i in range(1,nrows):
                shapeorientation = np.append(shapeorientation, np.roll(elementshapeorientations, -i)[:ncols])
                
        elif shapeorientationdim == "leftdiag":
                           
            if ((nrows+ncols)-1) % 2 != 0:
                orientation = list(np.concatenate((
                        orientation *int(int(((nrows+ncols-1)/2)+1) / len(orientation) ), 
                        orientation[0:int(((nrows+ncols-1)/2)+1) % len(orientation)],
                        list(orientation[0:int(((nrows+ncols-1)/2)) % len(orientation)])[::-1],
                        list(orientation * (int(((nrows+ncols-1)/2) / len(orientation)) ))[::-1])))
                elementshapeorientations = np.array(orientation * int(((nrows+ncols)-1)/ len(orientation)))
            else:
                orientation = list(np.concatenate((
                        orientation *(int(((nrows+ncols-1)/2) / len(orientation)) ), 
                        orientation[0:int(((nrows+ncols-1)/2)) % len(orientation)],
                        list(orientation[0:int(((nrows+ncols-1)/2)) % len(orientation)])[::-1],
                        list(orientation * (int(((nrows+ncols-1)/2) / len(orientation)) ))[::-1])))
                elementshapeorientations = np.array(orientation * int(((nrows+ncols)-1)/ len(orientation)))
                     
            shapeorientation = elementshapeorientations[:ncols][::-1]
            for i in range(1,nrows):
                shapeorientation = np.append(shapeorientation, np.roll(elementshapeorientations, -i)[:ncols][::-1])
               
    
    elif shapeorientationpattern == "identity":
        # create list that is as long as number of elements in grid (nrows * ncols)
        shapeorientation = np.resize(orientation, [nrows*ncols,1]).flatten()
        
    elif shapeorientationpattern == "random":
        # create list that is as long as number of elements in grid (nrows * ncols)
        shapeorientation = np.resize(orientation, [nrows*ncols,1]).flatten()
        np.random.shuffle(shapeorientation)
        
    ## IN SHAPE ##
    
    if shapepattern == "repeateach":
        shape = list(np.repeat(shape, repeateachshape))
        
        if shapedim == "element":
            # create list that is as long as number of elements in grid (nrows * ncols)
            elementshape = np.array(shape * int((nrows * ncols) / len(shape)))
            if ((nrows * ncols) % len(shape) != 0):
                elementshape = np.append(elementshape, shape[0:(nrows * ncols) % len(shape)]) 
            
        elif shapedim == "row":
            # create list that is as long as number of elements in grid (nrows * ncols)
            elementshape = np.array(shape * int((ncols) / len(shape)))
            if ((ncols) % len(shape) != 0):
                elementshape = np.append(elementshape, shape[0:(ncols) % len(shape)]) 
                
            elementshape = np.tile(elementshape, reps = nrows)
            
        elif shapedim == "col":
            # create list that is as long as number of elements in grid (nrows * ncols)
            elementshape = np.array(shape * int((nrows) / len(shape)))
            if ((nrows) % len(shape) != 0):
                elementshape = np.append(elementshape, shape[0:(nrows) % len(shape)]) 
                
            elementshape = np.repeat(elementshape, repeats = ncols)

        elif shapedim == "rightdiag":
            elementshapes = np.array(shape * int((nrows+ncols)-1 / len(shape)))
            if (((nrows+ncols)-1) % len(shape) != 0):
                elementshapes = np.append(elementshapes, shape[0:((nrows+ncols)-1) % len(shape)]) 
                     
            elementshape = elementshapes[:ncols]
            for i in range(1,nrows):
                elementshape = np.append(elementshape, np.roll(elementshapes, -i)[:ncols])
                
        elif shapedim == "leftdiag":
            elementshapes = np.array(shape * int((nrows+ncols)-1 / len(shape)))
            if (((nrows+ncols)-1) % len(shape) != 0):
                elementshapes = np.append(elementshapes, shape[0:((nrows+ncols)-1) % len(shape)]) 
                     
            elementshape = elementshapes[:ncols][::-1]
            for i in range(1,nrows):
                elementshape = np.append(elementshape, np.roll(elementshapes, -i)[:ncols][::-1])
                
    elif shapepattern == "symmetric":
        shape = list(np.repeat(shape, repeateachshape))
        
        if shapedim == "element":
            shape = np.concatenate((shape, shape[:-1][::-1]))
            elementshape = np.array(list(shape) * int((nrows * ncols) / len(shape)))
            if ((nrows * ncols) % len(shape) != 0):
                elementshape = np.append(elementshape, shape[0:(nrows * ncols) % len(shape)]) 
            
        elif shapedim == "row":
            if ncols % 2 != 0:
                shape = list(np.concatenate((
                    shape *int((int(((ncols)/2)+1) / len(shape)) ), 
                    shape[0:int(((ncols)/2)+1) % len(shape)],
                    list(shape[0:int(((ncols)/2)) % len(shape)])[::-1],
                    list(shape * (int(((ncols)/2) / len(shape)) ))[::-1])))
            else:
                shape = list(np.concatenate((
                    shape *(int(((ncols)/2) / len(shape)) ), 
                    shape[0:int(((ncols)/2)) % len(shape)],
                    list(shape[0:int(((ncols)/2)) % len(shape)])[::-1],
                    list(shape * (int(((ncols)/2) / len(shape)) ))[::-1])))
            elementshape = np.array(list(shape) * int((ncols) / len(shape)))
            if ((ncols) % len(shape) != 0):
                elementshape = np.append(elementshape, shape[0:(ncols) % len(shape)]) 
                
            elementshape = np.tile(elementshape, reps = nrows)
            
        elif shapedim == "col":
            if nrows % 2 != 0:
                shape = list(np.concatenate((
                    shape *int((int(((nrows)/2)+1) / len(shape)) ), 
                    shape[0:int(((nrows)/2)+1) % len(shape)],
                    list(shape[0:int(((nrows)/2)) % len(shape)])[::-1],
                    list(shape * (int(((nrows)/2) / len(shape)) ))[::-1])))
            else:
                shape = list(np.concatenate((
                    shape *(int(((nrows)/2) / len(shape)) ), 
                    shape[0:int(((nrows)/2)) % len(shape)],
                    list(shape[0:int(((nrows)/2)) % len(shape)])[::-1],
                    list(shape * (int(((nrows)/2) / len(shape)) ))[::-1])))
                
            elementshape = np.array(list(shape) * int((nrows) / len(shape)))
            if ((nrows) % len(shape) != 0):
                elementshape = np.append(elementshape, shape[0:(nrows) % len(shape)]) 
                
            elementshape = np.repeat(elementshape, repeats = ncols)

        elif shapedim == "rightdiag":
               
            if ((nrows+ncols)-1) % 2 != 0:
                shape = list(np.concatenate((
                        shape *int(int(((nrows+ncols-1)/2)+1) / len(shape) ), 
                        shape[0:int(((nrows+ncols-1)/2)+1) % len(shape)],
                        list(shape[0:int(((nrows+ncols-1)/2)) % len(shape)])[::-1],
                        list(shape * (int(((nrows+ncols-1)/2) / len(shape)) ))[::-1])))
                elementshapes = np.array(shape * int(((nrows+ncols)-1)/ len(shape)))
            else:
                shape = list(np.concatenate((
                        shape *(int(((nrows+ncols-1)/2) / len(shape)) ), 
                        shape[0:int(((nrows+ncols-1)/2)) % len(shape)],
                        list(shape[0:int(((nrows+ncols-1)/2)) % len(shape)])[::-1],
                        list(shape * (int(((nrows+ncols-1)/2) / len(shape)) ))[::-1])))
                elementshapes = np.array(shape * int(((nrows+ncols)-1)/ len(shape)))
                     
            elementshape = elementshapes[:ncols]
            for i in range(1,nrows):
                elementshape = np.append(elementshape, np.roll(elementshapes, -i)[:ncols])
                
        elif shapedim == "leftdiag":
                           
            if ((nrows+ncols)-1) % 2 != 0:
                shape = list(np.concatenate((
                        shape *int(int(((nrows+ncols-1)/2)+1) / len(shape) ), 
                        shape[0:int(((nrows+ncols-1)/2)+1) % len(shape)],
                        list(shape[0:int(((nrows+ncols-1)/2)) % len(shape)])[::-1],
                        list(shape * (int(((nrows+ncols-1)/2) / len(shape)) ))[::-1])))
                elementshapes = np.array(shape * int(((nrows+ncols)-1)/ len(shape)))
            else:
                shape = list(np.concatenate((
                        shape *(int(((nrows+ncols-1)/2) / len(shape)) ), 
                        shape[0:int(((nrows+ncols-1)/2)) % len(shape)],
                        list(shape[0:int(((nrows+ncols-1)/2)) % len(shape)])[::-1],
                        list(shape * (int(((nrows+ncols-1)/2) / len(shape)) ))[::-1])))
                elementshapes = np.array(shape * int(((nrows+ncols)-1)/ len(shape)))
                     
            elementshape = elementshapes[:ncols][::-1]
            for i in range(1,nrows):
                elementshape = np.append(elementshape, np.roll(elementshapes, -i)[:ncols][::-1])
               
    
    elif shapepattern == "identity":
        # create list that is as long as number of elements in grid (nrows * ncols)
        elementshape = np.resize(shape, [nrows*ncols,1]).flatten()
    
    elif shapepattern == "random":
        # create list that is as long as number of elements in grid (nrows * ncols)
        elementshape = np.resize(shape, [nrows*ncols,1]).flatten()
        np.random.shuffle(elementshape)
        
    text = np.resize(text, [nrows*ncols,1]).flatten()
    
    image = np.resize(image, [nrows*ncols,1]).flatten()
    
    # add image info
    
    n = 0
    img = np.repeat(None, (nrows*ncols))
    for i in range(nrows*ncols):
        if elementshape[i] == 'image': 
            img[i] = image[n]
            n += 1
    
    # add text info
    
    n = 0
    txt = np.repeat(None, (nrows*ncols))
    for i in range(nrows*ncols):
        if elementshape[i] == 'text': 
            txt[i] = text[n]
            n += 1
    
    # create list that is as long as number of elements in grid (nrows * ncols)    
    xyratioshape = np.resize(shapexyratio, [nrows*ncols,1]).flatten()
        
    ## TRANSLATION (HORIZONTAL, VERTICAL, HORIZONTALVERTICAL)
    
    # create list that is as long as number of elements in grid (nrows * ncols)
    mirror = np.resize(shapemirror, [nrows*ncols,1]).flatten() 
    
    # https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
    if ('txt' or 'txtinline') in output:
        df = pd.DataFrame({
                   'template': np.repeat(template, repeats = ncols*nrows),
                   'max_x': np.repeat(max_x, repeats = ncols*nrows),
                   'max_y': np.repeat(max_y, repeats = ncols*nrows),
                   'xdist': np.repeat(xdist, repeats = ncols*nrows),
                   'ydist': np.repeat(ydist, repeats = ncols*nrows),
                   'shaperepeat': np.repeat(repeateachshape, repeats = ncols*nrows),
                   'colourpattern': np.repeat(colourpattern, repeats = ncols*nrows),
                   'colourdim': np.repeat(colourdim, repeats = ncols*nrows),
                   'colourrepeat': np.repeat(repeateachcolor, repeats = ncols*nrows),
                   'number': range(1,nrows*ncols+1), 
                   'column': np.array(list(np.arange(1, ncols+1, 1)) * nrows),
                   'row': np.repeat(np.arange(1, nrows+1, 1), repeats = ncols),
                   'x': x,
                   'y': y,
                   'xjitter': xjitter,
                   'yjitter': yjitter,
                   'shape': elementshape,
                   'xyratio': xyratioshape,
                   'colour': col,
                   'size': size,
                   'shapeorientation': shapeorientation,
                   'mirror': mirror
                   })
    
    # if 'txt' in output:
    #     
    #     df.to_csv(txtfilename, index = False, header = True, sep = "|")
        
    if "txtinline" in output:
        # return dataframe      
        return df
        
    # if 'json' in output:    
    #     data = {}
    #     data['display'] = []
    #     data['display'].append({
    #                        'template': template, 
    #                        'max_x': max_x,
    #                        'max_y': max_y,
    #                        'xdist': xdist,
    #                        'ydist': ydist,
    #                        'xjitter': list(set(xjitter)),
    #                        'yjitter': list(set(yjitter)),
    #                        'shaperepeat': repeateachshape,
    #                        'colourpattern': colourpattern,
    #                        'colourdim': colourdim,
    #                        'colourrepeat': repeateachcolor})
    #     
    #     data['elements'] = []
    #     data['elements'].append({
    #                        'number': list(range(1,nrows*ncols+1)), 
    #                        'column': list(map(int, np.array(list(np.arange(1, ncols+1, 1)) * nrows))),
    #                        'row': list(map( int, np.repeat(np.arange(1, nrows+1, 1), repeats = ncols))),
    #                        'max_x': list(map(float, np.repeat(max_x, nrows*ncols))),
    #                        'max_y': list(map(float, np.repeat(max_y, nrows*ncols))),
    #                        'x': list(map(float, x)),
    #                        'y': list(map(float, y)),
    #                        'shape': list(elementshape),
    #                        'xyratio': list(map(float, xyratioshape)),
    #                        'colour': list(col),
    #                        'size': list(map(int, size)),
    #                        'shapeorientation': list(map(int,shapeorientation)),
    #                        'mirror': list(mirror)})  
    # 
    #     # write JSON file
    #     with open(jsonfilename, 'w') as outfile:
    #         json.dump(data, outfile, indent = 4)
        
    # if "jsoninline" in output:
    #     # return JSON      
    #     return data


### CREATE SVG FROM JSON
def create_pattern_fromjson_inline(data, viewbox = True, 
                                   writedir = "OCTA_stimuli",
                                   output = ['svginline']): # choose SVG OR SVGINLINE!!!
    
    # if 'svg' in output: 
    #     # If folder for .svg-files does not exist yet, create folder
    #     if not os.path.exists(writedir + '/svg/'):
    #         os.makedirs(writedir + '/svg/')
    #         
    #     # Get .svg img directory
    #     imgs = os.listdir(writedir + '/svg/') 
    
    data = pd.DataFrame(data)
    # Read parameter info from .txt file
    max_x = np.unique(data['max_x'][0])[0]
    max_y = np.unique(data['max_y'][0])[0]
    x = data['x'][0]
    y = data['y'][0]
    elementshape = data['shape'][0]
#    img = list(data['elements'][0]['img'])
#    txt = list(data['elements'][0]['txt'])
    xyratioshape = data['xyratio'][0]    
    col = data['colour'][0]
    size = data['size'][0]
    shapeorientation = data['shapeorientation'][0]
    mirror = data['mirror'][0]
    
    # if "svg" in output:
    #     # Naming of output image
    #     if viewbox == True:
    #         dwg = svgwrite.Drawing(writedir + '/svg/' + str(len(imgs)+1).zfill(8) + 
    #                            '.svg', size = (max_x, max_y), viewBox = ('0 0 {} {}'.format(max_x, max_y)))
    #     
    #     else: 
    #         dwg = svgwrite.Drawing(writedir + '/svg/' + str(len(imgs)+1).zfill(8) + 
    #                            '.svg')
        
    if "svginline" in output:  
        # Naming of output image
        if viewbox == True:
            dwg = svgwrite.Drawing(size = (max_x, max_y), viewBox = ('0 0 {} {}'.format(max_x, max_y)))
        
        else: 
            dwg = svgwrite.Drawing()

    # BACKGROUND COLOR
#    dwg.add(dwg.rect(insert=(0, 0), size=('1530', '530'), rx=None, ry=None, fill='lightgrey'))

         
    # for every element in the grid:
    for i in range(len(data['shape'][0])):
        
        # mirror/translate if required
        
        no_mirror = " "
    
        mirror_horizontalvertical = str("scale(" + str(-1) + ", " + str(-1) + ")"+
                                    "translate(" + str(-2*x[i]) + ", " + str(-2*y[i]) + ")")
        mirror_horizontal = str("scale(" + str(-1) + ", " + str(1) + ")" +
                                "translate(" + str(-2*x[i]) + ", " + str(0) + ")" )            
        mirror_vertical = str("scale(" + str(1) + ", " + str(-1) + ")" +
                              "translate(" + str(0) + ", " + str(-2*y[i]) + ")")         
        
        if mirror[i] == "none":
            mirrortype = no_mirror
        elif mirror[i] == "horizontal":
            mirrortype = mirror_horizontal
        elif mirror[i]  == "vertical":
            mirrortype = mirror_vertical
        elif mirror[i]  == "horizontalvertical":
            mirrortype = mirror_horizontalvertical
        else:
            mirrortype = no_mirror
        
        # draw element shape 
        if elementshape[i] == "none":
        
            # NO SHAPE
            continue

            
        elif elementshape[i] == "circle":
        
            # CIRCLES
            dwg.add(dwg.circle(center=(str(x[i]),str(y[i])),
                r = str(size[i]/2), 
                fill = col[i],
                transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")" )
            )
        
        elif elementshape[i] == "ellipse":
        
            # ELLIPSES
            dwg.add(dwg.ellipse(center=(str(x[i]),str(y[i])),
                r = (str((xyratioshape[i]*size[i])/2), str(size[i]/2)), 
                fill = col[i],
                transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")" )  #'white')
            )
        
        elif elementshape[i] == "rectangle":
        
            # RECTANGLES
            dwg.add(dwg.rect((str(x[i] - (xyratioshape[i]*size[i])/2) , str(y[i] - size[i]/2)), (str(xyratioshape[i]*size[i]), str(size[i])),
                fill = col[i],
                transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
    
        elif elementshape[i] == "rounded_rectangle":
        
            # ROUNDED RECTANGLES
            dwg.add(dwg.rect((str(x[i] - (xyratioshape[i]*size[i])/2) , str(y[i] - size[i]/2)), (str(xyratioshape[i]*size[i]), str(size[i])),
                rx = 5, ry = 5, fill = col[i],
                transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
    
        
        elif elementshape[i] == "triangle":
               
            # EQUILATERAL TRIANGLES
            dwg.add(dwg.polygon(points = [(str(x[i]), str(y[i] - size[i]/2)), 
                                          (str(x[i] - (xyratioshape[i]*size[i])/2), str(y[i] + size[i]/2)), 
                                          (str(x[i] + (xyratioshape[i]*size[i])/2), str(y[i] + size[i]/2))], 
                                fill = col[i],
                                transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
        
        elif elementshape[i] == "curve":
               
            # CURVES
            dwg.add(dwg.path( d='M'+str(x[i] - size[i]/2)+','+ str(y[i] - (size[i]/4))+
                             ' C'+str(x[i] - size[i]/2 + size[i]/5)+ ','+ str(y[i]+(size[i]/4))+', '+
                             str(x[i] + size[i]/2 - size[i]/5)+', '+str(y[i]+(size[i]/4))+', '+
                             str(x[i] + size[i]/2)+','+ str(y[i] - (size[i]/4)),
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 12,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
        
        elif elementshape[i] == "infinity":
            
            # inspired by https://medium.com/@batkin/making-an-infinity-symbol-with-svg-6ec50cc8074d
               
            # CURVES
            dwg.add(dwg.path( d='M'+str(x[i] - (size[i]/4))+','+ str(y[i] - (size[i]/8))+' C'+str(x[i] - ((2/3)*size[i]))+ ','+ str(y[i] - (((2/3)*size[i])/2))+', '+str(x[i] - ((2/3)*size[i]))+', '+str(y[i] + (((2/3)*size[i])/2))+', '+str(x[i] - (size[i]/4))+','+ str(y[i] + (size[i]/8)),
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            dwg.add(dwg.path( d='M '+str(x[i] - (size[i]/4))+','+ str(y[i] - (size[i]/8))+' L'+str(x[i] + (size[i]/4))+ ','+ str(y[i] + (size[i]/8)),
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            dwg.add(dwg.path( d='M '+str(x[i] - (size[i]/4))+','+ str(y[i] + (size[i]/8))+' L'+str(x[i] + (size[i]/4))+ ','+ str(y[i] - (size[i]/8)),
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            dwg.add(dwg.path( d='M'+str(x[i] + (size[i]/4))+','+ str(y[i] - (size[i]/8))+' C'+str(x[i] + ((2/3)*size[i]))+ ','+ str(y[i] - (((2/3)*size[i])/2))+', '+str(x[i] + ((2/3)*size[i]))+', '+str(y[i] + (((2/3)*size[i])/2))+', '+str(x[i] + (size[i]/4))+','+ str(y[i] + (size[i]/8)),
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
    
        elif elementshape[i] == "flowerleave":
               
            # CURVES
            dwg.add(dwg.path( d='M'+str(x[i] - (size[i]/4))+','+ str(y[i] - (size[i]/8))+' C'+str(x[i] - ((2/3)*size[i]))+ ','+ str(y[i] - (((2/3)*size[i])/2))+', '+str(x[i] - ((2/3)*size[i]))+', '+str(y[i] + (((2/3)*size[i])/2))+', '+str(x[i] - (size[i]/4))+','+ str(y[i] + (size[i]/8))+
                             ' L' +str(x[i])+ ','+ str(y[i]) +
                             ' L' +str(x[i] - (size[i]/4))+','+ str(y[i] - (size[i]/8)),
                             
                    stroke = "none",
                    fill = col[i],
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            
        elif elementshape[i] == "flowerleavecontour":
               
            # CURVES
            dwg.add(dwg.path( d='M'+str(x[i] - (size[i]/4))+','+ str(y[i] - (size[i]/8))+' C'+str(x[i] - ((2/3)*size[i]))+ ','+ str(y[i] - (((2/3)*size[i])/2))+', '+str(x[i] - ((2/3)*size[i]))+', '+str(y[i] + (((2/3)*size[i])/2))+', '+str(x[i] - (size[i]/4))+','+ str(y[i] + (size[i]/8))+
                             ' L' +str(x[i])+ ','+ str(y[i]) +
                             ' L' +str(x[i] - (size[i]/4))+','+ str(y[i] - (size[i]/8)),
                             
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            
        elif elementshape[i] == "droplet":
               
            # CURVES
            dwg.add(dwg.path( d='M'+str(x[i] - (size[i]/4))+','+ str(y[i])+' C'+str(x[i] - ((2/3)*size[i]))+ ','+ str(y[i] + ((10/12)*size[i]))+', '+str(x[i] + ((2/3)*size[i]))+', '+str(y[i] + ((10/12)*size[i]))+', '+str(x[i] + (size[i]/4))+','+ str(y[i])+
                             ' L' + str(x[i]) + ','+ str(y[i] - (size[i]/2)) +
                             ' L'+str(x[i] - (size[i]/4))+','+ str(y[i]),
                    stroke = "none",
                    fill = col[i],
                    stroke_width = 1,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            
        elif elementshape[i] == "dropletcontour":
               
            # CURVES
            dwg.add(dwg.path( d='M'+str(x[i] - (size[i]/4))+','+ str(y[i])+' C'+str(x[i] - ((2/3)*size[i]))+ ','+ str(y[i] + ((10/12)*size[i]))+', '+str(x[i] + ((2/3)*size[i]))+', '+str(y[i] + ((10/12)*size[i]))+', '+str(x[i] + (size[i]/4))+','+ str(y[i])+
                             ' L' + str(x[i]) + ','+ str(y[i] - (size[i]/2)) +
                             ' L'+str(x[i] - (size[i]/4))+','+ str(y[i]),
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            
#        elif elementshape[i] == "text":
#            
#            text = txt[i]
#            dwg.add(dwg.text(text = text, insert = (str(x[i]-(xyratioshape[i]*size[i])/2),
#                                                      str(y[i]+size[i]/16)),
#                             fill = col[i],
#                             style = 'text-align = "middle";',
#                             textLength = str(size[i]),
#                             font_size = str(size[i]/4), font_weight = str(700), font_family = 'Trebuchet MS',
#                             transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
#            )
#                

#        elif elementshape[i] == "image":
#            
#            image = img[i]
#            dwg.add(dwg.image(href = image, insert = (str(x[i]-(xyratioshape[i]*size[i])/2),
#                                                      str(y[i]- size[i]/2)),
#                              size = (str(xyratioshape[i]*size[i]), str(size[i])),
#                              transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
#            )
                      
        elif elementshape[i].endswith(".svg"):
            dwg.add(dwg.image(href = elementshape[i], insert = (str(x[i]-(xyratioshape[i]*size[i])/2),
                                                      str(y[i]- size[i]/2)),
                              size = (str(xyratioshape[i]*size[i]), str(size[i])),
                              transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
        
        elif elementshape[i].endswith(".png"):
            dwg.add(dwg.image(href = elementshape[i], insert = (str(x[i]-(xyratioshape[i]*size[i])/2),
                                                      str(y[i]- size[i]/2)),
                              size = (str(xyratioshape[i]*size[i]), str(size[i])),
                              transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
        
        else:
            dwg.add(dwg.text(text = elementshape[i], insert = (str(x[i]-(xyratioshape[i]*size[i])/2),
                                                      str(y[i]+size[i]/16)),
                             fill = col[i],
                             style = 'text-align = "middle";',
                             textLength = str(size[i]),
                             font_size = str(size[i]/4), font_weight = str(700), font_family = 'Trebuchet MS',
                             transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
    # 
    # if "svg" in output:
    #     # write svg file to disk
    #     dwg.save()
    
    if "svginline" in output:
        # return svg
        return dwg.tostring()

### CREATE SVG FROM TXTDF
def create_pattern_fromtxt_inline(data, viewbox = True, 
                                   writedir = "OCTA_stimuli",
                                   output = ['svg', 'svgimage']): # choose 'svg', 'svgimage', 'svginline'
    
    # if 'svg' in output: 
    #     # If folder for .svg-files does not exist yet, create folder
    #     if not os.path.exists(writedir + '/svg/'):
    #         os.makedirs(writedir + '/svg/')
    #         
    #     # Get .svg img directory
    #     imgs = os.listdir(writedir + '/svg/') 
    
    data = pd.DataFrame(data)
    # Read parameter info from .txt file
    max_x = np.unique(data['max_x'][0])[0]
    max_y = np.unique(data['max_y'][0])[0]
    x = data['x']
    y = data['y']
    elementshape = data['shape']
#    img = list(data['elements'][0]['img'])
#    txt = list(data['elements'][0]['txt'])
    xyratioshape = data['xyratio'] 
    col = data['colour']
    size = data['size']
    shapeorientation = data['shapeorientation']
    mirror = data['mirror']
    
    # if "svg" in output:
    #     # Naming of output image
    #     if viewbox == True:
    #         dwg = svgwrite.Drawing(writedir + '/svg/' + str(len(imgs)+1).zfill(8) + 
    #                            '.svg', size = (max_x, max_y), viewBox = ('0 0 {} {}'.format(max_x, max_y)))
    #     
    #     else: 
    #         dwg = svgwrite.Drawing(writedir + '/svg/' + str(len(imgs)+1).zfill(8) + 
    #                            '.svg')
        
    if "svginline" in output:  
        # Naming of output image
        if viewbox == True:
            dwg = svgwrite.Drawing(size = (max_x, max_y), viewBox = ('0 0 {} {}'.format(max_x, max_y)))
        
        else: 
            dwg = svgwrite.Drawing()
            
    if "svgimage" in output:  
        # Naming of output image
        if viewbox == True:
            dwg = svgwrite.Drawing(size = (max_x, max_y), viewBox = ('0 0 {} {}'.format(max_x, max_y)))
        
        else: 
            dwg = svgwrite.Drawing()

    # BACKGROUND COLOR
#    dwg.add(dwg.rect(insert=(0, 0), size=('1530', '530'), rx=None, ry=None, fill='lightgrey'))

         
    # for every element in the grid:
    for i in range(len(data['shape'])):
        
        # mirror/translate if required
        
        no_mirror = " "
    
        mirror_horizontalvertical = str("scale(" + str(-1) + ", " + str(-1) + ")"+
                                    "translate(" + str(-2*x[i]) + ", " + str(-2*y[i]) + ")")
        mirror_horizontal = str("scale(" + str(-1) + ", " + str(1) + ")" +
                                "translate(" + str(-2*x[i]) + ", " + str(0) + ")" )            
        mirror_vertical = str("scale(" + str(1) + ", " + str(-1) + ")" +
                              "translate(" + str(0) + ", " + str(-2*y[i]) + ")")         
        
        if mirror[i] == "none":
            mirrortype = no_mirror
        elif mirror[i] == "horizontal":
            mirrortype = mirror_horizontal
        elif mirror[i]  == "vertical":
            mirrortype = mirror_vertical
        elif mirror[i]  == "horizontalvertical":
            mirrortype = mirror_horizontalvertical
        else:
            mirrortype = no_mirror
        
        # draw element shape 
        if elementshape[i] == "none":
        
            # NO SHAPE
            continue

            
        elif elementshape[i] == "circle":
        
            # CIRCLES
            dwg.add(dwg.circle(center=(str(x[i]),str(y[i])),
                r = str(size[i]/2), 
                fill = col[i],
                transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")" )
            )
        
        elif elementshape[i] == "ellipse":
        
            # ELLIPSES
            dwg.add(dwg.ellipse(center=(str(x[i]),str(y[i])),
                r = (str((xyratioshape[i]*size[i])/2), str(size[i]/2)), 
                fill = col[i],
                transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")" )  #'white')
            )
        
        elif elementshape[i] == "rectangle":
        
            # RECTANGLES
            dwg.add(dwg.rect((str(x[i] - (xyratioshape[i]*size[i])/2) , str(y[i] - size[i]/2)), (str(xyratioshape[i]*size[i]), str(size[i])),
                fill = col[i],
                transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
    
        elif elementshape[i] == "rounded_rectangle":
        
            # ROUNDED RECTANGLES
            dwg.add(dwg.rect((str(x[i] - (xyratioshape[i]*size[i])/2) , str(y[i] - size[i]/2)), (str(xyratioshape[i]*size[i]), str(size[i])),
                rx = 5, ry = 5, fill = col[i],
                transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
    
        
        elif elementshape[i] == "triangle":
               
            # EQUILATERAL TRIANGLES
            dwg.add(dwg.polygon(points = [(str(x[i]), str(y[i] - size[i]/2)), 
                                          (str(x[i] - (xyratioshape[i]*size[i])/2), str(y[i] + size[i]/2)), 
                                          (str(x[i] + (xyratioshape[i]*size[i])/2), str(y[i] + size[i]/2))], 
                                fill = col[i],
                                transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
        
        elif elementshape[i] == "curve":
               
            # CURVES
            dwg.add(dwg.path( d='M'+str(x[i] - size[i]/2)+','+ str(y[i] - (size[i]/4))+
                             ' C'+str(x[i] - size[i]/2 + size[i]/5)+ ','+ str(y[i]+(size[i]/4))+', '+
                             str(x[i] + size[i]/2 - size[i]/5)+', '+str(y[i]+(size[i]/4))+', '+
                             str(x[i] + size[i]/2)+','+ str(y[i] - (size[i]/4)),
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 12,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
        
        elif elementshape[i] == "infinity":
            
            # inspired by https://medium.com/@batkin/making-an-infinity-symbol-with-svg-6ec50cc8074d
               
            # CURVES
            dwg.add(dwg.path( d='M'+str(x[i] - (size[i]/4))+','+ str(y[i] - (size[i]/8))+' C'+str(x[i] - ((2/3)*size[i]))+ ','+ str(y[i] - (((2/3)*size[i])/2))+', '+str(x[i] - ((2/3)*size[i]))+', '+str(y[i] + (((2/3)*size[i])/2))+', '+str(x[i] - (size[i]/4))+','+ str(y[i] + (size[i]/8)),
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            dwg.add(dwg.path( d='M '+str(x[i] - (size[i]/4))+','+ str(y[i] - (size[i]/8))+' L'+str(x[i] + (size[i]/4))+ ','+ str(y[i] + (size[i]/8)),
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            dwg.add(dwg.path( d='M '+str(x[i] - (size[i]/4))+','+ str(y[i] + (size[i]/8))+' L'+str(x[i] + (size[i]/4))+ ','+ str(y[i] - (size[i]/8)),
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            dwg.add(dwg.path( d='M'+str(x[i] + (size[i]/4))+','+ str(y[i] - (size[i]/8))+' C'+str(x[i] + ((2/3)*size[i]))+ ','+ str(y[i] - (((2/3)*size[i])/2))+', '+str(x[i] + ((2/3)*size[i]))+', '+str(y[i] + (((2/3)*size[i])/2))+', '+str(x[i] + (size[i]/4))+','+ str(y[i] + (size[i]/8)),
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
    
        elif elementshape[i] == "flowerleave":
               
            # CURVES
            dwg.add(dwg.path( d='M'+str(x[i] - (size[i]/4))+','+ str(y[i] - (size[i]/8))+' C'+str(x[i] - ((2/3)*size[i]))+ ','+ str(y[i] - (((2/3)*size[i])/2))+', '+str(x[i] - ((2/3)*size[i]))+', '+str(y[i] + (((2/3)*size[i])/2))+', '+str(x[i] - (size[i]/4))+','+ str(y[i] + (size[i]/8))+
                             ' L' +str(x[i])+ ','+ str(y[i]) +
                             ' L' +str(x[i] - (size[i]/4))+','+ str(y[i] - (size[i]/8)),
                             
                    stroke = "none",
                    fill = col[i],
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            
        elif elementshape[i] == "flowerleavecontour":
               
            # CURVES
            dwg.add(dwg.path( d='M'+str(x[i] - (size[i]/4))+','+ str(y[i] - (size[i]/8))+' C'+str(x[i] - ((2/3)*size[i]))+ ','+ str(y[i] - (((2/3)*size[i])/2))+', '+str(x[i] - ((2/3)*size[i]))+', '+str(y[i] + (((2/3)*size[i])/2))+', '+str(x[i] - (size[i]/4))+','+ str(y[i] + (size[i]/8))+
                             ' L' +str(x[i])+ ','+ str(y[i]) +
                             ' L' +str(x[i] - (size[i]/4))+','+ str(y[i] - (size[i]/8)),
                             
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            
        elif elementshape[i] == "droplet":
               
            # CURVES
            dwg.add(dwg.path( d='M'+str(x[i] - (size[i]/4))+','+ str(y[i])+' C'+str(x[i] - ((2/3)*size[i]))+ ','+ str(y[i] + ((10/12)*size[i]))+', '+str(x[i] + ((2/3)*size[i]))+', '+str(y[i] + ((10/12)*size[i]))+', '+str(x[i] + (size[i]/4))+','+ str(y[i])+
                             ' L' + str(x[i]) + ','+ str(y[i] - (size[i]/2)) +
                             ' L'+str(x[i] - (size[i]/4))+','+ str(y[i]),
                    stroke = "none",
                    fill = col[i],
                    stroke_width = 1,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            
        elif elementshape[i] == "dropletcontour":
               
            # CURVES
            dwg.add(dwg.path( d='M'+str(x[i] - (size[i]/4))+','+ str(y[i])+' C'+str(x[i] - ((2/3)*size[i]))+ ','+ str(y[i] + ((10/12)*size[i]))+', '+str(x[i] + ((2/3)*size[i]))+', '+str(y[i] + ((10/12)*size[i]))+', '+str(x[i] + (size[i]/4))+','+ str(y[i])+
                             ' L' + str(x[i]) + ','+ str(y[i] - (size[i]/2)) +
                             ' L'+str(x[i] - (size[i]/4))+','+ str(y[i]),
                    stroke = col[i],
                    fill = "none",
                    stroke_width = 3,
                    transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            
#        elif elementshape[i] == "text":
#            
#            text = txt[i]
#            dwg.add(dwg.text(text = text, insert = (str(x[i]-(xyratioshape[i]*size[i])/2),
#                                                      str(y[i]+size[i]/16)),
#                             fill = col[i],
#                             style = 'text-align = "middle";',
#                             textLength = str(size[i]),
#                             font_size = str(size[i]/4), font_weight = str(700), font_family = 'Trebuchet MS',
#                             transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
#            )
#                

#        elif elementshape[i] == "image":
#            
#            image = img[i]
#            dwg.add(dwg.image(href = image, insert = (str(x[i]-(xyratioshape[i]*size[i])/2),
#                                                      str(y[i]- size[i]/2)),
#                              size = (str(xyratioshape[i]*size[i]), str(size[i])),
#                              transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
#            )
                      
        elif elementshape[i].endswith(".svg"):
            dwg.add(dwg.image(href = elementshape[i], insert = (str(x[i]-(xyratioshape[i]*size[i])/2),
                                                      str(y[i]- size[i]/2)),
                              size = (str(xyratioshape[i]*size[i]), str(size[i])),
                              transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
        
        elif elementshape[i].endswith(".png"):
            dwg.add(dwg.image(href = elementshape[i], insert = (str(x[i]-(xyratioshape[i]*size[i])/2),
                                                      str(y[i]- size[i]/2)),
                              size = (str(xyratioshape[i]*size[i]), str(size[i])),
                              transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
            
        elif elementshape[i].endswith(".jpg"):
            dwg.add(dwg.image(href = elementshape[i], insert = (str(x[i]-(xyratioshape[i]*size[i])/2),
                                                      str(y[i]- size[i]/2)),
                              size = (str(xyratioshape[i]*size[i]), str(size[i])),
                              transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
        
        else:
            dwg.add(dwg.text(text = elementshape[i], insert = (str(x[i]-(xyratioshape[i]*size[i])/2),
                                                      str(y[i]+size[i]/16)),
                             fill = col[i],
                             style = 'text-align = "middle";',
                             textLength = str(size[i]),
                             font_size = str(size[i]/4), font_weight = str(700), font_family = 'Trebuchet MS',
                             transform = mirrortype + "rotate(" + str(shapeorientation[i]) + ", " + str(x[i]) + " " + str(y[i]) + ")")
            )
    
    # if "svg" in output:
    #     # write svg file to disk
    #     dwg.save()
    
    if "svginline" in output:
        # return svg
        return dwg.tostring()
    
    if "svgimage" in output:
        # return svg
        return dwg
    
### CREATE INLINE .JSON & .SVG 
def create_pattern_inline(template = "grid",
                   shape = ['rectangle'], 
                   image = "none", #'../vector_images/hotdog.svg',
                   text = "none",
                   nrows = 5, ncols = 5,
                   startx = 30, starty = 30,
                   xdist = 30, ydist = 30,
                   shapemirror = ['none'],
                   orientation = [0],
                   shapecolour = ["blue"],
                   repeateachcolor = 1,
                   colourpattern = 'identity',
                   colourdim = 'element',
                   repeateachshape = 1,
                   shapepattern = 'identity',
                   shapedim = 'element',
                   repeateachshapeorientation = 1,
                   shapeorientationpattern = 'identity',
                   shapeorientationdim = 'element',
                   shapesize = [20],
                   shapexyratio = [1],
                   jitterscale = [0],
                   viewbox = True,
                   writedir = "OCTA_stimuli"):
    
    # Create json
    json = create_pattern_json(template,
                   shape, 
                   image, 
                   text,
                   nrows, ncols,
                   startx, starty,
                   xdist, ydist,
                   shapemirror,
                   orientation,
                   shapecolour,
                   repeateachcolor,
                   colourpattern,
                   colourdim,
                   repeateachshape,
                   shapepattern,
                   shapedim,
                   repeateachshapeorientation,
                   shapeorientationpattern,
                   shapeorientationdim,
                   shapesize,
                   shapexyratio,
                   jitterscale,
                   writedir,
                   output = ["json", "jsoninline"])
    
    # Create svg from json
    elements = json['elements']
    svg = create_pattern_fromjson_inline(elements, viewbox, writedir, output = "svginline")
    return svg
