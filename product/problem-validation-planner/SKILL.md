---
name: problem-validation-planner
description: Plans how to verify that a proposed problem is real before implementation begins. Use when the user asks to validate a problem statement, de-risk a product idea, test whether users actually have a pain point, gather evidence before building, or design discovery research before committing engineering work.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: product-builders-founders-and-project-leads
  tags:
    - problem-validation
    - discovery
    - user-research
    - evidence-planning
    - product-planning
    - risk-reduction
  status: draft
  side_effects: none
---

# Problem Validation Planner

## Purpose

Create a practical validation plan for confirming whether a proposed problem is real, important, frequent, and worth solving before implementation begins.

This skill focuses on evidence design, not solution design. It helps agents turn an assumption-heavy problem statement into testable claims, discovery questions, lightweight research activities, decision thresholds, and a go/no-go recommendation path.

## When to use this skill

Use this skill when:

- The user has a product, feature, automation, internal tool, or project idea but has not yet proven the underlying problem.
- The user asks whether a proposed problem is real, painful, common, urgent, or worth building for.
- The task is to plan user discovery, customer interviews, surveys, concierge tests, diary studies, demand tests, or evidence gathering before implementation.
- A team wants to separate problem validation from solution validation, MVP scoping, or implementation planning.
- A project brief contains untested assumptions about users, pain points, frequency, existing workarounds, willingness to switch, or willingness to pay.
- Engineering work should be delayed until the problem, affected audience, and success criteria are clearer.

Common trigger phrases include:

- “How do we validate this problem before building?”
- “Plan problem discovery.”
- “Is this a real user pain?”
- “What evidence should we gather before implementation?”
- “Design a validation plan for this idea.”
- “De-risk this product problem.”
- “What should we learn before writing code?”

Do not use this skill when:

- The user already has strong evidence that the problem exists and needs help scoping an MVP; use `mvp-scope-planner`.
- The main need is turning a rough idea into a project brief; use `project-brief-builder` first.
- The task is validating whether a built solution works, is usable, or meets launch criteria.
- The user wants market sizing, competitor research, or source synthesis as the main deliverable; use a research-synthesis skill when available.
- The request is to implement the feature immediately rather than plan discovery.

## Inputs to inspect

Start with the smallest evidence set that clarifies the proposed problem:

- User-provided idea, problem statement, project brief, PRD, pitch, issue, roadmap item, or feature request.
- Target audience, user roles, contexts, jobs-to-be-done, workflows, and affected segments.
- Stated symptoms, pain points, current workarounds, costs, frequency, severity, and urgency.
- Existing evidence such as support tickets, analytics, search logs, sales notes, forum posts, reviews, interviews, survey results, churn reasons, or customer requests.
- Known constraints: timeline, access to users, privacy limits, sample availability, budget, stakeholder expectations, and ethical or legal considerations.
- Proposed solution only to identify bias and separate it from the underlying problem claim.

Avoid inspecting implementation files unless they reveal current workflows, telemetry, support evidence, or existing product behavior relevant to the problem claim.

## Workflow

1. **Restate the problem neutrally.** Rewrite the proposed problem without assuming the solution is correct. Identify the target user, context, trigger, obstacle, consequence, and current workaround.
2. **Separate claims from evidence.** List what is known, what is assumed, what is anecdotal, and what is unsupported. Mark solution-shaped claims that need to be translated back into problem claims.
3. **Define the validation decision.** State what decision the evidence must support: proceed, pivot, narrow the audience, reframe the problem, run more discovery, or stop.
4. **Identify riskiest assumptions.** Prioritize assumptions about problem existence, audience specificity, frequency, severity, current alternatives, switching friction, buyer/user mismatch, urgency, and willingness to invest time or money.
5. **Choose evidence methods.** Select the lightest credible methods for the assumptions, such as:
   - customer or user interviews for context, language, and causal understanding;
   - support-ticket or analytics review for frequency and patterns;
   - survey only after interview learning has clarified terms and options;
   - concierge or manual workflow tests for proof that users will engage with a problem-solving process;
   - landing page, waitlist, or outreach tests for demand signals;
   - diary study or observation when the problem occurs in a workflow that users may misremember.
6. **Design unbiased research prompts.** Draft questions that explore past behavior, concrete examples, current workarounds, costs, triggers, and consequences. Avoid leading questions, feature pitches, hypotheticals, and asking users to design the solution.
7. **Define participant and sample criteria.** Specify who to talk to, who to exclude, minimum sample size or evidence quantity, recruiting channels, and how to avoid overfitting to friendly or unrepresentative respondents.
8. **Set decision thresholds.** Define what evidence would validate, invalidate, or make the problem inconclusive. Use observable thresholds where possible, such as repeated unaided mentions, measurable workflow cost, active workaround use, recent occurrence, or committed follow-up behavior.
9. **Plan bias controls.** Include steps to reduce confirmation bias, leading questions, stakeholder pressure, cherry-picked anecdotes, survey wording bias, and solution enthusiasm masquerading as problem evidence.
10. **Sequence the work.** Order discovery from cheapest/highest-uncertainty evidence to higher-effort validation. Put stop/reframe checkpoints before implementation planning.
11. **Translate outcomes into next actions.** Define what to do if the problem is validated, narrowed, reframed, invalidated, or still uncertain. Do not proceed to solution scope unless the problem evidence meets the threshold.

## Output format

Return:

```md
## Validation objective

- Proposed problem:
- Target user/context:
- Decision this plan must support:
- Current confidence:

## Assumption map

| Priority | Assumption | Why it matters | Current evidence | Validation method |
|---|---|---|---|---|

## Research plan

| Step | Method | Participants/data | Questions or signals | Output | Stop/proceed rule |
|---|---|---|---|---|---|

## Interview or discovery prompts

- ...

## Evidence thresholds

- Validated if: ...
- Inconclusive if: ...
- Invalidated if: ...

## Bias and risk controls

- ...

## Decision path

- If validated: ...
- If narrowed or reframed: ...
- If inconclusive: ...
- If invalidated: ...

## Open questions

- ...
```

If the user provided very little context, first return a short discovery intake with the missing information needed to produce a responsible validation plan.

## Quality bar

The task is complete only when:

- The problem is stated independently from the proposed solution.
- The plan identifies the riskiest assumptions before selecting methods.
- Evidence methods match the type of uncertainty being tested.
- Research prompts focus on past behavior and concrete examples, not compliments or hypothetical intent.
- The plan includes decision thresholds that can stop, reframe, or narrow the project before implementation.
- Bias controls are explicit.
- The output tells the user what to do with validated, inconclusive, and invalidated results.

## Edge cases

- If the target user is vague, make audience definition the first validation step.
- If the user only has a solution idea, infer the underlying problem as a hypothesis and label it as unvalidated.
- If users and buyers differ, validate pain, urgency, and decision authority separately.
- If the problem is internal, include operational evidence such as time logs, error rates, rework, support load, or missed deadlines.
- If direct user access is unavailable, use proxy evidence cautiously and flag the confidence limit.
- If the problem involves health, safety, legal, finance, minors, or sensitive personal data, include privacy, consent, and expert review constraints before research.
- If stakeholders demand implementation before evidence is collected, propose a time-boxed validation checkpoint before build commitment.

## Related skills

- `project-brief-builder`
- `project-concept-planner`
- `mvp-scope-planner`
- `requirements-gap-finder`
- `feature-priority-planner`
- `implementation-order-planner`
