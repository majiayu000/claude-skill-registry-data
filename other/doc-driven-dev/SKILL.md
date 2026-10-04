---
name: doc-driven-dev
description: 'Reusable doc-driven development process for any project that keeps living design docs. Drives non-trivial engineering work through a cited evidence base (an architecture map), a PRD, an ADR set, and a tech spec — and keeps all of them in sync with the code as work lands. Use this whenever starting a unit of work ("start work on X", picking up a feature or ticket), making or recording a design decision ("should we…", "how do we decide/record this", "write an ADR"), authoring or updating a PRD / ADR / tech spec, or completing and shipping work whose docs must stay current ("mark this done", "keep the docs in sync", "what''s the definition of done"). Also use when bootstrapping a project''s docs/ structure. Reach for it even when the user doesn''t say "docs" — any load-bearing decision or any completed work whose rationale should be recorded is in scope. Orchestrates the doc-coauthoring and grill-with-docs skills as sub-tools.'
---

# Doc-Driven Development

A process for making the documentation the *spine* of engineering work rather than an afterthought. The premise: a design decision that isn't recorded with its reasoning will be re-litigated; a requirement that lives only in someone's head can't be verified; a spec that drifts from the code is worse than no spec. So work flows **through** the docs — they are both the plan and the durable record — and every claim in them is grounded in cited evidence.

This skill is the **umbrella process**. It calls two sub-skills when it needs them: `doc-coauthoring` to draft a document section-by-section, and `grill-with-docs` to interrogate a decision that isn't yet clear. Use those for the *how* of writing; use this for the *when* and the *shape*.

## The three moments

Almost everything maps to one of three moments. Identify which you're in, then follow that mode.

| Moment | Trigger | Mode |
|--------|---------|------|
| **Start work** | new feature/ticket; "let's build X" | Investigate → frame in the PRD |
| **Decide** | a design question; "should we…"; a decision worth recording | Clarity test → draft or grill → ADR |
| **Complete** | finishing a change/PR/phase; "mark this done" | The definition-of-done ritual |

## The document structure

Every project this process touches converges on one layout. If it's absent, **bootstrap it** (create files lazily — only when there's something real to put in them):

```
docs/
├── README.md            project charter: locked decisions, must-haves, doc index
├── PRD.md               what / why / for-whom (product requirements)
├── SPEC.md              how (architecture, data model, interfaces, rollout)
├── architecture-map.md  the evidence base: how the system is actually built, with file:line
└── adr/
    ├── README.md        decision index + statuses
    ├── 0000-template.md
    └── NNNN-<slug>.md     one record per decision
```

Why this split: the PRD answers *what/why* (stable, product-facing), ADRs capture *individual decisions + their rationale* (so future readers don't ask "why on earth did they do it this way?"), the spec describes *how it's built* (and is kept matching reality), and the architecture-map is the **shared evidence base** that ADRs and the spec both cite — so claims trace to code rather than to memory. Templates for each live in `references/templates.md`.

## Mode 1 — Start work

Goal: never plan on a guess.

1. **Locate or bootstrap `docs/`.** If the charter/PRD/spec/map don't exist, create the ones you need now and leave the rest for when they earn their place.
2. **Investigate first.** Map the part of the codebase the work touches and write distilled findings into `architecture-map.md` with `file:line` anchors — the seams, the call sites, what's coupled, what breaks if you change it. For a large surface, fan out parallel read-only agents and have each return a *summary* (not file dumps); for a small one, read it yourself. The rule is simply: **no plan without grounding.**
3. **Frame the work in the PRD.** Tie it to a problem/goal and place it in scope (in/out) and a phase. If the work implies new requirements, add them — marked clearly as draft until confirmed.
4. **Surface the decisions the work requires** and hand each to Mode 2. Most "start work" turns produce one or more decisions before any code is written.

## Mode 2 — Decide

Goal: every load-bearing decision is recorded, grounded, and reversible-with-context.

**The clarity test** — for each decision, ask two questions:

> Is the **what** (what we'd actually do) *and* the **why** (the drivers/rationale) both clear *and* grounded in evidence?

- **Yes → draft the ADR directly.** Use the ADR template; fill *Technical context* with cited evidence from the map, and *Considered options* + *Decision* + *Consequences* with the real trade-off. Status: `Accepted`. If the document is long or the section is subtle, run `doc-coauthoring` to build it collaboratively.
- **No → grill first.** Run `grill-with-docs` on that decision: it interviews one question at a time, each with a recommendation, walking the dependency tree until the *what* and *why* are sharp. Status: `Needs-grill` until resolved, then draft as above.

**Recording the decision:**
- One ADR per decision. Add it to `docs/adr/`, update the index (`adr/README.md`) with its status.
- When a past decision changes, **supersede — don't rewrite history**. Add a new ADR and set the old one's status to `Superseded by NNNN`. The trail of *how thinking evolved* is part of the value.

**Offer an ADR sparingly.** A decision earns an ADR only when it's (1) hard to reverse, (2) surprising without context, and (3) the result of a real trade-off. If any is missing, it's just a normal implementation choice — skip the ceremony.

## Mode 3 — Complete

Goal: the docs and the code never drift. A change is not "done" when the code works — it's done when the record is true again.

**Definition-of-done ritual** — before calling work complete, walk this list:

1. **PRD** — mark the requirement / phase item delivered.
2. **ADRs** — capture any new decision made during the work; supersede any prior ADR the work *changed*; and **reconcile any prior ADR the work *contradicted*** — if investigation proved an existing ADR's evidence or scope wrong, correct it in place (see the contradiction rule under *Cross-cutting rules*). Do not leave the contradiction merely flagged.
3. **SPEC** — update the affected section to match what was *actually built* (not the aspiration you started with).
4. **architecture-map.md** — refresh it if seams, structure, or key call sites moved; re-verify the `file:line` anchors you cited.
5. **Verification gate** — run the project's gates (tests, lint, type-check, and any project-specific invariant — e.g. a network-egress audit, a performance budget). Record that they passed.
6. **Changelog / worklog** — write one entry describing the change and why.
7. **Cross-references** — confirm the links between docs (index ↔ ADRs ↔ spec ↔ map) still resolve.

If you find yourself reluctant to update a doc because "it's just a small change," that's exactly the drift this process exists to prevent — small unrecorded changes are how a spec rots.

## Cross-cutting rules

- **Evidence standard.** Every factual claim in a doc cites proof — a `file:line`, an architecture-map section, command output, or an external spec/URL. The ADR *Technical context* and *References* sections exist to enforce this. An unsourced assertion is a future bug.
  - **Verify at the moment you cite — never only after.** A `file:line` you write is a claim you are making *now*; open the source and confirm it before the line ships, **especially** when you're copying the anchor out of `architecture-map.md`. Line numbers drift, and re-stamping a stale map line into the spec launders unverified data as freshly checked. If you won't re-verify a specific line, cite the map *section* and let the map own the line number. (The completion-ritual re-verification is a backstop, not the primary control — by then the wrong number has already been read and trusted.)
  - **A consequence-claim needs the consequence verified, not just the thing.** "Safe to remove X", "nothing depends on this", "this is the only caller" are claims about the dependency *graph*, not about X — confirm them with a dependents/callers search, not by reading X alone.
- **Decision lifecycle.** ADR statuses are `Proposed → Needs-grill → Accepted → Superseded`. Keep the index current so the decision set stays legible at a glance.
- **Docs are a deliverable**, sequenced *with* the code, not after it. The completion ritual is part of the work, not overhead bolted on at the end.
- **The map is shared truth.** Don't duplicate codebase facts into each ADR/spec section — state them once in `architecture-map.md` and cite it.
- **Reconcile contradictions on sight; a flag is not a resolution.** When verified evidence contradicts an existing doc — an ADR (even Accepted/locked), the spec, or the map — fix the doc; don't just annotate it and move on. A ⚠️ note records that you *noticed*; it does not make the record true again, and it rots into a permanent lie that the next reader trusts. Distinguish two cases:
  - **A factual error in the evidence layer** (wrong line, mischaracterized seam, wrong crate bucket, an overstated scope) → **correct it in place**, date-stamped, with a one-line note of what it said before and why it changed. This fixes evidence, it does *not* reverse a decision, so it does not violate "supersede, don't rewrite history."
  - **The decision itself is wrong or outdated** → **supersede** with a new ADR and set the old status to `Superseded by NNNN`.

  Never end work with a known doc-vs-evidence contradiction left open — including investigation that only *touched* an ADR without "changing" it. "Defer to the author" is not available: for the change in front of you, you are the author of record.
- **Phase the roadmap.** Sequence work so each phase is independently usable; define what "fully done" means up front so scope can't quietly shrink to an MVP.

## Templates and a worked example

- `references/templates.md` — copy-ready scaffolds for the charter, PRD, SPEC, architecture-map, ADR, and the ADR index. The ADR template is Michael Nygard's format extended with MADR-style *Decision drivers* / *Considered options*, plus *Technical context* (the cited evidence layer) and *References*.
- `references/example-adr.md` — a complete, real ADR showing the bar for the *Technical context* and *Consequences* sections.

## Working with the sub-skills

- Use **`grill-with-docs`** the moment the clarity test fails — don't try to draft your way out of genuine uncertainty. The grill resolves it and updates the docs inline as decisions crystallize.
- Use **`doc-coauthoring`** when a document (or a meaty section) needs to be built up collaboratively rather than dropped in fully formed — it runs context-gathering → section-by-section drafting → reader-testing.
- This skill decides *which* document, *which* mode, and *whether to draft or grill*; the sub-skills handle the writing mechanics.
