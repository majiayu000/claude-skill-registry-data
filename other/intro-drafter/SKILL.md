---
name: intro-drafter
description: >-
  Creates a sentence-level outline for a technical paper Introduction from a
  structured six-paragraph Flowchart: background and running example, existing
  limitations, problem essence and goal, key challenges, solution overview,
  contributions. Produces what each sentence should accomplish, not polished
  prose. Positions the paper as Technique or New Problem/Setting and aligns
  contributions with challenges. Use when the user asks to plan, draft,
  outline, or clarify the Introduction, especially before writing final prose.
license: CC-BY-4.0
---

# Introduction Drafter

## Overview

The Introduction is the compressed version of the entire paper. In one
and a half to two pages it must state the research object, why the
problem matters, why existing work falls short, what the paper
contributes, and how the contribution maps to section numbers.
Reviewers decide whether to keep reading by the time they finish the
Introduction, so the logical throughline has to be airtight.

This skill takes a small set of inputs (research area, limitations,
hard constraints, key idea, challenges, solution overview) and
produces a six-paragraph, sentence-level outline. For each paragraph,
it states what each sentence should do, which evidence or concept it
should contain, and what prose trap it should avoid. It does not write
final Introduction text. It enforces the rule that contributions align
one-to-one with challenges, and that every claim has a section to
deliver it.

## When to use this skill

- Before writing any Introduction prose.
- The user has finished planning but the Intro story feels fragmented.
- The user has a partial Intro and wants to restructure.
- The user asks to 'draft the Introduction', 'outline the
  Introduction', 'intro logic needs clarifying', or 'help structure
  the paper story'.
- The paper's contributions are clear, but the storyline connecting
  them is not.
- `idea-evaluator` has returned Strong Accept and the next step is
  planning the Introduction.

## When NOT to use this skill

- The paper's core idea is not yet stable. Use `idea-evaluator` first.
- The paper is a benchmark paper. Use `benchmark-paper-template` (separate plugin)
  instead; the flowchart differs.
- The user wants to polish Introduction prose that is already
  structured. Use `pre-submission-reviewer` instead.
- The user explicitly asks for final publishable Introduction prose.
  First offer this sentence-level plan, then use a writing/review skill
  only if the user confirms they want prose.
- The user wants to evaluate whether the Introduction is ready for
  submission. Use `pre-submission-reviewer`.

## Core procedure

### Step 1: Paper-type positioning

See: references/paper-types.md for the Technique versus New
Problem/Setting distinction, positioning criteria, and worked
examples from Alpha-SQL, AFlow, and LEAD.

Decide which type the paper is:

- **Technique Paper**: main contribution is a new method or mechanism
  solving an existing problem. Narrative axis is Key Idea / Mechanism.
  Goal gets one sentence in passing.
- **New Problem/Setting Paper**: main contribution is a new problem
  formulation. Narrative axis is Goal / Problem Formulation. Key
  Idea supports "why this definition is reasonable".

The positioning decides how much weight Paragraph 3 carries: in
Technique papers it is a short bridge; in New Problem papers it is a
load-bearing paragraph.

### Step 2: Paragraph-by-paragraph sentence plan

See: references/flowchart.md for each paragraph's canonical purpose,
sentence roles, and common failures.

For each of the six paragraphs, return a mini-section containing:

- **Purpose**: one sentence.
- **Target sentence count**: normally 3 to 6 sentences, adjusted by
  paper type and paragraph role.
- **Sentence plan**: S1, S2, ... bullets. Each bullet describes the
  job of that sentence, the concrete input it must use, and the claim
  boundary. Do not write a final sentence.
- **Gaps**: what the user's inputs do not yet cover for this
  paragraph. Tag each with severity (CRITICAL, MAJOR, MINOR).

Paragraphs:

1. Background and Motivation. Running example. Why the problem
   matters in the real world.
2. Limitations of existing work. At most three, each framed as
   "prior work X does not handle Y".
3. Problem essence and Our Goal. Hard constraints explicit. In
   Technique papers this is a bridge; in New Problem/Setting papers
   this is the contribution itself.
4. Key challenges. At most three, each explaining why naive
   extension of prior work fails.
5. Solution overview. Each module addresses a challenge. Expect a
   one-to-one mapping between Paragraph 4 challenges and Paragraph 5
   modules.
6. Contributions. Three or four numbered bullets. Each maps to a
   section reference.

### Step 3: Running example design

See: references/running-example.md for the design principles (real,
specific, simple-yet-complete, recurring throughout), two design
patterns (concrete-failure versus good-versus-bad), and worked
examples.

If the user's inputs do not yet include a running example, propose
two or three candidate examples and ask the user to pick. Record the
chosen example in Paragraph 1's sentence plan and make sure Paragraph
5 includes a sentence slot that reuses it. Describe this as a writing
instruction, not a polished sentence.

### Step 4: Contribution alignment check

See: references/contribution-patterns.md for strong-versus-weak
contribution patterns, anti-patterns, and the canonical mapping to
section numbers.

For each contribution bullet, verify:

- Maps to a challenge in Paragraph 4, a module in Paragraph 5, or a
  specific experiment result.
- Specific, not vague ("comprehensive evaluation" is not a
  contribution).
- Cites the section number that delivers it.
- Is phrased as a contribution plan: what the contribution must name,
  what evidence/result it must include, and which section it should
  cite. Do not emit final contribution prose.

### Step 5: Flowchart consistency check

Verify the six paragraphs form a single logical throughline:

- Paragraph 1's running example is referenced in Paragraph 5 or a
  case study forecast.
- Paragraph 2's limitations motivate Paragraph 4's challenges.
- Paragraph 3's goal aligns with Paragraph 6's contribution 1.
- Paragraph 4's challenges map one-to-one with Paragraph 5's modules.
- Paragraph 5's modules appear in Paragraph 6's contribution 2 or 3.

Any break in the chain is a CRITICAL gap.

### Step 6: Integrity gate

Before emitting the outline, run the checks in the Integrity gate
section below.

### Step 7: Output the outline

Emit the outline in the Output format below. For `interactive` mode,
do not emit; converse one paragraph at a time.

## Prose control

The output is a planning artifact, not Introduction text.

- Do not write polished paragraph prose.
- Do not write a "Goal sentence candidate" or final wording for a
  contribution.
- Do not use quotation marks around sentence candidates.
- Use imperative sentence roles, for example "S2: Name the specific
  deployment setting and cite the motivating application evidence",
  not a sentence that could be pasted into the paper.
- Keep each sentence-plan item short enough to preserve authorial
  control: normally one line, with optional `Inputs:` and `Avoid:`
  fragments when useful.
- When the user supplied little detail, mark the slot as a gap instead
  of inventing smooth prose.

## Integrity gate

All seven bullets are **[inspection]** class: the LLM verifies each
directly from its own output (counting, pattern-matching, or
comparing sections). No user-side attestation required.

Before returning the outline:

1. **[inspection]** Running example named in Paragraph 1 reappears
   in Paragraph 5 or 6 (or the Case Study forecast).
2. **[inspection]** Limitations (Paragraph 2) are at most three and
   each is specific to a named prior work or a named capability.
3. **[inspection]** Challenges (Paragraph 4) are at most three and
   each explains why a naive extension of prior work fails.
4. **[inspection]** Challenge-to-module mapping is one-to-one, not
   one-to-many or many-to-one.
5. **[inspection]** Contributions (Paragraph 6) are three or four
   and each maps to a section number.
6. **[inspection]** No contribution is vague language ("extensive
   experiments", "thorough analysis" on their own).
7. **[inspection]** Paper-type positioning from Step 1 is reflected
   in Paragraph 3's weight.

If any check fails, mark the paragraph as "needs user attention"
and do not claim the outline is complete.

## Output format

### 0. Type positioning
- Type: <Technique Paper or New Problem/Setting Paper>
- Rationale: <one sentence>
- Implication: <how Paragraph 3 weight adjusts>

### 1. Paragraph 1: Background and Motivation
- Purpose: <...>
- Running example: <...>
- Target sentence count: <3-6>
- Sentence plan:
  - S1: <what this sentence must establish; Inputs: ...; Avoid: ...>
  - S2: <...>
  - S3: <...>
- Gaps: <list with severity>

### 2. Paragraph 2: Limitations (at most 3)
- Purpose: <...>
- Target sentence count: <3-5>
- Sentence plan:
  - S1: <transition from motivation to prior-work families>
  - S2: <Limitation 1: named prior work/capability and missing property>
  - S3: <Limitation 2: ...>
  - S4: <Limitation 3 if needed, otherwise omit>
  - S5: <bridge from limitations to the problem essence, if needed>
- Gaps: <list with severity>

### 3. Paragraph 3: Problem Essence and Our Goal
- Purpose: <...>
- Hard constraints: <...>
- Target sentence count: <2-5 for Technique; 4-7 for New Problem/Setting>
- Sentence plan:
  - S1: <state the intrinsic problem property or setting boundary>
  - S2: <name hard constraints>
  - S3: <define the goal or research question as a role, not final wording>
  - S4: <connect goal to key idea or paper type, if needed>
- Gaps: <list with severity>

### 4. Paragraph 4: Key Challenges (at most 3)
- Purpose: <...>
- Target sentence count: <3-6>
- Sentence plan:
  - S1: <set up why the goal is non-trivial>
  - S2: <Challenge 1: obstacle plus why naive extension fails>
  - S3: <Challenge 2: obstacle plus why naive extension fails>
  - S4: <Challenge 3 if needed>
  - S5: <synthesis sentence linking challenges to needed design principles>
- Gaps: <list with severity>

### 5. Paragraph 5: Solution Overview
- Purpose: <...>
- Challenge to module mapping:
  - Challenge 1 -> Module A
  - Challenge 2 -> Module B
  - Challenge 3 -> Module C
- Target sentence count: <4-6>
- Sentence plan:
  - S1: <name the solution framework and its high-level principle>
  - S2: <Module A handles Challenge 1; include section pointer>
  - S3: <Module B handles Challenge 2; include section pointer>
  - S4: <Module C handles Challenge 3, if present>
  - S5: <reuse the running example or forecast the case study>
- Gaps: <list with severity>

### 6. Paragraph 6: Contributions
- Target sentence/bullet count: <3-4 contribution bullets>
- Contribution sentence plan:
  1. C1: <what the contribution bullet must name; evidence/result to include; Section <X>>
  2. C2: <...; Section <Y>>
  3. C3: <...; Section <Z>>
  4. C4: <optional; Section <W>>
- Gaps: <list with severity>

### 7. Flowchart consistency
- Running-example loop: <pass or fail>
- Limitations-challenges link: <pass or fail>
- Goal-contribution1 link: <pass or fail>
- Challenge-module mapping: <pass or fail>
- Contribution-section mapping: <pass or fail>

### 8. Integrity gate result
- Gate 1-7: <pass or fail>

### 9. Severity summary
- <n> CRITICAL, <m> MAJOR, <k> MINOR
- Top three actions first: ...
