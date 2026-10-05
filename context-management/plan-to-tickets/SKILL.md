---
name: plan-to-tickets
category: meta-orchestration
description: Break a spec, plan, or the current conversation into a local, numbered, spec-kit-style task list of tracer-bullet vertical slices with explicit dependencies. Use when a spec or plan is ready to become actionable tasks. Pushing to Jira is opt-in, only on request.
disable-model-invocation: true
codex-short-description: "Break a plan into a local numbered task list"
compatibility: claude-code codex opencode
---

# Plan to Tickets

Break a spec, plan, or conversation into **tasks** — **tracer-bullet** vertical slices, each declaring the tasks that **block** it — and stage them as a **local, numbered task list** (spec-kit style). Jira is an opt-in downstream target, never the default.

**Local-first.** Tasks are written to a local `tasks.md` you control. Nothing is created in Jira (or any remote) without the user explicitly asking, and never without confirming first. The local `tasks.md` is the source of truth; Jira tickets are a downstream projection of it.

## Process

### 1. Resolve the staging location

Tasks live beside their spec, spec-kit style:

```text
<staging>/NNN-<feature-slug>/spec.md      (from /plan-to-spec, if any)
<staging>/NNN-<feature-slug>/tasks.md     (this skill writes here)
```

Resolve `<staging>` in this order:

1. If the source is a `/plan-to-spec` folder, write `tasks.md` beside its `spec.md`.
2. A path the user passed as an argument this run.
3. The memory default `reference_plan_staging_dir.md`, if it exists.
4. Otherwise **ask** where to stage (offer `./specs/` or `.plans/`). Offer to record the answer to `reference_plan_staging_dir.md` — only with consent.

State the resolved path before writing.

### 2. Gather context

Work from the conversation. If the user passes a reference (a staged `spec.md`, a Confluence URL, a Jira key), fetch its full body and read it.

### 3. Explore the codebase (optional)

If you haven't already, explore to understand the current code. Task titles use the project's domain vocabulary and respect ADRs in the area. Look for **prefactoring** — "make the change easy, then make the easy change."

### 4. Draft vertical slices

Break the work into **tracer-bullet** tasks:

- Each slice cuts a narrow but **complete** path through every layer (schema, API, UI, tests) — vertical, not a horizontal slice of one layer.
- A completed slice is demoable or verifiable on its own.
- Each slice fits in a single fresh context window.
- Prefactoring goes first.

**Test each slice with one question: what can I demo when this is done?** A task with no answer is a horizontal slice wearing a vertical name — "all the schema", "wire up the API" — and it's the failure this rule exists to prevent. Put the answer in the task as a *demo path* line.

**Acceptance criteria must be able to fail.** For each criterion, name the observation that would show it false, and confirm it is false at the commit the implementer starts from. Three shapes recur and all three grade nothing: a criterion already true at the base commit, one that only another task's work can satisfy, and one that restates the request instead of deriving from the artifact.

**Resist over-decomposition.** The default pull is toward atomic units, and twelve tickets for a three-line change is the common result. There is a floor: if the whole change fits in one fresh context window, it doesn't need slicing at all — say so and send the user straight to `implement`.

Give each task its **blocking edges** — the tasks that must finish before it can start. A task with no blockers can start immediately, and independent tasks are marked `[P]` (parallelizable).

**Wide refactors are the exception.** A **wide refactor** — one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the codebase — can't land green as a single vertical slice. Sequence it **expand–contract**: *expand* (add the new form beside the old, nothing breaks), *migrate* the call sites in batches sized by blast radius (per package/dir), each batch a task blocked by the expand and green because the old form still exists, then *contract* (delete the old form) in a task blocked by every migrate batch.

### 5. Quiz the user

Present the breakdown as a numbered list. Per task: **ID + Title**, **Blocked by**, **What it delivers** (the end-to-end behaviour). Ask:

- Does the granularity feel right (too coarse / too fine)?
- Are the blocking edges correct — does each task depend only on tasks that genuinely gate it?
- Should any be merged or split?

Iterate until approved. **Do not write anything before approval.**

### 6. Write the local task list

Write the approved tasks to `<staging>/NNN-<feature-slug>/tasks.md` using the template below. Tasks are numbered `T001`, `T002`, … in dependency order (blockers first). This is where the skill **stops by default** — the tasks are staged, ready for `/implement` to work one at a time.

<tasks-template>

# <Feature name> — Tasks

Spec: [spec.md](spec.md)  ·  Source: <spec / plan / conversation>

Legend: `[P]` = parallelizable (no incomplete blockers). Work the **frontier** — any unchecked task whose blockers are all done.

## Tasks

- [ ] **T001** — <title>  ·  Blocked by: none `[P]`
  - What it delivers: <end-to-end behaviour, user's perspective>
  - Acceptance:
    - [ ] Criterion 1
    - [ ] Criterion 2
- [ ] **T002** — <title>  ·  Blocked by: T001
  - What it delivers: …
  - Acceptance:
    - [ ] Criterion 1

## Jira mapping

<!-- filled in only if pushed to Jira (step 7): T001 -> PRJ-1490, ... -->

</tasks-template>

Avoid file paths and code snippets — they go stale. Exception: a prototype snippet encoding a decision more precisely than prose (state machine, reducer, schema, type shape) — inline the decision-rich parts, note it came from a prototype.

### 7. Push to Jira — only if asked

If — and only if — the user asks to push, confirm the destination first (read the project key from `reference_jira_default_project.md`; confirm project + issue type), then create one issue per task in **dependency order** (blockers first) so blocking edges reference real keys:

1. `jira_create_issue` — `summary` = task title, `description` = the task's What-it-delivers + acceptance criteria.
2. After both endpoints of an edge exist, wire it with `jira_link_issues` using the **"Blocks"** link type (blocker = inward, blocked = outward). Confirm the exact link-type name once via `jira_get_issue_link_types` — it varies per instance.
3. If the source was a Jira ticket, link each new issue to it as the parent (don't modify the parent).

Write the `T00N -> KEY` mapping back into the local `tasks.md` **Jira mapping** section so local and remote stay reconciled. Report the created keys and the frontier.

## Rules

- **Local-first, always.** The numbered `tasks.md` is written before any remote call and remains the source of truth.
- **No Jira writes without an explicit ask AND a confirmed destination.** Never create tickets by default; confirm project + issue type first.
- **Staging location is the user's to choose.** Beside the spec > argument > memory default > ask. Persist the default only with consent.
- **Nothing written before approval.** The breakdown is quizzed and iterated first; the `tasks.md` write happens only after sign-off.
- **Blockers first, native links.** When pushing to Jira, create in dependency order and use the "Blocks" relationship (renders the frontier in Jira's UI), not just prose.
- **Never modify the parent.** Link to it; don't transition or close it.

## Quality Loop

Before returning, check the output against these criteria. If two or more fail, revise and re-check — at most two passes, then note what still falls short.

- Tickets are tracer-bullet vertical slices with explicit dependencies and [P] markers
- The local tasks.md is the artifact; Jira push happens only on opt-in
- Wide refactors use expand-contract sequencing where relevant
- Every ticket maps to something in the source spec/plan — none invented

> **Host portability:** tool names follow Claude Code conventions; on other hosts map by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/plan-to-tickets.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
