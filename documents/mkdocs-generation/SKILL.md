---
name: mkdocs-generation
description: Generate MkDocs documentation sites with Material theme, mkdocstrings for API docs, and versioning. Use when setting up or extending project documentation.
---

# MkDocs Documentation Generation

Generate professional documentation sites using MkDocs Material theme with automatic API reference generation.

## Stack

- **MkDocs**: Static site generator for project documentation
- **Material Theme**: Modern, responsive theme with navigation features
- **mkdocstrings**: Auto-generate API docs from Python docstrings
- **mike**: Version management for documentation

## Dependencies

Add to `pyproject.toml` (optional extras group):

```toml
[project.optional-dependencies]
docs = [
    "mkdocs>=1.5",
    "mkdocs-material>=9.4",
    "mkdocstrings[python]>=0.24",
    "mike>=2.0",
]
```

Or `requirements.txt`:

```
mkdocs>=1.5
mkdocs-material>=9.4
mkdocstrings[python]>=0.24
mike>=2.0
```

## Directory Structure

**Simple (flat)**:
```
docs/
├── index.md           # Home/overview
├── getting-started.md # Installation and quickstart
├── configuration.md   # Config options
└── tools.md          # Feature reference
```

**Complex (nested)**:
```
docs/
├── index.md
├── compatibility.md
├── guide/
│   ├── getting-started.md
│   ├── cli.md
│   └── advanced.md
└── api/
    ├── panel.md       # ::: module.Class
    └── entities/
        ├── area.md
        └── zone.md
```

## mkdocs.yml Configuration

See `templates/mkdocs.yml` for the full configuration template.

Key sections:
1. **Site metadata**: name, description, URLs
2. **Versioning**: mike provider for multi-version docs
3. **Theme**: Material with navigation features
4. **Plugins**: search + mkdocstrings for API docs
5. **Navigation**: Explicit nav structure

## API Reference with mkdocstrings

Create minimal markdown files that reference Python modules:

```markdown
# Panel API

::: mypackage.panel.Panel

::: mypackage.panel.PanelSync
```

mkdocstrings auto-generates documentation from docstrings. Configure in `mkdocs.yml`:
- `docstring_style: google` - Use Google-style docstrings
- `show_source: false` - Hide source code
- `merge_init_into_class: true` - Combine `__init__` with class docs
- `filters: ["!^_"]` - Exclude private members

## Commands

```bash
# Serve locally with hot-reload
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy

# Version management (mike)
mike deploy --push --update-aliases 0.1.0 latest
mike set-default --push latest
```

## Writing Guidelines

1. **index.md**: Brief overview, key features as bullet list, installation snippet, "Where to Next" links
2. **getting-started.md**: Prerequisites, step-by-step setup, minimal working example
3. **API docs**: Let mkdocstrings generate from docstrings; add brief intro if needed
4. **Guides**: Task-oriented, include code examples, link to related API docs

## Templates

- `templates/mkdocs.yml` - Configuration file
- `templates/index.md` - Home page
- `templates/getting-started.md` - Quickstart guide
- `templates/api-reference.md` - API doc page using mkdocstrings
