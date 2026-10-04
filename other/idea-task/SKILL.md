---
name: idea-task
description: Interactive idea shaping skill that turns a rough idea into a validated concept draft before prepare-task formalizes it into a Ready implementation task. Use when the user asks for early brainstorming, architecture/risk review, task decomposition, technical debt discovery, or asks questions such as '/idea-task [description]'.
---

# Idea Task

## Purpose

Use this skill before `prepare-task` when an idea is still ambiguous.

`idea-task` does discovery and risk shaping.
`prepare-task` does implementation-ready formalization and GitHub project readiness.

## Invocation

- `$idea-task`
- `/idea-task [description]`
- `/idea-task -url "https://example.com/tasks/<id>"`
- `I have an idea, help me shape it first`

Works in VS Code, Codex Web, and Codex Desktop repository chat.

## Workflow

1. Determine source: free-text idea or `-url` existing issue/task, then restate the idea in one paragraph.
2. Review repository context relevant to the idea.
3. Read the project profile and run an applicability pre-check for privacy, AI, security, safety, accessibility, and sector governance before suggesting implementation details.
4. Ask up to three focused questions at a time.
5. Maintain an `Open Questions` list and close items as answered.
6. Produce an `Idea Draft` with:
   - problem and outcome
   - in-scope/out-of-scope
   - likely modules/files
   - risks and technical debt hotspots
   - observability, logging, and rollback expectations
   - compliance notes
7. Classify the next route:
   - ordinary/local change: `$prepare-task`
   - new or changed user/business behavior: `$generate-use-case`
   - material business choice: `$generate-bdr`
   - cross-component, data-flow, deployment, or quality-attribute change: `$architecture-change`
8. Decide status:
   - `Ready for prepare-task`
   - `Blocked` (with reasons)
9. Emit exact marker line for downstream automations:
   - `Idea Task Status: Ready for prepare-task.` when ready.
10. If ready, recommend the classified next route instead of always defaulting to `$prepare-task`.

## Question Priorities

Ask only what is needed to remove ambiguity:

- user outcome and success metric
- impacted channels (API, chat simulator, mobile, web)
- data classes, retention/deletion, consent/transparency
- external API dependencies and fallback behavior
- acceptance test shape and release constraints

## Output Template

Use `references/idea-draft-template.md`.

## Guardrails

- Do not start code implementation in this skill.
- Stop and surface compliant alternatives when the proposal conflicts with applicable governance requirements.
- Keep answers concise, concrete, and directly actionable by `prepare-task`.
