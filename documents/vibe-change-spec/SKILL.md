---
name: vibe-change-spec
description: >
  Scope change workflow for modifying, adding, or removing requirements at any point during a build.
  Triggers on "change:" prefix, "I forgot to add", "actually I also want", "can we add",
  "remove X from scope", "I changed my mind about", "before we continue add",
  "one more thing", "I want to change the spec", "revert the X change".
  Handles new additions, removals, renames, backlog operations, and reverting previous changes.
  Assesses impact before touching any file. Updates all affected docs in the correct order.
  If BRIEF.md doesn't exist, updates SPEC.md and DECISIONS.md only.
---

# Vibe Change Spec Skill

Handles scope changes at any point during the build — safely, in the right order.
Always assesses impact first. Always waits for confirmation. Never edits files speculatively.

**Always run in Plan Mode (Shift+Tab). Do not write any code in this skill.**

> **Autonomous / headless mode.** At startup resolve the settings with
> `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode`. If `vibe_mode` is
> `autonomous`, every "wait", "ask", "confirm" and approval step in this skill follows
> vibe-mode's `references/HEADLESS.md` §2 instead: take the recommended option, accept your
> own draft after one self-check, log each choice to `vibe/DECISIONS.md`, never ask the
> user, and stop — writing `vibe/.run_state.json` — only when a person is genuinely required.

---

## The O'Reilly principle this enforces

**Drift prevention** — scope changes must be logged explicitly. An informal "just quickly add X"
mid-task produces a codebase that doesn't match its documentation. When review: runs,
it finds violations with no logged context. change: prevents this by stopping work,
assessing impact, and updating all affected documents before building continues.

---

## When this skill runs

Any time the user signals a scope change:
- `change: add dark mode before we build screens`
- `change: remove social login — email only`
- `change: add push notifications to backlog`
- `change: promote push notifications to active`
- `change: rename "ideas" to "posts" throughout`
- `change: revert the PDF attachment change we made last week`
- Natural language: "actually I also want X", "I forgot Y", "can we cut Z"

---

## Step 1 — Understand the change

Extract:
- What is being added, removed, modified, renamed, or reverted
- Whether it's a new feature, requirement tweak, removal, rename, backlog op, or revert
- Whether it's urgent (insert now) or deferred (backlog)

If ambiguous, ask the clarifying questions you actually need — batched together,
not one at a time.

Confirm:
> "Got it — you want to [add/remove/modify/revert] [X]. Let me check what this affects."

---

## Step 2 — Read current state

Read in order. Skip files that don't exist — note their absence:

1. `BRIEF.md` *(if exists)* — original problem, core value, v1 feature set
2. `vibe/ARCHITECTURE.md` *(if exists)* — established patterns and principles
3. `vibe/SPEC.md` — what is currently in scope
4. `vibe/SPEC_INDEX.md` — feature list and state
5. `vibe/TASKS.md` — active work, done vs pending
6. `vibe/PLAN.md` — current architecture
7. `vibe/CODEBASE.md` — what has actually been built

If active feature or bug folder exists (from TASKS.md active block):
8. Active `FEATURE_TASKS.md` or `BUG_TASKS.md`

---

## Step 3 — Assess impact

### Build stage

**Before any code** — doc updates only. Zero retrofit.
**Between tasks** — last task done, next not started. New tasks slot cleanly.
**Mid-phase** — some tasks done. May need to pause and insert new tasks.
**Cross-phase** — change affects already-built architecture or data layer. Retrofit needed.
**Post-completion** — fully built and conformance-checked. Full retrofit + regression strategy.

### Impact checklist

- [ ] Adds/removes feature from SPEC.md?
- [ ] Changes data model (table, field, relationship)?
- [ ] Changes any API endpoints already built?
- [ ] Affects screens or components already built?
- [ ] Changes architecture in PLAN.md?
- [ ] Changes patterns or conventions in ARCHITECTURE.md?
- [ ] Changes core value or feature set in BRIEF.md?
- [ ] Do tasks already marked [x] need retrofitting?
- [ ] Affects active feature/bug folder?
- [ ] Is this additive (now) or deferred (backlog)?

### Feature map cascade check

If vibe/PLAN.md exists and has a Section 6 feature map — run this check:

Find the affected feature in the feature map.

Extract:
- `depended_on_by` — features that cannot start until this one is done
- `shared_data` — entities this feature creates that others consume
- `parallel_candidates` — features planned to run alongside this one

For each feature in `depended_on_by`:
- Is it already built? → retrofit risk, flag as cross-phase
- Is it planned but not built? → update its spec deps before it starts
- Is it in progress? → pause it, assess data model impact first

For each `shared_data` entity this change affects:
- Which downstream features read this entity?
- Does the change alter the entity schema? → all consumers need review
- Does the change remove the entity? → all consumers are now broken

Surface cascade clearly in Step 4:
```
Feature map cascade:
  ⚠️  [Feature X] depends on [changed feature] — [built/in progress/planned]
      Impact: [what breaks or needs updating]
  ⚠️  [Feature Y] reads [affected entity] — [built/in progress/planned]
      Impact: [schema change affects Y's data layer]
  ✅  [Feature Z] — no dependency on changed feature
```

If no feature map in PLAN.md — skip this check, note its absence.

### Revert detection

If the change is reverting a previous scope change (e.g. "remove the PDF feature we added"):
- Find the original D-ID in DECISIONS.md
- Identify all tasks that were added or retrofitted at that time
- Assess which tasks have been completed since (those need retrofit to undo)
- Treat as a new scope change entry (not a deletion of the original D-ID)
- Run the feature map cascade check for the reverted feature too

---

## Step 4 — Tell the user impact before touching anything

> **Change requested:** [one sentence plain English]
>
> **Build stage:** [Before code / Between tasks / Mid-phase / Cross-phase / Post-completion]
>
> **What this affects:**
> - Spec: [what changes in plain English]
> - Tasks: [N new / M retrofit / K removed — plain English]
> - Code already built: [affected — what needs revisiting / not affected]
> - Architecture: [patterns affected / not affected]
>
> **Feature map cascade:** [None / see cascade findings above]
> - [Feature X] — [built/planned] — [impact]
> - [Feature Y] — [built/planned] — [impact]
>
> **Effort:** [Small — doc only / Medium — new tasks / Large — retrofit needed]
>
> **Recommendation:** [Add to backlog / Insert before next task / Address now with retrofit]
>
> Ready to proceed? (or "add to backlog instead")

Wait for confirmation. Never touch files before confirmation.

- "add to backlog" → jump to Step 11 (Backlog)
- "proceed" → continue to Step 5

---

## Step 5 — Update vibe/SPEC.md + vibe/SPEC_INDEX.md

Always updated together — never one without the other.

**Adding a feature:** Add section with acceptance criteria. Add update note at top:
```
> ⚠️ Last updated: [date] · Scope addition: [what] · Build stage: [stage]
```

**Removing a feature:** Strikethrough — never delete:
```
~~## Feature: [Name]~~
> ⚠️ Removed: [date] · Reason: [why] · See DECISIONS.md D-[ID]
```

**Modifying:** Edit in-place, mark what changed:
```
> ~~Original: [old]~~
> Changed [date]: [new] — [reason]
```

**SPEC_INDEX.md update:** Update relevant entry. Update sync date.

Save both.

---

## Step 6 — Update BRIEF.md *(if exists)*

If BRIEF.md doesn't exist — skip this step, note it in the user's summary.

BRIEF.md must reflect current reality — not the original idea.

**Feature added/removed:** Update v1 feature set table.
**Core value changed:** Update core value section with change and reason.
**Stack changed:** Update tech stack table.
**Always append:**
```
- Scope change [date]: [what changed and why — one line]
```

Save updated `BRIEF.md`.

---

## Step 7 — Update vibe/ARCHITECTURE.md *(if affected)*

Only if change affects: patterns, conventions, folder structure, state management,
API design, testing philosophy, or tech decisions.

Add new pattern or update changed decision. Always add changelog line if updated:
```
> 📝 [date] · Scope change D-[ID] — [what changed architecturally]
```

Skip and state explicitly if no architecture impact.

---

## Step 8 — Update vibe/PLAN.md *(if affected)*

Only if change affects: data model, API shape, architecture layers, or phase structure.

Add changelog line at top. Update relevant sections in-place.
Skip and state explicitly if no impact.

---

## Step 9 — Update vibe/TASKS.md

All TASKS.md updates in plain English. Task IDs stay for agent sequencing.

**Adding new tasks** — expand inline feature block, insert in correct sequence.
**Adding retrofit tasks** — add HM-001-R style entries inline with plain English.
**Removing tasks** — strikethrough inline with plain English reason.
**Reverting** — add retrofit tasks for any completed work that needs undoing.

Always update "What just happened" and "What's next":
```
## What just happened
🔄 Scope change: [plain English — what changed and why]
   [N new tasks / M retrofits / K removed]

## What's next
⬜ [TASK-ID] · [plain English next task]
Say "next" to continue.
```

---

## Step 10 — Update vibe/DECISIONS.md

```
---
### D-[ID] — [Short title]
- **Date**: [date] · **Type**: scope-change
- **Trigger**: change: command — user-initiated
- **Build stage**: [stage]
- **What changed**: [exact description]
- **Why**: [user's stated reason]
- **Before**: [original scope]
- **After**: [new scope]
- **Tasks affected**: New: [IDs] · Retrofit: [IDs] · Removed: [IDs]
- **Folders affected**: [feature/bug folders or "none"]
- **Architecture impact**: [Yes — what / None]
- **BRIEF.md updated**: [Yes / No — didn't exist]
- **Approved by**: human
---
```

---

## Step 11 — Update vibe/CODEBASE.md *(only if change affects built structure)*

Update only if: the change removes/renames something built, or establishes a new pattern.
Skip and state explicitly if no update needed.

---

## Step 12 — Backlog (add now, build later)

Add to `vibe/backlog/[YYYY-MM-DD]-[feature-slug].md`:

```
# [Feature Name]
> Added: [date] | Status: deferred

## What
[Description]

## Why deferred
[Reason]

## Effort estimate
[Small / Medium / Large]

## Dependencies
[What must be done before this]

## Promote when
[Condition]

## Promote with
change: promote [feature-name] to active
```

Update SPEC.md Backlog section, SPEC_INDEX.md, and TASKS.md backlog section.

### Promoting a backlog item

When user says `change: promote [item] to active`:
1. Read vibe/backlog/[date-slug].md
2. Run vibe-add-feature to generate the full feature kit
   (tell user: "Running feature: to build the full spec and task list for this")
3. Update SPEC.md — move from backlog to active features
4. Update SPEC_INDEX.md
5. Mark backlog file as promoted (or delete it)
6. Log in DECISIONS.md as scope-change

---

## Step 13 — Commit docs

```bash
# SPEC always — always paired:
git add vibe/SPEC.md vibe/SPEC_INDEX.md
git commit -m "docs(SPEC): [add/remove/modify] [what] — D-[ID]"

# TASKS + DECISIONS always:
git add vibe/TASKS.md vibe/DECISIONS.md
git commit -m "docs(TASKS+DECISIONS): scope change D-[ID] — [N new, M retrofit, K removed]"

# BRIEF.md if exists and changed:
git add BRIEF.md
git commit -m "docs(BRIEF): scope change D-[ID] — [what changed]"

# ARCHITECTURE.md if changed:
git add vibe/ARCHITECTURE.md
git commit -m "docs(ARCHITECTURE): [what changed] — D-[ID]"

# PLAN.md if changed:
git add vibe/PLAN.md
git commit -m "docs(PLAN): [what changed] — D-[ID]"

# Active feature/bug folder if changed:
git add vibe/features/[date-slug]/FEATURE_TASKS.md
git commit -m "docs(FEATURE_TASKS): scope change D-[ID] — [feature]"

# CODEBASE.md if changed:
git add vibe/CODEBASE.md
git commit -m "docs(CODEBASE): [what changed] — D-[ID]"

# Backlog if created:
git add vibe/backlog/[date-slug].md
git commit -m "docs(BACKLOG): add [feature-name] — deferred [date]"
```

---

## Step 14 — Hand off to user

```
✅ Scope change complete.

**What changed:** [plain English — one or two sentences]
**Your task list is updated** — open vibe/TASKS.md to see the new sequence.
**Next task:** [plain English]

Say "next" to continue building.
```

No session phrases. No file paths. Human readable only.

---

## Quick reference — change types and files touched

| Change type | BRIEF | ARCH | SPEC | PLAN | TASKS | CODEBASE | DECISIONS |
|-------------|-------|------|------|------|-------|----------|-----------|
| Add feature (pre-build) | ✅ if exists | maybe | ✅ | maybe | ✅ new | ⏭ | ✅ |
| Add feature (mid-build) | ✅ if exists | maybe | ✅ | maybe | ✅ +retrofit | ⏭ | ✅ |
| Remove feature (unbuilt) | ✅ if exists | maybe | ✅ strike | maybe | ✅ remove | ⏭ | ✅ |
| Remove feature (built) | ✅ if exists | maybe | ✅ strike | maybe | ✅ retrofit | ✅ | ✅ |
| Revert scope change | ✅ if exists | maybe | ✅ | maybe | ✅ +retrofit | maybe | ✅ |
| Add to backlog | ✅ if exists | ⏭ | ✅ | ⏭ | ✅ backlog | ⏭ | ✅ |
| Promote backlog item | ✅ if exists | maybe | ✅ | maybe | ✅ schedule | ⏭ | ✅ |
| Rename concept | ✅ if exists | maybe | ✅ | maybe | ✅ refs | ✅ if built | ✅ |
| Change tech/pattern | ✅ if exists | ✅ | maybe | ✅ | maybe | ✅ if built | ✅ |
