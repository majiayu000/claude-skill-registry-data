---
name: project-data-separation
description: "Pattern for separating repository code from user data and notebooks. Trigger: organizing scientific pipelines, separating code from data"
author: KINTSUGI Team
date: 2025-12-11
---

# Project-Data Separation Pattern

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-11 |
| **Goal** | Create a framework that separates repository code from user experimental data |
| **Environment** | Python 3.10+, scientific image processing pipeline |
| **Status** | Success |

## Context
Scientific pipelines often mix repository code with user data and modified notebooks, leading to:
- Git conflicts when updating the pipeline
- Difficulty sharing code without sharing data
- Users modifying template notebooks and losing changes on updates
- No standard project structure for experiments

## Verified Workflow

### Project Structure

```
Repository (KINTSUGI/)           User Project (MyExperiment/)
├── src/kintsugi/                ├── data/
│   └── project.py               │   ├── raw/              <- Input images
├── notebooks/                   │   └── processed/        <- Outputs
│   └── 1_Processing.ipynb       │       ├── stitched/     <- Stitched + illumination corrected
└── ...                          │       ├── deconvolved/  <- Deconvolved images
                                 │       ├── edf/          <- Extended depth of focus
                                 │       ├── registered/   <- Multi-cycle registered
                                 │       ├── signal_isolated/ <- Autofluorescence removed
                                 │       ├── segmented/    <- Segmentation masks
                                 │       └── analysis/     <- Analysis outputs
                                 ├── notebooks/            <- Working copies
                                 ├── configs/              <- Project configs
                                 ├── meta/                 <- Metadata
                                 ├── logs/                 <- Processing logs
                                 └── kintsugi_project.json
```

### Core Implementation

```python
# src/kintsugi/project.py

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union
import json

PROJECT_CONFIG_FILE = "kintsugi_project.json"

@dataclass
class ProjectPaths:
    """Structured paths for a project."""
    root: Path
    raw: Path
    processed: Path
    stitched: Path
    deconvolved: Path
    edf: Path
    registered: Path
    signal_isolated: Path
    segmented: Path
    analysis: Path
    notebooks: Path
    configs: Path
    meta: Path
    logs: Path
    cache: Path

    @classmethod
    def from_root(cls, root: Path) -> "ProjectPaths":
        root = Path(root).resolve()
        return cls(
            root=root,
            raw=root / "data" / "raw",
            processed=root / "data" / "processed",
            stitched=root / "data" / "processed" / "stitched",
            deconvolved=root / "data" / "processed" / "deconvolved",
            edf=root / "data" / "processed" / "edf",
            registered=root / "data" / "processed" / "registered",
            signal_isolated=root / "data" / "processed" / "signal_isolated",
            segmented=root / "data" / "processed" / "segmented",
            analysis=root / "data" / "processed" / "analysis",
            notebooks=root / "notebooks",
            configs=root / "configs",
            meta=root / "meta",
            logs=root / "logs",
            cache=root / ".cache",
        )

    def create_all(self) -> None:
        for name, path in self.__dict__.items():
            if isinstance(path, Path) and name != "root":
                path.mkdir(parents=True, exist_ok=True)


class Project:
    def __init__(self, root: Path, config: dict = None):
        self.root = Path(root).resolve()
        self.paths = ProjectPaths.from_root(self.root)
        self.config = config or {"name": self.root.name}

    @classmethod
    def create(cls, root: Path, name: str = None) -> "Project":
        root = Path(root).resolve()
        config_file = root / PROJECT_CONFIG_FILE

        if config_file.exists():
            return cls.load(root)

        project = cls(root, {"name": name or root.name})
        project.paths.create_all()
        project.save()
        return project

    @classmethod
    def load(cls, root: Path) -> "Project":
        config_file = Path(root) / PROJECT_CONFIG_FILE
        with open(config_file) as f:
            data = json.load(f)
        return cls(root, data.get("config", {}))

    def save(self) -> None:
        config_file = self.root / PROJECT_CONFIG_FILE
        with open(config_file, "w") as f:
            json.dump({"config": self.config}, f, indent=2)

    def setup_notebooks(self, repo_path: Path) -> None:
        """Copy notebook templates to project."""
        import shutil
        src = repo_path / "notebooks"
        for nb in src.glob("*.ipynb"):
            dst = self.paths.notebooks / nb.name
            if not dst.exists():
                shutil.copy2(nb, dst)


def init_project(project_dir: str, name: str = None) -> Project:
    """Main entry point for notebooks."""
    project_dir = Path(project_dir)
    config_file = project_dir / PROJECT_CONFIG_FILE

    if config_file.exists():
        return Project.load(project_dir)
    return Project.create(project_dir, name)
```

### Notebook Integration

At the start of each notebook:

```python
# Cell 1: Project Setup
from kintsugi.project import init_project

PROJECT_DIR = r"C:\Projects\MyExperiment"

project = init_project(
    PROJECT_DIR,
    name="My Experiment"
)

# Cell 2: Use project paths
image_dir = str(project.paths.raw)
output_dir = str(project.paths.stitched)
```

### Backward Compatibility

Map new paths to legacy variable names:

```python
# For backward compatibility with existing notebook code
image_dir = str(project.paths.raw)
stitch_dir = str(project.paths.stitched)
meta_dir = str(project.paths.meta)
base_dir = str(project.root.parent)
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Symlinks for notebooks | Windows doesn't support symlinks well | Copy notebooks instead |
| Storing paths as strings | Path operations became verbose | Use pathlib.Path throughout |
| No backward compatibility | Broke all existing notebook code | Map to legacy variable names |
| Complex config schema | Overkill for simple projects | Start simple, add complexity later |
| Auto-detecting repo path | Failed in various install scenarios | Use explicit detection with fallbacks |
| Different folder names in notebooks vs project.py | Created duplicate/inconsistent folder structures (`BaSiC_Stitched` vs `stitched`) | Always use canonical paths from `ProjectPaths`; never override with custom strings |

## Key Insights

- **Explicit > Implicit**: Users should explicitly set PROJECT_DIR, not guess
- **pathlib everywhere**: Use Path objects internally, convert to str at boundaries
- **Backward compat variables**: Map new paths to old variable names used in notebooks
- **Create all dirs upfront**: Avoid FileNotFoundError during processing
- **JSON config**: Simple, human-readable, easy to version control
- **Copy, don't link**: Notebooks should be copies users can modify freely
- **Canonical paths only**: Always use `project.paths.*` - never create ad-hoc paths with custom strings

## Configuration File Format

```json
{
  "version": "1.0.0",
  "config": {
    "name": "My Experiment",
    "description": "CODEX imaging data",
    "created": "2025-12-11T10:30:00",
    "cycles": [
      {"name": "cyc001", "channels": ["DAPI", "CD3", "CD20"]},
      {"name": "cyc002", "channels": ["DAPI", "CD4", "CD8"]}
    ]
  },
  "paths": {
    "raw": "data/raw",
    "processed": "data/processed"
  }
}
```

## Platform Considerations

```python
def setup_cuda_path(self) -> bool:
    """Windows-specific CUDA setup."""
    if platform.system() != "Windows":
        return True

    cuda_paths = [
        Path(r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\bin"),
        Path(r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin"),
    ]

    for cuda_bin in cuda_paths:
        if cuda_bin.exists() and list(cuda_bin.glob("nvrtc*.dll")):
            os.environ["PATH"] = str(cuda_bin) + os.pathsep + os.environ["PATH"]
            return True
    return False
```

## References
- Cookiecutter Data Science: https://drivendata.github.io/cookiecutter-data-science/
- Python pathlib: https://docs.python.org/3/library/pathlib.html
- Scientific project organization: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510
