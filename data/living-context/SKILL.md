---
name: living-context
description: This skill should be used when the user asks about "snapshot.md", "constraints.md", "decisions.md", "debt.md", ".ctx/", "living context", "documentation freshness", "stale docs", "ADR", "architecture decision", "technical debt", "system context", "co-located documentation", "context health", "validation", or needs help managing co-located documentation that stays synchronized with code.
---

# Living Context System

Co-located documentation that stays synchronized with code. No more archaeological digs through outdated wikis. Context lives where the code lives.

## Overview

Living Context provides a structured approach to keeping documentation synchronized with code through:

1. **System-level context** - Each system has its own `.ctx/` directory with standardized files
2. **Global context** - Project-wide knowledge database and dependency graph
3. **Validation engine** - Automated freshness checking and health validation
4. **ADR tracking** - Architecture Decision Records with full lifecycle management

## Commands Reference

All commands use the `uv run cctx` prefix.

### Initialize Project Context

```bash
uv run cctx init [PATH]
```

Create `.ctx/` directory structure including knowledge.db, graph.json, templates/, and README.md. Defaults to current directory if no path specified.

**Options:**
- `--ctx-dir, -c` - Override context directory name (default: .ctx)
- `--json` - Output as JSON
- `--quiet, -q` - Minimal output for CI

### Check Context Health

```bash
uv run cctx health [--deep]
```

Run health checks on Living Context documentation. Validates file presence, formatting, and synchronization.

**Validators run:**
- Snapshot validator - Checks file existence and dependencies
- ADR validator - Validates ADR consistency and indexing
- Debt auditor - Audits technical debt tracking
- Freshness checker - Detects stale documentation

**Options:**
- `--deep, -d` - Include constraint checking in health validation
- `--json` - Output as JSON
- `--quiet, -q` - Minimal output for CI

### Show Status Summary

```bash
uv run cctx status
```

Display overview of documented systems, ADR count and status breakdown, technical debt items, and last sync timestamp.

### Sync Documentation

```bash
uv run cctx sync [--dry-run]
```

Analyze codebase for changes requiring documentation updates. Uses freshness checker to identify stale documentation.

**Options:**
- `--dry-run, -n` - Preview changes without applying them

### Pre-commit Validation

```bash
uv run cctx validate
```

Run validation suitable for pre-commit hooks. Checks context file integrity, ADR format, required fields, and system registrations. Exits with code 2 if validation fails.

### Add System Context

```bash
uv run cctx add-system <PATH> [--name NAME]
```

Create `.ctx/` directory structure for a system/module with:
- snapshot.md - System overview and public API
- constraints.md - System invariants and boundaries
- decisions.md - Index of ADRs for this system
- debt.md - Technical debt tracking
- adr/ - Directory for Architecture Decision Records

**Options:**
- `--name, -n` - Human-readable system name (defaults to directory name)

### Create ADR

```bash
uv run cctx adr <TITLE> [--system PATH]
```

Create a new Architecture Decision Record from template with next available number. Creates in system's `.ctx/adr/` if system specified, otherwise in global `.ctx/adr/`.

**Options:**
- `--system, -s` - System path to create ADR in

### List Entities

```bash
uv run cctx list [systems|adrs|debt]
```

List registered entities. Defaults to systems if no entity type specified.

## Context File Structure

### Global Context (project-wide)

```
.ctx/
├── knowledge.db    # SQLite - ADRs, systems, dependencies
├── graph.json      # Generated dependency graph
├── schema.sql      # Database schema
├── templates/      # Documentation templates
└── README.md       # System documentation
```

### System-level Context (per system)

```
src/systems/<name>/.ctx/
├── snapshot.md     # Purpose, public API, dependencies
├── constraints.md  # Invariants and boundaries
├── decisions.md    # Index of ADRs for this system
├── debt.md         # Known technical debt
└── adr/            # Architecture Decision Records
    └── ADR-NNN.md
```

## Workflow Guidance

### When to Use Each Command

| Task | Command |
|------|---------|
| Start a new project with Living Context | `uv run cctx init` |
| Add context tracking to existing system | `uv run cctx add-system src/systems/auth` |
| Check if documentation is current | `uv run cctx health` |
| Deep validation including constraints | `uv run cctx health --deep` |
| Quick status overview | `uv run cctx status` |
| Find stale documentation | `uv run cctx sync --dry-run` |
| Pre-commit validation | `uv run cctx validate` |
| Record architectural decision | `uv run cctx adr "Use PostgreSQL"` |
| List all documented systems | `uv run cctx list systems` |
| Review all ADRs | `uv run cctx list adrs` |
| Audit technical debt | `uv run cctx list debt` |

### File Update Guidelines

| File | Update When |
|------|-------------|
| `snapshot.md` | Public API changes (exports, function signatures) |
| `constraints.md` | Adding/removing invariants, changing boundaries |
| `decisions.md` | New ADR added or status changed |
| `debt.md` | New debt incurred, debt resolved, or status changed |
| `adr/*.md` | New architectural decision made |

## Agent Behavior Rules

These rules define how AI agents should interact with Living Context.

### Before Modifying a System

1. Read `src/systems/<name>/.ctx/snapshot.md` to understand purpose, API, and constraints
2. Check `constraints.md` for invariants that must not be violated
3. Review `debt.md` for known issues that might affect the work

### After Modifying a System's Public API

1. Update `snapshot.md` with new/changed/removed exports
2. If a dependency was added, update the Dependencies section

### When Making Architectural Decisions

1. Create an ADR in `.ctx/adr/` explaining context, options, and rationale
2. Update `decisions.md` to index the new ADR
3. Register in `knowledge.db`

### When Introducing Technical Debt

1. Document it in `debt.md` with description and rationale
2. Never leave undocumented shortcuts

### Before Completing Work on a System

1. Run `uv run cctx health` to verify documentation is current
2. Fix any issues before considering work complete

## Common Workflows

### Creating a New System with Context

```bash
# Create system directory
mkdir -p src/systems/auth

# Add context structure
uv run cctx add-system src/systems/auth --name "Authentication System"

# Fill in snapshot.md with purpose, API, dependencies
# Add constraints to constraints.md
# Document any initial debt in debt.md
```

### Adding an Architecture Decision Record

```bash
# Create ADR for a system
uv run cctx adr "Use JWT for session tokens" --system src/systems/auth

# Or create global ADR
uv run cctx adr "Adopt monorepo structure"

# Update decisions.md to index the new ADR
# Register in knowledge.db
```

### Pre-commit Workflow

```bash
# Quick validation
uv run cctx validate

# If issues found, check health for details
uv run cctx health

# Find what needs updating
uv run cctx sync --dry-run
```
