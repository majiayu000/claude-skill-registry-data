---
name: task-decomposition
description: Task decomposition patterns for planner. Todo anatomy, specificity rules, sizing guidelines, dependency graphs, and coder task package structure.
user-invocable: false
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


# Task Decomposition

## Coder Task Package

Planner includes the following in each todo's `content` field (free-text markdown).
These are CONCEPTUAL sections, not separate DB columns — coder receives them as a single prompt via Agent SDK `query()`:

- **content** — specific instruction (prompt, not documentation)
- **code_context** — snippets of CURRENT code (what to change)
- **imports_needed** — which imports to add
- **anti_patterns** — what NOT to do
- **conventions** — rules for this file type
- **reference_file** — analog in project (do by example)
- **lessons** — known gotchas (PipelineMemory auto-recalls relevant lessons)
- **technologies** — external libs/APIs needed (e.g. ["vast-ai", "redis-streams"]). Only non-standard tech.
- **test_cases** — input/output pairs
- **verify_steps** — how to verify result (list of assertions)

**Coder does NOT read PROJECT.md, does NOT explore codebase, does NOT make architectural decisions.**
Everything needed — planner puts in todo. Project-specific skills (architecture, conventions) are auto-injected by pipeline.

## Todo Anatomy

**content:** Specific instruction (prompt for coder).
- Good: "In load_data() after `rows = await db.fetch(sql)` (~line 65), if rows empty AND freq_filter != 'all': log warning, retry query without filter, return result"
- Bad: "Add fallback logic"

**code_context:** Snippets of CURRENT code (via Grep/Read).
- Coder sees what exists now → knows what to change
- Doesn't guess, doesn't search, doesn't spend context on exploration

**imports_needed:** Full import lines.
- Good: `from src.core.config import settings`
- Bad: "need config module"

**test_cases:** Input/output pairs.
- Good: input="freq_filter='exact', rows=[]", expected="fallback to all, returns data"
- Bad: "should work with empty data"

**verify:** Functional assertion, NOT lint/format commands.
- Good: "Function _format_transactions() exists and limits output to 5 items"
- Good: "Build command passes without errors"
- Bad: `ruff check src/file.py` (lint is not verification)
- Bad: "works"

**done:** Measurable state.
- Good: "Valid credentials → 200 + JWT cookie, invalid → 401"
- Bad: "Auth is ready"

## Specificity Examples

| VAGUE | SPECIFIC |
|-------|----------|
| "Add auth" | "JWT via jose, httpOnly cookie, 15 min access / 7 days refresh" |
| "Create API" | "POST /api/projects: {name, description}, validation 3-50, response 201" |
| "Error handling" | "try/catch on API, {error: string} on 4xx/5xx, toast via sonner" |

## Sizing

Each step: **15-60 minutes** of coder work.
- < 15 min → merge steps
- > 60 min → split
- > 5 files → split

**Plan: maximum 5 steps.** More → task is too large.

## Merging Rules (CRITICAL — saves cost and time)

**Merge into 1 step when:**
- All steps use the SAME agent/stack (e.g. all `coder-fastapi`)
- Steps modify the SAME files or tightly coupled files (imports, module split)
- Steps are strictly sequential with no independent work between them
- Total estimated lines < 250

**Examples of tasks that should be 1 step, NOT multiple:**
- "Split file A into A + B, update imports" — one atomic refactor
- "Add field to model, update API handler, update types" — one vertical slice
- "Create endpoint + add route + add validation" — one feature unit

**Verification/lint is NOT a separate step** — it's part of the coder's job.
The orchestrator runs `run_typecheck` / `run_build` after coding steps.

**Each new subprocess = cold start (reads files, loads context).** Unnecessary splitting wastes 2-3 minutes per extra step on context loading alone.

## Dependency Graph: Vertical Slices (PREFER)

```
- id: user-feature → blocked_by: []
- id: product-feature → blocked_by: []
```
Steps are independent, can execute in parallel.

**AVOID horizontal layers:**
```
- id: all-models → blocked_by: []
- id: all-api → blocked_by: [all-models]
- id: all-handlers → blocked_by: [all-api]
```
Strictly sequential, slow.
