---
name: conda-multi-account-hipergator
description: "Set up conda with multiple group storage locations on HiPerGator"
author: KINTSUGI Team
date: 2025-12-11
---

# Conda Multi-Account Setup on HiPerGator

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-11 |
| **Goal** | Configure conda to use environments from multiple group storage locations |
| **Environment** | HiPerGator (UF), RHEL 9, multiple /blue/group/ directories |
| **Status** | Success |

## Context

On HiPerGator, users often belong to multiple research groups with separate storage allocations under `/blue/`. Each group may have its own conda installation and environments. The challenge is accessing environments from a different group's storage location.

### The Problem

Default conda only knows about environments in:
- `~/.conda/envs/` (home directory)
- The base conda installation's `envs/` directory

Environments created under `/blue/othergroup/username/` are not visible.

## Verified Workflow

### Solution: Create a Sourcing Script

Create `~/.use_conda_<groupname>.sh` for each group's conda:

```bash
#!/bin/bash
# ~/.use_conda_maigan.sh - Switch to maigan group's conda

# Initialize conda for this shell
source /blue/maigan/smith6jt/miniforge3/etc/profile.d/conda.sh

# Add environment search paths
export CONDA_ENVS_DIRS="/blue/maigan/smith6jt/miniforge3/envs:$HOME/.conda/envs"

# Optional: Set package cache to shared location
export CONDA_PKGS_DIRS="/blue/maigan/smith6jt/miniforge3/pkgs:$HOME/.conda/pkgs"
```

### Usage Pattern

```bash
# At start of session, source the appropriate conda
source ~/.use_conda_maigan.sh

# Now conda sees all environments
conda env list
# Shows environments from /blue/maigan/smith6jt/miniforge3/envs/

# Activate environment from that location
conda activate KINTSUGI
```

### For Multiple Groups

Create separate scripts for each group:

```bash
# ~/.use_conda_maigan.sh - for maigan group
source /blue/maigan/smith6jt/miniforge3/etc/profile.d/conda.sh
export CONDA_ENVS_DIRS="/blue/maigan/smith6jt/miniforge3/envs:$HOME/.conda/envs"

# ~/.use_conda_othergroup.sh - for another group
source /blue/othergroup/smith6jt/miniforge3/etc/profile.d/conda.sh
export CONDA_ENVS_DIRS="/blue/othergroup/smith6jt/miniforge3/envs:$HOME/.conda/envs"
```

### Integration with Claude Code

Add the sourcing command to Claude Code permissions in `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(source ~/.use_conda_maigan.sh)",
      "Bash(conda activate:*)",
      "Bash(conda env list:*)",
      "Bash(pip install:*)"
    ]
  }
}
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Adding paths to `.condarc` `envs_dirs` | Only works after conda init, path issues with multiple condas | Use environment variables instead |
| Symlinking envs to home directory | Permissions issues, clutters home | Keep envs in original location |
| Using full paths to activate | Verbose, error-prone | Sourcing script is cleaner |
| Running `conda init` for multiple condas | Conflicts in .bashrc, breaks shell | Use separate sourcing scripts |
| Using `module load conda` | HiPerGator module may not have your custom envs | Use your own miniforge installation |

## Final Parameters

### Directory Structure

```
/blue/maigan/smith6jt/
├── miniforge3/           # Conda installation
│   ├── etc/profile.d/
│   │   └── conda.sh      # Source this to initialize
│   ├── envs/
│   │   └── KINTSUGI/     # Your environments here
│   └── pkgs/             # Package cache
└── KINTSUGI/             # Project directory

~/.use_conda_maigan.sh    # Sourcing script
```

### The Sourcing Script

```bash
#!/bin/bash
# ~/.use_conda_maigan.sh

# Initialize conda (REQUIRED - sets up conda command)
source /blue/maigan/smith6jt/miniforge3/etc/profile.d/conda.sh

# Tell conda where to find environments
export CONDA_ENVS_DIRS="/blue/maigan/smith6jt/miniforge3/envs:$HOME/.conda/envs"

# Share package cache to save space
export CONDA_PKGS_DIRS="/blue/maigan/smith6jt/miniforge3/pkgs:$HOME/.conda/pkgs"

echo "Conda configured for maigan group"
conda env list
```

## Key Insights

- `conda.sh` sourcing is required before any conda commands work
- `CONDA_ENVS_DIRS` is colon-separated list of paths to search for environments
- The first path in `CONDA_ENVS_DIRS` is where new environments are created
- Don't run `conda init` for multiple installations - it modifies .bashrc
- Miniforge is preferred over Anaconda for HPC (faster, BSD licensed)
- Package cache (`CONDA_PKGS_DIRS`) can be shared to save quota

## Environment Creation

When creating new environments with this setup:

```bash
source ~/.use_conda_maigan.sh

# Create from environment file
conda env create -f envs/env-linux.yml

# Or create manually
conda create -n myenv python=3.10

# Environment will be created in /blue/maigan/smith6jt/miniforge3/envs/
```

## References

- Conda configuration: https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/
- HiPerGator documentation: https://help.rc.ufl.edu/doc/Conda
- Miniforge: https://github.com/conda-forge/miniforge
