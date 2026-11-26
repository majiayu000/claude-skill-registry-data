---
name: prior-work-check
description: Use before approving a spec or starting a multi-file implementation to confirm no existing skill, helper, or handler already covers the proposed work.
type: skill
license: MIT
compatibility:
  - claude-code
  - codex
user-invocable: false
effort: high
---

# Prior Work Check

> **Tool discipline:** read-only — `Read`/`Grep`/`Glob` and read-only `Bash` queries. Never `Edit`/`Write`; report what exists and let the caller decide.

## Overview

Before writing new code, confirm the codebase doesn't already do this — re-implementing a capability that exists under a different name is the most common waste in mature codebases. **Runs once per `implement` run:** spec-driven step 9 for a fresh request, or Phase 0.7's reconciliation mode when the engineer supplied the plan. Lessons and security-impact classification are covered elsewhere (the lessons query in Phase 0, the spec's security-impact step and drift check) and are not repeated here.

## When To Use

- `spec-driven-development` step 9, before the implement Phase 2.5 approval gate
- `implement` Phase 0.7 when a **pre-written plan is supplied as input** — the reconciliation mode below, so already-implemented batches are not re-run
- When the engineer says "let's add an X" and X sounds generic (cache, retry, validator, formatter, normalizer)

### When NOT To Use

- Typo fixes, single-line config tweaks, or bug fixes where the file in scope is already named
- A second time in the same run — planning does not re-run it

## Workflow

### Query — `search_prior_work`

Look for an existing implementation of the capability under any name.

1. Extract 2-4 capability keywords from the spec `summary` and
   `success_criteria`. Verbs + nouns ("issue token", "retry policy",
   "currency formatter").
2. Run, in parallel:
   - `grep -rn -i "<keyword>" --include="*.cs" --include="*.py" --include="*.ts" --include="*.tsx" --include="*.js" src/`
     (or the active stack's source roots — read `.claude/tech-stack`).
   - If `CODE_INDEX.md` exists at the repo root, query it with
     `bash scripts/query-code-index.sh find "<keyword>"` (case-insensitive
     row search that prints each match prefixed with its `## <Domain>`
     section) rather than a raw `grep`. If the script is absent (repo
     bootstrapped before v7.17) or the keyword may live outside table rows
     (domain headings, prose), fall back to `grep -i "<keyword>" CODE_INDEX.md`.
   - If an MCP code-index tool is available (e.g. `mcp__ast-index__*`), prefer
     it over raw grep.
3. For each hit, report:
   - file:line
   - one-line summary of what it does
   - whether it can be reused, extended, or is genuinely different

## Existing-Plan Reconciliation Mode

Invoked by `implement` Phase 0.7 when the input is a **pre-written plan**
(supplied by the engineer) rather than a fresh request. A supplied plan may be
stale — some batches were implemented since it was written. Re-implementing done
work is waste and a drift risk, so reconcile the plan against current code
**before** the Phase 2.5 gate:

1. Run the query above (`search_prior_work`) as usual to catch capability duplication.
2. **Per-batch satisfied-check (read-only).** For each batch in the supplied
   plan, take its `acceptance` / `verification` / linked `success_criteria` and
   probe current code for whether it is *already satisfied*:
   - grep for the batch's target symbols and `change_manifest` paths (and any
     public-contract signatures) and read the relevant lines;
   - where a batch has a runnable, non-mutating `verification`, note whether it
     already passes. Never mutate state to find out.
   - Classify each batch: `already-satisfied` | `partially-done` | `not-started`,
     each with `file:line` evidence.
3. Emit a reconciliation table (batch id → classification → evidence). The
   orchestrator then, before Phase 2.5: marks `already-satisfied` batches
   complete/skipped in the JSON sidecar and ticks them in `tasks/todo.md` with a
   one-line note naming what was pruned; surfaces `partially-done` batches for
   the engineer to re-scope. Never silently re-run a done batch, and never edit
   source here — this mode only classifies and reports.

## Output

```markdown
### Prior Work Check
- match: src/Auth/TokenService.cs:42 — already issues JWTs. **Reuse, do not
  reimplement.** Spec should be revised to extend, not create.
- (no other matches; synonyms tried: "token", "jwt", "bearer")
```

## Verdict

- An existing implementation the spec would duplicate → `BLOCKED`; revise the spec to reuse or extend it before the gate.
- A near match that could be extended → `PROCEED_WITH_CHANGES`; the engineer decides, and a deviation is justified in writing.
- No match after synonyms → `PASS`.

## Rules

- A grep miss is not a confirmed absence. If the capability is generic, widen the search with synonyms before declaring `PASS`.
- Read-only: it reports, the caller decides.

## Verification

- [ ] The query ran with output captured, and at least one synonym was tried
- [ ] In reconciliation mode, every supplied batch is classified with `file:line` evidence
- [ ] Verdict matches the strongest match found
