---
name: dry-philosophy
description: |
  Don't Repeat Yourself (DRY) and Never Reinvent the Wheel (NRtW) - core b00t
  principles. Use existing libraries, leverage Rust via PyO3 instead of duplicating
  logic in Python, and contribute to upstream projects rather than fork privately.
version: 1.0.0
allowed-tools: Read, Grep, Glob, Bash, WebSearch
---

## What This Skill Does

The DRY philosophy is a central tenet of b00t: YEI exist to contribute ONLY new and novel meaningful work. This skill helps you:

- Identify when code is being duplicated or reinvented
- Find existing libraries instead of writing new code
- Use Rust functionality via PyO3 rather than duplicate in Python
- Contribute upstream rather than maintain private forks
- Write lean, maintainable code with minimal dependencies

## When It Activates

Activate this skill when you see:

- "implement [common functionality]"
- "create a [parser/validator/client]"
- "write code to [read/parse/validate] [format]"
- Any task that sounds like it might already exist in a library
- Code that duplicates existing Rust functionality
- Multiple implementations of the same logic

## Core Principles

### 1. DRY: Don't Repeat Yourself

**AVOID writing code for functionality that exists in libraries:**

❌ **Anti-pattern**:
```python
# Writing custom JSON parser
def parse_json(text):
    # 200 lines of parsing logic...
```

✅ **DRY approach**:
```python
import json
data = json.loads(text)
```

### 2. NRtW: Never Reinvent the Wheel

**SEARCH for existing solutions before coding:**

```bash
# Search for Python packages
pip search [functionality]
# or
uv pip search [functionality]

# Check PyPI
https://pypi.org/search/?q=[functionality]

# Check Rust crates
https://crates.io/search?q=[functionality]
```

### 3. Leverage Rust via PyO3

**USE Rust for heavy lifting, expose to Python:**

❌ **Anti-pattern**:
```python
# Duplicating Rust datum parsing in Python
def parse_datum_file(path: str) -> dict:
    with open(path) as f:
        toml_data = toml.load(f)
    # Validation logic...
    # Parsing logic...
    return processed_data
```

✅ **DRY approach**:
```python
# Use Rust via PyO3
import b00t_py
datum = b00t_py.load_ai_model_datum("model-name", "~/.dotfiles/_b00t_")
```

**Why?** Rust implementation already exists, is faster, type-safe, and tested.

### 4. Contribute Upstream

**FORK and PATCH forward, don't maintain private copies:**

❌ **Anti-pattern**:
```bash
# Copy library code into project
cp -r /path/to/library my_project/vendored/
# Make private modifications
```

✅ **DRY approach**:
```bash
# Fork the library
gh repo fork upstream/library

# Create patch
git checkout -b fix/issue-123
# Make changes
git commit -m "fix: resolve issue #123"

# Submit PR
gh pr create --upstream

# Use your fork temporarily
# pyproject.toml
dependencies = [
    "library @ git+https://github.com/you/library@fix/issue-123"
]
```

## Decision Tree

```
Need to implement functionality?
    ↓
Does it already exist in a library?
    ├─ YES → Use the library (DRY)
    └─ NO ↓
           Is it standard functionality?
               ├─ YES → Search harder, it probably exists
               └─ NO ↓
                      Does similar Rust code exist in b00t?
                          ├─ YES → Expose via PyO3 (DRY)
                          └─ NO ↓
                                 Is this truly novel?
                                     ├─ YES → Implement (with tests!)
                                     └─ NO → Reconsider: use library
```

## Examples

### Finding Libraries

**Task**: Parse TOML files

```bash
# Search
pip search toml

# Results: tomli, tomlkit, pytoml
# Use established: tomli (or tomllib in Python 3.11+)
```

**Task**: Make HTTP requests

```bash
# DON'T: Write custom HTTP client
# DO: Use httpx or requests
pip install httpx
```

**Task**: Validate Pydantic models

```bash
# DON'T: Write custom validation
# DO: Use Pydantic's built-in validation
from pydantic import BaseModel, field_validator
```

### Using Rust via PyO3

**b00t Pattern**: Rust does heavy lifting, Python uses it.

#### Datum Operations

❌ **Duplicate** (Anti-pattern):
```python
# b00t_j0b_py/datum_parser.py
import toml

class DatumParser:
    def load_provider(self, name: str):
        path = f"~/.dotfiles/_b00t_/{name}.ai.toml"
        with open(os.path.expanduser(path)) as f:
            data = toml.load(f)
        # Validation...
        # Parsing...
        return data
```

✅ **DRY** (Use Rust):
```python
# Use PyO3 bindings
import b00t_py

datum = b00t_py.load_ai_model_datum("model-name", "~/.dotfiles/_b00t_")
```

**Why better?**
- ✅ No duplication - single source of truth in Rust
- ✅ Type-safe - Rust ensures correctness
- ✅ Tested - Rust tests cover this
- ✅ Faster - Rust performance
- ✅ Maintainable - one codebase, not two

#### Environment Validation

❌ **Duplicate**:
```python
def validate_provider_env(provider: str) -> bool:
    # Read datum
    # Parse required env vars
    # Check os.environ
    # Return result
```

✅ **DRY**:
```python
import b00t_py

validation = b00t_py.check_provider_env("openrouter", "~/.dotfiles/_b00t_")
if not validation["available"]:
    print(f"Missing: {validation['missing_env_vars']}")
```

### Contributing Upstream

**Scenario**: Bug in `pydantic-ai` library

❌ **Anti-pattern**:
```bash
# Copy code into project
cp -r site-packages/pydantic_ai b00t_j0b_py/vendored/
# Fix bug privately
# Now you maintain a fork forever
```

✅ **DRY approach**:
```bash
# Fork
gh repo fork pydantic/pydantic-ai

# Fix and test
git checkout -b fix/agent-validation-bug
# Make changes
pytest tests/
git commit -m "fix: agent validation for None values"

# Submit PR
gh pr create --title "fix: agent validation for None values"

# Temporarily use your fork
# pyproject.toml
dependencies = [
    "pydantic-ai @ git+https://github.com/elasticdotventures/pydantic-ai@fix/agent-validation-bug"
]

# After PR merged, switch back to upstream
dependencies = [
    "pydantic-ai>=0.0.15"  # includes fix
]
```

## Library Selection Criteria

When choosing a library:

### ✅ Good Signs

- ✅ Many stars (>1000 on GitHub)
- ✅ Active maintenance (commits in last month)
- ✅ Minimal open issues/PRs
- ✅ Good documentation
- ✅ Permissive license (MIT, Apache, BSD)
- ✅ Used by major projects
- ✅ Type hints (Python) or strong types (Rust)
- ✅ Comprehensive tests
- ✅ Lively, polite community discussions

### 🚩 Red Flags

- 🚩 Abandoned (no commits in 1+ years)
- 🚩 Many unresolved issues
- 🚩 No tests
- 🚩 Copyleft license (GPL) for permissive projects
- 🚩 No type hints
- 🚩 Breaking changes without semver
- 🚩 Hostile maintainers

## PyO3 Pattern

### When to Use Rust (via PyO3)

Use Rust for:
- ✅ Performance-critical code
- ✅ Type-safe validation
- ✅ Complex parsing
- ✅ Shared logic between Rust and Python
- ✅ System-level operations

### How to Expose Rust to Python

```rust
// b00t-py/src/lib.rs
use pyo3::prelude::*;

#[pyfunction]
fn my_function(py: Python<'_>, arg: &str) -> PyResult<String> {
    // Rust implementation
    Ok(format!("Processed: {}", arg))
}

#[pymodule]
fn b00t_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(my_function, m)?)?;
    Ok(())
}
```

```python
# Python usage
import b00t_py

result = b00t_py.my_function("test")
```

## Code Review Checklist

Before writing code, ask:

1. ☐ Does this functionality exist in a library?
2. ☐ Does similar Rust code exist in b00t?
3. ☐ Can I use PyO3 to expose Rust instead?
4. ☐ Is this truly novel functionality?
5. ☐ Have I searched PyPI/crates.io?
6. ☐ Have I checked existing b00t modules?

If all answers are "no", then implement.

## Anti-Patterns to Avoid

### 1. Reinventing Standard Library

❌ **Bad**:
```python
def read_json_file(path):
    with open(path) as f:
        return custom_json_parse(f.read())
```

✅ **Good**:
```python
import json

def read_json_file(path):
    with open(path) as f:
        return json.load(f)
```

### 2. Duplicating Rust Logic

❌ **Bad**:
```python
# Reimplementing datum validation in Python
class DatumValidator:
    def validate_env(self, provider): ...
    def parse_toml(self, path): ...
```

✅ **Good**:
```python
# Use Rust via PyO3
import b00t_py
validation = b00t_py.check_provider_env(provider, path)
```

### 3. Private Forks

❌ **Bad**:
```bash
# Fork library, never contribute back
# Maintain private version forever
```

✅ **Good**:
```bash
# Fork, fix, PR upstream
# Use fork temporarily until merged
# Switch back to upstream after merge
```

### 4. Not Using Type Hints

❌ **Bad**:
```python
def process_data(data):
    # No types, unclear what's expected
    return data.transform()
```

✅ **Good**:
```python
from pydantic import BaseModel

def process_data(data: dict[str, Any]) -> ProcessedData:
    return ProcessedData(**data)
```

## Benefits of DRY

1. **Less code to maintain** - fewer bugs, faster development
2. **Better quality** - libraries are tested by many users
3. **Security updates** - library maintainers handle CVEs
4. **Performance** - Rust is faster than Python for heavy tasks
5. **Type safety** - Rust ensures correctness
6. **Community** - contribute to ecosystem, get help

## Related Skills

- **datum-system**: Uses Rust via PyO3 (DRY example)
- **direnv-pattern**: Uses existing direnv tool (DRY)
- **justfile-usage**: Uses casey/just tool (DRY)

## References

- `CLAUDE.md` - YEI MUST ALWAYS/NEVER section
- `b00t-py/src/lib.rs` - PyO3 bindings example
- `b00t-j0b-py/pyproject.toml` - Dependency management

## Summary

**DRY Philosophy**:
- 🔍 Search for existing solutions first
- 📦 Use established libraries over custom code
- 🦀 Leverage Rust via PyO3 instead of duplicating in Python
- 🔄 Fork, fix, PR upstream - don't maintain private copies
- ✅ Write only novel, meaningful code
- 🧪 Test everything you write

**Alignment**: A lean hive is a happy hive. Finding and patching bugs in libraries is divine; committing buggy code is unforgivable.
