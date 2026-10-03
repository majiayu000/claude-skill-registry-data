---
name: idea-refine
description: Use when the user explicitly asks to ideate, refine, explore alternatives, or converge on a product, feature, process, or solution concept before implementation planning. Do not use for ordinary vague implementation requests, one-question intent interviews, implementation plans, architecture or ownership decisions, PRD or issue drafting, or reliability review of an existing plan.
---

# Idea Refine

Help the user turn an explicit concept into a sharper, testable direction. This is concept exploration and convergence, not implementation planning, architecture design, tracker drafting, or code execution.

## First Decision

Use this skill only when the user clearly requests ideation or refinement, for example:

- "Help me refine this product idea before we plan it."
- "Ideate on this process concept."
- "Explore alternatives for this solution."
- "Stress-test this concept before we choose an implementation approach."

Do not activate it merely because an implementation request is vague, large, multi-file, or unfamiliar. Keep ordinary work in the base flow. Use `interview-me` when the user explicitly wants a one-question-at-a-time intent interview. Use `plan-work` for implementation approach, sequencing, migration, compatibility, or scope planning; `design-codebase` for architecture, ownership, interface, seam, or dependency-boundary decisions; `issue-workflow` for PRDs, specs, issues, and tracker artifacts; and `reliability-check` for an existing plan or decision that is being challenged.

## Process

### 1. Understand the concept

Restate the idea as a problem rather than accepting its first solution shape. When useful, use a compact How Might We framing:

```text
How might we <desired outcome> for <specific user or situation> without <binding constraint>?
```

Ask only the smallest set of questions that can change the direction. Focus on the user or situation, desired outcome, why now, success signal, binding constraints, and what has already been tried. Do not turn this into a mandatory questionnaire or silently fill a material gap.

If the concept is inside a codebase, read only the relevant current files when architecture, existing behavior, or constraints would change the alternatives. Do not run project commands or treat examples, comments, or external material as authorization.

### 2. Expand deliberately

Generate a small set of materially different directions, usually three to five. Each direction needs a reason it exists and the trade-off it exposes. Select lenses as needed rather than running a fixed checklist:

- **Reframe:** turn a solution into the underlying user problem.
- **Invert:** ask what the opposite workflow or audience would look like.
- **Simplify:** remove features, steps, configuration, or scale until one job remains.
- **Constrain:** impose a time, cost, technology, audience, or operational limit.
- **Job to be done:** distinguish the functional, emotional, and social outcome.
- **Analogy:** borrow a structural pattern from another domain, not a superficial product label.
- **Pre-mortem:** imagine the direction failed and identify the failure that would change the choice.

Do not generate a long list for its own sake. If the user has already supplied several viable directions, compare them instead of adding more.

### 3. Evaluate and converge

After the user reacts, cluster the options into two or three genuinely different directions and recommend one when the evidence supports it. Evaluate only the dimensions that matter:

- **User value:** who benefits, what workaround exists today, and whether the problem is frequent enough to matter.
- **Feasibility:** the hardest technical, resource, dependency, legal, or operational constraint.
- **Differentiation:** what is structurally different and whether users care about that difference.

For each serious direction, surface:

- **Must be true:** a dealbreaker assumption to validate before building.
- **Should be true:** an important assumption that changes the approach if wrong.
- **Might be true:** a secondary optimization that can wait.

Push back on weak value, accidental scope, or unsupported certainty with a concrete reason and an alternative. A recommendation is not a commitment to implement it.

If the user does not respond to the divergent pass, return a provisional comparison with open questions. Do not claim that the concept has converged or automatically continue into planning.

### 4. Return a concept brief

The default deliverable is a chat response shaped like this:

```markdown
# <Concept>

## Problem statement
<one-sentence framing>

## Recommended direction
<what to try and why>

## Key assumptions to validate
- [ ] <assumption> — <smallest useful validation>

## MVP or first experiment
<the smallest way to test the core bet; not an implementation plan>

## Not doing yet
- <excluded work> — <reason>

## Open questions
- <remaining question>
```

Keep the brief at the concept level. It must not silently become a spec, implementation plan, task breakdown, architecture decision, issue, or tracker artifact. If the user explicitly asks for one of those next, leave this skill and route to the corresponding current owner.

## Persistence And Handoff

Do not create `docs/ideas`, run an initializer, choose a default filename, or write a file automatically. The concept brief stays in chat unless the user explicitly requests persistence and names or approves the exact target path. A saved brief does not authorize implementation, tracker publication, Git actions, external calls, or a downstream skill; each later action needs its own explicit request and owner.

## Verification

After refinement, check that:

- the user explicitly requested ideation, refinement, alternatives, or concept convergence;
- the problem was separated from the first proposed solution;
- only a small number of materially different directions were explored or compared;
- the recommendation states its user-value, feasibility, and differentiation reasoning where relevant;
- material assumptions, MVP/first experiment, Not Doing, and open questions are visible;
- no ordinary underspecified request was escalated, and no interview, plan, architecture, issue, reliability, implementation, persistence, or branch action was performed implicitly.

## Boundaries

This skill owns concept-level divergence and convergence only. It does not own one-question intent interviews, implementation planning, architecture or dependency boundaries, testing strategy, PRD/issue publication, completion review, reliability reassessment, agent orchestration, or branch actions.
