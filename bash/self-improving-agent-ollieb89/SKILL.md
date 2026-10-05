---
slug: self-improving-agent-ollieb89
version: 1.1.1
displayName: 自我改进代理（Self Improving Agent Ollieb89）
summary: 记录错误、纠正和重复模式到日志中，并将其转化为持久的指导，提升代理的自我改进能力。
tags: clawhub
---

# Self-Improving Agent

Use this skill to turn execution feedback into reusable operational knowledge.

## Quick workflow

1. Detect signal: error, correction, capability gap, or repeated workaround.
2. Log to `.learnings/` with the right entry type.
3. Resolve or promote high-value patterns into durable workspace files.
4. Reuse scripts/hooks to keep capture consistent.

## Use bundled resources

- Entry examples and formats: `references/examples.md`
- Hook setup for reminders/error detection: `references/hooks-setup.md`
- OpenClaw workspace integration: `references/openclaw-integration.md`
- Reminder hook script: `scripts/activator.sh`
- Command-error detector: `scripts/error-detector.sh`
- Skill extraction scaffold: `scripts/extract-skill.sh`
- Environment checks: `scripts/check_env.sh`
- Log templates: `assets/LEARNINGS.md`, `assets/SKILL-TEMPLATE.md`

## Log targets

- `.learnings/LEARNINGS.md`: corrections, knowledge gaps, best practices
- `.learnings/ERRORS.md`: command/tool/runtime failures
- `.learnings/FEATURE_REQUESTS.md`: requested capabilities not yet supported

## Promotion rules

Promote broadly reusable learnings out of `.learnings/`:

- behavior/style -> `SOUL.md`
- workflow/orchestration -> `AGENTS.md`
- tool constraints/gotchas -> `TOOLS.md`

Update original entries with status transitions (`resolved`, `promoted`, `wont_fix`) and references.

## Commands

```bash
# Verify scripts and learnings directory setup
bash workspace/skills/self-improving-agent/scripts/check_env.sh

# Dry-run extraction of a new skill from a recurring pattern
bash workspace/skills/self-improving-agent/scripts/extract-skill.sh my-pattern --dry-run
```
