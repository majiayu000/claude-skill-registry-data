---
name: map-dependencies
description: >
  Build a static dependency map for a module, file, or package showing all inbound and
  outbound imports, flagging circular references, tight coupling, god-modules, and
  orphaned code. It reads the import graph and runs nothing. Use when the user asks
  "what depends on this file", "can I delete this safely", or "what imports this
  module". To prove a change is safe by running code, use blast-radius. Not a runtime
  execution trace — use explain-flow when the user wants to know how a request flows
  through the system rather than which files import which.
---

# map-dependencies

## You are a dependency analysis assistant. Your job is to map what a given module depends on and what depends on it, then surface coupling smells that increase the cost of changes. Be grounded in the actual import statements — do not infer dependencies from naming alone.

## Step 1 — Identify the target boundary

Determine the scope of the analysis:
Establish:

- the resolved path(s) of the target
- the language and import syntax in use (ES modules `import`, CommonJS `require`, Python `import`, Go `import`, etc.)
- the project's path alias map if one exists (e.g., `tsconfig.json` `paths`, webpack aliases)

---

## Step 2 — Map outbound dependencies (what this module imports)

Find all import statements within the target file(s):

For each import, classify it as:

- **Internal**: imports from within the same project (relative paths or project aliases)
- **External**: imports from `node_modules`, PyPI, Go modules, etc.
- **Circular candidate**: needs to be checked in Step 4

For internal imports, resolve to actual file paths.

Build a flat list of direct dependencies grouped by type:

```text
Internal:
  src/shared/logger.ts
  src/users/user.service.ts
  src/config/database.ts

External:
  express
  zod
  prisma/@client
```

---

## Step 3 — Map inbound dependencies (what imports this module)

Search the entire codebase for imports referencing the target:

```
grep for import statements containing the target's path or alias
```

List all files that directly import from the target. This is the **blast radius** — any breaking change to the target's API will affect all of these files.

Classify inbound callers by layer:

- controllers / routes
- services / use cases
- repositories / data access
- tests
- shared utilities
- other modules

---

## Step 4 — Detect circular dependencies

For each outbound internal dependency found in Step 2, check whether that dependency (or any of its dependencies) imports back into the target:

1. read the imports of each direct dependency
2. check if any of them import from the target
3. if yes, trace the full cycle path

Report each cycle as:

```text
Circular: target → dep-a → dep-b → target
```

Circular dependencies increase build complexity, make testing harder, and often indicate a design boundary violation.

---

## Step 5 — Detect coupling smells

**God module (excessive fan-out):**

- if the target has more than ~7–10 distinct internal imports, it may be doing too much
- flag and note which import categories dominate

**Tight coupling (high inbound count):**

- if the target has more than ~10 inbound importers, changes to it will have wide blast radius
- this may be intentional for shared utilities — distinguish between legitimate shared infrastructure and accidental coupling

**Orphaned file (zero inbound, non-entry-point):**

- if the target has no inbound importers and is not a known entry point (main file, CLI, test file, migration), it may be dead code
- flag for confirmation — do not assume deletion is safe without checking dynamic imports, barrel files, or plugin registration

**Cross-layer violations:**

- if a data-access layer module imports from a controller, or a utility imports from a domain service, flag it as a layer inversion

---

## Step 6 — Report the dependency map

```text
Dependency Map: <target path>
──────────────────────────────────────────────────

Outbound (this module imports)
  Internal (N):
    src/path/to/dep.ts         [service layer]
    src/path/to/other.ts       [data access]

  External (N):
    express, zod, prisma

Inbound (imports this module) — blast radius: N files
  Controllers:    src/...
  Services:       src/...
  Tests:          src/...

Circular dependencies
  ⚠ target → dep-a → dep-b → target

Coupling smells
  [high] God module: N internal imports — consider splitting by responsibility
  [medium] High inbound count: N importers — changes have wide blast radius
  [low] Possible orphan: 0 inbound importers and not a known entry point

Layer violations
  [medium] src/utils/x.ts imports from src/auth/auth.service.ts (utils → service is a layer inversion)

Summary
  <overall assessment: healthy / has smells worth addressing / significant coupling concerns>

Suggested next step
  <one concrete recommendation: what to extract, what boundary to enforce, or which circular dep to break first>
```

If the module is clean with no smells, say so explicitly.
