---
name: kanban-plan
description: 'Plan and obtain human approval for a kanban feature contract or lightweight bug triage contract, then ask whether to start or defer to backlog. Use when a work item is in planning.'
---

# Kanban Phase 2 — Planning → Execution Contract (Human + Agent)

Argument: `<feature_name>`.

Phase 2 turns the confirmed requirement into a **binding execution contract** that the human approves. Everything written here is law for the rest of the pipeline — no silent scope creep afterwards.

---

## 1. Verify stage

```bash
kf status --change {feature_name}   # must show stage = planning
```

If approval is already valid, keep the contract unchanged and go to the start/backlog decision in section 4. If the approval is changed or pending, finish the applicable contract and obtain fresh human approval.

Read work item kind from `kf status --change {feature_name} --json`. For `kind: bug`, use the confirmed bug report as the contract: reproduction, expected fix, scope, regression strategy and docs impact. Skip section 2; present this concise contract, run approval in section 3 and ask start/backlog in section 4. Do not create feature planning artifacts for a bug. If the request introduces behavior beyond correcting the defect, explain the scope change and follow the user's decision before creating a related feature.

## 2. Write the four plan artifacts (in order)

Read the confirmed Test Strategy from `phase-1-spec-requirement.md` (`Level` in a feature spec, `Test Level` in a bug report, plus `UI Tests`, `Tools`, `Coverage Target`) — it was agreed with the human in Phase 1. Everything below must honour it.

### Who writes what

The four artifacts depend on each other: the UC list drives the diagram and the test cases, and every `TC-###` must cite a real `FR-###` and `UC-###`. So the skeleton stays with you, and subagents only take the work that is independent once the skeleton is fixed:

| Step | Who | Output |
| --- | --- | --- |
| a. Impact survey | 1-3 subagents in parallel, one per area (backend, frontend, DB/API/infra, existing tests) | Findings returned to you, never written to artifacts |
| b. Skeleton | You | `implementation-plan`, the `use-case-specification` index with the final UC IDs, slugs and one-line goals |
| c. UC files | One subagent per `UC-###`, in parallel | `use-cases/UC-###-<slug>.md` |
| d. Diagram + test cases | You | `use-case-diagram`, `test-cases` |
| e. Contract review | 1 subagent with a fresh context | Findings returned to you before section 3 |

Skip the subagents and do every step yourself when the change is small (two UCs or fewer, or a survey that fits in a few files): each handover re-reads the spec and the code, which costs more than it saves at that size. If your runtime has no subagent tool, do the same steps yourself in the same order.

**Subagent prompt contract** — every subagent prompt must state:

- Task: its step (a, c or e), and for step c the exact `UC-###`, slug and goal from the index
- Files to read: `phase-1-spec-requirement.md`, the skeleton artifacts, the relevant source paths
- Files it may write: step c only, exactly its one `use-cases/UC-###-<slug>.md`; steps a and e write nothing
- Constraints: never rename or renumber a `UC-###`/`FR-###`, never add scope beyond the confirmed requirement, never edit another artifact, never run `kf approve`, `kf stage`, `kf archive` or `kf run`
- Context: `.works/planning/{feature_name}/` (from `kf status --change {feature_name}`)

**Subagent status protocol** — require every subagent to end with:

```text
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Summary: one or two sentences
Concerns/Blockers: (optional)
```

Treat `DONE_WITH_CONCERNS`, `BLOCKED` and `NEEDS_CONTEXT` as not-done: resolve it before moving on. A missing `Status:` line is not done either.

### a. Impact survey

`kf stage <feature> planning` already fetched and fast-forwarded the base checkout to its upstream — survey the files as they are; if the transition output carried a `⚠ base is N commit(s) behind` warning, surface it to the user before writing the contract instead of pulling yourself.

Before writing the plan, dispatch the survey subagents in one batch. Each answers for its area: which modules, endpoints, tables and components the change touches, who depends on them, which existing tests cover them, and any risk to regression, security or performance. Ask for `file:line` references and conclusions, not file dumps. Feed the findings into the impact analysis of the implementation plan; do not paste them as-is.

### b-d. Skeleton, UC files, diagram and test cases

Write the implementation plan and the use-case index first (step b). Once the UC IDs are fixed, dispatch one subagent per UC file (step c), all in one batch. When they return, read each UC file and check that its ID, goal and acceptance criteria match the index, then write the diagram and the test cases yourself (step d).

Print each template and fill the file at its path:

```bash
kf instruct implementation-plan --change {feature_name}
kf instruct use-case-specification --change {feature_name}
kf instruct use-case-diagram --change {feature_name}
kf instruct test-cases --change {feature_name}
kf instruct use-case --change {feature_name} --id UC-001-create-task
```

### implementation-plan
- Scope: now / supporting / future / not-in-scope
- `TASK-###` breakdown, complexity, impact analysis (backend / frontend / DB / API / infra / security / performance / regression / deps)
- Read the spec's `## Affected surfaces` first: every declared surface gets a task row or a `## Documentation Impact` entry — `kf validate` warns on any surface the plan never mentions. `N/A` means none owed.
- Testing strategy incl. **coverage target from the spec's Test Strategy (default >= 80%)** and Definition of Done
- When Test Level is `full`: name the UI/E2E framework you will use (Playwright, Cypress and so on) and say which suite covers the critical flows and which covers everything.

### use-case-specification
- Use `phase-2-use-case-specification.md` only as an index and coverage summary.
- Write **one file per use case** under `use-cases/`, named `UC-###-<slug>.md` (e.g. `UC-001-create-task.md`), using `kf instruct use-case --id UC-###-<slug>`. The slug makes a file listing readable; plain `UC-###.md` stays valid.
- Each file contains one `UC-###`: goal, actors, preconditions, trigger, main / alternative / exception flows, postconditions, business rules, data and acceptance criteria.
- The `UC-###` prefix of the file name and the declared ID must match exactly. Do not put multiple UC narratives in one file.

### use-case-diagram
- Mermaid `graph TD` / `flowchart`: actors → use cases (one box per UC-###)

### test-cases
- **Generate test cases from the spec's Test Level (unit | unit+integration | full):**
  - `unit` → `Unit` cases only, one per acceptance criterion and per edge case, each tied to an FR and a UC.
  - `unit+integration` → add `Integration` cases wherever the change meets another system, the database or an API.
  - `full` → add **`UI / E2E`** cases for the user-facing flows: what is clicked, what is typed, what appears on screen, following the `UI Tests` scope (critical or all). Add the matching `## TC-###` sections from the detailed template, with references that match that scope.
- Keep the plan table-driven: fill overall totals, per-type counts, use-case coverage matrix and requirement coverage matrix before the detailed `## TC-###` tables.
- Define each test in a `## TC-###` section referencing `FR-###` (spec) and `UC-###` (the matching individual use-case file). `kf validate` blocks missing or unknown references before approval.
- If the user wants to change the test level during Phase 2, which is rare: update the Test Strategy in `phase-1-spec-requirement.md` before generating the cases, and say so when you present the contract for approval.

### e. Contract review

Before section 3, dispatch one review subagent with a fresh context. It reads the requirement and every planning artifact and reports: an `FR-###` with no test case, an acceptance criterion that cannot be tested, a UC or task outside the confirmed scope, an ID that differs between files, and an impact the plan misses. It edits nothing. Fix what it finds yourself, or record why a finding does not apply.

## 3. Human approval gate

```bash
kf validate --change {feature_name}
```

Before approval, `approval_required` is expected; `approval_changed` is expected when revising an old contract. Fix all other errors and assess warnings before presenting the contract. `kf approve` validates the artifacts without requiring an existing approval. Present a tight summary to the user:

- what the feature does (2-3 lines)
- implementation plan headlines (tasks, approach, risks)
- test strategy + coverage target *(as agreed in the spec's Test Strategy: unit / unit+integration / full + UI scope)*
- Definition of Done

Ask once: **"approve?"** On approval:

```bash
kf approve {feature_name}
```

`kf approve` fingerprints the requirement, four planning artifacts and all individual UC files for a feature; for a bug it fingerprints only the bug report. `kf stage` requires the approved contents to remain unchanged. Progress and test outcomes belong in tasks.md and the testing report; do not rewrite the approved contract during execution.

## 4. Start/backlog decision gate

Approval means the contract is valid; it does not mean implementation must start immediately. Ask the user once:

**"The plan is ready. Start implementation now, or put it in the backlog?"**

- Start now → `kf stage {feature_name} implementation`
- Defer → `kf stage {feature_name} backlog`

Do not choose on the user's behalf. A deferred item keeps its approved contract in `backlog` and can resume to implementation later after the user chooses to start.

---

## Done

Approval and the start/defer decision are recorded. Hand off:

```text
If the user chose start, load kanban-implement and move the feature to implementation. If the user chose defer, leave it in backlog and resume only after an explicit start decision.
```
