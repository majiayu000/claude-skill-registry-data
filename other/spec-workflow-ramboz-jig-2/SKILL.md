---
name: spec-workflow
description: >
  Drive the spec-driven lifecycle for any non-trivial work item: SPIDR-split a
  new spec into vertical slices, transition state markers (DRAFT → READY_FOR_REVIEW
  → READY_FOR_IMPLEMENTATION → IN_PROGRESS → REVIEWED → RECONCILED → DONE; also
  DEFERRED for parked slices with a stated resolution trigger), enforce the
  reconciliation checklist before commit, and surface stale specs/ADRs whose
  `last_verified` date has aged past dependency changes. Use when starting
  non-trivial new work, creating a spec, transitioning a slice's state,
  parking a slice as DEFERRED, reconciling a reviewed slice, or auditing
  doc freshness. Do not use for quick one-off fixes that don't need a spec,
  or for bug-shaped work where `jig:bug-fix` is the better fit.
user-invocable: true
---

> **Working posture ([ADR-0056](../../docs/decisions/adr-0056-adversarial-register-quarantine.md)).**
> Adversarial review is a *named, bounded operation.* This workflow invokes
> review passes (frame-critique / craft), whose skeptical register belongs
> *inside* those isolated reviewer subagents. Outside a review, default to
> collaborative and solution-forward; don't carry the adversarial stance into
> ordinary conversation.

> Spec 003 promoted this skill from stub to active. The deterministic state
> mutations live in `workflow.py`; this SKILL.md drives the judgment layer.

## What this skill does

- Guides SPIDR-splitting a new spec into vertical slices (Spike last, not first —
  try Rules / Data / Interface / Path first).
- Flags slices that look like horizontal phasing (no user-facing layer touched).
- Drives the spec lifecycle state transitions via `workflow.py`.
- Coordinates implementer + reviewer subagent invocations at the right points.
- Enforces the reconciliation checklist before a slice goes DONE.
- Consults `docs/memory/glossary.md` when drafting ACs to surface unknown domain terms.
- Surfaces skill-routing observability via `workflow.py routing-stats [--days N]` —
  a read-only histogram of which skills fired (jig baseline vs. richer/"other"
  skill per category) from `.claude/skill-usage.jsonl` (slice 041-02).
- Surfaces use-case coverage via `workflow.py coverage [--project-dir DIR]` — a
  read-only, **advisory** (non-blocking), project-wide **bidirectional** check
  (slice 068-03): a deterministic set-difference over the `use_cases:` trace
  links that reports use cases with no implementing spec (coverage gap) and
  specs citing no parent use case (scope creep). No-op when the project has no
  `## Use cases` section.
- Surfaces use-case progress via `workflow.py progress [--summary] [--project-dir DIR]` — a
  read-only, **advisory** rollup (slice 116-01, [ADR-0064](../../docs/decisions/adr-0064-use-case-progress-rollup-in-jig.md)):
  per use case, the specs citing it with their status and done/known slice
  **counts** (never percentages), then an **Unanchored** bucket for specs citing
  no resolvable use case. Derived on every run, stores nothing; a progress view,
  not a drift check. `--summary` prints the compact view `/jig:orient` copies
  (totals, use cases with no done slice or no spec, Unanchored specs; slice
  116-02). No-op when the project has no `## Use cases` section or its marker
  says `status: unfilled` / `skipped` (not elicited yet).
- Guards the status board via `workflow.py check-board <project-dir>` — a
  read-only audit that exits non-zero when `docs/specs/README.md` no longer
  matches the spec records, or when two spec directories claim one number.
  Writes nothing, so it is safe to run in CI against a checkout.
- Surfaces gate-bypass telemetry via `workflow.py gate-stats [--days N]` — a
  read-only per-gate histogram of how often each gate honored its env-var
  override (an override-frequency audit trail, not a gate-value verdict) from
  `.claude/skill-usage.jsonl` (slice 078-02).

## SPIDR splitting

All non-trivial specs are SPIDR-split into vertical slices before
implementation begins. **Spike is the last resort — try Path /
Interface / Data / Rules first.**

- **S — Spike**: research/learning activity. Only when none of P/I/D/R
  apply. AI agents default to spiking too eagerly — resist.
- **P — Path**: split by alternative paths through the story (happy
  path first, edge paths later).
- **I — Interface**: split by UI / platform / channel (minimal first,
  polish later).
- **D — Data**: split by data subset or format (less data first).
- **R — Rules**: split by business rules (simple first, edge cases later).

**Anti-horizontal-phasing rule:** every slice must touch the
user-facing layer and deliver end-to-end value. A slice that touches
only the DB or only the parser is horizontal phasing — re-split.

See [`worked-example-spidr-split.md`](worked-example-spidr-split.md)
for one applied example per axis plus a jig-native dogfood case (spec
017's three-axis split). The canonical primer for all five axes lives
at [`docs/spec-workflow/spidr-primer.md`](../../docs/spec-workflow/spidr-primer.md).

### Spike slices

When SPIDR's S axis fires during decomposition (none of P / I / D / R
apply because the team doesn't yet know enough to pick), the
resulting slice is marked `kind: spike` in its frontmatter — the
typed enum that `spec_lint.py` validates.

**When to introduce a spike during decomposition.** Reach for S only
after trying R / D / I / P. The bias to resist is "let me research
this first" as a prelude to "now let me build it as one big slab" —
that is horizontal phasing in a trench coat. If the spike would
conclude with "now ship the implementation," the implementation IS
the slice, and the research goes inside it.

**Body shape (four labelled blocks).** A `kind: spike` slice carries
four blocks alongside the standard Goal / DoR / AC / DoD scaffolding.
**Each label must be written with the trailing colon (`**Question:**`,
etc.) — that is what `spec_lint.py` matches against.**

- **Question:** — one sentence stating the open question. Set at DRAFT.
- **Time-box:** — explicit budget (e.g., "1 day", "4 hours"). Set at DRAFT.
- **Findings:** — bullet evidence collected during the spike. Filled
  during IN_PROGRESS.
- **Outcome:** — one of `ADR-NNNN created` / `spec NNN-NN unblocked` /
  `abandoned (reason)`. Multiple outcomes separated by `;`
  (e.g., `ADR-0007 created; spec 030-02 unblocked`). Set at DONE.

`spec_lint.py` soft-warns when a `kind: spike` slice is missing any of
the four labels — mid-flight spikes legitimately have empty Findings /
Outcome, so this is a warning, not a hard error.

**Always nested, never standalone.** Spike slices live inside a real
spec — never as a standalone `docs/spikes/` artifact. The
1-slice-spec case (no clear downstream spec yet, just an
investigation) collapses to "spawn a normal spec where the only slice
is `kind: spike`." This forces the investigator to articulate the
downstream change up front and keeps jig at two numbered families
(specs+slices, ADRs).

**Abandoned-spike manual-reshape failure mode.** When a spike's
Outcome is `abandoned (reason)`, dependents are NOT automatically
cascade-flagged. The human (or the next session) audits each
dependent slice and decides whether the original design still holds.
Automation here over-fires: "approach A abandoned" often means
"approach B from the same findings still satisfies the dependents."
`workflow.py` deliberately stays out of the cascade business; the
SKILL.md hand-off is the documented gate.

## How to use

### Creating a new spec

0. **Step 0 — confirm the project is scaffolded (spec 063 / ADR-0011).**
   BEFORE reserving a number or drafting ANY `docs/specs/` or slice
   structure, confirm this project is a scaffolded jig project. If it
   isn't, **route — do not hand-roll directories**:
   - **Greenfield** (no jig structure yet) → tell the user to run
     `/jig:scaffold-init`. It lays down conventions, templates, hooks, the
     status board, and a seed reference spec.
   - **Existing spec/`slices/` layout, but not jig-scaffolded** (no
     `scaffold.json`) → tell the user to run `/jig:migrate`. It adopts the
     existing layout into jig structure.

   You don't have to decide the state yourself: `workflow.py new` (step 2)
   **classifies and routes** for you (spec 063-01) — a `scaffold.json`-bearing
   project proceeds; a greenfield project is refused naming
   `/jig:scaffold-init`; an adoptable spec-driven project is refused naming
   `/jig:migrate`. The deterministic gate and this human-readable
   precondition agree by construction, so **don't restate the detection
   heuristic here** — run the helper and let it route. (Bypass for a
   deliberate out-of-band flow: `JIG_SCAFFOLD_PRECONDITION=0`.)

   **The anti-pattern this step exists to kill:** an auto-triggered
   `spec-workflow` run improvising a loose `slices/` folder (or any ad-hoc
   `docs/specs/` skeleton) because `/jig:scaffold-init` was skipped. That
   produces a non-jig layout that then needs migrating — exactly the
   reported failure. When in doubt, route to setup first; never invent the
   structure by hand.

1. Confirm the work needs a spec. Trivial fixes don't.
   - **Reference moved? Reframe first.** If a *load-bearing reference* changed
     from outside the system (a design system, vendor / API contract, test infra,
     compliance regime, platform, or product-positioning / strategic-vision
     shift), reach for `/jig:reframe` **before** drafting — re-baseline the corpus
     onto the new reference so you draft against it, not the dead premise (spec
     067 / [ADR-0024](../../docs/decisions/adr-0024-reference-reframe.md)).
1a. **Read the vision `## Use cases` section as framing — before drafting
   (spec 068-02 / [ADR-0025](../../docs/decisions/adr-0025-use-cases-breadth-layer.md)).**
   If the project's `docs/product-vision.md` carries a `## Use cases` section
   (the breadth-layer behaviors captured at init), **read it first** as framing
   context for this spec — *which captured behavior does this work serve?* The
   section is the shared frame specs anchor against; reading it before you draft
   is what keeps behavior-dense projects from each spec inventing its own slice
   of the world. (If there is **no** `## Use cases` section, the layer isn't
   adopted for this project — skip this step; nothing here applies.) You record
   the answer as a trace link in the spec's `use_cases:` frontmatter (step 2a).
1b. **Cross-check tracked bugs before drafting ACs.** For feedback/triage
   specs, read `docs/bugs/README.md` and any overlapping `docs/bugs/NNN-*.md`
   record before turning reported symptoms into acceptance criteria. If an
   item is a tracked defect with a bug record, route it through `bug-fix`
   (or link to that bug as an explicit dependency) instead of copying the
   defect into the spec as a second owner. Keep polish/design/new-behaviour
   items in the spec.
2. **Reserve the next free number on origin/main:**

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/spec-workflow/workflow.py" new <slug>
   ```

   The helper computes `max(NNN) + 1` across `docs/specs/`, writes a
   minimum stub `docs/specs/NNN-<slug>/spec.md` (frontmatter + Overview
   + SPIDR-analysis headers), commits it as
   `docs(specs): reserve NNN-<slug>`, and pushes to `origin/main`. If
   the push is refused by branch protection / permissions, the helper
   automatically falls back to a `reserve/NNN-<slug>` branch + `gh pr
   create`. This locks the number **team-wide** before any drafting
   begins, killing the parallel-worktree spec-number-collision failure
   mode logged across specs 014/015/016/017.

   **Works from any branch or worktree** (ADR-0015 / spec 051). The
   helper routes on the current branch: on `main` it runs the proven
   in-place flow (clean tree required, since the commit lands on local
   `main`); off `main` — a feature branch or a linked `.claude/worktrees/*`
   worktree — it builds the reservation commit in an *ephemeral detached
   worktree* checked out at `origin/main` and pushes it by SHA, never
   touching your branch, cwd, or working tree. You no longer need to
   switch to `main` (and a linked worktree can't, anyway).

   Flags: `--no-push` for solo machines without a remote, or for an
   off-main *provisional* reservation committed on the current branch
   (the number is local-view and may collide at merge — treat it as
   provisional); `--pr` to skip the direct-push attempt on
   protection-locked main.
2a. **Record the use-case trace link — and grow the vision on discovery
   (spec 068-02 / [ADR-0025](../../docs/decisions/adr-0025-use-cases-breadth-layer.md)).**
   The stub seeds an empty `use_cases:` frontmatter list. Fill it with the
   `UC-N` id(s) (from the vision `## Use cases` section, step 1a) this spec
   serves — the `dependencies:`-style flow-list shape, e.g.
   `use_cases: [UC-1, UC-3]`. This is the machine-resolvable trace link the
   reconcile-phase coverage check (slice 03) reads.

   **The discipline is soft — an empty/absent `use_cases:` never blocks a
   transition (AC4 / [ADR-0011](../../docs/decisions/adr-0011-spec-gate-model.md)).
   But it is not silent.** The trigger is **mechanical and deterministic** — the
   `classify_spec` predicate in
   [`skills/_common/use_cases.py`](../_common/use_cases.py) computes one of
   `no_section` / `empty` / `resolved` / `unresolvable` for this spec — **not** a
   voluntary "is this new?" self-report. **Whenever `classify_spec` returns `empty`
   or `unresolvable`** (the spec cites nothing, or cites a `UC-N` with no match
   in the vision) at draft/framing, surface a **three-path prompt** — every path
   is **one step** and **none blocks drafting**:

   - **(a) cite an existing use case** — this spec serves a behavior already in
     the vision: put its `UC-N` id(s) in `use_cases:`. Done.
   - **(b) grow the vision** — this spec serves a behavior **not yet captured**:
     **reuse `vision-elicitation`'s capture loop, seeded with the existing
     entries** (so the author sees the current set), → normalize → **confirm**,
     then **write additively** (append, never discard-and-replace) and **assign
     the next free `UC-N`** (`use_cases.next_use_case_id` allocates `max + 1`;
     retired numbers are never reused). The **confirm step guards grow quality**
     so a reachable trigger can't silently bloat the section: **(i)** enforce
     **goal-level grain** — reject spec-shaped / requirements-level phrasing,
     re-running slice 01's normalize (`"[actor] can [goal]"`); **(ii)** run a
     **near-duplicate check** against the seeded existing entries
     (`use_cases.is_near_duplicate`) — on an apparent match, **route back to
     path (a)-cite** rather than minting a duplicate. Then record the new id in
     `use_cases:`.
   - **(c) decline** — legitimately untraced (infra / refactor / no user-facing
     behavior) or defer: leave `use_cases: []`. The vision is unchanged, and any
     resulting gap is slice 03's advisory coverage backstop. No-op.

   **CRITICAL — the no-section no-op.** When `classify_spec` returns `no_section`
   (the project has **no** `## Use cases` section — the breadth layer is **not
   adopted**, e.g. a library or single-flow CLI), **the prompt is suppressed entirely**:
   nothing prompts and nothing errors. A project with specs but no use-case
   layer is wholly unaffected. The trigger fires **only** on `empty` /
   `unresolvable`, which presuppose the section exists.
3. Create `docs/specs/NNN-<slug>/{spec.md,plan.md,tasks.md}` with the conventional
   structure: status frontmatter, overview, SPIDR analysis, ordered slices.
4. SPIDR-split: for each slice, the goal is **one vertical piece** that delivers
   end-to-end value. Spike is the last resort, not the first reach.
5. Each slice is a whole-file document with the canonical frontmatter shape
   (`status`, `dependencies`, `last_verified`) plus DoR / AC / DoD / Close-out
   sections. `workflow.py new` (step 2) already emitted a well-formed starter
   `slice-01-tbd.md` from the packaged slice template, so you never hand-resolve
   a template path; add any further slices in that same shape. For the
   **structural reference** — what a filled-in slice looks like — mirror the
   in-project worked example that scaffolding installs at project root:
   `docs/specs/001-adopt-jig/` (`spec.md` + `slice-01-bootstrap.md`), the first
   spec, which your project's `CLAUDE.md` names as the worked example to
   imitate. Set `status: DRAFT` in the frontmatter. Legacy slices that use prose
   `**STATUS: DRAFT**` markers still work (lazy migration); no need to rewrite
   them.
5a. **Design-fidelity authoring nudge (spec 104-02 / ADR-0049).** When a
   slice you just wrote in step 5 ships **visual design** (a mockup, a design
   system spec, a screen with colours/spacing/sizes/layout rules to hit),
   don't let "doesn't match the mockup" live only in a picture:
   - **(a) Extract the design values into checkable ACs.** Pull the concrete
     values — colours, spacing, sizes, layout rules — out of the mockup and
     write them as this slice's acceptance criteria, the same way any other
     observable behavior becomes an AC. This is what turns a fuzzy "looks
     right" into something a reviewer (or an eval) can actually check.
   - **(b) When fidelity must *gate*, wire the servo rail.** If a screen's
     visual fidelity needs to be a hard, enforced condition of `DONE` — not
     just an eyeballed check — set `design_review: true` in the slice
     frontmatter and wire a servo `design-eval` (screenshots the running app
     against the reference, scores it with a pinned vision judge) as the
     done-condition. `design_review: true` is attested, read-only, at
     `REVIEWED` by spec 071's design-review pass (the deriver
     `slice_needs_design_review` in `workflow.py` reads the flag) — jig never
     re-derives the eval score itself.

   **Graduated, not mandatory — jig offers, never forces, servo.** Not
   every screen earns a frozen eval:
   - **Low-stakes visual polish** → design-values-in-ACs plus
     attest-by-eyeball at review time is enough; no servo `design-eval`
     required.
   - **A hard fidelity gate** (fidelity must not regress, or is a stated
     product requirement) → servo `design-eval` + `design_review: true`.

   Pick the tier that matches the stakes; when in doubt, start with (a) and
   add (b) only when eyeballing genuinely isn't enough. See
   [spec 071](../../docs/specs/071-design-review-pass/spec.md) and
   [ADR-0049](../../docs/decisions/adr-0049-design-fidelity-routing-to-originating-spec.md)
   for the full routing rationale; this step adds no new mechanism — teeth
   stay anchored to the existing `design_review` flag.
6. **Ground your factual claims (spec 064-02 / ADR-0020 §1–§2).** Any
   load-bearing factual claim about a *runnable* surface — library/API
   capability, version/perf behavior, behavior of existing code — must be
   backed by an **executed probe** (run the command, read the source /
   `node_modules`) or a citation. **A universal or negative claim** ("the
   only", "never", "always", "one-way", "nothing reads", "otherwise clean")
   is established by an ***enumeration*** — a search you can show returns the
   *complete* set — **not a single positive citation** ([ADR-0052](../../docs/decisions/adr-0052-grounding-enumeration-for-universal-claims.md)):
   one true example proves nothing about the rest of the set, and these are the
   highest-value claims a future reader relies on. To claim enumeration, **state
   why the search is exhaustive** — what closes the set so nothing escapes.
   Some sets are closed by syntax and this is easy (imports in a package,
   call-sites in a repo); many only *look* `grep`-bounded — a "nothing reads
   this" search misses dynamic / reflective / ORM / string-built / config-wired /
   codegen'd / cross-repo access (illustrative, **not a checklist to clear**: the
   burden is to show the search captures every member, not to rule out named
   escapes). When you cannot show the search is exhaustive, an **empty result is
   absence of evidence, not an enumeration**: weaken the claim, tighten the
   boundary until the search genuinely closes the set, or move it to
   `## Assumptions`. Never dress an empty search as an enumeration — the
   frame-critique reviewer treats "I searched and it was empty" as *un*grounded
   until you have shown what closes the set. Everything you cannot verify goes in
   the spec stub's risk-gated `## Assumptions` section, marked explicitly — never
   asserted as fact. This **makes mandatory + derived** the existing informal
   "Current state (verified …)" discipline that the 064-01 retro found jig
   already half-practices by hand: it was grounding-by-probe all along, just
   reliant on author diligence. The `## Assumptions` you surface here has
   downstream value — slice 064-04 derives the `frame_review` trigger
   mechanically from it, so honest framing now is what decides later whether
   the adversarial frame-critique pass fires. The section is risk-gated: write
   "None" / omit when there are no unverified load-bearing assumptions; don't
   pad with boilerplate. (For a worked example of marked assumptions plus
   probe-grounded claims, see [ADR-0020](../../docs/decisions/adr-0020-spec-frame-hardening.md)
   `## Assumptions` A1–A4 + `## Kill criteria`, and the
   [spec 064-01 retro](../../docs/specs/064-spec-frame-hardening/retro.md),
   which probe-verified its three most load-bearing claims before recording
   them.)
7. **Let the assumptions decide `frame_review` (spec 064-04 / ADR-0020).**
   You are **not** asked "is frame-review needed?" — the `## Assumptions` you
   just surfaced decide it, mechanically. Set the slice's `frame_review` flag
   from `workflow.py frame-review-needed`:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/spec-workflow/workflow.py" \
     frame-review-needed "docs/specs/NNN-<slug>/spec.md" "<slice-fragment>"
   ```

   The rule is a derivation, not a judgment call: `true` iff the slice's
   `## Assumptions` section carries ≥1 real (non-placeholder) assumption —
   so honest framing in step 6 is exactly what fires (or silences) the
   adversarial frame-critique pass. An inline-mirror / refactor slice with
   no unverified assumptions (`## Assumptions` absent or just "None") stays
   default-off. **ADRs are always-on** (OQ3): any ADR gets `frame_review:
   true` unconditionally — the deriver returns `true` for any `adr-*.md`
   path. When the value is `true`, set `frame_review: true` in the slice
   frontmatter so the gate + `session-plan` dispatch the pass.
8. Add rows to `docs/specs/README.md` (or regenerate via `workflow.py status-board`).

### Picking up a slice

1. Read the automatic `jig hint:` project-orientation headline injected at
   `SessionStart`, or refresh it manually before choosing work:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/spec-workflow/workflow.py" orient \
     --project-dir .
   ```
   The headline is computed from `scaffold.json` and lifecycle artifacts. Treat
   `docs/architecture.md`, the spec corpus, and the status board as authoritative;
   a shallow source-tree listing is not evidence that a scaffolded project is
   greenfield or that recorded stack decisions are absent.
2. Check `docs/specs/README.md` for the next slice in `READY_FOR_IMPLEMENTATION`
   (or `DRAFT` for a slice you intend to plan now).
3. Run:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/spec-workflow/workflow.py" transition \
     "docs/specs/NNN-<slug>/spec.md" "<slice-fragment>" IN_PROGRESS
   ```
   **Claim-on-working-state (spec 049-01, amended by
   [ADR-0045](../../docs/decisions/adr-0045-slice-claim-covers-active-lifecycle.md)).**
   On a frontmatter (file-per-slice) slice, a transition into a **working
   state** — `READY_FOR_REVIEW` / `IN_PROGRESS` / `REVIEWED` / `RECONCILED` —
   stamps `claimed_by:` (the current branch name, or `JIG_CLAIM_ID`), so
   spec-level work is marked too, not just implementation. Entering a **release
   point** clears it: the two pickup-queue states `DRAFT` /
   `READY_FOR_IMPLEMENTATION` (step 2 above tells you to choose work from
   exactly those, so a leftover owner there would mark a free slice as
   occupied), plus the terminal `DONE` / `DEFERRED` / `ABANDONED`.

   It **refuses** only when the slice is already `IN_PROGRESS` under a
   *different* identifier and you are moving it to `IN_PROGRESS` (naming the
   holder, pointing at `--release`); any other foreign claim — on your copy or
   on `origin/main` — is a loud **non-blocking warning**, because two sessions
   working one spec can be legitimate. The claim is **local by default**; add
   `--push` (direct) or `--pr` (via PR) to reserve it on `origin/main` so other
   worktrees see it, at any working state, though only an `IN_PROGRESS`
   reservation also publishes `status:` there (race / protected-branch handling
   mirrors `workflow.py new`). At a working state that reservation is
   **best-effort** (for a target other than `IN_PROGRESS`): if the trunk copy is
   already `status: IN_PROGRESS` under someone else's claim or none, it warns and
   pushes nothing, because that state is what the start-of-build guard
   hard-blocks on — stamping a claim over it would move a live lock, or
   manufacture the enforced pair on an unclaimed copy. Your own trunk claim just
   reports a benign no-op. To force-release a stale claim: `transition
   <spec> <slice> <state> --release --reason "<why>"` (clears `claimed_by:`,
   logs to `## Release log`).

   **Class-A cross-ref guard (spec 112 / ADR-0058).** A transition into a
   working state is *refused* when the slice is already `DONE` on `origin/main`
   — a stale branch re-advancing already-integrated work. The `→ IN_PROGRESS`
   case is caught by the start-collision guard (spec 051-04); the other working
   states (`READY_FOR_REVIEW` / `REVIEWED` / `RECONCILED`) by
   `_refuse_integrated_advance`, which reads the shared
   `cross_ref_state.identifier_state_on_ref` primitive. For a sanctioned re-open
   / supersession of integrated work, pass **`--reopen`** (a first-class,
   audited bypass distinct from the blanket `JIG_CROSSREF_GATE=0`); the
   `→ IN_PROGRESS` path's own escape remains `JIG_START_COLLISION_GATE=0`
   (convergence tracked in `docs/refinement-todo.md`). Unreachable `origin/main`
   → non-blocking warning, transition proceeds.

   **Do not read a blank `claimed_by:` as "free".** It means *no claim is
   recorded*: claims are local unless pushed, so another worktree's unpushed
   claim is invisible, and a plain `Edit`-tool write to a slice takes no claim
   at all. A claim that IS present names the session that last *moved* the
   slice into a working state — a presence hint, not a live lock. When it
   matters, ask rather than assume — see
   [bug 014](../../docs/bugs/014-slice-claim-covers-only-in-progress.md).
4. Fill in / refresh `plan.md` and `tasks.md` for the slice.
5. Spawn the `implementer` subagent with the spec path. Prefix the Task prompt
   with `[jig:phase=implementation] [jig:spec=NNN] [jig:slice=NNN-NN]` so
   `jig-telemetry.sh` can attribute implementation-phase cost. Implementer
   writes the deliverable to disk (TDD — failing tests first).

### After implementation

Slices 031-01 + 031-02 + 060-05 wired a **multi-pass review flow** into the
post-implementation step. Every slice runs through two passes before the
`IN_PROGRESS → REVIEWED` transition; two further passes fire on demand —
the **arch** pass when the slice declares `arch_review: true`, and the
**code-health** pass when it declares `code_health_review: true`.

The orchestrator runs the passes in this order:

1. **Compliance pass — `jig:independent-review`** (always). Spawn the
   `reviewer` subagent against the deliverable using the prompt built by
   `review.py implementation`. Reviewer is read-only; it evaluates each
   acceptance criterion and returns
   `pass | fail | needs-changes`.

2. **Craft pass — `pr-review`** (always). After the compliance pass
   returns, build the craft-pass prompt with `review.py pr-review` and
   spawn a second `reviewer`-shaped subagent. The reviewer is read-only
   (Read/Glob/Grep, **no `Skill` tool**), so it cannot route to a skill
   via Claude's skill router; instead `review.py` hands it a concrete
   richer-skill path to read-and-apply, falling back to jig's inlined
   baseline buckets (scope / blockers / nits / strengths). The pass
   returns the same `VERDICT / REASONING / SPECIFIC ISSUES /
   RECONCILIATION NOTES` envelope as the compliance pass, with
   SPECIFIC ISSUES entries tagged `[blocker]` / `[nit]` / `[strength]`.

   **Select the richer skill first (spec 096-03 / ADR-0040 D3).**
   `--richer-skill` is a **required** argument on `pr-review` (and `arch-review`
   / `code-health`). Before building the craft prompt:
   - **Run the candidate step:** `review.py candidates pr_review
     "docs/specs/NNN-<slug>/spec.md" "<slice-fragment>" --pass craft`. It
     prints a **tiered** list — `[high-confidence]` (with descriptions) and
     `[speculative]` (names only) — and writes the shown set to a sidecar.
   - **Pick the single best HIGH-CONFIDENCE candidate** for the category and
     pass it as `--richer-skill <name>`. If several are genuine, **pick one —
     do not refuse**; the alternatives are recorded as the shown-and-declined
     set. If none fits, pass `--richer-skill none` for jig's baseline.
   - **The pick is a heuristic, not a guarantee** — an explicit
     `review.<category>_skill` in `scaffold.json` (096-01) **overrides** it, and
     `candidates` never picks for you (a `[speculative]` false positive like a
     briefing skill must not be selected on lexical grounds alone).
   - **CI / no orchestrator:** pass `--richer-skill none --non-interactive`;
     config remains the reproducible path. Omitting `--richer-skill` entirely,
     or invoking a pass with no sidecar + no config + no `--non-interactive`,
     **fails fast** (naming the missing `candidates` step) rather than silently
     using the baseline.

3. **Arch pass — `arch-review`** (on-demand). Before running this pass,
   query the slice's `arch_review:` frontmatter flag via
   `workflow.py arch-review-needed`. When the helper prints `true`,
   build the arch-pass prompt with `review.py arch-review` and spawn a
   third `reviewer`-shaped subagent. The pass produces the four
   canonical arch buckets (summary / strengths / concerns / open
   questions) wrapped in the same verdict envelope, using the same
   candidate-channel resolution as the craft pass (096-03): run
   `review.py candidates arch_review …`, pick the best, pass `--richer-skill`;
   config (`review.arch_review_skill`) overrides, else jig's baseline buckets
   are inlined. When the helper prints `false`, skip this
   pass entirely. Slice authors flip the flag by uncommenting the
   `arch_review: true` line in the slice template's frontmatter — set
   it when the slice changes module boundaries, public contracts, or
   architecture-shaped concerns.

4. **Code-health pass — `jig:code-health`** (on-demand, **gated**). Before
   running, query the slice's `code_health_review:` frontmatter flag via
   `workflow.py code-health-review-needed`. When it prints `true`, **run
   `health.py` yourself** (the orchestrator / CI), capture its tight
   summary, and feed THAT summary into `review.py code-health … --summary-file`
   (`--summary-file -` to pipe it in). Then spawn a `reviewer`-shaped subagent. **The reviewer
   is read-only (Read/Glob/Grep, no Bash) — it must NOT run `health.py`;
   it judges the summary you provide.** The reviewer renders the judgment a
   tool can't: is duplication within the [ADR-0002](../../docs/decisions/adr-0002-extract-helper-on-third-caller.md)
   inline-mirror budget? is a complex function inherent or fixable? are
   the lint findings worth blocking on? The pass returns the same verdict
   envelope, with SPECIFIC ISSUES tagged `[blocker]` / `[nit]` /
   `[strength]`. **Why gated, not always-on:** [ADR-0017](../../docs/decisions/adr-0017-scaffolded-code-health.md)
   flags the per-slice review cost (specs 055/057 context-cost discipline)
   and recommends gating it like arch-review — so it defaults off and slice
   authors opt in with `code_health_review: true`. The evidence file is
   `reviews/slice-NN-code-health.md`.

When spawning any reviewer Task above, prefix the Task prompt with telemetry
tags before the `review.py` body: `[jig:phase=<phase>] [jig:spec=NNN]
[jig:slice=NNN-NN]`. Use `compliance` for `review.py implementation`,
`craft` for `pr-review`, `arch` for `arch-review`, `code-health` for
`code-health`, and `reconciliation` for the final reconciliation review.

**Block rule for the REVIEWED transition.** All required passes
(compliance + craft, plus arch when `arch_review: true`, plus code-health
when `code_health_review: true`) must pass before
`transition <slice> REVIEWED`:

- Any `fail` verdict from any pass blocks the transition.
- `needs-changes` from the compliance pass blocks (the implementer
  addresses findings and re-runs).
- `needs-changes` from the craft pass does NOT block — the
  `[nit]`-tagged entries become reconciliation-log items (the
  implementer captures them in the deviation log during reconciliation).
  Only `[blocker]`-tagged entries from the craft pass block the
  transition.
- The arch pass follows the same rule as the craft pass:
  `[blocker]`-tagged entries block; `[nit]`-tagged entries and
  `needs-changes` become reconciliation-log items.
- The code-health pass follows the same rule: `[blocker]`-tagged entries
  block the `REVIEWED` transition; `[nit]`-tagged entries become
  reconciliation-log items.

**Measurement tag (non-gating).** The craft/arch/code-health passes also
self-classify each SPECIFIC ISSUES entry `[spec]` (an acceptance-criteria /
spec-frame issue a smarter clarify pass could have prevented) or `[impl]`
(implementation-discipline — untested edge, brittle fixture, drift). This
carries no gating consequence — it exists purely so a future rollup can
count `[spec]`-tagged themes across specs (docs/refinement-todo.md
"Instrument the review→learnings→clarify loop before building it").

**The gate is mechanical, not advisory (slice 045-03 / [ADR-0014](../../docs/decisions/adr-0014-review-evidence-model.md) §5).**
`workflow.py transition` now *refuses* the `REVIEWED` / `RECONCILED` /
`DONE` moves unless the required review evidence — recorded with
`review.py record-review` as `docs/specs/NNN-<slug>/reviews/slice-NN-<pass>.md`
— exists and clears (`verdict: pass`). `REVIEWED` requires
`compliance` + `craft` (+ `arch` when the slice declares
`arch_review: true`, + `code-health` when it declares
`code_health_review: true`); `RECONCILED` requires the `reconciliation` verdict
**and** `### Deviation log` plus `### Reconciliation sweep` subsections;
`DONE` re-validates the post-implementation and reconciliation evidence set
(in addition to the existing `dependencies:` check). A refusal names
the missing/invalid artifact and the `record-review` command to produce
it. The gate enforces *evidence consistency*, not human sign-off (it
lives in the agent's trust boundary per [ADR-0011](../../docs/decisions/adr-0011-spec-gate-model.md)).
Bypass it for a deliberate out-of-band flow by setting
`JIG_REVIEW_EVIDENCE_GATE=0` (also `false`/`off`/`no`) — the status still
transitions and the `DONE` dependency check still runs; only the evidence
check is skipped.

After all required passes pass:

4. Address any reviewer findings, adding regression tests for any real
   bugs found.
5. **Record each pass's verdict** as durable evidence with
   `review.py record-review` (writes
   `docs/specs/NNN-<slug>/reviews/slice-NN-<pass>.md` — see the
   independent-review SKILL.md § "Recording and checking review
   evidence"). The `REVIEWED` transition is gated on this evidence, so it
   is not optional.
6. Transition: `transition <spec.md> <slice> REVIEWED`. The gate
   re-validates the recorded `compliance` + `craft` (+ `arch`,
   + `code-health`) verdicts before the status flips (and before the
   003-04 auto-tick).

**Recovering from a failed review.** A `fail`/`needs-changes` verdict — or
a `[blocker]`-tagged craft/arch finding, which is recorded as a non-`pass`
verdict — blocks the `REVIEWED` transition. To recover: address the
findings, re-run the pass against the updated deliverable, `record-review`
the new verdict (it **overwrites in place** the earlier file for that
`(slice, pass)`; git history keeps the prior one), then re-run
`transition … REVIEWED`. With every required pass now `pass`, the gate
clears. A non-`pass` artifact never overwritten by a later `pass` keeps
blocking — the "superseded without a later pass" case (ADR-0014 §4).

**When a review retracts a *claim*, sweep the corpus before re-recording.**
The recovery above is written for a code-shaped finding, which is local to one
file. A finding about **content** is not: a retracted assertion is usually
copied by design into `CHANGELOG.md`, the slice record, the inbox, and
cross-referenced docs. Fixing only the reviewed deliverable leaves the
retracted version authoritative in every **sibling** artifact — and the stale
copy is frequently the one the next session reads first (the project's own
rules make `CHANGELOG.md` a read-before-you-fix record), so the pass re-fails
round after round on a document you never touched. Before you `record-review`
the new verdict, **grep the retracted phrasing across the docs root and
`CHANGELOG.md`, and reconcile every hit** — the plain sweep is what reaches
the changelog, the inbox, and arbitrary cross-referenced files. Within the
spec itself, `/jig:analyze` is the structured complement: its **Duplication**
and **Terminology Drift** categories catch a retracted claim surviving across
the spec's own slice files and the docs it cross-references (`product-vision`,
accepted ADRs, the glossary, `architecture.md`) — but it audits one spec's
files plus that fixed set, not the whole corpus, so it sharpens the sweep
rather than replacing it. Distinguish **surviving** assertions (the claim
still stated as true — must fix) from **explicit** retractions (the claim
named as withdrawn in a changelog or history entry — correct, and worth
keeping).

```bash
# Compliance pass (always)
PROMPT=$(python3 "${CLAUDE_PLUGIN_ROOT}/skills/independent-review/review.py" \
  implementation "docs/specs/NNN-<slug>/spec.md" "<slice-fragment>" \
  "<deliverable-path-1>" ...)
SUBAGENT=$(python3 "${CLAUDE_PLUGIN_ROOT}/skills/independent-review/review.py" \
  subagent-type implementation)
# … feed "[jig:phase=compliance] [jig:spec=NNN] [jig:slice=NNN-NN]\n\n$PROMPT"
# … to Task with subagent_type: $SUBAGENT, wait for pass …

# Craft pass (always) — spec 096-03: select the richer skill first.
# 1. Show the tiered candidates + write the sidecar:
python3 "${CLAUDE_PLUGIN_ROOT}/skills/independent-review/review.py" \
  candidates pr_review "docs/specs/NNN-<slug>/spec.md" "<slice-fragment>" \
  --pass craft
# 2. Read the [high-confidence] tier, pick the single best (or `none`), then
#    build the prompt with the REQUIRED --richer-skill (config overrides it):
PROMPT=$(python3 "${CLAUDE_PLUGIN_ROOT}/skills/independent-review/review.py" \
  pr-review "docs/specs/NNN-<slug>/spec.md" "<slice-fragment>" \
  "<deliverable-path-1>" ... --richer-skill "<name-or-none>")
SUBAGENT=$(python3 "${CLAUDE_PLUGIN_ROOT}/skills/independent-review/review.py" \
  subagent-type pr-review)
# … feed "[jig:phase=craft] [jig:spec=NNN] [jig:slice=NNN-NN]\n\n$PROMPT"
# … to Task with subagent_type: $SUBAGENT, wait for pass …
# (CI / no orchestrator: --richer-skill none --non-interactive.)

# Arch pass (only when slice frontmatter has `arch_review: true`)
# IMPORTANT: capture the helper exit code — a non-zero exit means the
# slice lookup failed (missing spec / unknown fragment / ambiguous),
# not "no arch pass needed." Surface the error rather than silently
# skipping the pass.
if ! NEED_ARCH=$(python3 "${CLAUDE_PLUGIN_ROOT}/skills/spec-workflow/workflow.py" \
    arch-review-needed "docs/specs/NNN-<slug>/spec.md" "<slice-fragment>"); then
  echo "arch-review-needed failed — aborting" >&2
  exit 2
fi
if [ "$NEED_ARCH" = "true" ]; then
  # 096-03: show candidates for arch_review, then pick (config overrides).
  python3 "${CLAUDE_PLUGIN_ROOT}/skills/independent-review/review.py" \
    candidates arch_review "docs/specs/NNN-<slug>/spec.md" "<slice-fragment>" \
    --pass arch
  PROMPT=$(python3 "${CLAUDE_PLUGIN_ROOT}/skills/independent-review/review.py" \
    arch-review "docs/specs/NNN-<slug>/spec.md" "<slice-fragment>" \
    "<deliverable-path-1>" ... --richer-skill "<name-or-none>")
  SUBAGENT=$(python3 "${CLAUDE_PLUGIN_ROOT}/skills/independent-review/review.py" \
    subagent-type arch-review)
  # … feed "[jig:phase=arch] [jig:spec=NNN] [jig:slice=NNN-NN]\n\n$PROMPT"
  # … to Task with subagent_type: $SUBAGENT, wait for pass …
fi

# Code-health pass (only when slice frontmatter has `code_health_review: true`)
# The orchestrator runs health.py and feeds its summary IN — the read-only
# reviewer never runs the tool (no Bash).
if ! NEED_CH=$(python3 "${CLAUDE_PLUGIN_ROOT}/skills/spec-workflow/workflow.py" \
    code-health-review-needed "docs/specs/NNN-<slug>/spec.md" "<slice-fragment>"); then
  echo "code-health-review-needed failed — aborting" >&2
  exit 2
fi
if [ "$NEED_CH" = "true" ]; then
  # Run the jig:code-health runner yourself (health.py check .) and capture
  # its tight summary to /tmp/health-summary.txt — the read-only reviewer
  # MUST NOT run it. (The runner ships with the Tier-1 jig:code-health skill;
  # if it isn't installed, note "summary unavailable" and judge on the
  # deliverables.)
  # 096-03: show candidates for code_health, then pick (config overrides).
  python3 "${CLAUDE_PLUGIN_ROOT}/skills/independent-review/review.py" \
    candidates code_health "docs/specs/NNN-<slug>/spec.md" "<slice-fragment>" \
    --pass code-health
  PROMPT=$(python3 "${CLAUDE_PLUGIN_ROOT}/skills/independent-review/review.py" \
    code-health "docs/specs/NNN-<slug>/spec.md" "<slice-fragment>" \
    "<deliverable-path-1>" ... --summary-file /tmp/health-summary.txt \
    --richer-skill "<name-or-none>")
  SUBAGENT=$(python3 "${CLAUDE_PLUGIN_ROOT}/skills/independent-review/review.py" \
    subagent-type code-health)
  # … feed "[jig:phase=code-health] [jig:spec=NNN] [jig:slice=NNN-NN]\n\n$PROMPT"
  # … to Task with subagent_type: $SUBAGENT, wait for pass …
fi
```

### Reconciliation (REVIEWED → RECONCILED)

Walk the **Reconciliation checklist** below. Every item is a gate.

### Closing the slice

1. After the reconciliation review passes, **record its verdict** with
   `review.py record-review … --pass reconciliation`, then
   `transition <spec.md> <slice> RECONCILED`. That move is gated on the
   recorded `reconciliation` verdict (`pass`) **and** `### Deviation log`
   plus `### Reconciliation sweep` subsections under the slice heading
   (ADR-0014 §5 + ADR-0029).
2. Commit the work.
3. After commit: `transition <spec.md> <slice> DONE`. `DONE` re-validates
   the whole evidence set — `compliance` + `craft` (+ `arch`,
   + `code-health`) + `reconciliation` — plus the deviation log and
   reconciliation sweep, on top of the existing
   `dependencies:` check.
4. Regenerate the board: `workflow.py status-board <project-dir>`.
5. Run `/jig:memory-sync` (or `memory.py`) to consolidate any new learnings.

**Before landing, audit the board.** `docs/specs/README.md` is derived — every
column is computed from the spec records, and the curated Notes column is
carried across regens — so it is regenerated, never hand-edited. A merge
conflict on it is resolved by re-running `status-board`, not by picking a side:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/spec-workflow/workflow.py" \
  check-board <project-dir>
```

Read-only; exits non-zero on either problem it can find. **Stale board** — the
spec records changed and `status-board` wasn't re-run. **Duplicate spec
number** — two spec directories claim one number, which is what parallel
branches produce when the number was never reserved on the trunk. The renderer
emits both without complaint and a staleness check can't see it (both *are*
faithfully derived), so it needs its own detector; the message names both
directories so you know which to renumber.

Notes-column text is not drift — it is hand-written by design and survives
regen. What *is* drift is any other cell edited by hand: it will be overwritten
on the next regen, so change the slice record instead.

## Spec lifecycle states

```
DRAFT → READY_FOR_REVIEW → READY_FOR_IMPLEMENTATION → IN_PROGRESS
  → REVIEWED → RECONCILED → DONE

         DEFERRED ⇄ DRAFT   (parked slices with a stated resolution trigger)
         ABANDONED ⇄ DRAFT  (permanently dropped slices, pre-DONE only)
```

Status transitions are mutations on either `spec.md`'s frontmatter `status:`
field (new convention, slice 015-01) or the prose `**STATUS: ...**` line
(legacy — still supported via lazy migration), AND the matching row in
`docs/specs/README.md`. Use `workflow.py transition` for the spec mutation
and `workflow.py status-board` to re-sync the board.

**Spec-level `status:` is derived, not authored** (slice 030-01; widened by
slice 085-01). The frontmatter `status:` at the top of each `spec.md`
overview file is computed by `compute_spec_status(spec_path)` from its
slices: `DONE` when every slice, excluding `DEFERRED`/`ABANDONED` ones, is
DONE (a mix of `DONE` + `DEFERRED` and/or `ABANDONED` still rolls up to
`DONE`); `ABANDONED` when every slice is `ABANDONED` (the spec's entire
scope was dropped); `DRAFT` when no slices exist, every slice is
`DEFERRED`, every non-`DEFERRED` slice is `DRAFT`, or the only non-`DONE`
slices are a `DEFERRED`+`ABANDONED` mix with no live work; otherwise
`IN_PROGRESS`. The rollup write happens automatically inside `workflow.py
transition` (after the slice mutation) and inside `workflow.py
status-board` (during regen). Don't set `spec.md`'s `status:` by hand —
it'll be overwritten on the next transition or regen anyway.

### DEFERRED state

A slice is `DEFERRED` when scoped but parked — the work is identified but
not the current priority. Different from `DRAFT` which means "not yet
fleshed out." Transitions:

- Any state → `DEFERRED` is allowed.
- `DEFERRED` → `DRAFT` (re-open) is allowed.
- `DEFERRED` → any other state is **refused** — re-open via DRAFT first
  so review gates aren't silently skipped. This is the first
  FROM-state-restricted transition in jig's lifecycle.

When transitioning a slice to `DEFERRED`, add a `**Resolution trigger:**`
line in the slice body (same convention `docs/refinement-todo.md` uses).
The status-board renders deferred slices in a separate `## Deferred slices`
section with that trigger as the per-row context.

### ABANDONED state

A slice is `ABANDONED` when it's permanently dropped — scoped, sometimes
even fully specced, and deliberately decided against with no intent to
ever resume. Different from `DEFERRED`, which means "parked, with a stated
resolution trigger that will resurface it." Added in slice 085-01 (filed as
[GitHub issue #72](https://github.com/ramboz/jig/issues/72)). Transitions:

- Any **pre-`DONE`** state → `ABANDONED` is allowed.
- `DONE` → `ABANDONED` is **refused** — "never attempted" and "shipped,
  then deliberately removed" are different events with different audit
  value; overloading one bucket for both would erase that distinction
  where an auditor most needs it (see spec 085 Non-goals). Un-shipping
  already-`DONE` work is a different, unbuilt concept.
- `ABANDONED` → `DRAFT` (re-open) is allowed.
- `ABANDONED` → any other state is **refused** — re-open via DRAFT first,
  mirroring `DEFERRED`'s restriction.

When transitioning a slice to `ABANDONED`, add a `**Abandonment reason:**`
line in the slice body (same convention shape as `**Resolution
trigger:**`). The status-board renders abandoned slices in a separate
`## Abandoned slices` section with that reason as the per-row context.
The transition also prints a one-time, non-blocking warning naming any
other slice, anywhere in the project, whose `dependencies:` names the
now-abandoned slice and whose own status isn't already `DONE`/`ABANDONED`
— advisory only, it never blocks the transition, modifies the dependent,
or cascades (a human decides what a live dependent should do next).

### Slice frontmatter (slice 015-01 convention, file shape per 018-03)

New slices are whole-file templates — frontmatter at the top, `## Slice ...`
heading immediately following the closing frontmatter delimiter. `workflow.py
new` emits a starter `slice-01-tbd.md` alongside `spec.md` in this
shape (from the packaged slice template); for a filled-in reference, mirror the
scaffolded worked example `docs/specs/001-adopt-jig/slice-01-bootstrap.md`.
Legacy specs that embed `## Slice` sections inside `spec.md`
(heading-first, frontmatter-after) remain supported by every helper —
no forced migration.

```yaml
---
status: DRAFT
dependencies: [007-02, adr-0004]
last_verified:
---
```

- `status` — current lifecycle state. `workflow.py transition` updates
  this when present.
- `dependencies` — flow-style list of slice fragments (e.g. `007-02`)
  and ADR IDs (e.g. `adr-0004`). `transition <slice> DONE` refuses if
  any listed dependency is not DONE / accepted.
- `last_verified` — date the slice was last reconciled. `transition`
  stamps this automatically on `→ RECONCILED`. Used by `stale`.

Legacy slices using prose `**STATUS:**` markers still work — the
transition helper writes to whichever shape is present. No retroactive
mass migration; new slices use the template, old slices stay as-is.

## Reconciliation checklist

When a slice transitions `REVIEWED → RECONCILED`, walk this checklist before the
status flip is allowed. Each item is a gate.

- [ ] **Deviation log** — write what changed during implementation and why,
      under a "Deviation log (after reconciliation)" subsection of the slice
      in `spec.md`. Original ACs preserved above; deviations append, not overwrite.
- [ ] **Reconciliation sweep** — write which drift-prone surfaces were checked,
      using `updated` / `no-op` / `deferred` dispositions. The transition gate
      checks the subsection exists; the reconciliation reviewer judges coverage
      and rationale quality.
- [ ] **Leanness sweep** — did the implementation over-build? Confirm nothing
      was added beyond what the acceptance criteria required — no
      over-engineering, premature abstraction, or speculative generality
      (indirection, config knobs, or extension points with no current caller).
      Anchored to the spec's needs (added-beyond-need), never a push to strip
      behavior the spec required. Complements the arch-pass leanness lens (spec 109). Non-blocking
      nudge; not a gate.
- [ ] **Lightweight decisions** — did this session's review or implementation
      settle any non-spec decisions (UI strings, visual choices, translation
      corrections, scoped brand/icon calls)? If yes, record them in
      `docs/decisions/lightweight-decisions.md`. (Non-blocking nudge; not a gate.)
- [ ] **Architecture impact** — did module boundaries or public contracts change?
      If yes, update `docs/architecture.md` AND write an ADR. **Ground what you
      write (ADR-0020 §1, same rule as spec-authoring step 6).** Reconciliation
      rewrites long-lived front-door prose that everyone reads and nobody
      re-derives, so any load-bearing factual claim about a runnable surface —
      library/API capability, version/perf behavior, behavior of existing code —
      must be backed by an executed probe or a `file:line` citation. Anything you
      cannot verify is marked as an assumption, never asserted as fact. (A prose
      claim naming a code symbol but citing no line is a candidate warning.)
- [ ] **Load-bearing decision (ADR trigger, judgment)** — beyond a boundary
      change, was a load-bearing design choice with rejected alternatives made?
      Canonical wording — single-sourced from ADR-0031, drift-tested verbatim
      across all four surfaces:
      A load-bearing design choice with rejected alternatives — one a future agent would need to know about to avoid undoing it — warrants an ADR even when it changes no module boundary or public contract.
- [ ] **Revised a recorded decision?** (spec 100 / [ADR-0042](../../docs/decisions/adr-0042-decision-routing-gate.md))
      Routing is asked once at first write and never again, so a decision
      re-priced during this slice can stay misfiled. If a revised entry now
      clears the trigger above, promote it (`decisions.py promote --title
      "<title>" --no-push` — push mode reserves the ADR on `origin/main` from
      an ephemeral worktree, so off `main` it never reaches your working copy
      and `promote` refuses); if it is still settled, local and bounded, revise
      it (`decisions.py update`). Never hand-edit `lightweight-decisions.md`.
- [ ] **Conventions impact** — did this slice introduce or change a rule worth
      recording? If yes, edit `docs/conventions.md` (requires
      `JIG_CONVENTIONS_APPROVED=1`).
- [ ] **Inbox triage** — sweep `docs/inbox.md` for items resolved by this slice;
      move them to the relevant memory file or strike them through.
- [ ] **Primer hygiene** — if this slice closes the spec (all non-deferred
      slices DONE), apply the spec 025 compress-on-close-out rule per the slice
      template's `### Close-out (post-DONE)` section. Check every primer surface
      present in this project: `CLAUDE.md`, `AGENTS.md`, and scaffold templates.
      Active-spec sections should only carry in-flight work; load-bearing
      per-slice invariants migrate to the status board Notes column (which
      `workflow.py status-board` preserves across regen), memory, or the
      reconciled spec/slice record.
- [ ] **Memory-sync** — run `/jig:memory-sync` (or invoke `memory.py` directly)
      to persist any new domain terms, dead-end learnings, or tool decisions
      that emerged during implementation. **This is where slice 002-04's
      integration lives**: the reconciliation phase explicitly surfaces
      memory-worthy items for persistence. The reviewer subagent reads from
      memory but never writes to it (see `agents/reviewer.md`).
- [ ] **Closed-spec drift** — if reconciliation surfaces a prior
      closed-spec inaccuracy (a `DONE` / `SUPERSEDED` spec/slice, or
      load-bearing skill/router/workflow prose that no longer matches
      reality), follow the policy in [ADR-0010](../../docs/decisions/adr-0010-amendment-scope-records-vs-live-prose.md)
      (supersedes ADR-0008). **Records** (closed specs/slices): append a
      dated `## Amendments` entry preserving the original. **Live prose**
      (SKILL.md / workflow.md / README): fix it **inline** — git history
      is the audit trail. New ADR (or superseding spec) only for
      decision-content changes.
      **Authorisation to amend (issue #125).** Amending a closed **record**
      requires **explicit owner approval** — a separate grant from approval of a
      *behaviour*. When two canon artifacts disagree, **surface the conflict and
      stop**: propose the amendment as text in the conversation and write it only
      after the owner agrees. **Never write the resolution in the same turn as
      discovering the conflict** — *including when the owner has already approved
      the underlying behaviour* (approving what the app does is not authority to
      rewrite what the spec says). And before asserting that artifact X
      contradicts criterion Y, read **all** of Y's sibling criteria: another may
      already satisfy X — for a cross-cutting question the unit of reading is the
      whole criteria block, not the item that appears to speak to it. This
      authorisation rule governs **records** only; correcting live operational
      prose inline (per the split above) is git-history-audited and needs no
      sign-off.
- [ ] **Reconciliation review** — spawn a second reviewer subagent with a
      reconciliation-review prompt prefixed by
      `[jig:phase=reconciliation] [jig:spec=NNN] [jig:slice=NNN-NN]`: are the
      doc changes faithful? Is the deviation log honest? Is scope appropriate
      (no scope creep in docs)?
- [ ] **Use-case coverage (advisory)** — run `workflow.py coverage
      [--project-dir DIR]` and review any **coverage gap** (a use case with no
      implementing spec) or **scope creep** (a spec citing no resolvable use
      case). **Non-blocking** — unlike the gates above, a finding here does
      **not** block `RECONCILED` / `DONE` (ADR-0025 OQ3 / ADR-0011); it is the
      reconcile-time backstop to slice 02's framing-time grow prompt. No-op
      when the project has no `## Use cases` section.
- [ ] **Commit** — only after all gates pass.

### Auditing staleness (`workflow.py stale`)

Slice 015-03 added a read-only freshness audit:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/spec-workflow/workflow.py" stale \
  [--project-dir DIR] [--days N]
```

Walks `docs/specs/*/spec.md` and `docs/decisions/adr-*.md`, extracts
`last_verified` + `dependencies` from frontmatter, and lists items
meeting the **conjunctive criterion**:

> An item is stale iff (a) `today - last_verified > --days` (default 90)
> AND (b) at least one file referenced by `dependencies` was modified
> since `last_verified`.

Pure age isn't enough — a verified-2-years-ago ADR for an unchanged
decision shouldn't fire. Pure recency-of-dep isn't either — a doc
verified yesterday with old deps is fine. Both conditions must hold.

The check uses `git log -1 --format=%cs <path>` for committed-state
authority and falls back to filesystem mtime when git is unavailable
or the file isn't tracked. Read-only: it lists, doesn't transition.
Bumping `last_verified` is a deliberate human/agent action — edit the
file, or re-run `transition <slice> RECONCILED` after re-verifying.

## Gotchas

- **Spike is the LAST SPIDR technique** to reach for, not the first. AI agents
  default to spiking too eagerly; try Rules / Data / Interface / Path first.
- **Every slice must be vertical** (crosses all layers, delivers end-to-end value).
  A slice that touches only the DB or only the parser is horizontal phasing — flag it.
- **The reviewer subagent must NOT be invoked with prior implementation context.**
  Write the deliverable to disk first; reviewer reads only the spec + deliverable
  + acceptance criteria.
- **The reviewer is read-only on `docs/memory/`** — memory-sync runs as a separate
  step during reconciliation, never as part of review.
- **`workflow.py transition` uses substring matching on slice names** — `001-01`
  matches `## Slice 001-01 — greenfield-scaffold`. If you have multiple slices
  whose names share a fragment, the helper refuses with an `ambiguous` error;
  use a more specific fragment.
- **`workflow.py status-board` preserves the preamble** before the `| Spec` table
  header. Custom intro text survives regen. Idempotent: no churn if the board is
  already current. **Notes column** also survives regen (the helper parses existing
  Notes and re-emits them). **Deferred slices** appear in a separate `## Deferred
  slices` table below the active table; only the active table preserves Notes.
- **`workflow.py status-board` refuses to overwrite on a mid-regen race** (slice
  028-03). The helper captures a SHA256 of `docs/specs/README.md` at the start of
  regen and re-checksums right before the write; if another writer mutated the file
  in the gap, it raises `StatusBoardRaceError` and exits **4** with the message
  `status board changed during regen — another writer may have run. Re-run
  workflow.py status-board to retry.`. Pass `--force` to bypass the guard and
  overwrite anyway (use only when you've manually reconciled the conflict).
  Identical-content rewrites do NOT trigger a refusal (checksum is content-based,
  not mtime-based).
- **`workflow.py` ignores `## Spike` headers.** Spikes are research artifacts, not
  lifecycle-managed work items. They don't have a STATUS marker the helper can
  transition. If you need a spike to be tracked in the status board, model it as a
  `## Slice Nnna — <name>` instead, or update the board's Notes column manually.
- **Avoid raw `|` characters in the Notes column** of `docs/specs/README.md`.
  Markdown tables use pipes as cell separators; raw pipes in a Note value would
  truncate the cell during regen's preservation step. Use HTML-entity `&#124;`
  or rephrase if you really need a pipe.
- **`DEFERRED → DONE` (or any non-DRAFT state) is refused.** Re-open the
  slice with `DEFERRED → DRAFT` first, then advance through the normal
  lifecycle. This prevents silently skipping review gates when a parked
  slice is picked back up.
- **`transition <slice> DONE` validates `dependencies:`.** If any
  listed dep slice isn't DONE or any listed ADR isn't Accepted, the
  helper refuses with a structured error naming each unsatisfied dep.
  Empty / missing `dependencies:` skips the check.
