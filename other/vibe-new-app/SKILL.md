---
name: vibe-new-app
description: >
  Full spec-driven setup workflow for building a brand new app from scratch with an AI coding agent.
  Triggers on "new:" prefix, "I want to build a new app", "starting a new project",
  "help me spec out a new app", "new project".
  Always use when the user is starting a greenfield project — even without the exact prefix.
  Generates CLAUDE.md at project root and the complete vibe/ folder.
  Reads BRIEF.md and ARCHITECTURE.md if they exist — skips questions already answered.
  Step 5 generates a complete multi-phase feature map in PLAN.md — every feature sequenced,
  dependencies explicit, parallel opportunities identified, future phases sketched.
  TASKS.md Phase 2+ shows ordered features with dependencies visible — not slugs.
  Generates a minimal ARCHITECTURE.md from PLAN.md if architect: was skipped.
  TASKS.md is the single human-facing file. TODO.md does not exist.
  Requires: frontend-design skill for Step 3 wireframe generation.
---

# Vibe New App Skill

Generates the complete project kit from brief and architecture.
Produces CLAUDE.md at project root and the full vibe/ folder the AI coding agent uses.

**Always run in Plan Mode (Shift+Tab). Exit Plan Mode only before task execution.**

> **Autonomous / headless mode.** At startup resolve the settings with
> `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode`. If `vibe_mode` is
> `autonomous`, every "wait", "ask", "confirm" and approval step in this skill follows
> vibe-mode's `references/HEADLESS.md` §2 instead: take the recommended option, accept your
> own draft after one self-check, log each choice to `vibe/DECISIONS.md`, never ask the
> user, and stop — writing `vibe/.run_state.json` — only when a person is genuinely required.

---

## The O'Reilly principles this enforces

**Spec before code** — SPEC.md with acceptance criteria exists before any task runs.
**Context preservation** — CLAUDE.md, CODEBASE.md, ARCHITECTURE.md, SPEC_INDEX.md, TASKS.md
read every session so the agent never re-discovers what's been built.
**Incremental verifiable progress** — TASKS.md breaks the build into single verifiable tasks.
**Drift prevention** — DECISIONS.md created ready to log from the first task forward.

---

## Two audiences. Two file types.

**Human-facing — open this:**
- `vibe/TASKS.md` — your single progress view. Plain English. Updated after every task.

**Agent-facing — agent reads these, you never need to open them:**
- `CLAUDE.md` · `vibe/ARCHITECTURE.md` · `vibe/CODEBASE.md`
- `vibe/SPEC.md` · `vibe/SPEC_INDEX.md` · `vibe/PLAN.md` · `vibe/DECISIONS.md`
- `vibe/IMPLEMENTATION_LOG.md` — agent: append-only implementation-decision log (why-this-approach / why-this-library)
- `vibe/DESIGN_SYSTEM.md` *(created by design: — agent reads for design context)*
- `vibe/reviews/` · `vibe/features/` · `vibe/bugs/` · `vibe/backlog/`

---

## Folder structure this skill creates

```
your-project/
├── BRIEF.md                   ← brainstorm output (if exists)
├── CLAUDE.md                  ← agent rules — auto-read by Claude Code
└── vibe/
    ├── TASKS.md               ← YOUR progress view — only file you open
    ├── ARCHITECTURE.md        ← agent: patterns, read every session
    ├── CODEBASE.md            ← agent: live codebase snapshot
    ├── SPEC.md                ← agent: full requirements
    ├── SPEC_INDEX.md          ← agent: compressed spec map
    ├── PLAN.md                ← agent: phases and architecture
    ├── DECISIONS.md           ← agent: spec/scope drift and change log (append-only)
    ├── IMPLEMENTATION_LOG.md  ← agent: implementation-decision log — why-this-approach (append-only)
    ├── DESIGN_SYSTEM.md       ← agent: design tokens (created by design:)
    ├── reviews/
    │   └── backlog.md
    ├── features/
    ├── bugs/
    └── backlog/
```

Note: `vibe/DESIGN_SYSTEM.md` is not created here — it is generated the first time
`design:` runs. The agent checks for it at session startup and reads it if it exists.

---

## Step 1 — Capture the idea and check for existing files

**Run the parity check first.** Read `references/PIPELINE.md` and follow its parity
check: classify UI vs non-UI, detect the pipeline stage, and route to any missing
upstream step. In particular:
- If `BRIEF.md` is **missing, empty, or in a foreign shape** (an idea pasted or
  dropped from elsewhere, e.g. the Claude desktop app): route to `brainstorm:`
  first — its Step 0 ingests and normalizes external input into a canonical
  BRIEF.md. This is what brings an externally-produced idea to parity. Don't
  scaffold from a hollow or non-canonical brief.
- Note whether this is a **UI project** — it determines the design gate in Step 10C.

**Then check for BRIEF.md and ARCHITECTURE.md at project root.**

**Both exist** (ran brainstorm: and architect: — recommended path):
- Read both fully before doing anything else
- Confirm: "Found brief and architecture. [App name] — [core value]. [N] decisions locked. Building from these — no repeated questions."
- Pre-populate Steps 2–5 from BRIEF.md. Use ARCHITECTURE.md for PLAN.md folder structure and CLAUDE.md conventions.
- Skip all answered questions. Surface open questions from the brief.

**Only BRIEF.md exists** (ran brainstorm: but not architect:):
- Read BRIEF.md fully
- Confirm: "Found brief. [App name] — [core value]. [N] decisions locked."
- Pre-populate Steps 2–5. Skip answered questions.
- Note: architect: was skipped — minimal ARCHITECTURE.md will be generated from PLAN.md decisions in Step 9.

**Neither exists** (starting fresh — not recommended but supported):
- Extract: what the app does, who uses it, the core value.
- If unclear, ask the few genuinely-needed clarifying questions together (batched,
  not one at a time) — but only what you actually need to proceed.
- Confirm: "Got it — building [X] for [who], core value: [Y]. Starting spec."
- Note: both BRIEF.md and ARCHITECTURE.md will be absent — minimal versions generated.

---

## Step 2 — Generate vibe/SPEC.md

Draft SPEC.md covering:
1. **Overview** — What this app does and why (2-3 sentences)
2. **Target users** — Who uses this and what they need
3. **Core features** — Each feature with acceptance criteria
4. **Out of scope** — Explicitly NOT in v1
5. **Tech stack** — Confirmed choices with reasoning
6. **Data model** — Key entities and relationships
7. **API shape** — Core endpoints (if applicable)
8. **Non-functional requirements** — Performance, security, responsiveness
9. **Conformance checklist** — What must be true for v1 to be done

Present draft. Ask: "Does this spec look right? Anything to add, change, or cut?"
Wait for approval. Save as `vibe/SPEC.md`.

**Living document rules:**
- Edit in-place on scope changes (via `change:` only — never informally)
- ~~Strikethrough~~ for removed items — never delete
- Update note at top: `> ⚠️ Last updated: [date] · [reason]`
- SPEC.md and SPEC_INDEX.md always updated as a pair — never one without the other

---

## Step 3 — UI Design

**Requires: frontend-design skill.** If not installed, proceed with prose wireframe description.

**If `DESIGN.md` (project root) or `vibe/design/CONTRACT.md` already exists**
(the user ran `design-md:` / `design:` first), read it and treat its tokens as
authoritative — the wireframe must use those colours/type/spacing rather than
inventing a new aesthetic. `DESIGN.md` wins where it and `DESIGN_SYSTEM.md` conflict.

Tell the user: "Before planning the build phases, let's lock the UI."

Ask all at once:
1. **Screens** — How many screens/views? List briefly.
2. **Primary screen** — Where do users spend most time?
3. **Layout & nav** — Preferences? (sidebar, bottom nav, top nav — or no preference)
4. **Device** — Desktop only, mobile first, or both?
5. **Interactions** — Anything complex? (drag-drop, real-time, multi-step)
6. **References** — Any apps whose UI you like?
7. **Constraints** — Component library already chosen? Anything must show above fold?

Wait for answers. Generate wireframe using **frontend-design skill** principles:
- Commit to a bold, intentional aesthetic based on the app's purpose
- Complete HTML wireframe artifact covering all screens
- Realistic placeholder content — not Lorem ipsum
- Show navigation between screens

Present wireframe. Iterate until approved. Append UI Specification to vibe/SPEC.md:

```
## UI Specification
### Design direction
[One sentence: aesthetic direction and why]
### Component library
[What's being used, or "none specified"]
### Navigation structure
[Top-level destinations and flow — locked here, expensive to change mid-build]
### Screens
#### [Screen name]
- **Purpose**: [What the user does here]
- **Layout**: [Describe]
- **Key components**: [List]
- **User interactions**: [What the user can do]
- **States**: [Empty, loading, error states]
### Responsive behaviour
[Desktop/mobile approach]
```

Tell the user: "UI spec locked. Moving to planning."

---

## Step 4 — Generate vibe/SPEC_INDEX.md

Read vibe/SPEC.md in full. Generate SPEC_INDEX.md — compressed map under 40 lines:

```
# SPEC_INDEX — [Project Name]
> Compressed map of SPEC.md. Read each session. Fetch only the section you need.
> Last synced: [date]
## Overview — [one sentence] → SPEC.md#overview
## Features — [Feature]: [one sentence] (N criteria) → SPEC.md#feature-name
## UI — [N screens, direction summary] → SPEC.md#ui-specification
## Boundaries — Out of scope: [N items] → SPEC.md#out-of-scope
## Technical — Stack: [key choices] · Data: [N entities] · API: [N endpoints]
## Done condition — Conformance: [N items] → SPEC.md#conformance-checklist
## Backlog — [N items deferred] → vibe/backlog/
```

Save as `vibe/SPEC_INDEX.md`.
Rule: SPEC.md and SPEC_INDEX.md always committed together. Never one without the other.

---

## Step 5 — Generate vibe/PLAN.md

Read `references/PLAN_MD.md` for the full template.
Read vibe/SPEC.md in full. Read ARCHITECTURE.md if it exists.
Read BRIEF.md — specifically: feature list, non-goals, complexity estimate.

The critical section is the **Feature Map** (Section 6).
This is the complete build plan — every feature, every phase, fully sequenced.
It is not a list of slugs. It is not deferred to later.
It is planned now, before Phase 1 begins.

**Step 5A — Draft Sections 1–5 (structure, stack, architecture, data model, API):**

These are standard — fill from SPEC.md and ARCHITECTURE.md.
Identify shared data now: which tables/entities will be read or written by
multiple features. List them explicitly in Section 4 "Shared data" table.
This is the most common source of inter-feature conflicts caught too late.

**Step 5B — Build the Feature Map (Section 6) — the most important step:**

> 🧠 **Effort:** sequencing features by dependency is the reasoning that every
> later build wave and parallel dispatch relies on. Run it at high/xhigh effort
> with adaptive thinking — get the dependency ordering and shared-data analysis
> right here, because errors propagate through the whole build.

Read vibe/SPEC.md features section. Read BRIEF.md feature list and non-goals.

For every v1 feature, determine:

1. **Build order** — which features have no dependencies (start here),
   which need another feature's data model first, which can run in parallel.

   Ask yourself for each feature:
   - Does this feature READ data created by another feature?
     → It depends on that feature. Build that one first.
   - Does this feature WRITE data that another feature reads?
     → It must come before that feature.
   - Do two features share NO data writes and have the same dependencies?
     → They can run in parallel. Mark both explicitly.

2. **Shared data** — which entities/tables are created by one feature
   and consumed by another. These are the inter-feature dependency points
   that cause mid-build surprises if not planned now.

3. **Future phase sketch** — for Phase 4+ features from BRIEF.md backlog:
   note what Phase 1-3 must NOT hard-code to keep them possible.
   This prevents architectural decisions that feel fine now but block v2.

Build the dependency diagram:
```
Phase 1 complete
    ↓
[Feature with no deps — can start immediately after Phase 1]
    ↓              ↓
[Next feature]  [Parallel feature — no shared writes]
    ↓
[Feature that needs both above]
```

If the dependency order is unclear — ask the user ONE focused question:
> "Does [Feature B] need [Feature A]'s [entity] to exist first, or can they be built independently?"

**Step 5C — Present the feature map for approval:**

> "Here's the complete build plan — all phases mapped out before we start.
>
> [Present the feature map — Phase 1, Phase 2 ordered features with deps,
> Phase 3 tasks, Phase 4+ sketch if applicable]
>
> Build order for Phase 2:
> [ASCII dependency diagram]
>
> Parallel opportunities: [list features that can run simultaneously]
> Shared data points: [list entities that cross feature boundaries]
>
> Does this sequencing look right? Any features that should move earlier or later?"

Wait for approval. Adjust if needed.

**Step 5D — Save as `vibe/PLAN.md`.**

The feature map in PLAN.md is the source of truth for:
- TASKS.md Phase 2+ section (generated from it in Step 7)
- vibe-add-feature (reads it before drafting each feature spec)
- vibe-change-spec (reads it to assess phase impact of scope changes)
- vibe-parallel (reads dependency diagram for wave planning)

---

## Step 6 — Generate CLAUDE.md (project root)

Read vibe/SPEC.md, vibe/PLAN.md, vibe/ARCHITECTURE.md (if exists).
Read `references/CLAUDE_MD.md` for the full template.

Generate CLAUDE.md at **project root** substituting all [placeholders]:
- Project overview from SPEC.md
- Tech stack from PLAN.md
- Commands from chosen stack
- Code style and naming from ARCHITECTURE.md (if exists) or PLAN.md
- Phase gates section — mandatory review gates baked in from day one
- Execution mode section — the three settings **as resolved now** by
  `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode` (never hardcode
  `manual`: a driver may have set `VIBE_MODE=autonomous` in the environment)
- Session completion checklist — the 10-step post-task sequence (full checklist from template)
- CLAUDE.md active feature sections — cleanup rule included

**The per-task "next" sequence must be included verbatim in CLAUDE.md:**

```
## Per-task sequence (runs on every "next")

1. Verify acceptance criteria in FEATURE_TASKS.md are all ticked
2. Run tests: `[test command]` — must pass before commit
3. Run lint: `[lint command] --silent` — must pass before commit
4. Commit code changes — stage the files THIS task touched, not `git add -A`
   (blanket-staging risks committing .env, build artifacts, or stray files;
   ensure .gitignore covers .env*, node_modules, build output first):
   git add [the specific paths this task created/modified]
   git commit -m "feat([scope]): [TASK-ID] — [one line plain English description]"
5. If this task made a MEANINGFUL implementation decision (hard to reverse · picked
   among real alternatives — a library/pattern/data-model/API shape · would surprise a
   future reader · deviates from ARCHITECTURE.md), append one entry to
   vibe/IMPLEMENTATION_LOG.md per the schema in that file's header (newest last; set
   Touches: to the files/functions changed). Routine work needs no entry — don't add noise.
6. Commit doc updates separately:
   git add vibe/TASKS.md vibe/DECISIONS.md vibe/IMPLEMENTATION_LOG.md vibe/CODEBASE.md
   git commit -m "docs(TASKS): mark [TASK-ID] done — [plain English]"
7. Update "What just happened" and "What's next" in vibe/TASKS.md
8. Re-read vibe/TASKS.md silently
9. State next task in plain English and confirm before starting

Rules:
- NEVER skip the commit step — uncommitted work is invisible to vibe-graph and vibe-review
- Code commit and doc commit are ALWAYS separate — never mix feat and docs in one commit
- If tests fail — fix before committing, do not commit broken code
- If lint fails — fix before committing, do not commit with lint errors
```

**Investigation discipline (include verbatim):**
```
## Investigation discipline
For requests under 10 words: restate intent in one sentence before reading any files.
Data/state operations (reset, clear, seed, refresh) are not code bugs — do not investigate code.
Confirm the actual request before opening any file.
```

Save as `CLAUDE.md` at project root.

---

## Step 7 — Generate vibe/TASKS.md

Read `references/TASKS_MD.md` for full template and update rules.
Read vibe/SPEC.md, vibe/SPEC_INDEX.md, vibe/PLAN.md — especially Section 6 (Feature Map).

Generate TASKS.md with every phase fully represented:

**Header section:**
```
# TASKS — [Project Name]
> [2-3 plain English sentences: what this app does, who it's for, core value]
> One file to watch. Updated after every task.
```

**Phase 1 — Foundation:**
Each task as a checkbox with one plain English line.
```
## Phase 1 — Foundation
> No user-facing features. Sets up everything Phase 2 depends on.
> Phase 1 exit: run `review: phase 1` when all tasks complete.

[ ] P1-001 · [Task] — [one plain English line]
[ ] P1-002 · [Task] — [one plain English line]
...
[ ] P1-00N · Populate CODEBASE.md — document everything built in Phase 1

## Phase 1 gate
⬜ review: phase 1 — pending

## Design gate (UI projects)
⬜ design: — pending · UI features in Phase 2 need a design language first
   (run `design-md:` then `design:`, or `design:` alone). Skip only for non-UI.
```

**Phase 2 — Core features (fully ordered from PLAN.md feature map):**

This is the critical change. Phase 2 is not slugs — it is the complete
ordered feature list with dependencies visible, derived from PLAN.md Section 6.

```
## Phase 2 — Core features
> Build order is deliberate. Features are sequenced by dependency.
> A feature marked [needs: X] cannot start until X is complete.
> Features marked [parallel with: X] can run simultaneously with X.
> Phase 2 exit: run `review: phase 2` when all features complete.

⬜ [Feature 1 name] — [what the user can do when this is done]
   Build order: 1 · No dependencies · Start here after Phase 1 gate passes
   Shared data: creates [Entity] used by Feature 2 and Feature 3
   Estimate: ~[N] hours
   Spec: run `feature: [name]` to plan this feature in detail

⬜ [Feature 2 name] — [what the user can do]
   Build order: 2 · Needs: Feature 1 complete
   Reason: reads [Entity] created by Feature 1
   Parallel with: Feature 3 (no shared writes)
   Estimate: ~[N] hours
   Spec: run `feature: [name]` to plan this feature in detail

⬜ [Feature 3 name] — [what the user can do]
   Build order: 2 · Needs: Feature 1 complete
   Parallel with: Feature 2 (no shared writes)
   Estimate: ~[N] hours
   Spec: run `feature: [name]` to plan this feature in detail

⬜ [Feature 4 name] — [what the user can do]
   Build order: 3 · Needs: Feature 2 + Feature 3 complete
   Reason: reads [Entity] from Feature 2 and [Entity] from Feature 3
   Estimate: ~[N] hours
   Spec: run `feature: [name]` to plan this feature in detail

## Phase 2 gate
⬜ review: phase 2 — pending
```

**Phase 3 — Polish and hardening:**
```
## Phase 3 — Polish and hardening
> Runs after Phase 2 gate passes. No new features.
> Phase 3 exit: run `review: final` — 0 P0 + 0 P1 before deploy.

⬜ Performance audit — profile and fix slow paths
⬜ Error handling pass — all edge cases, empty states, error boundaries
⬜ Accessibility audit — WCAG AA for all screens
⬜ E2E tests — critical user flows automated
⬜ Security review — auth, input validation, secrets, dependencies
⬜ Documentation — README, API docs, deployment guide

## Final gate
⬜ review: final — pending
```

**Phase 4+ (if in PLAN.md — future phases sketched):**
```
## Phase 4+ — Future (not in current build)
> Planned so Phase 1-3 architecture doesn't foreclose these.
> Run `brainstorm:` when ready to plan the next version.

⬜ [Future feature] — [one sentence] · planned for v2
⬜ [Future feature] — [one sentence] · planned for v2
```

**Footer:**
```
---
## What just happened
[Project name] project kit created. Phase 1 ready to begin.

## What's next
⬜ P1-001 · [First Phase 1 task in plain English]
Start Phase 1: read CLAUDE.md then vibe/TASKS.md. Say "next" for each task.
Run `review: phase 1` when all Phase 1 tasks are complete.
```

**Non-negotiable rules:**
- Build order and dependency reasons visible for every Phase 2+ feature
- `feature: [name]` trigger visible on every planned feature — user knows exactly what to run
- Phase gate instruction visible at end of each phase
- Plain English everywhere — what the user sees/experiences, not technical details
- Human should never need to open PLAN.md to know what to build next or in what order

Save as `vibe/TASKS.md`.

---

## Step 8 — Generate vibe/CODEBASE.md (placeholder)

Read `references/CODEBASE_MD.md` for the full template.

For a new app, CODEBASE.md starts as a placeholder.
The last task in Phase 1 populates it fully from the scaffolded project.

Generate the placeholder version. Save as `vibe/CODEBASE.md`.

---

## Step 9 — Generate remaining vibe/ files and handle ARCHITECTURE.md

### vibe/DECISIONS.md

```
# DECISIONS — [Project Name]
> Append-only. Every drift, scope change, tech choice — logged with full context.

## Decision types
- drift — deviated from PLAN.md or ARCHITECTURE.md
- blocker-resolution — impossible; workaround found
- tech-choice — chose between valid approaches not in plan
- scope-change — added/removed via change: command
- discovery — unexpected finding affecting future tasks

## Format
### D-[ID] — [Short title]
- **Date**: · **Task**: [TASK-ID] · **Type**: [type]
- **What was planned**: · **What was done**: · **Why**: 
- **Alternatives considered**: · **Impact on other tasks**:
- **Approved by**: human | agent-autonomous

(No entries yet)
```

### vibe/IMPLEMENTATION_LOG.md

Write this file from the canonical template in
`references/IMPLEMENTATION_LOG_MD.md` (use the **FILE TEMPLATE** block there verbatim).
It is the append-only **implementation-decision** log — code-altitude "why this approach,
why this library" — the companion to DECISIONS.md (which stays at spec/scope altitude).
It starts empty; the build skills append to it as meaningful decisions are made, and
`Touches:` lines link each decision to vibe-graph nodes. Do not duplicate the schema here —
the file's own header carries it.

### vibe/reviews/ folder

Create `vibe/reviews/backlog.md`:
```
# Review Backlog
> P1/P2/P3 issues tracked across all phase reviews.
> P1 must resolve before deploy. Updated after every review.
## Outstanding P1 Issues
(none yet)
## Outstanding P2 Issues
(none yet)
## Resolved Issues
(none yet)
```

### ARCHITECTURE.md handling

**If ARCHITECTURE.md exists at project root:** Move to `vibe/ARCHITECTURE.md`.

**If ARCHITECTURE.md does not exist** (architect: was skipped):
Generate a minimal `vibe/ARCHITECTURE.md` from PLAN.md decisions:
- Extract the folder structure, naming conventions, and tech choices from PLAN.md
- Apply the O'Reilly Principles section verbatim from `references/ARCHITECTURE_MD.md`
- Mark it clearly: `> ⚠️ Auto-generated from PLAN.md — architect: was not run.`
- `> Consider running architect: to make these decisions explicit and add missing sections.`
This ensures review: has an ARCHITECTURE.md to check against from Phase 1.

---

## Step 10 — Spec review gate

Before telling the user the kit is ready, announce and hand off to spec-review:

> "vibe/ folder created. Running spec-review before first task..."

Invoke `vibe-spec-review` with:
- Trigger source: `new-app`
- Scope: SPEC.md + ARCHITECTURE.md + BRIEF.md + AGENT_ARCH.md (all that exist)

After spec-review completes:

## Step 10B — Initialise dependency graph

Invoke `vibe-graph: init`.

This builds the spec graph from SPEC.md and ARCHITECTURE.md —
all planned nodes created before any code is written.
Nodes will transition from `planned` to `built` as features are implemented.

After graph init completes:

## Step 10S — Record the spec sign-off

The spec gate is the person's sign-off on the plan the build will follow. Record it in
`vibe/.gates.json` (and the `## Spec gate` line in TASKS.md) with the helper — pass the
spec-review report from Step 10 as `--report`:

```bash
VS="$HOME/.claude/skills/vibe-mode/scripts/vibe_state.py"
python3 "$VS" mode        # → vibe_mode, approvals
```

- **Manual mode:** the user approved the SPEC in Step 2 and has seen the spec review —
  `python3 "$VS" gate set spec --status approved --by human --report [report]`.
- **Autonomous, `APPROVALS=auto`:** `gate set spec --status approved --by agent-autonomous --report [report]`, and continue.
- **Autonomous, `APPROVALS=human`:** `gate set spec --status pending --report [report]`,
  then STOP — `python3 "$VS" run-state set --status needs_human --reason spec_approval --next "approve the spec, then run vibe-mode: run"`
  — and end the session. Do not start the design or any task. `vibe-mode: run` resumes
  from here once the spec is approved (HEADLESS.md §5).

## Step 10C — Design gate (UI projects)

Design is a required pipeline step for UI projects, not an afterthought (see
`references/PIPELINE.md`). Do not let the build start UI features with no design
language — that is the "it skipped design" failure.

- **Non-UI project** (API / CLI / library / pure backend): skip this step; note
  "design gate N/A — no UI", record it with `vibe_state.py gate set design --status na`,
  and continue.
- **UI project, no design system yet** (`DESIGN.md` / `vibe/DESIGN_SYSTEM.md` /
  `vibe/design/CONTRACT.md` all absent): announce and hand off —
  > "This is a UI project. Before building screens, let's lock the design so they
  >  share one derived design language. Optionally run `design-md:` first to
  >  capture brand tokens, then `design:` to produce the design contract.
  >  Recommended. Reply 'skip design' to build without a design pass."
  Invoke `design:` on a clear yes; when the user approves the result, record
  `gate set design --status approved --by human`. If the user says skip, log it in
  `vibe/DECISIONS.md` ("design gate skipped by user") so it's a visible decision, and
  record `gate set design --status skipped`.
- **Design system already exists** (user ran `design-md:`/`design:` earlier):
  design gate already passed — record `gate set design --status approved --by human` if
  it isn't recorded yet, and continue.
- **Autonomous mode (UI project, no design system):** never skip. Run `design:` up to its
  Step 3.5 checkpoint (contract, tokens, preview — no production UI files before sign-off), then
  `design: critique`, then one `design: fix must` pass. Then per `APPROVALS`:
  `auto` → `gate set design --status approved --by agent-autonomous --report vibe/design/critique.md`
  and continue; `human` → `gate set design --status pending --report vibe/design/critique.md`,
  STOP with `run-state set --status needs_human --reason design_approval --next "approve the design, then run vibe-mode: run"`,
  and end the session.

The generated TASKS.md carries a matching **Design gate** line before Phase 2 so
this is visible in the human-facing plan.

After the design gate resolves:

## Step 10D — Install the gate hard-lock (git pre-push hook)

The phase/deploy gates are enforced by flow + `vibe/.gates.json` (see
`vibe-review/references/GATES.md`), but the only true machine-level lock is a git
hook. Offer to install it:

> "Install the gate hard-lock? It blocks `git push` while any review gate is open
>  (P0 or P1 outstanding) — so quality gates hold even if a step is skipped. Override
>  anytime with `git push --no-verify`. (y/n)"

If yes, write `.git/hooks/pre-push` (chmod +x) with the check from GATES.md
(reads `vibe/.gates.json`; any `open` gate → exit 1). If the project uses husky,
add it as a husky `pre-push` instead. If declined, note it — gates then rely on
flow + state only. In autonomous mode, install it (the recommended option) and note it
in DECISIONS.md.

## Step 11 — Tell the user

---
> 🎉 **Your project kit is ready.**
>
> **One file to watch:** `vibe/TASKS.md`
>
> **Structure created:**
> ```
> CLAUDE.md
> vibe/TASKS.md        ← open this
> vibe/ARCHITECTURE.md ← [locked from architect: / auto-generated from plan]
> vibe/CODEBASE.md     ← placeholder until Phase 1 done
> vibe/SPEC.md + SPEC_INDEX.md + PLAN.md + DECISIONS.md
> vibe/IMPLEMENTATION_LOG.md  ← implementation decisions logged as you build
> vibe/reviews/backlog.md
> vibe/spec-reviews/   ← spec review history
> vibe/graph/          ← dependency graph (spec graph initialised)
> ```
> **Spec review:** [✅ clean / ⚠️ [N] warnings acknowledged / 🔴 [N] P0s fixed]
> **Graph:** [N] planned nodes · [N] concepts mapped · updates automatically
>
> **Read execution mode:**
> ```bash
> python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode
> ```
>
> If `autonomous` → read the vibe-mode skill's `references/AUTONOMOUS_EXECUTION_BLOCK.md`
> (resolve the vibe-mode install dir — commonly `~/.claude/skills/vibe-mode/`, or
> `~/.claude/plugins/marketplaces/*/skills/vibe-mode/` under a plugin install)
> and follow the autonomous execution protocol for Phase 1 tasks. Begin immediately.
> (If Step 10S or 10C stopped for an approval, the session has already ended — this
> step runs on the resumed session instead.)
>
> If `manual` or not set → tell the user:
> ```
> Read CLAUDE.md, then vibe/CODEBASE.md, then vibe/ARCHITECTURE.md,
> then vibe/SPEC_INDEX.md, then vibe/TASKS.md.
> Confirm the first task before writing any code.
> ```
> Say **"next"** after each task.
> Run **"review: phase 1"** when Phase 1 completes — mandatory gate.
---
