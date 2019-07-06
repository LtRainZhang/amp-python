#!/usr/bin/env python
# coding=utf-8

"""
@author: Yingchun Zhang
@e-mail: yczhang@smail.nju.edu.cn
@time: 2019/6/11 13:32
@org: Nanjing University
"""
from ase import io
import numpy as np

dirName = r'./'
initialStructure = '64w-equied.xyz'
initialTrj = 'test.xyz'


def generateStructureFromOneConfiguration(initialStructure, nFrames=1000, maxDistance=0.5, cell=(10, 10, 10),
                                          pbc="T T T"):
    maxDistance = np.power(maxDistance, 1.0/3.0)
    image = io.read(initialStructure)
    # image.cell = cell
    # image.set_pbc((1, 1, 1))
    nAtoms = len(image)
    with open(initialStructure.split('.')[0] + '-generated-%d.xyz' % nFrames, 'w') as foo:
        print(nAtoms, file=foo)
        print('Lattice="%f 0.0 0.0 0.0 %f 0.0 0.0 0.0 %f" Properties=species:S:1:pos:R:3 pbc="%s"' % (
            cell[0], cell[1], cell[2], pbc), file=foo)
        for iatom in range(nAtoms):
            print('%s %15.8f %15.8f %15.8f' % (image[iatom].symbol, image[iatom].x, image[iatom].y, image[iatom].z),
                  file=foo)
        for iframe in range(nFrames):
            image1 = image.copy()
            image1.set_positions(image.positions + maxDistance * (np.random.random((nAtoms, 3))-0.5))
            # io.write(foo, image1, format='extxyz')
            print(nAtoms, file=foo)
            print('Lattice="%f 0.0 0.0 0.0 %f 0.0 0.0 0.0 %f" Properties=species:S:1:pos:R:3 pbc="%s"' % (
                cell[0], cell[1], cell[2], pbc),
                  file=foo)
            for iatom in range(nAtoms):
                print('%s %15.8f %15.8f %15.8f' % (
                    image1[iatom].symbol, image1[iatom].x, image1[iatom].y, image1[iatom].z), file=foo)


def generateStructureFromTraj(initialTraj, slice=':', nStructuresPerFrame=5, maxDistance=0.5, cell=(9.832, -4.916, 8.515, 10.811),
                              pbc="T T T", shift=(0, 0, 0)):
    trj = io.read(initialTraj, index=slice)
    maxDistance = np.power(maxDistance, 1.0/3.0)
    with open('generated-%d.xyz' % nStructuresPerFrame, 'w') as foo:
        for x, image in enumerate(trj):
            if x % 10 == 0:
                print('Frame: %d' % x)
            # image.cell = cell
            # image.set_pbc((1, 1, 1))
            nAtoms = len(image)
            # io.write(foo, image, format='xyz')
            print(nAtoms, file=foo)
            print('Lattice="%f 0.0 0.0 %f %f 0.0 0.0 0.0 %f" Properties=species:S:1:pos:R:3 pbc="%s"' % (
                cell[0], cell[1], cell[2], cell[3], pbc),
                  file=foo)
            for iatom in range(nAtoms):
                print('%s %15.8f %15.8f %15.8f' % (
                    image[iatom].symbol, image[iatom].x + shift[0], image[iatom].y + shift[1],
                    image[iatom].z + shift[2]),
                      file=foo)

            for iframe in range(nStructuresPerFrame):
                # image1 = image.copy()
                # image1.set_positions(image.positions + maxDistance * np.random.random((nAtoms, 3)))
                # io.write(foo, image1, format='extxyz')
                image1 = image.copy()
                image1.set_positions(image.positions + maxDistance * (np.random.random((nAtoms, 3))-0.5))  # produce the matrix with nAtoms row and 3 column between 0 and 1.0 with uniform distribution
                print(nAtoms, file=foo)
                print('Lattice="%f 0.0 0.0 %f %f 0.0 0.0 0.0 %f" Properties=species:S:1:pos:R:3 pbc="%s"' % (
                    cell[0], cell[1], cell[2], cell[3], pbc),
                      file=foo)
                for iatom in range(nAtoms):
                    print('%s %15.8f %15.8f %15.8f' % (
                        image1[iatom].symbol, image1[iatom].x + shift[0], image1[iatom].y + shift[1],
                        image1[iatom].z + shift[2]), file=foo)


# generateStructureFromOneConfiguration(dirName + initialStructure, nFrames=100, maxDistance=0.5, cell=(12.43, 12.43, 12.43))
generateStructureFromTraj(dirName + initialTrj, slice='1:', nStructuresPerFrame=2, maxDistance=0.5,
                          cell=(9.832, -4.916, 8.515, 10.811), pbc="F F F", shift=(0,0,0))
