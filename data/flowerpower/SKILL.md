---
name: flowerpower
description: Create and manage data pipelines using the FlowerPower framework with Hamilton DAGs and uv. Use when users request creating flowerpower projects, pipelines, Hamilton dataflows, or ask about flowerpower configuration, execution, or CLI commands.
---

# FlowerPower Pipeline Skill

Create and manage data processing pipelines using FlowerPower with Hamilton DAGs.

## Quick Start

```bash
# Install flowerpower
uv pip install flowerpower

# Initialize project
flowerpower init --name my-project

# Create pipeline
flowerpower pipeline new my_pipeline

# Run pipeline
flowerpower pipeline run my_pipeline
```

## Project Initialization

Use `scripts/init_project.py` or CLI:

```bash
# CLI
flowerpower init --name <project-name>

# Python
from flowerpower import FlowerPowerProject
project = FlowerPowerProject.init(name='my-project')
```

Creates structure:
```
my-project/
├── conf/
│   ├── project.yml
│   └── pipelines/
├── pipelines/
└── hooks/
```

## Creating Pipelines

Use `scripts/create_pipeline.py` or CLI:

```bash
flowerpower pipeline new <name>
```

Creates:
- `pipelines/<name>.py` - Hamilton functions
- `conf/pipelines/<name>.yml` - Configuration

### Pipeline Module Template

```python
from hamilton.function_modifiers import parameterize
from pathlib import Path
from flowerpower.cfg import Config

PARAMS = Config.load(
    Path(__file__).parents[1], pipeline_name="my_pipeline"
).pipeline.h_params

@parameterize(**PARAMS.input_config)
def load_data(source: str) -> dict:
    """Load data from source."""
    return {"source": source}

def process_data(load_data: dict) -> dict:
    """Process loaded data."""
    return {"processed": load_data}

def final_result(process_data: dict) -> str:
    """Return final result."""
    return str(process_data)
```

### Pipeline Config Template

```yaml
params:
  input_config:
    source: "data.csv"

run:
  final_vars:
    - final_result
  executor:
    type: threadpool
    max_workers: 4
  retry:
    max_retries: 3
    retry_delay: 1.0
```

## Running Pipelines

```bash
# Basic run
flowerpower pipeline run my_pipeline

# With inputs
flowerpower pipeline run my_pipeline --inputs '{"key": "value"}'

# With executor
flowerpower pipeline run my_pipeline --executor threadpool --executor-max-workers 8

# With retries
flowerpower pipeline run my_pipeline --max-retries 3 --retry-delay 2.0
```

Python API:
```python
from flowerpower import FlowerPowerProject

project = FlowerPowerProject.load('.')
result = project.run('my_pipeline')

# With RunConfig
from flowerpower.cfg.pipeline.run import RunConfig
config = RunConfig(inputs={"key": "value"}, final_vars=["output"])
result = project.run('my_pipeline', run_config=config)
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `flowerpower init --name <name>` | Initialize project |
| `flowerpower pipeline new <name>` | Create pipeline |
| `flowerpower pipeline run <name>` | Run pipeline |
| `flowerpower pipeline show-pipelines` | List pipelines |
| `flowerpower pipeline show-dag <name>` | Visualize DAG |
| `flowerpower pipeline delete <name>` | Delete pipeline |

## Executor Types

| Type | Use Case | Config |
|------|----------|--------|
| `synchronous` | Default, sequential | - |
| `threadpool` | I/O-bound tasks | `max_workers: N` |
| `processpool` | CPU-bound tasks | `max_workers: N` |
| `ray` | Distributed computing | `num_cpus: N` |
| `dask` | Distributed computing | `num_cpus: N` |

## Optional Dependencies

```bash
uv pip install flowerpower[io]   # I/O plugins
uv pip install flowerpower[ui]   # Hamilton UI
uv pip install flowerpower[all]  # All extras
```

## Resources

- **references/overview.md** - Key concepts, architecture, project structure
- **references/configuration.md** - Complete YAML configuration patterns
- **references/hamilton-patterns.md** - Hamilton function decorators and patterns

## Scripts

- **scripts/init_project.py** - Initialize new flowerpower project
- **scripts/create_pipeline.py** - Create new pipeline with template
- **scripts/run_pipeline.py** - Execute pipeline with options
- **scripts/list_pipelines.py** - List available pipelines
