---
name: planning-and-task-breakdown
description: Use after a spec is approved and before multi-file implementation begins, to break work into verifiable batches with checkpoints.
type: skill
license: MIT
compatibility:
  - claude-code
  - cursor
  - codex
user-invocable: false
---

# Planning And Task Breakdown

## Overview

Convert the approved plan into small, executable tasks that can be verified one at a time. Good task breakdown reduces hidden coupling, scope drift, and fake progress.

> **Model tier:** runs on `sonnet` (bounded decomposition against a written spec) per `.claude/references/model-routing.md`.
> **Tool discipline (phase-locked):** planning is a read + plan-artifact phase. Write **only** the plan/todo artifacts (`docs/plans/`, `tasks/todo.md`) — never source or test code. Implementation belongs to Phase 3; a source edit here is a scope violation the `scope-guard` hook will flag.

## When To Use

- After spec approval
- Before any multi-file implementation
- When implementation needs explicit checkpoints or re-planning boundaries

### When NOT To Use

- Tiny single-file work already small enough to execute safely
- Exploratory debugging before the root cause is known

## Workflow

1. Start from the approved change manifest and test manifest.
2. Break work into batches of 2-4 related files, dependency-ordered. Two batches that list the same file in `files` **must** carry a dependency edge between them (later depends on earlier) — this is what lets the scheduler run edge-free batches concurrently without two implementers editing one file. Files that many batches touch by nature — DI registration (`Program.cs`, `*Startup*`, `DependencyInjection*`, `ServiceRegistration*`), project/solution files (`*.csproj`, `*.sln*`, `package.json`, `pyproject.toml`), and migration snapshots — are **serialize-if-touched**: every batch that touches one of them depends on the previous batch that did.
3. For each task, write:
   - task description
   - acceptance criteria
   - **verification step — quoted, not composed.** Copy the build/test/format
     command verbatim from the active tech-stack skill's `## Build & Test Commands`
     or the reference section it points at, and cite that source in the batch
     (`per dotnet/data-layer.md §5.5`). A command written from memory is
     `[UNVERIFIED]` and must be marked so, because the implementer will run it: a
     freehand `dotnet ef … --startup-project AIProxy` cost a batch a failed run
     when the correct invocation was already written down in the stack reference
     (2026-09 field run).
   - files in scope
   - **Boundary — state the invariant, not the file.** Write what must remain true,
     not which file must stay shut. A bare file prohibition is a bug generator: a
     brief saying "don't touch `SkillsDataRepository`" meant "don't add filtering
     there", but the implementer read it literally and loaded every bundled file on
     every request to route around it — and the correct fix was two lines in the
     file the brief had forbidden (2026-09 field run). Write "filtering stays out of
     the repository layer — it remains a plain data accessor", not "no changes to
     `Foo.cs`". Name a file only when the file itself is the constraint (a frozen
     migration, a vendored artifact), and then say why it is frozen.
   - **Depends (mandatory):** the batch ids this batch assumes are complete (e.g., "B1 — needs the entity to exist"). An empty list is a claim of independence and must say why (`depends_rationale: "independent: no shared files, reads no type another batch creates"`). The scheduler runs edge-free batches in the same wave, so a missing edge is a concurrency bug, not a style nit.
   - **Governing constraints:** the Critical Rule / principle ids that constrain
     this batch — from the spec's Constitution Check in extended mode, otherwise
     from `bash scripts/constitution-digest.sh`.
     Each batch states which rules it must satisfy, not just what it builds —
     recorded in the plan so the implementer and human reviewers see, per
     batch, exactly which rules constrain it.
     An empty list is allowed only with an explicit "no rule constrains this
     batch" note.
4. Prefer vertical slices where possible so each batch leaves the system in a working state.
4b. **Package-legitimacy gate for new dependencies.** If any batch introduces a third-party package **not already present** in the repo's dependency manifests — especially one an AI assistant, blog post, or the spec's research brief recommended — do not plan a bare install step. Instead:
   - Run the stack's registry-verification command (from `.claude/references/dependency-intake-checklist.md` criterion 0, also listed in the active tech-stack skill) to confirm the package exists and is the real one (not a typosquat / hallucination).
   - Tag the package `[ASSUMED]` in the plan until verified, and insert an explicit `checkpoint:human-verify` step **before** the install task. This checkpoint is one of the conditions that blocks `MTK_AUTO_PROCEED` at the `implement` Phase 2.5 gate, so an unverified package can never be installed autonomously.
   - A criterion-0 Poor (not found / dead repo / typosquat signal) blocks the dependency outright — re-plan without it.
5. State the resulting wave schedule in the plan (`W0: B1 · W1: B2 B3 B4 · W2: B5`) — derived from `depends` as topological levels, wave width capped at `MTK_BATCH_WAVE_MAX` (default 3). The schedule is a readback of the edges, not a second source of truth: if it looks wrong, fix `depends`.
6. Read `tasks/todo.md` before writing it. Unfinished items for different work (not batches of this plan, the same comparison `batch-fix` makes against its stub's findings) stay in the file under a short heading below the new plan, or you ask the engineer; never overwrite them silently. Then write `tasks/todo.md` with:
   - task title
   - scope and branch
   - batches with checkboxes
   - post-implementation review items
7. If a spec file exists in `docs/specs/`, persist the plan alongside it:
   - **If the plan was supplied by the engineer as input** (adopted by
     `implement` Phase 0.7 — the file already exists at the plan path): do **not**
     author a new plan or version-bump the engineer's file. Adopt the supplied
     path as-is and validate its `plan.batches` against the JSON sidecar schema;
     Phase 0.7 has already reconciled it against current code (`prior-work-check`
     runs once per run). Skip the authoring sub-steps below.
   - Use the **full filename stem of the active spec**, including any version suffix (e.g., `-v2`, `-v3`). If the spec was written as `docs/specs/2026-04-23-foo-v2.md`, the plan is `docs/plans/2026-04-23-foo-v2.md`.
   - If no spec path is available (standalone planning run), use `YYYY-MM-DD-<feature-slug>.md` with no suffix.
   - Create `docs/plans/` if it does not exist.
   - Add `docs/plans/` to `.gitignore` if not already present.
   - This enables session recovery and plan reuse across sessions.
8. **Append the `plan` section to the existing JSON handoff artifact** at
   `docs/specs/<date>-<slug>.json` (created by spec-driven-development).
   Schema: `.claude/schemas/handoff.schema.json`. Required keys:
   ```json
   "plan": {
     "batches": [
       { "id": "B1", "files": ["src/X.cs"], "acceptance": "...",
         "verification": "...", "boundary": "...",
         "depends": [], "depends_rationale": "independent: first batch, creates the entity",
         "governing_constraints": ["C0.2", "S1.15"] },
       { "id": "B2", "files": ["src/XHandler.cs"], "acceptance": "...",
         "verification": "...", "boundary": "...",
         "depends": ["B1"],
         "governing_constraints": ["C0.2"] }
     ]
   }
   ```
   Every `files` entry must already exist in the top-level `change_manifest`.
   If it does not, re-plan first — don't quietly widen scope here. `depends` is
   required on every batch; `depends_rationale` is required when it is empty.
   Any two batches sharing a `files` entry without an edge between them fail
   the sidecar check and the `plan-gap-reviewer` marks it `BLOCKING`.
9. Keep the task list synchronized with reality. If a new file is needed, re-plan before continuing.
10. Record the plan/todo paths on the workflow artifact and leave `plan_trust_gate` at `pending` — only the engineer's Phase 2.5 approval flips it to `pass`. See `.claude/references/orchestration-gates.md`.
10.5. **Update the workflow artifact (additive, capability-gated).** With `plan_path`/`todo_path` recorded, follow `.claude/references/artifact-publishing.md` to add the Plan section to the workflow's Claude Artifact. Because the artifact is keyed to the workflow uuid, this **updates the existing URL in place** (passing the recorded `results.artifact_url`) — it does not mint a new link. Silent no-op when the tool is unavailable or `MTK_ARTIFACT_PUBLISH=0`.
11. **Anti-anchored gap check.** Before surfacing the plan to the engineer, dispatch the `plan-gap-reviewer` agent with the original user request and the saved plan path — plus, when they exist, the spec markdown path, the spec JSON sidecar path, and `tasks/todo.md`. Passing the sidecar and todo activates the agent's **cross-artifact consistency check**: spec ↔ plan ↔ todo are mapped against each other in both directions (manifest entries ↔ batches, success criteria ↔ tests, out-of-scope ↔ batch contents) so disagreement between the artifacts is caught before the approval gate, not after implementation. The agent runs in a forked context and is forbidden from reading lessons, prior reviewer output, or the workflow artifact — its job is to challenge the plan against the repo with no anchors. Surface every `BLOCKING` finding back to the planner and revise before the approval gate. Surface `ADVISORY` findings unchanged at the approval gate so the engineer decides. A plan-gap `PASS` does not replace engineer approval: the gate still runs.

## Rules

- Every hand-written file touched must already exist in the change manifest. **Derived artifacts are the exception** — lockfiles, snapshots, generated sources, and files whose own header says they are generated stay out of it. Name the regenerator in the batch's verification step instead (`then run scripts/build-references-index.sh`); `validate-handoff.sh` classifies the output as collateral, so an unlisted one is never drift.
- Every batch must be buildable.
- Every behavior change must have an associated test task.
- No task should require changing more than a small handful of files without justification.
- Re-planning is mandatory if the task grows beyond the approved manifest.

## Verification

- [ ] `tasks/todo.md` exists and is actionable
- [ ] Batches are dependency-ordered; every batch has `depends`, every empty `depends` has a rationale, and no two edge-free batches share a file
- [ ] Each task has acceptance and verification
- [ ] Each batch ends with a concrete checkpoint
- [ ] Each task has Boundary and Depends annotations, and every Boundary states an invariant (a file name appears only when the file itself is frozen, with the reason)
- [ ] Every verification command is quoted from the tech-stack skill or a reference it cites, with the source named — or explicitly marked `[UNVERIFIED]`
- [ ] No circular dependencies exist between tasks
- [ ] Workflow artifact updated in place (same URL) or gate correctly closed, per `.claude/references/artifact-publishing.md` (step 10.5)
