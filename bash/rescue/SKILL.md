---
name: rescue
description: Use when Codex should ask Claude CLI for a rescue-style investigation, second opinion, debugging pass, or explicitly requested follow-up fix. Trigger on requests such as ask Claude to rescue this, have Claude investigate, use Claude to debug, ask Claude for a fix plan, or let Claude try a constrained fix.
---

# Claude Rescue

Use Claude CLI for investigation or follow-up rescue work from Codex. Unlike `review` and `adversarial-review`, this skill can support implementation only when the user explicitly asks for a fix or patch. Otherwise keep Claude in investigation and plan mode.

## Preflight

Do not run automatic executable validation or print-mode smoke tests. Limit local verification to static file and line inspection.

If the user explicitly requests executable validation, `setup` remains available as an explicit diagnostic command:

```powershell
node .\scripts\claude-bridge.mjs setup
```

For an explicitly requested fix, add `--allow-edits` to the helper invocation. This enables and permits built-in `Edit` and `Write`; without it, return investigation findings and a fix plan. The option does not authorize shell writes or program execution.

## Runtime Isolation

The helper runs Claude Code with safe mode, no MCP configuration, slash commands disabled, Chrome disabled, and built-in tools limited by default to `Read`, `Glob`, `Grep`, and `Bash`. It uses `dontAsk` permission mode so unavailable actions fail instead of pausing for approval. Organization-managed policy may still apply.

## Bounded Execution Policy

Do not execute project code or validation commands unless the user explicitly and directly requests that execution. This includes tests, builds, package managers, scripts, servers, applications, CI, deployment, release, and workflow automation. A review or investigation request alone is not permission to execute them.
Read-only repository inspection commands required to obtain the requested scope are allowed, including `git diff`, `git status`, `git show`, `git log`, `git blame`, and `git ls-files`.
When the scope is current uncommitted work, include staged, unstaged, and untracked files; enumerate them with read-only Git inspection before reviewing only those changes.
Do not use shell commands for any other purpose, and do not run commands that modify files, the index, refs, configuration, or other repository state.
Complete one bounded pass within the helper-selected timeout: ten minutes for standard models, fifteen minutes for model names containing `opus`, and twenty minutes for model names containing `fable`.
Do not retry, add reviewers, expand the scope, or switch to a deeper model automatically.
If the available time or evidence is insufficient, return the supported findings and state the remaining gap.
Start with the exact diff or named files in scope and inspect only directly relevant dependencies needed to support a concrete finding.
Do not perform repository-wide discovery, recursively follow references, or pursue speculative context.
Once a finding has enough static evidence, report it; if evidence remains insufficient, state the uncertainty and remaining gap instead of continuing to investigate.

Executable validation, Opus, `--deep`, retries, and fixes each require explicit user intent. Do not infer that intent from risk, difficulty, a failed attempt, or a rescue request.

Normalize model shorthand only after the user explicitly selects a model:

- `sonnet5` or `sonnet-5` -> `claude-sonnet-5`
- `opus` or `opus5.5` -> `claude-opus-5-5`; `fable` or `fable5.1` -> `claude-fable-5-1`
- Explicit `opus5` / `claude-opus-5` and `fable5` / `claude-fable-5` remain pinned to version 5
- `opus4.8` or `opus 4.8` -> `claude-opus-4-8`

Use Fable 5.1 only when the user explicitly requests Fable.

## Mode Selection

- Use `claude-sonnet-5` by default for investigation, log interpretation, and fix planning.
- Use `claude-opus-5-5` only when the user explicitly asks for Opus or `--deep`.
- Do not retry, add reviewers, or change models after a failed attempt unless the user directly requests another pass.
- If the user asks only for investigation, return findings and a plan; make a constrained fix only when explicitly requested.

## Investigation Prompt

```text
You are a rescue engineer giving Codex an external second opinion.
Scope: <exact user request and relevant files, logs, or diff>
Do not edit files unless the user explicitly requested a fix.
Do not execute project code or validation commands unless the user explicitly and directly requests that execution. This includes tests, builds, package managers, scripts, servers, applications, CI, deployment, release, and workflow automation. A review or investigation request alone is not permission to execute them.
Read-only repository inspection commands required to obtain the requested scope are allowed, including `git diff`, `git status`, `git show`, `git log`, `git blame`, and `git ls-files`.
Do not use shell commands for any other purpose, and do not run commands that modify files, the index, refs, configuration, or other repository state.
Complete one bounded pass within the helper-selected timeout: ten minutes for standard models, fifteen minutes for model names containing `opus`, and twenty minutes for model names containing `fable`.
Do not retry, add reviewers, expand the scope, or switch to a deeper model automatically.
If the available time or evidence is insufficient, return the supported findings and state the remaining gap.
Start with the exact diff or named files in scope and inspect only directly relevant dependencies needed to support a concrete finding.
Do not perform repository-wide discovery, recursively follow references, or pursue speculative context.
Once a finding has enough static evidence, report it; if evidence remains insufficient, state the uncertainty and remaining gap instead of continuing to investigate.
Limit verification to static file and line inspection.
Return actionable findings, likely root cause, and the smallest safe next step.
If proposing a fix, include files and line references.
```

## Preferred Helper

```powershell
node .\scripts\claude-bridge.mjs rescue --scope "<user request and relevant context>"
# Only after an explicit request for a fix:
node .\scripts\claude-bridge.mjs rescue --allow-edits --scope "<authorized fix scope>"
```

If using this skill from its installed plugin cache, resolve the helper relative to this `SKILL.md` as `../../scripts/claude-bridge.mjs`.

Use `--deep` or `--model claude-opus-5-5` only when the user explicitly requests Opus. The default timeout is `10m0s`, `15m0s` for model names containing `opus`, or `20m0s` for model names containing `fable`; an explicit `--timeout <duration>` overrides it.

Treat Claude output as advisory. Preserve observed facts, inferences, open questions, and next steps. Verify code claims, command claims, and proposed fixes locally. If Claude was not successfully invoked, report the failure and do not invent a substitute rescue answer.
