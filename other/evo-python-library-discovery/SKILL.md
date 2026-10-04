---
name: evo-python-library-discovery
description: Detects Python libraries/packages in a directory by checking for pyproject.toml, setup.py, setup.cfg, or other standard Python project markers. Provides utilities to list library paths and analyze their structure, entry points, and key functions for testing.
---

# Python Library Discovery

This skill identifies Python library directories within a given base path and analyzes their public APIs to produce testing notes.

## Detection Heuristics

A subdirectory is considered a Python library if it contains any of:
- `pyproject.toml` (modern PEP 517/621 standard)
- `setup.py` (legacy setuptools)
- `setup.cfg` (legacy setuptools config)

## Key Functions

- `find_python_libraries(base_dir)` - Scan directory for Python libraries, returns list of absolute paths
- `analyze_library_api(lib_path)` - Analyze a library's public API and structure, returns dict
- `write_libraries_txt(libs, output_path)` - Write discovered libraries to a file
- `write_testing_notes(lib_info, output_path)` - Write testing notes for each library

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-python-library-discovery/scripts')
from discover import find_python_libraries, analyze_library_api, write_libraries_txt, write_testing_notes

libs = find_python_libraries("/app")
write_libraries_txt(libs, "/app/libraries.txt")
for lib in libs:
    info = analyze_library_api(lib)
    write_testing_notes(info, f"{lib}/notes_for_testing.txt")
```
