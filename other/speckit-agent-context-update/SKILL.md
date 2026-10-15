---
name: speckit-agent-context-update
description: Refresh the managed Spec Kit section in coding agent context file(s)
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: extension:agent-context
user-invocable: true
disable-model-invocation: false
model: sonnet
---

# Agent Context Update Skill

# Update Coding Agent Context

Refresh the managed Spec Kit section inside the active coding agent's context/instruction file (e.g. `CLAUDE.md`, `.github/copilot-instructions.md`, `AGENTS.md`).

## Behavior

The script reads the agent-context extension config at
`.specify/extensions/agent-context/agent-context-config.yml` to discover:

- `context_file` — the path of the coding agent context file to manage.
- `context_files` — optional project-relative paths for multiple coding agent context files. When non-empty, the script updates each listed file and the list takes precedence over `context_file`.
- `context_markers.start` / `.end` — the delimiters surrounding the managed section. Defaults to `<!-- SPECKIT START -->` and `<!-- SPECKIT END -->` when the field is missing.

It then creates, replaces, or appends the managed block so that the section points at the most recent plan path when one can be discovered (any `plan.md` under `specs/`, including nested scoped layouts such as `specs/<scope>/<feature>/plan.md`).

If `context_files` and `context_file` are empty, the command reports nothing to do and exits successfully. Context file paths must stay project-relative; absolute paths, Windows drive paths, backslash separators, and `..` path segments are rejected.

## In motor-fix

The config names `.specify/agent-context.local.md`, a git-ignored file, and the
`after_specify` and `after_plan` hooks that ran this command are off. The block
named the active plan, and a tracked copy of it made every open feature branch
conflict at each merge; `.claude/hooks/session-context.mjs` now prints
the pointer from `.specify/feature.json` at session start. Never point the
config at a tracked file, and never leave it empty: the script then self-seeds
`CLAUDE.md`. `.claude/scripts/active-plan-pointer.spec.mjs` checks both.

## Execution

- **Bash**: `.specify/extensions/agent-context/scripts/bash/update-agent-context.sh [plan_path]`
- **PowerShell**: `.specify/extensions/agent-context/scripts/powershell/update-agent-context.ps1 [plan_path]`

When `plan_path` is omitted, the script auto-detects the most recently modified `specs/**/plan.md` (searched recursively, so nested scoped layouts are discovered).

## Done When

- [ ] The managed `<!-- SPECKIT START/END -->` block is the only region touched — nothing outside it changed
- [ ] No spec-kit content was written into a tracked file; `AGENTS.md` stays the shared guidance and local practice stays in `CLAUDE.local.md`
- [ ] The refreshed block names only technologies the repo actually uses, verified against `package.json`

## The file may shrink; it may not grow

Before finishing, run:

```bash
node .claude/scripts/context-audit.mjs
```

The agent context file, `CLAUDE.local.md`, is ratcheted against
`.specify/context-baseline.json`, and `pre:edit:config-protection` blocks an
edit that takes it past that line. The rule is BMAD's, and it is the right one
for a file loaded into every session: a line earns its place only if **removing
it would change what the agent does**. Implementation detail the agent can read,
ecosystem defaults it already knows, repo structure maps and history all fail
that test.

So this command is not append-only. Each run:

1. Add what genuinely changed behaviour.
2. Act on the audit findings — dead references, strikethrough history, lines
   that only name a path, lines duplicated from the constitution.
3. Leave the total the same or smaller. If it must grow, record why:
   `node .claude/scripts/context-audit.mjs --bless --allow-growth "<reason>"`.

One rule that is not symmetrical, also BMAD's: a policy or pitfall is removed
only when the thing it is about is gone, or when a human removes it. No recent
failure is not evidence a rule is unnecessary — a working rule erases the
evidence of its own need.
