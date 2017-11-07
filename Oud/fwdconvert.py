# -*- coding: utf-8 -*-
"""

This script converts falling weight deflection data from the old format (.fwd) to the modern variant .F25. 
 
"""
__author__      = "Coen Smits"
__copyright__   = "Copyright 2017, Unihorn BV"
__credits__     = "Coen Smits"
__license__     = "GPL"
__version__     = "1.0.0"
__maintainer__  = "Coen Smits"
__email__       = "csmits@unihorn.nl"
__status__      = "under development"

def conversion( importfile, CROW_factor ):

    from datetime import datetime
    import math 
    import re
    import os
    
    # Open file
    file = open(importfile, 'r')
    lines = file.read().split('\n')
    
    # Get starting date of measurements
    datestring = lines[14].split('\t')[1]
    date = datetime.strptime(datestring, '%d/%m/%y').timestamp()
    filename = lines[7].split('\t')[1]
    filename = re.sub('.fwd$', '', filename)
    
    # Setup empty variables
    chainage = []
    lane = []
    longitude_raw = []
    lattitude_raw = []
    timestring = []
    time = []
    num_drops_raw = []
    num_drops = []
    drops = []
    #CROW_factor, last_Location = getDefaults()
    timestring2 = []
    longitudeSplitSpace = []
    lattitudeSplitSpace = []
    longitudeDegree = []
    lattitudeDegree = []
    longitudeDecimal = []
    lattitudeDecimal = []
    filePath = os.path.dirname(importfile)
    
    # Fill variables with measurement data
    for current_line in range(0, len(lines)):
        if lines[current_line] =='$2':
            chainage.append(lines[current_line+1].split('\t')[1])
            
            lane.append(lines[current_line+2].split('\t')[1])
            
            longitude_raw.append(lines[current_line+5].split('\t')[1])
            
            lattitude_raw.append(lines[current_line+5].split('\t')[2])
            
            num_drops_raw.append(lines[current_line+8].split('\t')[1])
            num_drops.append(num_drops_raw[len(num_drops_raw)-1].split(' ')[3])
            
            timestring.append(lines[current_line+8].split(' ')[6])
            
            for drop in range(0, int(num_drops[len(num_drops_raw)-1])):
                dropline = (str(len(num_drops_raw)) + '\t' + lines[current_line+drop+11])
                drops.append(dropline)
    
    for i in range(0,len(timestring)):
        timestring2.append('99/01/01 ' + timestring[i])
        time.append(datetime.strptime(timestring2[i], '%y/%m/%d %H:%M').timestamp()) 
        
        longitudeSplitSpace.append(longitude_raw[i].split(' '))
        lattitudeSplitSpace.append(lattitude_raw[i].split(' '))      
        
        if longitudeSplitSpace[i][1] == 'East' and lattitudeSplitSpace[i][1] == 'North':
            
            lattitudeDegree.append(lattitudeSplitSpace[i][2].replace('°', ','))
            lattitudeDegree[i]=lattitudeDegree[i].replace('\'',',')
            lattitudeDegree[i]=lattitudeDegree[i].replace('",','')
            
            longitudeDegree.append(longitudeSplitSpace[i][2].replace('°', ','))
            longitudeDegree[i]=longitudeDegree[i].replace('\'',',')
            longitudeDegree[i]=longitudeDegree[i].replace('",','')
            
        elif i > 0:
            lattitudeDegree.append(lattitudeDegree[i-1])
            longitudeDegree.append(longitudeDegree[i-1])
            
        else:
            lattitudeDegree.append('52,0,0')
            longitudeDegree.append('5,0,0')
       
    longitude = [[0 for x in range(3)] for y in range(len(longitude_raw))]
    lattitude = [[0 for x in range(3)] for y in range(len(lattitude_raw))] 
    
    for y in range (0,len(longitude_raw)):
        for x in range(0,3):
            longitude[y][x] = longitudeDegree[y].split(',')[x]
    
    for y in range (0,len(lattitude_raw)):
        for x in range(0,3):
            lattitude[y][x] = lattitudeDegree[y].split(',')[x]
            
    for i in range(0,len(longitude)):
        longitudeDecimal.append(float(longitude[i][0]) + float(longitude[i][1])/60 + float(longitude[i][2])/3600 )
        lattitudeDecimal.append(float(lattitude[i][0]) + float(lattitude[i][1])/60 + float(lattitude[i][2])/3600 )
    
    # Insert drops-strings in a 2D-array
    deflectiondata = [[0 for x in range(17)] for y in range(len(drops))]
    
    for y in range (0,len(drops)):
        for x in range(0,17):
            deflectiondata[y][x] = drops[y].split('\t')[x]
    
    # Close .fwd input file        
    file.close()
    
    # Create and open output .f25 file
    outputFileName = filePath + '\\' + filename + '.f25'
    fileF25 = open(outputFileName, 'w')
    
    # Write header into .f25 file
    file = open('includes\header.txt', 'r')
    headerLines = file.read().split('\n')
    
    for i in range(0, 31):
        fileF25.write('%s\n' % headerLines[i])
    
    fileF25.write('5031,"%-76s"\n' % filename)
    
    for i in range(32, len(headerLines)):
        fileF25.write('%s\n' % headerLines[i])
    
    # Write data into .f25 file
    dropRowPosition = 0
    for i in range(0, len(num_drops)):
        # Create the lines with loaction and temperature data
        fileF25.write('5280,0,     0,+%2.7f,+00%1.7f,91.7, 4, 10, 100,  0.9 \n' % (lattitudeDecimal[i], longitudeDecimal[i]) )
        
        if i > 1 and time[i] < time[i-1]:
            date = date+86400
        
        fileF25.write('5301,2,1,4,2,  %6s,1,1,"%s       ",20%s,%s,%s,%s,%s\n' % (chainage[i], lane[i], datetime.fromtimestamp(date).strftime('%y'), \
                                                                                 datetime.fromtimestamp(date).strftime('%m'), datetime.fromtimestamp(date).strftime('%d'), \
                                                                                 datetime.fromtimestamp(time[i]).strftime('%H'), datetime.fromtimestamp(time[i]).strftime('%M')))
        
        if lane[i] == 'R':
            fileF25.write('5302,0,0,A,p,0,0,1,0,\n')
        elif lane[i] == 'L':
            fileF25.write('5302,0,0,A,p,1,0,0,0,\n')    
        elif lane[i] == 'M':
            fileF25.write('5302,0,0,A,p,0,1,0,0,\n')
        else:
            fileF25.write('5302,0,0,A,p,0,1,0,0,\n')    
        
        for j in range(0,len(drops)):
            if int(deflectiondata[j][0]) == i+1:
                fileF25.write('5303,0,%5.1f,%5.1f,%5.1f\n' % (float(deflectiondata[j][15]), float(deflectiondata[j][14]), float(deflectiondata[j][13])))
                break
        
        # Create the lines with deflection data       
        for j in range(0,int(num_drops[i])):
            fileF25.write('  %2.0f, %5.0f,%4s.0,%4s.0,%4s.0,%4s.0,%4s.0,%4s.0,%4s.0,%4s.0,%4s.0, %5s0\n' % (j+1, float(deflectiondata[dropRowPosition][12])/(math.pi*0.15*0.15*CROW_factor), deflectiondata[dropRowPosition][2], \
                                                                                                                 deflectiondata[dropRowPosition][3], deflectiondata[dropRowPosition][4], deflectiondata[dropRowPosition][5], \
                                                                                                                 deflectiondata[dropRowPosition][6], deflectiondata[dropRowPosition][7], deflectiondata[dropRowPosition][8], \
                                                                                                                 deflectiondata[dropRowPosition][9], deflectiondata[dropRowPosition][10], deflectiondata[dropRowPosition][16] ))
            dropRowPosition+=1
            
    # Close output .f25 file
    fileF25.close()
    setNewDefaults(CROW_factor, filePath)

def getDefaults():
    defaultsFile = open("defaults.setup", 'r')
    defaultsLines = defaultsFile.read().split('\n')
    CROWfactor = float(defaultsLines[1])
    lastLocation = defaultsLines[4]
    defaultsFile.close()
    return CROWfactor, lastLocation

def setNewDefaults( CROWfactor, lastPath ):
    import os
    os.remove('defaults.setup')
    outputDefaults = 'defaults.setup'
    newOutputDefaults = open(outputDefaults, 'w')
    newOutputDefaults.write("\# CROW Factor:\n")
    newOutputDefaults.write(str(CROWfactor))
    newOutputDefaults.write(" \n")
    newOutputDefaults.write(" \n")
    newOutputDefaults.write("# Last used filepath: \n")
    newOutputDefaults.write(lastPath)   
    newOutputDefaults.write("\n")                 
    newOutputDefaults.close()