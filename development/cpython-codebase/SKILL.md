---
name: cpython-codebase
description: Use this skill when working in the CPython repository. It provides essential context about the CPython codebase structure, recommended tools, source code navigation, and best practices for maintaining engineering notebooks while working on Python runtime and standard library development.
---

# CPython Codebase

You are working in the CPython repository - the implementation of the Python language runtime and standard library itself.

## Recommended Tools

Prefer these tools when available: `rg`, `gh`, `jq`

## Source Code Structure

**`Lib/`** - Python standard library (pure Python). Example: `Lib/zipfile.py`

**`Modules/`** - C extension modules for performance/low-level access. Example: `Modules/_csv.c`

**`Objects/` and `Python/`** - Core types (list, dict, int), builtins, runtime, interpreter loop

**`Include/`** - C header files for public and internal C APIs

**`Lib/test/`** - All unittests
- Test naming: `test_{module_name}.py` or `test_{module_name}/`
- Examples: `Lib/zipfile.py` → `Lib/test/test_zipfile**`, `Modules/_csv.c` → `Lib/test/test_csv.py`
- Test packages require `load_tests()` in `test_package/__init__.py` to work with `python -m test`

**`Doc/`** - Documentation in .rst format (source for python.org docs), builds to `Doc/build/`

**`InternalDocs/`** - Maintainer documentation (`InternalDocs/README.md` is the starting point)

**`Tools/`** - Build tools like Argument Clinic, development utilities

## Argument Clinic

**`**/clinic/**` subdirectories are auto-generated** - never edit these directly. See `cpython-build-and-test` skill for regeneration commands.

## Engineering Notebooks

ALWAYS load and maintain notebooks when working on features or PRs:
- **For PRs**: `.claude/pr-{PR_NUMBER}.md`
- **For branches**: `.claude/branch-{branch_name_without_slashes}.md` (when not on `main`)

Keep notebooks updated with learnings and project state as you work and after commits. Include: problem statement, key findings, file locations, design decisions, testing strategy, and status.

## Scratch Space

**NEVER create throwaway files in repo root.** Use `.claude/sandbox/` for exploration files, test scripts, and prototypes.

## Optional Developer Resources

- **Developer Guide**: If `REPO_ROOT/../devguide/` exists, see `developer-workflow/` and `documentation/` subdirectories
- **PEPs**: May exist in `REPO_ROOT/../peps/` tree - reference relevant PEPs when working on changes
