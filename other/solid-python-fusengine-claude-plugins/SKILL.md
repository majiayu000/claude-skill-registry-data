---
name: solid-python
description: "Use when writing or refactoring Python code, structuring modules/[feature]/ layers, or defining Protocol-based interfaces (SOLID, files within FUSE_SOLID_MAX_LINES)."
versions:
  python: "3.14"
user-invocable: true
references: references/principles.md, references/patterns.md
related-skills: solid-detection
---

<objective>
SOLID Python enforces a modular architecture for Python 3.14+: every feature lives under `modules/[feature]/` (routes, services, repositories, interfaces, models) with shared code in `core/`, interfaces are defined with `typing.Protocol` and live only in `interfaces/` directories, type hints are mandatory on every signature, and every public function carries a docstring.

Before writing any new code it requires a DRY check against `core/services` and `core/interfaces`. See `principles.md` for the 5 SOLID principles and `patterns.md` for directory layout, testing, and typing conventions.
</objective>

# SOLID Python - Modular Architecture

## Agent Workflow (MANDATORY)

Before ANY implementation, spawn 3 agents in parallel, one `Agent` call each with a `name`:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing architecture
2. **fuse-ai-pilot:research-expert** - Verify Python docs via Context7
3. **fuse-ai-pilot:sniper** - Post-implementation validation

---

## DRY - Reuse Before Creating (MANDATORY)

**Before writing ANY new code:**
1. **Grep the codebase** for similar interfaces, services, or logic
2. Check shared locations: `core/services/`, `core/interfaces/`
3. If similar code exists -> extend/reuse instead of duplicate
4. If code will be used by 2+ features -> create it in `core/`

---

## Architecture (Modules MANDATORY)

| Layer | Location |
|-------|----------|
| Routes | `modules/[feature]/routes/` |
| Services | `modules/[feature]/services/` |
| Repositories | `modules/[feature]/repositories/` |
| Interfaces | `modules/[feature]/interfaces/` |
| Models | `modules/[feature]/models/` |
| Shared | `core/{services,interfaces,models}/` |

**NEVER use flat `src/` structure - always `modules/[feature]/`**

---

## Critical Rules (MANDATORY)

| Rule | Value |
|------|-------|
| File limit | `FUSE_SOLID_MAX_LINES` |
| Routes | Thin, delegate to services |
| Interfaces | `interfaces/` directory ONLY |
| Docstrings | Every public function documented |
| Type hints | MANDATORY on all signatures |
| Protocols | Use `typing.Protocol` for interfaces |
| Small interfaces | 1-3 methods max |

---

## Reference Guide

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **SOLID Principles** | [principles.md](references/principles.md) | Quick reference for all 5 principles |
| **Patterns & Structure** | [patterns.md](references/patterns.md) | Directory layout, testing, typing |

---

## Forbidden

| Anti-Pattern | Fix |
|--------------|-----|
| Files over `FUSE_SOLID_MAX_LINES` | Split by responsibility |
| Interfaces in impl files | Move to `interfaces/` directory |
| Fat interfaces (4+ methods) | Split into small Protocols |
| Flat `src/` structure | Use `modules/[feature]/` |
| Concrete dependencies | Use Protocol + dependency injection |
| Missing type hints | Add type annotations to all signatures |
