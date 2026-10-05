---
name: to-prd
description: Synthesize the current conversation and repository context into a concise product and engineering spec, publish it to the project issue tracker, and gate agent readiness before decomposition. Use when high-level work needs product framing, implementation and testing decisions, or success criteria captured without another general interview.
---

# To PRD

Use after `clarify-work` has resolved fuzzy terminology or scope, when the conversation still
needs a durable product and engineering spec. Skip this for narrow, issue-shaped work.

## Workflow

1. Synthesize the current conversation; do not repeat a general requirements interview.
2. Inspect relevant code, the domain glossary, and applicable ADRs before drafting when they are available. Preserve established vocabulary and decisions.
3. Reuse the highest existing test seam that proves external behavior. Use nearby test prior art to identify the expected layer and observable assertions.
4. Ask at most one focused confirmation only when the highest existing test seam is genuinely unresolved after inspecting the conversation, repository, and project decisions. Wait for that answer before drafting or publishing. Otherwise continue directly to the spec. Do not use this confirmation for product, implementation or architecture, publication or access, or other blockers; record those in the spec instead.
5. Write a concise spec with these sections: Problem, Goal and solution, Prioritized user stories, Success criteria, Non-goals, Constraints, Open product decisions, Implementation decisions, and Testing decisions.
6. Detect the project issue tracker from repository configuration, remotes, or available integrations. Publish the spec to the detected project issue tracker.
7. Apply `ready-for-agent` only after every blocker is resolved and publication succeeds. Product, test-seam, implementation or architecture, publication or access, and other blockers all prevent readiness. When access allows, publish a blocked spec without the label and identify every blocker and owner.
8. Hand the published spec to `decompose-to-issues`; do not turn the PRD into an issue breakdown.

If no tracker or publishing access can be detected, return the finished spec with that explicit
blocker. Do not invent a destination, claim publication or readiness, or hand off to decomposition.

## Spec guidance

- Frame the problem from the affected user's or operator's perspective.
- State the goal and solution as observable outcomes, not a task list.
- Include prioritized user stories only when they clarify distinct actors, outcomes, or ordering; keep them few and outcome-focused.
- Make success criteria verifiable and include constraints that materially shape delivery.
- Distinguish unresolved product decisions from settled implementation decisions.
- In Testing decisions, name the chosen existing seam, test layer, relevant prior-art pattern, important external behaviors, and any necessary manual validation.

## Guardrails

- Exclude volatile file paths and code snippets. Include a prototype artifact only when it records a decision more clearly than prose; trim it to the decision-rich state machine, schema, type shape, or interaction.
- Do not reopen settled decisions or invent requirements unsupported by the conversation and repository.
- Do not duplicate `clarify-work`'s terminology interview or `decompose-to-issues`' task breakdown.
- Keep the published spec short enough for an implementation agent to use as its source of truth.
