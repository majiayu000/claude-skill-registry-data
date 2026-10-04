---
name: case-study-writer
description: Write, restructure, edit, or strengthen UX/UI portfolio case studies, portfolio pieces, project stories, and interview narratives from supplied product-design evidence. Extract proof, clarify individual and team ownership, connect decisions to outcomes, plan visuals, and handle confidential results. Trigger on "write my UX case study", "improve this portfolio project", "create a portfolio piece", "review my design portfolio", "prepare an interview case study", or "structure this design story". Do not invent research, metrics, quotes, outcomes, or a linear process.
metadata:
  version: "1.1.0-main"
  argument-hint: "[project notes, artifacts, role, audience, and outcomes]"
---

# Case Study Writer

Write a decision story, not a process diary. Show what changed in the team's understanding, what the author specifically contributed, why key choices were made, and what evidence supports the result.

## 1. Define audience and format

Identify:

- target role, seniority, company type, and reviewer needs;
- format: portfolio page, interview deck, PDF, application excerpt, or verbal walkthrough;
- expected reading time and confidentiality constraints;
- competencies the project can genuinely demonstrate.

Optimize the same evidence differently for a recruiter scan, hiring-manager review, craft critique, and cross-functional interview. Do not make one page carry every detail.

## 2. Build an evidence ledger

Read [references/evidence-and-claims.md](references/evidence-and-claims.md). Extract only what is supported:

`Claim | Evidence | Source | Author's role | Confidence | Confidentiality | Visual candidate`

Separate:

- direct contribution from team contribution;
- observed user evidence from stakeholder opinion;
- shipped outcome from prototype result;
- measured result from directional signal;
- fact from interpretation and retrospective learning.

Ask for missing material when it changes credibility. If it remains unavailable, write around the gap transparently.

**Checkpoint:** Before shaping the story, verify that the pivotal decision and headline outcome each map to evidence or an explicit limitation. After drafting, re-check every claim against the ledger; downgrade, qualify, or remove unsupported claims, then repeat until every retained claim is supported or visibly limited.

## 3. Find the narrative spine

Use:

`Context -> Tension -> Evidence -> Decision -> Change -> Outcome -> Learning`

The tension should be a real conflict or uncertainty: competing user goals, technical limits, harmful existing behavior, ambiguous data, organizational constraint, or a failed first approach. The decision must show judgment, not merely sequence.

Draft one sentence:

`We needed to help [user] achieve [goal] despite [constraint]; evidence showed [insight], so I/we [decision], resulting in [supported outcome or learning].`

Synthetic micro-example:

- Claim: `The redesign improved task completion.`
- Evidence: `In six supplied task sessions, completion changed from 2/6 on the baseline to 5/6 on the prototype.`
- Sentence: `Prototype task completion increased from 2/6 to 5/6 in a six-participant evaluative study; production impact was not measured.`

If the spine is weak, return to the evidence ledger and re-extract the tension, decision, or supported result before polishing prose.

## 4. Select proof

Choose visuals that make a claim inspectable:

- before/after, journey, flow, or information architecture with the changed decision annotated;
- research, rejected directions, or prototype iterations with method and decision criteria;
- final behavior with relevant edge, responsive, and implementation states;
- outcome evidence with baseline, period, population, and attribution caveat.

Avoid galleries of unlabeled screens. Every visual needs a caption that states what it proves and why it mattered.

## 5. Write the story

Read [references/story-architecture.md](references/story-architecture.md). Lead with outcome and role, then reveal enough process to explain the decisions. Use plain language, concrete verbs, and short sections.

Prefer:

`I redesigned the exception workflow and facilitated two usability rounds; the product manager owned prioritization and two engineers implemented the release.`

Avoid:

`We leveraged a human-centered framework to deliver an intuitive best-in-class experience.`

Use `I` for the author's contribution and `we` for team decisions. Do not erase collaborators or hide individual ownership.

## 6. Handle outcomes honestly

Use the strongest truthful outcome class:

1. shipped user or business result with baseline and period;
2. observed task improvement in evaluative research;
3. implementation or operational result;
4. stakeholder or adoption signal;
5. validated learning and next decision;
6. unresolved outcome with a credible measurement plan.

Do not claim causality from a before/after metric without controlling other changes. Do not turn `users liked it` into `improved usability`.

## 7. Produce the case study

For a complete input-to-output demonstration, read [references/worked-example.md](references/worked-example.md). Use it to calibrate claim strength, narrative compression, attribution, and visual proof; never import its fictional project facts.

Return:

### Project card

`One-line outcome | Role | Team | Duration | Platform | Status`

### Executive summary

In 80 to 140 words, cover context, contribution, pivotal decision, and supported result.

### Full narrative

Use only the sections needed:

- Context and stakes
- My role and constraints
- What we learned
- Decisions and tradeoffs
- Iteration and validation
- Shipped experience or final direction
- Outcomes
- Reflection and next step

### Visual plan

`Placement | Artifact | Claim proved | Caption | Redaction or recreation needed`

### Evidence notes

List missing proof, attribution limits, and confidentiality transformations.

### Alternate cuts

Provide a 30-second summary and a 5-minute interview outline when useful.

## Final validation gate

Publish only when every check passes:

- the first screen or minute communicates the problem, role, pivotal decision, and strongest supported result;
- every major claim and selected visual maps to evidence or an explicit limitation;
- generic process narration, unsupported adjectives, repeated problems, and duplicate final screens are removed;
- one or two meaningful tradeoffs explain where evidence changed the direction;
- individual and team ownership are accurate and unmistakable;
- every number, quote, date, status, outcome class, and causal qualification is verified;
- confidential transformations remain honest and labeled in the polished summary;
- reflection states changed judgment or the next evidence needed.

If a check fails, return to the evidence ledger or affected section, revise it, and run the gate again.
