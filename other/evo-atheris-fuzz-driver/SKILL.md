---
name: evo-atheris-fuzz-driver
description: Creates Atheris-based coverage-guided fuzz drivers for Python libraries using FuzzedDataProvider for structured input generation. Includes templates and patterns for different library types (parsers, formatters, serializers, ML frameworks).
---

# Atheris Fuzz Driver Generator

Generates fuzz.py harness files for Python libraries with proper Atheris instrumentation, FuzzedDataProvider usage, and exception handling.

## Driver Design Principles

1. Import target library inside `atheris.instrument_imports()` context manager
2. Use `FuzzedDataProvider` to generate structured typed inputs
3. Catch only expected exceptions (ValueError, TypeError, domain-specific errors)
4. Guard with `if __name__ == "__main__":` block
5. Use `atheris.Setup(sys.argv, TestOneInput)` then `atheris.Fuzz()`

## Supported Libraries

- **arrow**: Date/time parsing, timestamp boundary testing
- **black**: Code formatting with Mode configuration
- **ipython**: Input transformation pipeline
- **minisgl**: JSON/msgpack parsing (lightweight targets)
- **ujson**: Differential fuzzing against stdlib json

## Key Functions

- `generate_fuzz_driver(lib_path)` - Generate and write fuzz.py for a library
- `get_driver_template(lib_name)` - Get driver source code for a library
- `get_exception_handlers_for_lib(lib_name)` - Get expected exceptions list
- `create_fuzz_driver_file(lib_path, lib_name)` - Write fuzz.py to disk

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-atheris-fuzz-driver/scripts')
from fuzz_driver import generate_fuzz_driver, create_fuzz_driver_file

generate_fuzz_driver('/app/arrow')
generate_fuzz_driver('/app/black')
```
