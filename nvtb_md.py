#coding=utf-8

import os
import ase
from ase import units
from ase import io
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution as mb
#from ase.md import VelocityVerlet as vv
from ase.md.nvtberendsen import NVTBerendsen as NVTB
from amp import Amp
def generate_data(count, filename='cmd.traj'):
    """Generates test or training data with a simple MD simulation."""
    if os.path.exists(filename):
        return
    traj = io.Trajectory(filename, 'w')
    atoms = io.read('2.xyz')
    atoms.set_calculator(Amp.load('sio2.amp'))
    atoms.get_potential_energy()
    traj.write(atoms)
    mb(atoms, 300. * units.kB)
#    dyn = vv(atoms, dt=1. * units.fs, logfile='cmd.log')
    dyn = NVTB(atoms, timestep=0.5*units.fs, temperature=300, taut=2.0*units.fs, logfile='cmd.log')
    for step in range(count - 1):
        dyn.run(1)
        traj.write(atoms)
generate_data(2000)