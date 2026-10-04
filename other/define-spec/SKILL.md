---
name: define-spec
description: Use when the user wants to turn a project idea, feature request, bug, or vague goal into a concise implementation-ready spec. Triggered by phrases like "create a spec", "write a spec", "define this project", "spec this feature", "start a project spec", or "turn this idea into a spec".
---

# Define Spec

Announce at start: `Defining spec...`

Create a short, decision-oriented spec that can be broken into tasks.

## Process

1. Read existing context before asking questions:
   - `AGENTS.md`
   - `context/*.md`
   - `README.md`
   - any linked issue, ticket, note, or existing spec
2. Ask only for missing product or behavior decisions. Keep questions concrete.
3. Save the spec to:

```text
~/.agents/specs/<repo>/YYYY-MM-DD-<slug>.md
```

4. If the user explicitly asks for repo-local docs, save under the repo instead.
5. After saving, show the path and a 3-5 bullet summary. Do not dump the full spec in chat.

## Spec Format

```markdown
# <Spec Title>

Date: YYYY-MM-DD
Repo: <repo>

## Goal
<What the user gets. One short paragraph.>

## Stakeholders / Systems
- <who or what uses, owns, or depends on this>

## Scope
- <included behavior>

## Out of Scope
- <explicit exclusions>

## Requirements
- <observable behavior or system rule>

## Acceptance Criteria
- <testable outcome>

## Open Questions
- <question or "None.">
```

## Rules

- Keep the spec concise. Prefer bullets over prose.
- Omit sections that genuinely do not apply.
- Write observable behavior, not implementation plans.
- Do not invent future phases unless the user asked for them.
- Do not create tasks here. Use `breakdown-tasks` after the spec is accepted.
- Do not include commit, push, or PR steps.
