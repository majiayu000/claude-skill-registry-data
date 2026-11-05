---
name: expository-research-writing
description: >-
  Write or revise mathematical research papers in Olivier Bousquet's preferred
  expository style: self-contained for motivated non-experts, rich in background
  and intuition, explicit about motivation and prior work, visually organized
  with diagrams/tables, progressively disclosed from overview to full proof
  detail, and candid about limitations and applicability. Use when drafting,
  restructuring, completing, reviewing, or polishing LaTeX papers,
  introductions, theorem sections, proof sections, examples, related-work
  sections, or submission-ready manuscripts.
---

# Expository Research Writing

Use this skill to make a mathematical paper teach the area while presenting new results. The target
reader is a motivated mathematician or theoretical researcher who may not be an expert in the
specific subfield.

## Core Style

- Make the paper self-contained around its main ideas: define central objects, notation, examples,
  and standard background before relying on them.
- Explain why the problem is interesting, what was known before, where the new results sit, and what
  they do not settle.
- Use intuition as a guide to formal content, not as a substitute for it.
- Prefer standard mathematical prose. Avoid internal campaign terms, vague proof-process words, or
  invented labels unless they are formally defined and genuinely useful.
- Give the reader multiple entry points: a quick conceptual read, a theorem-level read, and a full
  proof-level read.

## Paper-Level Architecture

When drafting or restructuring, aim for this progression:

1. **Motivation and landscape.** State the mathematical question, why it matters, and how it connects
   to known themes.
2. **Background for non-experts.** Introduce the area, standard examples, terminology, and the
   minimal prior results needed to understand the contribution.
3. **Definitions and running examples.** Give formal definitions together with small worked examples
   that can be revisited throughout the paper.
4. **Main results at a glance.** Present the main theorems, their hypotheses, their relation to
   previous results, and their limitations.
5. **Proof strategy before proof details.** Explain the route, key reductions, and new ingredients
   before the technical proof.
6. **Detailed proofs.** Give complete rigorous arguments with signposted lemmas, all cases handled,
   and dependencies explicit.
7. **Consequences, limitations, and open directions.** Discuss applicability, examples covered or not
   covered, sharpness, failure modes, and natural next questions.

Do not turn the introduction into a chronological research log. It should describe the current
mathematical state and the reader's path through the paper.

## Progressive Disclosure

For each major result, build layers:

```text
One-sentence statement of the point:
Informal version:
Precise theorem:
Example showing the theorem in action:
Proof roadmap:
Key lemmas and dependencies:
Full proof:
Limitations or boundary cases:
```

The first pass should tell the reader what is true and why it is plausible. The second pass should
explain the proof architecture. The final pass should supply every technical detail.

## Background And Prior Work

- Include enough background that a non-expert can learn the setting from the paper.
- State standard definitions even when they are familiar to specialists, if they are central to the
  argument.
- Explain how earlier results relate to the present theorem: weaker/stronger, orthogonal,
  incomparable, special case, generalization, different hypotheses, or different method.
- Avoid unsourced priority claims. If saying a result is new, sharp, optimal, or improves prior
  work, cite the precise comparison or state it as a clearly delimited claim to verify.
- When the literature is broad, use a compact table or paragraph map rather than a long undirected
  list of references.

## Examples, Diagrams, And Tables

Add visual and structural aids when they reduce reader load:

- **Running examples:** small objects used repeatedly to illustrate definitions, theorem hypotheses,
  proof steps, and boundary cases.
- **Diagrams:** commutative diagrams, implication maps, posets, cubes, graph pictures, operator
  diagrams, dependency diagrams, or schematic proof-flow figures.
- **Tables:** comparison with prior results, hypothesis/conclusion matrices, examples versus
  properties, proof ingredients by theorem, status of open cases, or notation glossaries.
- **At-a-glance summaries:** one table near the main results should often show what is proved, under
  which assumptions, how it compares to known results, and where proofs appear.

Every diagram or table should carry mathematical content. Do not add decorative visuals.

## Proof Presentation

- Start long proof sections with a roadmap: main idea, reductions, key lemmas, and where the hard
  step occurs.
- State simplified or special cases first when they reveal the mechanism without obscuring
  hypotheses.
- Keep proof dependencies visible. Use phrases like "By Lemma X..." only after the reader knows what
  Lemma X contributes.
- Insert short intuition paragraphs before technical lemmas when they explain why the lemma has the
  right form.
- After a difficult proof, add a brief remark explaining which assumptions were used and what would
  fail without them.
- Do not compress a proof so much that only an expert in the subfield can reconstruct the missing
  ideas.

## Limitations And Applicability

Include a clear discussion of:

- which hypotheses are essential, known to be removable, or open;
- examples covered by the theorem and examples outside its scope;
- whether bounds are sharp, conjecturally sharp, or merely sufficient;
- which parts of the method are robust and which are tailored to the setting;
- natural follow-up problems that are mathematical rather than promotional.

Limitations should be precise and useful, not defensive disclaimers.

## Revision Checklist

Before considering a section polished, check:

```text
Can a motivated non-expert identify the objects, motivation, and main result?
Are all central terms defined before use?
Is there at least one small worked example for the main definitions/results?
Is the relation to prior work explicit and cited?
Is there an at-a-glance table, diagram, or summary where it would help?
Does each major proof have a roadmap before technical detail?
Can the paper be skimmed at theorem/idea level before reading full proofs?
Are limitations and applicability stated concretely?
Has jargon been replaced by standard terms or precise definitions?
```

When this skill conflicts with brevity, prefer clarity and reader orientation, but move routine
technical bulk to appendices when it interrupts the narrative.
