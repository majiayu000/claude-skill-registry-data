---
name: git-repository-cloning
description: Use when you need to obtain source code or computational workflows from a published repository, particularly when the article explicitly provides a GitHub URL and documents that the repository contains code required to regenerate published results (e.g., simulation outputs, figures, or tables).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3391
  tools:
  - Git
  - Python
  - Jupyter
derived_from:
- doi: 10.1371/journal.pcbi.1009105
  title: ORA
evidence_spans: []
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

# git-repository-cloning

## Summary

Clone a remote Git repository to obtain source code, notebooks, and reproducible workflows for scientific analysis. This skill is essential for accessing published computational methods and ensuring reproducibility of research results.

## When to use

Use this skill when you need to obtain source code or computational workflows from a published repository, particularly when the article explicitly provides a GitHub URL and documents that the repository contains code required to regenerate published results (e.g., simulation outputs, figures, or tables).

## When NOT to use

- The code or notebook is already present in your working environment or has been previously downloaded.
- You only need to read the article text and do not require access to the actual executable source code or notebooks.
- The article does not provide a repository URL or explicitly state that code is available in a public repository.

## Inputs

- GitHub repository URL (string)
- Target local directory path (string)

## Outputs

- Cloned repository directory with full project structure
- Source code files (.py, .ipynb, .R, etc.)
- Configuration and dependency files (requirements.txt, environment.yml, etc.)
- Documentation files (README, CHANGELOG, etc.)

## How to apply

Identify the repository URL from the article or supplementary materials (format: github.com/username/repo-name). Use git clone to download the repository to your local environment. Verify that the cloned directory contains the expected structure (e.g., src/, notebooks/, README) and matches the repository structure referenced in the article. The cloning preserves the full commit history and allows you to install dependencies and execute code as documented in the repository README or article methods.

## Related tools

- **Git** (Version control system used to clone the remote repository and manage source code retrieval) — https://github.com
- **Python** (Language used for simulation code and data analysis scripts within the cloned repository) — https://github.com/cwieder/metabolomics-ORA
- **Jupyter** (Environment for executing reproducible notebooks (e.g., reproducible_simulations.ipynb) after cloning) — https://github.com/cwieder/metabolomics-ORA

## Examples

```
git clone https://github.com/cwieder/metabolomics-ORA.git
```

## Evaluation signals

- The cloned directory structure matches the repository layout referenced in the article (e.g., presence of src/, notebooks/, README)
- Required files are present and accessible (e.g., reproducible_simulations.ipynb, requirements.txt, dependency manifests)
- Git status shows the repository is up-to-date with the remote (git status returns 'nothing to commit')
- The README and documentation in the cloned repository match or reference the DOI and authors cited in the article
- Dependencies listed in the repository configuration can be successfully installed in the specified Python environment

## Limitations

- Cloning requires network access and sufficient disk space for the repository and its full commit history.
- The cloned code is only as current as the last commit on the default branch; the article may reference a specific commit hash or release tag that must be explicitly checked out.
- If the repository has been deleted or made private since publication, cloning will fail; archived or deprecated repositories may lack ongoing maintenance.
- Cloning does not automatically install dependencies or set up the environment; subsequent steps (e.g., pip install, conda env create) are required before code can be executed.

## Evidence

- [other] 1. Clone the cwieder/metabolomics-ORA repository from GitHub.: "Clone the cwieder/metabolomics-ORA repository from GitHub."
- [intro] This repository contains the code to run the simulations presented in the study: "This repository contains the code to run the simulations presented in the study"
- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
- [intro] git clone https://github.com/cwieder/metabolomics-ORA.git: "git clone https://github.com/cwieder/metabolomics-ORA.git"
