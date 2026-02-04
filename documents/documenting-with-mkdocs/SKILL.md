---
name: documenting-with-mkdocs
description: Project documentation with MkDocs Material - consistent structure, API auto-generation, GitHub Pages deployment
---

# Documenting with MkDocs

## Purpose

Comprehensive project documentation using **MkDocs Material**. Works for any project type: libraries, applications, services.

## Structure

```
docs/
├── index.md                    # Landing page
├── getting-started/
│   ├── installation.md
│   └── quickstart.md
├── guides/
│   ├── architecture.md
│   └── core-concepts.md
├── reference/                  # Components/modules
│   └── feature-name.md
├── examples/
│   └── example-1.md
└── api/                        # Auto-generated (libraries)
    └── module.md
```

## mkdocs.yml

```yaml
site_name: Project Name
site_url: https://username.github.io/repo/
repo_url: https://github.com/username/repo

theme:
  name: material
  palette:
    - media: "(prefers-color-scheme)"
      scheme: default
      primary: indigo
      toggle:
        icon: material/brightness-7
        name: Dark mode
    - scheme: slate
      primary: indigo
      toggle:
        icon: material/brightness-4
        name: Light mode
  features:
    - navigation.sections
    - content.code.copy
    - search.suggest

plugins:
  - search

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - admonition

nav:
  - Home: index.md
  - Getting Started:
      - Installation: getting-started/installation.md
      - Quick Start: getting-started/quickstart.md
  - Reference:
      - Feature: reference/feature.md
```

## API Auto-Generation

**Python (mkdocstrings):**
```yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
            docstring_style: google
```

```toml
# pyproject.toml
[project.optional-dependencies]
docs = ["mkdocs-material>=9.5", "mkdocstrings[python]>=0.24"]
```

**TypeScript:**
```bash
npx typedoc --plugin typedoc-plugin-markdown --out docs/api
```

**Rust/Go:** Link to docs.rs or pkg.go.dev

## Justfile Commands

```just
# Serve docs locally
docs-serve:
    uv run mkdocs serve --dev-addr 0.0.0.0:8000

# Build docs
docs-build:
    uv run mkdocs build

# Deploy to GitHub Pages
docs-deploy:
    uv run mkdocs gh-deploy --force
```

## GitHub Pages

**.github/workflows/docs.yml:**
```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]
    paths: ['docs/**', 'mkdocs.yml']

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install mkdocs-material
      - run: mkdocs gh-deploy --force
```

## Landing Page Template

```markdown
# Project Name

**Brief tagline**

One-paragraph description.

## Key Features

- **Feature 1** - Description
- **Feature 2** - Description

## Quick Example

\`\`\`python
# Complete, runnable example (< 20 lines)
\`\`\`

## Installation

\`\`\`bash
pip install project-name
\`\`\`

## Next Steps

- [Installation Guide](getting-started/installation.md)
- [Quick Start](getting-started/quickstart.md)
```

## Content Guidelines

**Guides:**
- Start with "Why" (motivation)
- Include diagrams
- Complete code examples
- Link to API docs

**Reference:**
- Feature purpose
- Parameters/options
- Code examples
- Common patterns

**Quality:**
- `docs-build` succeeds without warnings
- All internal links work
- Code examples tested
- Dark/light mode work
