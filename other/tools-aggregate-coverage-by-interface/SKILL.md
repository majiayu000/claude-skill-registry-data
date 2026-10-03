---
name: tools-aggregate-coverage-by-interface
description: Render the ONE combined per-component scoring page (`<component>_scoring.html`) from the reconciled `unified_properties.yaml` — per-tool KPI cards, a combined Creusot|Kani scorecard over the public-method bundles, property-bundle and spec-vs-each-tool tables, unproved-causes, measurement, anti-vacuity, and provenance. Consumes the Role-1 property set + Role-2 per-tool status blocks that already live in `unified_properties.yaml`; attaches nothing new. Does NOT extract, bundle, or prove — the inventory owns the property set and the bundles, Role 2 owns the status. This is Role 3.
argument-hint: "[component-name]"
---

## Purpose

Given a component whose verifiable properties are extracted, agreed (Role 1), and proved/attempted
(Role 2) — all captured in `unified_properties.yaml` — produce **one presentation-ready scoring page** whose
scorecard aggregation unit is fixed: the **public methods of the `I<component>` trait** (the
`define_interface!` block). The page folds the earlier three thin slides into a single superset:
- the **scorecard** ("How many public methods did we verify?") — one row per public method,
  `Creusot | Kani`, headline *"Out of N public methods, Creusot proved X and Kani proved Y"*;
- the **bundle view** ("to verify a method, we verify every property in its bundle") — per-`id` rows;
- the **assumptions / spec-vs-tool view** — what is proved vs. proved-against-an-abstraction (`★`), where
  the Creusot-ghost-mirror ↔ Kani-real-type distinction is disclosed from each property's `fidelity`.

This skill **does not extract properties and does not run a prover.** It renders `unified_properties.yaml`.
An **incomplete** input (some properties not yet scored — their tool blocks carry no `status` key) is
**not** an error: render it, mark the unscored cells **pending `·`**, and show a prominent INCOMPLETE
banner. Only a **structurally inconsistent** input — a tool block citing an `id` absent from the property
set, or a scored value that contradicts the shared obligation — makes it stop and ask for reconciliation.
This lets a dry run or a partial (one-tool, mid-flight) run render honestly without crashing and without
overclaiming.

## The model (match the deck exactly)

- **Unit of coverage = public method.** The scorecard denominator is the **number of public methods**
  (`counts.methods`, e.g. 16/20, 12/20), NOT a property count.
- **A method is `✓` for a tool** when every property in its bundle reaches a terminal covered state and
  that tool proved (`✓`/`★`) at least one of them; `–` when every property is scored but the tool proved
  nothing for it, or a scored proof-lane property of its bundle is `⊘`; and `·` (pending) when any bundle
  property is not yet scored. (Full rule under **Method verdict**.)
- **Terminal covered states come from `unified_properties.yaml`:** `proved` (`✓`), `proved-against-abstraction`
  (`★` — ghost-mirror / trusted-boundary), or `delegated` (`⤴` — owned by another component, or covered
  by a non-proof lane such as Loom/Spin concurrency or a targeted fault-injection/hardware test named in
  the property's `note`). A `⤴`-delegated property does **not** block a proof tool's `✓` **iff** its
  delegation names a real owner/test — exactly as `create_memory_tier_entry` stays `✓` for Creusot while
  its SSD-atomicity property is delegated to a targeted test.
- **A Creusot/Kani-lane property that is a scored `⊘` (tool boundary), or still pending (unscored), DOES
  block that method's `✓`.** A scored-`⊘` bundle is unfinished, reported honestly as `–`; a bundle with any
  unscored property is pending, reported as `·` — never relabel either one covered.
- **Footnotes (keep them):** `*` = this tool is the better-fit prover for the method; `**` = the
  method's logic lives in other components (those rows are `– / –`).
- **The scorecard is two terminal states `✓/–` plus a pending marker `·` — no `◐`.** `✓` and `–` are the
  only *scored* verdicts (`★` still reads as `✓` at the method level; the abstraction/fidelity detail
  surfaces in the bundle & spec-vs-tool sections, never as a third scored state). `·` is **not** a third
  verdict — it is the "not yet scored" placeholder for a method whose bundle still has properties the scorer
  hasn't reached. `·` never counts toward `✓` and never toward the definitive `–`; it just means the run is
  incomplete for that cell. A fully scored run shows no `·`.
- **Display grouping by capability area is allowed** (Reference-counting, Tier-transitions, …) — it is
  *visual* only. The counting unit stays the public method. The renderer keeps one column per tool in
  `counts.tools`, so adding Loom/Spin later is a column, not a rewrite.

## Inputs (consume; do NOT re-extract, do NOT re-bundle)

**Primary input: `components/<component>/verif/unified_properties.yaml`** — the reconciled single source of truth
Role 1 built and Role 2 filled in. It carries, per property: the id-keyed obligation with its `methods`
bundle, `object_fn`, `kind`, `global`, `attachments`, `origin`, `source`, `statement` (owned by Role 1),
**and** the per-tool `creusot:`/`kani:` blocks (`status`, `symbol`, `fidelity`, `evidence`, `miss_class`,
`note`) written by Role 2. It also carries `counts:` (N methods, spec_total, code_total, unified M,
attachments, not_verifiable) and the `NV-*` ledger. **This skill renders from `unified_properties.yaml`; it does not
re-derive any of those fields.** There is **no `.md` backing file** — this HTML is the only human-readable
form, and every value it shows comes from `unified_properties.yaml`.

Two distinct conditions, two distinct responses:
- **Not-yet-scored (pending) is normal, render it.** A tool block with **no `status` key** means the scorer
  has not reached that property. Render it as pending `·` and raise the INCOMPLETE banner — do **not** stop.
- **Structural inconsistency STOPS.** A `creusot:`/`kani:` block that cites an `id` absent from the property
  set, or a scored status that disagrees with the shared obligation, is a real defect — **STOP and flag it**;
  never paper over divergence, invent a property, or re-bundle.
Reconciliation of the property *set* already happened in Role 1; the *status* is written by the scorer, and
a run where the scorer has not yet covered every property is a legitimate partial render, not a failure.

## The property record (all fields owned upstream; this skill renders, it does not overlay)

Every field comes from `unified_properties.yaml` — **read, never re-derive.** From Role 1:
`id`, `subject`, `methods` (the bundle), `object_fn`, `kind`, `global`, `attachments`, `origin`, `source`,
`statement`. The per-tool `creusot:`/`kani:` block has **two classes of field with two different writers**
under the reproduction gate — the renderer must respect the split:
```
  # SCORER-WRITTEN (by scorer_{creusot,kani}.py, by reproducing the proof — never by an agent):
  status:     proved | delegated | tool-boundary       # NOTE: no "not-attempted" — see below
  symbol:     "✓" | "★" | "⤴" | "⊘"    # ✓ native · ★ ghost-mirror/trusted-boundary · ⤴ delegated · ⊘ tool boundary
  evidence:   {vcs, coma, wall_clock_s, peak_rss_mb}  (Creusot) | {harness, result, unwind, wall_clock_s, peak_rss_mb}  (Kani)
  _scored_by: scorer_creusot | scorer_kani             # provenance stamp the scorer leaves
  # AGENT-SUPPLIED (advisory only; Role 2 may fill; the renderer shows them but they never set the verdict):
  fidelity:   <real-type | ghost-mirror | trusted-boundary>  (Creusot) | <real-type-bounded | representative | arithmetic-core>  (Kani)
  miss_class: TOOL | AGENT | null
  note:       <what the proof actually covers>
  delegate_to: <the owning component/test, when the agent proposes a delegation>
```
**Key-absence is the pending state.** A tool block with **no `status` key** (the null-placeholder Role 1
wrote, `{evidence: null, fidelity: null, note: null}`) means the scorer has not scored this property yet —
render it as **pending `·`**, never as covered and never as a failure. There is no `not-attempted` status
anymore; "not yet scored" is signalled by the *absence* of `status`. This skill computes only the **derived
rollups** (per-method verdicts, counts, headlines) from `status`/`symbol`; it writes nothing back into
`unified_properties.yaml`.

### Bundle ownership (read from the inventory — do not recompute)

- The `methods` bundle of each property, the per-method bundle sizes, and both counts (*distinct
  properties* M, *method→property attachments*) are **already computed in the inventory**. Read them.
- A shared-helper property (e.g. `align_up`) is already attached to every dependent method there — carry
  that through unchanged; it is expected for one property to sit in many bundles.
- The counting unit stays the public method. If you feel a need to reassign an owner, that is an
  inventory fix (Role 1), not something this skill does silently.

## Method verdict (per tool)

For public method `m` and tool `T` (Creusot or Kani), reading each property's `T` block from `unified_properties.yaml`.
First classify each property in `m`'s bundle for `T`: **scored** (has a `status`) or **pending** (no
`status` key yet). Then:
- `·` **(pending)** if **any** property in `m`'s bundle is still pending for `T` — the run has not finished
  scoring this method, so no terminal verdict is honest yet. Pending dominates: never resolve a method to
  `✓` or `–` while a bundle property is unscored.
- `✓` if **every** property in `m`'s bundle is scored to a terminal covered state — proved (`✓`/`★`) by
  some tool, or `delegated` (`⤴`) across a real interface boundary — **and** `T` itself proved (`✓`/`★`) at
  least one of `m`'s properties.
- `–` otherwise: every property is scored (none pending) but `T` proved nothing for `m`, or some property of
  `m`'s bundle is a scored `tool-boundary` (`⊘`). A `⊘` proof-lane property blocks the method's `✓` — report
  it honestly, never relabel; and never render a scored `–` for a method that is really still pending.

Component score: `Creusot X / N`, `Kani Y / N`, where **N = number of public methods** (`counts.methods`).
When any method is pending, also report the pending count and keep the INCOMPLETE banner up — `X` and `Y`
count only methods that are fully scored to `✓`, never pending ones.
Also report the net: **methods whose whole bundle is covered (done) vs incomplete**. `★` counts toward
`✓` at the method level but its fidelity (ghost-mirror / trusted-boundary) is disclosed in the scorecard
and the assumptions/spec-vs-tool sections — never hidden.

## Required output — ONE combined scoring page

Emit a **single** self-contained `<component>_scoring.html` rendered from `unified_properties.yaml` — the superset
page that replaces the old three thin slides (8/9/11). One page per component, extensible to more tool
columns (Loom/Spin can be added one at a time later — the renderer is N-tool-ready, not hard-wired to two).
Sections, in order (this mirrors the hand-curated `SEPT_2026/SEPT_14/*_scoring.html` reference layout):
1. **Title + sub-line** — interface, N, `.coma`/VC totals (Creusot), Kani harness count, run pin + date.
2. **Banner callout** — the three end-states (Proved / Delegated ⤴ / Tool-boundary ⊘) and the anti-vacuity note.
3. **FROM_SPEC callout** — links `spec_properties.yaml`/`code_properties.yaml`, states `spec_total` / `code_total` / unified `M`,
   and explains they differ from M (spec∩code).
4. **Per-tool KPI cards** — Creusot and Kani each: `X/N` methods, VCs/`.coma` (Creusot) or harness count (Kani),
   wall-clock + peak RSS.
5. **Combined scorecard** — the one table with columns **Props | Method | Creusot | Kani | Boundaries/notes**;
   per-method rows grouped by capability area; per-tool cell shows the method verdict symbol; `*`/`**` footnotes
   (`*` = better-fit prover; `**` = logic lives in other components → `–/–`).
6. **Property-bundles table** — **Property | What it requires | Creusot | Kani | Owner/note**, per `id`, each
   tool cell showing its `symbol` and (on hover/'★') its `fidelity`.
7. **Spec-vs-each-tool table** — **Spec property | What Kani proves | What Creusot proves | The weakening** —
   this is where the abstraction↔real finding surfaces from the `fidelity` fields (Creusot ghost-mirror/★ vs
   Kani real-type-bounded).
8. **Unproved rows and their causes** — narrative over the `⊘` properties with their `miss_class`
   (TOOL vs AGENT) and reproducible signatures from `note`/`evidence`.
9. **Measurement table** — **Tool/run | Wall-clock | Peak RSS | Discharged** (VCs/`.coma` or harnesses).
10. **Anti-vacuity** statement and **Provenance** (pin, sources, generator).

HTML must be **self-contained and theme-aware**; deliverables are read in-repo and may be cut onto plain
white slides (keep backgrounds light, avoid heavy colored bands). Reference implementation: the
hand-curated `SEPT_2026/SEPT_14/<component>_scoring.html`.

(Optional) if a machine-readable rollup is wanted, it is already `unified_properties.yaml` — do **not** re-emit a
hand-formatted `.md` rollup; the YAML is the structured artifact and the HTML is the presentation.

## Honesty rules (non-negotiable)

- **A method is `✓` only when its whole bundle is covered.** A scored `⊘` proof-lane property makes the
  method `–`; a still-pending (unscored) one makes it `·`. Either way it is not `✓` — do not inflate the
  method count by ignoring unfinished or unscored properties.
- **N = number of public methods** (`counts.methods`), fixed by the trait. Never shrink N to improve the ratio.
- Every `proved` claim traces to a real artifact (VC/`.coma` or harness) via the property `id` and `evidence`.
- **`★` is disclosed, not hidden.** A method whose `✓` rests on a ghost-mirror/trusted-boundary property
  still shows `✓` at the method level, but the scorecard/bundle/spec-vs-tool sections must surface the
  `fidelity` so the abstraction is visible. Under-claim, never over-claim.

## Procedure

1. Read `unified_properties.yaml`: the public methods, N (`counts.methods`), the `methods` bundles, and each
   property's `creusot:`/`kani:` blocks (do not recompute any Role-1/Role-2 field).
2. **Consistency gate (not a completeness gate):** stop and flag ONLY on a structural defect — a tool block
   citing an `id` absent from the property set, or a scored status contradicting the shared obligation.
   Properties with **no `status` key are pending, not errors** — render them `·` and raise the INCOMPLETE
   banner; do not stop. (A dry run or a one-tool partial run is expected to be all- or mostly-pending.)
3. Compute each method's `✓/–/·` per tool (verdict rule above — pending dominates), the score X/N and Y/N
   over fully-scored methods, the pending count, and the done/incomplete split. Pull `fidelity`, `evidence`,
   `miss_class`, and `note` straight through for display.
4. Render the single `<component>_scoring.html` (sections above) from `unified_properties.yaml`.
5. Report: `<component> — Creusot X/N, Kani Y/N public methods proved; Z methods have complete bundles,
   P methods still pending (unscored), (N−Z−P) scored-but-incomplete (list the blocking ⊘ properties with
   their signatures)`. If P > 0, say so plainly — the run is a partial render, not a final score.

## Anti-patterns (the rabbit holes)

- ❌ Counting **properties** as the scorecard denominator. (Denominator = public methods.)
- ❌ Using `◐` on the scorecard. (Scored verdicts are two-state ✓/–; `★`/fidelity detail lives in the bundle
  & spec-vs-tool sections. Pending `·` is legitimate but is *not* a verdict — it marks a not-yet-scored cell.)
- ❌ Marking a method `✓` while a proof-lane property is still `⊘`, or resolving it to `✓`/`–` while any
  bundle property is still **pending** (unscored). Pending dominates — render `·` and keep the banner up.
- ❌ Treating a not-yet-scored property (no `status` key) as a failure and STOPping. Absence of `status` is
  pending, not an error; only a structural inconsistency stops the render.
- ❌ Re-extracting, re-bundling, or re-deriving status. (Everything comes from `unified_properties.yaml`.)
- ❌ Emitting the old three thin slide files or a hand-formatted `.md` rollup. (One combined HTML; YAML is the data.)
- ❌ Guessing a round property/method count to fit a table.

## Routing

General methodology → `unstable` (promote via PR; don't leave siloed on a verif branch).
Deliverables (`spec_properties.yaml`, `code_properties.yaml`, `unified_properties.yaml`, `<component>_scoring.html`) → written under
**`formal-verification/<component>/`** and shipped to `unstable` via PR. Under the `component-verify`
orchestrator, the orchestrator performs that commit/PR (gated to `formal-verification/<component>/`); run
standalone, open the PR yourself. **No Box, no scp** — the repo folder is the shareable home.
