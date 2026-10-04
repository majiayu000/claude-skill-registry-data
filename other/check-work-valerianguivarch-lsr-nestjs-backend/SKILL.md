---
name: check-work
description: >
  Verifies the quality and completeness of a local implementation — no PR, no GitHub required.
  Can be triggered manually after any code change, or automatically at the end of implement-ticket.
  Trigger on: "check mon travail", "vérifie l'implémentation", "est-ce que c'est correct ?",
  "valide mon code", "fais un check", "regarde si c'est bon", "vérifie avant la PR".
  Optional: Jira MCP for AC coverage. Always requires workspace file access.
---

## Purpose

Produce a structured, MoSCoW-classified report on the correctness and quality of recently
created or modified files. This skill is **read-only** — it never modifies files on its own.
When triggered automatically from `implement-ticket`, the owning skill drives any corrections.

---

## Step 0 — Identify the scope

Determine which files to check:

1. **Automatic trigger (from `implement-ticket`)** — the scope is the exact list of files created
   or modified during that implementation session.
2. **Manual trigger** — infer scope from:
   - Git: run `git diff --name-only HEAD` to list changed files. If the working tree has unstaged
     changes, also include `git diff --name-only` (unstaged).
   - If neither yields results, ask the user to specify the scope explicitly.

Also collect context:

- **Jira ticket key** — look in the current branch name (`IDF-\d+`). If found and Jira MCP is
  available, fetch the ticket via `fields=summary,description,customfield_12948,customfield_12947,customfield_12946`
  to retrieve the acceptance criteria and DoD.
- If no key is found and the user hasn't provided one, proceed without ticket context — skip the
  AC coverage section of the report.

---

## Step 1 — Read the authoritative sources

Before evaluating any finding, read these files. **This skill does not duplicate their rules — it
delegates to them.** The rules live exactly once, in these docs:

- `apps/idf-young-documentation/docs/coding-standards/architecture.md`
- `apps/idf-young-documentation/docs/coding-standards/result-pattern.md`
- `apps/idf-young-documentation/docs/coding-standards/naming-conventions.md`
- `apps/idf-young-documentation/docs/coding-standards/testing-strategy.md`

---

## Step 2 — Architecture check

Apply the **"Architecture layering"** signal table from **Step 3 of
`.claude/skills/debt-radar/SKILL.md`**, scoped to the files in scope only — not the entire domain.

Any violation **introduced by the current change** → **Must**. A violation already present before
the change (pre-existing debt) → **Could** at most, flagged as pre-existing.

---

## Step 3 — Result-pattern check

Apply the rules from `apps/idf-young-documentation/docs/coding-standards/result-pattern.md`
(read in Step 1) to every `*.service.ts` and `*.repository.ts` in scope.

Key signals: unexpected `throw`, missing `isErr()` guard, `DatabaseUnknownError` in `Result` →
**Must**. Missing `Result<E, A>` return type where a failure path exists → **Should**.

---

## Step 4 — Tests check

Apply the rules from `apps/idf-young-documentation/docs/coding-standards/testing-strategy.md`
(read in Step 1) to all service methods added or modified in scope.

Key signals: no `.spec.ts` for a new public method → **Should**. Spec missing a happy path or an
error path → **Should**.

For each distinct project found, run:

```bash
pnpm exec nx test <project-name>
```

---

## Step 5 — Lint check

Identify the Nx projects impacted by the files in scope: map each file path to its project by
looking up the nearest `project.json` (e.g. `libs/grants/grants-api/src/...` → project
`grants-api`).

For each distinct project found, run:

```bash
pnpm exec nx lint <project-name>
```

Parse the output:

- **ESLint errors** (exit code non-zero, lines prefixed with `error`) → **Must**
- **ESLint warnings** (lines prefixed with `warning`) → **Should**

Include each finding with: rule name, file, line number.

> Do **not** run `format:check` or `check-format` here — those are Prettier checks captured
> by the pre-commit hook and are not relevant at this stage.

---

## Step 6 — Migration check

If any `*.entity.ts` file was created or modified in scope:

- Is a new migration file present in `libs/databases/young-db/src/migrations/`? If not → **Must**
- Does the migration name match what the entity change does (e.g. `AddGrantsTable`)? If not → **Could**

---

## Step 7 — Acceptance criteria coverage (only when a Jira ticket is available)

For each acceptance criterion extracted from the Jira ticket:

- Read the relevant changed files and reason about whether the criterion is implemented
- Verdict: ✅ Implemented / ⚠️ Partially implemented or unclear / ❌ Not implemented

Any criterion marked ❌ is a **Must** finding.
Any criterion marked ⚠️ is a **Should** finding.

---

## Step 8 — Produce the report

Output the findings in this exact format:

```
## Check-work report — [scope summary] ([date])

### Summary
| Level  | Count |
|--------|-------|
| Must   | N     |
| Should | N     |
| Could  | N     |

### Findings

#### [Must] Architecture — <file>
<description of the violation>
Fix: <what to do>

#### [Should] Tests — <file>
<description>

#### [Could] ...

### Acceptance criteria coverage
| Criterion | Status | Notes |
|-----------|--------|-------|
| [AC1]     | ✅     | ...   |
| [AC2]     | ⚠️     | ...   |
| [AC3]     | ❌     | ...   |

### Verdict
✅ No Must findings — ready to proceed.
or
❌ N Must finding(s) — must be resolved before proceeding.
```

If there is no Jira context, omit the "Acceptance criteria coverage" section.

---

## Rules

- **Never modify files** — this skill is read-only; corrections are driven by the caller (e.g. `implement-ticket` Step 5) or by the user.
- Only surface findings that are genuinely present in the diff — do not invent defects.
- Write the report in the same language as the user's request (French or English).
- If a finding is already present in the codebase but was not introduced by the current change, raise it as **Could** at most, and note it as pre-existing debt.
- When triggered automatically from `implement-ticket`, return the report as a structured object so the caller can act on Must findings directly.
