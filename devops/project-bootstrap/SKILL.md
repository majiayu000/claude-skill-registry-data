---
name: project-bootstrap
description: Bootstrap open-source projects with documentation, CI/CD, and polish. Use when user asks to "set up docs", "add MkDocs", "create GitHub Actions", "add funding", "polish README", "add Giscus comments", "bootstrap project", or wants to improve project presentation and infrastructure.
---

# Project Bootstrap

Bootstrap open-source projects with professional documentation, CI/CD, and polish.

## Components

| Component | What it does |
|-----------|--------------|
| **MkDocs** | Material theme docs with tabs, code copy, dark mode |
| **GitHub Actions** | Auto-deploy docs on push to main |
| **Giscus** | GitHub Discussions-based comments on docs |
| **README** | Polished README with badges, tables, examples |
| **Funding** | Ko-fi badge, GitHub Sponsors |

## Quick Reference

### MkDocs Setup

Create `mkdocs.yml`:

```yaml
site_name: Project Name
site_url: https://ninyawee.github.io/REPO
repo_url: https://github.com/ninyawee/REPO

theme:
  name: material
  custom_dir: docs/overrides
  palette:
    - scheme: default
      primary: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - content.code.copy
    - navigation.sections
    - navigation.expand

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - tables
  - admonition
  - pymdownx.details

nav:
  - Home: index.md
  - Getting Started: getting-started.md
```

Add mise task:

```toml
[tasks."docs:serve"]
run = "uv run --with mkdocs-material mkdocs serve"

[tasks."docs:build"]
run = "uv run --with mkdocs-material mkdocs build"
```

### GitHub Actions - Docs Deploy

Create `.github/workflows/docs.yml`:

```yaml
name: Deploy Docs

on:
  push:
    branches: [main]
    paths: ['docs/**', 'mkdocs.yml', '.github/workflows/docs.yml']
  workflow_dispatch:

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install mkdocs mkdocs-material
      - run: mkdocs gh-deploy --force
```

### Giscus Comments

**Prerequisites** (Giscus requires public repo with Discussions enabled):

```bash
# Enable discussions
gh repo edit ninyawee/REPO --enable-discussions

# Verify repo is public and discussions enabled
gh repo view ninyawee/REPO --json visibility,hasDiscussionsEnabled
```

**Setup steps:**

1. Run the commands above to enable discussions
2. Go to https://giscus.app and enter repo name
3. Copy `data-repo-id` and `data-category-id`

Create `docs/overrides/main.html`:

```html
{% extends "base.html" %}

{% block content %}
  {{ super() }}

  <h2 id="__comments">{{ lang.t("meta.comments") }}</h2>

  <script
    src="https://giscus.app/client.js"
    data-repo="ninyawee/REPO"
    data-repo-id="REPO_ID_FROM_GISCUS"
    data-category="General"
    data-category-id="CATEGORY_ID_FROM_GISCUS"
    data-mapping="pathname"
    data-strict="0"
    data-reactions-enabled="1"
    data-emit-metadata="0"
    data-input-position="bottom"
    data-theme="preferred_color_scheme"
    data-lang="en"
    data-loading="lazy"
    crossorigin="anonymous"
    async
  ></script>
{% endblock %}
```

### README Polish

#### Docs Link (add after description)

```markdown
📖 **[Documentation](https://ninyawee.github.io/REPO/)**
```

#### Badges

```markdown
[![PyPI](https://img.shields.io/pypi/v/PACKAGE)](https://pypi.org/project/PACKAGE/)
[![npm](https://img.shields.io/npm/v/PACKAGE)](https://www.npmjs.com/package/PACKAGE)
[![crates.io](https://img.shields.io/crates/v/PACKAGE)](https://crates.io/crates/PACKAGE)
[![Documentation](https://img.shields.io/badge/docs-ninyawee.github.io%2FREPO-blue)](https://ninyawee.github.io/REPO)
[![License](https://img.shields.io/github/license/ninyawee/REPO)](LICENSE)
```

#### Structure Pattern

1. **Title** with Thai meaning if applicable
2. **Badges** row (optional)
3. **One-liner** tagline (Thai + English for Thai projects)
4. **Docs link** `📖 **[Documentation](https://ninyawee.github.io/REPO/)**`
5. **Packages table** (if multi-package)
6. **Quick example** code block
7. **Installation** section
8. **Usage** examples
9. **Support/Funding** section
10. **License**

See `references/readme-template.md` for full example.

### Funding

#### Ko-fi Badge

```markdown
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20me%20☕-ff5f5f?logo=ko-fi&logoColor=white)](https://ko-fi.com/ninyawee)
```

#### GitHub Sponsors

Create `.github/FUNDING.yml`:

```yaml
ko_fi: ninyawee
github: ninyawee
```

### Package Metadata

Add docs/repo URLs to package manifests:

#### Cargo.toml (Rust)

```toml
[package]
name = "package-name"
version = "0.1.0"
edition = "2021"
license = "MIT"
description = "Short description"
repository = "https://github.com/ninyawee/REPO"
homepage = "https://ninyawee.github.io/REPO"
documentation = "https://ninyawee.github.io/REPO"
keywords = ["keyword1", "keyword2"]
categories = ["category"]
```

#### pyproject.toml (Python)

```toml
[project]
name = "package-name"
version = "0.1.0"
description = "Short description"
license = "MIT"
readme = "README.md"
requires-python = ">=3.9"
keywords = ["keyword1", "keyword2"]
authors = [{ name = "Nutchanon Ninyawee", email = "me@nutchanon.org" }]

[project.urls]
Homepage = "https://github.com/ninyawee/REPO"
Documentation = "https://ninyawee.github.io/REPO"
Repository = "https://github.com/ninyawee/REPO"
```

#### package.json (Node.js)

```json
{
  "name": "package-name",
  "version": "0.1.0",
  "description": "Short description",
  "license": "MIT",
  "author": "Nutchanon Ninyawee <me@nutchanon.org>",
  "repository": {
    "type": "git",
    "url": "https://github.com/ninyawee/REPO"
  },
  "homepage": "https://ninyawee.github.io/REPO",
  "bugs": "https://github.com/ninyawee/REPO/issues",
  "keywords": ["keyword1", "keyword2"]
}
```

## Checklist

When bootstrapping a project:

- [ ] Create `mkdocs.yml` with Material theme
- [ ] Create `docs/` structure (index.md, getting-started.md, api/)
- [ ] Create `docs/overrides/main.html` for Giscus
- [ ] Create `.github/workflows/docs.yml`
- [ ] Add `docs:serve` and `docs:build` tasks to mise.toml
- [ ] Add docs link to README (`📖 **[Documentation](https://ninyawee.github.io/REPO/)**`)
- [ ] Add badges to README
- [ ] Polish README structure
- [ ] Add `.github/FUNDING.yml`
- [ ] Enable GitHub Discussions for Giscus
- [ ] Update package metadata (Cargo.toml/pyproject.toml/package.json) with docs URLs
