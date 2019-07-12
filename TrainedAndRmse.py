#!/usr/bin/env python
# coding=utf-8

"""
@author: Yingchun Zhang
@e-mail: yczhang@smail.nju.edu.cn
@time: 2019/6/14 21:36
@org: Nanjing University
"""
from ase import io
from amp import Amp
from amp.descriptor.gaussian import Gaussian
from amp.model.neuralnetwork import NeuralNetwork
from amp.model import LossFunction
import numpy as np

dirName = './'
x = io.read(dirName + '../../traj/' + 'train.traj',index=':')[200:400]
#y = io.read(dirName + '../' + 'h3o-spe-1.traj', index=':')[50:100]
test_images = x
nimages = len(test_images)
test_energy = [image.get_potential_energy() for image in test_images]
rmse = []
for namp in range(100,1500,100):
    print('Current amp parameters: %d'%namp)
    calc = Amp.load(dirName + 'checkpoint/'+'%d.amp'%namp, cores=1)
    nnp_energy = [calc.get_potential_energy(image) for image in test_images]
    testfile = open(dirName + 'trained-%d.dat'%namp,'w')
    for i in range(nimages):
        print('%15.8f %15.8f'%(test_energy[i], nnp_energy[i]), file=testfile)
    testfile.close()
    rmse.append(np.sqrt(np.sum((np.array(test_energy) - np.array(nnp_energy)))**2*1.0/nimages))

with open(dirName + 'trained-rmse.dat', 'w') as foo:
    for i, value in enumerate(rmse):
        print('%5d %15.8f'%((i+1)*100,value), file=foo)
