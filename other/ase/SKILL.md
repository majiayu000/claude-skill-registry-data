---
name: ase
description: ASE (Atomic Simulation Environment) - Python library for setting up, manipulating, and analyzing atomistic simulations. Use when working with molecular dynamics, DFT calculations, structure manipulation, or any atomistic modeling. Provides unified interface to multiple simulation codes (VASP, Quantum ESPRESSO, LAMMPS, GPAW, etc.).
metadata:
    skill-author: MindSpore Science Team
---

# ASE (Atomic Simulation Environment)

## Overview

ASE is a Python library for working with atoms and molecules. It provides tools for setting up, manipulating, and visualizing atomic structures, and interfaces with 40+ computational chemistry and materials science codes through a unified calculator API. ASE is released under the GNU Lesser General Public License (LGPL-3.0).

## When to Use This Skill

1. **DFT workflow setup and analysis** - Setting up calculations with VASP, Quantum ESPRESSO, GPAW, or other DFT codes
2. **Molecular dynamics simulations** - Running NVE, NVT, or NPT ensemble simulations with various thermostats
3. **Geometry optimization** - Relaxing atomic structures using BFGS, FIRE, or other optimization algorithms
4. **NEB calculations for reaction barriers** - Finding minimum energy paths and saddle points between states
5. **Surface calculations** - Building and analyzing surfaces, adsorption, and surface diffusion
6. **Vibrational analysis** - Computing vibrational modes, IR spectra, and Raman spectra
7. **Structure manipulation and file I/O** - Converting between file formats (CIF, POSCAR, XYZ, etc.)
8. **High-throughput computational workflows** - Batch processing with ASE database and calculator interfaces

## Installation

```bash
pip install ase

conda install -c conda-forge ase

git clone https://gitlab.com/ase/ase.git
cd ase && pip install -e .
```

## Quick Start

```python
from ase import Atoms
from ase.optimize import BFGS
from ase.calculators.emt import EMT

h2 = Atoms('H2', positions=[[0, 0, 0], [0, 0, 0.7]])
h2.calc = EMT()
opt = BFGS(h2)
opt.run(fmax=0.02)
print(h2.get_potential_energy())

from ase.io import write
write('H2.xyz', h2)
```

## Core Capabilities

### Calculator Interface

ASE provides unified interfaces to 40+ computational codes:

**DFT Codes:** VASP, Quantum ESPRESSO, ABINIT, GPAW, CP2K, CASTEP, FHI-aims, SIESTA, ORCA, Elk, exciting, FLEUR, CRYSTAL, Octopus, ONETEP, OpenMX, DMol3, DFTK, NWChem, Q-Chem, psi4, GAMESS-US, Gaussian, BigDFT

**Classical/ML Codes:** LAMMPS, Gromacs, Amber, EAM, EMT, Tersoff, DeePMD-kit, xtb, KIM, DFTB+, PLUMED, MOPAC

**Specialized:** Harmonic calculator, QMMM, SocketIO calculators, Checkpointing calculator

```python
from ase.calculators.vasp import Vasp
from ase.calculators.espresso import Espresso
from ase.calculators.lammpsrun import LAMMPS
from ase.calculators.gaussian import Gaussian

calc = Vasp(xc='PBE', encut=400, kpts=[4, 4, 4])
calc = Espresso(label='test', pseudopotentials={'Si': 'Si.pbe-n-rrkjus_psl.1.0.0.UPF'})
atoms.calc = calc
energy = atoms.get_potential_energy()
forces = atoms.get_forces()
stress = atoms.get_stress()
```

### Optimization Algorithms

Local optimizers: `BFGS`, `LBFGS`, `LBFGSLineSearch`, `QuasiNewton`, `FIRE`, `FIRE2`, `MDMin`, `GPMin`, `RFO`, `CellAwareBFGS`, `GoodOldQuasiNewton`

Global optimizers: `BasinHopping`, `MinimaHopping`

Preconditioned: `PreconLBFGS`, `PreconFIRE`

```python
from ase.optimize import BFGS, FIRE, LBFGS

opt = BFGS(atoms, trajectory='opt.traj')
opt.run(fmax=0.05)

opt = FIRE(atoms, trajectory='fire.traj')
opt.run(fmax=0.05)
```

### Molecular Dynamics

**NVE:** `VelocityVerlet`

**NVT:** `Langevin`, `NoseHooverChainNVT`, `Bussi`, `Andersen`, `NVTBerendsen`

**NPT:** `NPTBerendsen`, `MTKNPT`, `IsotropicMTKNPT`, `MelchionnaNPT`, `LangevinBAOAB`

```python
from ase.md import Langevin, VelocityVerlet, NPTBerendsen
from ase import units

dyn = Langevin(atoms, 1*units.fs, temperature_K=300, friction=0.01/units.fs)
dyn.run(1000)

dyn = VelocityVerlet(atoms, 2*units.fs, trajectory='md.traj')
dyn.run(5000)

dyn = NPTBerendsen(atoms, 1*units.fs, temperature_K=300, pressure=1.0*units.bar)
dyn.run(1000)
```

### NEB Calculations

Methods: `NEB`, `DyNEB` (dynamic/scaled optimization), `AutoNEB`

Interpolation: Linear, IDPP (Image Dependent Pair Potential)

```python
from ase.mep import NEB, DyNEB
from ase.optimize import FIRE, MDMin
from ase.calculators.emt import EMT

initial = bulk('Cu', 'fcc', a=3.6)
final = initial.copy()
final.translate([0.5, 0.5, 0.5])

images = [initial]
for i in range(5):
    image = initial.copy()
    image.calc = EMT()
    images.append(image)
images.append(final)

neb = NEB(images, climb=True)
neb.interpolate()
opt = FIRE(neb, trajectory='neb.traj')
opt.run(fmax=0.04)
```

### Vibrational Analysis

Modules: `Vibrations`, `Infrared`, `Raman`, `Franck-Condon`

```python
from ase.vibrations import Vibrations, Infrared

 vib = Vibrations(atoms)
 vib.run()
 vib.summary()

 ir = Infrared(atoms)
 ir.run()
 ir.summary()
```

## Key Modules

### Atoms Object

```python
from ase import Atoms
from ase.build import bulk, molecule, fcc111

atoms = bulk('Cu', 'fcc', a=3.6)
water = molecule('H2O')
slab = fcc111('Cu', size=(2, 2, 3), vacuum=10.0)

print(atoms.positions)
print(atoms.cell)
print(atoms.get_chemical_symbols())

atoms.translate([1, 0, 0])
atoms.rotate(90, 'z')
atoms.center()
```

### File I/O

```python
from ase.io import read, write

atoms = read('structure.cif')
atoms = read('POSCAR')
atoms = read('vasprun.xml')

atoms_list = read('trajectory.traj', index=':')

write('output.cif', atoms)
write('POSCAR', atoms, format='vasp')
write('trajectory.xyz', atoms_list)
```

### Band Structure & DOS

```python
from ase.dft.dos import DOS
from ase.dft.bandgap import bandgap

dos = DOS(calc, width=0.2, window=(-10, 10))
energies = dos.get_energies()
weights = dos.get_dos()

atoms = bulk('Si', 'diamond', a=5.43)
path = atoms.cell.bandpath('GXWK', density=20)
bs = calc.get_band_structure(path)
bs.plot()
```

## Common Workflows

### 1. DFT Structure Optimization Workflow

```python
from ase.build import bulk
from ase.calculators.vasp import Vasp
from ase.optimize import BFGS
from ase.io import write

atoms = bulk('Si', 'diamond', a=5.43)
atoms.calc = Vasp(xc='PBE', encut=400, kpts=[4, 4, 4])

opt = BFGS(atoms, trajectory='relax.traj')
opt.run(fmax=0.01)

write('relaxed_POSCAR', atoms, format='vasp')
print(f'Final energy: {atoms.get_potential_energy()} eV')
print(f'Lattice constant: {atoms.cell[0, 0]} Ang')
```

### 2. Surface Adsorption Calculation

```python
from ase.build import fcc111, add_adsorbate
from ase.calculators.emt import EMT
from ase.optimize import BFGS
from ase.io import write

slab = fcc111('Cu', size=(3, 3, 4), vacuum=10.0)
add_adsorbate(slab, 'H', height=1.5, position='ontop')
slab.calc = EMT()

opt = BFGS(slab, trajectory='ads.traj')
opt.run(fmax=0.05)

write('adsorption.xyz', slab)
energy_ads = slab.get_potential_energy()
```

### 3. NVT Molecular Dynamics Simulation

```python
from ase.build import bulk
from ase.calculators.emt import EMT
from ase.md import Langevin
from ase import units
from ase.io import Trajectory

atoms = bulk('Cu', 'fcc', a=3.6) * (4, 4, 4)
atoms.calc = EMT()

dyn = Langevin(atoms, timestep=5*units.fs, temperature_K=300, friction=0.01/units.fs)

traj = Trajectory('md.traj', 'w', atoms)
dyn.attach(traj.write, interval=100)

dyn.run(10000)
```

### 4. NEB Reaction Barrier Calculation

```python
from ase.build import molecule
from ase.mep import NEB
from ase.optimize import FIRE
from ase.calculators.emt import EMT

initial = molecule('H2')
initial.calc = EMT()
opt = FIRE(initial)
opt.run(fmax=0.05)

final = initial.copy()
final[1].position = [0, 0, 5]
final.calc = EMT()
opt = FIRE(final)
opt.run(fmax=0.05)

images = [initial]
for i in range(5):
    image = initial.copy()
    image.calc = EMT()
    images.append(image)
images.append(final)

neb = NEB(images)
neb.interpolate()
opt = FIRE(neb)
opt.run(fmax=0.05)
```

## Best Practices

1. **Use trajectory files** - Always save optimization/MD progress with `trajectory='file.traj'` for restart capability and analysis

2. **Choose appropriate optimizer** - Use `BFGS` or `LBFGS` for small systems, `FIRE` for large systems or climbing-image NEB; avoid `BFGSLineSearch` with NEB

3. **Set proper convergence criteria** - Use `fmax=0.01-0.05 eV/Ang` for geometry optimization; tighter for vibrational calculations

4. **Thermalize before production MD** - Run equilibration before collecting data; use `MaxwellBoltzmannDistribution()` to set initial velocities

5. **Optimize endpoints before NEB** - Always fully relax initial and final states before NEB calculation

6. **Use IDPP interpolation for NEB** - `idpp_interpolate()` provides better initial guesses than linear interpolation for complex reactions

## Troubleshooting

1. **Optimizer not converging** - Try switching optimizer (FIRE instead of BFGS), check for unreasonable starting geometry, reduce `fmax` requirement

2. **MD energy blowing up** - Reduce timestep (use 1-2 fs for H-containing systems), check initial geometry, verify calculator forces are reasonable

3. **NEB not finding saddle point** - Ensure endpoints are properly relaxed, use `climb=True` after initial relaxation, try `idpp_interpolate()`, increase number of images

4. **Calculator not working** - Verify calculator executable is in PATH, check pseudopotential/settings files exist, use `SocketIOCalculator` for long-running calculations

5. **File format issues** - Check format-specific options in docs; `read('file', format='vasp')` may help with ambiguous formats

## GUI Tool

```bash
ase gui structure.cif
ase gui trajectory.traj
ase gui --help
```

## Command Line

```bash
ase convert input.cif output.xyz
ase info structure.cif
ase build bulk Cu fcc a=3.6 > Cu.cif
ase nebplot neb.traj
```

## Resources

- Official Documentation: https://wiki.fysik.dtu.dk/ase (or https://ase-lib.org)
- Tutorials: https://wiki.fysik.dtu.dk/ase/tutorials.html
- GitLab: https://gitlab.com/ase/ase
- MatSci Forum: https://matsci.org/ase
- Language: Python
- License: LGPL-3.0

## Citation

```txt
A. H. Larsen, J. J. Mortensen, J. Blomqvist, I. E. Castelli, R. Christensen,
M. Dułak, J. Friis, M. N. Groves, B. Hammer, C. Hargus, E. D. Hermes,
P. C. Jennings, P. B. Jensen, J. Kermode, J. R. Kitchin, E. L. Kolsbjerg,
J. Kubal, K. Kaasbjerg, S. Lysgaard, J. B. Maronsson, T. Maxson,
T. Olsen, L. Pastewka, A. Peterson, C. Rostgaard, J. Schiøtz, O. Schütt,
M. Strange, K. S. Thygesen, T. Vegge, L. Vilhelmsen, M. Walter,
Z. Zeng, K. W. Jacobsen. The Atomic Simulation Environment—A Python
library for working with atoms. J. Phys.: Condens. Matter 29, 273002 (2017).
```