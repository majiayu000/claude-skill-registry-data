---
name: audit
description: Audit DegenExus Claude Code internals against the routing contract, evidence schema, hooks, settings, and inventories.
disable-model-invocation: true
argument-hint: "[optional internals scope]"
---

# Audit Workflow

Use for Claude Code internals and documentation consistency reviews.

## Canonical References

- `.claude/rules/synergy-contract.yml`
- `.claude/rules/evidence-schema.yml`
- `.claude/rules/02-agent-synergy.md`
- `.claude/README.md`
- `.claude/skills/claude-config-audit/references/live-smoke-template.md`

## Steps

1. Run `python .claude/hooks/validate-claude-config.py`.
2. Run `python -m compileall -q .claude/hooks`.
3. Verify agents, skills, commands, hooks, rules, settings, and memory are inventoried in `.claude/README.md`.
4. Verify every `memory: project` agent has `.claude/agent-memory/<agent>/MEMORY.md`.
5. Verify `/ship`, `/audit`, `/review`, and `/test` command shims reference the routing contract and evidence schema.
6. Use the live smoke template after internals changes when an interactive Claude Code environment is available; otherwise mark each smoke command `NOT_RUN` with the environment reason.
7. Emit the fields required by `.claude/rules/evidence-schema.yml`.
