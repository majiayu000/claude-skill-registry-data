---
name: conda-multi-account-hipergator
description: "Set up conda with multiple group storage locations on HiPerGator, including cache isolation"
author: KINTSUGI Team
date: 2026-01-11
---

# Conda Multi-Account Setup on HiPerGator

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-11 |
| **Goal** | Configure conda and ALL caches to use separate group storage locations |
| **Environment** | HiPerGator (UF), RHEL 9, multiple /blue/group/ directories |
| **Status** | Success |

## Context

On HiPerGator, users often belong to multiple research groups with separate storage allocations under `/blue/`. Each group may have its own conda installation and environments. The challenge is:
1. Switching between different group conda installations
2. Isolating ALL caches (pip, Jupyter, PyTorch, etc.) per-group to avoid conflicts and quota issues

### The Problem

- Default conda only knows about environments in home directory or current base
- Caches (pip, Jupyter, torch, HuggingFace, etc.) accumulate in home directory
- With multiple accounts, caches can conflict or exceed quota
- Hardcoding cache paths in `.bashrc` breaks when switching accounts

## Verified Workflow

### Solution: Dynamic Account Switching with Cache Isolation

**Architecture:**
```
~/.bashrc                    # Sources default use_conda script
~/.use_conda_maigan.sh       # Sets BLUE_BASE, sources cache_redirect.sh
~/.use_conda_clive.sh        # Sets BLUE_BASE, sources cache_redirect.sh
~/.cache_redirect.sh         # Uses BLUE_BASE to set all cache paths
```

### Step 1: Create Cache Redirect Script

Create `~/.cache_redirect.sh` that uses a `BLUE_BASE` variable:

```bash
# ~/.cache_redirect.sh
# BLUE_BASE must be set before sourcing this file

if [ -z "$BLUE_BASE" ]; then
    echo "Warning: BLUE_BASE not set, defaulting to maigan" >&2
    export BLUE_BASE="/blue/maigan/smith6jt"
fi
export CACHE_DIR="${BLUE_BASE}/scratch/cache"

# Python & Pip caches
export PIP_CACHE_DIR="${CACHE_DIR}/pip"
export PYTHONPYCACHEPREFIX="${CACHE_DIR}/pycache"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUSERBASE="${CACHE_DIR}/python_user"

# Jupyter & IPython
export JUPYTER_RUNTIME_DIR="${CACHE_DIR}/jupyter_runtime"
export JUPYTER_DATA_DIR="${CACHE_DIR}/jupyter_data"
export JUPYTER_CONFIG_DIR="${CACHE_DIR}/jupyter_config"
export IPYTHONDIR="${CACHE_DIR}/ipython"

# Deep Learning framework caches
export TORCH_HOME="${CACHE_DIR}/torch"
export TORCH_EXTENSIONS_DIR="${CACHE_DIR}/torch_extensions"
export TRANSFORMERS_CACHE="${CACHE_DIR}/huggingface"
export HF_HOME="${CACHE_DIR}/huggingface"
export NUMBA_CACHE_DIR="${CACHE_DIR}/numba"

# Matplotlib & plotting
export MPLCONFIGDIR="${CACHE_DIR}/mpl"
export MPLBACKEND="Agg"

# XDG directories (Linux standard)
export XDG_CACHE_HOME="${CACHE_DIR}/xdg"
export XDG_CONFIG_HOME="${CACHE_DIR}/config"
export XDG_DATA_HOME="${CACHE_DIR}/data"

# R libraries
export R_LIBS_USER="${BLUE_BASE}/R_libs"

# VSCode server cache
export VSCODE_SERVER_DIR="${CACHE_DIR}/vscode-server"

# Conda paths
export CONDA_PKGS_DIRS="${BLUE_BASE}/miniforge3/pkgs"
export CONDA_ENVS_PATH="${BLUE_BASE}/miniforge3/envs"

# Create directories if they don't exist
for dir in pip pycache python_user jupyter_runtime jupyter_data jupyter_config \
           ipython torch torch_extensions huggingface numba mpl xdg config data \
           vscode-server; do
    mkdir -p "${CACHE_DIR}/${dir}"
done
mkdir -p "${BLUE_BASE}/R_libs"

# Confirm setup in interactive shells
if [ -n "$PS1" ]; then
    echo "✓ Cache redirection active: ${CACHE_DIR}"
fi
```

### Step 2: Create Account-Specific Conda Scripts

**For maigan account (`~/.use_conda_maigan.sh`):**

```bash
#!/bin/bash
# ~/.use_conda_maigan.sh

# Stop any previous conda context
unset CONDA_EXE CONDA_PREFIX CONDA_SHLVL _CE_CONDA _CE_M CONDA_DEFAULT_ENV

# Set base directory FIRST
export BLUE_BASE="/blue/maigan/smith6jt"

# Conda configuration
export CONDARC="${BLUE_BASE}/.condarc"
export CONDA_ENVS_PATH="${BLUE_BASE}/miniforge3/envs"
export CONDA_PKGS_DIRS="${BLUE_BASE}/miniforge3/pkgs"

# Initialize conda
source "${BLUE_BASE}/miniforge3/etc/profile.d/conda.sh"

# Source cache redirection (uses BLUE_BASE set above)
if [ -f ~/.cache_redirect.sh ]; then
    source ~/.cache_redirect.sh
fi

echo "Switched to maigan conda environment"
```

**For other accounts (e.g., `~/.use_conda_clive.sh`):**

```bash
#!/bin/bash
# ~/.use_conda_clive.sh

unset CONDA_EXE CONDA_PREFIX CONDA_SHLVL _CE_CONDA _CE_M CONDA_DEFAULT_ENV

export BLUE_BASE="/blue/clive/smith6jt"

export CONDARC="${BLUE_BASE}/.condarc"
export CONDA_ENVS_PATH="${BLUE_BASE}/miniforge3/envs"
export CONDA_PKGS_DIRS="${BLUE_BASE}/miniforge3/pkgs"

source "${BLUE_BASE}/miniforge3/etc/profile.d/conda.sh"

if [ -f ~/.cache_redirect.sh ]; then
    source ~/.cache_redirect.sh
fi

echo "Switched to clive conda environment"
```

### Step 3: Configure .bashrc

```bash
# ~/.bashrc

case $- in
    *i*) ;;
    *) return;;
esac

PS1='\u@\h:\w\$ '

# Aliases
alias ls='ls --color=auto'
alias ll='ls -lh --color=auto'
alias grep='grep --color=auto'

# Account switchers
alias use_clive='source ~/.use_conda_clive.sh'
alias use_maigan='source ~/.use_conda_maigan.sh'

# Default account on startup (sets BLUE_BASE and sources cache_redirect)
if [ -f ~/.use_conda_maigan.sh ]; then
    source ~/.use_conda_maigan.sh
fi

export PATH="$HOME/.local/bin:$PATH"

# NVM (uses BLUE_BASE dynamically)
if [ -n "$BLUE_BASE" ]; then
    export NVM_DIR="${BLUE_BASE}/scratch/cache/config/nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi
```

### Step 4: Clean Up environments.txt

Remove other accounts' environments from `~/.conda/environments.txt`:

```bash
# Only include environments from your primary account
/blue/maigan/smith6jt/miniforge3
/blue/maigan/smith6jt/miniforge3/envs/KINTSUGI
```

## Usage

```bash
# Start of session - already using maigan (default from .bashrc)
conda env list
# Shows only maigan environments

# Switch to different account
use_clive
# Switches conda AND redirects all caches to /blue/clive/...

# Check cache location
echo $CACHE_DIR
# /blue/clive/smith6jt/scratch/cache

# Switch back
use_maigan
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Sourcing cache_redirect AFTER use_conda in .bashrc | Overwrites conda paths with hardcoded values | cache_redirect must be called BY use_conda scripts |
| Hardcoding cache paths in .bashrc | Doesn't switch when changing accounts | Use BLUE_BASE variable |
| Adding both accounts' envs to CONDA_ENVS_DIRS | Confusing, shows all envs from both accounts | Keep environments isolated per-account |
| Using CONDA_ENVS_DIRS colon-separated list | First path becomes default for new envs, unexpected behavior | Use CONDA_ENVS_PATH (single path) |

## Key Insights

- Set `BLUE_BASE` FIRST, then source cache_redirect
- Cache redirect script should use the variable, never hardcode paths
- `.bashrc` should NOT separately source cache_redirect - let use_conda scripts handle it
- Clean `~/.conda/environments.txt` to avoid confusion
- Each `/blue/group/` needs its own `.condarc` file
- Create cache directories (`/blue/group/user/scratch/cache/`) for each account

## Directory Structure

```
/blue/maigan/smith6jt/
├── miniforge3/
│   ├── etc/profile.d/conda.sh
│   ├── envs/KINTSUGI/
│   └── pkgs/
├── scratch/cache/          # All caches for this account
│   ├── pip/
│   ├── torch/
│   ├── jupyter_runtime/
│   └── ...
└── .condarc

/blue/clive/smith6jt/
├── miniforge3/
│   ├── envs/
│   └── pkgs/
├── scratch/cache/          # All caches for this account
└── .condarc

~/
├── .bashrc                 # Sources default use_conda script
├── .use_conda_maigan.sh    # Account switcher
├── .use_conda_clive.sh     # Account switcher
├── .cache_redirect.sh      # Dynamic cache paths (uses BLUE_BASE)
└── .conda/environments.txt # Clean - only default account
```

## References

- Conda configuration: https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/
- HiPerGator documentation: https://help.rc.ufl.edu/doc/Conda
- Miniforge: https://github.com/conda-forge/miniforge
