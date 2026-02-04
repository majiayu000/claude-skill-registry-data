---
name: cpython-docs
description: Use this skill when working with CPython documentation in the Doc/ tree, including reStructuredText (.rst) files, adding versionadded/versionchanged markers, creating Misc/NEWS.d entries for bug fixes or features, running documentation validation (make -C Doc check), or building HTML docs.
---

# CPython Documentation

CPython documentation is in reStructuredText (ReST) format in the `Doc/` tree.

## Documentation Tooling

```bash
# Set up documentation build environment
make -C Doc venv

# Validate documentation (run this to check your changes)
make -C Doc check

# Build HTML documentation (if full build is needed)
make -C Doc html
```

## Version Markers

**IMPORTANT**: When adding `versionadded::`, `versionchanged::`, or similar markers in documentation, always use `next` as the version "number". The doc build and release process fills this in appropriately.

```rst
.. versionadded:: next

.. versionchanged:: next
   Description of what changed.
```

## NEWS Entries

Bug fixes and new features require a `Misc/NEWS.d/next/` file entry.

**IMPORTANT**: The filename MUST refer to the correct GitHub Issue number in the upstream `python/cpython` repository. **Do not pick a number on your own!** Ask the user what issue number to use.

Example filename format: `Misc/NEWS.d/next/<category>/<YYYY-MM-DD-HH-MM-SS>.gh-issue-<NUMBER>.<UNIQUE_ID>.rst`
