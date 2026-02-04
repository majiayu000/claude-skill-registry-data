---
name: repo-reorganization
description: "Python package reorganization with pyproject.toml inside package directory"
author: smith6jt
date: 2024-12-27
---

# Repo Reorganization - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-27 |
| **Goal** | Reorganize maxfuse repo to be self-contained in src/maxfuse/ with pyproject.toml inside the package |
| **Environment** | Python 3.12, hatchling build backend |
| **Status** | Success |

## Context
Needed to reorganize a project so the entire package (including pyproject.toml and README.md) lives inside `src/maxfuse/`. This enables the package to be portable - the repo name can change but the package remains self-contained.

Standard src layout puts pyproject.toml at repo root, but we needed it inside the package directory itself.

## Verified Workflow

### Final Directory Structure
```
repo/
├── src/
│   ├── maxfuse/               # Self-contained package
│   │   ├── __init__.py
│   │   ├── pyproject.toml     # Inside package!
│   │   ├── README.md
│   │   ├── core/              # Submodules
│   │   └── mario/
│   └── other-repo/            # Can coexist with other repos
├── notebooks/
├── data/                      # Gitignored
├── results/                   # Gitignored
└── .gitignore
```

### Working pyproject.toml Configuration
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "maxfuse"
version = "0.1.0"
readme = "README.md"
# ... other project metadata

[tool.hatch.build.targets.wheel]
only-include = ["__init__.py", "core", "mario"]

[tool.hatch.build.targets.wheel.force-include]
"__init__.py" = "maxfuse/__init__.py"
"core" = "maxfuse/core"
"mario" = "maxfuse/mario"
```

### Installation
```bash
pip install -e src/maxfuse
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| `packages = ["."]` | Hatchling couldn't find package, .pth file was empty | Cannot use "." as package name |
| `packages = ["maxfuse"]` with `sources = [".."]` | Editable install didn't expose module | Source remapping doesn't work for editable installs |
| `directory = ".."` in `[tool.hatch.build]` | Module not found after install | Directory setting alone insufficient |
| Standard `packages = ["src/maxfuse"]` | Path wrong since pyproject.toml is already inside package | Must use force-include when pyproject.toml is inside package |

## Final Parameters
The key is using `force-include` to explicitly map files to their destination paths:

```toml
[tool.hatch.build.targets.wheel]
only-include = ["__init__.py", "core", "mario"]

[tool.hatch.build.targets.wheel.force-include]
"__init__.py" = "maxfuse/__init__.py"
"core" = "maxfuse/core"
"mario" = "maxfuse/mario"
```

This tells hatchling:
1. Only include these specific files/directories from current location
2. Map them to `maxfuse/` prefix in the wheel

## Key Insights
- When pyproject.toml is inside the package directory, standard src layout patterns don't work
- `force-include` is the solution for non-standard layouts
- The wheel size changing (e.g., 1.7KB to 52KB) indicates whether code is actually included
- Editable installs create .pth files - check if they're empty when debugging
- This pattern enables truly portable, self-contained packages

## References
- Hatchling build configuration: https://hatch.pypa.io/latest/config/build/
- force-include documentation: https://hatch.pypa.io/latest/plugins/builder/wheel/#options
