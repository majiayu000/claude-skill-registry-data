---
name: audience-fit-evaluator
description: Evaluates or plans a user-facing artifact from the perspective of its intended audience. Use when audience fit, user intent, usefulness, evidence, clarity, trust, expectations, or decision criteria materially affect a website, interface, feature, article, documentation set, case study, portfolio, product, presentation, or demo.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with access to supplied artifacts, briefs, audience research, or repository files unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: review
  audience: designers-product-teams-content-creators-developers
  tags:
    - audience-fit
    - user-intent
    - persona
    - evidence
    - usability
    - content-strategy
    - design-review
  status: draft
  side_effects: none
---

# Audience Fit Evaluator

## Purpose

Determine whether a user-facing artifact enables its primary audience to understand what matters, find credible evidence, and reach the intended outcome without unnecessary friction.

This is a consultative skill. It may run independently or provide a bounded audience checkpoint inside another workflow. It does not implement changes or take over a parent task unless the user explicitly requests implementation.

## When to use this skill

Use this skill when:

- Audience fit, user intent, usefulness, clarity, evidence, trust, or expectations materially affect the result.
- A team needs audience constraints before creating an artifact.
- A draft or direction needs a lightweight audience checkpoint.
- An existing artifact needs a prioritized audience-fit review.
- The correct primary audience has not yet been identified.
- Another skill needs concise audience guidance before continuing.

Do not use this skill when:

- The user only needs copy editing, visual polish, technical validation, or implementation with no material audience decision.
- A specialist accessibility, security, performance, SEO, legal, or domain-correctness audit is the main task.
- The request requires primary user research rather than evaluation from available evidence.
- The artifact has no meaningful audience-facing outcome.

## Inputs to inspect

Inspect the smallest useful set of available inputs:

- The artifact, substantial draft, prototype, screenshot, implementation, or content.
- The task brief, user goal, expected outcome, and parent-skill instructions.
- Audience, persona, user-research, product, requirements, brand, or content documentation.
- Relevant analytics, feedback, examples, or evidence supporting important claims.

Do not require every input or depend on specific filenames. Prioritize evidence in this order:

1. Explicit task instructions.
2. An explicitly named primary audience.
3. Audience or persona research.
4. Product, content, brand, or project requirements.
5. Conservative inference from the artifact and its intended outcome.

## Operating modes

Choose the smallest mode that fits the task:

- **SELECT** — identify one primary audience when it is unclear.
- **PLAN** — define audience constraints before creation.
- **CHECKPOINT** — test whether work in progress remains aligned; report only material deviations.
- **REVIEW** — evaluate a substantial draft or finished artifact and prioritize findings.

If the user or parent skill specifies a mode, use it. Otherwise infer the mode from the artifact's stage. Do not run a deep review when a lightweight checkpoint is enough.

## Audience model

Define the primary audience by intent and context, not invented demographics. Capture only characteristics that change decisions:

- **Context:** Why are they encountering the artifact?
- **Goal:** What are they trying to accomplish?
- **Central question:** What must the artifact answer?
- **Knowledge:** What can it reasonably assume they know?
- **Required evidence:** What must they see, understand, verify, or experience?
- **Decision criteria:** How will they judge whether the artifact is useful or credible?
- **Friction and objections:** What could confuse, slow, discourage, or create distrust?
- **Desired outcome:** What should they think, know, decide, or do afterward?

When audience information is missing, create a provisional **audience hypothesis** containing only the role or relationship, reason for arriving, desired outcome, expected knowledge, and likely decision criteria. State the hypothesis and its confidence. Do not invent names, ages, hobbies, biographies, or unsupported access needs.

Choose one primary audience whenever possible. Ask: “If this artifact could serve only one audience well, who should it be?” Add secondary audiences only when they materially change the result, and do not weaken the primary experience to satisfy everyone equally.

## Workflow

1. **Establish the target and mode.** Identify the artifact, its stage, the requested decision, and whether the evaluation should be lightweight, standard, or deep.
2. **Separate evidence from inference.** Record confirmed audience facts, reasonable assumptions, and consequential unknowns. Ask a clarifying question only when a missing fact would materially change the evaluation and cannot be inferred safely.
3. **Select the primary audience.** Use the evidence priority above. Define a bounded audience hypothesis if necessary.
4. **Build the audience model.** State the audience's context, goal, central question, knowledge, required evidence, decision criteria, friction, objections, and desired outcome.
5. **Trace the audience path.** Determine what the audience notices first, what they understand next, whether they can find the required proof, where doubt or effort appears, and what outcome the artifact enables.
6. **Evaluate relevant dimensions.** Inspect relevance, clarity, evidence, depth, friction, trust, distinction, and actionability only where they affect the intended outcome.
7. **Run a skeptical pass when warranted.** For major artifacts or consequential decisions, test what the audience might dismiss, distrust, misunderstand, or find unsupported. Do not manufacture criticism.
8. **Prioritize root findings.** Report the smallest set of material issues. Consolidate symptoms that share a cause, identify what should be preserved, and treat removal or simplification as valid recommendations.
9. **Return the mode-specific handoff.** Keep the result proportionate and actionable. When invoked by another skill, yield control after the handoff.

## Evaluation rules

Use the chain:

> audience → intent → question → evidence → friction → outcome

- Prefer evidence over claims. Valid evidence may include working behavior, examples, data, source code, demonstrations, screenshots, reasoning, constraints, trade-offs, or documented results.
- Require only evidence relevant to the artifact and audience decision.
- Evaluate audience fit rather than personal taste.
- Do not recommend more sections, features, content, animation, or abstraction unless each solves a specific audience problem.
- Preserve strong decisions that already serve the audience.
- It is valid to conclude that no material audience-fit issue was found.
- Identify specialist concerns only at the audience-risk level, then route detailed accessibility, security, performance, visual-design, motion, architecture, SEO, legal, or domain analysis to the relevant workflow.

## Severity

- **BLOCKER** — fundamentally prevents the primary audience from reaching its goal, such as the wrong audience, missing core information, an impossible central task, or a contradicted critical claim.
- **MAJOR** — materially weakens comprehension, confidence, usefulness, or success and should normally be addressed.
- **MINOR** — improves quality but does not threaten the primary outcome.
- **OPTIONAL** — a subjective refinement or possible enhancement; never present it as required.

## Output format

Use the format for the selected mode and omit empty optional sections.

### SELECT

```md
## Audience Selection

**Primary audience:** …
**Why:** …
**Primary goal:** …
**Central question:** …
**Secondary audience:** …
**Confidence:** HIGH | MEDIUM | LOW
```

### PLAN

```md
## Audience Gate

**Mode:** PLAN
**Primary audience:** …
**Audience goal:** …
**Central question:** …

**Must communicate:**
- …

**Must prove or demonstrate:**
- …

**Likely friction:**
- …

**Avoid:**
- …

**Success condition:** …
**Confidence:** HIGH | MEDIUM | LOW
```

### CHECKPOINT

```md
## Audience Gate

**Mode:** CHECKPOINT
**Primary audience:** …
**Still aligned:** YES | PARTIALLY | NO

**Material deviations:**
- [SEVERITY] …

**Preserve:**
- …

**Adjust:**
- …
```

### REVIEW

```md
## Audience Review

**Primary audience:** …
**Audience goal:** …
**Immediate read:** …

### Findings
- [SEVERITY] **Issue** — Evidence: … Impact: … Recommendation: …

### Missing evidence
- …

### Remove or simplify
- …

### Preserve
- …

### Verdict
PASS | PASS WITH MINOR CHANGES | REVISE | RECONSIDER

**Reason:** …
```

For a lightweight evaluation, return only the audience definition, alignment or verdict, material findings, and next action. For a deep evaluation, include the skeptical pass and evidence analysis.

## Parent-skill handoff

When another skill invokes this evaluator:

1. Preserve the parent task's objective and scope.
2. Use the audience evidence and mode supplied by the parent.
3. Return concise audience constraints or findings in the relevant format.
4. Do not redesign, rewrite, implement, or repeatedly reevaluate unless explicitly delegated.
5. Yield control after the handoff; the parent skill remains responsible for execution.

## Quality bar

The task is complete only when:

- One primary audience and its intended outcome are explicit or clearly marked as a hypothesis.
- Findings connect audience intent, observable evidence, friction, and outcome.
- Material issues are separated from optional refinements and unsupported taste.
- Strong existing decisions are preserved.
- The depth matches the artifact's importance and available evidence.
- Consequential uncertainty and confidence are visible.
- A parent workflow receives a concise handoff without scope expansion.

## Edge cases

- **Conflicting audience sources:** Follow the evidence priority, expose the conflict, and explain which source controls the evaluation.
- **Several plausible audiences:** Select the audience most closely tied to the intended outcome; name a secondary audience only if it creates a material constraint.
- **No artifact yet:** Use PLAN mode and return constraints, not a critique of imagined work.
- **Thin evidence:** Produce a provisional result, state its limits, and avoid definitive claims.
- **Inaccessible or unavailable artifact:** Evaluate only supplied evidence and state what could not be verified.
- **Strong artifact:** Return a pass, preserve the decisions that create the fit, and avoid inventing changes.
- **Specialist issue:** Explain its audience impact and recommend the relevant specialist review without attempting to replace it.

## Related skills

- `design-problem-framer` — defines the broader purpose, message, priorities, constraints, and success criteria before design work.
- `website-distinctiveness-review` — evaluates brand ownability and audience specificity for websites.
- `inclusive-task-flow-review` — reviews complete journeys for inclusion, accessibility, resilience, and usability.
- `conversion-creative-director` — develops audience-aware ethical persuasion and conversion direction.
- `microcopy-polish` — improves interface language after audience needs are clear.
