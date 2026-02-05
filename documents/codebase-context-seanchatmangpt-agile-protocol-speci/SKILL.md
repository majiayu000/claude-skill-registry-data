---
name: codebase-context
description: |
  Generates and maintains codebase context documentation (.context.md files).
  Implements the Codebase Context Specification for AI-friendly project
  documentation. Activates when documenting architecture or onboarding.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Codebase Context Documentation Skill

This skill implements the Codebase Context Specification for creating AI-friendly project documentation.

## When This Skill Activates

- Starting new projects or modules
- Documenting architecture decisions
- Creating developer onboarding guides
- Updating project context files
- Generating .context.md hierarchies

## Context File Formats

### Markdown (.context.md)
Primary format with YAML frontmatter and markdown body.

### YAML (.context.yaml)
Pure YAML for machine parsing.

### JSON (.context.json)
JSON format for programmatic access.

## Context Hierarchy

```
project-root/
├── .context.md           # Project-level context
├── .contextignore        # Patterns to ignore
├── .contextdocs.md       # External doc references
├── src/
│   ├── .context.md       # Source directory context
│   ├── api/
│   │   └── .context.md   # API module context
│   └── components/
│       └── .context.md   # Components context
└── tests/
    └── .context.md       # Testing context
```

## Context File Template

```yaml
---
module-name: [Module Name]
version: [X.Y.Z]
description: |
  [Comprehensive description of the module's
  purpose, functionality, and scope]

related-modules:
  - name: [Related Module]
    path: [./relative/path.md]

technologies:
  - [Technology 1]
  - [Technology 2]

conventions:
  - [Convention 1]
  - [Convention 2]

architecture:
  style: [Architecture pattern]
  components:
    - [Component 1]
    - [Component 2]
  data-flow: |
    [Description of data flow]

development:
  setup-steps:
    - [Step 1]
    - [Step 2]
  build-command: [command]
  test-command: [command]

business-requirements:
  key-features:
    - [Feature 1]
    - [Feature 2]
  target-audience: [Audience description]
  success-metrics:
    - [Metric 1]

quality-assurance:
  testing-frameworks:
    - [Framework 1]
  coverage-threshold: [percentage]
  performance-benchmarks:
    - [Benchmark 1]

deployment:
  platform: [Platform name]
  cicd-pipeline: [Pipeline description]
  staging-environment: [Staging URL/location]
  production-environment: [Prod URL/location]
---

# [Module Name]

[Extended description and documentation in markdown format]

## Architecture Overview

[Detailed architecture explanation]

## Key Components

[Component documentation]

## Usage Examples

[Code examples and usage patterns]
```

## .contextignore Format

```gitignore
# Dependencies
node_modules/
vendor/
.venv/

# Build outputs
dist/
build/
*.pyc

# IDE files
.idea/
.vscode/

# Sensitive files
.env
*.key
secrets/
```

## .contextdocs.md Format

```yaml
---
contextdocs:
  - name: API Documentation
    type: url
    link: https://docs.example.com/api
    relationship: primary
    description: Official API reference

  - name: Design System
    type: local
    path: ./docs/design-system.md
    relationship: supporting

  - name: Architecture Decision Records
    type: directory
    path: ./docs/adr/
    relationship: reference
---
```

## Context Accumulation Rules

1. **Proximity Precedence**: Closer context files override distant ones
2. **Inheritance**: Child contexts inherit from parent contexts
3. **Explicit Override**: Explicit declarations override inherited values
4. **Merge Strategy**: Arrays merge, objects deep-merge

## Generation Guidelines

1. **Start at Root**: Create project-level .context.md first
2. **Descend Hierarchically**: Add module-level contexts as needed
3. **Keep Current**: Update contexts when architecture changes
4. **Link Related**: Cross-reference related modules
5. **Document Decisions**: Include architecture decision rationale

## Best Practices

1. **Completeness**: Fill all relevant sections
2. **Accuracy**: Keep information current
3. **Clarity**: Write for both humans and AI
4. **Hierarchy**: Organize by module structure
5. **Maintenance**: Update with code changes
