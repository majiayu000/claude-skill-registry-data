---
name: code-documentation
description: "Generate docs: README, API reference, architecture, guides."
allowed-tools:
  - bash
  - read_file
  - write_file
  - list_dir
enabled: true
related-skills: [codebase-inspection]
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# Code Documentation

## Overview

Generate professional, comprehensive documentation for software projects,
codebases, libraries, and APIs. Follows best practices from React, Django,
Stripe, Kubernetes to produce accurate, well-structured docs.

## When to Use

- User asks to "document", "create docs", or "write documentation" for code
- User requests a README, API reference, or developer guide
- User shares a codebase and wants documentation generated
- User asks to improve or update existing documentation
- User needs architecture documentation with diagrams
- User requests a changelog or migration guide

## Workflow

### Phase 1: Codebase Analysis

#### Step 1.1: Project Discovery

| Field | How to Determine |
|-------|-----------------|
| **Language(s)** | File extensions, `package.json`, `pyproject.toml`, `go.mod` |
| **Framework** | Dependencies (React, Django, Express, Spring) |
| **Build System** | `Makefile`, `CMakeLists.txt`, `webpack.config.js` |
| **Package Manager** | npm/yarn/pnpm, pip/uv/poetry, cargo |
| **Project Structure** | Map directory tree |
| **Entry Points** | main files, CLI entry points, exported modules |
| **Existing Docs** | README, docs/, wiki, inline docs |

```bash
# Discover project structure
list_dir(".")
# Read key files
read_file("package.json")  # or pyproject.toml, go.mod, etc.
# Find all source files
bash("find . -name '*.py' -not -path '*/venv/*' -not -path '*/.venv/*' | head -30")
```

#### Step 1.2: Code Structure Analysis

```bash
# Find entry points
bash("grep -rl 'if __name__' --include='*.py' . | head -10")

# Find API routes/endpoints
bash("grep -rn '@app.route\|@router\.\|def get\|def post' --include='*.py' . | head -20")

# Find exported modules
bash("grep -rn 'export\|module.exports' --include='*.js' --include='*.ts' . | head -20")

# Find classes (for API reference)
bash("grep -rn '^class ' --include='*.py' . | head -20")
```

### Phase 2: Documentation Generation

#### README.md

```markdown
# Project Name

> One-line description

## Features
- Feature 1
- Feature 2

## Installation
\`\`\`bash
pip install project-name
\`\`\`

## Quick Start
\`\`\`python
from project import Client
client = Client()
result = client.do_thing()
\`\`\`

## API Reference
### `Client.do_thing(param: str) -> Result`
Description of what this does.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param | str | Yes | The input |

## Configuration
| Key | Default | Description |
|-----|---------|-------------|

## Contributing
See CONTRIBUTING.md

## License
MIT
```

#### API Reference

For each public function/class:
- Signature (parameters, return type)
- Description
- Parameters table
- Return value
- Example usage
- Exceptions raised

#### Architecture Documentation

- System overview diagram (use `architecture-diagram` skill)
- Component descriptions
- Data flow
- Key design decisions (ADR format)

### Phase 3: Review

- [ ] All public APIs documented
- [ ] Examples are runnable
- [ ] Installation instructions tested
- [ ] No broken links
- [ ] Language-appropriate conventions (docstrings, JSDoc, GoDoc)
- [ ] Architecture diagram included for complex projects

## Documentation Conventions by Language

| Language | Inline Format | Reference Format |
|----------|--------------|-----------------|
| Python | docstrings (Google/NumPy style) | Sphinx, MkDocs |
| JavaScript/TypeScript | JSDoc/TSDoc | JSDoc, TypeDoc |
| Go | GoDoc comments | godoc |
| Java | Javadoc | javadoc |
| Rust | rustdoc (`///`) | rustdoc |

## Changelog Generation

```bash
# From git log
bash("git log --oneline --no-decorate v1.0.0..HEAD | head -50")

# Generate changelog from commits
bash("git log v1.0.0..HEAD --pretty=format:'- %s (%h)' --no-merges")
```

## Pitfalls

- **Stale docs**: documentation must match code. If code changed, docs must
  update. Note the commit/version the docs were generated from.
- **No examples**: documentation without runnable examples is useless. Always
  include copy-pasteable examples.
- **Over-documenting internals**: document public API, not implementation
  details. Internal code should have inline comments, not API docs.
- **No table of contents**: for long docs, include a TOC with anchor links.
- **Missing prerequisites**: list all dependencies, environment requirements,
  and minimum versions.
