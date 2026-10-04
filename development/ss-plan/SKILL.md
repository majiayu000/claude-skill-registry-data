---
name: ss-plan
description: Use before writing any code, once you have a requirement, technical proposal, or spec that needs to become an executable, task-level plan. Decomposes the input into self-contained, TDD-ordered tasks with explicit dependencies, exact file paths, and acceptance criteria traced to OpenSpec scenarios; splits multi-subsystem requirements into separate plans and produces a master plan when the split spans multiple repositories.
---

# Build Execution Plan

Decompose a requirement or technical proposal into an executable, task-level implementation plan. Each task must be small enough for a single agent to complete independently, with explicit dependencies, exact file paths, and verification criteria.

**Language of the plan:** write the plan's prose in the same language as the input document (or the project's existing docs, if that's a clearer signal); default to English when neither gives a signal. Code, commands, and file paths always stay in their original form regardless of prose language.

**Zero-context assumption:** write the plan as if the executor has zero knowledge of the codebase and limited design taste. Every task must be fully self-contained — the executor should never need to "figure out" what to do. If a step changes code, show the code. If a step runs a command, show the command and its expected output.

## Inputs

One of:
- A link to a requirement or proposal document that your document-reading tool can fetch.
- A local Markdown file path.
- Plain text describing the requirement directly.

If the input is missing or too thin to extract a goal, scope, and acceptance criteria, ask the user rather than guessing.

## Iron Rules

**Violating any of these means stop and start over:**

1. **Comprehend before planning** — do not start decomposing until the entire input is read and understood. Skipping this voids the plan.
2. **Never guess** — if the input is ambiguous or missing information, ask the user. Do not assume and continue.
3. **No placeholders** — see "No Placeholders" below for the full list of forbidden patterns.
4. **Every task must be independently verifiable, and acceptance traces to the spec** — each task ends with a concrete acceptance command and expected output. When Phase 0 produced delta specs, the acceptance MUST cover a named Scenario from that delta (the Scenario is the single source of truth for expected behavior) — do not author parallel, independent acceptance prose that restates the Scenario.
5. **Exact file paths** — every referenced file is a real path from the project root. No vague descriptions.
6. **TDD-driven** — code tasks have test steps before implementation steps.
7. **DRY / YAGNI** — do not plan features that weren't requested; do not add abstraction layers for hypothetical future needs.
8. **Self-contained tasks** — each task produces a change that makes sense on its own, and the project still compiles/runs after it. Never write "similar to Task N" — repeat the code, since executors may work tasks out of order.
9. **Plan the full scope, no unauthorized reduction** — the plan must cover every requirement point in the input. Never defer work to "phase 2 / a later iteration / future enhancement," plan only an "MVP / P0 / core" subset, or quietly downgrade a requirement. Splitting the plan (see Scope Check) changes delivery packaging, not scope — every sub-plan still gets written. If the full scope can't be planned, stop and ask the user. The only valid reduction is one the user explicitly requested — record it in the plan header's "User-Confirmed Scope Adjustments" section, which downstream review also reads.

## No Placeholders

These are plan failures — never write them:

- "TBD", "TODO", "to be added later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" without actual test code
- "Similar to Task N" — repeat the code, since executors may read tasks out of order
- "Refer to module X" without a concrete code path
- Steps that describe *what* to do without showing *how* (code steps need code blocks)
- References to types, functions, or methods not defined in any task
- "Add necessary imports" instead of listing them explicitly

## Input Handling

| Input type | Detection | Method |
|-----------|-----------|--------|
| Document link | A URL your document-reading tool can fetch | Fetch and read it as Markdown/text |
| Local Markdown | Starts with `/` or `./`, ends in `.md` | Read the file directly |
| Plain text | Neither of the above | Use the input as-is |

## Specs Discovery

Before starting any phase, discover the repository's own specs/conventions:

1. Read `CLAUDE.md` and/or `AGENTS.md` at the project root.
2. Extract any referenced spec files (paths, submodules, or inline rules).
3. Read the relevant spec files identified above (e.g., coding conventions, test conventions, commit-message conventions).

If specs are found, they apply to every subsequent phase:
- Plan structure and naming follow the spec's conventions.
- Task-level code complies with coding conventions (naming, error handling, testing patterns).
- Self-review verifies spec compliance.

**OpenSpec `config.yaml` context injection:** if `openspec/config.yaml` exists, its `context` block is binding project context and MUST be applied to every generated artifact (delta specs and the task plan alike). Specifically:
- Treat `context` as authoritative background for capability-ownership decisions, naming, and scope.
- Treat `rules.delta` and `rules.spec` entries as binding format/quality constraints on the Phase 0 delta; a violation is a plan failure.
- When handing work to a subagent, carry these constraints forward explicitly — they are not optional context.

**If specs exist, note them — they become binding constraints for the plan.**

## OpenSpec Delta Phase

Before Phase 1, run **Phase 0: Generate Delta Spec** unless the request is clearly zero-spec.

### Zero-spec Mode

Skip Phase 0 only when the request cannot affect observable system behavior:

- Documentation-only changes
- Comment-only changes
- Internal refactoring with no public API or behavior change
- Build/CI/dependency configuration updates
- Test-only changes

If uncertain, don't skip — generate a minimal delta instead.

### Phase 0: Generate Delta Spec

This phase internalizes the `ss-write-spec` skill; you normally don't need to invoke that skill directly when running this one.

1. Read OpenSpec context:
   - `openspec/config.yaml` if present — treat `context` as binding project context and `rules.delta`/`rules.spec` as binding format constraints; inject them into every artifact generated below.
   - existing `openspec/specs/*/spec.md`
   - active `openspec/changes/*/specs/*/spec.md`, excluding `archive/`
   - relevant OpenAPI YAML files if the proposal mentions API paths
2. Derive a stable `change-id` in kebab-case from the proposal title, branch name, or requirement text.
3. Decide capability ownership:
   - Prefer existing capability directories.
   - New capability names are kebab-case business noun phrases.
   - If ownership is ambiguous, stop and ask the user to confirm — never guess.
4. Write delta files to `openspec/changes/<change-id>/specs/<capability>/spec.md`.
5. Copy the proposal or input summary to `openspec/changes/<change-id>/proposal.md`.

Delta format is strict:

```markdown
## ADDED Requirements

### Requirement: <name>
The system SHALL ...

#### Scenario: <name>
- **WHEN** ...
- **THEN** ...
- **AND** ...
```

Allowed sections are exactly:

- `## ADDED Requirements`
- `## MODIFIED Requirements`
- `## REMOVED Requirements`
- `## RENAMED Requirements`

Rules:

- Every Requirement MUST have at least one `#### Scenario:`.
- Scenario headings MUST use four `#`.
- `MODIFIED` MUST copy the original Requirement from the source of truth in full, then edit it.
- `REMOVED` MUST include `**Reason:**` and `**Migration:**`.
- `RENAMED` uses `FROM: <old> → TO: <new>`.
- Keep SHALL/MUST/MAY/SHOULD in English regardless of the prose language used elsewhere in the delta.

### Phase 0 Self-Review

Before proceeding:

- [ ] Every functional requirement maps to a Requirement or Scenario.
- [ ] Existing capabilities were reused where appropriate.
- [ ] `MODIFIED` content is complete, not a short diff note.
- [ ] `REMOVED` includes a Migration note.
- [ ] `openspec/config.yaml`'s `context` was applied as binding project context, and every `rules.delta`/`rules.spec` entry is satisfied by the generated delta.
- [ ] Scenario headings use `#### Scenario:`.

## Scope Check

**This check runs before any planning work. If the input covers multiple independent subsystems, split it into separate plans.**

**Split ≠ cut.** Splitting produces multiple plans that are all written and all delivered — it reorganizes the work, never removes or defers any requirement point. Dropping a subsystem from the plan requires an explicit user instruction.

### When to split

Split into multiple plans when any of these hold:

| Signal | Example | Action |
|--------|---------|--------|
| Input spans 2+ services/repos | "Order service + Payment service" | One plan per service |
| Input spans frontend + backend | "React page + Go API + DB migration" | One plan per layer |
| Input has 2+ features with no shared code | "User login + Report export" | One plan per feature |
| Decomposition yields 20+ tasks with heavy cross-dependencies | — | Go back and split |

### When not to split

- Single service, single feature, even if complex (many tasks are fine as long as they form a clean DAG).
- Multiple tasks that share the same data model or interface (splitting would create duplication).

### How to split

1. Identify independent subsystems from the input.
2. For each subsystem, create a separate plan file: `YYYY-MM-DD-<name>-<module>.md`.
3. Each sub-plan must be independently deliverable — after executing one plan, the system is in a valid state.
4. If sub-plans have ordering dependencies (e.g., the backend API must exist before the frontend calls it), state the execution order explicitly:
   ```
   Execution order:
   1. docs/plans/2026-05-10-payment-backend.md (creates APIs)
   2. docs/plans/2026-05-10-payment-frontend.md (consumes APIs)
   ```
5. Confirm the split approach with the user before proceeding to Phase 1.

### Multi-repo split: master plan (required when the split spans 2+ git repositories)

When the sub-plans belong to **different git repositories** (not just different modules of the current repo), the split MUST also produce a **master plan** so the `ss-multi-repo-workflow` skill can execute the set:

1. **Sub-plan header field:** every sub-plan gets a `**Repo:** <repo-name>` line in its header, and its `**Files:**` paths are relative to that repository's root.
2. **Repository path detection:** probe `../<repo-name>` (a sibling directory of the current repo). If it doesn't exist or its git remote doesn't match, ask the user for the correct local path — never guess.
3. **Master plan file:** `docs/plans/YYYY-MM-DD-<slug>-master.md` in the current repo:

```markdown
# <Requirement Name> Multi-Repo Execution Master Plan

> **Agent execution guide:** use the `ss-multi-repo-workflow` skill to execute this master plan.

**Repos:**
| Repo | Local Path | Base SHA | Sub-plan | Batch | Depends On |
|---|---|---|---|---|---|
| payment-service | ../payment-service | `<planning-time HEAD>` | 2026-07-03-refund-payment.md | 1 | — |
| order-service | ../order-service | `<planning-time HEAD>` | 2026-07-03-refund-order.md | 2 | payment-service (consumes its API) |

**Unified branch name:** feat/<slug>
**Problem ID:** <required for troubleshooting input; otherwise omit>
**Investigation Report:** <exact path for troubleshooting input; otherwise omit>
**Violated Invariant:** <required for troubleshooting input; otherwise omit>
**Owning Boundary:** <required for troubleshooting input; otherwise omit>
**Patch-Style Alternative Rejected:** <required for troubleshooting input; otherwise omit>
**Contract changes:** <path to the shared API-contract repo, if the contract change was prepared separately / none>
**User-Confirmed Scope Adjustments:** none
```

4. **Batching rules:** repos with no cross-repo dependency share a batch (parallel); an API consumer is always in a later batch than its provider. The batch/dependency columns are hard constraints for downstream execution.
5. **Splits within a single repository are unaffected** — no master plan, no `**Repo:**` field, behavior unchanged.

### If already split upstream

If the input comes from the `ss-proposal` skill and was already scoped to one subsystem, skip this check and proceed directly to Phase 1.

### Baseline Freshness

Before finalizing any execution plan, record `git rev-parse HEAD` for the repository whose code was
read as canonical `**BASE_SHA:**` metadata. Each multi-repo sub-plan records its own repository's
base; the master plan repeats those refs in its `**Repos:**` table. Validate refs as 7–64 lowercase
hex characters. `BASE_SHA` is a freshness snapshot, not test evidence or the delivered ref.

## Phase 1: Comprehend

**Gate: do not proceed to Phase 2 until every item below is extracted.**

1. Read the entire input document.
2. Read `openspec/changes/<change-id>/specs/` generated by Phase 0, if present, and treat it as binding requirement input.
3. Extract and list:
   - **Goal:** what problem does this solve? (one sentence)
   - **Scope:** which modules/services/layers are involved?
   - **Constraints:** technical, timeline, and dependency constraints.
   - **Acceptance criteria:** how do we know it's done? When Phase 0 produced delta specs, the acceptance criteria ARE the Scenarios in `openspec/changes/<change-id>/specs/<cap>/spec.md` — each Scenario's WHEN/THEN is one criterion; reference them by name instead of re-inventing or rephrasing them. Only in zero-spec mode, extract criteria from the input or confirm with the user.

**If any item above can't be extracted from the input, ask the user — do not assume and proceed.**

When the input is an `ss-inspect` investigation report, also require all of the following before
planning: a stable `**Problem ID:**`; `Confidence: HIGH` with no material evidence gaps; a verified
root cause and evidence chain; complete impact-scoped design/implementation understanding; the
canonical `**Violated Invariant:**`, `**Owning Boundary:**`, and
`**Patch-Style Alternative Rejected:**` fields; canonical one-entry-per-bullet
`**Affected Paths:**` and `**Repositories Requiring Fix:**` lists;
and repair, rollback, observability, compatibility/migration, and regression-verification guidance.
An incomplete report returns to investigation rather than being filled in by the planner. A
confirmed multi-repository list is binding: produce the matching master/sub-plan set and never
silently drop a repository.

## Phase 2: Architect

### Troubleshooting Repair Design

For a plan sourced from an investigation report:

- **Gate before architecture or task writing:** restate and validate the report's relevant component
  responsibilities/ownership, end-to-end flow, dependencies, contracts/invariants, existing
  mechanisms, healthy analogous paths, included/excluded scope, and affected paths. If the planner
  cannot explain how they connect, return to `ss-inspect`; do not invent a local repair.
- Restore the violated invariant at the correct abstraction or ownership boundary; do not turn a
  symptom-only conditional at the failure line into the permanent design unless the evidence proves
  that boundary owns the behavior.
- Reuse an existing mechanism or extension point where the report identifies one.
- Map every `**Affected Paths:**` bullet from the report to at least one implementation task and
  one verification task or acceptance command.
- Include compatibility and downstream effects, migration work, rollback, observability, focused
  regression tests, full-suite verification, and runtime recovery signals in the architecture and
  task graph.
- Link the plan header to the exact Problem ID and investigation report path so downstream resume
  checks cannot confuse it with another incident.

### File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

**Design principles:**
- Each file has one clear responsibility.
- Files that change together live together — split by responsibility, not technical layer.
- Prefer smaller, focused files over large ones that do too much.
- In existing codebases, follow established patterns; don't unilaterally restructure.
- If a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

**Format:**
```
- Create: src/service/payment/handler.go       # payment callback handler
- Modify: src/service/order/service.go:45-80   # add payment status update
- Create: src/service/payment/handler_test.go  # unit tests
```

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

### Dependency Graph

Identify task dependencies:
- Which tasks have no dependencies and can run in parallel?
- Which tasks must be sequential (B depends on A's output)?

### Technical Decisions

If the proposal offers multiple implementation paths, state the chosen one and the reason in one line.

### Diagrams

Use diagrams to clarify architecture and flow where text alone would be ambiguous:
- **Architecture / sequence / activity diagrams:** use PlantUML syntax in fenced ```plantuml code blocks.
- **Simple structural diagrams** (directory trees, data flow, component layout): use ASCII art.
- Prefer diagrams over long text for system interactions, call chains, and state transitions.
- Every diagram needs a title (`title ...` in PlantUML) and must be referenced from a task or the dependency graph.

## Phase 3: Decompose

Break the architecture into appropriately-sized tasks.

**Granularity criteria:**
- One task = one focused concern (one endpoint, one model, one feature point).
- After each task, the project still compiles/runs.
- Each task is self-contained — an executor with zero codebase context can complete it.

### Bite-Sized Step Granularity

**Each step within a task is one action (2–5 minutes):**
- "Write the failing test" — step
- "Run it to confirm it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and confirm they pass" — step
- "Commit" — step

Do not bundle multiple actions into one step.

### Task Template

````markdown
### Task N: [Concrete name, not generic]

**Depends on:** Task X (or "None")
**Parallel group:** A (tasks in the same group can execute concurrently)

**Files:**
- Create: `exact/path/to/file.ext`
- Modify: `exact/path/to/existing.ext:line-range`
- Test: `tests/exact/path/to/test_file.ext`

**Steps:**

- [ ] Step 1: Write the failing test

```language
// Complete test code — not pseudocode, not "add test here"
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] Step 2: Run the test to verify it fails

Run: `exact test command`
Expected: FAIL — "specific error message"

- [ ] Step 3: Write the minimal implementation

```language
// Complete implementation code — every import, every line
def function(input):
    return expected
```

- [ ] Step 4: Run the test to verify it passes

Run: `exact test command`
Expected: PASS

- [ ] Step 5: Commit

```bash
git add exact/path/to/file.ext tests/exact/path/to/test_file.ext
git commit -m "type(scope): description"
```

**Covers Scenario:** `<capability>/<Scenario name>` (from `openspec/changes/<change-id>/specs/`; use "None" only in zero-spec mode)

**Acceptance:** `verification command` → expected output (the assertion MUST verify the WHEN/THEN of the covered Scenario)
````

### Remember

- Exact file paths, always.
- Complete code in every step — if a step changes code, show the code.
- Exact commands with expected output.
- Never "similar to Task N" — repeat the full code.
- DRY, YAGNI, TDD, frequent commits.

## Phase 4: Self-Review

**After completing the plan, review it with fresh eyes. This is not a rubber stamp — actively search for issues.**

### 1. Requirement coverage
Skim each section/requirement in the source. Can you point to a task that implements it? List any gaps and add the missing task.

### 2. Scope reduction scan
Search the plan for phasing/deferral language: MVP, Phase 2, staged rollout, later iteration, simplified version, core-only, P0-only, "out of scope." Every hit must trace to an explicit user instruction recorded in the plan's "User-Confirmed Scope Adjustments" section; otherwise add the missing tasks now.

### 3. Placeholder scan
Search the plan for every pattern in "No Placeholders" above. Fix every occurrence immediately.

### 4. Exact paths
For every file path in the plan, verify it's a real path from the project root (check against the codebase). Vague paths like "in the service directory" get replaced with exact paths.

### 5. Name consistency
Do the types, method signatures, and property names used in later tasks match what earlier tasks defined? A function called `processPayment()` in Task 3 but `handlePayment()` in Task 7 is a bug — fix it.

### 6. No circular dependencies
Trace the dependency graph. If Task A depends on Task B which depends on Task A, restructure.

### 7. Every task has acceptance, traced to a Scenario
Each task ends with a runnable verification command and expected output. When delta specs exist: every task names the Scenario it covers (`**Covers Scenario:**`), and every Scenario in the delta is covered by at least one task. If a Scenario has no task, add it. If a non-zero-spec task lacks a `Covers Scenario` link, fix the linkage rather than inventing parallel acceptance prose.

### 8. Parallel groups annotated
Tasks with no interdependency are marked with a parallel group label.

### 9. Spec compliance
If repo specs were discovered: verify naming conventions, error-handling patterns, test structure, and commit-message format all conform.

For troubleshooting plans, also verify that every `**Affected Paths:**` and
`**Repositories Requiring Fix:**` bullet in the confirmed investigation report remains covered; the
design restores the named invariant at the correct
boundary; and compatibility, migration, rollback, observability, regression, and runtime recovery
work is present. Any omission is a plan defect, not an allowed scope reduction.

### 10. Baseline freshness metadata
Verify every execution plan/sub-plan has a valid canonical `**BASE_SHA:**` equal to the repository
snapshot used for code and interface assumptions; verify each multi-repo master row repeats the
matching sub-plan ref. Refresh stale assumptions before saving.

### 11. PlantUML validation
For each `plantuml` fenced block:
- Render it via a PlantUML server — the public instance at `https://www.plantuml.com/plantuml`, or a local/self-hosted renderer if the project configures one — by encoding the source and requesting `/png/{encoded}` (or `/svg/{encoded}`).
- Verify the returned image contains no "Syntax Error" text.
- If image rendering isn't available in your environment, at minimum validate `@startuml`/`@enduml` presence and correct diagram-type keywords.

**Found issues get fixed inline — no need to re-run the full process.**

## Phase 5: Independent Agent Review

**If your tool supports spawning a subagent with fresh context:**

Spawn an independent review agent that has NOT seen the generation process:

**Review agent prompt:**
```
You are a plan reviewer. Review the execution plan below against:
1. The original requirement/spec (provided)
2. Repository coding specs (if any, provided)

Focus areas:
- Does every requirement point map to a task?
- Any requirement silently deferred ("Phase 2", "MVP scope", "future iteration") or downgraded without a user instruction recorded in the plan's "User-Confirmed Scope Adjustments" section? Flag as MUST-FIX.
- Do code snippets follow the repository's naming/style conventions?
- Are test patterns consistent with the spec's test guidelines?
- Are file paths valid for this project structure?
- Any placeholder violations (TBD/TODO/"refer to"/"similar to")?
- Is the dependency graph a valid DAG?
- Are PlantUML diagrams syntactically correct?
- Can a fresh-context implementer locate the exact task by plan path + heading and execute it using the task-referenced specs, every repository-spec/guardrail path supplied by dispatch, concise dispatch context, and permitted repository exploration?
- Is `**BASE_SHA:**` valid and does the plan still match relevant files/symbols/interfaces at that snapshot? For multi-repo plans, do master rows match sub-plans?
- For troubleshooting input, is `Troubleshooting Repair Basis` complete, are canonical invariant/boundary/patch-rejection fields preserved, and does every affected path map to implementation plus verification?
- When delta specs exist: does every Scenario map to at least one task's `Covers Scenario`, and does each task's acceptance verify that Scenario's WHEN/THEN rather than restating it as separate prose?

Output: a list of issues, each with severity (MUST-FIX / SHOULD-FIX / NIT) and location (Task N, Step M).
If no issues: confirm "LGTM — plan is ready for execution."
```

**Input to the review agent:**
- The generated plan markdown
- The original requirement source (link or text)
- Paths to repository specs, if discovered

**After review:**
- MUST-FIX items get fixed immediately, before saving.
- SHOULD-FIX items get fixed, or the plan documents why they were skipped.
- NIT items get fixed if trivial, otherwise ignored.

**If subagents aren't available:** the Phase 4 self-review is sufficient — skip this phase.

## Output: Plan Document

**Save location:** `docs/plans/`

**Naming convention:** `YYYY-MM-DD-<requirement-name>[-<module-name>].md`
- Date: today's date
- `requirement-name`: an English slug of the requirement/proposal (lowercase, hyphens)
- `module-name`: only when splitting into multiple sub-plans

**Examples:**
- Single plan: `docs/plans/2026-05-10-user-payment.md`
- Multiple plans: `docs/plans/2026-05-10-user-payment-backend.md`, `docs/plans/2026-05-10-user-payment-frontend.md`

**Document header:**

```markdown
# [Requirement Name] Execution Plan

> **Agent execution guide:** use the `ss-coding` skill to execute these tasks in parallel per this plan.

**Goal:** [one-sentence goal]
**Architecture:** [2-3 sentences: pattern used, layering approach, core data flow]
**Tech Stack:** [key technologies/frameworks/middleware involved]
**Scope:** [modules/services touched]
**Repo:** [required for a multi-repo sub-plan; repository name matching the master table; otherwise omit]
**Source:** [link or description of the input document]
**Problem ID:** [required for plans sourced from an investigation report; otherwise omit]
**Investigation Report:** [exact path when applicable; otherwise omit]
**BASE_SHA:** [7–64 lowercase hex planning-time HEAD for this repository]
**Date:** YYYY-MM-DD
**OpenSpec Change:** openspec/changes/<change-id>/ (if applicable)
**User-Confirmed Scope Adjustments:** [record each instruction, verbatim, only when the user explicitly asked to reduce/phase/accept a blocker; otherwise "none"]

---

## Troubleshooting Repair Basis
<!-- Required only for plans sourced from an investigation report; otherwise omit this section. -->

**Relevant design and implementation:** [responsibilities/ownership, end-to-end flow, dependencies, contracts/invariants, existing mechanisms, healthy analogous paths, included/excluded scope]
**Violated Invariant:** [exact invariant and evidence]
**Owning Boundary:** [where the behavior belongs and why]
**Patch-Style Alternative Rejected:** [tempting symptom/local-special-case patch and why it fails to restore the invariant]

| Affected path from report | Implementation task | Verification task/command |
|---|---|---|
| `<repo>:<path>` | Task N | Task M / `<command>` |

## File Map
[Phase 2 file structure map]

## Dependency Graph
[Dependency graph with parallel group annotations]

## Task List
[All tasks from Phase 3]
```

The execution plan lives only in `docs/plans/`. Do not write a separate `openspec/changes/<change-id>/tasks.md` — nothing consumes it, and `docs/plans/` is the single source for tasks. The OpenSpec change directory holds only `proposal.md` and the delta `specs/`.

## Execution Handoff

After saving the plan, present execution options:

```
Plan saved to docs/plans/<filename>.md. Execution options:

1. ss-coding — multi-agent parallel execution (recommended for medium/large plans)
2. Sequential execution — execute tasks one by one in this session (for small plans, ≤5 tasks)
3. Manual review first — have the team review the plan before execution

Which approach?
```

**If a multi-repo master plan was generated** (see Scope Check), recommend the multi-repo path instead:

```
Multi-repo plan set saved:
- Master: docs/plans/<date>-<slug>-master.md
- Sub-plans: <list>

Recommended next step: run the ss-multi-repo-workflow skill on docs/plans/<date>-<slug>-master.md
(one capability-checked repository runner per real repo cwd, batched by dependency order)
```

## Anti-Patterns

| Anti-pattern | Why it's harmful | Correct approach |
|-------------|-----------------|-----------------|
| Single task modifies 5+ files | Too large, hard to verify, hard to roll back | Split by concern into multiple tasks |
| "Implement XXX" with no code | Executor guesses implementation details | Show complete code in every step |
| Implementation without tests | Cannot verify correctness | TDD: test first, implement second |
| Implicit dependencies between tasks | Conflicts during parallel execution | Explicitly annotate dependencies |
| Skipping Phase 1 and jumping to tasks | Incomplete understanding, missed tasks | Extract goal/scope/constraints first |
| Over-engineering (unneeded abstraction) | Adds complexity, deviates from the requirement | YAGNI: only plan what's requested |
| Silently deferring requirements ("MVP first", "Phase 2", "P0 only") | User receives a partial delivery they never agreed to | Plan 100% of the input; phased delivery only on explicit user request, recorded in the plan |
| "Similar to Task N" | Executor may work out of order and can't find Task N | Repeat the full code — always self-contained |
| Bundling multiple actions in one step | Agent skips sub-actions when a step looks "done" | One action per step: write / run / implement / run / commit |

## Red Flags — Stop

If you catch yourself doing any of these, stop and return to the appropriate phase:

- Writing tasks before finishing the input → back to Phase 1
- Writing "TBD" or "to be confirmed" → ask the user instead
- A task description has no file paths → back to Phase 2
- Code steps use pseudocode or "add appropriate handling" → write complete code
- Referencing "similar to Task N" → repeat the code in full
- 20+ tasks with heavy interdependencies → back to Scope Check, split into sub-plans
- A step contains two actions ("write test and run it") → split into two steps

## Examples

Input can be any of:
- A link to an issue or requirement document, e.g., `https://github.com/<owner>/<repo>/issues/123`
- A local proposal file, e.g., `docs/proposals/2026-05-08-payment-refund.md`
- Plain text, e.g., "Implement user login: support phone+SMS-code and WeChat-style QR scan"
