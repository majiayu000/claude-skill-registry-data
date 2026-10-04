---
name: vibe-add-feature
description: >
  Full spec-driven workflow for adding a feature to an existing codebase with an AI coding agent.
  Triggers on "feature:" prefix, "I want to add a feature", "add X to my project",
  "new feature", "build a feature for".
  Always use when adding functionality to an existing project — even without the exact prefix.
  Reads PLAN.md feature map before drafting — checks build order, dependencies, shared data.
  Stops and surfaces clearly if dependencies are not yet met. Marks unplanned features explicitly.
  Updates PLAN.md feature map after planning so it stays the live source of truth.
  Creates vibe/features/[date-slug]/ with FEATURE_SPEC.md, FEATURE_PLAN.md, FEATURE_TASKS.md.
  Checks for existing incomplete feature with same name before creating a duplicate.
  Reads SPEC.md before drafting to align with existing acceptance criteria.
  Updates TASKS.md (human progress view) and agent files.
---

# Vibe Add Feature Skill

Spec-driven feature planning for an existing project.
Creates a dated feature folder and updates the human progress view.
CODEBASE.md verified or generated first — future sessions never re-read from scratch.

**Always run in Plan Mode (Shift+Tab). Exit before executing tasks.**

> **Autonomous / headless mode.** At startup resolve the settings with
> `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode`. If `vibe_mode` is
> `autonomous`, every "wait", "ask", "confirm" and approval step in this skill follows
> vibe-mode's `references/HEADLESS.md` §2 instead: take the recommended option, accept your
> own draft after one self-check, log each choice to `vibe/DECISIONS.md`, never ask the
> user, and stop — writing `vibe/.run_state.json` — only when a person is genuinely required.

---

## The O'Reilly principles this enforces

**Spec before code** — FEATURE_SPEC.md with acceptance criteria exists before any task.
**Context preservation** — CODEBASE.md read first, ARCHITECTURE.md conventions followed.
**Incremental verifiable progress** — task breakdown with S/M/L estimates.
**Drift prevention** — DECISIONS.md updated, CLAUDE.md active feature section appended.

---

## Two audiences. Two file types.

**Human-facing:**
- `vibe/TASKS.md` — single progress view, plain English, updated after every task

**Agent-facing (human never opens these):**
- `vibe/features/[date-slug]/FEATURE_SPEC.md`
- `vibe/features/[date-slug]/FEATURE_PLAN.md`
- `vibe/features/[date-slug]/FEATURE_TASKS.md`
- `vibe/CODEBASE.md` · `vibe/ARCHITECTURE.md` · `vibe/DECISIONS.md` · `CLAUDE.md`

---

## Folder structure this skill creates

```
vibe/
├── TASKS.md                            ← human progress view — updated here
├── CODEBASE.md                         ← generated/updated here
├── DECISIONS.md                        ← updated (spec/scope)
├── IMPLEMENTATION_LOG.md               ← appended (implementation decisions)
└── features/
    └── [YYYY-MM-DD]-[feature-slug]/
        ├── FEATURE_SPEC.md
        ├── FEATURE_PLAN.md
        └── FEATURE_TASKS.md
CLAUDE.md                               ← project root, updated
```

**Slug rule:** kebab-case, first 4-5 meaningful words, stop words removed. Date = today.
Examples: `2026-03-20-reading-sessions` · `2026-03-20-dark-mode` · `2026-03-20-push-notifications`

---

## Step 1 — Check for existing feature and read codebase

**Check for existing feature with same or similar name:**
Scan `vibe/features/` for folders matching the requested feature.
If an incomplete feature folder exists:
> "Found an existing [feature] folder: vibe/features/[date-slug]/
> Resume that feature or start fresh with a new folder?"
Wait for answer before proceeding.

**Read vibe/CODEBASE.md (or generate it):**

If vibe/CODEBASE.md exists:
Read it fully. Verify accuracy. If significantly out of date, refresh relevant sections.
Add changelog line: `> 📝 [date] · Verified during [feature-name] planning`

If vibe/CODEBASE.md does not exist:
- **If there is NO `vibe/` folder at all** (an existing repo never onboarded):
  recommend `vibe-init` first — it generates the full vibe/ set (ARCHITECTURE.md,
  SPEC.md, DECISIONS.md, TASKS.md, CLAUDE.md, …) so this feature builds on real parity, not
  a lone improvised CODEBASE.md. Offer: "This repo isn't set up for vibe yet — run
  `vibe-init` first (recommended), or I can generate just CODEBASE.md and proceed?"
- If the user declines init (or only CODEBASE.md is missing): read
  `references/CODEBASE_MD.md` for the generation template, explore the codebase
  (folder structure, package.json, patterns, DB schema, routes), and generate
  `vibe/CODEBASE.md`.

**Read vibe/ARCHITECTURE.md** if it exists — conventions must be followed throughout.

Confirm:
> "Codebase read. [Generated fresh / Verified existing] CODEBASE.md.
>  [Stack] project. Feature to add: [feature].
>  Proposed folder: vibe/features/[date-slug]/
>  Any questions before I draft the spec?"

---

## Step 2 — Read feature map and check dependencies

Before drafting FEATURE_SPEC.md, read:
- `vibe/SPEC.md` — existing features, acceptance criteria, out-of-scope items, data model
- `vibe/SPEC_INDEX.md` — for quick orientation to feature relationships
- `vibe/PLAN.md` Section 6 (Feature Map) — sequencing, dependencies, shared data

**Feature map check — run before drafting:**

Find this feature in PLAN.md Section 6 and extract:

```python
feature_entry = plan_md.find_feature(requested_feature_name)

checks = {
    "dependencies_met":    all deps marked ✅ in TASKS.md,
    "shared_data_reads":   entities this feature reads from other features,
    "shared_data_writes":  entities this feature creates for other features,
    "parallel_candidates": features that can run simultaneously with this one,
    "depended_on_by":      features that cannot start until this one is done,
    "build_order":         expected position in the Phase 2 sequence
}
```

**If dependencies are NOT met — stop and surface clearly:**
> "⚠️ [Feature name] depends on [Feature X] which is not yet complete.
>
> [Feature X] must be built first because: [reason from PLAN.md]
> [Feature X] current status: [⬜ not started / 🔄 in progress]
>
> Options:
> (a) Build [Feature X] first — run `feature: [Feature X name]`
> (b) Proceed anyway — I'll flag all the missing data model pieces
>
> Which do you prefer?"
>
> Wait for answer. If (b) — note all missing dependencies in FEATURE_SPEC.md
> under a "Missing dependencies" section so the agent knows what to stub.

**If this feature creates data used by others — note it explicitly:**
> "This feature creates [Entity] which [Feature Y] and [Feature Z] will later consume.
> I'll make the schema decisions in this spec. Those features will reference back to it."

**If this feature can run in parallel with another — note it:**
> "[Feature N] can run in parallel with this one — no shared writes.
> If you want to build both simultaneously, say `parallel:` after both feature kits are ready."

**If this feature is NOT in PLAN.md — flag it:**
> "This feature wasn't in the original plan. This is fine — run `change:` first
> to assess impact on the data model and phase sequencing before I draft the spec.
> Or I can proceed and we treat it as an unplanned addition."

This ensures every feature spec:
- Is aware of what data already exists from earlier features
- Doesn't redefine entities that should come from a dependency
- Doesn't assume data model fields that haven't been built yet
- Integration points reference the correct existing spec sections
- Conformance checklist complements rather than duplicates the main conformance checklist

---

## Step 3 — Generate FEATURE_SPEC.md

Draft FEATURE_SPEC.md covering:
1. **Feature overview** — What it does and why (2-3 sentences)
2. **User stories** — Who does what, outcome
3. **Acceptance criteria** — Concrete, testable conditions for done
4. **Scope boundaries** — Included and explicitly deferred
5. **Integration points** — Exact files, routes, DB tables (use CODEBASE.md section 9)
   Reference relevant SPEC.md sections by anchor (e.g. SPEC.md#data-model)
6. **New data model changes** — Tables, fields, relationships
7. **New API endpoints** — Method, path, request/response (if applicable)
8. **Edge cases and error states** — What can go wrong
9. **Non-functional requirements** — Performance, security, mobile
10. **Conformance checklist** — What must be true for this feature to be shippable

Present. Ask: "Does this spec look right? Anything to change?"
Wait for approval. Save as `vibe/features/[date-slug]/FEATURE_SPEC.md`.

---

## Step 4 — UI check (graduated — not binary)

Ask:
> "How much UI work does this feature involve?
> (a) New screens or significant new components → full wireframe
> (b) Minor additions to existing screens → brief UI note in spec
> (c) No UI — purely logic, data, or backend → skip"

**(c)** → skip to Step 6.
**(b)** → add a brief UI note to FEATURE_SPEC.md, skip to Step 6.
**(a)** → **design-gate check first:** if the project has **no** design system yet
(`DESIGN.md` / `vibe/DESIGN_SYSTEM.md` / `vibe/design/CONTRACT.md` all absent),
this feature would invent a look from scratch — the "skipped design" failure.
Offer to establish it before building:
> "No design language exists yet. Run `design:` first (optionally `design-md:` to
>  lock brand tokens) so this and future screens are consistent? Recommended.
>  Reply 'skip design' to build this feature's UI ad hoc."
Invoke `design:` on yes; log the skip in DECISIONS.md if declined. Then continue
to Step 5. If a design system already exists, go straight to Step 5.

---

## Step 5 — UI Design (only for significant UI work)

**Requires: frontend-design skill.** Reference existing design system from
(in precedence order — `DESIGN.md` wins where they conflict):
- `DESIGN.md` (project root) if it exists — the brand token contract from
  `design-md:`. **Authoritative** for colours/type/spacing.
- `vibe/design/CONTRACT.md` if it exists — the per-project design contract from
  `design:`. New UI must obey it.
- `vibe/DESIGN_SYSTEM.md` if it exists (existing tokens — must be consistent).
- CODEBASE.md sections 2 and 6 (stack, patterns).

Ask all at once:
1. New screens or views being added? Existing screens being modified?
2. Main user interaction?
3. Layout preference? (modal, drawer, full page, inline)
4. Device? (mobile, desktop, both)
5. Anything complex? (multi-step, real-time, drag-drop)
6. UI references for inspiration?
7. Existing patterns to match? (from CODEBASE.md section 6 and DESIGN_SYSTEM.md)

Generate wireframe — must feel like it belongs in the existing product.
Present. Iterate until approved. Append UI Specification to FEATURE_SPEC.md.

---

## Step 6 — Generate FEATURE_PLAN.md

Read FEATURE_SPEC.md, CODEBASE.md, ARCHITECTURE.md, vibe/SPEC.md (integration sections).
Read integration point files directly before drafting.

Draft FEATURE_PLAN.md:
1. **Impact map** — Files to modify vs new files (exact paths from CODEBASE.md section 9)
2. **Files explicitly out of scope** — Must not be touched
3. **DB migration plan** — Exact schema changes
4. **Backend changes** — Routes, controllers, services with file paths
5. **Frontend changes** — Components, pages, hooks with file paths
6. **Conventions to follow** — Paste relevant patterns from CODEBASE.md section 6
7. **Task breakdown**: Data layer → Backend → Frontend (skip if no UI) → Tests
8. **Rollback plan** — How to undo this feature
9. **Testing strategy** — New tests, existing tests needing updates
10. **CODEBASE.md sections to update** — Which sections change as tasks complete

Present. Wait for approval. Save as `vibe/features/[date-slug]/FEATURE_PLAN.md`.

---

## Step 7 — Update CLAUDE.md (project root)

Read existing CLAUDE.md. Append feature section — do NOT overwrite:

```
---
### Active Feature: [Feature Name]
> Folder: vibe/features/[date-slug]/ | Added: [date]

**Feature summary**: [1-line]
**Files in scope**: [exact list from FEATURE_PLAN.md]
**Files out of scope**: [explicit list]
**Design system**: [Check vibe/DESIGN_SYSTEM.md for existing tokens before any styling]

**Conventions** (from vibe/CODEBASE.md section 6 + vibe/ARCHITECTURE.md):
[Reproduce directly relevant patterns]

**Scope changes**: If user says "change:" — stop and run vibe-change-spec immediately.

**Boundaries:**
Always: follow ARCHITECTURE.md patterns · run existing tests after every change ·
        keep changes additive · update CODEBASE.md for new files/routes/schema ·
        update TASKS.md after every task in plain English ·
        check DESIGN_SYSTEM.md before any styling work

Ask first: modifying existing API response shapes · touching auth ·
           changing shared components · any non-additive DB schema change
Never: change behaviour of existing features · remove/rename DB fields ·
       modify existing passing tests · touch files not in FEATURE_PLAN.md

**Session startup:**
1. Read CLAUDE.md · 2. Read vibe/CODEBASE.md · 3. Read vibe/ARCHITECTURE.md
4. Read vibe/DESIGN_SYSTEM.md if exists · 5. Read vibe/SPEC_INDEX.md
6. Read vibe/TASKS.md · 7. Read FEATURE_TASKS.md
8. Confirm task before writing any code

**Between tasks:** "next" triggers this exact sequence — no deviations:
1. Run tests: `npm test 2>&1 | tail -20` (or project test command)
2. Run lint: `npm run lint --silent 2>&1 | tail -10`
3. Stage and commit code changes:
   ```
   git add -A
   git commit -m "feat([feature-slug]): [TASK-ID] — [one line plain English]"
   ```
4. If this task made a MEANINGFUL implementation decision (hard to reverse · picked among
   real alternatives — library/pattern/data-model/API shape · would surprise a future
   reader · deviates from ARCHITECTURE.md), append an entry to vibe/IMPLEMENTATION_LOG.md
   per that file's header schema (newest last; `Touches:` = files/functions changed). This
   promotes the task's `Decisions:` note into the durable, graph-linked project log. Skip
   routine work — no noise.
5. Stage and commit doc updates separately:
   ```
   git add vibe/features/[date-slug]/FEATURE_TASKS.md vibe/TASKS.md vibe/DECISIONS.md vibe/IMPLEMENTATION_LOG.md vibe/CODEBASE.md
   git commit -m "docs(FEATURE_TASKS+TASKS): mark [TASK-ID] done — [feature]"
   ```
6. Re-read TASKS.md silently → state next task in plain English → confirm.

Do NOT request new session unless 10+ tasks this session.
Do NOT skip the commit step — uncommitted work is invisible to vibe-graph and vibe-review.

**Session completion:** Follow main checklist in CLAUDE.md.
All tasks committed individually during the session — no large end-of-session commit needed.
---
```

**CLAUDE.md cleanup rule:**
When this feature is complete and its phase review passes, archive or remove this section.
If all its rules are now in ARCHITECTURE.md, remove the section entirely.
CLAUDE.md must stay under ~150 lines excluding archived sections.

Save updated `CLAUDE.md`.

---

## Step 8 — Generate FEATURE_TASKS.md

Read FEATURE_SPEC.md, FEATURE_PLAN.md, CODEBASE.md, ARCHITECTURE.md.

Add effort estimate at the top:
```
> **Estimated effort:** [N tasks — S: X (<2hrs), M: Y (2-4hrs), L: Z (4+hrs) — approx. [N] hours total]
```

Every task uses this structure:

```
---
### [TASK-ID] · [Task title]
- **Status**: `[ ]`
- **Size**: [S / M / L]
- **Spec ref**: FEATURE_SPEC.md#[section]
- **Dependencies**: [task IDs or "None"]
- **Touches**: [exact file paths from CODEBASE.md section 9]

**What to do**: [Specific instructions — precise enough for fresh context to execute]

**Acceptance criteria**:
- [ ] [Checkable condition from FEATURE_SPEC.md]

**Self-verify**: Re-read FEATURE_SPEC.md#[section]. Tick every criterion.
**Test requirement**: [What test must exist and what it verifies]
**⚠️ Boundaries**: [Relevant Ask first / Never rules for this specific task]
**CODEBASE.md update?**: [Yes — describe / No — logic only]
**Architecture compliance**: [Which ARCHITECTURE.md patterns apply to this task]

**Decisions**:
> Filled in by agent after completing.
- None yet.
---
```

Phases: Data layer → Backend → Frontend (skip if no UI) → Tests

End with Feature Conformance Checklist:
```
---
#### Conformance: [Feature Name]
> Tick after every task. All items ✅ before feature is shippable.
- [ ] [Acceptance criterion verbatim from FEATURE_SPEC.md]
- [ ] All new tests pass
- [ ] All existing tests still pass
- [ ] Linter clean
- [ ] No regressions in related features
- [ ] CODEBASE.md updated for structural changes this feature introduced
- [ ] ARCHITECTURE.md updated if new patterns were established
- [ ] DESIGN_SYSTEM.md updated if design: added new tokens for this feature
---
```

Save as `vibe/features/[date-slug]/FEATURE_TASKS.md`.

---

## Step 9 — Update vibe/TASKS.md

Read current TASKS.md. Two changes:

**1. Expand feature inline in Phase 2:**

Replace flat slug line `⬜ [Feature Name] — [description]` with:
```
🔄 [Feature Name] — [what this lets users do] (0/N)
   Estimated: approx. [N] hours (S: X, M: Y, L: Z)
   [ ] [TASK-ID] · [task name] — [one plain English line]
   [ ] [TASK-ID] · [task name] — [one plain English line]
   ...
   → Full specs: vibe/features/[date-slug]/FEATURE_TASKS.md (agent use)
```

**2. Update "What just happened" and "What's next" after each task:**
```
## What just happened
✅ [TASK-ID] · [Task name in plain English] — complete
   Est. cost: ~$[X.XX] · Session running total: ~$[X.XX]
   Committed: feat([feature-slug]): [TASK-ID] — [description]

## What's next
⬜ [TASK-ID] · [Plain English next task]
   [One sentence: what the user will see when done]
Say "next" to begin.
```

**Cost estimate per task (Mode A — automatic):**
Read task size from FEATURE_TASKS.md (S / M / L). Rough estimate at
`claude-sonnet-5` pricing (source of truth: vibe-cost/references/PRICING.md —
scale for other tiers, and expect lower with prompt caching):
- S task: ~$0.03-0.07
- M task: ~$0.08-0.15
- L task: ~$0.18-0.35

Running session total = sum of all tasks completed this session.
These are estimates. User can run `cost:` for precise numbers from `/cost` output.

After each task: mark [x], update count, update What just happened + What's next.
Feature complete: collapse to `✅ [Feature Name] — [summary] (N/N ✅)`

---

## Step 10 — Update vibe/DECISIONS.md

```
---
## — Feature Start: [Feature Name] — [date]
> Folder: vibe/features/[date-slug]/
> [One line description]
> Tasks: [list all IDs] | Estimated: [N hours]
> Drift logged below.
---
```

## Step 10B — Update PLAN.md feature map

Mark this feature as planned in PLAN.md Section 6:

Find the feature entry and update its status line:
```
⬜ [Feature name] → 🔄 [Feature name] — spec in vibe/features/[date-slug]/
```

If the feature was NOT in PLAN.md — add it with a note:
```
#### [Feature name] — [one sentence] ← UNPLANNED ADDITION
> Added: [date] · See DECISIONS.md D-[ID] for context
> Build order: [N] · Depends on: [what was determined in Step 2]
> Shared data: [what it reads, what it creates]
```

This keeps PLAN.md as the live source of truth for what's been planned
vs what's been built, across all phases.

## Step 11 — Spec review gate

Announce to the user:
> "FEATURE_SPEC.md written. Running spec-review before feature build..."

Invoke `vibe-spec-review` with:
- Trigger source: `add-feature`
- Scope: FEATURE_SPEC.md + vibe/SPEC.md (contradiction check)

After spec-review completes:

Tell the user:

---
> ✅ **Feature kit ready.**
>
> **Created:** vibe/features/[date-slug]/
>   FEATURE_SPEC.md · FEATURE_PLAN.md · FEATURE_TASKS.md
> **Updated:** vibe/TASKS.md · CLAUDE.md · vibe/CODEBASE.md · vibe/DECISIONS.md
> **Estimated:** [N tasks — approx. [N] hours]
> **Spec review:** [✅ clean / ⚠️ [N] warnings acknowledged / 🔴 [N] P0s fixed]

**Plan-only (`feature: [name] plan-only`).** The autonomous phase loop plans a batch of
independent features first and then builds them together through vibe-parallel (Entry
point E). When called with `plan-only`, stop here: report the feature as planned and
return to the caller. Do not build, and skip Step 14 — the caller runs the phase gate.

**Read execution mode:**
```bash
grep "VIBE_MODE" CLAUDE.md 2>/dev/null | cut -d= -f2 | tr -d ' '
```

If `autonomous` → read the vibe-mode skill's `references/AUTONOMOUS_EXECUTION_BLOCK.md`
(resolve the vibe-mode install dir — commonly `~/.claude/skills/vibe-mode/`, or
`~/.claude/plugins/marketplaces/*/skills/vibe-mode/` under a plugin install)
and follow the autonomous execution protocol. Begin immediately.

If `manual` or not set → tell the user:
> Tell your coding agent:
> ```
> Read CLAUDE.md, vibe/CODEBASE.md, vibe/ARCHITECTURE.md,
> vibe/SPEC_INDEX.md, vibe/TASKS.md, then FEATURE_TASKS.md.
> Confirm the first task before writing any code.
> ```
> Say **"next"** after each task.
---

## Step 12 — Update dependency graph

After the feature is built and tasks are complete, invoke `vibe-graph: update`.

The graph reads `git diff --name-only HEAD` to detect exactly which files
changed this session. Only those nodes are re-indexed. Planned nodes for
this feature transition to `built`. Concept completion percentage updates.

This step runs automatically — no user input needed.
Takes 1-2 minutes on a typical feature. Updates DEPENDENCY_GRAPH.json,
CONCEPT_GRAPH.json, and graph.html for the affected subgraph only.

---

## Step 13 — Blast-radius test coverage

Invoke `vibe-test` (the `test:` skill) on the files this feature touched. The
inline `npm test` in Step 7 only *runs* the existing suite — this step
*generates or extends* coverage across the feature's blast radius (the changed
files plus their dependents / contract consumers), which is what vibe-test
advertises as its auto-handoff from vibe-add-feature.

- In `VIBE_MODE=autonomous`: run it automatically after the graph update.
- In `VIBE_MODE=manual`: offer it —
  > "Feature built. Generate blast-radius tests for the [N] files it touched? (y/n)"

vibe-test reads the `Touches` sections of this feature's `FEATURE_TASKS.md`
(and the graph, if present) to scope coverage. Skip only if the user declines.

---

## Step 14 — Phase gate check

If this feature was the **last task of a phase**, the phase review gate runs now —
run `review: phase N` (autonomous: automatically; manual: announce and run). Do not
drift into the next phase's features first. The gate is enforced by the CLAUDE.md
advancement rule + `vibe/.gates.json` (see `vibe-review/references/GATES.md`): the
next phase cannot start until `phases["N"].review` is `passed`. If the feature is
mid-phase, just continue.
