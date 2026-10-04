---
name: fix-debt
description: >
  Applies targeted, incremental tech debt fixes across one or more files within a given scope.
  Can consume a debt-radar report or run a scan internally. Always presents a grouped plan
  before writing any code.
  Trigger on: "corrige la dette de", "migre ce fichier", "fix debt sur", "applique le radar",
  "nettoie la couche domain de", "résous la dette de", or any request to actually fix
  known tech debt in a domain, directory, or specific file.
---

## Purpose

Apply known tech debt fixes incrementally, in a controlled way, across a scope chosen by the user.
This skill **always presents a plan first** and waits for explicit validation before writing code.
Multiple files can be fixed in a single session; the user chooses which debt category to tackle.

---

## Step 0 — Verify characterization tests exist

Before touching any code, check whether the target domain already has characterization tests:

```bash
find libs/<domain>/<domain>-api/src -name '*.characterization.spec.ts'
```

| Result                                  | Action                                                                                                                      |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| File exists and snapshots are committed | Proceed to Step 1                                                                                                           |
| File missing or snapshots not committed | **Stop.** Trigger the `write-char-tests` skill on the same scope, run the tests, commit the `.snap` files, then return here |

> These tests are the safety net for the refactoring. Without them, there is no objective exit
> criterion. Do not skip this step, even if the domain seems simple.

---

## Step 1 — Acquire the violation list

Determine the source of violations to fix:

| Source                                      | Action                                                                                                    |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| User provides a `debt-radar` report output  | Parse it directly — extract the violations list and recommended fix order                                 |
| User provides a scope (domain name or path) | Run debt-radar internally (following the `debt-radar` skill steps 1–3), display the report, then continue |
| User provides a specific file path          | Treat that single file as the entire scope                                                                |

After this step you have: a list of violations with file paths, types, and priorities.

---

## Step 2 — Choose the debt category to address

If the violation list contains **multiple debt categories** (e.g. architecture layering + transactions),
ask the user which one to focus on in this session. Do not mix categories in a single session.

If only one category is present, proceed directly.

---

## Step 3 — Read the relevant debt documentation

Before writing any code, read the documentation file for the chosen category.
The category → documentation file mapping is in the **Known Tech Debt** table in `AGENTS.md`.

---

## Step 4 — Present the grouped fix plan

**Never write code before this step is validated by the user.**

Group files by logical unit (e.g. all views of a domain together, all commands together).
Present the plan in this format:

```
## Fix plan — Architecture layering — libs/grants/ (March 5, 2026)

### Group 1 — Views (3 files)
| Action   | File                                                              | Details                                              |
| -------- | ----------------------------------------------------------------- | ---------------------------------------------------- |
| CREATE   | libs/grants/grants-domain/src/interfaces/views/grant-view.interface.ts | Extract interface from existing class          |
| MOVE     | libs/grants/grants-domain/src/views/grant.view.ts → libs/grants/grants-api/src/views/grant.view.ts | Move + add `implements GrantViewInterface` |
| UPDATE   | All importers of the old domain path                              | Repoint to new api path (back) or interface (front)  |

### Group 2 — Commands (2 files)
...

### Group 3 — Queries (1 file)
...

### Summary
- {n} interfaces to create in domain
- {n} files to move to api layer
- {n} import sites to update

Proceed with Group 1?
```

Wait for the user to confirm ("go", "ok", "oui", or equivalent) before implementing.

---

## Step 5 — Implement group by group

Implement each group in full before moving to the next. After each group:

1. Briefly confirm what was done (files created, moved, imports updated)
2. Ask: "Continuer avec le groupe suivant ?" before proceeding

### Architecture layering — fix order within each group

For each `.view.ts` / `.query.ts` / `.command.ts` being migrated, apply in this order:

1. **Read the existing class** in `*-domain/src/` to extract properties and types
2. **Create the interface** in `*-domain/src/interfaces/{views|queries|commands}/` :
   - Filename: `{name}-view.interface.ts` / `{name}-query.interface.ts` / `{name}-command.interface.ts`
   - Interface name: `{Name}ViewInterface` / `{Name}QueryInterface` / `{Name}CommandInterface`
   - Content: plain TypeScript interface, zero decorators, zero framework imports
   - Export from the domain `index.ts`
3. **Move the decorated class** to `*-api/src/{views|queries|commands}/` :
   - Keep all existing decorators (`@Expose`, `@ApiProperty`, `@IsString`, etc.)
   - Add `implements {Name}ViewInterface` (or Query/Command)
   - Update the import of the interface to reference the domain package
4. **Update imports across the codebase** :
   - Backend files (`*-api`, `*-runner`, `apps/idf-young-api`) that imported the class from domain → repoint to `*-api`
   - Frontend files (`*-ui`, `apps/idf-young-app`) that imported the class → repoint to the interface from `*-domain`
5. **Remove the old file** from `*-domain/src/` and clean up the domain `index.ts`

### Architecture layering — `.error.ts` with `@ApiProperty`

Do not move the file. Only:

1. Remove the `@ApiProperty` decorators and the `@nestjs/swagger` import
2. Verify the error still extends `DomainBaseError` correctly
3. Confirm the Swagger documentation is handled at the controller level via `@ApiResponse`

### TypeORM transactions — fix pattern

Per the transaction-wrapper documentation:

- Replace `transaction.read(this.datasource)(runner => ...)` in controllers with `DataSource.transaction(...)` scoped to the service
- Remove `QueryRunner` parameters from service method signatures where possible
- Use the hybrid `QueryRunner | undefined` pattern only as a transitional step

---

## Step 6 — Final summary

After all groups are done:

```
## Fix complete — {scope}

### What was done
- {n} interfaces created in domain layer
- {n} classes moved to api layer
- {n} import sites updated (backend: {n}, frontend: {n})
- {n} @ApiProperty decorators removed from error classes

### Remaining violations (not addressed in this session)
- {file} — {reason skipped or out of scope}

→ Run **debt-radar** again on this scope to verify the health score improved.
```

---

## Constraints

- Never mix debt categories in a single session — one category at a time.
- Never skip the plan validation step (Step 4).
- Never leave an import broken — always update all consumers before finishing a group.
- If moving a class would require changes in more than 20 import sites, flag it in the plan
  and suggest splitting it into a dedicated session.
- If a file's content is ambiguous (e.g. unclear whether a class is used by the frontend),
  check `tsconfig.base.json` path aliases and `libs/*-ui` imports before deciding.
