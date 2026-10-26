---
name: rite-polish
description: Polish the active feature's code and any touched UI before review. Use for finish or normalization requests; not for repository-wide refactors.
argument-hint: "[target | bolder | quieter | distill | harden | normalize-only]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/candidate-integrity.md","rite-polish/reference/code.md","rite-polish/reference/anti-patterns.md","rite-polish/reference/anti-ai-slop.md","rite-polish/reference/harden-checklist.md","rite-polish/reference/ledger.md","rite-build/reference/checkpoint.md"],"triggers":{"adr":["rite-polish/reference/adr-promotion.md"],"agents":["devrites-lib/reference/standards/agents.md"],"backend":["rite-polish/reference/backend-polish.md"],"coding":["devrites-lib/reference/standards/coding-style.md","devrites-lib/reference/standards/duplicate-code.md"],"errors":["devrites-lib/reference/standards/error-handling.md"],"ui":["rite-polish/reference/ui.md","rite-polish/reference/design-memory.md","rite-polish/reference/design-system-discovery.md","rite-polish/reference/browser-polish-evidence.md","devrites-lib/reference/standards/browser-proof-checklist.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md","decision-coverage.md","architecture.md","plan.md","tasks.md","traceability.md","eng-review.md","test-plan.md","gates.md","evidence.md","touched-files.md","design-brief.md","browser-evidence.md","polish-report.md"],"workspaceByRole":{"slice-wright":["spec.md","architecture.md","plan.md","tasks.md","test-plan.md","state.md","decisions.md","design-brief.md"]},"rootOnly":["rite-build/reference/checkpoint.md"]} -->
> Read-set manifest: `devrites-engine context --skills-root .omp/skills <slug> --phase polish` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-polish: finish before review

Polish code for every feature. When the feature touches UI, normalize and polish the
UI as well. Complete this self-review before `/rite-review`. The code and UI phases
live in [`reference/code.md`](reference/code.md)
([`anti-ai-slop.md`](reference/anti-ai-slop.md),
[`backend-polish.md`](reference/backend-polish.md))
and [`reference/ui.md`](reference/ui.md)
([`browser-polish-evidence.md`](reference/browser-polish-evidence.md),
[`design-system-discovery.md`](reference/design-system-discovery.md),
[`harden-checklist.md`](reference/harden-checklist.md));
read only the phase in scope.

## Operating rules

- **Functionality complete first.** Polish runs after `/rite-prove` (full
  feature proven).
- Follow the shared
  [`candidate-integrity.md`](skill://devrites-lib/reference/candidate-integrity.md).
  Polish owns every candidate-affecting correction and durable rollup before Review.
- Feature scope only.
- For UI, **normalize before polishing**. Do not add decoration on top of drift.
- **Bounded polish passes.** Verification runs in bounded passes, not a loop: after the
  Phase 4 assessment, at most one more correction round for **new** findings, then stop —
  residual subjective preference is recorded in `polish-report.md`, not re-polished.
  **Failing case:** the same surface reopened a third time with no new failing evidence.
- **Root selects; wright edits.** The controlling chat assesses and reconciles, but every
  accepted source/test correction is dispatched to the sole writer,
  `devrites-slice-wright`, through
  [`agents.md`](skill://devrites-lib/reference/standards/agents.md). Never edit source inline or
  run two correction writers concurrently.

## Polish axes (C3 — completeness vs craft)

Score **separately**; conflating them hides gaps:

| Axis | Question | Failing case |
| --- | --- | --- |
| **ux_coverage** | Did we compare every stated alternative/state? | Omitted empty/error state treated as agreement |
| **completeness** | Are required states, copy, and flows present? | Hero-only layout with no loading/error |
| **craft / anti-slop** | Does the UI avoid generic template patterns? | Inter + purple gradient hero with no product-specific hierarchy |
| **distinction** | Is there one intentional signature detail? | Polished but indistinguishable from a template |

Incomplete comparison is **not** agreement. Record axis deltas in `polish-report.md`.

## Orchestration

0. **Read** `.omp/skills/devrites-lib/reference/standards/core.md` first (the always-on operating rules). The
   per-phase rule files ([`coding-style.md`](skill://devrites-lib/reference/standards/coding-style.md), [`error-handling.md`](skill://devrites-lib/reference/standards/error-handling.md), …) load on demand
   from `reference/code.md` / `reference/ui.md` when their phase runs; for UI scope also read
   `.omp/skills/devrites-lib/reference/standards/browser-proof-checklist.md`.
   Then read the explicit or active workspace's `state.md` directly.
1. **Read** `state.md`, `touched-files.md`, the current candidate digest, and the
   `git diff` for the active workspace (or `$ARGUMENTS` if a target was given).
2. **Detect UI scope:** UI is touched when the diff changes rendered output:
   markup, template, style, design token, client component, or a visible string
   (including an API error message shown in the UI). These paths are leads to
   inspect, not the predicate: `.tsx`, `.jsx`, `.vue`, `.svelte`, `.html`, `.css`,
   `.scss`, `.sass`, `.less`, `.styl`, component dirs (`components/`,
   `pages/`, `routes/`, `app/`, `views/`, `screens/`), Storybook stories,
   or design-token files; when in doubt whether output changes, treat it as UI
   scope. A diff with no rendered-output change records
   `UI scope: none (no rendered output)` and skips Phases 3–4; non-visual client
   code still gets frontend engineering review (`devrites-code-reviewer` frontend lane).
   **Failing case:** an `app/services/billing.rb` diff opens Phase 4 and demands
   captures.
3. **Always** read [`reference/code.md`](reference/code.md) and assess **Phase 1
   (code polish)**; if backend was touched, assess **Phase 2 (backend polish)** from
   the same file. Assess step 4's UI phases on the same frozen digest while the
   code assessment runs, reconcile both, then send every accepted code and UI
   correction as one bounded wright contract (normalize corrections before polish
   ones): build its read-set with
   `devrites-engine context --skills-root .omp/skills <slug> --phase polish --role slice-wright`, run the
   single-agent wave through `devrites-engine dispatch <slug> open|start|seal|return`
   (auto-records dispatch/return metrics; `open` passes `--claim-session <id>` and one
   `--claim <path>` per contract path, so the root-edit tripwire attributes its edits), and gate returned paths
   with `devrites-engine check diff-scope <slug> --allow <contract-paths>` before
   proof.
4. **If UI scope detected** read [`reference/ui.md`](reference/ui.md), and read
   `design-brief.md` if present so the polish follows the direction and states established
   by `devrites-ux-shape` and refined by `devrites-frontend-craft`. **Read the
   `## Visual Verdict` table in `browser-evidence.md` if present:
   its `FAIL` and `PARTIAL` rows are the normalize/quality-bar worklist**: identify the root
   cause of each (a missing state, an off-token CTA, or an anti-slop hit) rather than
   hiding it with decoration. Assess **Phase 3 (normalize)** → **Phase 4 (UI polish)**,
   and fold accepted UI
   corrections into step 3's single wright contract (the wright invokes the relevant craft skill). Honor argument modes:
   - `bolder | quieter | distill | harden`: passed to Phase 4 as the
     emphasis dial.
   - `normalize-only`: assess Phase 3 and stop (no Phase 4).
5. **Finish durable rollups before Review.** Apply the capability
   [`ledger`](reference/ledger.md) when requirements changed, the optional UI
   [`design memory`](reference/design-memory.md), and durable
   [`ADR promotion`](reference/adr-promotion.md). Add every changed project path
   to the candidate manifest and record each root-written ADR or `DESIGN.md` path the
   tripwire flags (`check candidate` names it) with `devrites-engine dispatch <slug> attribute --reason "polish rollup" --path <path>`;
   none of these writes waits for Ship.
6. **Re-prove and close.** After all accepted code/UI corrections and rollups,
   run `devrites-engine check candidate <slug>` and `devrites-engine check
   windows <slug>` — an unwaived deferral marker surfaces here, not at Seal.
   Any digest change requires
   affected real re-proof using the approved commands, fresh proof-runner
   validation, refreshed evidence/browser bindings, and an updated candidate
   manifest. Record a **`Re-verification:`** line in `polish-report.md`. Close
   the candidate for Review only after these checks are green. Then checkpoint
   remaining candidate diffs per
   [`checkpoint.md`](skill://rite-build/reference/checkpoint.md).
7. **Aggregate output:** each phase appends to the single `polish-report.md`.

## Refinement modes

Pass the requested UI direction to Phase 4. Modes do not bypass normalization or the
quality bar; they apply after the system is aligned. See `reference/ui.md`.

> **Mid-flight discipline.** When tempted to polish UI without normalize, cite
> clean lint as proof of quality, skip Phase 2 on a backend diff, or delete a
> Chesterton's Fence: see [anti-patterns](reference/anti-patterns.md).
