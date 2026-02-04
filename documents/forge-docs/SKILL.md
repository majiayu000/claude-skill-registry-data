---
name: forge-docs
description: MkDocs documentation standards with mkdocs-material theme. Use when creating documentation, README files, or project docs structure.
---

# Documentation Standards

## MkDocs Structure

```
docs/
├── index.md                 # Project overview
├── getting-started.md       # Quick start guide
├── architecture/
│   └── decisions/           # ADR files (0001-*.md)
├── guides/
│   ├── installation.md
│   ├── configuration.md
│   └── deployment.md
└── reference/
    ├── api.md
    └── cli.md
```

## mkdocs.yml Template

```yaml
site_name: Project Name
theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
    - content.code.copy

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - admonition
  - pymdownx.details

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Guides:
    - Installation: guides/installation.md
    - Configuration: guides/configuration.md
  - Reference:
    - API: reference/api.md
    - CLI: reference/cli.md
  - Architecture:
    - Decisions: architecture/decisions/
```

## Architecture Decision Records (ADR)

Format: `NNNN-title-with-dashes.md`

```markdown
# NNNN: Title

## Status

Proposed | Accepted | Deprecated | Superseded by [NNNN](NNNN-*.md)

## Context

What is the issue that we're seeing that is motivating this decision?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

### Positive
- Benefit 1
- Benefit 2

### Negative
- Drawback 1
- Drawback 2

## References

- Link to relevant docs
- Link to related ADRs
```

## README.md Template

```markdown
# Project Name

Brief description of the project.

## Installation

\`\`\`bash
pip install project-name
\`\`\`

## Quick Start

\`\`\`python
from project import main
main()
\`\`\`

## Documentation

Full docs at: https://project.readthedocs.io

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

[MIT](LICENSE)
```
