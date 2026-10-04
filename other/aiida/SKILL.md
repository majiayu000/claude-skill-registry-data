---
name: aiida
description: AiiDA (Automated Infrastructure and Database for Ab-initio Design) - Python framework for managing and preserving computational workflows and data. Use when managing computational materials science workflows, tracking calculation provenance, automating DFT/MD simulations, or building reproducible research pipelines. Supports plugins for VASP, Quantum ESPRESSO, CP2K, and many other codes.
metadata:
    skill-author: MindSpore Science Team
---

# AiiDA

## Overview

AiiDA is a Python framework for automating, managing, and preserving computational workflows in materials science. It provides automatic provenance tracking, workflow orchestration, and data management with a focus on reproducibility.

## When to Use This Skill

Use this skill when you need to:

1. **Track computational provenance** - Automatically record inputs, outputs, and metadata for all calculations to ensure reproducibility
2. **Automate DFT/MD simulations** - Run high-throughput calculations with Quantum ESPRESSO, VASP, CP2K, or other codes
3. **Build reproducible research pipelines** - Create self-documenting workflows that can be shared and re-executed
4. **Manage HPC workflows** - Submit and monitor jobs on clusters with SLURM, PBS, SGE, or LSF schedulers
5. **Query calculation results** - Search through thousands of calculations using the provenance graph database
6. **Develop simulation plugins** - Create interfaces for new simulation codes with input generation and output parsing
7. **Share research data** - Export provenance graphs for publication on Materials Cloud or with collaborators
8. **Handle complex workflow logic** - Implement iterative convergence loops, error recovery, and conditional execution

## Installation

### Basic Installation

```bash
pip install aiida-core
```

### With Optional Dependencies

```bash
pip install aiida-core[atomic_tools,docs,pre-commit,rest,ssh]
```

### Quick Setup (Profile Creation)

```bash
verdi profile setup core.sqlite_dos --profile-name quicksetup --dbname aiida_db

verdi profile setup core.psql_dos --profile-name myprofile --dbname aiida_db --dbuser aiida --dbpassword secret

verdi profile setdefault myprofile
```

### Verify Installation

```bash
verdi status
verdi profile list
```

## Quick Start Examples

### Creating Structures

```python
from aiida import orm

structure = orm.StructureData(cell=[[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 4.0]])
structure.append_atom(position=(0.0, 0.0, 0.0), symbols='Si')
structure.append_atom(position=(2.0, 2.0, 2.0), symbols='Si')
structure.store()
print(f"Stored structure with PK: {structure.pk}")

from ase.build import bulk
ase_atoms = bulk('Si', 'diamond', a=5.43)
structure = orm.StructureData(ase=ase_atoms)
structure.store()
```

### Loading and Using Existing Data

```python
from aiida import orm

structure = orm.load_node(pk=123)
print(f"Loaded: {structure.label}")
print(f"Formula: {structure.get_formula()}")
print(f"Volume: {structure.get_cell_volume()}")

qb = orm.QueryBuilder()
qb.append(orm.StructureData, filters={'extras.formula': 'Si2'})
for (node,) in qb.iterall():
    print(f"Found structure: {node.pk}")
```

### Running Calculations

```python
from aiida import orm, engine
from aiida.calculations import CalculationFactory

code = orm.load_code('qe-pw@localhost')
builder = code.get_builder()

builder.structure = structure
builder.parameters = orm.Dict(dict={
    'CONTROL': {'calculation': 'scf'},
    'SYSTEM': {'ecutwfc': 30.0, 'ecutrho': 240.0},
    'ELECTRONS': {'conv_thr': 1.0e-6}
})
builder.settings = orm.Dict(dict={})
builder.metadata.options = {
    'resources': {'num_machines': 1},
    'max_wallclock_seconds': 3600,
}

result = engine.submit(builder)
print(f"Submitted calculation: {result}")
```

### Using calcfunction for Automatic Provenance

```python
from aiida import orm
from aiida.engine import calcfunction, run

@calcfunction
def create_diamond_structure(element: orm.Str, lattice: orm.Float) -> orm.StructureData:
    from ase.build import bulk
    atoms = bulk(element.value, 'diamond', a=lattice.value)
    return orm.StructureData(ase=atoms)

@calcfunction
def calculate_properties(structure: orm.StructureData) -> orm.Dict:
    import numpy as np
    volume = structure.get_cell_volume()
    cell = structure.cell
    lattice_params = {
        'a': np.linalg.norm(cell[0]),
        'b': np.linalg.norm(cell[1]),
        'c': np.linalg.norm(cell[2]),
        'volume': volume
    }
    return orm.Dict(dict=lattice_params)

structure = create_diamond_structure(orm.Str('Si'), orm.Float(5.43))
props = calculate_properties(structure)
print(f"Properties: {props.dict}")
```

### Querying Data

```python
from aiida import orm

qb = orm.QueryBuilder()
qb.append(orm.StructureData, tag='structure')
qb.append(orm.CalcFunctionNode, with_incoming='structure', tag='calc')
results = qb.all()

for structure, calc in results:
    print(f"Structure PK: {structure.pk}, Calculation PK: {calc.pk}")

qb = orm.QueryBuilder()
qb.append(orm.StructureData, filters={'extras.tag': 'high-throughput'})
qb.append(orm.Dict, with_outgoing=orm.StructureData)
for structure, params in qb.iterall():
    print(f"{structure.label}: {params.dict}")
```

## Best Practices

### Profile Management

```python
import aiida
from aiida import orm

aiida.load_profile('myprofile')

verdi profile setup core.psql_dos --profile-name production --dbname aiida_prod

verdi profile list
verdi profile setdefault production

from aiida.manage.configuration import get_config
config = get_config()
profile = config.get_profile('myprofile')
print(profile.dictionary)

verdi profile delete --force old_profile
```

**Best practices:**
- Use PostgreSQL for production; SQLite is suitable for testing
- Create separate profiles for different projects
- Set meaningful profile names that reflect their purpose
- Regularly backup your profile configuration
- Use environment variables for database credentials in production

### Data Provenance

```python
from aiida import orm
from aiida.engine import calcfunction, workfunction

@calcfunction
def normalize_structure(structure: orm.StructureData) -> orm.StructureData:
    from ase.build import niggli_reduce
    ase_atoms = structure.get_ase()
    niggli_reduce(ase_atoms)
    return orm.StructureData(ase=ase_atoms)

@workfunction
def analyze_convergence(structures: orm.List) -> orm.Dict:
    energies = []
    for struct_pk in structures:
        struct = orm.load_node(struct_pk)
        qb = orm.QueryBuilder()
        qb.append(orm.Dict, with_incoming=struct, project=['attributes.energy'])
        result = qb.first()
        if result:
            energies.append(result[0])
    return orm.Dict(dict={'energies': energies, 'converged': len(energies) == len(structures)})

structure.label = 'Silicon diamond structure'
structure.description = 'Created from ASE bulk builder with a=5.43 Angstrom'
structure.set_extra('material_type', 'semiconductor')
structure.set_extra('creator', 'my_username')
```

**Best practices:**
- Always use `@calcfunction` or `@workfunction` decorators for functions that create data
- Store all calculation inputs as AiiDA nodes, not Python objects
- Use labels and descriptions for important nodes
- Add extras for searchable metadata that won't affect provenance
- Never modify stored nodes - create new versions instead

### Workflow Design

```python
from aiida import orm
from aiida.engine import WorkChain, ToContext, calcfunction

class ConvergedWorkflow(WorkChain):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input('structure', valid_type=orm.StructureData)
        spec.input('code', valid_type=orm.Code)
        spec.input('cutoffs', valid_type=orm.List, default=lambda: orm.List(list=[20, 30, 40]))
        spec.outline(
            cls.setup,
            cls.run_calculations,
            cls.check_convergence,
            cls.finalize,
        )
        spec.output('final_energy', valid_type=orm.Float)
        spec.exit_code(100, 'ERROR_NO_CONVERGENCE', message='No converged calculation found')

    def setup(self):
        self.ctx.energies = []
        self.ctx.converged = False

    def run_calculations(self):
        from aiida.engine import submit
        for cutoff in self.inputs.cutoffs:
            builder = self.inputs.code.get_builder()
            builder.structure = self.inputs.structure
            builder.parameters = orm.Dict(dict={'ecutwfc': cutoff})
            future = self.submit(builder)
            key = f'calc_{cutoff}'
            self.to_context(**{key: future})

    def check_convergence(self):
        for key, value in self.ctx.items():
            if key.startswith('calc_'):
                calc = value
                if calc.is_finished_ok:
                    energy = calc.outputs.output_parameters['energy']
                    self.ctx.energies.append((key, energy))

    def finalize(self):
        if self.ctx.energies:
            self.ctx.energies.sort(key=lambda x: x[1])
            self.out('final_energy', orm.Float(self.ctx.energies[0][1]))
        else:
            return self.exit_codes.ERROR_NO_CONVERGENCE
```

**Best practices:**
- Use `WorkChain` instead of functions for complex multi-step workflows
- Define inputs with `valid_type` for automatic validation
- Use `spec.outline()` for clear workflow structure
- Implement error handling with exit codes
- Use `ToContext` for managing asynchronous calculations
- Keep workflows modular and reusable

### Query Optimization

```python
from aiida import orm

qb = orm.QueryBuilder()
qb.append(orm.StructureData, project=['id'])
structures = [r[0] for r in qb.all()]

qb = orm.QueryBuilder()
qb.append(orm.CalcJobNode,
    filters={
        'attributes.exit_status': 0,
        'ctime': {'>=': '2024-01-01'},
    },
    project=['id']
)
for (pk,) in qb.iterall():
    pass

qb = orm.QueryBuilder()
qb.append(orm.StructureData, tag='s')
qb.append(orm.CalcJobNode, with_incoming='s', tag='c')
qb.append(orm.Dict, with_incoming='c', tag='d')
results = qb.distinct().all()

qb = orm.QueryBuilder()
qb.append(orm.Node,
    filters={'node_type': {'like': 'data.structure.%'}},
    project=['id', 'label', 'ctime']
)
qb.order_by({orm.Node: {'ctime': 'desc'}})
qb.limit(100)
```

**Best practices:**
- Use `iterall()` instead of `all()` for large result sets
- Project only the fields you need
- Use specific node types instead of generic `Node`
- Apply filters early in the query to reduce result size
- Use `distinct()` to avoid duplicate results in joins
- Set `limit()` for exploratory queries on large databases

## Troubleshooting

### Profile Issues

```bash
verdi profile list
verdi status

verdi profile setup core.sqlite_dos --profile-name new_profile

verdi profile setdefault correct_profile

rm -rf ~/.aiida
verdi setup
```

**Common issues:**
- `ProfileNotFoundError`: Check profile exists with `verdi profile list`
- Database connection errors: Verify PostgreSQL is running and credentials are correct
- Permission denied: Check file permissions on `.aiida` directory

### Daemon Problems

```bash
verdi daemon status
verdi daemon start
verdi daemon stop
verdi daemon restart

verdi daemon incr 4

verdi process list -p 1
verdi process report <PID>
```

**Common issues:**
- Daemon not starting: Check `verdi daemon log` for errors
- Stuck processes: Use `verdi process kill <PID>` to terminate
- Memory issues: Reduce worker count with `verdi daemon stop && verdi daemon start --workers 2`

### Calculation Failures

```python
from aiida import orm

calc = orm.load_node(pk=123)
print(calc.exit_status)
print(calc.exit_message)

print(calc.process_state)

for key, value in calc.outputs.items():
    print(f"{key}: {value}")

verdi process report 123
verdi process show 123
```

**Common issues:**
- `exit_status != 0`: Check `verdi process report` for error details
- Missing outputs: Parser may have failed, check retrieved files
- Timeout errors: Increase `max_wallclock_seconds` in metadata options

### Database Performance

```bash
verdi database integrity detect-duplicate-uuid

verdi database migrate

verdi storage maintain --dry-run
verdi storage maintain
```

**Common issues:**
- Slow queries: Create database indexes, use more specific filters
- Database corruption: Run `verdi database integrity` commands
- Large database: Archive old data with `verdi export create`

### Import/Export Issues

```bash
verdi export create -N 123,456,789 output.aiida

verdi import archive.aiida

verdi export inspect archive.aiida
```

**Common issues:**
- Import conflicts: Use `--ignore_unknown_nodes` flag
- Large exports: Use entity filters to reduce size
- Version mismatch: Check AiiDA version compatibility

## Common Workflows

### Structure Relaxation Workflow

```python
from aiida import orm
from aiida.engine import WorkChain, calcfunction, run

@calcfunction
def check_forces(output_params: orm.Dict, threshold: orm.Float) -> orm.Bool:
    forces = output_params['forces']
    max_force = max(abs(f) for f in forces)
    return orm.Bool(max_force < threshold.value)

class StructureRelaxationWorkChain(WorkChain):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input('structure', valid_type=orm.StructureData)
        spec.input('code', valid_type=orm.Code)
        spec.input('max_iterations', valid_type=orm.Int, default=lambda: orm.Int(5))
        spec.input('force_threshold', valid_type=orm.Float, default=lambda: orm.Float(0.01))
        spec.outline(
            cls.setup,
            cls.relax_loop,
            cls.finalize,
        )
        spec.output('relaxed_structure', valid_type=orm.StructureData)
        spec.output('total_energy', valid_type=orm.Float)
        spec.exit_code(101, 'ERROR_MAX_ITERATIONS', message='Maximum iterations reached without convergence')

    def setup(self):
        self.ctx.iteration = 0
        self.ctx.current_structure = self.inputs.structure
        self.ctx.converged = False

    def relax_loop(self):
        from aiida.engine import while_
        return while_(self.should_continue)(
            self.run_relaxation,
            self.check_convergence,
        )

    def should_continue(self):
        return not self.ctx.converged and self.ctx.iteration < self.inputs.max_iterations.value

    def run_relaxation(self):
        self.ctx.iteration += 1
        builder = self.inputs.code.get_builder()
        builder.structure = self.ctx.current_structure
        builder.parameters = orm.Dict(dict={
            'CONTROL': {'calculation': 'vc-relax'},
            'SYSTEM': {'ecutwfc': 30.0},
        })
        builder.metadata.options = {
            'resources': {'num_machines': 1},
            'max_wallclock_seconds': 3600,
        }
        self.to_context(relax_calc=self.submit(builder))

    def check_convergence(self):
        calc = self.ctx.relax_calc
        if calc.is_finished_ok:
            self.ctx.current_structure = calc.outputs.output_structure
            converged = check_forces(calc.outputs.output_parameters, self.inputs.force_threshold)
            self.ctx.converged = converged.value
        else:
            self.report(f'Relaxation iteration {self.ctx.iteration} failed')

    def finalize(self):
        self.out('relaxed_structure', self.ctx.current_structure)
        if not self.ctx.converged:
            return self.exit_codes.ERROR_MAX_ITERATIONS

result = run(
    StructureRelaxationWorkChain,
    structure=input_structure,
    code=code,
    max_iterations=orm.Int(10),
)
```

### Band Structure Calculation Workflow

```python
from aiida import orm
from aiida.engine import WorkChain, run

class BandStructureWorkChain(WorkChain):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input('structure', valid_type=orm.StructureData)
        spec.input('code', valid_type=orm.Code)
        spec.input('parameters', valid_type=orm.Dict, required=False)
        spec.outline(
            cls.run_scf,
            cls.run_bands,
            cls.finalize,
        )
        spec.output('band_structure', valid_type=orm.BandsData)
        spec.output('fermi_energy', valid_type=orm.Float)

    def run_scf(self):
        builder = self.inputs.code.get_builder()
        builder.structure = self.inputs.structure
        builder.parameters = self.inputs.parameters or orm.Dict(dict={
            'CONTROL': {'calculation': 'scf'},
            'SYSTEM': {'ecutwfc': 30.0},
        })
        self.to_context(scf_calc=self.submit(builder))

    def run_bands(self):
        scf_calc = self.ctx.scf_calc
        if not scf_calc.is_finished_ok:
            self.report('SCF calculation failed')
            return

        builder = self.inputs.code.get_builder()
        builder.structure = self.inputs.structure
        builder.parameters = orm.Dict(dict={
            'CONTROL': {'calculation': 'bands'},
            'SYSTEM': {'ecutwfc': 30.0},
        })
        builder.parent_folder = scf_calc.outputs.remote_folder

        kpoints = orm.KpointsData()
        kpoints.set_cell(self.inputs.structure.cell)
        kpoints.set_kpoints_path([
            ('GAMMA', 0, [0, 0, 0]),
            ('X', 10, [0.5, 0, 0]),
            ('M', 10, [0.5, 0.5, 0]),
            ('GAMMA', 10, [0, 0, 0]),
        ])
        builder.kpoints = kpoints

        self.to_context(bands_calc=self.submit(builder))

    def finalize(self):
        bands_calc = self.ctx.bands_calc
        if bands_calc.is_finished_ok:
            self.out('band_structure', bands_calc.outputs.band_structure)
            self.out('fermi_energy', bands_calc.outputs.fermi_energy)

result = run(
    BandStructureWorkChain,
    structure=silicon_structure,
    code=code,
)
```

### High-Throughput Screening Workflow

```python
from aiida import orm
from aiida.engine import WorkChain, run, submit

class HighThroughputScreeningWorkChain(WorkChain):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input('structures', valid_type=orm.List)
        spec.input('code', valid_type=orm.Code)
        spec.input('base_parameters', valid_type=orm.Dict)
        spec.outline(
            cls.launch_calculations,
            cls.collect_results,
        )
        spec.output('results', valid_type=orm.Dict)

    def launch_calculations(self):
        self.ctx.calc_pks = []
        for idx, struct_pk in enumerate(self.inputs.structures):
            structure = orm.load_node(struct_pk)
            builder = self.inputs.code.get_builder()
            builder.structure = structure
            builder.parameters = self.inputs.base_parameters
            builder.metadata.label = f'screening_calc_{idx}'
            builder.set_extra('screening_batch', self.uuid)
            calc = self.submit(builder)
            self.ctx.calc_pks.append(calc.pk)
            self.to_context(**{f'calc_{idx}': calc})

    def collect_results(self):
        results = {}
        for idx, pk in enumerate(self.ctx.calc_pks):
            calc = orm.load_node(pk)
            if calc.is_finished_ok:
                energy = calc.outputs.output_parameters['energy']
                results[f'structure_{idx}'] = {
                    'pk': pk,
                    'energy': energy,
                    'status': 'success',
                }
            else:
                results[f'structure_{idx}'] = {
                    'pk': pk,
                    'status': 'failed',
                    'exit_status': calc.exit_status,
                }
        self.out('results', orm.Dict(dict=results))

structure_pks = orm.List(list=[101, 102, 103, 104, 105])
result = submit(
    HighThroughputScreeningWorkChain,
    structures=structure_pks,
    code=code,
    base_parameters=orm.Dict(dict={'CONTROL': {'calculation': 'scf'}}),
)
```

## Key Modules and Classes

### Process

Base class for all executable entities (calculations and workflows).

```python
from aiida.engine import Process

class MyProcess(Process):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input('x', valid_type=orm.Int)
        spec.output('result', valid_type=orm.Int)

    def run(self):
        self.out('result', orm.Int(self.inputs.x.value * 2))

result = engine.run(MyProcess, x=orm.Int(5))
```

### WorkChain

Workflow orchestration class for chaining calculations.

```python
from aiida import orm
from aiida.engine import WorkChain, calcfunction

@calcfunction
def multiply(x, y):
    return orm.Float(x.value * y.value)

class MultiplyAddWorkChain(WorkChain):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input('x', valid_type=orm.Int)
        spec.input('y', valid_type=orm.Int)
        spec.input('z', valid_type=orm.Int)
        spec.outline(
            cls.multiply,
            cls.add,
            cls.results,
        )
        spec.output('result', valid_type=orm.Int)

    def multiply(self):
        self.ctx.product = multiply(self.inputs.x, self.inputs.y)

    def add(self):
        self.ctx.sum = self.ctx.product + self.inputs.z

    def results(self):
        self.out('result', self.ctx.sum)
```

### Node

Base class for all data and process nodes in the provenance graph.

```python
from aiida import orm

data = orm.Int(42)
data.store()

print(f"PK: {data.pk}, UUID: {data.uuid}")
print(f"Node type: {data.node_type}")
print(f"Creator: {data.creator}")

node = orm.load_node(pk=123)
print(f"Label: {node.label}")
print(f"Description: {node.description}")
print(f"Extras: {node.extras}")
print(f"Created: {node.ctime}")
```

### Data Classes

Specialized data types for computational workflows.

```python
from aiida import orm

structure = orm.StructureData(cell=[[4, 0, 0], [0, 4, 0], [0, 0, 4]])
structure.append_atom(position=(0, 0, 0), symbols='C')

parameters = orm.Dict(dict={'ecutwfc': 30.0, 'ecutrho': 240.0})

kpoints = orm.KpointsData()
kpoints.set_kpoints_mesh([4, 4, 4])

folder = orm.FolderData(tree='/path/to/folder')

remote = orm.RemoteData(computer=computer, remote_path='/scratch/job_123')

trajectory = orm.TrajectoryData()
trajectory.set_trajectory(
    stepids=[0, 1, 2],
    cells=[[[4, 0, 0], [0, 4, 0], [0, 0, 4]]] * 3,
    positions=[[[0, 0, 0], [2, 2, 2]]] * 3,
    symbols=['Si', 'Si']
)
```

### Calculation

Process classes for running external codes.

```python
from aiida import orm
from aiida.engine import CalcJob

class MyCalcJob(CalcJob):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input('structure', valid_type=orm.StructureData)
        spec.input('parameters', valid_type=orm.Dict)
        spec.output('output_parameters', valid_type=orm.Dict)
        spec.output('output_structure', valid_type=orm.StructureData, required=False)

    def prepare_for_submission(self, folder):
        with folder.open('input.in', 'w') as handle:
            handle.write(self.inputs.parameters.dict.to_yaml())

        return CalcInfo(
            codes_info=[CodeInfo(
                code_uuid=self.inputs.code.uuid,
                stdin_name='input.in',
                stdout_name='output.out',
            )],
            retrieve_list=['output.out', 'trajectory.xyz'],
        )
```

## Workflow Examples

### Simple Workflow with calcfunction

```python
from aiida import orm
from aiida.engine import calcfunction, run

@calcfunction
def create_structure(element: orm.Str, lattice_constant: orm.Float) -> orm.StructureData:
    from ase.build import bulk
    atoms = bulk(element.value, 'fcc', a=lattice_constant.value)
    return orm.StructureData(ase=atoms)

@calcfunction
def compute_volume(structure: orm.StructureData) -> orm.Float:
    return orm.Float(structure.get_cell_volume())

structure = create_structure(orm.Str('Cu'), orm.Float(3.6))
volume = compute_volume(structure)
print(f"Volume: {volume.value} Å³")
```

### Complex Workflow with WorkChain

```python
from aiida import orm
from aiida.engine import WorkChain, run, while_

class RelaxWorkChain(WorkChain):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input('structure', valid_type=orm.StructureData)
        spec.input('code', valid_type=orm.Code)
        spec.input('max_iterations', valid_type=orm.Int, default=lambda: orm.Int(5))
        spec.outline(
            cls.setup,
            while_(cls.should_continue)(
                cls.run_relaxation,
                cls.check_convergence,
            ),
            cls.finalize,
        )
        spec.output('relaxed_structure', valid_type=orm.StructureData)

    def setup(self):
        self.ctx.iteration = 0
        self.ctx.converged = False
        self.ctx.current_structure = self.inputs.structure

    def should_continue(self):
        return not self.ctx.converged and self.ctx.iteration < self.inputs.max_iterations.value

    def run_relaxation(self):
        self.ctx.iteration += 1
        builder = self.inputs.code.get_builder()
        builder.structure = self.ctx.current_structure
        self.ctx.relax_calc = self.submit(builder)
        return self.to_context(relax_result=self.ctx.relax_calc)

    def check_convergence(self):
        result = self.ctx.relax_result
        forces = result.outputs.output_parameters.dict['forces']
        max_force = max(abs(f) for f in forces)
        self.ctx.converged = max_force < 0.01
        if not self.ctx.converged:
            self.ctx.current_structure = result.outputs.output_structure

    def finalize(self):
        self.out('relaxed_structure', self.ctx.current_structure)
```

### Error Handling in WorkChains

```python
from aiida import orm
from aiida.engine import WorkChain, BaseRestartWorkChain, process_handler, ProcessHandlerReport

class RobustRelaxWorkChain(BaseRestartWorkChain):
    _process_class = RelaxCalculation

    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input('structure', valid_type=orm.StructureData)
        spec.input('code', valid_type=orm.Code)
        spec.outline(
            cls.setup,
            while_(cls.should_run_process)(
                cls.run_process,
                cls.inspect_process,
            ),
        )

    def setup(self):
        super().setup()
        self.ctx.inputs = {'structure': self.inputs.structure, 'code': self.inputs.code}

    @process_handler(priority=100)
    def handle_unconverged(self, node):
        if not node.is_finished_ok:
            self.ctx.inputs['parameters'] = self._increase_cutoff()
            return ProcessHandlerReport(do_break=False)
```

## Database and Querying Examples

### Basic Queries

```python
from aiida import orm

qb = orm.QueryBuilder()
qb.append(orm.StructureData)
structures = qb.all()
print(f"Found {len(structures)} structures")

qb = orm.QueryBuilder()
qb.append(orm.StructureData, project=['label', 'id'])
for label, pk in qb.iterall():
    print(f"{label}: PK={pk}")

qb = orm.QueryBuilder()
qb.append(orm.StructureData, filters={'extras.formula': 'Si'}, project=['uuid'])
results = [r[0] for r in qb.all()]
```

### Provenance Queries

```python
from aiida import orm

qb = orm.QueryBuilder()
qb.append(orm.StructureData, tag='structure', project=['label'])
qb.append(orm.CalcJobNode, with_incoming='structure', tag='calc')
qb.append(orm.Dict, with_incoming='calc', tag='output', project=['attributes.energy'])
for label, energy in qb.iterall():
    print(f"{label}: Energy = {energy} eV")

qb = orm.QueryBuilder()
qb.append(orm.WorkChainNode, tag='workflow')
qb.append(orm.StructureData, with_outgoing='workflow', tag='output_structure')
qb.append(orm.StructureData, with_incoming='workflow', tag='input_structure')
results = qb.all()
```

### Advanced Filters

```python
from aiida import orm

qb = orm.QueryBuilder()
qb.append(orm.CalcJobNode,
    filters={
        'attributes.exit_status': 0,
        'ctime': {'>=': '2024-01-01'},
        'attributes.options.resources.num_machines': 1
    },
    project=['id', 'label']
)

qb = orm.QueryBuilder()
qb.append(orm.StructureData,
    filters={'extras.kinds': {'contains': ['Si']}},
    project=['id']
)

qb = orm.QueryBuilder()
qb.append(orm.Node,
    filters={'node_type': {'like': 'data.structure.%'}},
    project=['id', 'label']
)
```

### Aggregation Queries

```python
from aiida import orm

qb = orm.QueryBuilder()
qb.append(orm.User, tag='user', project=['email'])
qb.append(orm.Node, with_user='user', project=['id'])
results = qb.all()
from collections import Counter
user_counts = Counter(email for email, _ in results)
```

### Export/Import Data

```python
from aiida import orm, tools

qb = orm.QueryBuilder()
qb.append(orm.StructureData)
nodes = [n[0] for n in qb.all()]
tools.export(nodes, 'structures.aiida')

imported = tools.import_tree('archive.aiida')

node = orm.load_node(pk=123)
node.export('node.aiida')
```

## Code Integration Examples

### Setting Up a Code

```python
from aiida import orm

computer = orm.Computer(
    label='cluster',
    hostname='cluster.example.com',
    description='HPC cluster',
    transport_type='core.ssh',
    scheduler_type='core.slurm',
    workdir='/scratch/{username}/aiida'
).store()

code = orm.Code(
    label='qe-pw',
    description='Quantum ESPRESSO pw.x',
    filepath_executable='/usr/bin/pw.x',
    computer=computer
).store()

code.set_prepend_text('module load quantum-espresso/7.0')
code.store()
```

### Using verdi CLI

```bash
verdi code setup -L qe-pw -D 'Quantum ESPRESSO pw.x' -P core.pw --on-computer -Y cluster --prepend-text 'module load qe'
verdi computer setup -L localhost -H localhost -T core.local -S core.direct -w /tmp/aiida
verdi code list
verdi computer list
verdi process list -a
verdi node show 123
```

### Plugin Development

```python
from aiida import orm, plugins

entry_point = 'quantumespresso.pw'
CalculationClass = plugins.CalculationFactory(entry_point)
ParserClass = plugins.ParserFactory(f'{entry_point}.parser')

from aiida.engine import CalcJob

class MyPluginCalculation(CalcJob):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input('structure', valid_type=orm.StructureData)
        spec.input('parameters', valid_type=orm.Dict)
        spec.input('settings', valid_type=orm.Dict, required=False)
        spec.output('output_parameters', valid_type=orm.Dict)
        spec.output('output_structure', valid_type=orm.StructureData, required=False)
        spec.exit_code(100, 'ERROR_UNCONVERGED', message='Calculation did not converge.')
```

### Connecting to External Codes

```python
from aiida import orm, engine

computer = orm.load_computer('localhost')
code = orm.Code(
    label='python-script',
    filepath_executable='/path/to/script.py',
    computer=computer
).store()

builder = code.get_builder()
builder.input_file = orm.SinglefileData(file='/path/to/input.txt')
builder.metadata.options = {'resources': {'num_machines': 1}}
result = engine.run_get_node(builder)
```

## AiiDAlab Usage

AiiDAlab is a browser-based platform for running AiiDA workflows.

### Accessing AiiDAlab

```bash
pip install aiidalab
aiidalab start
```

### Using AiiDAlab Apps

```python
from aiidalab_widgets_base import StructureBrowserWidget, StructureManagerWidget
from aiidalab_widgets_base import ProcessNodesTreeWidget

structure_browser = StructureBrowserWidget()
display(structure_browser)

from aiida import orm
qb = orm.QueryBuilder()
qb.append(orm.WorkChainNode)
tree = ProcessNodesTreeWidget()
tree.nodes = [n[0] for n in qb.all()]
display(tree)
```

### Jupyter Integration

```python
from aiida import orm, engine
from aiidalab_widgets_base import StructureUploadWidget, SubmitButtonWidget

structure_uploader = StructureUploadWidget()
display(structure_uploader)

def submit_callback():
    structure = structure_uploader.structure_node
    builder = code.get_builder()
    builder.structure = structure
    return engine.submit(builder)

submit_btn = SubmitButtonWidget()
submit_btn.on_click(submit_callback)
display(submit_btn)
```

### AiiDAlab Environment

```python
from aiidalab import load_profile
load_profile()

from aiidalab.app import AppManager
apps = AppManager.list_apps()
for app in apps:
    print(f"{app.name}: {app.description}")

AppManager.install('quantum-espresso')
AppManager.install('aiidalab-empa-vibes')
```

## Resources

- Official Website: https://aiida.net
- Documentation: https://aiida.readthedocs.io
- GitHub: https://github.com/aiidateam/aiida-core
- Forum: https://aiida.discourse.group
- Language: Python
- Current Version: 2.8.0