---
name: paper-writer
description: >-
  Drafts publishable paper prose from the author's own materials, from a
  single paragraph to a full manuscript, across STEM and non-STEM fields.
  Every factual claim traces to user input, verified retrieval, or field
  common knowledge; citations pass an independent verification ladder;
  delivery is clean prose with zero placeholder tags. Use when the user asks
  to write a section, turn an idea or results into paper text, or draft a
  full paper.
license: CC-BY-NC-SA-4.0
---

# Paper Writer

## Overview

This skill turns a researcher's ideas and materials into submittable paper
prose. One paragraph works; a full manuscript works.

It is not an outline generator and not a writing tutor. It writes the text,
under one non-negotiable condition: every written word must be traceable to
evidence. The author owns the substance (ideas, designs, results,
conclusions); this skill owns the linguistic realization of that substance,
and nothing more.

## Hard rules

These hold for every task this skill performs:

1. Every factual claim has one of three origins: the user's materials, this
   session's verified retrieval, or field common knowledge that carries no
   numbers, names, or comparisons. Model memory is never a source.
2. Delivered prose contains zero bracketed placeholder tags of any kind. A
   claim without a source is resolved by searching, rewriting, or deleting,
   never by tagging.
3. Concrete details the user did not provide are not written: no invented
   scenarios, mechanisms, magnitudes, procedures, or identifiers.
4. Claim strength never exceeds evidence strength.
5. Real results and planned or expected results are phrased differently and
   never mixed.
6. Internal planning never leaks into the output.

The full discipline, including the evidence hierarchy and the Evidence Map:
see references/evidence-discipline.md.

## When to use this skill

- "Write this idea into an English introduction paragraph."
- "Draft the Discussion in the style of a specific venue."
- "Write a full first draft of the paper."
- "Turn these notes into a Methods section."
- "Produce an abstract."

## When NOT to use this skill

- The user wants an Introduction specifically: `intro-drafter` owns that
  section (this skill routes there automatically).
- The paper is a benchmark paper still being planned: `benchmark-paper-template`
  first, then return here for the prose.
- Existing prose needs language polishing: `paper-polish`.
- The logic skeleton is not settled: `tech-paper-template` first.
- The idea itself is unvetted: `idea-evaluator`.

## Capability check (run once per session)

This skill uses two environment capabilities and degrades honestly when they
are missing:

- **Literature search**: a scholarly search tool if the harness provides
  one; otherwise web search against scholarly indexes; otherwise shell access
  to public APIs (Crossref, Semantic Scholar, arXiv, DBLP). If none exist,
  operate closed-book: cite only user-supplied references, keep citation
  claims at citation level, and disclose in the delivery note that no
  independent retrieval was possible.
- **Fresh-context sub-agents**: used for independent citation verification.
  Without them, fall to the same-context grounding rung. The ladder and its
  disclosure rules: see references/verification-ladder.md.

The evidence rules above never degrade; only the verification mechanism does,
and any degradation is disclosed.

## Workflow

Six phases. A full paper walks all of them explicitly; a single section runs
the same phases in lighter form, but never skips Evidence or Review.

### Phase 1: Scope

Settle three things quickly, without interrogating the user:

- **Granularity**: full paper (produce working files: Evidence Map, chapter
  blueprint, then the draft) versus single section or paragraph (inventory
  mentally, deliver prose directly).
- **Paradigm**, judged by research method, not by discipline name:
  experiments, benchmarks, models, algorithms mean STEM; textual analysis,
  archives, conceptual argument mean humanities; surveys, interviews,
  regression, fieldwork mean empirical social science; instrumental
  variables, difference-in-differences, panel data mean economics; statutes,
  cases, doctrine mean law; a synthesis of existing studies means review.
  Unclear: ask one question about the core method and target venue.
- **Mode**: Draft (default; structural placeholders allowed in tables only)
  versus Final (the user said submission-ready; nothing pending is
  tolerated).

### Phase 2: Evidence

Before any words, lay out what the evidence base contains.

1. Inventory the user's materials. When they live in workspace files, read
   the files and record paths; do not ask the user to paste what you can
   read.
2. Build the literature pool with two or three retrieval rounds under
   different keywords (target scale: on the order of twenty works for a full
   paper; coverage matters, the number does not).
3. Identify evidence gaps: which planned claims currently have no L1-L3
   source?

Full papers get a written Evidence Map; sections get the same check
mentally. Template, levels, and gate: references/evidence-discipline.md.

**Gate**: a claim with no L0-L3 source is not written as fact. Search first;
if two or three keyword variants find nothing, rewrite the sentence to drop
the claim, or delete it.

### Phase 3: Blueprint

Route by paradigm and section:

| Case | Route |
|---|---|
| STEM Introduction | hand off to `intro-drafter` (six-paragraph internal scaffold) |
| STEM other sections | references/section-guidance.md content contracts |
| Non-STEM, any section | plan each paragraph on a CER skeleton: Claim (what should the reader believe), Evidence (what supports it, at which level), Reasoning (why that evidence supports it), Role (motivate, situate, propose, execute, present, interpret, qualify, or connect) |
| Benchmark papers | plan in `benchmark-paper-template`, then return here |

For a full paper, produce a chapter blueprint as a working file: section,
role, main judgment, evidence IDs, open gaps. For STEM work, check the logic
chain end to end: limitations feed the key idea, the key idea raises the
challenges, modules answer challenges one to one, contributions cover the
modules. Broken links get fixed in the plan, never papered over in prose.

All of this is internal. None of it appears in the deliverable.

### Phase 4: Draft

Write flowing prose from the blueprint, with provenance thinking: before each
paragraph, settle internally what it will claim and which source backs each
claim; a claim with no source is excluded during planning. Write clean text
with no embedded markers of any kind.

Hard writing rules:

1. **Never generate content from model memory.** Three legitimate origins
   only (user, retrieval, L0). Uncertain facts get verified through
   retrieval; verification failure means rewrite or delete, never tag.
2. **Evidence level caps claim strength.** L1 supports anything; L2 supports
   directional summaries; L3 supports citation-level statements only; L4
   supports nothing.
3. **No invented specifics.** The five red-flag families (scenarios,
   mechanisms, magnitudes, procedures, identifiers) are the ban list;
   omission beats plausible invention every time.
4. **Separate real from planned results.** Confirmed results: "we observe",
   "results show". Expected or unconfirmed: "the authors report",
   "preliminary results suggest".
5. **Never oversell for the author.** Without evidence: "may", "shows
   promise for", "is expected to".
6. **Each section does its own job, once.** Introduction makes the reader
   care, shows the gap, states the goal. Methods let another researcher
   reproduce. Results report observations without why. Discussion explains
   why, connects to prior work, admits limits. Conclusion answers the
   Introduction. Abstract is a self-contained miniature written last. The
   same finding appears in at most three sections.
7. **No internal scaffolding in the output.** CER skeletons, paradigm calls,
   chain checks all stay silent.

### Phase 4.5: Red flags (stop signals while writing)

| The thought | The correct move |
|---|---|
| "I remember this scale has 10 items" | Stop. Uncertain. Omit the item count |
| "I recall this paper used a meta-analysis" | Stop. No full text seen. Citation level only: "X et al. (Year) studied Y" |
| "I remember this case's citation number" | Stop. One digit off is wrong. Omit the identifier |
| "This material's conductivity is roughly..." | Stop. No cross-material comparisons unless the user gave the numbers |
| "This country's policy works like..." | Stop. Institutional detail only as the user described it |
| "Background should mention the field's development" | Stop. Background claims beyond L0 need L1-L3 sources. Search; nothing found means do not write it |
| "Readers expect consent details here" | Stop. Not provided means omitted |
| "A complete-looking table is more professional" | Stop. `--` in a cell is 100 times safer than an invented value |
| "This Discussion should be fuller" | Stop. Enrich with evidence, not invented mechanisms. Short and accurate beats long and hollow |
| "This method could apply to solar farms / autonomous driving..." | Stop. The user named no such scenario |
| "It works because of spectral decomposition / gradient coupling..." | Stop. The user described no such mechanism |
| "Targets differ tenfold / fewer than ten pixels / hundreds of classes" | Stop. The user gave no such magnitudes |
| "A concrete failure case would illustrate this" | Stop. No invented domain vignettes. Use the user's own description |

### Phase 5: Review

Three parts, in order:

1. **Source recall check plus inline checklist.** Walk
   references/verification-checklist.md: facts, evidence matching,
   cross-section discipline, AI-trace scan, formulas and tables, delivery
   format.
2. **Independent citation verification.** Mandatory for full papers, Final
   mode, or three or more citations; a fresh-context sub-agent receives only
   the prose and the reference list and verifies every entry through
   retrieval. Statuses, resolution routes, and the degradation ladder:
   references/verification-ladder.md. Delivery waits until no unresolved
   problem entries remain.
3. **Know what review cannot do.** Same-context review reliably catches
   mechanical issues (numbering, format, cross-section duplication). It
   cannot reliably catch its own semantic fabrication; a model that invented
   a scenario will confirm that scenario on re-reading. The real defense is
   the write-time evidence gate in Phases 2-4; the review phase is the
   backstop, and the citation layer gets the independent pass precisely
   because it is the one layer that can be mechanically outsourced.

### Phase 6: Deliver

Deliverable and prohibitions: references/prose-delivery.md.

- Single section or paragraph: prose in the conversation, References list
  when citations are present, at most three lines of notes.
- Full paper: the manuscript written to a workspace file (Markdown or
  LaTeX), References included; Evidence Map and blueprint remain separate
  working files, available on request, never embedded in the manuscript.
- Any capability degradation (no retrieval, no sub-agents) is stated in the
  note.

## Proactive literature searching

Do not wait for the user to hand over every reference. Sparse citation reads
as an opinion piece and reviewers reject it.

Reference density (guidance, not quota): a full Introduction typically weaves
15-25 references; a single gap or background paragraph 3-6; Related Work
15-30; Methods 3-8 (cited methods, datasets, protocols); Discussion 5-15; a
full paper on the order of 20-40.

**Search before writing, not after.** Before drafting any section, run three
to five retrieval rounds under different angles: core terminology; method or
model names; application domain; venue or author names. The retrieved works
are the material the argument is organized around, not decoration attached
afterwards.

Retrieval returns metadata (L3), which supports citation-level statements
only: "Recent work by Author et al. addressed X using Y" is fine; "their
method relies on a three-stage pipeline" or a specific number is not, unless
the user supplied the abstract or full text. Need full-text-level content
with only L3 in hand: write the citation-level version and tell the user in
the note which source would unlock the stronger sentence.

If a drafted section comes out visibly under-cited, go back and search
another round, then weave real findings in. Never bridge the gap with a
placeholder.

## Citations and references

Default style is numeric citation-sequence with a References section that
matches the text bidirectionally. Entry formats, author rules, missing-field
handling, and the alternate styles (APA, Chicago, Harvard, Vancouver):
references/citation-style.md.

## Output language

Follow an explicit language request first. If the target is a Chinese
journal or a Chinese thesis, write Chinese academic prose; otherwise default
to English. Never infer the output language from the language the user typed
in: describing ideas in Chinese and submitting in English is the normal
case.

## Boundaries with sibling skills

- `intro-drafter`: Introduction prose (this skill routes STEM Introductions
  there).
- `paper-polish`: polishing existing prose, including Chinese-to-English.
- `tech-paper-template`: the pre-writing logic skeleton.
- `benchmark-paper-template`: planning benchmark papers.
- `pre-submission-reviewer`: reviewer-style audit of the finished draft.
- `idea-evaluator`: whether the idea is worth pursuing at all.

If drafting reveals that the problem is not "how to write it" but "does the
core claim hold", say so plainly in the delivery note and point to
`pre-submission-reviewer` or `idea-evaluator`. Never write a defense for a
claim the user's own data undermines.
