---
name: apply-step
description: >-
    Apply a single step of a tmp/ plan — read the plan README and all previous steps for accumulated
    context and decisions, then implement the current step test-first against plainworks'
    engineering baseline, validate the affected package(s), and mark the step done. Use to execute
    one specific plan step, or as the per-step unit that apply-plan drives.
---

# Applying one plan step, in context

`apply-step` implements exactly one step of a plan folder (from `create-plan`). It is the unit of work `apply-plan` calls per step, and it can also run directly on a single step file.

## Input

A path to one step file, e.g. `tmp/channel-sse-reconnect/02-sse-adapter.md`.

## 1. Load full context before editing

A step is not self-contained — earlier steps make naming, layering, and API decisions this step depends on. Read, in order:

1. **`README.md`** of the plan folder — goal, dependency order, and the cross-cutting baseline rules.
2. **Every previous step** (`NN-*.md` with a lower number) — for the decisions and files they established. Honor them unless one leaves legacy in place (a shim, a parallel old-and-new model, or new code built around an old path). In that case, stop and add a redesign step with `create-plan`; don't build on the flaw.
3. **The current step** — its scope, numbered actions, files touched, and acceptance criteria.

Confirm the current step's *Depends on* steps are `done` before starting. If a dependency is unfinished, stop and say so.

## 2. Implement the step against the baseline

Apply the current step's actions **test-first**, honoring the baseline in [`../../copilot-instructions.md`](../../copilot-instructions.md) — the plan does not override it:

- **TDD.** For each behavior: failing vitest test → minimal code → refactor while green, failure paths included. Never write production code first and add tests after. Reuse `@plainworks/testkit` fakes/harnesses.
- **Best-practices bar.** The *simplest* design that fully solves the step — flexible (small typed seams over rigid/speculative abstraction), scalable (bounded buffers, cancellation, no unbounded streams), current idiomatic TS/React. Complexity must earn its place.
- **Placement & layering.** Right package and layer; a package in `Ln` imports only `L<n`; a cross-layer need defines the seam in the lower package (`std` owns shared contracts/event shapes) and implements it higher. A new package is born through `bun run gen package` (see `new-package`) and added to `internal/boundaries/layers.json`.
- **Host-independence.** Server-safe `.` entry (no React/DOM); optional `./client` with per-module `"use client"`; server-only/auth token-custody stays out of client graphs.
- **Composition.** No import-time side effects, no module-level singletons — per-request factories; adapters register explicitly into an injected registry.
- **Typed & minimal.** No `any` in public surfaces; typed errors preserving cause; timeout + cancellation on remote calls.
- **Root-cause, no compatibility (alpha).** Redesign on current best practices rather than patching; breaking changes are welcome. Build new code for the end state, never around the old path. When the step supersedes something, move every consumer and delete the old path, its exports, and its docs in this step, unless the plan names a later deletion step. Leave no shims, aliases, deprecated re-exports, or compat flags. See [Development stage](../../copilot-instructions.md#development-stage-alpha-redesign-over-compatibility).
- **Vendored atoms stay locked.** Never hand-edit `packages/elements/src/shadcn/**` or `shadcn.lock.json`, even when a step's `Files touched` lists them — change an atom only with `registry:update`. A visual or behavior change follows the **deviation ladder** (theme → call site → `ui` wrapper); see the [Vendored atoms](../../copilot-instructions.md#vendored-atoms) baseline.
- **Organize by concern; self-documenting by path.** Group related modules into a **concern folder** with a re-export-only `index.ts` barrel plus concern-named files (as `rskit` groups `retry/{backoff,policy}.rs` under a barrel-only `mod.rs`); a single concern is one clearly named file. No junk-drawer `utils`/`helpers`/`core`, no bare verb modules/exports (`compose`, `classify`) — qualify by concern (`pipeline/interceptor.ts` → `composeInterceptors`). Fold **proactively** when a second sub-concern appears — never pile several concerns flat in `src/`. A barrel `index.ts` re-exports only, holds no logic. When you touch a file that already mixes distinct concerns, promote it **in this step** — don't defer the reorg.

Keep the edit scoped to *this* step's `Files touched`; if the step is mis-scoped, report it rather than silently expanding.

## 3. Validate, review, and mark done

- **Validate** the affected package(s) with [`validate`](../validate/SKILL.md), scoped `turbo`/`bun run`, vitest green under race/shuffle. A step does not land red. Run `bun run check-boundaries` on any structural change.
- For a step that changes what an app user sees, meet the [UI Definition of Done](../../copilot-instructions.md#build-test-and-lint): check the touched flows in e2e, capture them with `ui:capture --flow <flow>` and look at the frames, and note the summary in the step's decisions.
- Add the **Changeset** the step's acceptance requires.
- **Review** the step's diff with the relevant [`review`](../review/SKILL.md) passes — ideally in a fresh agent.
- Only when acceptance criteria are genuinely met, flip the progress signal so `apply-plan` can resume: set `**Status:** done` and check its `- [x]` boxes. Never mark a step done on a partial or red result.

## Repo workflow

Work on a branch (`create-branch`), leave edits **uncommitted** for the maintainer to commit and push; open a PR (draft) only when explicitly asked. When the change becomes a branch/PR, name it by the change — never `step-2`.
