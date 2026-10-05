---
name: reframe
description: >
  Re-baseline a jig corpus onto a moved load-bearing reference by drafting a
  keystone ADR and an affected-artifact disposition manifest. Use when a
  vendor/API contract moved and specs and decisions must be re-anchored.
  Auto-triggers when you say reframe onto this, we changed direction, the
  design moved, or re-baseline the project; invoke explicitly as
  `/jig:reframe`. Defers to any
  other installed skill whose description identifies it as handling project
  re-baselining or migrating onto a new reference. Does not defer to the
  generic built-in. Do not use for adopting jig (use `/jig:migrate`), cleanup
  against a fixed reference (use `jig:refactor`), changing one decision (use
  `adr.py supersede`), or cross-artifact drift detection (use `/jig:analyze`).
user-invocable: true
---

> Spec 067 introduces this skill; [ADR-0024](../../docs/decisions/adr-0024-reference-reframe.md)
> decides its shape. Reframe is a **lightweight correction capability over the
> lifecycle spine** ([ADR-0023](../../docs/decisions/adr-0023-lifecycle-family-spine.md) §4),
> **not** a new gated lifecycle member: it has no `transition` and no state
> machine of its own — its arc (recognize → decide dispositions → execute)
> *orchestrates* the ADR and spec lifecycles it spawns, and every gate it relies
> on (the keystone ADR's frame-critique `accept`; the review passes on the
> retrofit specs) belongs to those lifecycles. Shipping as its own skill is a
> user-facing-surface choice — a deliberate, named operation a user reaches for —
> not a lifecycle one.
>
> Like `/jig:clarify` and `/jig:explain`, reframe is a **judgment skill** — it
> ships **no `.py` helper**. The determinism it needs (reserve the keystone ADR,
> reserve retrofit specs) it borrows from the existing `adr.py` / `workflow.py`
> scaffolding; the corpus read and the drafting are model judgment. Its testable
> surface is **structural** (this SKILL.md's contract: the keystone-ADR-via-
> `adr.py new` flow, the disposition vocabulary, the coverage-floor shape, the
> deferral language, registration). The *quality* of the corpus read and the
> honesty of a given coverage floor are judgment, exercised by this prompt and by
> the keystone ADR's frame-critique `accept` gate — not something a unit test can
> assert (the accepted gap for every judgment-only jig skill).

## What this skill does

jig keeps work **consistent with prior decisions**: every spec and ADR is a
durable record, and new work reads the accepted corpus as authoritative. That is
jig's strength — and its blind spot when a **load-bearing premise changes from
outside the system**. A team drops a new design (or contract, or vision) into
the repo intending to retrofit onto it; but the corpus already encodes the *old*
premise as settled truth, so the new artifact enters as an **inert file with no
authority** and the consistency machinery faithfully carries the dead premise
forward — the agent patches at the edges instead of re-baselining.

A **load-bearing reference** is any authoritative external input the corpus is
premised on: a design system, a test-infrastructure choice, a vendor / API
contract, a compliance regime, a target platform, or a product-positioning /
strategic-vision shift. A **reframe** re-anchors the corpus to one that has
*moved*. `/jig:reframe`, given the new reference:

1. **Reads the accepted corpus against the reference** (the corpus read).
2. **Drafts the keystone reframe-ADR** via `adr.py new` — elevating the new
   reference from an inert file to an accepted decision, superseding the old
   premise, and carrying the **re-baselining manifest**.
3. **Assigns every affected artifact a disposition** in that manifest (no `TBD`),
   each routing to an operation that already exists.
4. **States a two-level coverage floor** — what corpus was scanned, at what
   granularity, and what was *not* — so a partial read is visible at the ADR's
   `accept` gate rather than silently carrying a dead premise forward under fresh
   authority.

A competent session, handed the accepted keystone ADR + the manifest, then
executes the dispositions through the existing ADR and spec lifecycles. The skill
**drafts**; the session **executes**. This is a **best-effort correction floor**:
it makes re-baselining *expressible* and human-gated — it does not auto-solve
enumeration completeness (parked, see the coverage floor) and it is not a
silent-drift *detector* (that half is the [067-03](../../docs/specs/067-reframe/slice-03-noticing-nudge.md)
noticing nudge + parked detection).

## When to use vs. when to defer

**Defer to a richer installed skill first.** If another installed skill's
description identifies it as handling **project re-baselining** or **migrating
onto a new reference**, prefer it — jig's reframe is a slim baseline. This skill
does **not** defer to the generic built-in; it only steps aside for a skill whose
description names the re-baselining / reference-migration job.

Sibling jig operations that are easy to confuse with reframe — reach for the
right one:

- **`/jig:migrate`** — brings an existing project *into* jig (adopts an outside
  layout into jig structure). Reframe operates *within* an already-jig project
  whose *premise* moved. Migrate is about the container; reframe is about the
  contents' authority.
- **`jig:refactor`** ([ADR-0019](../../docs/decisions/adr-0019-refactor-workflow.md))
  — changes *structure* while **preserving behaviour** against a *fixed*
  reference. Reframe is the level above: the *reference itself* moved, which then
  *spawns* behaviour-change work (retrofit specs) that flows through refactor /
  bug-fix / spec-workflow. Reframe is **not** a member of ADR-0019's
  behaviour-change taxonomy.
- **`adr.py supersede`** — retires **one** decision with **one** replacement
  (1:1, decision-scoped). A reframe re-baselines a *corpus* premised on the moved
  reference — many artifacts, many dispositions — and mints the keystone ADR that
  makes the new reference authoritative. If the shift really is a single
  1:1 decision change, use `adr.py supersede` directly (over-built otherwise —
  see ADR-0024 Kill criteria).
- **`/jig:analyze`** — surfaces *drift between* existing artifacts (does spec A
  contradict ADR B?). Reframe *introduces* a new authority and routes the fallout.
  Analyze audits the corpus as-is; reframe changes what the corpus is anchored to.

Rule of thumb: **the premise moved → this skill. Adopt a project into jig →
`/jig:migrate`. Behaviour-preserving cleanup → `jig:refactor`. One decision
changed → `adr.py supersede`. Audit alignment → `/jig:analyze`.**

## Inputs — the moved reference

The argument is the **new load-bearing reference**: a path to a dropped-in
artifact (`design/new-system.fig`, `docs/vision-2.0.md`, an OpenAPI file) or a
clearly named reference the user points at.

- **Not locatable → refuse and ask.** If the named reference can't be located
  (no such path, ambiguous name), the skill **refuses** and asks the user for a
  path or a precise identifier. It does **not** guess a reference or draft a
  keystone ADR against a reference it never read.
- **Nothing to re-baseline → say so, draft nothing.** If the corpus read finds
  **no artifact** that the reference actually invalidates (the reference is
  additive, or the corpus never encoded the old premise), the skill reports
  *"nothing to re-baseline"* and drafts **no** keystone ADR. An empty keystone
  ADR is never minted. (Resolves spec 067 Clarification Q1.)

## The corpus read

Given a located reference, the skill **reads the accepted corpus (decisions +
prose) against it** as the basis for drafting — which artifacts encode the *old*
premise the new reference replaces. Two things this read is explicitly **not**:

- **Not a `## Assumptions` sweep.** The `## Assumptions` ledger is *risk-gated*
  ([ADR-0020](../../docs/decisions/adr-0020-spec-frame-hardening.md)): it logs
  only *contested* assumptions, never *settled* premises. A dead design that was
  settled truth never appears there — settled premises are invisible to the
  ledger for the same reason they silently steer the model: they are unquestioned
  ground. Scanning the ledger would structurally miss the exact thing a reframe
  must catch.
- **Not a built corpus-walker.** There is no detection engine, no `references:`
  frontmatter tagging, no [spec 024-02](../../docs/specs/024-analyze/spec.md)
  corpus-walking helper. Those are **parked** behind triggers T1/T2/T3
  (ADR-0024 §7). The read is the model's judgment over Read — its completeness is
  the binding risk the coverage floor surfaces (below).

## The keystone reframe-ADR

Reserve and scaffold the keystone ADR through the **real ADR lifecycle** so it
inherits the frame-critique `accept` gate:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/adr-workflow/adr.py" new reframe-onto-<slug>
```

Then author its body:

- **Declare the new reference authoritative as of `<date>`.**
- **Supersede the old premise** (name it; link the decisions/prose that encoded
  it).
- **Carry the re-baselining manifest** (below) and the **coverage floor** (below).

Because the keystone ADR rides `adr.py`, its Proposed→Accepted flip is
**frame-critique-gated** (*probed:* `adr.py`'s `_gate_frame_critique()` refuses
`accept` without a passing verdict; new ADRs are stamped `frame_review: true`).
This is load-bearing: the coverage floor is **human-confirmed at that gate** — the
natural checkpoint for "did the read miss anything?"

## The re-baselining manifest

A table of **every affected artifact**, each assigned a deliberate **disposition**
— **no `TBD`**. `retire-draft` items are surfaced **first** (future-work drafts on
the dead premise mint dead-premise work; kill them before anything builds on
them).

Net-new forward work the reframe *spawns* — specs/ADRs the new reference *reveals*
that did not exist before, distinct from fixing an *existing* artifact — is
recorded in a separate **`## Emergent work`** section, **not** forced into a
disposition row (a disposition is the fate of an *already-affected* artifact;
spawned work has no prior artifact to dispose of).

### Disposition vocabulary

Each disposition routes to an operation that already exists (ADR-0024 §3):

| Disposition | Meaning | Routes to |
|---|---|---|
| `reaffirm` | premise survives the new reference | refresh `last_verified` + note the reframe |
| `amend` | closed record, still valid, needs a pointer | `## Amendments` ([ADR-0010](../../docs/decisions/adr-0010-amendment-scope-records-vs-live-prose.md)) |
| `supersede` | decision now wrong | `adr.py supersede` / superseding spec |
| `retire-draft` | future-work on the dead premise | DEFERRED or discard — **do first** |
| `retrofit` | shipped code must change | a slice in a retrofit spec `/jig:reframe` mints via `workflow.py new` (see **Retrofit spec drafts**) |
| `rewrite` | **live, non-record prose** whose framing must change (not a closed record → not `amend`; not a decision → not `supersede`; not code → not `retrofit`) | rewrite in place, citing the keystone ADR |

## The two-level coverage floor

The manifest's coverage statement is **not free text** — a bare "here's what I
scanned" note is checked against nothing, so a confident narration of a *partial*
scan reads as complete. It is a **two-level coverage floor** (ADR-0024 §2–§3):

- **Level 1 — whole corpus, class-level.** Walk the corpus's
  deterministically-listable **top-level artifact classes** and mark **each**
  `scanned` or `excused (reason)`:
  - `docs/decisions/` (ADRs)
  - `docs/specs/` (specs + slices)
  - live-prose docs under the docs root (`product-vision.md`, `architecture.md`,
    `workflow.md`, `README`-style guides, roadmap, glossary)
  - `skills/*/SKILL.md`
  - the root primer(s) (`CLAUDE.md` / `AGENTS.md`)
  - `README`

  L1 covers the **authority-bearing corpus** — decisions, specs, and the prose /
  skill contracts that *encode premises* — **not** the code tree: shipped code
  that must change is dispositioned `retrofit` and handled by a retrofit spec, not
  scanned by the floor. L1 makes a **whole class silently dropped**
  impossible-to-hide: an omission requires actively writing `skills/: not scanned`,
  which is *visible*. (This is the miss that bit the n=2 servo reframe, whose read
  covered only `docs/` + `README` and silently skipped `skills/`.)
- **Level 2 — artifact-level, within touched classes.** For **each class the
  reference actually touches** (the classes the keystone supersedes *into*),
  enumerate the **artifacts within** and state the **method** by which you decided
  which encode the dead premise — so the manifest's disposition rows are the
  *output* of an explicit within-class read, not a hand-waved "class scanned." L2
  confronts the **intra-class miss** — the motivating Android-design failure,
  where dead-premise files lived *inside* `docs/specs/` and `docs/decisions/`
  entries a class-level floor would mark `scanned`.

State the overall **method** and the **residual uncertainty**. Say plainly that
the floor **reduces and surfaces** the enumeration risk — it does **not**
eliminate it. Genuinely-open residuals (own them, don't hide them):

- a class wrongly judged *untouched* gets only L1, so an intra-class miss there
  survives;
- even within a touched class the read can miss an artifact;
- a human can rubber-stamp a weak `excused`.

All three are backstopped by **T1's two-pronged evidence** (ADR-0024 §7): the
accept-time floor **or** *post-reframe discovery* — a later session that finds a
surviving dead-premise artifact **inside a class the manifest marked `scanned`**
un-parks systematic detection. This is the honest fallback, not a completeness
claim.

> **Maintenance note — the L1 class list is jig-corpus-shaped.** The top-level
> classes above match jig's own corpus layout. If a downstream project grows a
> **new** top-level artifact class this list doesn't name (or uses a
> [configurable docs root](../../docs/decisions/adr-0033-configurable-docs-root.md)),
> extend the L1 walk to name it — otherwise that class is invisible to L1 (the
> whole-class-drop failure moved up one level, into the template). This is a
> foreseeable maintenance seam, adjacent to the T2 corpus-growth trigger; written
> down here rather than left silent, per this skill's own "omissions must be
> visible" ethos.

## Retrofit spec drafts

For **every `retrofit` disposition** in the manifest, `/jig:reframe` also mints a
**retrofit spec draft** — the shipped-code change the reference forces, queued in
the spec lifecycle rather than left for the session to hand-author. For each
`retrofit` row:

1. **Reserve a spec** via `workflow.py new`:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/spec-workflow/workflow.py" new \
     retrofit-<artifact>-onto-<reference-slug>
   ```

   Slugify the substituted parts — lowercase, `[a-z0-9-]` only, no `--`;
   `workflow.py new` refuses a malformed slug.

2. **Goal the draft on the reference.** The draft's Overview / first-slice goal
   reads **"bring `<artifact/code>` in line with `<reference>`"**, naming the moved
   reference explicitly — so the retrofit's purpose is unambiguous and measured
   against the *new* authority, not the dead premise.

3. **Anchor `## Assumptions` on the new reference.** The retrofit spec's
   `## Assumptions` cite the new reference as the authority the work is measured
   against, so a future frame-critique on that spec is anchored correctly
   ([ADR-0024](../../docs/decisions/adr-0024-reference-reframe.md) §3) — not against
   the premise the reframe just retired.

4. **Close the loop — no `retrofit` disposition silently dropped.** Every
   `retrofit` row maps to a drafted spec **or** to an **explicitly-recorded reason
   it was not drafted** surfaced to the user (e.g. `deferred — <why>`). Update the
   keystone manifest to **link each `retrofit` row to its drafted spec number**, so
   the disposition→draft mapping is **complete and visible** — the same "omissions
   must be visible" ethos as the coverage floor.

The retrofit specs then ride the normal review-gated `spec-workflow` lifecycle:
`/jig:reframe` *drafts* them, a competent session *implements* them. (This mirrors
the keystone-ADR flow — reframe reserves + drafts through the real lifecycle so the
spawned work inherits its gates for free.)

## No `.py` helper

Like `/jig:clarify` and `/jig:explain`, this skill ships **no helper script**. The
only determinism it needs runs through existing tooling:

- **reserve the keystone ADR** via `adr.py new` (frame-critique-gated `accept`);
- **reserve retrofit specs** via `workflow.py new` (one per `retrofit` disposition);
- **corpus reading** via the Read tool.

There is no `reframe.py`. The corpus read and the drafting are model judgment; the
structural surface (this contract) is what tests assert.

## Gotchas

- **Draft, don't execute.** The skill produces the keystone ADR + manifest +
  drafts; a competent session executes the dispositions through the existing
  lifecycles. No heavy auto-execution (ADR-0024 §6).
- **No empty keystone ADR.** If nothing in the corpus encodes the moved premise,
  report "nothing to re-baseline" and draft nothing (Q1). If the reference isn't
  locatable, refuse and ask.
- **The coverage floor is the point, not a formality.** A weak `excused` reason or
  a class you mark `scanned` without an L2 read reproduces the motivating failure
  under fresh keystone authority. Make the read honest; the frame-critique gate is
  where a human confronts it.
- **`retire-draft` first.** Dead-premise drafts mint dead-premise work — retire
  them before anything builds on them.
- **Not the `## Assumptions` ledger.** Never detect the shift by sweeping
  `## Assumptions` — it is risk-gated and blind to settled premises (the exact
  thing to catch).
- **Capability, not a lifecycle member.** Reframe adds no `transition` and no
  state machine; it orchestrates the ADR/spec lifecycles it spawns. Don't build a
  `reframe.py` state machine (ADR-0024 Option B — rejected at n=1).

## Relationship to other skills

- **`adr-workflow` (`adr.py`)** — reframe reserves the keystone ADR via `adr.py
  new` and routes `supersede` dispositions through `adr.py supersede`. The
  keystone's frame-critique `accept` gate is where coverage is human-confirmed.
- **`spec-workflow` (`workflow.py`)** — `retrofit` dispositions become retrofit
  spec drafts via `workflow.py new` (slice 067-02); those specs then ride the
  normal review-gated lifecycle.
- **`jig:refactor` / `jig:bug-fix`** — the behaviour-change lifecycles a reframe
  *spawns* work into; reframe is explicitly not a member of their taxonomy.
- **`/jig:migrate`** — the sibling entry path (project *into* jig) that reframe is
  not; see "When to use vs. when to defer".
- **`/jig:analyze`** — audits drift between existing artifacts; reframe introduces
  a new authority and routes the fallout. Reuse of analyze is *conceptual* (its
  six-category model), not code.
