---
name: project-concept-planner
description: Turns an undeveloped idea, vague opportunity, early product thought, or creative prompt into a concrete project concept with a target user, core problem, value proposition, solution direction, and initial boundaries. Use when the user asks to shape a raw idea before writing a project brief, PRD, MVP scope, roadmap, implementation plan, or pitch.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: founders-product-managers-developers-designers-and-builders
  tags:
    - concept-development
    - project-planning
    - value-proposition
    - target-user
    - problem-framing
    - scope-boundaries
  status: draft
  side_effects: none
---

# Project Concept Planner

## Purpose

Turn an undeveloped idea into a clear project concept before detailed briefing, scoping, design, or implementation begins.

This skill identifies the likely target user, core problem, value proposition, solution direction, first useful outcome, and initial boundaries. It is intentionally earlier than a full project brief: the goal is to make the idea coherent enough to discuss, validate, compare, or hand off for deeper planning.

## When to use this skill

Use this skill when:

- The user has a vague idea and wants to make it concrete.
- The user asks to define the concept, target user, core problem, value proposition, or first version of a project.
- A raw product, app, content, tool, service, research, or portfolio idea needs a clearer wedge.
- The user is deciding whether an idea is worth turning into a brief, MVP, roadmap, or implementation plan.
- Several possible audiences or problems could fit the same idea and the best starting angle needs to be selected.
- The user needs initial boundaries before scope, features, milestones, or technical architecture are planned.

Do not use this skill when:

- A structured project brief already exists and only needs refinement; use a brief or requirements skill instead.
- The user asks for a detailed implementation plan, issue breakdown, roadmap, or engineering sequence.
- The main task is market research, competitive analysis, or source-backed validation requiring current external data.
- The user only wants marketing copy, a pitch deck, launch post, or naming ideas.
- The request is to build, edit, or deploy code rather than clarify the project concept.

## Inputs to inspect

Start with the user's idea, notes, examples, constraints, and conversation context.

If working from local materials, inspect only concept-relevant sources such as:

- `README.md`
- `VISION.md`
- `IDEA.md`
- `BRIEF.md`
- `PRD.md`
- `NOTES.md`
- `PLAN.md`
- `docs/`
- `planning/`
- `product/`
- sketches, prototypes, demos, or examples that reveal intent

Do not inspect the whole repository unless the concept depends on broad existing context. Preserve uncertainty when the available material is thin.

## Concept principles

A strong project concept should:

- Start with a specific user and problem, not a feature list.
- Name the situation where the problem occurs.
- Explain why the project is useful now.
- State a simple value proposition in plain language.
- Define the smallest meaningful project shape without over-scoping.
- Separate known facts from assumptions and guesses.
- Avoid inventing market proof, user demand, metrics, deadlines, or constraints.
- Keep alternate interpretations visible when the idea could go in several directions.
- Create boundaries that make later planning easier.

## Workflow

1. **Restate the raw idea.** Summarize what the user provided in one or two sentences. Note whether it is a product, tool, service, content project, research project, internal workflow, creative work, or unclear hybrid.
2. **Extract what is known.** List explicit facts about the audience, problem, motivation, desired outcome, constraints, domain, platform, format, and any existing examples. Do not treat inferred details as facts.
3. **Identify possible concept angles.** If the idea is ambiguous, generate two to four plausible combinations of target user, problem, and value. Prefer sharply defined wedges over broad general-purpose concepts.
4. **Choose or recommend a primary wedge.** Select the strongest starting concept based on clarity, user pain, feasibility, differentiation, validation potential, and fit with the user's stated goals. If the evidence is insufficient, present the alternatives and name the decision needed.
5. **Define the target user.** Describe the primary user precisely, including context, current behavior, pain point, desired outcome, and any important secondary stakeholders or operators.
6. **Frame the core problem.** State the problem in user-centered language. Avoid merely restating the proposed solution. Include the trigger situation, current workaround, cost of the problem, and why solving it matters.
7. **Write the value proposition.** Explain what the project enables, for whom, and why it is better than the likely current alternative. Keep this concrete and falsifiable.
8. **Shape the solution direction.** Describe the project concept at a high level: the first useful experience, core capability, expected output, interaction model, or delivery format. Avoid detailed feature backlog decisions unless needed to clarify the concept.
9. **Set initial boundaries.** Identify what is in concept, what is intentionally deferred, and what is out of concept. Use boundaries to prevent premature expansion into unrelated audiences, platforms, integrations, or feature sets.
10. **Surface assumptions and validation needs.** List the riskiest assumptions and the smallest next actions that would clarify demand, feasibility, usability, data needs, content needs, or operational burden.
11. **Prepare the handoff.** Recommend the next planning artifact: project brief, requirements gap review, MVP scope, user flow, roadmap, research brief, or implementation plan.

## Output format

Return:

```md
## Concept snapshot

- Working title:
- Concept type:
- One-sentence concept:
- Primary target user:
- Core problem:
- Value proposition:
- First useful outcome:

## Why this concept

- User situation:
- Current workaround or alternative:
- Pain or opportunity:
- Why now:

## Concept boundaries

| Boundary | Decision | Rationale |
|---|---|---|
| In concept | ... | ... |
| Deferred | ... | ... |
| Out of concept | ... | ... |

## Assumptions to validate

| Assumption | Why it matters | Suggested validation |
|---|---|---|

## Open questions

- ...

## Recommended next step

- ...
```

When several concept angles are viable, add this before `Concept snapshot`:

```md
## Concept options

| Option | Target user | Core problem | Value proposition | Best fit when |
|---|---|---|---|---|
```

## Quality bar

The task is complete only when:

- The concept is narrow enough to guide the next planning step.
- The target user is more specific than “users” or “people.”
- The core problem is distinct from the proposed solution.
- The value proposition names a concrete benefit and likely alternative.
- Boundaries identify in-concept, deferred, and out-of-concept areas.
- Assumptions and open questions are clearly labeled instead of hidden as facts.
- The recommended next step matches the maturity of the idea.

## Edge cases

- If the user provides only a solution idea, infer possible problems cautiously and label them as assumptions.
- If the idea serves multiple audiences, choose one primary starting user or present separate concept options rather than blending them.
- If the idea is too broad, narrow it by first useful outcome, target user segment, channel, platform, or use case.
- If the idea depends on market demand or external trends, state that current research is needed before making market claims.
- If the user wants a portfolio project, include evidence the finished project should generate, such as demo scenarios, screenshots, architecture rationale, or case-study material.
- If the user is emotionally attached to a broad vision, preserve the long-term vision while defining a smaller initial concept wedge.

## Related skills

- `project-brief-builder`
- `mvp-scope-planner`
- `requirements-gap-finder`
- `user-flow-planner`
- `project-roadmap-builder`
