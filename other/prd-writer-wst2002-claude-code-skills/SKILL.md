---
name: prd-writer
description: Use when writing a PRD, product requirements document, feature spec, product brief or requirements doc, turning a feature idea into requirements, or reviewing an existing PRD for gaps.
---

# PRD Writer

## Overview

A PRD makes a team agree on the problem, the definition of success, and the scope before anyone designs or builds. Separate evidence from assumptions, make every goal measurable, and make every requirement testable.

## Method

1. **Gather context:** the request, any notes or data the user provides, the existing product (read the code or docs if available), constraints and deadlines.
2. **State the problem before the solution:** who has the problem, how often, what it costs them and the business, and the evidence.
3. **Ask only blocking questions.** If an unknown would change the scope, ask. Otherwise record it under Open questions and keep going.
4. **Write** using [template.md](template.md).
5. **Self-check** against the quality bar below before handing it over.

## Quality bar

| Section | Must have |
|---|---|
| Problem | Evidence (data, quotes, tickets) with source; anything unsupported is labelled `Assumption:` |
| Goals | Metric + current baseline + target + time frame ("checkout conversion 2.1% → 2.6% within 60 days of launch") |
| Non-goals | Explicitly excluded scope that someone might expect |
| Users | Primary and secondary personas with the job they are trying to do |
| Requirements | User stories with priority (Must, Should, Could) and acceptance criteria in Given / When / Then |
| Edge cases | Empty, error, permission, limits, concurrency, offline or slow network, migration of existing data |
| Dependencies and risks | Teams, services, legal or privacy concerns, each risk with a mitigation |
| Rollout | Phases or flags, who gets it first, how success is measured, rollback trigger |
| Open questions | Each with an owner and a decision deadline |

## Rules

- Never present invented numbers as facts. Use the user's data, or write `Assumption:` and say how to validate it.
- Keep design and implementation details out unless they are hard constraints.
- Prefer one page of precise text over five pages of generic sections.
- When reviewing an existing PRD, list the gaps against the quality bar, most important first, then offer the revised sections.

## Common mistakes

- Solution-first: "Build a saved-carts page" with no statement of the user problem.
- Vague goals: "improve engagement".
- Acceptance criteria that cannot fail ("works well on mobile").
- Missing non-goals, which lets scope grow silently.
- Treating open questions as decided.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
