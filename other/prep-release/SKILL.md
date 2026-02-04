---
name: prep_release
description: バージョン更新、CHANGELOG整備、パッケージビルドなど、リリース前の準備を行う
---

# Prepare Release

This skill automates the steps required to prepare a new version release.

## Instructions

1.  **Update Version**:
    *   Ask the user for the new version number (e.g. `0.4.1`).
    *   Update `version` in `pyproject.toml`.
    *   Update `__version__` variable in `gwexpy/__init__.py` if it exists.

2.  **Update Changelog**:
    *   Read `CHANGELOG.md`.
    *   Create a new header for the new version with the current date.
    *   Move "Unreleased" changes under this new header.

3.  **Build Package**:
    *   Clean old distribution files: `rm -rf dist/ build/ *.egg-info`.
    *   Run build command: `python -m build`.
    *   Check if correct `.tar.gz` and `.whl` files are created in `dist/`.

4.  **Verify**:
    *   (Optional) Run `twine check dist/*` to verify metadata validation if `twine` is available.
