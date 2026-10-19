---
name: sphinx-documentation
description: >
  Build, structure, and maintain technical documentation sites using Sphinx,
  reStructuredText (rST), MyST Markdown, and autodoc. Use when configuring conf.py,
  extracting API documentation from Python docstrings with sphinx-autodoc, managing
  toctrees and cross-references (:doc:, :ref:, :class:), applying modern themes
  like Furo, or hosting on Read the Docs.
compatibility: >
  Agent Skills-compatible coding agents configuring and building Sphinx documentation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "sphinx, rst, myst, autodoc, readthedocs, documentation, python"
  topics: "documentation, devtools, software-development"
---

# Sphinx Documentation & API Site Generation

Sphinx is the standard documentation generator for Python and many large open-source systems. Combining reStructuredText (rST) or MyST Markdown with extensions like `sphinx.ext.autodoc` and `sphinx.ext.intersphinx`, Sphinx extracts docstrings directly from source code and compiles comprehensive, searchable HTML documentation sites.

## Core Rules

1. **Use `toctree` for navigation hierarchy**: Every `.rst` or `.md` document must be included in a `.. toctree::` directive to avoid unlinked orphan document warnings.
2. **Never hardcode HTML anchors**: Use semantic cross-referencing roles (`:doc:`, `:ref:`, `:class:`, `:func:`) so references are validated at build time.
3. **Keep `conf.py` minimal and declarative**: Configure extensions, theme options, and Python paths cleanly.
4. **Treat doc build warnings as errors in CI**: Run `sphinx-build -W --keep-going` to catch broken links, missing docstrings, and syntax errors during CI.
5. **Support Markdown via MyST-Parser**: Enable `myst_parser` in `extensions` so contributors can write standard Markdown alongside rST files.

---

## 1. Project Layout & Configuration (`conf.py`)

Standard Sphinx directory structure:

```text
my-project/
├── docs/
│   ├── conf.py           # Sphinx configuration
│   ├── index.rst         # Root document / Table of Contents
│   ├── api/
│   │   └── core.rst      # Autodoc API reference
│   └── guides/
│       └── quickstart.md # MyST Markdown guide
├── .readthedocs.yaml     # Read the Docs hosting config
└── src/
    └── my_project/
```

### Minimal Modern `conf.py`
```python
import os
import sys
from pathlib import Path

# Add source directory to sys.path for autodoc
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

project = "DataPipeline"
copyright = "2026, Michael Weiss"
author = "Michael Weiss"
release = "1.2.0"

extensions = [
    "sphinx.ext.autodoc",       # Extract docstrings
    "sphinx.ext.napoleon",      # Support Google / NumPy docstring format
    "sphinx.ext.viewcode",      # Add links to highlighted source code
    "sphinx.ext.intersphinx",  # Link to standard library / external docs
    "myst_parser",             # Support Markdown files (.md)
]

# Intersphinx mapping to Python standard library
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Theme selection (Furo is modern, clean, and responsive)
html_theme = "furo"
html_title = f"{project} v{release}"
```

---

## 2. Root Index & Table of Contents (`index.rst`)

```rst
.. DataPipeline documentation master file

Welcome to DataPipeline
=======================

**DataPipeline** is a high-throughput streaming parser for structured datasets.

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   guides/quickstart
   guides/configuration

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/core

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

---

## 3. Automatic API Documentation with `autodoc` (`docs/api/core.rst`)

```rst
Core Module Reference
=====================

.. automodule:: my_project.core
   :members:
   :undoc-members:
   :show-inheritance:
```

---

## 4. Cross-Referencing Roles

- Link to a document: `:doc:`guides/quickstart``
- Link to an arbitrary target: `.. _target-anchor:` -> `:ref:`target-anchor``
- Link to a Python class: `:class:`my_project.core.Engine``
- Link to a Python function: `:func:`my_project.core.parse_data``

---

## 5. Read the Docs Hosting Configuration (`.readthedocs.yaml`)

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

sphinx:
  configuration: docs/conf.py
  fail_on_warning: true

python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - docs
```

---

## 6. Build Commands and Verification

```bash
# Build HTML documentation locally
sphinx-build -b html docs docs/_build/html

# Strict build (treat warnings as errors)
sphinx-build -W --keep-going -b html docs docs/_build/html

# Check for broken external links
sphinx-build -b linkcheck docs docs/_build/linkcheck
```

---

## 7. Verification Checklist

- [ ] `sphinx-build -W` finishes with zero warnings or errors.
- [ ] All `.rst` and `.md` files are registered in a `.. toctree::`.
- [ ] Source package is discoverable and `autodoc` generates methods without import errors.
- [ ] HTML output renders with search index and clean sidebar navigation.
- [ ] `linkcheck` reports zero dead external or internal hyperlinks.
