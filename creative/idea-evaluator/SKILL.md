---
name: idea-evaluator
description: >-
  Evaluates a preliminary research idea against a five-dimension framework
  (Higher, Faster, Stronger, Cheaper, Broader) plus idea-lifecycle and
  student-capability matching, paradigm-shift probing, and a fatal-flaws
  audit. Returns a reviewer-style verdict. Use when the user has a draft
  research idea and asks whether it is worth pursuing, asks to 'evaluate
  this idea', 'score this idea', 'assess feasibility', 'novelty check',
  'is this a good research direction', or before committing to a paper
  scope.
license: CC-BY-4.0
---

# Idea Evaluator

## Overview

This skill evaluates a preliminary research idea from the combined
perspective of a top-venue reviewer and an experienced advisor. It
scores the idea against five improvement dimensions from the
idea-generation guide (Higher, Faster, Stronger, Cheaper,
Broader), matches the idea's lifecycle against the user's actual
capability and available hours per week, probes whether the idea has
paradigm-shift potential, flags fatal flaws, and returns one of three
verdicts: Strong Accept, Accept with Revisions, or Reject and Pivot.

The goal is to kill weak ideas before the student invests months, and to
shape promising-but-underdeveloped ideas into stronger forms before
writing begins.

## When to use this skill

- The user has a draft idea and asks whether it is worth pursuing.
- The user asks for novelty check, feasibility assessment, or scoring.
- Before the user commits to a paper scope or starts implementation.
- The user is comparing two or three candidate ideas and needs a
  structured trade-off.
- The user suspects scope creep and wants an external check.
- The user mentions 'evaluate this idea', 'score this idea', 'assess
  feasibility', or 'is this a good research direction'.

## When NOT to use this skill

- The user has already implemented the idea and is writing the paper.
  Use `intro-drafter`, `tech-paper-template`, or
  `benchmark-paper-template` (separate plugin) instead.
- The user explicitly wants brainstorming of new ideas from scratch.
  Use plain conversation; see handbook 2.3 for a disruptive-innovation
  playbook.
- The user asks for review of an existing manuscript. Use
  `pre-submission-reviewer`.
- The user asks to evaluate a benchmark contribution specifically.
  Use `benchmark-paper-template` (separate plugin) in targeted mode.

## Core procedure

### Step 1: First impression and paper-type positioning

Read the user's idea description. In one paragraph, state whether the
idea reads as Novel Problem, Novel Method, or New Setting. Is the
story compelling in one sentence? If you cannot write that sentence,
the idea itself is probably not yet clear enough for evaluation; ask
the user to restate.

### Step 2: Fatal-flaws audit (early gate)

See: references/fatal-flaws.md for the ten canonical fatal flaws,
each with a detection rule and a defense strategy.

Run the fatal-flaws audit **before** the scoring steps rather than
after them. Identify at most two fatal flaws. For each, state the
flaw, cite the detection rule, and recommend a concrete defense.

**Short-circuit rule.** If any fatal flaw is tagged CRITICAL in the
severity taxonomy (single-handedly causes rejection, unfixable
within the lifecycle), stop here and emit the verdict directly:

- Verdict: Reject and Pivot.
- Output sections 1 (First impression), 2 (Fatal flaws with the
  CRITICAL flaw), and 8 (Verdict with the flaw-driven rationale)
  only.
- Do **not** run the five-dimension scoring, paradigm-shift probe,
  feasibility check, or integrity gate. Those would be decoration
  on a rejection.

If no CRITICAL flaw is found, continue to Step 3.

### Step 3: Lifecycle and capability matching

See: references/lifecycle-capability-matching.md for the six-category
lifecycle matrix, capability self-assessment rubric, and mismatch
recovery strategies.

Map the idea onto one of six categories (Application, Foundational
Theory, Cross-Disciplinary, Frontier Exploration, Data-Intensive,
Innovative Technique). Match against the user's declared capability
(effective hours per week, skill depth, theoretical versus applied
strength). Output a mismatch flag if lifecycle is shorter than the
user's realistic execution window.

### Step 4: Five-dimension scoring

See: references/five-dimensions.md for each dimension's entry
strategies, scoring rubric, and worked examples.

Score the idea on each of:

- **Higher**: effectiveness and accuracy gains.
- **Faster**: efficiency and cost reduction.
- **Stronger**: robustness, noise tolerance, generalisation.
- **Cheaper**: data, annotation, or solution cost reduction.
- **Broader**: cross-domain transplantation or unification.

Score each 1-10 with explicit evidence from the user's stated
contribution. Identify the two or three dimensions where the idea
has the highest ceiling and recommend emphasising those in the paper.

### Step 5: Paradigm-shift probe

See: references/paradigm-shift-probe.md for the four probing principles
(First Principles, Elephant in the Room, Technology Cycle, Hamming's
Rule) and the cross-reference to handbook section 2.3 when deeper
disruptive-innovation exploration is needed.

Test the idea against four questions:

1. Does it challenge a hidden assumption the field takes for granted?
2. Does it address an elephant-in-the-room problem everyone sees but
   nobody wants to touch?
3. Does it ride a technology-cycle shift (for example, LLMs making a
   previously impractical approach now feasible)?
4. If this problem solved itself, would the field change meaningfully?
   (Hamming's Rule)

Two or more yes answers means the idea has disruptive potential. Note
that, and recommend reading handbook 2.3 to deepen the thinking on
disruptive-innovation dimensions.

### Step 6: Feasibility check

Against the user's stated resources (hardware, data access, team size,
engineering skills, timeline), assess:

- Compute risk: does the experiment fit on stated hardware?
- Data risk: is the required data accessible, or does it need
  expensive annotation or private sources?
- Engineering risk: does the implementation match the user's skill
  stack?
- Timeline risk: does the estimated end-to-end duration (coding,
  experiments, writing, revision) fit within the idea's lifecycle?

If any risk is high, flag it explicitly with a suggested mitigation.

### Step 7: Integrity gate

Before emitting the verdict, run the checks in the Integrity gate
section below.

### Step 8: Final verdict

Issue one of three verdicts:

- **Strong Accept**: execute now. Two or more dimensions at 8+, no
  fatal flaws, capability match green, lifecycle fit.
- **Accept with Revisions**: pivot the scope per recommendations
  before starting. Some dimensions weak, fixable flaws, or lifecycle
  mismatch that can be shortened.
- **Reject and Pivot**: do not pursue this version. Dominated by a
  prior benchmark or method, unfixable capability mismatch, or more
  than one fatal flaw.

Emit the evaluation in the Output format below.

## Integrity gate

Each bullet is tagged with an enforceability class. [inspection]
means the LLM can verify the bullet from the produced output alone.
[attestation] means the LLM states it has done the check, but the
user remains responsible for verification. [user-attest] means the
bullet is a user-side rule the skill cannot confirm.

Before returning the verdict:

1. **[inspection]** Every dimension score cites specific evidence
   from the user's stated contribution; no score is "gut feeling".
2. **[inspection]** Feasibility claims reference the user's stated
   resources, not generic assumptions.
3. **[inspection]** Novelty claims either cite specific prior work
   or are labelled "unverified; literature check required".
4. **[inspection]** Fatal flaws are specific and actionable; "this
   might not work" is not a flaw statement.
5. **[inspection]** Verdict is consistent with scoring: Strong
   Accept requires at least two dimensions at 8+ and zero CRITICAL
   flaws.
6. **[inspection]** Paradigm-shift claim cites which probing
   question was answered positively.
7. **[attestation]** Lifecycle prediction is reasoned from the
   field's recent pace; the user should sanity-check against their
   own knowledge of the subfield before acting on it.

If any [inspection] check fails, downgrade the verdict and mark
the corresponding output section as "needs user attention". For
[attestation] bullets, the skill states the check was run and the
user confirms the result.

## Output format

### 1. First impression
- Paper type: <Novel Problem or Novel Method or New Setting>
- One-sentence story: <...>

### 2. Fatal-flaws audit (early gate)
| # | Flaw | Severity | Defense |
|---|---|---|---|
| 1 | ... | CRITICAL or MAJOR | ... |

*If any CRITICAL flaw is present, skip sections 3-7 and go to
section 8 with verdict Reject and Pivot.*

### 3. Lifecycle and capability match
| Aspect | User's input | Assessment |
|---|---|---|
| Idea category | ... | ... |
| Lifecycle | ... months | ... |
| Weekly effective hours | ... | ... |
| Fit | ... | Green or Yellow or Red |

### 4. Five-dimension radar
| Dimension | Score 1-10 | Evidence | Lift suggestion |
|---|---|---|---|
| Higher | ... | ... | ... |
| Faster | ... | ... | ... |
| Stronger | ... | ... | ... |
| Cheaper | ... | ... | ... |
| Broader | ... | ... | ... |

### 5. Paradigm-shift probe
| Probe | Yes or No | Rationale |
|---|---|---|
| First Principles | ... | ... |
| Elephant in the Room | ... | ... |
| Technology Cycle | ... | ... |
| Hamming's Rule | ... | ... |

Disruptive potential: <none, possible, strong>.

### 6. Feasibility
| Risk | Level | Mitigation |
|---|---|---|
| Compute | ... | ... |
| Data | ... | ... |
| Engineering | ... | ... |
| Timeline | ... | ... |

### 7. Integrity gate result
- Gate 1 through 7: <pass or fail>

### 8. Verdict
**<Strong Accept or Accept with Revisions or Reject and Pivot>**

Top three actions to take first:
1. ...
2. ...
3. ...
