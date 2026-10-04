---
name: "Design Agent Claude"
description: "Run a focused UI polish or mockup-to-implementation pass through Claude Code using the custom subagent `design-agent-claude`. Default to Opus 4.6 with high effort; fall back to Sonnet 4.6 when Opus is unavailable or unnecessary."
alwaysAllow: ["Bash"]
---

# Design Agent Claude

Use this skill when you, the orchestrating agent, need to launch Claude Code for a visual-first UI pass.

## What this skill is for
This is an orchestrator-facing launch skill. It tells the current agent how to route the task, shape the prompt, and choose the right Claude-side agent.

Use it to:
- choose the correct Claude agent/subagent
- shape the delegation prompt for visual/design work
- avoid generic coding-agent prompting when the task is really UI/UX polish

Do not use it by telling the downstream Claude worker to read or activate this skill itself unless the user explicitly wants that. The normal flow is:
1. You read this skill.
2. You launch Claude correctly.
3. The Claude worker does the task using its own agent instructions.

## Preferred agent
On Claude Code, prefer the custom subagent:

- `design-agent-claude`

## Model guidance
- Default: Opus 4.6 with high effort for ambiguous or high-stakes visual work.
- Fallback: Sonnet 4.6 when Opus is unavailable, rate-limited, or more power than the task needs.
- Claude Code treats `model` as preference rather than hard enforcement, so keep the prompt explicit when you really want Opus-first behavior.
- Inspect screenshots or real UI before making design claims.

## Recommended prompt shape
"Use design-agent-claude for a UI polish pass on <surface>. Inspect the current UI or screenshots first, state the design intent, make the smallest high-leverage improvements, then report visual QA findings, interaction QA findings, and remaining weaknesses."

## Output checklist
- Design intent summary
- Top UI/UX issues found
- Concrete changes recommended or applied
- Breakpoint and interaction QA notes
- Remaining risks / next pass
