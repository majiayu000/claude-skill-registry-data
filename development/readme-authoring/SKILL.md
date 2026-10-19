---
name: readme-authoring
description: >
  Draft, structure, and refine professional repository README.md files that clearly
  communicate project value, quickstart steps, configuration, architecture, and
  contribution guidelines. Use when creating new README files, revamping outdated
  project documentation, adding badges, or structuring developer onboarding guides.
compatibility: >
  Agent Skills-compatible coding agents creating or reviewing repository README files.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "readme, documentation, onboarding, open-source, markdown, badges"
  topics: "documentation, devtools"
---

# Professional README Authoring

A repository's `README.md` is the primary entry point for developers, users, and evaluators. A professional README immediately answers: **What problem does this project solve? How do I install and run it in under 60 seconds? How is it configured? How do I contribute?**

## Core Rules

1. **State the purpose in the first sentence**: Never open with vague abstractions or marketing hype. State exactly what the tool does and who it is for.
2. **Include a 60-Second Quickstart**: Provide copy-pasteable terminal commands that take a user from clone to running software immediately.
3. **Keep examples verified and runnable**: Every code sample or CLI command in the README must be tested against current software versions.
4. **Use badges purposefully**: Include badges that communicate real project health (CI build status, package version, license, test coverage). Avoid gratuitous badge clutter.
5. **Document prerequisites explicitly**: List minimum language versions (e.g. Python >= 3.10, Node.js >= 20) and required system libraries upfront.

---

## 1. Canonical README Architecture

```markdown
# Project Name

A concise, high-impact one-sentence description of the project's purpose and core value proposition.

[![CI Status](https://github.com/org/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/org/repo/actions)
[![PyPI Version](https://img.shields.io/pypi/v/my-project)](https://pypi.org/project/my-project/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- **Blazing Fast**: Streams records with zero memory accumulation.
- **Strictly Typed**: Full type annotations and static analysis verified with Mypy.
- **Zero Lock-in**: Exports cleanly to standard JSON, CSV, and Parquet.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 14+ (optional, for persistent storage)

## Quick Start

### Installation

```bash
pip install my-project
```

### Basic Usage

```python
from my_project import DataEngine

engine = DataEngine()
result = engine.process("input.csv")
print(result.summary())
```

## Configuration

Configure behavior via environment variables or a `.env` file:

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | string | *Required* | PostgreSQL connection string |
| `LOG_LEVEL` | string | `INFO` | Logging verbosity (`DEBUG`, `INFO`, `WARN`, `ERROR`) |
| `MAX_WORKERS` | integer | `4` | Number of background worker processes |

## Development and Testing

```bash
# Clone and install dependencies
git clone https://github.com/org/repo.git
cd repo
uv sync --dev

# Run unit and integration tests
uv run pytest

# Check code formatting and types
uv run ruff check .
uv run mypy src/
```

## Contributing

Contributions are welcome! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for details on code style, commit conventions (Conventional Commits), and the pull request process.

## License

This project is licensed under the MIT License - see the [`LICENSE`](LICENSE) file for details.
```

---

## 2. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Broken code snippets in Quick Start | Immediate bounce: users abandon tool on first failure | Test every README snippet in automated CI |
| Wall of text with no visual hierarchy | Readers cannot scan for installation or API reference | Use clear H2/H3 headings, tables, and fenced code blocks |
| Outdated setup instructions | Frustrates new contributors | Keep README updated during release engineering |
| Omitting license information | Enterprise developers cannot legally adopt the tool | State license and link to `LICENSE` file |

---

## 3. Verification Checklist

- [ ] Project purpose stated in opening paragraph.
- [ ] Quick Start commands verified in a clean terminal.
- [ ] Configuration options documented in a structured table.
- [ ] Prerequisites and supported runtimes clearly stated.
- [ ] License and contribution links point to valid repository files.
