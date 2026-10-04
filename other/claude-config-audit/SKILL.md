---
name: claude-config-audit
description: >
  Audit the .claude configuration for valid frontmatter, discoverable agents and
  skills, missing skill references, stale slash-command plugin names, broad
  permissions, and hook/settings regressions.
disable-model-invocation: true
when_to_use: >
  Invoke explicitly for `.claude/**`, CLAUDE.md, AGENTS.md, hooks, commands, skills,
  agents, or agent-memory changes; docs-memory-curator and /audit may preload it.
---

# Claude Config Audit

Use this skill before merging any change under `.claude/**`, `CLAUDE.md`, or agent-memory files.

## Workflow

1. Parse YAML frontmatter in every `.claude/**/*.md` file.
2. Build inventories for agents, skills, commands, rules, imports, output styles, hooks, and memory.
3. Verify every agent `skills:` entry maps to `.claude/skills/<name>/SKILL.md`.
4. Search slash commands for stale `agent-skills:*` references and browser-only workflows that do not apply to this terminal simulator.
5. Check orchestrators for overly broad delegation and confirm `/ship` requires DegenExus verification evidence.
6. Confirm `.claude/settings.json` exists and contains conservative secret/destructive-command denies plus hook wiring.
7. Report findings as `BLOCKER`, `IMPORTANT`, or `SUGGESTION` with exact file paths.

## Required Local Commands

```bash
python .claude/hooks/validate-claude-config.py
python -m compileall -q .claude/hooks
```

## Exit Criteria

- Frontmatter parses cleanly.
- Agent skill references are resolvable.
- Commands reference local agents/skills or documented project workflows only.
- Hooks and settings are present and auditable.
