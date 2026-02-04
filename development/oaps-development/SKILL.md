---
name: oaps-development
description: >-
  This skill should be used when the user asks to "modify OAPS internals",
  "add a new subsystem", "understand OAPS architecture", "add a CLI command",
  "write OAPS tests", "create builtin hooks", "add a hook rule", "debug OAPS",
  "fix OAPS bug", "extend OAPS", "navigate the OAPS codebase", "understand
  the spec system", "understand hooks", "OAPS CI failing", or when working on
  src/oaps/ code, oaps.cli._commands, oaps.hooks, oaps.spec, oaps.config,
  oaps.repository, or oaps.artifacts packages.
version: 0.1.0
---

# OAPS development

This skill provides guidance for developing, maintaining, and extending the OAPS (Overengineered Agentic Project System) codebase. It covers architecture, subsystem design, code conventions, testing patterns, and the distinction between plugin-distributed and project-specific artifacts.

## About OAPS

OAPS is a maximalist project system for Claude Code that provides a comprehensive framework for building, managing, and automating software projects using agentic principles. The system includes:

- **Specification system** for managing requirements, tests, and artifacts
- **Idea system** for lightweight idea capture and development
- **Hooks system** for rule-based automation responding to Claude Code events
- **Artifacts system** for generic artifact management
- **Repository system** for managing the `.oaps/` git repository
- **Configuration system** for layered configuration with validation

The codebase follows strict conventions around module organization, public API exports, typing, and testing.

## Source organization

The `src/oaps/` package contains the core implementation:

| Directory     | Purpose                                                          |
| ------------- | ---------------------------------------------------------------- |
| `artifacts/`  | Generic artifact management (registry, store, validation)        |
| `commands/`   | CLI subcommands (`oaps config`, `oaps spec`, `oaps idea`, etc.)  |
| `config/`     | Layered configuration system with TOML loading and validation    |
| `hooks/`      | Claude Code hook system (inputs, outputs, actions, expressions)  |
| `project/`    | Project-level state and context                                  |
| `repository/` | OAPS repository management (`.oaps/` directory, git operations)  |
| `session/`    | Session-level state management                                   |
| `spec/`       | Specification system (requirements, tests, artifacts, queries)   |
| `state/`      | Scoped state entity framework for persistent state               |
| `utils/`      | Shared utilities (git, logging, paths, etc.)                     |

## Key patterns

OAPS follows several consistent patterns across the codebase.

### Manager pattern

Complex subsystems use manager classes that encapsulate CRUD operations and business logic. Examples include `SpecManager`, `RequirementManager`, `TestManager`, and `ArtifactManager` in the spec system. Managers typically:

- Accept configuration and paths in their constructor
- Provide methods for create, read, update, delete operations
- Maintain indexes for fast lookups
- Handle validation and error reporting

### Public API exports

Each package defines its public API through `__init__.py` with explicit `__all__` lists. Private implementation modules use a leading underscore (e.g., `_spec_manager.py`). Import public symbols from the package, not from private modules.

### Private modules

Implementation details live in underscore-prefixed modules. The public `__init__.py` re-exports only the symbols that constitute the package's API. This pattern enables refactoring internal structure without breaking external consumers.

### Frozen dataclasses with slots

Data models use frozen dataclasses with slots for immutability and memory efficiency:

```python
@dataclass(frozen=True, slots=True)
class SpecValidationIssue:
    spec_id: str
    field: str
    message: str
    severity: Literal["error", "warning"]
```

## Quick start

To begin OAPS development:

1. **Understand the architecture** - Load the `architecture` reference to understand source organization and directory layout
2. **Study the target subsystem** - Load `subsystems` to understand how the subsystem you are modifying works
3. **Follow conventions** - Load `conventions` for OAPS-specific patterns (manager pattern, public API exports, type annotations)
4. **Write tests** - Load `testing-patterns` for guidance on unit tests, integration tests, and property-based tests

## Reference guide

The skill includes reference documents for detailed information:

| Reference          | When to load                                                     |
| ------------------ | ---------------------------------------------------------------- |
| `architecture`     | Understanding source organization, directory structure           |
| `subsystems`       | Deep dives into hooks, spec, config, artifacts, repository       |
| `conventions`      | OAPS code conventions, manager pattern, public API exports       |
| `builtin-hooks`    | Understanding or modifying builtin hook rules                    |
| `testing-patterns` | Writing tests for OAPS components                                |
| `cli-structure`    | CLI command organization, adding new commands                    |
| `plugin-vs-project`| Distinguishing plugin-distributed vs project-specific artifacts  |

To load references, run:

```bash
oaps skill context oaps-development --references <names...> --workflow default --project
```

## Common tasks

Several development tasks recur frequently.

### Adding a new CLI command

1. Create a new package under `src/oaps/commands/_<name>/`
2. Define `_app.py` with a cyclopts App
3. Export the app through `__init__.py`
4. Register in the root CLI app
5. Add unit tests under `tests/unit/commands/<name>/`
6. Add integration tests under `tests/integration/commands/`

### Adding a new subsystem

1. Create a new package under `src/oaps/<name>/`
2. Define models in `_models.py` using frozen dataclasses
3. Create manager class(es) for business logic
4. Export public API through `__init__.py`
5. Add comprehensive tests following the testing patterns

### Modifying hook rules

1. Review existing rules in `src/oaps/hooks/builtin/`
2. Understand the event type and context variables
3. Write conditions using rule-engine expressions
4. Configure appropriate actions (deny, warn, inject, etc.)
5. Test rules with `oaps hooks test`

### Writing tests

OAPS requires >95% test coverage. Tests are organized by type:

- `tests/unit/` - Isolated unit tests
- `tests/integration/` - Integration tests with real filesystem
- `tests/properties/` - Hypothesis property-based tests
- `tests/benchmarks/` - Performance benchmarks

## Design principles

OAPS follows these principles:

- **SOLID, DRY, YAGNI, KISS** - Apply rigorously; KISS takes precedence
- **Secure by Default** - Require explicit opt-in for less secure behavior
- **Defense in Depth** - Multiple validation layers
- **Measure, Don't Guess** - Profile before optimizing
- **Pay for What You Use** - No runtime overhead for unused features

## Gotchas and pitfalls

Several patterns require attention to avoid common mistakes.

### Never use future annotations

OAPS uses runtime type inspection for hook rule evaluation and configuration validation. Using `from __future__ import annotations` breaks this functionality because it converts all annotations to strings. Always use string literals for forward references instead:

```python
# Correct - string literal for forward reference
def get_manager(self) -> "SpecManager":
    ...

# Wrong - breaks runtime inspection
from __future__ import annotations
def get_manager(self) -> SpecManager:
    ...
```

### Circular imports

The codebase uses TYPE_CHECKING imports extensively to avoid circular dependencies. When adding new imports between subsystems, always check if the import should be guarded:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from oaps.spec import SpecManager  # Only for type hints

def process(manager: "SpecManager") -> None:
    ...
```

### Always use uv run

All Python execution must use `uv run`. Never use bare `python` or `python3` commands:

```bash
# Correct
uv run pytest tests/
uv run python script.py

# Wrong
pytest tests/
python script.py
```

### Private modules are private

Never import from underscore-prefixed modules directly. Use the public API from `__init__.py`:

```python
# Correct
from oaps.spec import SpecManager

# Wrong - bypasses public API
from oaps.spec._spec_manager import SpecManager
```

## Steps

1. **Gather context** - Run `oaps skill orient oaps-development --project` to see available references and workflows

2. **Identify relevant references** - Review the references table and select those matching your task

3. **Load dynamic context** - Run `oaps skill context oaps-development --references <names...> --workflow default --project`

4. **Review loaded references** - Read through the guidance. The **Allowed commands** table at the end of the output is authoritative for what commands can be run.

5. **Follow the workflow** - Adhere to the selected workflow's steps for developing OAPS components
