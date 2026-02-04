---
name: maturin-debugger
description: Diagnose and fix maturin build issues for PyO3 Python bindings. Use when encountering problems with maturin develop, missing Python exports, module registration errors, or type stub generation issues. Particularly useful when new PyO3 methods compile but don't appear in Python.
---

# Maturin Debugger

## Overview

Provide systematic debugging workflows for maturin and PyO3 development issues, with particular focus on the known caching problem where new methods compile successfully but don't appear in Python.

## When to Use This Skill

Use this skill when encountering:

- New `#[pymethods]` functions that compile but don't appear in Python's `dir()` or `hasattr()`
- Module import failures despite successful Rust compilation
- `maturin develop` caching issues that persist after `cargo clean`
- Questions about whether classes are properly registered in `#[pymodule]`
- Type stub generation or mypy type checking problems
- General confusion about maturin build vs develop workflows

## Debugging Decision Tree

```
Is the issue related to maturin/PyO3?
├─ Yes → Continue with workflow below
└─ No → Exit skill

Can the code compile successfully with `cargo build`?
├─ No → Fix Rust compilation errors first (outside this skill)
└─ Yes → Continue

Does the issue involve new methods/classes not appearing in Python?
├─ Yes → ⚠️ CHECK STEP 0 FIRST (UV + Maturin Conflict) - 90% of issues!
│        Then proceed to "Missing Methods Workflow"
└─ No → Continue

Is it an import error?
├─ Yes → Jump to "Import Debugging Workflow"
└─ No → Jump to "General Diagnostic Workflow"
```

## ⚠️ Priority Checklist - Most Common Issues First

Before diving into complex debugging, check these in order:

1. **UV + Maturin Conflict** (90% of "methods not appearing" issues)
   - Are you using `uv run python` after `maturin develop`?
   - → Jump to "Missing Methods Workflow Step 0"

2. **Maturin Develop Caching** (9% of remaining issues)
   - Have you added new methods to existing classes?
   - → Jump to "Missing Methods Workflow Step 2"

3. **Module Registration** (1% of remaining issues)
   - Have you added new `#[pyclass]` types?
   - → Jump to "Missing Methods Workflow Step 1"

## Missing Methods Workflow

**Scenario**: New `#[pymethods]` compile successfully but don't appear in Python.

### Step 0: ⚠️ CRITICAL - Check for UV + Maturin Conflict

**This is the #1 cause of methods not appearing** - Before anything else, verify you're not mixing `uv run` with maturin builds.

**Problem**: [PyO3/maturin#2314](https://github.com/PyO3/maturin/issues/2314) - UV may reinstall cached packages after maturin builds, causing fresh code to never load.

**Symptoms**:

- Code compiles successfully without errors
- New methods/classes don't appear despite being in source
- `hasattr(obj, 'new_method')` returns `False`
- Even after `cargo clean` + rebuild, old code still loads
- You see: `Uninstalled 1 package in 1ms` / `Installed 1 package in 2ms` when running Python

**THE SOLUTION - Never Mix `maturin develop` with `uv run python`**:

```bash
# ✅ CORRECT WORKFLOW (from Python package directory)

# Step 1: Remove old venv (if troubleshooting)
rm -rf .venv && uv venv

# Step 2: Build wheel (NOT develop)
uv run --with maturin --with patchelf maturin build --release

# Step 3: Install wheel with uv pip
uv pip install ../target/wheels/<package>-*.whl --force-reinstall

# Step 4: Test using venv Python DIRECTLY (not uv run!)
.venv/bin/python -c "from your_module import YourClass"
.venv/bin/python -m pytest tests/

# ❌ WRONG - DO NOT DO THIS:
maturin develop
uv run python  # This reinstalls from cache, wiping out your fresh build!
```

**Debugging Checklist**:

1. **Check binary contents**:
   ```bash
   strings .venv/lib/python*/site-packages/your_module/*.so | grep "your_new_method"
   ```

2. **Check file timestamps**:
   ```bash
   ls -lh .venv/lib/python*/site-packages/your_module/*.so
   ls -lh src/your_modified_file.rs
   # If .so is older than source, it wasn't updated!
   ```

3. **Check where Python is loading from**:
   ```bash
   .venv/bin/python -c "import your_module; print(your_module.__file__)"
   ```

4. **Nuclear option - fresh venv**:
   ```bash
   rm -rf .venv
   uv venv
   uv run --with maturin maturin build --release
   uv pip install ../target/wheels/*.whl
   .venv/bin/python  # Test with venv Python directly
   ```

**Key Rules**:

- ✅ Use `maturin build` + `uv pip install` + `.venv/bin/python`
- ❌ Never use `uv run python` after maturin operations
- ✅ Check binary contents and timestamps when debugging
- ❌ Don't trust that `--force-reinstall` actually reinstalls with uv
- ✅ Use fresh venv when in doubt

If this solves the issue, **STOP HERE**. Otherwise, continue to Step 1.

### Step 1: Verify Module Registration

Run the verification script to check if all `#[pyclass]` types are registered:

```bash
python scripts/verify_module_registration.py
```

**Expected output**: Script reports all classes are registered, or lists missing registrations with fix suggestions.

**If classes are missing from registration**:

1. Add them to the `#[pymodule]` function:
   ```rust
   #[pymodule]
   fn your_module(m: &Bound<'_, PyModule>) -> PyResult<()> {
       m.add_class::<YourMissingClass>()?;
       Ok(())
   }
   ```
2. Rebuild with `uv run --with maturin maturin develop`
3. Re-test in Python

**If all classes are registered**, proceed to Step 2.

### Step 2: Apply Known Caching Issue Workaround

This is the **most common cause** of missing methods. `maturin develop` has a known caching bug (PyO3/maturin#381) where new methods don't export properly.

**Solution - Full Rebuild Sequence**:

```bash
# From the Python package directory
cargo clean -p <package-name>
uv run --with maturin --with patchelf maturin build --release
uv pip install target/wheels/<package-name>-*.whl --force-reinstall
```

Replace `<package-name>` with the actual Rust package name from `Cargo.toml`.

### Step 3: Verify Fix in Python

```python
# Test that the class and methods are accessible
import your_module
print('YourClass' in dir(your_module))  # Should be True

from your_module import YourClass
instance = YourClass()
print(hasattr(instance, 'your_new_method'))  # Should be True
```

**If still failing**:

1. Verify `#[pyclass]` and `#[pymethods]` are in the **same Rust file**
2. Check there are no typos in the method name
3. Ensure method is marked `pub` if needed
4. Review `references/maturin_best_practices.md` for additional edge cases

## Import Debugging Workflow

**Scenario**: `ImportError` or `ModuleNotFoundError` when trying to import.

### Step 1: Run Diagnostic Script

```bash
python scripts/diagnose_maturin.py <module_name> [ExpectedClass1] [ExpectedClass2]
```

Example:

```bash
python scripts/diagnose_maturin.py pubmed_client Client PubMedClient SearchQuery
```

**Script checks**:

- Build artifacts (`.so` and `.whl` files)
- Module import success/failure
- Exported symbols from both package and `.so` submodule
- Presence of expected classes

### Step 2: Analyze Output

**If no build artifacts found**:

```bash
uv run --with maturin maturin develop
```

**If `.so` file exists but import fails**:

- Check `module-name` in `pyproject.toml` matches expected import path
- Verify Python version compatibility (`python --version`)
- Check for conflicting installations: `uv pip list | grep <package>`

**If module imports but classes are missing**:

- Return to "Missing Methods Workflow" Step 1 (module registration)

### Step 3: Check for Cache Issues

Python caches imported modules. After rebuilding:

```python
# Option 1: Restart Python interpreter (recommended)
exit()  # then restart

# Option 2: Use importlib.reload()
import importlib
import your_module
importlib.reload(your_module)
```

## General Diagnostic Workflow

For issues not covered above, follow this systematic approach:

### 1. Check Build Status

```bash
# Clean build from scratch
cargo clean -p <package-name>
uv run --with maturin maturin develop --release

# Verify compilation succeeded
echo $?  # Should output: 0
```

### 2. Run Full Diagnostic

```bash
python scripts/diagnose_maturin.py <module_name>
```

Review all sections of the output for anomalies.

### 3. Verify Module Structure

Check that the package structure matches expectations:

```bash
# From the Python package directory
tree -L 3 target/wheels  # Check .whl structure
unzip -l target/wheels/*.whl  # Inspect .whl contents
```

Expected structure:

```
your_package/
├── __init__.py
├── your_module.cpython-*.so
└── py.typed
```

### 4. Test Step-by-Step

Test progressively from lowest to highest level:

```python
# Level 1: Import .so directly
import your_package.your_module as so
print(dir(so))

# Level 2: Import package
import your_package
print(dir(your_package))

# Level 3: Import specific class
from your_package import YourClass
print(dir(YourClass))

# Level 4: Instantiate and use
instance = YourClass()
print(hasattr(instance, 'expected_method'))
```

Identify at which level the failure occurs, then investigate that specific layer.

## Type Stubs and Mypy Issues

**Scenario**: Type checking fails or IDE autocomplete doesn't work.

### Regenerate Type Stubs

```bash
# From the Python package directory
cargo run --bin stub_gen

# Copy to correct location (adjust path as needed)
cp your_package/your_module.pyi your_module.pyi
```

### Verify Type Stub Accuracy

```bash
# Run mypy on tests
uv run mypy tests/ --strict

# If errors occur, compare stub with runtime:
python -c "from your_module import YourClass; print(dir(YourClass))"
# vs.
grep "class YourClass" your_module.pyi -A 20
```

**If stubs don't match runtime**:

1. Ensure `#[gen_stub_pyclass]` and `#[gen_stub_pymethods]` macros are applied
2. For complex types, implement custom `PyStubType` (see `references/maturin_best_practices.md`)
3. Regenerate stubs after fixing

## Quick Reference: Common Commands

### Development Iteration (Fast)

```bash
uv run --with maturin maturin develop
uv run pytest tests/
```

### Production Build (For Publishing)

```bash
uv run --with maturin maturin build --release
```

### Nuclear Option (When All Else Fails)

```bash
cargo clean
rm -rf target/
uv pip uninstall <package-name>
uv run --with maturin --with patchelf maturin build --release
uv pip install target/wheels/<package-name>-*.whl --force-reinstall
```

### Verification Commands

```bash
# Check what's installed
uv pip show <package-name>

# List package contents
python -c "import <module>; print(dir(<module>))"

# Check .so location
python -c "import <module>; print(<module>.__file__)"
```

## Resources

### scripts/

**diagnose_maturin.py**: Comprehensive diagnostic tool that checks build artifacts, module exports, and suggests rebuild steps. Run with module name and expected class names.

**verify_module_registration.py**: Scans Rust source files to verify all `#[pyclass]` types are registered in the `#[pymodule]` function. Reports missing registrations with exact fix code.

### references/

**maturin_best_practices.md**: Detailed reference covering the known maturin caching issue, module registration rules, type stub generation, common pitfalls, and debugging strategies. Load this into context for deep-dive troubleshooting or when implementing new PyO3 bindings.

## Success Indicators

After following these workflows, verify:

- ✅ All expected classes appear in `dir(module)`
- ✅ `hasattr(instance, 'method')` returns `True` for all methods
- ✅ Direct imports work: `from module import ClassName`
- ✅ Type stubs match runtime behavior (`mypy` passes)
- ✅ All pytest tests pass
- ✅ No import errors or module not found errors

If any of these fail, revisit the appropriate workflow above or consult `references/maturin_best_practices.md` for edge cases.
