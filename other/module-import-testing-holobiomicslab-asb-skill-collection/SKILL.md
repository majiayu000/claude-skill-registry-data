---
name: module-import-testing
description: Use when releasing a new version of a Python package, validating packaging infrastructure changes, or confirming that distribution channels (PyPI, Bioconda) remain functional after upstream updates. Use it as a gate before finalizing a release to catch installation or import breakage early.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3673
  tools:
  - matchms
  - pip
  - conda
  - Python
derived_from:
- doi: 10.21105/joss.02411
  title: matchms
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- Verify new release is on [PyPi](https://pypi.org/project/matchms/#history)
- Wait until new release is also on Bioconda (https://anaconda.org/bioconda/matchms)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.21105/joss.02411
    title: matchms
  dedup_kept_from: coll_matchms
schema_version: 0.2.0
---

# module-import-testing

## Summary

Verify that a Python package installs correctly from its documented distribution channels (PyPI, Bioconda) and that the installed module can be imported without errors. This skill ensures reproducibility and accessibility of scientific software across multiple installation methods.

## When to use

Apply this skill when releasing a new version of a Python package, validating packaging infrastructure changes, or confirming that distribution channels (PyPI, Bioconda) remain functional after upstream updates. Use it as a gate before finalizing a release to catch installation or import breakage early.

## When NOT to use

- Do not use this skill to validate non-Python packages or packages distributed only as source tarballs without wheel artifacts.
- Do not apply this skill if your release is pre-release or development-only; save it for final tagged releases intended for end users.
- Do not use this as a substitute for full unit test coverage; this skill only tests basic accessibility, not functional correctness.

## Inputs

- package name and version identifier
- Python interpreter (3.10 or later for matchms)
- clean virtual environment or container

## Outputs

- installation success/failure status for each channel
- import success/failure status for each channel
- error logs or traceback if import fails
- documentation of tested Python versions and platforms

## How to apply

For each documented distribution channel (e.g., PyPI via pip, and Bioconda via conda), execute the installation command in a clean environment, then attempt to import the package in Python and verify no import errors or missing dependencies are reported. Test both installation methods separately in isolated virtual environments to avoid cross-contamination. Document the installation status, import success, and Python version compatibility for each channel. The rationale is that a package may build and upload successfully but fail at the user's installation or import stage due to missing dependencies, incompatible wheels, or metadata issues; testing both channels ensures users can reliably access and use the software regardless of their preferred package manager.

## Related tools

- **pip** (Package installer for PyPI distribution channel) — https://pip.pypa.io/
- **conda** (Package manager for Bioconda and Anaconda distribution channels) — https://conda.io/
- **Python** (Interpreter for testing module imports) — https://www.python.org/
- **matchms** (Example package under test) — https://github.com/matchms/matchms

## Examples

```
pip install matchms && python -c "import matchms; print(matchms.__version__)" && conda install -c bioconda matchms && python -c "import matchms; print(matchms.__version__)"
```

## Evaluation signals

- Installation command exits with status code 0 (success) for both pip and conda
- Python import statement (e.g., `import matchms`) completes without raising ImportError, AttributeError, or ModuleNotFoundError
- Package version queried via `__version__` or equivalent attribute matches the released version
- No missing or unmet dependency warnings are reported during import or package initialization
- Installation and import succeed across all declared supported Python versions (3.10–3.14 for matchms)

## Limitations

- PyPI distribution availability is near-instantaneous, but Bioconda availability may be delayed; the contributing guidelines note to 'Wait until new release is also on Bioconda via automaticly created PR', meaning testing must account for asynchronous channel propagation.
- Import testing in isolation does not verify functional correctness of package methods or submodules; only basic import and namespace accessibility.
- Testing is sensitive to the host environment (OS, architecture, Python patch version); wheel availability varies by platform (e.g., aarch64/arm64 vs. x86_64).
- This skill does not catch runtime errors that occur only when calling specific functions with particular input data.

## Evidence

- [other] 1. Install matchms from PyPI using pip or equivalent package manager. 2. Import the installed matchms package in Python and verify no import errors occur. 3. Install matchms from Bioconda using conda package manager. 4. Import the Bioconda-installed matchms package in Python and verify no import errors occur.: "1. Install matchms from PyPI using pip or equivalent package manager. 2. Import the installed matchms package in Python and verify no import errors occur. 3. Install matchms from Bioconda using conda"
- [other] Matchms is distributed through multiple channels including PyPI and Bioconda, as referenced in the contributing guidelines which specify procedures for release management and waiting for availability on Bioconda.: "Matchms is distributed through multiple channels including PyPI and Bioconda, as referenced in the contributing guidelines which specify procedures for release management and waiting for availability"
- [other] Wait until new release is also on Bioconda via a automaticly created PR on bioconda recipes repo: "Wait until new release is also on Bioconda via a automaticly created PR on bioconda recipes repo"
- [readme] Prerequisites: Python 3.10 - 3.14, (higher versions should work as well, but are not yet tested systematically): "Prerequisites: Python 3.10 - 3.14, (higher versions should work as well, but are not yet tested systematically)"
- [readme] Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data: "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data"
