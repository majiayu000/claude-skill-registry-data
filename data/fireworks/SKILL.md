---
name: fireworks
description: Python workflow engine developed at LBNL for managing high-throughput computational workflows. Use when orchestrating complex DFT calculations, managing job queues, or needing dynamic workflow management with failure recovery.
metadata:
    skill-author: MindSpore Science Team
---

## Overview

FireWorks is a Python workflow engine developed at LBNL for managing high-throughput computational workflows. It provides dynamic workflow management with MongoDB-backed persistence, failure recovery, and integration with HPC queue systems (SLURM, PBS, SGE). Complex workflows are defined using Python, JSON, or YAML and can be monitored through a built-in web interface.

# When to Use This Skill

1. **Multi-step computational workflows** - Orchestrating complex pipelines with dependencies between calculation stages
2. **High-throughput computing** - Managing thousands of independent or dependent computational jobs
3. **Dynamic workflow creation** - Creating new workflow branches based on intermediate results
4. **Failure recovery and job rerun** - Automatically detecting failed jobs and restarting from failure points
5. **HPC queue integration** - Submitting jobs to SLURM, PBS, SGE, or other queue systems with automatic management
6. **Long-running computational campaigns** - Running projects spanning weeks or months with persistent state tracking
7. **Distributed computing across machines** - Running workflows across multiple workers and computing centers
8. **Progress monitoring and reporting** - Tracking job status via web GUI or command-line queries

# Best Practices

- **Use meaningful workflow names** - Name workflows descriptively for easy filtering with `lpad get_wflows -n <name>`
- **Set job priorities** - Use `lpad set_priority` or `add_priority` powerup to ensure critical jobs run first
- **Implement proper error handling** - Return `FWAction` with stored data on exceptions for debugging
- **Use `_pass_job_info` for parent data** - Pass launch directories and metadata between dependent FireWorks
- **Configure reservation mode limits** - Use `-m` flag with `qlaunch rapidfire` to prevent queue flooding
- **Monitor lost runs regularly** - Schedule `lpad detect_lostruns` to catch crashed or orphaned jobs
- **Back up LaunchPad database** - Run `mongodump` regularly to preserve workflow state
- **Test workflows locally first** - Use `rlaunch singleshot` for debugging before queue submission
- **Use category-based routing** - Set `category` in fworker config to route specific workflows to specific workers

# Troubleshooting

| Problem | Solution |
|---------|----------|
| Cannot connect to MongoDB | Verify MongoDB is running: `mongod --fork`. Check connection string in `my_launchpad.yaml`. |
| Workflows stuck in READY | No worker is pulling jobs. Run `rlaunch rapidfire` or `qlaunch rapidfire`. |
| Job fizzled | Check `lpad get_fws -s FIZZLED -d all` for error traceback. Use `--pdb` flag for debugging. |
| Workflows not progressing | Check for parent FireWorks that fizzled. Use `lpad get_wflows -d more` to inspect dependencies. |
| Queue submission fails | Verify qadapter config matches your queue system. Check walltime format and queue names. |
| Web GUI not loading | Ensure port is available. Try `lpad webgui -p 8888` with alternate port. |
| Lost runs detected | Fizzle with `lpad detect_lostruns --fizzle`, then rerun with `lpad rerun_fws -s FIZZLED`. |
| Duplicate workflows created | FireWorks doesn't auto-deduplicate by default. Use unique names or implement duplicate checking. |
| Slow database queries | Run `lpad maintain` to compact database. Consider adding indexes for frequently queried fields. |

# FireWorks

FireWorks is a free, open-source workflow management system for defining, managing, and executing workflows. Complex workflows can be defined using Python, JSON, or YAML, are stored using MongoDB, and can be monitored through a built-in web interface.

## Installation

### Install MongoDB

FireWorks requires MongoDB for workflow storage. Options:

**Local installation:**
```bash
# macOS (Homebrew)
brew install mongodb-community

# Ubuntu/Debian
sudo apt-get install mongodb

# Start MongoDB
mongod --logpath mongod.log --fork
```

**Cloud provider (MongoDB Atlas):**
1. Create free 500MB shared cluster at mongodb.com/cloud/atlas
2. Create database user and note credentials
3. Add your IP to access list
4. Use connection URI in FireWorks config

### Install FireWorks

```bash
# Via pip (recommended)
pip install FireWorks

# Optional dependencies
pip install matplotlib   # web GUI plots
pip install paramiko     # remote file transfer
pip install fabric       # daemon mode qlaunch
pip install requests     # NEWT queue adapter

# Via git (developer mode)
git clone git@github.com:materialsproject/fireworks.git
cd fireworks
python setup.py develop

# Run tests
python setup.py test
```

### Configure LaunchPad

```bash
# Initialize configuration
lpad init

# Or with URI mode (MongoDB Atlas)
lpad init -u
```

Create `my_launchpad.yaml`:
```yaml
host: localhost
port: 27017
name: fireworks
username: null
password: null
```

For MongoDB Atlas:
```yaml
host: mongodb+srv://<username>:<password>@cluster.mongodb.net
name: fireworks
uri_mode: true
```

## Core Concepts

### Firetask
Atomic computing job - executes a shell script or Python function.

```python
from fireworks import ScriptTask, PyTask

# Shell command task
task = ScriptTask.from_str('echo "hello"')

# Python function task
task = PyTask(func='my_module.my_function', args=['input1', 'input2'])
```

### FireWork
Contains JSON spec with tasks and input parameters.

```python
from fireworks import Firework

fw = Firework(
    ScriptTask.from_str('echo "hello"'),
    name="hello",
    spec={"input_param": 42}
)
```

### Workflow
DAG of FireWorks with dependencies.

```python
from fireworks import Workflow

fw1 = Firework(ScriptTask.from_str('echo "step 1"'), name="step1")
fw2 = Firework(ScriptTask.from_str('echo "step 2"'), name="step2", parents=[fw1])

wf = Workflow([fw1, fw2], name="linear_workflow")
```

### LaunchPad
MongoDB-backed server managing workflows.

```python
from fireworks import LaunchPad

lp = LaunchPad()
lp.add_wf(wf)          # Add workflow
lp.get_fw_by_id(1)     # Query workflow
```

### FireWorker
Worker requesting and executing jobs from LaunchPad.

```yaml
# my_fworker.yaml
name: my_worker
category: ''
query: '{}'
```

## Quick Start Examples

### Command Line

```bash
# Reset database
lpad reset

# Add simple workflow
lpad add_scripts 'echo "hello"' 'echo "goodbye"' -n hello goodbye -w test_workflow

# View workflows
lpad get_wflows -n test_workflow -d more

# Run all jobs (rapidfire mode)
rlaunch --silencer rapidfire

# Run single job
rlaunch singleshot

# Launch web GUI
lpad webgui
```

### Python API

```python
from fireworks import Firework, Workflow, LaunchPad, ScriptTask
from fireworks.core.rocket_launcher import rapidfire

launchpad = LaunchPad()
launchpad.reset('', require_password=False)

fw1 = Firework(ScriptTask.from_str('echo "hello"'), name="hello")
fw2 = Firework(ScriptTask.from_str('echo "goodbye"'), name="goodbye", parents=[fw1])
wf = Workflow([fw1, fw2], name="test workflow")

launchpad.add_wf(wf)
rapidfire(launchpad)
```

## Workflow Composition

### Linear Workflow

```yaml
# hamlet_wf.yaml
fws:
  - fw_id: 1
    spec:
      _tasks:
        - _fw_name: ScriptTask
          script: echo "To be, or not to be,"
    name: hamlet line 1
  - fw_id: 2
    spec:
      _tasks:
        - _fw_name: ScriptTask
          script: echo "that is the question:"
    name: hamlet line 2
links:
  1: [2]
```

### Diamond Workflow (Branching)

```python
from fireworks import Firework, Workflow, ScriptTask

task1 = ScriptTask.from_str('echo "CEO"')
task2 = ScriptTask.from_str('echo "Manager 1"')
task3 = ScriptTask.from_str('echo "Manager 2"')
task4 = ScriptTask.from_str('echo "Intern"')

fw1 = Firework(task1, name="CEO")
fw2 = Firework(task2, name="Manager 1", parents=[fw1])
fw3 = Firework(task3, name="Manager 2", parents=[fw1])
fw4 = Firework(task4, name="Intern", parents=[fw2, fw3])

workflow = Workflow([fw1, fw2, fw3, fw4])
```

### Custom Firetask

```python
from fireworks import Firetask, explicit_serialize

@explicit_serialize
class AdditionTask(Firetask):
    def run_task(self, fw_spec):
        input_array = fw_spec['input_array']
        m_sum = sum(input_array)
        print(f"The sum of {input_array} is: {m_sum}")
        return FWAction(stored_data={'sum': m_sum})
```

## Dynamic Workflow Modification

### Passing Job Info

```python
# Parent passes launch_dir to child
fw1 = Firework(
    ScriptTask.from_str('echo "parent"'),
    spec={"_pass_job_info": True}
)
fw2 = Firework(PrintJobTask(), parents=[fw1])
```

Child receives `_job_info` array with parent's `fw_id`, `name`, `launch_dir`.

### Passing Data with FWAction

```python
from fireworks import FWAction

@explicit_serialize
class AddAndModifyTask(Firetask):
    def run_task(self, fw_spec):
        input_array = fw_spec['input_array']
        m_sum = sum(input_array)
        return FWAction(
            stored_data={'sum': m_sum},
            mod_spec=[{'_push': {'input_array': m_sum}}]
        )
```

### Creating New FireWorks Dynamically

```python
@explicit_serialize
class FibonacciAdderTask(Firetask):
    def run_task(self, fw_spec):
        smaller = fw_spec['smaller']
        larger = fw_spec['larger']
        stop_point = fw_spec['stop_point']

        m_sum = smaller + larger

        if m_sum < stop_point:
            print(f"Next Fibonacci: {m_sum}")
            new_fw = Firework(
                FibonacciAdderTask(),
                spec={'smaller': larger, 'larger': m_sum, 'stop_point': stop_point}
            )
            return FWAction(stored_data={'next_fibnum': m_sum}, additions=new_fw)
        else:
            print(f"Limit exceeded at: {m_sum}")
            return FWAction()
```

## Job Scheduling

### Queue Adapter Configuration

```yaml
# my_qadapter.yaml (SLURM)
_fw_name: SlurmAdapter
queue: batch
walltime: '24:00:00'
nodes: 1
ppnode: 24
job_name: fireworks
logdir: /path/to/logs
pre_rocket: null
post_rocket: null

rocket_launch: rlaunch -l /path/to/my_launchpad.yaml -w /path/to/my_fworker.yaml singleshot
```

PBS example:
```yaml
_fw_name: PBSAdapter
queue: regular
walltime: '24:00:00'
nodes: 1
ppnode: 24
job_name: fireworks
rocket_launch: rlaunch -l /path/to/my_launchpad.yaml singleshot
```

### Queue Launch Commands

```bash
# Single job submission
qlaunch singleshot

# Rapidfire - maintain jobs in queue
qlaunch rapidfire -m 10

# Infinite mode - continuous submission
qlaunch rapidfire -m 2 --nlaunches infinite

# Multiple rockets per queue job
qlaunch -q my_qp_multi.yaml singleshot  # uses rapidfire in qadapter

# Remote queue launch
qlaunch -rh compute.host.gov -ru username rapidfire -m 50
```

### Supported Queue Systems

- SLURM
- PBS/Torque
- Sun Grid Engine (SGE)
- IBM LoadLeveler
- NEWT (NERSC)

## Monitoring and Management Commands

### LaunchPad (lpad) Commands

```bash
# Workflow management
lpad add <workflow.yaml>       # Add workflow
lpad get_wflows                # List all workflows
lpad get_wflows -n <name>      # Filter by name
lpad get_wflows -s READY       # Filter by state
lpad get_fws -i <fw_id>        # Get specific Firework

# Job control
lpad set_priority -i <fw_id> <priority>  # Set priority
lpad defuse_fws -i <fw_id>     # Pause (defuse) Firework
lpad archive_fws -i <fw_id>    # Archive Firework
lpad delete_wflows -i <fw_id>  # Delete workflow

# Database maintenance
lpad reset                     # Clear database
lpad maintain                  # Compact database
lpad detect_lostruns           # Find orphaned jobs

# Web interface
lpad webgui                    # Launch web GUI
lpad webgui -p 8080            # Specify port

# Reporting
lpad report                    # Generate summary
lpad introspect                # Analyze failures
```

### Rocket Launcher (rlaunch) Commands

```bash
rlaunch singleshot             # Run one job
rlaunch rapidfire              # Run all available jobs
rlaunch -s rapidfire           # Silent mode
rlaunch -f <fw_id> singleshot  # Run specific Firework
rlaunch singleshot --pdb       # Debug mode on exception
```

### Queue Launcher (qlaunch) Commands

```bash
qlaunch singleshot             # Submit one queue job
qlaunch rapidfire -m <max>     # Submit up to max jobs
qlaunch rapidfire --nlaunches infinite  # Continuous mode
qlaunch -rh <host> rapidfire   # Remote submission
```

## Failure Recovery and Rerun

### Detect Failures

```bash
# List fizzled FireWorks
lpad get_fws -s FIZZLED

# Detect lost/crashed jobs (running >4 hours without ping)
lpad detect_lostruns --fizzle

# Detect jobs running >1 second (for testing)
lpad detect_lostruns --time 1 --fizzle
```

### Rerun FireWorks

```bash
# Rerun specific Firework
lpad rerun_fws -i <fw_id>

# Rerun all fizzled jobs
lpad rerun_fws -s FIZZLED

# Task-level rerun (resume from failed task)
lpad rerun_fws -s FIZZLED --task-level

# Rerun with data copy from previous run
lpad rerun_fws -s FIZZLED --task-level --copy-data

# Clear recovery info for fresh start
lpad rerun_fws -i <fw_id> --clear-recovery
```

### Rerun by Error Message

```bash
lpad rerun_fws -q '{"action.stored_data._exception._stacktrace": {"$regex": "MemoryError"}}' -lm
```

### Python Failure Handling

```python
from fireworks import FWAction

@explicit_serialize
class RobustTask(Firetask):
    def run_task(self, fw_spec):
        try:
            result = perform_calculation(fw_spec['input'])
            return FWAction(stored_data={'result': result})
        except Exception as e:
            # Store error details
            return FWAction(stored_data={'error': str(e)})
```

## Workflow States

| State | Description |
|-------|-------------|
| READY | Ready to run |
| WAITING | Waiting for parent completion |
| RESERVED | Reserved for queue submission |
| RUNNING | Currently executing |
| COMPLETED | Successfully finished |
| FIZZLED | Failed with error |
| ARCHIVED | Soft deleted |

## Resources

- Documentation: https://materialsproject.github.io/fireworks/
- GitHub: https://github.com/materialsproject/fireworks
- Forum: https://discuss.matsci.org/c/fireworks
- Citation: Jain et al. (2015) Concurrency Computat.: Pract. Exper., 27: 5037-5059