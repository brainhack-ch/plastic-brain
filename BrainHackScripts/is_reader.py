#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PlasticBrain - Reads Cartool inverse problem file format.

Developed at the 2019 Brainhack Geneva event for the PlasticBrain project, runs on windows with a prerecorded file.
Participants : Manik Bhattacharjee,Victor Ferat, Italo Fernandes, Jelena, Gaetan, Elif, Jorge

Original project by Manik Bhattacharjee and Pierre Deman

"""


import struct
import numpy as np

def read_is(fname):
    iso = []
    for i in range(0,4):
        byte = f.read(1)
        iso.append(struct.unpack('c', byte)[0])
    byte = f.read(4)
    n_channel = struct.unpack('i', byte)[0]
    byte = f.read(4)
    numsolutionpoints = struct.unpack('i', byte)[0]
    byte = f.read(4)
    numregularizations = struct.unpack('i', byte)[0]
    byte = f.read(1)
    isinversescalar = struct.unpack('c', byte)[0]
    for k in range(0,n_channel):
        for i in range(0,32):
            byte = f.read(1)
            s = struct.unpack('c', byte)[0]

    for k in range(0,numsolutionpoints):
        for i in range(0,16):
            byte = f.read(1)
            s = struct.unpack('c', byte)[0]

    for k in range(0,numregularizations):
        byte = f.read(8)
        s = struct.unpack('d', byte)[0]

    for k in range(0,numregularizations):
        for i in range(0,32):
            byte = f.read(1)
            s = struct.unpack('c', byte)[0]
    regularisation_solutions = []
    for k in range(0,numregularizations):
        buf = f.read( 3 * numsolutionpoints * n_channel * 4 )
        data = np.frombuffer(buf, dtype=np.float32)
        data = data.reshape(3, numsolutionpoints, n_channel)
        regularisation_solutions.append(data)

    return(n_channel, numsolutionpoints, numregularizations, isinversescalar, regularisation_solutions)

if __name__ == '__main__':
    f = open("./Inverse Solution/MniNlinasyma/MniNlinasyma.Loreta.is", "rb")
    n_channel, numsolutionpoints, numregularizations, isinversescalar, regularisation_solutions = read_is(f)
    print(n_channel, numsolutionpoints, numregularizations, isinversescalar)
    print(len(regularisation_solutions))

