---
name: generating-audience-tier-reports
description: >
  Use when the same underlying research or dataset needs to ship as multiple
  audience-specific documents from one source of truth — e.g. "write this for
  investors, for students, and for the general reader," "make an entrepreneur
  version and an internal-memo version of this report," "same data, different
  audiences," "multi-tier report," "persona-routed report," or "one dataset,
  five write-ups." Produces N parallel documents that share a locked fact
  layer (same companies, same numbers, same section skeleton) but diverge in
  voice, framing, and one persona-specific section. Do NOT use for a single
  audience/single document — write it directly. Do NOT use for the newsletter
  3-tier pipeline (Non-Tech/Tech Dept/AI Team) — that's kyle-os:newsletter.
license: MIT
metadata:
  version: "1.0.0"
  known-gaps: >
    Does not cover live data refresh between lane variants (all lanes must be
    generated from the same frozen fact set in the same session — regenerating
    one lane later risks fact drift against the others). Does not cover
    automated diff-checking across lanes; consistency is manually verified via
    the Fact-Lock Audit step. Does not cover more than ~6 lanes before the
    shared-fact-layer becomes unwieldy to hand-audit.
  chains:
    - nlm-core:routing-pipeline-lanes
    - correcting-ai-generated-content
    - deep-research-lcot
  source: >
    Pattern extracted 2026-07-08 from 5 Google Drive docs (2026 unicorn/VC
    landscape) generated ~15 seconds apart, each targeting a different reader
    persona from the same source data.
---

# Generating Audience-Tier Reports

## TL;DR

One research pass, N audience lanes. Freeze the facts first (companies,
numbers, sources) into a shared fact layer. Every lane inherits that layer
verbatim. Only the framing, voice, and ONE persona-specific section change per
lane. This prevents the most common failure: numbers quietly drifting between
the investor version and the student version of the same report.

## Decision Tree

```
Does every lane need the SAME underlying facts (same companies/numbers)?
├─ No → this isn't a multi-lane report, it's N separate research tasks.
│        Don't use this skill — just write each one directly.
└─ Yes
   ├─ Are there 2-6 target audiences? → proceed below.
   └─ More than 6? → known-gaps limit hit. Split into two batches with
        separate fact-lock passes, or reconsider whether some "lanes" are
        actually the same audience with different formatting.

Is this a one-off report or a recurring format (weekly/monthly)?
├─ One-off → run the Golden Path once, ship, done.
└─ Recurring → after the first run, extract the per-lane section headers
     into assets/lane-templates.md so future runs skip re-deriving voice.
```

## The Shared Fact Layer (do this before writing any lane)

Every lane must trace back to the identical fact set. Build it once:

1. **Anchor stat** — one headline number every lane opens with (e.g. "~90
   unicorns minted in H1"). If a lane restates this number differently, that's
   drift — fix it before continuing.
2. **Company table** — name, sector, valuation, one lane-agnostic fact (total
   raised, or founding year). This table is copy-pasted into every lane's
   core data section unchanged. Lane-specific columns get ADDED, not
   substituted.
3. **Source list** — whatever grounds the facts (search results, uploaded
   docs, NotebookLM export). Every lane cites the same sources; a lane
   introducing a fact not in this list is fabricating, not reframing.

If any of the three above isn't stable yet, you're not ready to fan out into
lanes — finish the research first.

## Per-Lane Skeleton

```
### [Hook Title]: [Persona-appropriate subtitle]

##### 1. [Opening Frame]
- Cold open with the ANCHOR STAT (identical number across all lanes,
  different sentence construction per voice)
- One named company from the COMPANY TABLE as the flagship example

##### 2. [Core Data Section]
| Company | Sector | Valuation | [lane-specific 4th column] |
(rows come verbatim from the shared company table — do not re-derive)

##### 3. [Persona-Specific Deep Dive]  <- THE ONLY STRUCTURALLY DIFFERENT SECTION
- This is where voice and stakes diverge. See Lane Voice Reference below.

##### 4-N. [Shared Sector Sweeps]
- Same sub-topics, same companies, across every lane (only prose changes)

##### Final. [Lane-Specific Close]
- Reframes the doc's thesis for that persona's stakes in one line
```

## Lane Voice Reference

| Lane | Opens With | Section 3 Becomes | Closes With |
|---|---|---|---|
| Analyst / general reader | Provocative rhetorical framing | Narrative "frontier markets" exploration | Unresolved rhetorical question — no verdict |
| Institutional / internal memo | "As partners, we must..." | Named-firm investment theses ("Institutional Playbooks") | Numbered "Strategic Takeaways" |
| Educational / student | "As a student, you must..." | Tiered taxonomy + glossary callouts, CSV-style tables allowed | Reflective "ask yourself" prompt |
| Entrepreneur / practitioner | Direct address, "you" voice | Paired case-study comparison (fast path vs. slow path) | Bulleted "formula" — replicable takeaways |
| Formal intelligence briefing | Highest register, no rhetorical flourish | Heatmap / ranked-signal framing | Imperative "Strategic Outlook" bullets |

Add or remove rows for whatever lanes the task actually needs — don't force
all 5 if only 2 are wanted.

## Mechanical Constants (apply to every lane, no exceptions)

- Title uses `###`, numbered body sections use `#####` (skip `##`/`####` —
  keeps heading depth consistent across lanes so they diff cleanly)
- Company names **bolded** on first mention per section, valuation in parens
  immediately after
- Standard tables: pipe-delimited markdown. CSV-style comma tables are
  reserved for the educational lane only — don't mix formats within a lane
- The anchor stat and company table numbers must be byte-identical across all
  lanes. If you catch yourself typing a different number in lane 3 than lane
  1, stop and fix the shared fact layer, not the individual lane

## Fact-Lock Audit (run before shipping any lane batch)

1. Pull the anchor stat from every lane — do they match verbatim?
2. Pull every company's valuation from every lane it appears in — any
   mismatch is a ! CONTRADICTION, not a style choice. Fix immediately.
3. Confirm no lane introduces a company or number absent from the shared
   fact layer.
4. Confirm section 3 (the persona section) is the only section with
   materially different content across lanes — if sections 1/2/4+ have
   diverged in substance (not just phrasing), the lanes have forked
   incorrectly.

## Example Trigger Phrases

- "Write this market research as an investor memo, a student guide, and a
  general-audience article — same data."
- "I need this same report in three registers: internal, external, and
  entrepreneur-facing."
- "Take this NotebookLM export and fan it out into audience-specific
  versions."

## Self-Verification Checklist

```
1. Shared fact layer built and frozen before any lane was drafted
2. Anchor stat identical (verbatim) across every lane
3. Company table numbers identical across every lane that includes them
4. Only section 3 (persona deep dive) differs in substance between lanes
5. Heading depth consistent (### title, ##### sections) across all lanes
6. CSV-style tables used only in the educational lane, if present
7. Fact-Lock Audit run and passed before delivery
8. No lane fabricates a source or number outside the shared source list
```

## CLAIMS

- [SOURCED] Structural pattern (heading depth, section order, per-lane voice
  divergence limited to one section) extracted directly from 5 Google Drive
  documents generated in the same ~15-second window, 2026-07-08.
- [GENERATED] The recommendation to freeze a shared fact layer before
  drafting lanes is a reasoned safeguard against fact drift — not observed as
  an explicit step in the source docs, inferred from the risk the pattern
  creates.

## COUNTEREXAMPLE

- The source docs did NOT include an explicit fact-lock or audit step — they
  were generated in parallel with no visible cross-check. The audit step in
  this skill is a hardening this skill adds, not something the source
  material demonstrated doing correctly (see the Recursive/Recursive
  Intelligence valuation discrepancy flagged during extraction).

## CONTRADICTIONS

! Source doc 3 (Student lane) lists "Recursive Intelligence" at $4B while
  docs 2 and 5 list a separate "Recursive" (AI research lab) at $4.65B —
  unresolved naming collision in the original source data. Treat as a
  cautionary example of exactly the drift this skill's Fact-Lock Audit
  exists to catch, not as a pattern to replicate.
