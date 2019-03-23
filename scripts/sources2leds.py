#!/usr/bin/env python

import csv
import re
import numpy as np
import math

radiusAverage = 10 # All values within 10mm will be averaged into the LED value
lineNumber = []
spiXYZ = []
spiNames = []

# Read the list of LEDs and the line number of their location in the .spi file
with open('leds.csv', newline='') as ledsfile:
    ledsreader = csv.reader(ledsfile, delimiter="\t", quotechar='|')
    for row in ledsreader:
        if (len(row) >= 2):
            lineNumber.append(int(row[1]))
        else:
            print("ERROR READING LEDS file " + repr(row))


# Read the SPI file
with open('sources.spi', newline='') as spifile:
    spilines = spifile.readlines()
    for row in spilines:
        row2 = re.split('\s+', row)
        if len(row2) < 4:
            print("ERROR READING SPI file -> " + str(row))
            continue
        print (repr(row2))
        spiXYZ.append([float(row2[1]), float(row2[2]), float(row2[3])])
        spiNames.append(row2[3])


# Get XYZ for all LEDs
ledsXYZ = [spiXYZ[idx-1] for idx in lineNumber]
for led in ledsXYZ:
    print("LED at "+repr(led))
# Create matrix
matrix = []#np.zeros(len(lineNumber), len(spiXYZ))
matrix2 = []
# For each led, find the dipoles in a 10 mm radius
fDist = lambda p1, p2: math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
for led in ledsXYZ:
    matrix.append([float(fDist(led, p) < radiusAverage) for p in spiXYZ])
    matrix2.append([fDist(led, p) for p in spiXYZ])


# Normalize each line
matrix = np.asarray(matrix)
sums = matrix.sum(axis=1, keepdims=True)
matrix = matrix/sums

np.savetxt("sources2leds.csv", matrix, delimiter=",")
np.savetxt("sources2ledsDist.csv", matrix2, delimiter=",")
