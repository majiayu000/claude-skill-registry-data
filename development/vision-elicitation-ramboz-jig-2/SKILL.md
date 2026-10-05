---
name: vision-elicitation
description: >
  Lightweight baseline elicitation pass that fills in `docs/product-vision.md`
  and the five `docs/architecture.md` elicitation slots after `scaffold-init`.
  Auto-triggers when you say set up project vision, elicit architecture,
  define what we're building, run the vision wizard, refresh the project
  pitch, or capture product scope. Defers to any other installed skill whose
  description identifies it as handling vision elicitation, product
  discovery, project framing, or product scope capture — if such a skill is
  present, prefer it over this one (jig's version is a slim baseline). Does
  not defer to the generic built-in `init` skill. Do not use for: ad-hoc
  brainstorming with no `docs/product-vision.md` slot to write into;
  silently overwriting vision content the user has already hand-edited
  (the re-run protocol's divergence detection handles that — see the
  Re-run protocol section below); spec authoring (use
  `/jig:spec-workflow`); seeding ADRs for already-named decisions (use
  `/jig:adr-workflow new`).
user-invocable: true
---

> Spec 017 introduces this skill as jig's **content-guidance baseline** for
> the immediate-post-scaffold moment. It is the third non-stub active jig
> skill that ships without a `.py` helper — vision-elicitation is
> fundamentally a judgment skill, and the determinism it needs (find the
> elicitation slots, transition markers, render Q&A into template bodies)
> Codex can run inline via Read/Edit. If any other skill is installed
> whose description identifies it as handling vision elicitation, product
> discovery, project framing, or product scope capture, the Codex
> skill router prefers that one over jig's baseline — the deferral is
> category-based, not name-specific, so a richer user skill named anything
> (`vision-wizard`, `product-canvas`, `lean-pitch`, etc.) wins. Jig's slim
> version remains the auto-trigger when no such skill is installed.

## What this skill does

Runs a structured 13-section Q&A immediately after `scaffold-init`, then
writes the captured answers into the elicitation slots that slice 017-01
introduced (extended by slice 022-02 with Section 13 — Contract surfaces
— feeding the `/jig:contracts` skill):

- `docs/product-vision.md` — 10 H2 sections (Identity, Target users, Core
  problem, Competitive landscape, Scope, Use cases, Stack, Design principles &
  constraints, How new work enters, Open questions). Each section's
  `<!-- elicited: PENDING / status: unfilled -->` marker transitions
  to `status: filled` (with today's ISO date) or `status: skipped`. The
  **Use cases** section (added by slice 068-01 / ADR-0025) is filled by a
  distinct **conversational capture loop**, not the rigid per-section Q&A —
  see the [Use cases capture](#use-cases-capture) section below.
- `docs/architecture.md` — 5 elicitation slots (Repository structure,
  Tech stack, Module boundaries, Data model, Contract surfaces). Same
  marker transition. Two sibling sections (Core architecture decisions,
  Open questions) carry no markers and are populated by ADRs /
  refinement-todo entries over time, not by elicitation. The Contract
  surfaces slot was added by spec 022-02 to feed the `/jig:contracts`
  skill.

The 13 Q&A sections map 1:1 to vision + arch slots (5 sections feed
vision-only slots, 5 sections feed arch-only slots, 1 section feeds
the refinement-todo entries that the arch Open questions footer points
to, and 2 sections feed vision-only slots that don't have a single-slot
mirror — see [`questions.md`](questions.md) for the canonical mapping).

The skill is **breadth over depth**: catch the essentials of what the
user wants to build, leave deeper product-discovery facilitation
(lean-canvas workshops, multi-persona scoping, prioritization frameworks)
to a richer user-installed skill at the discovery surface.

## When to use vs. when to defer

There are four things people often confuse with this skill. Pick the right
one:

- **Any other user-installed vision-elicitation / product-discovery /
  project-framing skill.** Common locations include
  `$HOME/.agents/skills/vision-elicitation/`, `$HOME/.agents/skills/product-canvas/`,
  `$HOME/.agents/skills/lean-pitch/`, etc. — but the deferral is
  **category-based, not name-based**, so a skill named anything whose
  description claims vision elicitation, product discovery, project
  framing, or product scope capture will be preferred. If one is present,
  **defer to it.** The one exception jig's description carves out is the
  bundled `init` skill — jig:vision-elicitation does **not** defer to that
  one (it's the generic AGENTS.md-bootstrap helper, a different surface).
- **`/jig:spec-workflow`** — sibling jig skill for **spec authoring**
  (drafting a slice, SPIDR-splitting features, transitioning state
  markers). That's about *what we'll build next*. This skill is about
  *what the project is fundamentally* — the substrate spec-workflow runs
  on top of. Reach for `/jig:spec-workflow` when you have a feature in
  mind and need to author a slice. Reach for this skill when the project's
  identity, target users, core problem, or architectural shape isn't yet
  captured in `docs/product-vision.md` / `docs/architecture.md`.
- **`/jig:adr-workflow new`** — for seeding ADRs from decisions the user
  has already named. If the user comes in saying "we've decided on
  SQLite, let's write that down," that's an ADR job, not vision
  elicitation. Slice 017-04 (deferred) will add an optional seed-ADR
  pass at the end of this skill's Section 7 (Tech stack); until then,
  ADRs are seeded by hand via `/jig:adr-workflow new`.
- **`/jig:scaffold-init`** — the install-time wizard that produces the
  empty slots this skill fills. `scaffold-init` runs once; this skill
  runs after, can be re-run, and produces the substantive content.

Rule of thumb: **empty slot → this skill. Named decision → adr-workflow.
Feature scope → spec-workflow. Empty repo → scaffold-init.**

## How the elicitation works

The skill is **judgment-only** — no `.py` helper. Codex reads the
question set, conducts the Q&A inline with the user, and writes the
rendered answers via the Edit tool. The per-section flow is:

1. **Load the question set** from [`questions.md`](questions.md). 13
   sections; each lists 1–4 questions plus optional follow-ups.
2. **Detect existing markers.** Open the project's
   `docs/product-vision.md` and `docs/architecture.md`. Find each
   section's `<!-- elicited: ... -->` marker. Branch on the
   `status:` value:
   - `unfilled` → elicit (this is the first-run case).
   - `filled` → run the Re-run protocol below (hash check; warn on
     divergence).
   - `skipped` → offer fresh Q&A. The user explicitly skipped this
     section previously; a re-run is the natural moment to revisit
     it. No hash check is performed (skipped sections have no
     canonical body to compare against).
3. **For each candidate section, ask the questions in order.** Let the
   user answer, skip, or come back later. A user can answer "skip" to
   transition the section to `status: skipped` without filling it.
4. **Render the answer into the template slot.** Replace the
   placeholder prose between the marker and the next H2 with the
   user's words. Update the marker:
   - Answered → `<!-- elicited: YYYY-MM-DD / status: filled -->`
   - Skipped → `<!-- elicited: YYYY-MM-DD / status: skipped -->`
5. **Move to the next section.** No looping; no upselling; stop when
   all 13 sections have been visited.

### Per-section flow, not per-question flow

The Path SPIDR decision (spec 017's SPIDR table) is per-section.
Each *section* is independently skippable and re-runnable; *individual
questions within a section* are not their own skip-units. If a user
wants to answer Q7.1 but skip Q7.2, the skill should still write the
Q7.1 answer into the Tech stack slot, then move to Section 8 — not
treat that as a half-filled section.

## Inputs

Three input modes, ordered by richness:

1. **Full session context (preferred).** You're inside a Codex
   session at the project root, with `docs/product-vision.md` and
   `docs/architecture.md` on disk from `scaffold-init`. The user can
   answer questions interactively; you write to disk as each section
   completes.
2. **Pitch-document context.** The user pasted or pointed at a project
   pitch (e.g. `/Users/ramboz/Projects/AGENTS.md` for YarnFinder; a
   README; a one-pager). Use the pitch to ground the questions but
   still ask the user — the skill does not auto-fill from a pitch
   alone (the user's voice in the final doc matters).
3. **No prior pitch.** Start cold. The first Section (Identity) is
   load-bearing in this case — the rest of the elicitation flows from
   the one-sentence answer to Q1.1.

## Rendering rule: the skill writes the user's words

**The skill does not paraphrase, expand, or "improve" the user's
answers.** If Q3.1 is "describe the problem in 2–3 sentences" and the
user answers "crafters can't find regional yarn alternatives," the slot
reads "crafters can't find regional yarn alternatives." Not "Crafters in
non-US regions face difficulty locating equivalent yarn substitutes for
US-sourced patterns." The skill's job is to ask, not to interpret.

This is a hard rule. It's enforced inline by the worked-example
transcripts ([worked-example-jig.md](worked-example-jig.md) and
[worked-example-yarnfinder.md](worked-example-yarnfinder.md)) — both
demonstrate the user's literal words rendered into the slot.

Two narrow exceptions:
- **Markdown structure.** The skill formats answers as bullet lists,
  tables, or sub-bullets where the template prescribes that shape
  (e.g. the Competitive landscape table). The user's *content* is
  unchanged; only the markdown around it is added.
- **Section ordering.** If a user's answer to Q5.1 (core features)
  enumerates 5 items in priority order, the skill writes them in that
  order. The skill never reprioritizes.

## Use cases capture

The **`## Use cases`** vision section (slice 068-01 / [ADR-0025](../../docs/decisions/adr-0025-use-cases-breadth-layer.md))
captures the project's intended user-facing **behaviors** — the breadth frame
specs later anchor against. Unlike the other slots, it is **not** filled by the
rigid per-section Q&A above; it runs a short **conversational capture loop**,
because behaviors come out unevenly (a few at a time, or one big paste) and need
shaping before they land. The loop is **goal-level only** (`"[actor] can [goal]"`,
never spec-level — see the section's own guidance) and has four steps:

1. **Capture — any shape, loop to exhaustion.** Accept behaviors however the
   user supplies them: typed in **incrementally** one at a time, OR pasted in
   **bulk** as a list. After each batch, ask **"anything else?"** and keep
   looping **until** the user signals **done**. Do not stop at the first answer;
   do not cap the count.
2. **Normalize — a single pass.** Run exactly **one** normalize pass over the
   captured set: **dedupe** near-identical entries, **split** compound entries
   ("search and filter results" → two behaviors), and rephrase each to the
   **goal-level** `"[actor] can [goal]"` form. One pass — not an iterative
   rewrite loop.
3. **Confirm before any write — edit round-trips.** Present the normalized set
   back to the user for **confirm/edit**. **Nothing is written** to the vision
   `## Use cases` section **before** the user confirms. If the user edits the
   set, re-present the edited list — the **edit round-trips** through confirm —
   and write **only** once they confirm. On confirm, render the entries into the
   section **each prefixed with a stable `UC-N` id** (a plain integer — `UC-1`,
   `UC-2`, … — assigned in order on this first capture) and flip the marker to
   `status: filled` (with hash). The id is **append-only**: a later grow pass
   (slice 068-02) keeps the existing ids stable and assigns the next free
   number, never renumbering or reusing one. The id is what a spec's
   `use_cases:` trace link resolves against.
4. **No silent inference — ever.** A use case the user did **not** state is
   **never** auto-added / inferred into the set. If you *suspect* an obvious
   behavior is missing, surface it as a **question** — *"You didn't mention X —
   intentional?"* — and add it **only on an explicit yes**. A "no" or silence
   leaves it out. This is a hard rule: the section is the user's stated breadth,
   not the skill's guess at it.

**Seed, not the final set.** This init capture is deliberately a **seed** — it
does not assume every behavior is knowable at init. *Additive growth* of the set
as new behaviors surface while drafting specs is **slice 068-02's** scope, not
slice 01's; this skill ships the initial capture only.

**Overridable.** The `## Use cases` section is a normal vision slot: the
per-section **skip** mechanic applies (skipping writes the `status: skipped`
marker and leaves the section empty — valid for project classes where breadth
modeling adds nothing, e.g. a single-flow CLI or a library), and the
[Re-run protocol](#re-run-protocol)'s hash-based divergence detection applies to
it on re-run like any other filled section. The capture loop above governs the
**initial** capture session.

The capture loop + normalize + confirm + the no-infer question are demonstrated
end-to-end in [`worked-example-yarnfinder.md`](worked-example-yarnfinder.md).

## Worked examples

Two annotated transcripts ship with this skill:

- [`worked-example-jig.md`](worked-example-jig.md) — runs the
  elicitation against jig's own pitch (the README's "what it does"
  + the audit-stage positioning recovery story). Produces
  **template-shaped output** with the 10 H2s defined by
  `templates/docs/product-vision.md.template` (Identity / Target
  users / Core problem / Competitive landscape / Scope / Use cases /
  Stack / Design principles & constraints / How new work enters /
  Open questions). The worked example explicitly acknowledges the H2-name
  divergence from the hand-seeded `docs/product-vision.md` (which
  predates the template and uses bespoke H2 names like "Vision
  statement" / "Future scope" / "References"). **The template is
  the structural ground truth for elicitation output shape** — if
  the skill produces H2s that don't match the template, something
  is wrong.
- [`worked-example-yarnfinder.md`](worked-example-yarnfinder.md) —
  runs the elicitation against the YarnFinder pitch described in
  `/Users/ramboz/Projects/AGENTS.md`. Demonstrates a different
  project shape (consumer product vs. dev tooling) and shows how
  YarnFinder's bespoke concepts (Data sourcing, Recommended slice
  order, prioritized backlog) map to the template's slots. Two
  shapes keep the question set honest.
- [`worked-example-rerun.md`](worked-example-rerun.md) — runs the
  elicitation a *second time* against jig's vision doc, with one
  section manually edited between runs. Demonstrates the re-run
  protocol's divergence detection + the three-choice resolution
  (refresh / skip / diff) end-to-end. Required reading for any
  re-run invocation.

## Re-run protocol

Slice 017-03 added re-run mechanics. When a section's marker is
`status: filled` and the user invokes the skill again, the skill
must detect whether the section body has been hand-edited since
last elicitation. If it has, the skill warns before overwriting.

The protocol is four steps per section:

1. **Read** the section's marker comment. Three states matter:
   - `status: unfilled` → eligible for elicitation, no hash check needed
   - `status: skipped` → offer fresh Q&A. A re-run is the natural
     moment to revisit a previously-skipped section; no hash check
     applies (skipped sections have no canonical body).
   - `status: filled / hash: sha256:<12hex>` → run the next three steps
2. **Compute hash** of the section's current body (bytes between the
   marker line and the next H2 heading; whitespace-trimmed at both
   ends; SHA-256, first 12 hex characters of the digest).
3. **Compare** the computed hash to the marker's `hash:` field. If they
   match, the section body is unchanged since last elicitation — safe
   to re-elicit silently. If they diverge, the user has hand-edited
   the section between runs.
4. **Surface decision.** On divergence, the skill warns inline:
   > *"Section `<H2 name>` has been manually edited since the last
   > elicitation pass (hash mismatch). Refresh, skip, or diff?"*
   Three choices:
   - **refresh** — discard the hand-edits and re-run the Q&A for this
     section. The new answer replaces the body; the marker's date +
     hash are updated.
   - **skip** — keep the hand-edits as-is. The marker is updated to
     `status: filled` with today's date and the *new* hash (so future
     re-runs see the hand-edited body as the new baseline). No Q&A
     happens for this section in this run.
   - **diff** — print a unified diff of the hand-edits against the
     last-elicited body, then re-prompt with refresh / skip choices.

### Per-section refresh

A user can target a specific section explicitly via:

```
/jig:vision-elicit --section "Core problem"
```

This bypasses the divergence check for that section and forces a
fresh Q&A. Useful when the user knows they want to redo a section
and doesn't want to see the warning. Section name matching is
case-insensitive substring match against the template H2 names.

### Silent path: no edits, no surprises

If no sections have hand-edits (all hashes match), the re-run is
silent — only sections still `unfilled` get elicited. This is the
common case after a brief gap (re-run today's elicitation tomorrow
to fill the sections that were skipped).

### Implementation note

The skill computes the hash inline using `hashlib.sha256`. There is no
`.py` helper for this — same judgment-only shape as the rest of the
skill. The hash algorithm + prefix length are fixed by
[`docs/conventions.md`](../../docs/conventions.md) "Elicitation slots"
rule; do not vary them.

## Gotchas

- **The deferral hint is the routing mechanism, not a code path.**
  Same as pr-review and arch-review: jig's description tells the
  Codex router "prefer any other installed skill whose
  description identifies it as handling vision elicitation, product
  discovery, project framing, or product scope capture." There is no
  filesystem probe, no plugin-precedence lookup. The deferral is
  category-based: a user skill named anything that claims the
  discovery / framing surface will win.
- **Lightweight is a feature.** This baseline does not run multi-
  persona facilitation, does not impose a lean-canvas template, does
  not produce a JTBD framework artifact. If you find yourself wishing
  the baseline did more, you are in the target audience for installing
  a richer skill at the user scope.
- **No state machine.** This skill does not transition spec slice
  state markers (that's `spec-workflow`), does not write ADRs (that's
  `adr-workflow new`), and does not enforce the conventions gate
  (that's `jig-spec-gate`). It only writes content into the slots that
  slice 017-01 introduced.
- **Re-runs are protected by hash-based divergence detection.** See
  the "Re-run protocol" section above. The skill computes a SHA-256
  hash of each `filled` section's body and stores it in the marker;
  on re-run, it recomputes and compares before overwriting. If a user
  has hand-edited a section between runs, the skill warns and offers
  refresh / skip / diff before touching the body. Skipped sections
  are offered fresh Q&A on re-run (no hash check — they have no
  canonical body).
- **Fallback mode** (if the routing-dogfood in spec 017-02's AC #9
  ever fails): the SKILL.md frontmatter gets `disable-model-invocation:
  true` and this skill becomes explicit-invocation-only
  (`/jig:vision-elicitation`). In that mode, no auto-trigger fires —
  the user has to type the slash command. If you see
  `disable-model-invocation: true` in this skill's frontmatter,
  that's why.

## Relationship to other skills

- **`/jig:scaffold-init`** — produces the empty slots this skill
  fills. The two skills compose: scaffold-init creates the templates,
  vision-elicitation populates them.
- **`/jig:spec-workflow`** — sibling. Spec-workflow drives the
  what-we-build-next surface; this skill defines the what-the-project-
  is surface that spec-workflow operates within.
- **`/jig:adr-workflow new`** — produces ADRs from named decisions.
  Slice 017-04 (deferred) will add an optional seed-ADR pass at the
  end of Section 7 (Tech stack) that calls `adr-workflow new` for any
  locked-in decision the user names. Until 017-04, ADR seeding stays
  manual.
- **`/jig:memory-sync`** — orthogonal. Memory-sync captures
  cross-session learnings (hot cache, glossary, learnings); this
  skill captures project-level positioning. Different surfaces.
