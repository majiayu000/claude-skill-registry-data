---
name: debt-radar
description: >
  Scans a given scope (functional domain or explicit path) for known tech debt violations and
  produces a structured, read-only report. Never modifies files — output only.
  Trigger on: "analyse la dette de", "état des lieux de", "debt-radar sur", "montre la dette de",
  "scan la dette", "combien de violations dans", or any request to audit a domain or directory
  for technical debt without immediately fixing it.
---

## Purpose

Produce a **read-only audit report** of known tech debt violations within a given scope.
This skill never writes or modifies any file. If the user wants to fix what is found, they must
use the `fix-debt` skill.

---

## Step 1 — Resolve the scope

Identify what to scan from the user's input:

| Input type             | Example                          | Resolution                                             |
| ---------------------- | -------------------------------- | ------------------------------------------------------ |
| Functional domain name | "grants", "offers", "young"      | Scan `libs/{domain}/` recursively                      |
| Explicit path          | "libs/grants/grants-domain/src/" | Scan that path and its subdirectories                  |
| App                    | "api", "runner"                  | Scan `apps/idf-young-{app}/src/`                       |
| Ambiguous              | "le domaine des jeunes"          | Ask one targeted clarifying question before continuing |

---

## Step 2 — Identify which debt categories to analyse

By default, analyse **all known debt categories** unless the user restricts the scope explicitly
(e.g. "seulement l'architecture", "juste les transactions").

The category → documentation file mapping is in the **Known Tech Debt** table in `AGENTS.md`.
**Always read the relevant doc(s) before scanning.** The docs define exactly what constitutes a
violation and what the expected direction is.

---

## Step 3 — Scan for violations

Search the resolved scope for the following signals. Collect every match with its file path,
the nature of the violation, and an estimated impact level (HIGH / MEDIUM / LOW).

### Architecture layering

| Signal                         | Where to look                                | Violation                                                          |
| ------------------------------ | -------------------------------------------- | ------------------------------------------------------------------ |
| `import.*class-validator`      | `*-domain/**/*.ts`                           | Framework dep in domain layer                                      |
| `import.*class-transformer`    | `*-domain/**/*.ts`                           | Framework dep in domain layer                                      |
| `import.*@nestjs/swagger`      | `*-domain/**/*.ts`                           | Framework dep in domain layer                                      |
| `import.*@nestjs/common`       | `*-domain/**/*.ts`                           | Framework dep in domain layer                                      |
| Files named `*.view.ts`        | `*-domain/src/`                              | View class in domain layer — should be in `*-api/src/views/`       |
| Files named `*.query.ts`       | `*-domain/src/`                              | Query class in domain layer — should be in `*-api/src/queries/`    |
| Files named `*.command.ts`     | `*-domain/src/`                              | Command class in domain layer — should be in `*-api/src/commands/` |
| `@ApiProperty` in `*.error.ts` | `*-domain/src/`                              | Swagger decorator on a domain error                                |
| Import of `*-api` package      | `*-ui/**/*.ts`, `apps/idf-young-app/**/*.ts` | Frontend importing backend class (not an interface)                |

### TypeORM transactions

| Signal                  | Where to look                                          | Violation                                                    |
| ----------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| `transaction.read(`     | `*-api/src/controllers/**`                             | Legacy read wrapper invoked directly in controller           |
| `transaction.write(`    | `*-api/src/controllers/**`                             | Legacy write wrapper invoked directly in controller          |
| `QueryRunner` parameter | `*-api/src/services/**`, `*-api/src/infrastructure/**` | QueryRunner propagated through service/repository signatures |

### Naming conventions

| Signal                                      | Where to look                                                         | Violation                                                    |
| ------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------ |
| File name not in kebab-case                 | `**/*.ts`                                                             | File naming must be kebab-case                               |
| Artefact file missing mandatory suffix      | `**/*.ts`                                                             | e.g. a service file not ending in `.service.ts`              |
| Interface class without `Interface` suffix  | `*-domain/**/*.ts`                                                    | Interfaces must be named `FooInterface`, not `Foo`           |
| API class not implementing domain interface | `*-api/src/views/**`, `*-api/src/queries/**`, `*-api/src/commands/**` | View/Query/Command class must `implements FooInterface`      |
| Class name not matching file name           | `**/*.ts`                                                             | e.g. file `foo-bar.service.ts` should export `FooBarService` |

---

## Step 4 — Produce the report

Output the report using the exact format below. **Do not suggest fixes inline** — the report is
descriptive only. Always end with the `→ fix-debt` call to action.

```
## Debt Radar — {scope} ({date})

### Health overview

| Layer / Area            | Score  | Violations |
| ----------------------- | ------ | ---------- |
| {layer-or-area}         | {n}/10 | {count}    |
| ...                     | ...    | ...        |

> Score = 10 − min(violations × 1.5, 10), rounded. A file outside its correct layer counts as 2.

### Violations

#### Architecture layering ({n} violations)

| Priority | File | Violation |
| -------- | ---- | --------- |
| HIGH     | path/to/file.ts | Framework import `@nestjs/swagger` in domain layer |
| ...      | ...  | ...       |

#### TypeORM transactions ({n} violations)
...

#### Monitoring & logging ({n} violations)
...

### Recommended fix order

1. {file} — {reason why it is highest priority}
2. ...

---
→ To address these violations, use the **fix-debt** skill.
```

**Priority rules:**

- HIGH: any framework import (`@nestjs/swagger`, `class-validator`, `class-transformer`, `@nestjs/common`) anywhere in the domain layer — regardless of whether the file is consumed by the frontend (includes `@ApiProperty` on error classes, decorated views/commands/queries); any controller using `transaction.read` or `transaction.write`
- MEDIUM: `QueryRunner` propagated through service or repository method signatures
- LOW: naming convention violations — file not in kebab-case, wrong or missing artefact suffix (`.service.ts`, `.repository.ts`, etc.), interface missing the `Interface` suffix, class name not matching file name, API class not implementing its corresponding domain interface, constant not in `UPPER_SNAKE_CASE`

---

## Output constraints

- **Never** suggest code changes or fixes in this report.
- **Never** modify any file.
- If no violations are found in a category, omit that section entirely.
- If the scope is very large (> 50 files with violations), cap the violations table at the 20 highest-priority items and add a note: `(showing top 20 — run debt-radar on a sub-scope for full details)`.
