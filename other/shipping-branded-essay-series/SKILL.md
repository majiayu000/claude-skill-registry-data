---
name: shipping-branded-essay-series
description: >-
  Use whenever Kyle hands over a content-series brief or spec (Load-Bearing,
  FlashFusion blog, any Abstrekkt-lane essay series) and wants it turned into
  finished, brand-templated, publishable pages. Triggers on "synthesize the
  series spec", "build out the rest", "build the rest of the posts", "draft the
  series", "turn the spec into posts", "template the essays", "ship the series",
  "ship it", "build the Load-Bearing series", "renumber these essays", "make
  these into standalone pages", or any request to take a multi-post writing plan
  to shipped HTML. Use even if Kyle only says "continue" or "ship" after a spec
  exists — a bare terse command mid-series means execute this pipeline. Fires on
  Load-Bearing / Abstrekkt / FlashFusion content work even when the brand isn't
  named. NOT for LOXIHART/day-job content, a single post or newsletter issue (use
  producing-ai-newsletter for a regular issue), or the memoir — those have their
  own lanes and skills.
license: MIT
compatibility: >-
  Cowork / Claude Code. Uses parallel subagents (Agent tool) and the Projects
  tool. scripts/verify-series.sh needs bash + ripgrep or grep.
metadata:
  version: 2.0.0
  lane: personal / Abstrekkt
  author: Kyle Rosebrook
  known-gaps: >-
    Covers spec -> manuscript -> shipped HTML only; NOT platform/URL selection,
    distribution, or press outreach. FlashFusion brand block in
    references/brand-template-contract.md has confirmed color tokens but
    unconfirmed display/body fonts — confirm before first FF run.
  chains:
    - producing-ai-newsletter
    - packaging-skills
---

# Shipping a Branded Essay Series

Takes a series brief or spec and produces the full set of brand-templated,
hard-rule-compliant, publishable HTML essays — with lane enforcement, reuse
detection, protected-material gating, and adversarial verification before
delivery.

## TL;DR

Read ground truth first. Draft the content as a reviewable manuscript. Template
into standalone HTML from ONE reference file via parallel subagents. Scan for
forbidden terms before delivery. Gate anything that touches a protected lane or
unconfirmed fact — never guess it clean.

The moat is not the writing. It's the enforcement: employer never surfaces, no
fabricated numbers, memoir material stays cut, reused assets get renumbered
instead of rewritten.

---

## Reference Map

The body covers a normal run. Pull these only for the depth they name.

| You need | Read |
|---|---|
| Exact template CSS/structure per brand (Load-Bearing + FlashFusion) | `references/brand-template-contract.md` |
| The full hard-rule / lane-separation table + provenance rules | `references/hard-rules-and-lanes.md` |
| Voice rules, openers/closers, banned words | `references/voice-spec.md` |
| Subagent templating pattern + the verification scan in detail | `references/templating-and-verification.md` |
| Which brand, reference-essay path, project store, act names | `assets/config.md` |
| The acceptance gate before shipping | `assets/success-criteria.md` |
| Runnable pre-delivery verifier | `scripts/verify-series.sh` |

---

## Decision Tree

```
Do I have ground truth (project instructions, voice spec, existing essays)?
  ├─ No  → project_read/project_search FIRST. Read the voice files and one
  │        shipped essay for the exact template. Do not draft from the brief alone.
  └─ Yes → continue.

Does the brief conflict with ground truth?
  └─ Flag it explicitly. Do NOT average. Ground truth wins; say so.

Which brand is this series?
  └─ Read assets/config.md. If active brand unset → ask (config pattern).
     Load the matching block in references/brand-template-contract.md.

For each planned post — material status?
  ├─ Fully sourced, no protected lane        → draft it
  ├─ Reuses an existing shipped essay         → RENUMBER (badge edit), do NOT rewrite
  ├─ Touches memoir / clinical / [PERSON]      → CUT-FORM only, or gate for Kyle's call
  ├─ Touches the day-job / employer           → GATE. No anonymization salvages it.
  └─ Depends on an unconfirmed fact/date      → GATE. Draft around needing it.

Output stage?
  ├─ First pass  → content-first MANUSCRIPT (one .md, all posts, footers).
  │                Let Kyle correct the voice before HTML locks.
  └─ On "ship"   → template each into HTML from ONE reference file, in parallel.

Before delivery → run scripts/verify-series.sh. Resolve every hit's context
(substring false positives are common). Only then SendUserFile + project_write.
```

---

## Usage Examples

**Example 1 — Spec first**
```
User: "Synthesize the series spec for the first published blog series (14 posts)."
→ Read ground truth + voice files. Propose 3 spines, pick one, justify.
→ Map each post to a real inventory item or flag [NEEDS MATERIAL].
→ Detect reusable existing essays; flag protected-lane posts as GATED.
→ Deliver the spec with CLAIMS/GAPS footers. Do NOT draft essays yet.
```

**Example 2 — Build the rest**
```
User: "Build out all the rest."
→ Draft every buildable post in ONE manuscript .md (content-first, reviewable).
→ Reused posts = renumber note, not a rewrite. Gated posts = held with reason.
→ Per-post CLAIMS/GAPS. Flag any tonal-sameness risk across similar posts.
```

**Example 3 — Ship**
```
User: "ship"
→ Template each drafted post into standalone HTML from ONE reference file, in
   parallel (one subagent per post, character-for-character prose).
→ Renumber reused essays via badge edit. Run scripts/verify-series.sh.
→ Resolve scan hits → SendUserFile + project_write.
```

---

## The 7-Step Pipeline

1. **Ground truth before drafting.** `project_read`/`project_search` the project
   instructions, voice files, and one shipped essay. Flag brief-vs-truth
   conflicts — don't reconcile silently. Material can be split across project
   stores; a "missing" file may live in the other store.

2. **Enforce hard rules / lane separation.** These are FAIL conditions — one
   violation kills the post. Full table + provenance rules:
   `references/hard-rules-and-lanes.md`.

3. **Detect reuse — renumber, don't rewrite.** If an existing shipped essay
   already covers a slot, change only the badge + footer meta. Project docs are
   full-replace only; reproduce from a fresh read. See
   `references/templating-and-verification.md`.

4. **Gate protected / unconfirmed material.** Do not guess a post clean. Hold it,
   state the exact confirmation needed, and note the count impact. Draft the rest
   around not needing it.

5. **Content-first manuscript, then template.** Draft all buildable posts as ONE
   markdown manuscript so Kyle can correct voice before HTML locks. On "ship",
   template in parallel — one subagent per post. Pattern + brand template:
   `references/templating-and-verification.md`, `references/brand-template-contract.md`.
   Voice: `references/voice-spec.md`.

6. **Adversarial verification before delivery.** Run `scripts/verify-series.sh`
   over the outputs. RESOLVE each hit's context — substring false positives are
   common (`spect`→"inspection"; `percentile` inside a "no percentile" line).
   Confirm template integrity: title, badge number, no editorial note leaked.

7. **Deliver with footers.** `SendUserFile` the set (attach for many files) and
   `project_write` each under `claude/`. End every deliverable with CLAIMS /
   GAPS. Name the real publish blocker (platform / live URL), not just "content
   done".

---

## Gotchas

1. **Material is split across project stores.** A file the brief calls "missing"
   may live in the Abstrekkt project while the search ran against
   ChaosCollective/Notion. Read the actual store before declaring a gap.

2. **Memoir material must be CUT, not anonymized.** The cognitive percentiles and
   "Construction, Not Recovery" sit inside a clinical record. A "bare fact, no
   origin" version still fingerprints. Default: cut. Flag as Kyle's call — it
   touches an active custody matter; don't auto-execute either way.

3. **Reuse = renumber, never rewrite.** Regenerating a shipped essay to change a
   badge is a rebuild where a two-string edit was correct.

4. **The forbidden-term scan produces false positives.** Always print context and
   confirm before treating a hit as a violation — and never treat a clean scan as
   proof of voice quality; it catches terms, not tone.

5. **Editorial notes leak into published copy.** "Cut-form note", `[NEEDS
   MATERIAL]`, manuscript scaffolding — strip them when templating. Tell
   subagents explicitly to omit them.

6. **Content-first is not optional for a first-ever public series.** Ten HTML
   files locked from unreviewed voice is a gamble. Manuscript first.

7. **Watch tonal sameness across similar posts.** Posts sharing a rhetorical move
   (name a number/credential, then undercut it) read fine alone and samey in a
   run. Flag which cluster to differentiate.

8. **Terse command mid-series = execute.** "ship" / "continue" / "build the rest"
   after a spec exists means run the pipeline with documented defaults, not ask
   more questions. State the defaults, proceed.

9. **Overlaps `producing-ai-newsletter` — Load-Bearing IS the newsletter.** This
   skill owns the multi-post *series → shipped HTML* pipeline. A single regular
   newsletter issue belongs to `producing-ai-newsletter`. Chain, don't collide.

---

## Self-Verification Checklist

0. Ground truth (project instructions + voice files + a shipped essay) read before drafting.
1. Every brief-vs-ground-truth conflict flagged, not averaged.
2. Zero hard-rule violations (per `references/hard-rules-and-lanes.md`).
3. Reused essays renumbered (badge only), not rewritten.
4. Gated posts held with an explicit confirmation ask + count impact — none guessed clean.
5. Manuscript delivered before HTML (unless Kyle said ship outright).
6. HTML templated from ONE reference file; prose reproduced character-for-character.
7. `scripts/verify-series.sh` run; every hit's context resolved; no editorial note leaked.
8. Template integrity: correct title, badge number, footer meta per file.
9. `[SOURCED]` / `[GENERATED]` provenance; CLAIMS / GAPS footers on the deliverable.
10. Real publish blocker named (platform / live URL), not just "content done".

---

## Trigger Evals

Positive (must activate):
- "synthesize the series spec for the 14-post series" → activates
- "build out all the rest of the posts" → activates
- "ship" / "template these into standalone pages" after a spec exists → activates

Negative (must stay silent):
- "write me one LinkedIn post about AI adoption" → `generating-social-posts`, not this
- "draft this week's Load-Bearing newsletter issue" → `producing-ai-newsletter`, not this

---

## CLAIMS

- [SOURCED] The Load-Bearing template and hard rules — shipped essays
  `lb-essay-04`, `lb-essay-07`, and Abstrekkt project instructions (Jul 7 2026).
- [SOURCED] FlashFusion color tokens (void-dark `#0B0B14`, violet `#A855F7`) —
  project design-token artifacts.
- [GENERATED] Parallel-subagent templating from one reference file is the
  lowest-drift way to produce many consistent pages — held across 10 files with
  no drift this session.

## COUNTEREXAMPLE

- For 1–2 fully-sourced posts with no protected-lane exposure, the manuscript step
  is overhead — draft straight to HTML.
- A clean forbidden-term scan is necessary, not sufficient — it misses a memoir
  leak phrased in novel words, or a flat, off-voice closer.

## CONTRADICTIONS

! "Ship fast on a terse command" vs. "content-first manuscript" — resolved by the
  command word: "ship" templates directly; "build the rest" delivers the
  manuscript first.
! "Reuse, don't rewrite" vs. a clean arc-numbered file set — resolved by
  renumbering the reused essay into a correctly-numbered copy with the badge
  changed and content otherwise identical.
! "Cut the memoir material" (safe default) vs. its differentiation value —
  defaults to cut but must surface the tradeoff for Kyle's decision; it is his
  risk to set, not the skill's.
