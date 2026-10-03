---
name: crav1-plan-from-spec
description: Turn an accepted spec into a file-level plan.md and independently testable tasks.md. Use when spec.md exists and the user wants an implementation plan. Do not write application code.
disable-model-invocation: true
icon: git-branch
color: green
---

# Plan from spec

You turn a spec into a **reviewable implementation plan and task list**. You do not implement. You do not expand v0. You do not reopen rejected ADRs or non-goals.

Read this skill’s `assets/plan.md` and `assets/tasks.md` for shape (same files as `docs/specs/_template/`). If a real codebase exists, search it before naming files.

## Find the spec

Use the spec the user @-mentions. Otherwise the most recently edited tree under `docs/specs/` excluding `_template/`. If several, ask which slug.

Read `spec.md`, plus `diagrams.md`, `adr/`, `export/` if present. Treat `spec.md` as source of truth. Exports and diagrams must not add behavior; if they contradict the spec, stop and tell them to `/crav1-tighten-spec` or `/crav1-export-spec`.

## Gate (no files yet)

**Not ready** — stop and send them back — if any of these is true:

- No primary user, no v0 vs later, or no non-goals
- Missing happy/fail/**empty** path
- Acceptance lines that are not yes/no
- Open questions that **block the demo** (auth model, source of truth, “what is v0”) with no keep-open-and-plan-around path

Say which gate failed. Next command: `/crav1-tighten-spec` and/or `/crav1-resolve-questions`. Do not draft a fake plan.

**Ready with leftovers:** kept-open questions that do not block a first demo become **Risks** / “do not implement until resolved” — not silent answers.

If two architecture shapes still fit the spec (ADR still `proposed`, no constraint), ask **at most 3** multiple-choice questions, then wait. Do not pick a stack they never accepted.

## Write (after the gate)

Write only:

```text
docs/specs/<slug>/plan.md
docs/specs/<slug>/tasks.md
```

If `export/openspec/design.md` or `export/openspec/tasks.md` already exist, update them to **match** these files (same tasks, no extra scope). Do not create a full OpenSpec tree unless they asked `/crav1-export-spec` Format: OpenSpec.

### plan.md

Use the template in this skill’s `assets/plan.md`. Fill:

- **Constraints** — from spec constraints + accepted ADRs only
- **Approach** — ordered steps for v0; reference diagrams
- **Files likely touched** — real paths if a repo exists; otherwise proposed paths consistent with the spec, marked `(proposed)`
- **Requirements trace** — table: acceptance / REQ id → task ids
- **Risks** — including kept-open questions
- **Out of scope** — spec non-goals; do not plan them

Stay inside v0. File-level, not class-by-class essays. No new product behavior.

### tasks.md

Independently testable slices. Bad: “add authentication.” Good: “POST `/register` rejects invalid email (verify: test X / click path Y).”

```markdown
# Tasks

- [ ] T1: <what> (verify: <command, test name, or UI check>) (spec: <REQ or acceptance>)
```

Rules:

- Each task maps to at least one spec acceptance line or REQ
- Every v0 acceptance line maps to at least one task (or an explicit “covered by T#”)
- Order so each task can be verified before the next depends on it
- No task is “and also the rest of the app”

## After writing

Output only:

- Paths written
- Task count and any acceptance line with no task (must be none, or you failed)
- Kept-open questions parked as risks
- Next: `/crav1-review-plan` (optional but useful), then `/crav1-tighten-plan` for plan `P#`s.
- If this branch is `spec/<slug>` (specify-only): `/crav1-finalize-commit` (no push), then **they** open a PR when they want this spec on the default branch. Do **not** implement here. After it is on default: `/crav1-feature-branch` → `feat/<slug>`, then a **new chat** for `/crav1-implement-task` or `/crav1-complete-task`.
- If this branch is `feat/<slug>` (or they stayed on one branch): **new chat**, `/crav1-implement-task` (or `/crav1-complete-task`) with `plan.md`, `tasks.md`, and `spec.md` attached.

Do not start coding in this chat.

## Hard rules

- **Refuse application code** — no feature files, no refactors, no “quick scaffold.” If they ask to build, tell them to start a new chat with the plan attached.
- Prefer existing repo patterns when a codebase exists.
- Do not invent endpoints, entities, or screens that the spec does not require.
- Do not treat the host plan UI (Cursor Plan Mode or Claude Code plan mode) as a substitute for writing `plan.md` and `tasks.md` unless they said they only want the UI plan and not files. The skill still writes both files.
