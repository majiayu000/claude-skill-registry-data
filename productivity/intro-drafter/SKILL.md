---
name: intro-drafter
description: >-
  Drafts the Introduction prose for a technical paper, guided internally by
  a six-paragraph flowchart: background and running example, existing
  limitations, problem essence and goal, key challenges, solution overview,
  contributions. Positions the paper as Technique or New Problem/Setting,
  aligns contributions with challenges, and weaves verified citations.
  Outputs flowing prose by default, or an outline on request. Use when the
  user asks to draft, outline, or restructure an Introduction.
license: CC-BY-NC-SA-4.0
---

# Introduction Drafter

## Overview

The Introduction is the compressed version of the entire paper. In one and a
half to two pages it must state the research object, why the problem
matters, why existing work falls short, what the paper contributes, and how
the contributions map to sections. Reviewers decide whether to keep reading
by the end of the Introduction, so the logical throughline has to be
airtight.

This skill is a **prose generator**, not an outline generator. It takes a
small set of inputs (research area, limitations, key idea, challenges,
solution overview, optional references) and produces **six paragraphs of
real Introduction prose**. The six-paragraph flowchart works underneath as
an internal scaffold and never appears in the output.

The delivered text must read as if a researcher wrote it: flowing
paragraphs, no inline tags, no "Paragraph 1: Background" headings, no
severity tables, no consistency reports. Just the Introduction.

An explicit outline is still available: see "Outline mode" below.

## Evidence rules (inherited)

This skill follows the shared evidence discipline: every factual claim
traces to the user's materials, this session's verified retrieval, or field
common knowledge; model memory is never a source; delivered prose carries
zero bracketed placeholder tags; details the user did not provide (specific
scenarios, mechanisms, magnitudes, procedures, identifiers) are omitted, not
invented.

See: references/evidence-discipline.md and references/prose-delivery.md
(shared with `paper-writer`).

## When to use this skill

- "Write the Introduction." "Draft the Intro from this idea."
- The user has a paragraph of research thinking and wants finished prose,
  not bullets.
- The user has Goal and Key Idea settled but no Introduction text yet.
- The user pastes references and asks for them woven into the Introduction.

## When NOT to use this skill

- Benchmark papers: `benchmark-paper-template` (the flowchart differs).
- Any non-Introduction section: `paper-writer`.
- Prose exists and needs polishing: `paper-polish`.
- The user wants a submission-readiness verdict: `pre-submission-reviewer`.

## Pre-check: STEM or not

The six-paragraph model (background, limitations, goal, challenges,
solution, contributions) is built for STEM and technical papers. If the
research is non-STEM by method (humanities, social science, economics,
law), do not force it through this scaffold; hand the task to `paper-writer`,
whose CER planning covers those paradigms, while all evidence rules still
apply. The test is the research method: experiments, benchmarks, models, or
algorithms come here; everything else routes to `paper-writer`.

## Core procedure (STEM)

Internal thinking first, prose second. None of the intermediate thinking is
printed.

### Step 1: paper-type positioning (internal)

See: references/paper-types.md for the Technique versus New Problem/Setting
distinction and worked examples from Alpha-SQL, AFlow, and LEAD.

- **Technique paper**: the contribution is a new method for an existing
  problem; the narrative axis is the key idea; Paragraph 3 is a short
  bridge.
- **New Problem/Setting paper**: the contribution is the problem
  formulation itself; Paragraph 3 is load-bearing.

### Step 2: plan the six paragraphs (internal)

See: references/flowchart.md for each paragraph's purpose, writing points,
and common failures.

For each paragraph, settle: its purpose; two to four concrete writing
points drawn from the user's inputs; and its gaps (what the inputs do not
yet cover). Gaps are reported to the user after the prose, never inside it.

1. Background and motivation; running example; why the problem matters.
2. Limitations of existing work (at most three).
3. Problem essence and goal; hard constraints explicit.
4. Key challenges (at most three).
5. Solution overview; one module per challenge.
6. Contributions (three or four, each mapping to a section).

### Step 3: the running example (internal)

See: references/running-example.md for the design principles and patterns.

If the user has not provided a running example, **do not fabricate one**.
The reference file's first principle is that the example is real, drawn
from real data or a real deployment. Write the background paragraph from
the user's own abstract problem description, and in the closing note ask:
"a concrete running example would make Paragraph 1 stronger; can you share
a real case from your experiments or deployment?"

### Step 4: alignment checks (internal, before writing)

See: references/contribution-patterns.md for strong versus weak
contribution patterns.

Verify silently: the running example from Paragraph 1 reappears in
Paragraph 5 or 6; every challenge answers a limitation or a hard
constraint; the goal aligns with contribution 1; challenges map one-to-one
to modules; contributions number three or four, each tied to a section,
none of them vague ("extensive experiments" is not a contribution).

A failed check is fixed in the plan before any prose is written. Never
write around a broken chain.

### Step 5: write the prose

Six flowing paragraphs, under these disciplines:

- **No paragraph labels in the output.** Natural transitions carry the
  structure ("Despite this progress, ...", "In this work, we ...", "We
  summarise our contributions as follows.").
- **Each paragraph is one block**, roughly 100-250 words, weighted by the
  paper type (see references/paper-types.md).
- **Citations**: numeric citation-sequence, `[1]`, `[2]`, ... by first
  appearance. A full six-paragraph Introduction typically weaves **15-25
  references**: 3-5 in the background, 5-8 in the limitations, 2-4 in each
  of paragraphs three to five, 0-2 in the contributions. A thin
  bibliography reads as an opinion piece. Search before writing: three to
  five retrieval rounds under different keywords build the pool, and the
  argument is organized around retrieved, verified works. A claim whose
  source cannot be found is rewritten to drop the need, never tagged. The
  prose is followed by a **References** list matching the marks
  bidirectionally. At three or more citations, run the independent
  citation-verification ladder defined in `paper-writer` (a fresh-context
  check of every entry when the environment allows it, with honest
  degradation and disclosure otherwise).
- **Numbers and claims**: no invented percentages, speedups, or benchmark
  numbers. A specific gain appears only if the user reported it; otherwise
  "improves over prior baselines", with no annotation attached.
- **Tense**: past for prior work and observations; present or future for
  the paper's own unvalidated claims ("this paper proposes"). Without
  reported results, never "we achieved" or "we demonstrated".
- **Tone pass**: before finalising, strip AI-tone signals and unsupported
  superlatives, and match verbs to evidence strength (see the "Tone
  references" section below for where the shared wordlists live).

### Step 6: a short closing note (optional, three lines at most)

After the prose (and References), at most a short plain-language note:
gaps the user should fill, a paragraph written tentatively for lack of
input, or the running-example request from Step 3. No tables, no lists, no
severity labels. Nothing useful to say means no note at all.

## What the user receives

- Six paragraphs of Introduction prose separated by blank lines, citations
  as `[1]`, `[2]`, ...
- A References list right after the prose, when citations are present.
- Optionally, one one-to-three-line plain note.

Nothing else. The full prohibition list (headings, gate results, severity
summaries, placeholder tags, process preambles) lives in
references/prose-delivery.md and is binding.

## Outline mode (on explicit request)

When the user explicitly asks for an outline instead of prose ("just the
outline", "give me the skeleton first"), return the classic structure
instead: the type positioning (type, rationale, implication), then for each
of the six paragraphs its purpose, writing points, and gaps with severity,
then the five consistency checks (running-example loop,
limitations-to-challenges, goal-to-contribution-1, challenge-to-module
mapping, contribution-to-section mapping). The same internal planning,
externalized once, on request.

## Tone references

The shared style references live with their canonical copies in
`paper-polish` (ai-tone-guardrails, academic-phrasebank,
section-conventions) and apply to this skill's prose pass; consult them
through that skill's references when finer wording support is needed.

## Cross-skill handoffs

- Introduction done, rest of the paper wanted: `paper-writer`.
- Prose in place but stiff: `paper-polish`.
- Doubts that the idea itself can carry a top-venue paper: do not write
  that into the Introduction; put one line in the closing note and point to
  `idea-evaluator`.

## Output language

Follow an explicit language request first; a named Chinese journal or
Chinese thesis means Chinese prose; otherwise default to English. Never
infer the output language from the language of the user's message.
