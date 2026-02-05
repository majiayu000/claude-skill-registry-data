---
name: cpython-code-style
description: Use this skill when writing or modifying CPython code, preparing commits, or running style checks. Covers PEP 7 (C code) and PEP 8 (Python) compliance, pre-commit hooks, patchcheck validation, trailing whitespace rules, the no-type-annotations-in-Lib policy, and documentation formatting standards.
---

# CPython Coding Style and Standards

## Style Guidelines

**Python code** (`Lib/` etc): Follow PEP 8. Be consistent with nearby code.

**C code** (`Modules/`, `Objects/`, `Python/`, `Include/`): Follow PEP 7. Be consistent with nearby code.

## Critical Rules

**NEVER leave trailing whitespace on any line.** Pre-commit hooks will catch this.

**ALWAYS preserve the final newline** at the end of files.

**NEVER add type annotations to `Lib/` tree.** Stdlib doesn't use inline annotations (maintained in typeshed separately). Annotations may be OK in `Tools/` or test code if requested.

**No autoformatting by default.** Only use `Doc/venv/bin/ruff format` if explicitly requested.

## Pre-Commit Workflow

Before committing, run from repo root:

```bash
# 1. Pre-commit hooks (checks whitespace, file endings, syntax)
pre-commit run --all-files

# 2. Patchcheck (MUST PASS - validates C/Python style, docs, whitespace)
make -C $BUILD_DIR patchcheck

# 3. If you modified Doc/, verify reStructuredText
make -C Doc check

# 4. Run relevant tests
$BUILT_PY -m test test_yourmodule -j $(nproc)
```

## Documentation

- **Python docstrings**: Follow PEP 257, document params/returns/exceptions
- **C comments**: Follow PEP 7, document complex algorithms
- **reStructuredText** (`Doc/`): Follow Sphinx/reST conventions, verify with `make -C Doc check`
