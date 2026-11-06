---
name: test-project-manager
description: Use for this project's work. Own project rules, user output preferences, project knowledge, and session-derived updates before answering or changing code.
---

# test Project Manager

This skill is the project owner for test. It keeps the user's habits, output rules, project architecture, function details, and session summaries active throughout the work.

## Required Workflow

1. The NewBrain runtime injects this skill's reference contents into the system context before the model runs.
2. Apply injected user rules unless they conflict with safety, correctness, or explicit newer instructions.
3. Do not call tools merely to read these references; their contents are already present in context.
4. Do not create or edit `.newbrain`, `.codebuddy`, reference, memory, or session-summary files. The runtime updates them after the response.
5. Treat this skill as responsible for completing the user's request end to end within this project.

## Knowledge Files

- `references/user-output-rules.md`: distilled user habits, response rules, and output preferences.
- `references/project-knowledge.md`: project descriptions, architecture, feature behavior, and implementation notes.
- `references/session-digest.md`: append-only conversation summaries used to improve this skill over time.
