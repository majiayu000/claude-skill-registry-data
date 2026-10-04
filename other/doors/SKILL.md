---
name: doors
description: This skill should be used when the user asks to "classify a decision", "is this a one-way or two-way door", "apply the doors framework", "triage this decision", "how much thinking does this need", "should I decide fast or slow", "apply Bezos decision framework", "Type 1 or Type 2 decision", or wants to determine how much analysis a decision requires before acting.
version: 0.1.0
---

# One-Way / Two-Way Door Decision Triage

## Overview

Apply the One-Way / Two-Way Door decision framework (Type 1 / Type 2 decisions), articulated by Jeff Bezos in his 2015 and 2016 Amazon shareholder letters. This is a meta-analytical triage tool designed for velocity. Its primary purpose is to prevent decision paralysis by determining *how much thinking is actually required* before acting.

This is not a deep analytical framework like the other four in this toolkit. It is a pre-analytical classifier: it answers "how should I decide?" before you decide "what should I decide?" Highly analytical thinkers often make the mistake of treating all decisions as One-Way doors, deploying heavy cognitive machinery on reversible problems. This framework categorizes the decision, sets the required information threshold, and most importantly, attempts to structurally transform One-Way doors into Two-Way doors to maintain momentum.

The framework is a practitioner tool from business leadership, not academic theory. However, its core insight — that irreversibility under uncertainty creates option value — is rigorously grounded in real options theory (Dixit & Pindyck, *Investment under Uncertainty*, 1994). The vocabulary is Bezos's; the economics are sound.

## Core Methodology

1. **Classify the Door** — Determine whether the decision is reversible (Two-Way Door / Type 2) or irreversible (One-Way Door / Type 1). Reversibility is a spectrum, not a binary. Evaluate along three dimensions:
   - **Reversal cost:** How expensive is it to undo? ($100 vs. $1M are both "reversible" but very different decisions.)
   - **Reversal speed:** How long does it take to walk back? A feature flag takes seconds; a public announcement takes months of reputation repair.
   - **Blast radius:** How many people, systems, or commitments are affected? A team experiment vs. a company-wide reorganization.

   If the decision is clearly a Two-Way door, apply the 70% rule and act. If it is clearly a One-Way door, proceed to step 2. If ambiguous, treat it as a One-Way door and proceed to step 3 (transformation).

2. **Assess Information State** — How much of the relevant information do you have? Bezos prescribes: "Most decisions should probably be made with somewhere around 70% of the information you wish you had. If you wait for 90%, in most cases, you're probably being slow." For Type 2 decisions, 70% is sufficient — act now and course-correct. For Type 1 decisions, identify what specific information is missing and whether it is obtainable. If the missing information would not change the decision, you already have enough.

3. **Transform the Door** — If the decision is a One-Way door, attempt to downgrade it to a Two-Way door using these tactics:
   - **Pilot:** Test the decision at micro-scale before committing fully. Run a limited experiment, prototype, or trial that gives real data without full commitment.
   - **Decouple:** Break the decision into sub-decisions. Some parts may be reversible even if the whole is not. Execute the reversible parts now; reserve the irreversible parts for later.
   - **Painted Door:** Test demand or viability without building the full solution. Present the option to stakeholders or users and measure actual response before investing. (A well-established product/UX technique: present a feature that doesn't exist yet to measure real intent.)
   - **Stage:** Structure the commitment as a sequence of smaller investments with go/no-go checkpoints, so you can exit at each stage. This is the practical application of real options theory — each stage "purchases" the option to continue or abandon with better information.

   If none of these tactics apply, accept the decision as a genuine One-Way door and deploy heavyweight analysis (or escalate to a deeper framework).

## Key Concepts

- **Reversal Cost Spectrum:** The original framework presents a clean binary (reversible/irreversible), but real decisions exist on a continuous spectrum. A useful heuristic from Shane Parrish: cross reversibility with consequences to get four quadrants — irreversible+consequential (decide late, carefully), reversible+consequential (experiment — these are underrated), irreversible+inconsequential (decide and move on), reversible+inconsequential (decide immediately).
- **The 70% Rule:** "Most decisions should probably be made with somewhere around 70% of the information you wish you had. If you wait for 90%, in most cases, you're probably being slow. Plus, either way, you need to be good at quickly recognizing and correcting bad decisions." — Bezos, 2016 shareholder letter. This applies to Type 2 decisions. For Type 1, the threshold is higher but never 100%.
- **Disagree and Commit:** When consensus cannot be reached on a Two-Way door decision, use "disagree and commit" to maintain velocity. A participant can say: "I disagree but I'll commit to this and help make it work." This prevents the default dispute resolution mechanism, which Bezos identifies as "exhaustion."
- **Accumulation Risk:** A sequence of individually reversible decisions may collectively create irreversible path dependencies — technical debt, cultural norms, contractual obligations. The framework operates at the individual decision level and may miss this emergent irreversibility. When analyzing a sequence of Two-Way door decisions, check whether they are creating a One-Way pattern.
- **Day 1 / Day 2:** Bezos's larger philosophy: "Day 2 is stasis. Followed by irrelevance. Followed by excruciating, painful decline." Organizations enter Day 2 when they start treating every decision as a One-Way door, creating bureaucratic overhead that kills experimentation speed. The Doors framework is the operational mechanism for maintaining Day 1 velocity.
- **Framework Limitations:** The classification is perspective-dependent — what is a Two-Way door for a well-funded company may be a One-Way door for a bootstrapped team. The framework can also be weaponized to move fast irresponsibly if decisions are misclassified as Two-Way when they are actually One-Way. Accurate classification is everything.

## Analysis Protocol

### Structured Mode (default)

Produce the analysis in this exact section order:

```
## Decision Statement
[The decision under examination, stated clearly and specifically]

## Door Classification
**Type:** [One-Way Door / Two-Way Door / Ambiguous]
- Reversal cost: [Low / Medium / High — with brief justification]
- Reversal speed: [Fast / Slow — how long to undo?]
- Blast radius: [Narrow / Wide — who and what is affected?]
[One sentence summary: why this is a One-Way or Two-Way door]

## Information State
- Estimated information level: [X% — how much of the relevant information do you have?]
- Key unknowns: [What specific information is missing?]
- Would the missing information change the decision? [Yes / No / Maybe — explain]
[If Two-Way door with ≥70% information: "Sufficient for action. Proceed and course-correct."]

## Transformation Engine
[If Two-Way door: "Already a Two-Way door. No transformation needed — proceed to verdict."]
[If One-Way door, attempt to downgrade:]
- **Pilot:** [How to test at micro-scale? If not applicable, state why.]
- **Decouple:** [Which sub-decisions can be executed safely now?]
- **Painted Door:** [How to test the assumption without building the solution?]
- **Stage:** [How to structure as sequential commitments with exit points?]
[If no tactic applies: "Genuine One-Way door. Deploy heavyweight analysis or escalate to [recommended framework]."]

## Triage Verdict
[One clear paragraph: Step through now, deploy a transformation tactic, or escalate to deeper analysis. If escalating, recommend which framework (Scholastic for truth claims, Cartesian for complex systems, Pirsig for value judgments, Six Hats for multi-perspective evaluation).]

**Confidence: [0.0–1.0]** — [Brief justification for the rating]
```

### Interactive Mode

When the user requests interactive analysis:

1. Ask the user to state the decision they are facing
2. Walk through the three classification dimensions together: reversal cost, reversal speed, blast radius
3. Assess information state: ask what they know, what they don't, and whether the unknowns matter
4. If One-Way door, explore transformation tactics one by one — ask the user if each applies to their situation
5. Arrive at the triage verdict collaboratively
6. If the verdict is "escalate," recommend a specific framework and explain why

## Example

A brief example illustrating door transformation on "Should we migrate our database from PostgreSQL to MongoDB?":

> **Door Classification:** Appears to be a One-Way door — migration is expensive, affects all services, and switching back requires a second migration. Reversal cost: High. Reversal speed: Slow (months). Blast radius: Wide (every service that reads/writes data).
>
> **Transformation attempt:**
> - **Pilot:** Run one non-critical service on MongoDB for 3 months. Measure performance, developer experience, and operational burden against PostgreSQL baseline.
> - **Decouple:** The decision to *evaluate* MongoDB is a Two-Way door even if the decision to *migrate* is One-Way. Separate the evaluation from the commitment.
> - **Stage:** Phase the migration by service rather than big-bang. Each phase has a go/no-go checkpoint. After phase 1, the team has real data to decide whether to continue.
>
> **Verdict:** Successfully transformed. The evaluation is a Two-Way door — proceed immediately with a pilot. The full migration remains a One-Way door but can be staged to create exit points. Do not commit to full migration until pilot data is available.

## When to Apply This Framework

**Strong fit:**
- Any decision where the primary question is "should we act now or think more?"
- Decision paralysis — over-analyzing reversible choices
- Time-sensitive decisions where speed of action matters
- Organizational or team decisions where process overhead may be disproportionate
- Pre-analytical triage — determining which deeper framework to use

**Weak fit:**
- Evaluating the truth of a claim (use Scholastic instead)
- Decomposing a complex system (use Cartesian Reductionism instead)
- Judging quality or value (use Pirsig instead)
- Exploring a decision from multiple cognitive perspectives (use Six Thinking Hats instead)
- Decisions that are clearly One-Way and clearly consequential — this framework will tell you to escalate, so go directly to the deeper framework
