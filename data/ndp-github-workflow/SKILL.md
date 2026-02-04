---
name: "ndp-github-workflow"
description: "NDP-specific GitHub workflow using Trunk-Based Development (TBD). Commit directly to main with conventional commits. Use this skill for ALL git operations in the Neural Data Platform project."
---

# NDP GitHub Workflow

## What This Skill Does

Defines **Trunk-Based Development (TBD)** conventions for the Neural Data Platform. Everyone commits directly to `main` with small, frequent commits.

**Always use this skill for:**
- Writing commit messages
- Committing to main
- Tagging releases

## Trunk-Based Development

### Core Principles

1. **Commit directly to `main`** - No feature branches
2. **Small, frequent commits** - Multiple times per day
3. **Always deployable** - Every commit should build and pass tests
4. **Feature tracking via commit scope** - Use `{type}(feature-id):` format

### Why TBD for NDP?

| Problem with Feature Branches | TBD Solution |
|------------------------------|--------------|
| Merge conflicts | No branches = no conflicts |
| PR overhead | Direct commits = instant integration |
| Stale branches | Everything on main = always current |
| Integration pain | Continuous integration by default |

---

## Commit Convention

### Format

```
{type}({scope}): {description}

{optional body}

{optional footer}
```

### Types

| Type | Use For |
|------|---------|
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that doesn't fix bug or add feature |
| `test` | Adding or updating tests |
| `chore` | Build, CI, dependencies, tooling |
| `perf` | Performance improvement |
| `wip` | Work in progress (incomplete but buildable) |

### Scope

The scope identifies **what** is affected:

| Scope Type | Examples |
|------------|----------|
| Feature ID | `dp-001`, `fe-001` |
| Component | `storage`, `router`, `config` |
| Layer | `deploy`, `docker`, `ci` |

### Rules

1. **Type and scope are lowercase**
2. **Description is lowercase, no period at end**
3. **Description is imperative mood** ("add" not "added")
4. **Scope matches feature ID when working on a feature**
5. **Max 72 characters for first line**
6. **Every commit must build** - `cargo build` must pass

### Examples

```bash
# Feature work - commit directly to main
feat(dp-001): add duckdb silver layer views
feat(dp-001): implement pivot from long to wide format
fix(dp-001): correct timestamp conversion in bronze data
test(dp-001): add partition key regression tests

# Work in progress (builds but incomplete)
wip(dp-002): start timescaledb integration scaffold

# Component work (not feature-specific)
fix(storage): partition by stream_id instead of location_id
refactor(router): simplify validation logic
perf(parquet): reduce memory allocation in batch writes

# Infrastructure
chore(deploy): update docker-compose resource limits
docs(architecture): add silver layer design doc
```

### Multi-line Commits

For complex changes, add a body:

```bash
git commit -m "feat(dp-001): route mqtt through ingestion router

- MQTT now goes through SourceManager like HTTP
- IngestionRouter adds stream_id tag to points
- ParquetStore uses stream_id for partition path

Fixes indoor air data writing to device MAC instead of stream name"
```

---

## Feature Tracking

Features are tracked via **commit scope** and **product/features/** directories, not branches.

### Feature ID Format

Feature IDs follow `{phase}-{NNN}` pattern:

| Phase | Prefix | Example | Focus |
|-------|--------|---------|-------|
| Air Quality | `air` | `air-005` | Sensors, external data |
| Data Platform | `dp` | `dp-001` | Silver layer, ETL |
| Feature Engineering | `fe` | `fe-001` | ML features |
| Dashboards | `db` | `db-001` | Grafana |
| Predictions | `ml` | `ml-001` | ruv-FANN |
| Alerts | `al` | `al-001` | Triggers |

### Starting a New Feature

```bash
# 1. Create feature directory (for SPARC docs)
mkdir -p product/features/dp-002/{specification,pseudocode,architecture,refinement,completion,bugs,reports}

# 2. Commit directly to main
git add product/features/dp-002/
git commit -m "chore(dp-002): initialize feature directory structure"
git push

# 3. Continue working, committing frequently
git commit -m "feat(dp-002): add timescaledb schema"
git push

git commit -m "feat(dp-002): implement etl from parquet"
git push
```

### Feature Progress

Track progress via:
- **Commit history**: `git log --oneline --grep="dp-001"`
- **STATUS.md**: `product/features/dp-001/STATUS.md`
- **Commit frequency**: Multiple small commits per day

---

## Daily Workflow

### Before Starting Work

```bash
git pull origin main
cargo build
cargo test
```

### During Work

```bash
# Make changes, then commit frequently
git add .
git commit -m "feat(dp-001): add silver layer view for indoor air"
git push

# More changes
git add .
git commit -m "fix(dp-001): correct column names in pivot"
git push
```

### End of Day

```bash
# Ensure everything is pushed
git status
git push

# If work is incomplete but builds
git commit -m "wip(dp-001): partial grafana integration"
git push
```

---

## Release Tagging

### Version Format

```
v{major}.{minor}.{patch}
```

- **Major**: Breaking changes, architectural shifts
- **Minor**: New features, phase completions
- **Patch**: Bug fixes, small improvements

### Tagging Process

```bash
# Ensure on main with latest
git pull origin main

# Verify build
cargo build
cargo test

# Create annotated tag
git tag -a v1.3.0 -m "Release v1.3.0: DP-001 DuckDB Analytics Layer

Features:
- DuckDB Silver layer with PIVOT views
- MQTT routing through IngestionRouter
- Grafana integration with SQLite export

Bug Fixes:
- Indoor air data now writes to air-quality directory"

# Push tag
git push origin v1.3.0
```

---

## When to Use Branches (Exceptions)

PRs are **optional** and only for specific cases:

| Situation | Use Branch? | Why |
|-----------|-------------|-----|
| Normal feature work | No | Commit to main |
| Bug fixes | No | Commit to main |
| Risky refactor | Maybe | If you want a rollback point |
| External contributor | Yes | Review before merge |
| Experimental spike | Maybe | If you might abandon it |

### If You Do Use a Branch

```bash
# Create short-lived branch
git checkout -b experiment/try-new-approach

# Work on it
git commit -m "wip: experimental approach"

# Either merge quickly or abandon
git checkout main
git merge experiment/try-new-approach  # or git branch -D to abandon
git branch -d experiment/try-new-approach
git push
```

---

## Quick Reference Card

### Commit Prefixes
```
feat(scope):     # New feature
fix(scope):      # Bug fix
docs(scope):     # Documentation
test(scope):     # Tests
chore(scope):    # Maintenance
refactor(scope): # Code improvement
perf(scope):     # Performance
wip(scope):      # Work in progress
```

### Daily Commands
```bash
git pull                    # Start of day
git add . && git commit     # After each logical change
git push                    # After each commit
git log --oneline -10       # Check recent history
```

### Feature Commands
```bash
git log --oneline --grep="dp-001"    # See feature commits
git diff HEAD~5                       # Review recent changes
git tag -a v1.x.x -m "..."           # Release
```

### Example Session
```bash
# Morning
git pull origin main
cargo build && cargo test

# Work
git commit -m "feat(dp-002): add timescaledb connection pool"
git push

git commit -m "feat(dp-002): implement hypertable creation"
git push

git commit -m "test(dp-002): add integration tests for etl"
git push

# End of day
git commit -m "wip(dp-002): partial continuous aggregate setup"
git push
```

---

## Enforcement

All NDP agents MUST follow TBD:

1. **Commit directly to main** - No feature branches unless explicitly requested
2. **Use conventional commits** - `{type}({scope}): {description}`
3. **Push frequently** - After each logical change
4. **Ensure builds pass** - `cargo build` before commit
5. **Track features via scope** - Use feature ID in commit scope

If you see branch creation for normal work, suggest committing to main instead.
