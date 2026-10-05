---
name: replan
description: Iterative deep planning with critiques and alternatives. Use when facing complex design decisions requiring thorough analysis.
metadata:
  website: "https://photostructure.com/coding/claude-code-replan/"
---

# Replan

> Documented in depth: [Claude picks the first idea that works. Make it pick the best one.](https://photostructure.com/coding/claude-code-replan/)

You are going to **replan** — an iterative process of designing, critiquing, and refining a plan.

Coding agents tend to commit to the first workable approach
they find. For design decisions with high switching costs (architecture, data
models, API surfaces), seek the best approach rather than the first one that
clears the bar. This skill forces multiple structured critiques before settling
the design.

## Process

### 1. Understand & Clarify

- Read relevant code, documentation, and constraints
- State any assumptions you're making
- Ask clarifying questions before proceeding — don't build an elaborate plan on a misunderstood requirement

### 2. Initial Plan

Design your first approach, considering requirements and existing solutions. Expect it to be imperfect.

### 3. Critique

Generate thorough, *specific* critiques of your plan:

- Does it balance simplicity with good engineering?
- Is it maintainable, testable, DRY, scalable?
- Scrutinize for "hand-wavy" aspects — don't assume how things work, study the code
- For novel libraries/APIs, validate assumptions with web searches
- Note uncertainties as risks

Vague critiques like "this could be more robust" are useless. Aim for "this assumes the client handles reconnection, but I haven't verified that."

### 4. Alternatives

Brainstorm alternatives that address the specific weaknesses found in step 3. Goals:

- Simplify the plan
- Reduce complexity and risk
- Improve code quality and maintainability

### 5. Develop Best Alternative

Select the most promising alternative and flesh it out to the *same level of detail* as the original. A hand-wavy alternative that "sounds simpler" isn't a real comparison.

### 6. Iterate

Repeat steps 3-5 at least **three times**, asking for user feedback at each iteration. The checkpoints aren't just for steering — they're where the user injects context you can't grep for: product goals, domain constraints, recent team decisions, upcoming migrations.

### 7. Final Plan

Assemble the best features from all iterations into a robust final plan.

## Output Format

For each iteration, present options with pros/cons:

### Option A: [Name]

[Description]

**Pros:** ...
**Cons:** ...
**Risks:** ...

### Recommendation

[Which option and why, per design principles]

## Guidelines

- Consider Kent Beck's Simple Design rules (or your project's stated design principles)
- Consider coupling, cohesion, testability
- Be honest about tradeoffs
- Ask questions — don't guess

This skill is for *thinking*, not *doing*. Treat the workflow as read-only: do
not edit project files or begin implementation while replanning.

Read-only commands are allowed, and encouraged, to settle an assumption the
plan rests on: `git log` for how a module got this way, `npm ls` for what is
actually installed, a small probe for whether an API behaves as assumed. An
unverified assumption is a risk you are handing to the implementer.

The line is intent, not tooling: run commands to *test the plan*, never to
*start building it*. "Let me just write a quick script to try this" is how
replanning turns into implementing.

## Adapting for your project

- **Add a "Required Reading First" section** pointing to `AGENTS.md`, optional
  `CLAUDE.md`, architecture docs, or design principles — every listed file is
  read at the start of each invocation, so keep it short and high-value.
- **Add domain-specific critique prompts** (e.g. "does this respect our backwards-compatibility guarantees?", "how does this affect cold-start latency?", "does this add dependencies, and are they justified?").
- **Adjust the iteration count.** Three is a floor; bump to five for high-stakes decisions like schema migrations or public API design.
