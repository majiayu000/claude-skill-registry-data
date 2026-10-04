---
name: evo-fuzz-env-runner
description: Sets up Python virtual environments using uv for each library, installs dependencies from project configuration files, and executes the fuzzer for a specified duration with proper log redirection.
---

# Fuzz Environment Runner

Sets up isolated Python virtual environments using `uv`, installs library dependencies and atheris, runs fuzz.py with LibFuzzer flags, and captures output to fuzz.log.

## Workflow

1. Create .venv using `uv venv .venv` in each library directory
2. Install atheris and library dependencies via `uv pip install`
3. Run fuzzer with `-max_total_time=10` flag
4. Capture stdout+stderr to fuzz.log

## Key Functions

- `setup_venv_with_uv(lib_path)` - Create virtual environment
- `install_dependencies(lib_path, venv_path)` - Install deps and atheris
- `run_fuzzer_with_timeout(lib_path, timeout_seconds=10)` - Run fuzzer and log output
- `capture_fuzz_log(lib_path)` - Read fuzz.log contents

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-fuzz-env-runner/scripts')
from runner import setup_venv_with_uv, install_dependencies, run_fuzzer_with_timeout

venv = setup_venv_with_uv('/app/arrow')
install_dependencies('/app/arrow', venv)
run_fuzzer_with_timeout('/app/arrow', timeout_seconds=10)
```
