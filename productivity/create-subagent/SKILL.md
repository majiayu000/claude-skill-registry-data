---
name: create-subagent
description: 'Design and author reusable subagents for specialized AI tasks. Use when the task needs an isolated agent persona, scoped system prompt, or reusable domain-specific assistant rather than a general skill.'
disable-model-invocation: true
metadata:
  owner: global-agents
  tier: contextual
  canonical_source: ~/.agents/skills/create-subagent
---









# Create Subagent

Use this skill to decide whether a subagent is the right abstraction and to author it correctly.

## Use When

- The task needs an isolated prompt and context boundary.
- A reusable specialist agent would be clearer than one large skill or one-off prompt.
- The user wants a named assistant for repeat work such as review, debugging, or domain analysis.

## Do Not Use When

- A skill is the better abstraction because the behavior is procedural and tool-driven.
- The user only needs one temporary prompt, not a reusable subagent.
- The request is about orchestrating many agents together. Use `agent-teams`.

## Inputs / Prereqs

- The subagent's job, scope, and success criteria.
- Target location and priority rules.
- Example prompts or tasks the subagent must handle.
- `references/subagent-examples.md`, `references/location-rules.md`, or `references/troubleshooting.md` when needed.

## Workflow

1. Decide whether the behavior belongs in a subagent, a skill, or a one-off prompt.
2. Define the subagent's scope, boundaries, and expected outputs.
3. Pick the correct storage location and naming convention.
4. Author the prompt and configuration with one clear responsibility.
5. Validate the subagent against one representative task and report the expected invocation pattern.

## Outputs / Evidence

- A subagent brief with role, scope, prompt shape, and storage location.
- The criteria that make a subagent preferable to a skill or one-off prompt.
- One representative invocation example.

## Failure / Stop Conditions

- Stop if the behavior is too broad for one subagent.
- Stop if the request would be better served by a skill or plain prompt.
- Do not create overlapping subagents with unclear ownership.

## Load These Resources

- `references/location-rules.md`
- `references/subagent-examples.md`
- `references/troubleshooting.md`

## Memory Hooks

- Read memory when existing project-specific agent conventions matter.
- Write memory only if the session establishes a durable subagent standard or naming rule.
