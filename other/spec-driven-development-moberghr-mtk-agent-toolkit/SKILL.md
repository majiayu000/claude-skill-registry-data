---
name: spec-driven-development
description: Use when the task is a new feature, breaking change or multi-file change whose spec and design should be approved before any code is written.
type: skill
license: MIT
compatibility:
  - claude-code
  - codex
user-invocable: false
---

# Spec-Driven Development

## Overview

Write the implementation spec before writing code. The spec is the shared source of truth between the engineer, the command flow, and the reviewers. Code without a spec is guessing.

> **Tool discipline (phase-locked):** spec authoring is a read + spec-artifact phase. Write **only** the spec artifacts (`docs/specs/<date>-<slug>.md` and its `.json` sidecar) — never source or test code. Code starts at Phase 3, after the approval gate; a source edit here is a scope violation.

> **Supplied spec/plan (adoption, not authoring):** when the engineer hands in a complete spec or plan as the input (e.g. `docs/specs/…md` or `docs/plans/…md` already on disk), `implement`'s Phase 0.7 *adopts* it as the source of truth. In that case this skill validates the supplied artifact against the schema and reconciles it against the current code (see `prior-work-check`'s existing-plan reconciliation) rather than re-authoring to a fresh path — never overwrite or version-bump the engineer's input. See `implement/SKILL.md` Phase 0.7.

## When To Use

- New endpoints, handlers, routes, or views; database changes or migrations
- Multi-file work or breaking changes
- Any task where approval should happen before coding, or likely to outlast a short focused session

### When NOT To Use

- Typo fixes, one-line config updates with no behavior impact, or small bug fixes that clearly stay within quick-fix scope → `fix`

## Modes

- **Standard (default).** The steps below: ambiguity gate, the spec sections, the JSON sidecar, honest `security_impact`, prior-work check.
- **Extended spec (opt-in).** Adds EARS/ANT requirements with `lint-ears.sh`, the INVEST+C 16-item score, a cited Constitution Check, and a delta against a per-area baseline. Turn it on when the engineer asks for it, or when the Phase 2 rigor score lands at **MAX** — then add the extended sections before the Phase 2.5 gate. Record the mode in the spec header (`Spec mode: extended`). See **Extended Spec Mode** below.

## Workflow

### Steps

1. Read the coding guidelines from the active tech stack's `## Reference Files`, the stack's testing supplement, `.claude/references/domain-finance.md` (finance and security supplement) when scope touches auth/financial/infra, and `architecture-principles.md` if present. Query relevant lessons:
   `bash "$([ -n "${MTK_HELPER_ROOT:-}" ] && echo "$MTK_HELPER_ROOT/scripts/learnings.sh" || ([ -f scripts/learnings.sh ] && echo scripts/learnings.sh || echo "${CLAUDE_PLUGIN_ROOT}/scripts/learnings.sh"))" query --phase spec --files "<comma-separated paths from initial scope>" --max 8` (falls back to reading `tasks/lessons.md`; resolve it from the main worktree when in a worktree).
2. Surface assumptions before planning — runtime, architecture, storage, auth, boundaries. Do not silently fill in major gaps.
3. Classify scope: `internal-refactoring` · `new-feature` · `breaking-change`.
3b. **Dirty-worktree step.** Run `git status --porcelain`. Every modified or untracked path not in this change manifest goes under **Risks** as a `dirty-worktree` entry and into `out_of_scope` in the sidecar, so the `plan-gap-reviewer` can reject any batch that touches it.
4. Read 2-3 nearby files that represent the local pattern to follow.
5. **Ambiguity gate (BEFORE drafting).** Detect whether the task has genuine ambiguity that would change the spec. Trigger if **any** of:
   - Two or more plausible designs exist and the request doesn't pick one (e.g., reflection vs source-gen, sync vs async, single vs split package).
   - Scope edges are undefined (e.g., "users" — authenticated only? including service accounts? soft-deleted?).
   - An architectural choice is unresolved (e.g., new boundary, new persistence target, cross-slice contract).
   - A success criterion would be untestable as stated.

   If triggered: stop and call `AskUserQuestion` with one question per ambiguity (max 4). Each question presents 2–4 concrete options with the tradeoff in the description. Wait for answers, then proceed to drafting with answers folded into the spec — do not defer them to "Open questions" in the spec body.

   **Interview mode (Socratic, one question per round).** Switch from the batched form above to a structured interview when **either**: three or more ambiguities triggered, or the request is one or two sentences for clearly multi-file scope (the ask is underspecified relative to its blast radius). In interview mode:

   - Ask **one** question per `AskUserQuestion` round, starting with the highest-leverage ambiguity — the one whose answer most reshapes the spec (usually the success definition or the architectural boundary, not the naming choice).
   - Probe **intent**, not just option preference: lead with what the engineer is trying to achieve or avoid ("what should happen to in-flight payments when this flag flips?"), then offer the 2–4 concrete options informed by that framing.
   - After each answer, **re-derive the remaining ambiguities** before asking the next question — answers routinely resolve later questions or surface new ones; a pre-computed question list goes stale after round one.
   - Cap at **5 rounds**. Anything still open after the cap is written into the spec as an explicit assumption with the chosen default and its rationale — never as a silent guess.

   Batched mode remains the default for one or two independent ambiguities — don't stretch a two-question gate into an interview.

   If `AskUserQuestion` is deferred, load it via `ToolSearch` with `select:AskUserQuestion`. If the harness doesn't expose it, print the questions as a numbered list and stop until the engineer answers.

   Skip the gate when: the engineer's request already specifies the approach, the task follows an obvious existing pattern, or only one viable design fits the constraints. Document the skip in one line ("ambiguity gate skipped: <reason>") so it's visible in the session log.

   **When an ambiguity is version-sensitive** — the right answer depends on current external best-practice, the installed package version's behavior, or a recent migration path rather than a preference — first follow `.claude/skills/research-context/SKILL.md` to produce a grounded, cited brief, then fold its recommendation into the options you present at the `AskUserQuestion` gate. Resolve "which design" from current information, not training-cutoff memory.
6. Produce a spec with these sections: Summary · Success criteria · Architecture and design · Security and compliance impact · Change manifest · Test manifest · Implementation batches · Risks and assumptions · Open questions.
7. **Security impact, honestly.** Map each `change_manifest` path against the trust boundaries: auth, payments, audit, secrets, PII, IAM, financial state. If any path touches one, `security_impact` is not `none` — state the level and a one-line justification. A mis-classified impact is the one spec error that silently removes reviewers later (it feeds the rigor floor and the drift check).
8. Elegance check: reduce file count, new abstractions, and moving parts if a simpler design exists.
9. **Prior-work check** — run `prior-work-check` once against the draft. A BLOCKED verdict (an existing implementation the spec would duplicate) holds the approval gate until the spec is revised. Append its output under `## Prior Work Check` in the spec.
10. Persist the spec to disk:
   - **Resolve the artifact root first:** `bash scripts/resolve-artifact-root.sh "<a path the change touches>"`. Every `docs/specs/...` path below is relative to **that** root, not automatically the repo root. In a polyglot repo a subtree that owns its artifacts (its own `docs/specs/` plus a `CLAUDE.md`) keeps them — writing to the repo root instead would scatter one project's specs across two locations. A repo with no such subtree resolves to the repo root, so single-project repos are unaffected.
   - Create `docs/specs/` under the resolved root if it does not exist.
   - Compute the base target: `<artifact-root>/docs/specs/YYYY-MM-DD-<feature-slug>` (no extension yet).
   - **Version detection:** Check whether `docs/specs/YYYY-MM-DD-<feature-slug>.md` already exists.
     - If it does not exist → write to `docs/specs/YYYY-MM-DD-<feature-slug>.md` (no suffix).
     - If it DOES exist → find the highest existing `-vN` suffix:
       ```bash
       ls docs/specs/YYYY-MM-DD-<slug>*.md 2>/dev/null | grep -oE '\-v[0-9]+' | sort -V | tail -1
       ```
       If a `-vN` suffix is found, write as `-v(N+1)`. If the file exists but no `-vN` variants do, write as `-v2`.
     - The JSON sidecar gets the **same version suffix** (e.g., `docs/specs/YYYY-MM-DD-<slug>-v2.json`).
     - Emit one line before writing: `Writing spec → docs/specs/<final-filename>.md` so the engineer can confirm the version chosen.
   - **Also emit a machine-parseable sidecar** at `docs/specs/<final-filename>.json` with the schema in **Machine-Parseable Manifest** below. This sidecar drives `spec-drift-detection` after implementation.
   - This enables session recovery, human review outside chat, and reuse across sessions.
   - Add `docs/specs/*` to `.gitignore` with the negations `!docs/specs/baseline/` and `!docs/specs/baseline/**`: per-feature specs are working artifacts, an extended-mode baseline is committed.
11. **Publish the spec artifact (additive, capability-gated).** After the spec is on disk, follow `.claude/references/artifact-publishing.md` to create the workflow's Claude Artifact from the spec — this is the first section of a single browsable URL that later phases (plan, handoff, health) update in place. Publishing is additive: disk is the source of truth and the step is a silent no-op when the `Artifact` tool is unavailable or `MTK_ARTIFACT_PUBLISH=0`. Never publish anything not already written to disk.
12. Always stop for approval (as `.claude/references/implement-approval-gate.md` defines it) before implementation. When invoked from the implement workflow, this means handing control back to Phase 2.5 approval gate (which uses `AskUserQuestion`). When this skill asks on its own and the session context has the `WORK SESSION:` line, first open the spec `.md` beside the terminal with that reference's best-effort `work show` line, which is silent and never blocks the question. Do not silently continue to implementation.

**Approval is sealed, not asserted.** On approval, the implement gate records a SHA-256 **approval seal** over the approved spec/plan bodies — the two scope-encoding artifacts (`scripts/workflow-artifact.sh seal`). The todo is deliberately *not* sealed: it is progress state designed to mutate as batches complete, so sealing it would flip the seal STALE on the first checkbox tick. Because the seal binds the exact approved bytes, editing an approved spec or plan afterward invalidates the approval deterministically — `verification-before-completion` re-checks it with `verify-seal` (refusing completion on a STALE seal) and the `spec-approval-trigger.sh` hook re-queues the gate, rather than trusting a stale `status: approved` marker. This is why moving a success-criterion goalpost post-approval requires re-opening Phase 2.5: the seal will not match.

## Extended Spec Mode

Only when the engineer asks for it, or at rigor MAX. Each item is added to the spec before the Phase 2.5 gate.

1. **Requirements in EARS.** A `## Requirements` section where every bullet uses one template: *Ubiquitous* "The system shall …" · *Event-driven* "When <trigger>, the system shall …" · *State-driven* "While <state>, the system shall …" · *Optional* "Where <feature>, the system may …" · *Unwanted* "If <trigger>, then the system shall …". **ANT check:** if you cannot describe a counter-example for a bullet ("shall be reliable", "handle errors gracefully", "where appropriate"), rewrite or drop it.
2. **EARS lint.** `bash scripts/lint-ears.sh docs/specs/<file>.md` must return zero violations before the gate; record the spec path in the same call (`&& "$WFA" set "$MTK_WF_UUID" results.spec_path=…`). It checks only the `## Requirements` section.
3. **INVEST+C score** against `.claude/references/claude-ready-checklist.md`. Any failing +C item is fixed before the gate; ≤13/16 goes back to draft. Cite failing item numbers.
4. **Constitution Check.** Run `bash scripts/constitution-digest.sh`, then list in a `## Constitution Check` section every Critical Rule or principle that constrains this design, cited by id, with one line on how the design satisfies it. A bent rule is an explicit exception with rationale; an `[EXTRACTED]` violation normally means redesign. `spec-drift-detection` verifies what is cited here.
5. **Delta against a baseline.** Set `baseline_area` (and `delta.adds/modifies/removes` when known; removals are always explicit) so Phase 7.5 can archive it — see `.claude/references/delta-spec-model.md`.

## Machine-Parseable Manifest (JSON Sidecar)

Every spec is accompanied by `docs/specs/<date>-<slug>.json`, validated against
`.claude/schemas/handoff.schema.json`. It is the source of truth for drift detection
and for the `plan` / `implement` sections downstream skills append. Required top-level
keys: `slug`, `date`, `scope`, `change_manifest[]` (`path`, `action`, `purpose`,
`mechanical`), `public_contracts[]` (`kind`, `signature`, `change`, `surface`),
`success_criteria[]` (`id`, `description`, `verification`, `evidence_channel`,
`observable`), `test_manifest[]`, `out_of_scope[]`, `security_impact`, `assumptions[]`,
`risks[]`; `baseline_area` + `delta` in extended mode only;
`coverage_claims[]` and `conditional_descopes[]` when they apply. Every `change_manifest`
path must exist or be marked `create`; an `[ASSUMED]` entry or an unverified coverage
claim is an open decision and blocks `MTK_AUTO_PROCEED`.

**Read `.claude/references/spec-sidecar-manifest.md`** for the full field reference,
allowed values, and the worked example before writing or amending a sidecar.

## Verification

- [ ] Spec is self-contained and scope still matches the original request
- [ ] Every file and test file appears in the manifest; the JSON sidecar matches the markdown's change_manifest, test_manifest, success_criteria, and security_impact
- [ ] Success criteria are specific and testable; assumptions are explicit
- [ ] `security_impact` honestly reflects touched trust boundaries (step 7)
- [ ] Ambiguity gate ran or its skip was stated in one line
- [ ] `prior-work-check` ran once with no BLOCKED verdict (step 9)
- [ ] Extended mode only: `lint-ears.sh` returns 0, +C score > 13/16 recorded, Constitution Check present, `baseline_area` set
- [ ] Spec artifact published (or gate correctly closed) per `.claude/references/artifact-publishing.md`, disk written first
