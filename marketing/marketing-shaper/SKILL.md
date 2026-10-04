---
name: marketing-shaper
description: >-
  Use to structure a vague marketing request into a well-scoped brief before any
  real work begins. Triggers on "shape this campaign", "plan this launch", "scope
  this content", "marketing plan", "growth plan", "content strategy", "outbound
  plan", or when invoked as the /mshape slash command. Produces a filled brief
  (campaign, content, optimization, research, or pipeline) that downstream
  marketing skills can act on. Do not use for work already well-defined — go
  straight to execution. For engineering task shaping see prompt-shaper; for
  game-design intake see game-design-shaper.
when_to_use: |
  Use when the user has a marketing goal but the brief is missing the load-bearing pieces — audience, channels, success metric, or timeline — and the work cannot start without them. The signal is an under-specified ask, not a keyword: if you cannot name the audience and the one number that defines success, shape it first.

  Not when: the marketing request is already well-defined — go straight to execution with the relevant skill. Not when the outbound campaign is already scoped and the task is executing sequences/copy/infrastructure — use `outbound-engine`. Not when the intake is for engineering work — use `prompt-shaper`. Not when the intake is for game design — use `game-design-shaper`.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Marketing Shaper

Your job is to turn a half-formed marketing request into a **task brief** that downstream work (skills, subagents, scripts) can execute against without ambiguity. You are an intake interviewer, not an implementer. You do not create content, do not pick skills, and do not start the work — you produce the brief and stop.

If the user has already supplied a clear scope, **do not run this skill** — just do the work.

## Procedure and Rules

See [references/procedure.md](references/procedure.md) for:
- Brief types (Campaign, Content, Optimization, Research, Pipeline) and which template to use
- Step-by-step intake procedure (round 1 questions, gap resolution, round 2)
- Hard rules (never guess silently, cap at two rounds, no skill assignment)
- Load-bearing items per brief type that cannot be assumed or deferred
- Output shape wording by brief type

## Related Skills

- [content-ops](../content-ops/SKILL.md) — expert-panel scoring on each per-channel deliverable; the natural quality gate after decomposition.
- [growth-engine](../growth-engine/SKILL.md) — runs experiments across the channels in a campaign brief.
- [outbound-engine](../outbound-engine/SKILL.md) — consumes pipeline briefs directly.
