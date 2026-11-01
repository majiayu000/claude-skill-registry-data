---
name: python-environment-setup
description: Use when you have cloned a scientific repository containing Python code (scripts, Jupyter notebooks, or module imports) and need to execute it locally or on new hardware.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3173
  tools:
  - Python
  - Jupyter
  - venv or conda
derived_from:
- doi: 10.1371/journal.pcbi.1009105
  title: ORA
evidence_spans:
- The Python code to generate the results is contained within the Jupyter notebook
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ora
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  dedup_kept_from: coll_ora
schema_version: 0.2.0
---

# python-environment-setup

## Summary

Configure a Python environment with specified version and dependencies to execute reproducible computational workflows. This skill ensures that simulation code, Jupyter notebooks, and analysis pipelines can run with consistent tool versions and package availability.

## When to use

You have cloned a scientific repository containing Python code (scripts, Jupyter notebooks, or module imports) and need to execute it locally or on new hardware. The repository specifies Python version constraints and dependency lists, and you need to isolate the environment to avoid conflicts with system or other project packages.

## When NOT to use

- Python code is already running successfully in a pre-existing system environment without errors or version conflicts.
- You are working in a container (Docker, Singularity) where Python and dependencies are already baked into the image.
- The repository contains no Python code or does not specify dependency versions.

## Inputs

- Python version specification (e.g., from README or setup documentation)
- Dependency list (requirements.txt, environment.yml, setup.py, or equivalent)
- Source code repository (cloned Git repository with Python code)

## Outputs

- Activated Python virtual environment with correct version
- Installed and verified packages matching specified versions
- Environment ready to execute Jupyter notebooks or Python scripts

## How to apply

First, identify the required Python version from the repository documentation or setup files (e.g., Python 3.8 as specified in the article). Create an isolated environment using a tool like venv or conda to prevent dependency conflicts. Install all dependencies listed in the repository's requirements file (requirements.txt, environment.yml, setup.py, or pyproject.toml) into that environment. Activate the environment before executing any scripts or launching Jupyter. Verify the installation by importing key packages and checking version numbers. This approach ensures reproducibility across different machines and operating systems (the study was tested on MacOS with standard hardware but the environment isolation makes it portable).

## Related tools

- **Python** (Interpreter and runtime for executing simulation code and Jupyter notebooks) — https://www.python.org
- **Jupyter** (Interactive notebook environment for executing and visualizing Python code sequentially) — https://jupyter.org
- **venv or conda** (Environment manager to create isolated Python environments with specified dependencies)

## Examples

```
python3 -m venv env && source env/bin/activate && pip install -r requirements.txt && jupyter notebook src/reproducible_simulations.ipynb
```

## Evaluation signals

- Python version in the environment matches the specification (Python 3.8 or as documented).
- All packages listed in dependencies can be imported without ImportError or version mismatch warnings.
- Jupyter kernel is available and uses the correct Python environment.
- Notebook cells execute sequentially without environment-related errors (missing modules, version incompatibilities).
- Generated outputs (figures, tables) are reproducible and match reference results reported in the publication.

## Limitations

- Environment setup does not guarantee reproducibility of numerical results across all hardware or OS combinations due to floating-point arithmetic differences and platform-specific library behavior.
- Dependency versions may become outdated or unavailable on package repositories over time, requiring manual pinning or sourcing from archived repositories.
- The study was tested on MacOS with standard hardware; execution on other operating systems or hardware configurations may require additional troubleshooting or platform-specific dependencies.

## Evidence

- [other] Set up a Python 3.8 environment with all required dependencies listed in the repository.: "Set up a Python 3.8 environment with all required dependencies listed in the repository."
- [other] The code tested using Python 3.8 on MacOS with standard hardware.: "with the code tested using Python 3.8 on MacOS with standard hardware."
- [other] Clone the cwieder/metabolomics-ORA repository from GitHub and launch Jupyter to open the notebook.: "1. Clone the cwieder/metabolomics-ORA repository from GitHub. 2. Set up a Python 3.8 environment with all required dependencies listed in the repository. 3. Launch Jupyter and open"
- [intro] The Python code to generate the results is contained within the Jupyter notebook.: "The Python code to generate the results is contained within the Jupyter notebook"
