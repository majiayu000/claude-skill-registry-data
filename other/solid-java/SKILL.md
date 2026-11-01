---
name: solid-java
description: "Use when writing or refactoring Java code, structuring modules/[feature]/ layers, or defining interfaces/ contracts (SOLID, files within FUSE_SOLID_MAX_LINES)."
versions:
  java: "25"
user-invocable: true
references: references/solid-principles.md, references/single-responsibility.md, references/open-closed.md, references/liskov-substitution.md, references/interface-segregation.md, references/dependency-inversion.md, references/architecture-patterns.md, references/templates/module.md, references/templates/service.md, references/templates/interface.md, references/templates/repository.md, references/templates/error.md, references/templates/test.md
related-skills: solid-detection
---

<objective>
SOLID Java enforces a modular architecture for Java 25+ (current LTS): every feature lives under `modules/[feature]/` (controllers, services, repositories, interfaces, models/DTOs) with shared code in `modules/core/`, interfaces live only in `modules/[feature]/interfaces/`, controllers stay thin and delegate to services, with files within `FUSE_SOLID_MAX_LINES`, records are used for DTOs and sealed types for restricted hierarchies, and every public method carries Javadoc.

Before writing any new code it requires a DRY check against `modules/core/services` and `modules/core/interfaces`. See `solid-principles.md` for the overview, the per-principle references for SRP/OCP/LSP/ISP/DIP detail, and the templates for module/service/interface/repository/error/test scaffolding.
</objective>

# SOLID Java - Modular Architecture

## Agent Workflow (MANDATORY)

Before ANY implementation, spawn 3 agents in parallel, one `Agent` call each with a `name`:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing architecture
2. **fuse-ai-pilot:research-expert** - Verify Java docs via Context7
3. **fuse-ai-pilot:sniper** - Post-implementation validation

---

## DRY - Reuse Before Creating (MANDATORY)

**Before writing ANY new code:**
1. **Grep the codebase** for similar interfaces, services, or logic
2. Check shared locations: `modules/core/services/`, `modules/core/interfaces/`
3. If similar code exists -> extend/reuse instead of duplicate
4. If code will be used by 2+ features -> create it in `modules/core/`

---

## Architecture (Modules MANDATORY)

| Layer | Location |
|-------|----------|
| Controllers | `modules/[feature]/controllers/` |
| Services | `modules/[feature]/services/` |
| Repositories | `modules/[feature]/repositories/` |
| Interfaces | `modules/[feature]/interfaces/` |
| Models/DTOs | `modules/[feature]/models/` |
| Shared | `modules/core/{services,interfaces,models}/` |

**NEVER use flat `src/` structure - always `modules/[feature]/`**

---

## Critical Rules (MANDATORY)

| Rule | Value |
|------|-------|
| File limit | `FUSE_SOLID_MAX_LINES` |
| Controllers | Thin, delegate to services |
| Interfaces | `modules/[feature]/interfaces/` ONLY |
| Javadoc | Every public method documented |
| Records | Use for DTOs (Java 16+) |
| Sealed | Use for restricted hierarchies (Java 17+) |

---

## Reference Guide

### Concepts

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **SOLID Overview** | [solid-principles.md](references/solid-principles.md) | Quick reference |
| **SRP** | [single-responsibility.md](references/single-responsibility.md) | Fat classes |
| **OCP** | [open-closed.md](references/open-closed.md) | Adding providers |
| **LSP** | [liskov-substitution.md](references/liskov-substitution.md) | Contracts |
| **ISP** | [interface-segregation.md](references/interface-segregation.md) | Fat interfaces |
| **DIP** | [dependency-inversion.md](references/dependency-inversion.md) | Injection |
| **Architecture** | [architecture-patterns.md](references/architecture-patterns.md) | Modular patterns |

### Templates

| Template | When to use |
|----------|-------------|
| [module.md](references/templates/module.md) | Feature module structure |
| [service.md](references/templates/service.md) | Business logic service |
| [interface.md](references/templates/interface.md) | Contract definition |
| [repository.md](references/templates/repository.md) | Data access layer |
| [error.md](references/templates/error.md) | Custom exceptions |
| [test.md](references/templates/test.md) | Unit tests with mocks |

---

## Forbidden

| Anti-Pattern | Fix |
|--------------|-----|
| Files over `FUSE_SOLID_MAX_LINES` | Split by responsibility |
| Interfaces in impl files | Move to `interfaces/` directory |
| `new ConcreteClass()` in services | Use dependency injection |
| Flat `src/` structure | Use `modules/[feature]/` |
| God classes | Split by responsibility |
