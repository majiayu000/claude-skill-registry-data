---
name: planning-and-task-breakdown
description: Use when .forge/prd.md and .forge/architecture.md exist and the work needs to be decomposed before implementation, when sizing tasks for a sprint, when mapping dependencies between modules, or when a critical path needs to be identified before parallel work begins.
---

# Planning and Task Breakdown

## Overview

Read `.forge/prd.md`, `.forge/architecture.md`, and `.forge/contracts/` to produce `.forge/tasks.yaml` — a sized, dependency-ordered list of tasks where each task is a thin vertical slice through all layers. Output feeds `incremental-implementation`.

## When to Use

- `.forge/prd.md` and `.forge/architecture.md` both exist
- Ready to break work into implementable tasks before coding starts
- Need to identify dependencies and parallelize work

## When NOT to Use

- Architecture doesn't exist yet — run `architecture-and-contracts` first
- PRD is not complete — gaps produce tasks with unknown scope
- Single-module change with no integration — implement directly with `tdd`

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "I can keep the task list in my head" | Tasks in your head have no acceptance criteria |
| "We'll figure out dependencies as we go" | Undiscovered dependencies stall work mid-implementation |
| "All tasks are the same size" | They never are — sizing forces honest scope assessment |
| "Vertical slicing is overkill here" | Horizontal slicing (all API, then all UI) delays feedback until integration |
| "Tasks can reference file paths" | File paths rot — describe behaviors and module names |

## Red Flags

- Tasks that touch more than 3 modules (not a vertical slice — split it)
- No acceptance criteria per task (untestable)
- No dependency graph (implementation order unknown)
- Task descriptions name files/functions instead of behaviors
- XL tasks with no breakdown path (too much unknown — spike first)
- All tasks marked "no dependencies" (integration is being deferred)

## Core Process

### Step 1: Read the artifacts

Read `.forge/prd.md` for requirements. Read `.forge/architecture.md` for components. Read all files in `.forge/contracts/` for module interfaces.

### Step 2: Identify vertical slices

Each task must be a tracer bullet: a thin but complete path through ALL layers. Not "implement the API" — that's horizontal. Instead: "user can submit a form and see a success message" — that's a vertical slice cutting through UI, API, and storage.

Rules:
- Completed task is demoable or verifiable on its own
- Each slice covers one user story or one acceptance criterion
- Prefer many thin tasks over few thick ones
- Tasks must reference contract names, not file paths

### Step 3: Size each task

| Size | LOC estimate | Description |
|------|-------------|-------------|
| XS | < 20 | Config change, single function, text update |
| S | 20–100 | Single module change with tests |
| M | 100–300 | One vertical slice through 2-3 modules |
| L | 300–600 | Multi-slice with integration wiring |
| XL | 600+ | Too large — decompose or spike first |

### Step 4: Map dependencies

For each task, list which other tasks must complete first. Build the dependency graph. Identify the critical path and which tasks can run in parallel.

### Step 4b: Tag tasks with shaping skills (optional but recommended)

For each task, decide which other forge-skills shape the implementation and add a `skills:` field. This is read by `incremental-implementation` before the first test is written, loading the relevant constraints into context at the moment they're needed.

Common patterns:
- UI work touching components → include `design-system`, `accessibility`
- Interaction shape decisions (modal vs sheet, expand vs nav) → include `interaction-patterns`
- New REST endpoints → include `api-design`
- Migrations or schema changes → include `database-design`
- Tasks producing observability or alerts → include `observability`
- Tasks with non-trivial error paths → include `error-handling-and-resilience`

Omit the field if the task is pure plumbing with no domain-shaping skill applicable. Leaving it blank is fine — `incremental-implementation` treats `skills:` as optional and backward compatible.

### Step 5: Quiz the user

Present the breakdown. For each task: title, size, dependencies, acceptance criteria. Ask: granularity right? Dependencies correct? Any tasks to merge or split?

Iterate until approved.

### Step 6: Write .forge/tasks.yaml

Prepend a `forge:meta` header (`generated_by: planning-and-task-breakdown`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/prd.md, .forge/architecture.md, .forge/contracts/*]` — paths only, never hashes, `generated_from: {.forge/prd.md: <hash>, .forge/architecture.md: <hash>, .forge/contracts/<each-resolved>.md: <hash>}` — each upstream's content_hash AT generation time, `content_hash: <sha256 first 8 over THIS file's body, excluding the forge:meta block>`) — comment-style for YAML (`# forge:meta ...`).

**Co-output rule:** `tasks.yaml` and `tasks-summary.md` are co-generated in this single skill run. Both files MUST carry the **same** `depends_on` AND **same** `generated_from` set (`[.forge/prd.md, .forge/architecture.md, .forge/contracts/*]`). Do NOT write `tasks-summary.md` with `depends_on: [.forge/tasks.yaml]` — that creates a silent staleness bug where a PRD edit flips `tasks.yaml` stale but leaves `tasks-summary.md` UP_TO_DATE. See [forge-dependency-graph: co-output rule](../../references/forge-dependency-graph.md#co-output-rule).

```yaml
# forge:meta
#   generated_by: planning-and-task-breakdown
#   generated_at: 2026-05-13T12:00:00Z
#   depends_on: [.forge/prd.md, .forge/architecture.md, .forge/contracts/*]
#   generated_from:
#     .forge/prd.md: <prd.md's content_hash at this moment>
#     .forge/architecture.md: <architecture.md's content_hash at this moment>
#     .forge/contracts/auth-service.md: <hash>   # one entry per resolved glob match
#   content_hash: <first 8 chars of sha256 over THIS file's body>

tasks:
  - id: T001
    title: "User can submit registration form"
    size: M
    phase: 1
    depends_on: []
    contracts: [UserService, SessionService]
    skills: [api-design, design-system, accessibility]   # optional — read by /build before first test
    acceptance_criteria:
      - Given valid email+password, form submission creates a user and redirects to dashboard
      - Given duplicate email, submission returns inline validation error
      - Given network failure, form shows retry option without data loss
    verification:
      - Unit tests for UserService.create() covering success and duplicate cases
      - Integration test: POST /register with valid payload returns 201 + session cookie
      - E2E: form submission with valid data lands on dashboard
    files_likely_affected:
      - UserService (new)
      - registration route handler (new)
      - registration form component (new)
    status: pending          # pending | in_progress | done | split | blocked
    started_at: null
    completed_at: null
    commit: null
    notes: []

  - id: T002
    title: "..."
    depends_on: [T001]
    status: pending
    ...
```

### Step 7: Write .forge/tasks-summary.md

Produce a human-readable summary alongside the YAML. Prepend its own `forge:meta` header with the **same** `depends_on` set as `tasks.yaml` (`[.forge/prd.md, .forge/architecture.md, .forge/contracts/*]`) — see the co-output rule above. Use `<!-- forge:meta ... -->` (Markdown, not YAML comment form).

Contents:
- **Day-by-day ship view**: which tasks ship on which days (estimated)
- **Critical path**: the longest dependency chain — this sets the minimum timeline
- **Risk days**: days with the highest-complexity tasks or most integration points
- **Parallel work opportunities**: tasks that can run simultaneously with different engineers
- **Buffer recommendations**: where to add slack based on task size and uncertainty

## Verification

- [ ] `.forge/tasks-summary.md` written with ship view and critical path
- [ ] All user stories from PRD covered by at least one task
- [ ] No task touches more than 3 modules
- [ ] Every task has at least 2 acceptance criteria
- [ ] Every task has a verification step (what proves it's done)
- [ ] Every task has lifecycle fields initialized: `status: pending`, `started_at: null`, `completed_at: null`, `commit: null`, `notes: []`
- [ ] UI tasks tagged with `design-system` + `accessibility`; endpoint tasks tagged with `api-design`; schema tasks tagged with `database-design`
- [ ] Dependency graph has no cycles
- [ ] No XL tasks without a spike or decomposition plan
- [ ] Task descriptions use module/contract names, not file paths
- [ ] `.forge/tasks.yaml` written and parseable
- [ ] User approved the breakdown before writing the file

## Fit-Check

Before declaring done, emit one of:

- A short list of specific fit issues observed (e.g., "Plan produced 4 tasks for what is genuinely a 2-hour single-file change — task overhead exceeds the work; recommend `incremental-implementation` directly" / "skills: tags don't apply — this is a backend-only project with no design-system or accessibility concerns").
- The explicit line: **"No fit issues observed for this use case."**

Silence is not allowed. See [docs/skill-anatomy.md#fit-check](../../docs/skill-anatomy.md#fit-check-the-meta-honesty-step).
