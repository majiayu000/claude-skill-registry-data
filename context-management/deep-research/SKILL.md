---
name: deep-research
description: >-
  Runs a deep, survey-grade literature investigation on a research topic:
  freezes research questions, searches from multiple adversarial
  perspectives, verifies every citation, synthesizes evidence into a MECE
  taxonomy with in-sentence cross-comparison, and answers the research
  questions in an evidence-first report. Use when the user asks for a
  literature review, a survey of a field, research landscape mapping, or a
  deep dive into what is known about a topic.
license: CC-BY-NC-SA-4.0
---

# Deep Research

## Overview

The role is a senior researcher who has written strong surveys and served as
a section editor. Someone brings a research topic; the job is to map the
terrain, lay out the key works, surface the tensions and the gaps, and end
with a judgment the evidence has earned.

This is not a search engine and not a bullet-point answer. The deliverable
reads like a real survey paper: questions defined first, evidence developed
systematically, conclusions emerging from the evidence rather than announced
up front and back-filled.

## When to use this skill

- "Survey this direction for me." "What is the state of X?"
- "What are the key works, debates, and open problems in this area?"
- "I need a literature review before committing to this topic."

## When NOT to use this skill

- Judging whether one specific idea is worth pursuing: `idea-evaluator`.
- Drafting or polishing paper prose: `paper-writer`, `intro-drafter`,
  `paper-polish`.
- A quick lookup of one or two papers: plain search suffices; this skill is
  for depth.

## Capability check

- **Literature search**: a scholarly search tool if available; otherwise web
  search over scholarly indexes; otherwise shell access to public APIs
  (Crossref, Semantic Scholar, arXiv, DBLP). With no retrieval at all, this
  skill does not run: say so rather than writing a survey from memory.
- **Sub-agents**: when the environment can spawn parallel sub-agents, each
  search perspective runs as its own agent with a clean context; without
  them, run the perspectives serially yourself. The method does not change,
  only the execution.

## Step 0: freeze the research brief

Before any searching, pin down what is being investigated.

**The brief must contain research questions**: not a topic, but two or three
specific, answerable questions. They are the survey's promise; the
conclusion must answer each one.

If the user gives only a topic ("survey CRISPR for me"), convert it with one
or two clarifying questions:

- "CRISPR clinical progress" becomes RQ1: which diseases have phase-III or
  approved CRISPR therapies? RQ2: where is the safety boundary for in-vivo
  editing? RQ3: what limits accessibility?
- "social media and adolescent mental health" becomes RQ1: does causal
  (not correlational) evidence support harm? RQ2: what is the effect size?
  RQ3: who is most affected?

Brief = topic + research questions + angle + intended reader. Every later
step answers to this brief; drift is not allowed.

The strongest angles come from unexpected convergence or tension across
independent sources. The Angle gate in references/quality-gates.md gives the
tests.

## Phase 1: scout (search and verify)

Generate three to five **search perspectives** around the brief, each with
its own question and its own keywords:

- the mainstream school (who advances this direction, and with what);
- the critics (who doubts it, with what counter-evidence);
- adjacent fields (what other disciplines say about the same question);
- methodology (who challenges how the mainstream measures things:
  meta-analyses, systematic reviews);
- application and policy (what deployment or regulation evidence exists).

Each perspective searches independently, wide then narrow: a first round on
core keywords, a second round narrowed by what the first returned (method
names, dataset names, terms of art). Keyword construction patterns and the
discipline adjustments: references/search-strategy.md.

When sub-agents are available, run one per perspective in parallel; each
returns candidate works with one-line findings. Then merge across
perspectives and check blind spots: perspectives that returned almost
nothing (a real gap, or bad keywords?), sub-directions no perspective
covered, high-frequency works cited by the found papers but missing from
the pool, and discarded results that point somewhere uncovered.

**Every candidate reference is verified before use.** The two-step protocol,
five-grade verdict, and the grey-zone rule (unconfirmable means unused):
references/citation-protocol.md.

Corpus size has no quota; coverage of every sub-direction (three or more
works each) is the bar. Over-collecting is fine; the synthesis phase
filters.

## Phase 2: synthesize

With the verified corpus in hand: extract per-paper findings, cluster by
theme into a MECE taxonomy, assign works to branches, then write the
branches serially, each section citing only its assigned works. In-sentence
cross-comparison is mandatory; contradictions are presented with condition
analysis, never averaged away. The full method:
references/synthesis-framework.md.

After synthesis, run the self-adversarial review (three retrospective
questions, perspective-omission check, concession rules):
references/self-adversarial.md.

## The six gates and the iteration loop

Throughout, six internal gates guard quality (never shown to the reader):

| Gate | One line | Severity | Failure route |
|---|---|---|---|
| Angle | a judgment, or just a listing? | CRITICAL | back to Step 0 |
| Coverage | key works all found? | MAJOR | targeted re-scout |
| Citation | references real and honestly quoted? | CRITICAL | re-verify; delete inventions |
| Taxonomy | organized by theme, MECE? | MAJOR | redesign axes |
| Calibration | claim strength matches evidence? | MAJOR | re-calibrate wording |
| Weaving | in-sentence comparison present? | MAJOR | rewrite flagged sections |

Detection questions and routes: references/quality-gates.md.

The loop this creates is the point: a Coverage or Citation failure sends the
work back to scouting for a **targeted** supplement (new works append to the
corpus; the synthesis updates incrementally), not a restart. Iterate until
every gate is CLEAR and the self-adversarial pass stops finding corrections.
Depth is driven by the topic's complexity, not by a fixed round count.

## Presentation

Organize the final report as a survey paper: abstract; introduction with the
research questions; methodology; taxonomy; branches with comparison tables;
cross-branch synthesis discussion; open problems; a conclusion that answers
the RQs one by one; references. The skeleton, per-part guidance, and
formatting discipline: references/output-structure.md.

Wording strength follows the hedge ladder (claim never exceeds evidence):
references/hedge-calibration.md.

**Evidence-first narration**: the introduction poses the questions, the body
develops the evidence, the conclusion answers. The reader derives the
conclusions alongside the text instead of being told first and shown
supporting quotes after. This ordering is the survey's defense against its
own confirmation bias.

## Cross-discipline evidence standards

Switch what counts as strong evidence by field:

- **CS / AI**: benchmarks, ablations, reproducibility; note model versions
  and evaluation conditions.
- **Biomedicine**: trial phase, patient counts, follow-up length, approval
  status.
- **Social science**: causal versus correlational designs (RCT, natural
  experiments, IV); effect sizes and heterogeneity.
- **Economics and finance**: identification strategy (IV, DID, RDD);
  statistical versus economic significance.
- **Cross-disciplinary**: separate model predictions, observational
  attribution, and field experiments; carry uncertainty ranges.

Non-CS reports include the evidence-type table from the output-structure
reference so readers can weigh evidence kinds.

## Unconfirmed markers: a deliberate difference from paper prose

A survey report is a working document addressed to the researcher, so an
explicit unconfirmed marker ("[unconfirmed: no work retrieved in this
direction]") is honest signaling and is allowed, under the uniform
convention in references/citation-protocol.md. Paper prose (paper-writer,
intro-drafter) forbids all bracketed markers. The two regimes differ on
purpose; do not import this convention into paper drafting.

## Output language

The report follows the language of the user's request: a question asked in
Chinese gets a Chinese survey, English gets English. (This deliberately
differs from the drafting skills, which default to English: a survey is read
by the researcher, not submitted to a venue.) In Chinese reports, keep
technical terms in English with a half-width space around them. An explicit
language request always wins.

## Delivery

A full survey is written to a workspace file (Markdown), with the structure,
tables, and reference list intact. Short literature answers can stay in the
conversation. Capability degradations (perspectives run serially, weaker
retrieval for some literature) are disclosed in a short note.

## Boundaries with sibling skills

- Wants a verdict on one idea: `idea-evaluator`.
- Wants prose written or polished: `paper-writer` / `paper-polish`.
- The evaluator or writer discovers the user actually needs the landscape
  first: they route here.
