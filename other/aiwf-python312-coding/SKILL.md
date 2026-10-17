---
name: aiwf-python312-coding
description: Use for Python 3.12 code, packaging metadata, modern typing, stdlib changes, C-extension boundaries, and validation.
---

# AIWF Python 3.12 Coding

## Core Rule

Use Python 3.12 features only when the project actually targets Python 3.12 or gates them behind compatibility checks. Python 3.12 work should improve clarity or compatibility with the configured runtime, not quietly drop older supported interpreters.

## Workflow

1. Inspect `requires-python`, CI, tox/nox, lock files, Docker images, app launchers, and deployment scripts to confirm Python 3.12 is a supported or required target.
2. Check dependency wheels and native extensions before adopting 3.12-only behavior. Packaging and binary compatibility are often the real blocker.
3. Patch syntax, typing, async, and stdlib usage to match the supported version range.
4. For libraries, preserve older-version compatibility if metadata says `>=3.10` or `>=3.11`. Do not use 3.12-only syntax in shared code unless metadata is updated deliberately.
5. Validate with Python 3.12 and the repo-native checks.

## Python 3.12 Guardrails

- The Python 3.12 `type` statement and type-parameter syntax are 3.12-only. Do not use them in code that still supports 3.10 or 3.11.
- Account for `distutils` removal from the standard library. Prefer maintained packaging tools already used by the project.
- Python 3.12 virtual environments no longer install `setuptools` as a core dependency. Declare it when runtime code actually imports `setuptools` or `pkg_resources`; do not assume a fresh venv provides them.
- PEP 701 f-string parsing is more capable in 3.12; avoid relying on it when code must parse under 3.10 or 3.11.
- Keep `typing_extensions` usage consistent when the project spans multiple Python versions.
- For C extensions, inspect CPython API usage, limited API settings, wheel tags, and compiler/linker settings before changing build files.

## Validation Defaults

Prefer existing commands. Useful fallbacks:

```powershell
py -3.12 -m compileall <package-or-file>
py -3.12 -m pytest
py -3.12 -m pip check
```

For packaging changes:

```powershell
py -3.12 -m build
py -3.12 -m twine check dist/*
```

Use packaging commands only when those tools are already installed or the project expects them.

## Primary Source Anchors

- Python 3.12 documentation: https://docs.python.org/3.12/
- Python 3.12 "What's New": https://docs.python.org/3.12/whatsnew/3.12.html

When current maintenance status, packaging behavior, or stdlib details matter, verify the official Python docs before finalizing.
