---
name: pstack-arena
description: "Compare concrete candidates for the same task and synthesize the best result. Use only when the user explicitly requests arena or pstack-arena."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/arena
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# Arena

Produce alternatives, choose a base with evidence, and integrate only the improvements that preserve one coherent design.

Run this workflow only when the user explicitly names arena or pstack-arena, including a request within pstack-mode. A request for alternatives, rigor, or architecture alone is not opt-in. A router or another skill cannot supply that opt-in. Without it, handle the task directly without starting an arena.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Frame

State the artifact, constraints, and completion condition. Derive a few task-specific comparison criteria before seeing candidates. Give candidates the same task and constraints; reserve scoring for the comparison.

Prefer two candidates for a meaningful choice. More candidates require distinct useful directions and an adequate budget. Give each writer an isolated output or worktree.

## Produce and compare

Use fresh inherited-model workers when supported and authorized. Otherwise build distinct sketches sequentially and label the evaluation as self-review. This preserves candidate comparison, not the original multi-model method.

Each candidate supplies an artifact and a short account of rejected alternatives. A dropout is a gap. Wait until artifacts are complete before comparing them.

Read every candidate and score each against the criteria. An authorized fresh reviewer can provide another judgment using the chat model. Same-model consensus does not prove correctness.

Choose a base on its real contract fit, maintainability, and verification. If all candidates miss because the brief was ambiguous, reframe the brief rather than averaging failures.

## Synthesize and verify

Inspect losing candidates for specific useful pieces. Integrate deliberately; do not combine incompatible ownership or data models. Keep a local synthesis note with the selected base, grafts, rejections, dropouts, and evidence.

Verify the synthesized artifact against the original completion condition. Candidate scores do not substitute for running or inspecting the resulting artifact. Publish only within the user's request.
