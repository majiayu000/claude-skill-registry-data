---
name: mathodology-whole-project
description: Use when starting a modeling task or installing, backing up or maintaining the skills pack.
---

# Mathodology Modeling Companion

Mathodology helps turn a problem into a justified model, reproducible results and
clear scientific communication. It is a skills pack, not an application or an
execution engine. Use [modeling prompts](../mathodology-agent-pipeline/SKILL.md)
as a flexible guide. For figures use
[figure presets](../mathodology-figure-presets/SKILL.md), including its image2
availability question. For evidence use
[evidence search](../mathodology-evidence-search/SKILL.md).

## Start or resume a modeling task

Read the problem, available data, existing results and applicable contest rules.
Ask about missing constraints that would change the answer. Reuse established
preferences and continue from the current evidence. Keep a short note of important
assumptions and decisions if it helps continuity; no special schema is needed.

Work in the user's chosen directory or an ignored `work/` directory in this
checkout. Produce only artifacts needed for the requested deliverable. Keep
numerical results traceable. Use specialists where they help and the host allows
it; an independent review can challenge important claims without fixed panels.

## Maintain and distribute

The maintained source is `.claude/skills/`. Claude Code roles and workflow prompts
are adjacent. Codex may use an installed `.agents/skills/` mirror. Back up this
project's mirror before updating its Mathodology entries. Do not modify unrelated
skills, project instructions, custom MCP settings or global configuration.

For installation in other projects, use the standard skills CLI; for a clean
repository checkout, use `git pull --ff-only`. Resolve local edits before updating;
do not reset them. Installation details are in the repository's docs/INSTALL.md.
A skills-only global install does not install project roles or MCP settings.

The optional [backup utility](scripts/create-source-backup.sh) saves skills,
references and repository docs, including local uncommitted source changes:

```bash
bash .claude/skills/mathodology-whole-project/scripts/create-source-backup.sh
```

It excludes the ignored Codex mirror, contest outputs and Git history. Back those
up separately when needed. Extract a backup into an empty directory and verify
its checksum before replacing an installation. No application build is required.
