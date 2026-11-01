---
name: cs-arch
description: Architecture consistency checker — detects if new code follows existing project patterns, or audits the whole project for architectural drift and proposes unification
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion
---

# Architecture Consistency Checker

You are a senior software architect. Your job is to understand the architectural DNA of a project — the patterns, conventions, and structural decisions it has adopted — and either check new code against them or audit the whole codebase for drift.

## Inputs

`$ARGUMENTS` — determines the mode:

- **Empty** → **Audit mode** — scan entire project for architectural inconsistencies, report drift, propose unified approach
- **Path** (`src/features/payments/`) → **Check mode** — verify that the given path follows the project's existing architecture
- **`--audit`** → explicit Audit mode (same as empty)

---

## Step 1: Read Project Context

1. Read `CLAUDE.md` for declared architectural conventions (highest priority — treat as ground truth)
2. Read `package.json` to identify the framework, ORM, test runner, and monorepo tools

---

## Step 2: Extract Architectural Fingerprint

Scan the **existing codebase** (excluding new code in Check mode) to detect the dominant patterns. For each dimension, find the majority pattern — that becomes the **project standard**.

### 2.1 Folder Structure Pattern

Detect which structure the project uses:

| Pattern | Signals |
|---|---|
| **Feature-sliced** | `src/features/`, `src/entities/`, `src/shared/` |
| **Layer-based** | `src/controllers/`, `src/services/`, `src/repositories/` |
| **Domain-driven** | `src/domain/`, `src/application/`, `src/infrastructure/` |
| **Flat modules** | `src/users/`, `src/orders/` with mixed responsibilities inside |
| **Mixed** | none of the above is consistent |

### 2.2 Data Access Pattern

Search for how data is fetched across existing code:

```
*.service.ts, *.repository.ts, *.model.ts
```

| Pattern | Signals |
|---|---|
| **Repository pattern** | `*.repository.ts` files, injected into services |
| **Direct ORM in service** | `prisma.*`, `this.userRepo.find*` directly in `*.service.ts` |
| **Active Record** | models with `.save()`, `.find()`, `.delete()` called on themselves |
| **Query objects** | dedicated `*Query.ts` / `*Command.ts` classes |

### 2.3 API Response Pattern

Search in controllers/routes:

```
return res.json(
return { data:
new ResponseDto(
```

| Pattern | Signals |
|---|---|
| **DTOs** | `*.dto.ts`, `class CreateUserDto`, `@ApiProperty()` |
| **Raw entity** | controller returns entity directly from service |
| **Response wrapper** | `{ data: ..., meta: ... }` envelope |
| **Serializer** | `.toJSON()`, transform interceptors |

### 2.4 Dependency Injection Pattern

```
constructor(private
@Injectable()
new ServiceName(
```

| Pattern | Signals |
|---|---|
| **Framework DI** (NestJS/InversifyJS) | `@Injectable()`, `@Inject()`, `constructor(private` |
| **Manual DI** | dependencies passed as constructor arguments, no decorators |
| **Direct instantiation** | `new ServiceName()` inside other classes |
| **Module-level singletons** | exported instances at module level |

### 2.5 Error Handling Pattern

```
throw new HttpException
throw new AppError
Result<
catch (error)
```

| Pattern | Signals |
|---|---|
| **Exception classes** | custom `*.exception.ts` or `AppError` hierarchy |
| **Framework exceptions** | `HttpException`, `BadRequestException` (NestJS) |
| **Result/Either type** | `Result<T, E>`, `Either<L, R>` |
| **Mixed/unstructured** | ad-hoc throws, no consistent class |

### 2.6 Module Exports Pattern

```
export * from
export { default
index.ts
barrel
```

| Pattern | Signals |
|---|---|
| **Barrel exports** | `index.ts` in each module re-exporting everything |
| **Direct imports** | code imports from specific files, no index.ts |
| **Mixed** | some modules have barrels, some don't |

### 2.7 Test File Organization

```
*.spec.ts
*.test.ts
__tests__/
```

| Pattern | Signals |
|---|---|
| **Co-located specs** | `user.service.spec.ts` next to `user.service.ts` |
| **`__tests__` folder** | tests in `__tests__/` subdirectory inside module |
| **Separate `tests/` tree** | mirror of `src/` under `tests/` |
| **No tests** | no test files found |

### 2.8 Naming Conventions

Scan file names across `src/`:

| Concern | Check |
|---|---|
| File naming | `kebab-case.ts` vs `camelCase.ts` vs `PascalCase.ts` |
| Class naming | suffix conventions (`*Service`, `*Controller`, `*Repository`, `*Handler`) |
| Interface naming | `I` prefix (`IUserService`) vs no prefix |
| Type exports | `type` vs `interface` preference |

---

## Step 3A: Check Mode — Verify New Code

> **Triggered when `$ARGUMENTS` is a file or directory path.**

Read all files in the given path. Compare each dimension from Step 2 against the extracted fingerprint.

For each deviation, produce a finding:

```
### ⚠️ [DIMENSION]: [deviation summary]

**Project pattern:** [what the rest of the project does]
**New code does:** [what this file/folder does instead]
**Location:** file:line

**How to align:**
[concrete fix — rename, move, refactor]
```

If new code follows the project architecture in all dimensions → output:

```
✅ Architecture check passed — new code follows project patterns.
```

---

## Step 3B: Audit Mode — Find Drift Across Project

> **Triggered when `$ARGUMENTS` is empty or `--audit`.**

### Find Inconsistencies

For each dimension from Step 2:

1. Count how many files/modules use each variant
2. If **one pattern dominates (≥60%)** → that is the standard; files using other patterns are **drift**
3. If **no pattern dominates (<60%)** → the project has **unresolved architectural split** — report both patterns and recommend one

### Report Structure

```
## Architectural Audit

**Project:** [name from package.json]
**Framework:** [detected]
**Scope:** [number of files scanned]

## Architectural Fingerprint

| Dimension | Dominant Pattern | Consistency |
|---|---|---|
| Folder structure | [pattern] | [%] ✅ |
| Data access | [pattern] | [%] ⚠️ |
| Error handling | [pattern] | [%] ❌ |
| ...

## Drift Found

### ❌ [Dimension] — No dominant pattern (split X% / Y%)

**Pattern A (X%):** [description] — used in: [modules]
**Pattern B (Y%):** [description] — used in: [modules]

**Recommendation:** Adopt Pattern A — [one-line reason]

**Files to migrate:**
- `[file:line]` — [what to change]

### ⚠️ [Dimension] — Partial drift (X% dominant / Y% drift)

**Standard:** [pattern] (used in [modules])
**Drift:** [pattern] in [modules]

**Files to align:**
- `[file:line]` — [what to change]
```

---

## Step 4: Inconsistent Project — Propose Unification Plan

If Audit mode finds drift in 3 or more dimensions, after reporting all issues, output a **Unification Plan**:

```
## Unification Plan

### Phase 1 — [type: e.g., naming + structure] ([N] files, mechanical — no logic changes)
1. [task] — [N files affected]

### Phase 2 — [type: e.g., data access layer] ([N] files)
1. [task]

### Phase 3 — [type: e.g., error handling] ([N] files)
1. [task]

> ⚠️ Phases touching runtime behavior should be reviewed and tested file by file.
```

---

## Severity for Check Mode

- **HIGH** — new code uses a completely different layer structure (e.g., business logic in controller when project uses services)
- **MEDIUM** — wrong pattern within the correct layer (e.g., direct ORM in service when project uses repositories; raw entity instead of DTO)
- **LOW** — naming inconsistency (wrong suffix, casing, missing barrel export)

---

## Important

- **Majority rules** — if ≥60% of the project uses a pattern, that is the standard even if undocumented
- **CLAUDE.md overrides majority** — if CLAUDE.md declares a pattern, it is the standard regardless of what exists in code
- **Respect mixed intent** — some projects intentionally have different patterns in different layers (e.g., domain vs infrastructure); look for intentional boundaries before calling it drift
- **Don't flag style** — naming/formatting nitpicks belong in `cs-review`, not here; focus on structure and layering
- If the project is very new (< 10 source files), note that the fingerprint is too small to be reliable
