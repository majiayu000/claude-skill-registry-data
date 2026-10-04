---
name: review
description: Use when Codex should ask Claude CLI for an independent ordinary read-only code review, second-pass review, or sanity check. Trigger on requests such as ask Claude to review, run Claude review, get a Claude pass, use Claude Bridge review, or compare Claude's review against Codex findings.
---

# Claude Review

Use the local `claude` executable as an external reviewer. Treat Claude output as advisory and verify findings against the repository before editing or reporting them as true.

## Preflight

Do not run automatic executable validation or print-mode smoke tests. Limit local verification to static file and line inspection.

If the user explicitly requests executable validation, `setup` remains available as an explicit diagnostic command:

```powershell
node .\scripts\claude-bridge.mjs setup
```

## Runtime Isolation

The helper runs Claude Code with safe mode, no MCP configuration, slash commands disabled, Chrome disabled, and built-in tools limited to `Read`, `Glob`, `Grep`, and `Bash`. It uses `dontAsk` permission mode so unavailable actions fail instead of pausing for approval. Organization-managed policy may still apply.

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

Executable validation, Opus, `--deep`, retries, and fixes each require explicit user intent. Do not infer that intent from risk, difficulty, a failed review, or a review request.

Use Fable 5.1 only when the user explicitly requests Fable.

## Model Selection

- Use `claude-sonnet-5` by default for an ordinary review.
- Use `claude-opus-5-5` only when the user explicitly asks for Opus or `--deep`.
- Normalize shorthand only after the user selects a model: `sonnet5` and `sonnet-5` -> `claude-sonnet-5`; `opus` and `opus5.5` -> `claude-opus-5-5`; `fable` and `fable5.1` -> `claude-fable-5-1`; explicit `opus5` and `fable5` remain pinned to version 5; explicit legacy `opus4.8`, `opus 4.8`, and clear `opsu4.8` typos -> `claude-opus-4-8`.

## Review Prompt

Use this shape and preserve the user's scope:

```text
You are an independent code reviewer.
Scope: <exact diff, branch, files, or user-provided scope>
Do not edit files.
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
Prioritize correctness bugs, behavioral regressions, security risks, and missing tests.
Return findings first, ordered by severity, with file/line references.
If there are no actionable findings, say that clearly and mention residual test gaps.
```

## Preferred Helper

Prefer the bundled helper over hand-rolled Claude CLI calls. From a checked-out plugin source tree, run:

```powershell
node .\scripts\claude-bridge.mjs review --scope "all current uncommitted changes, including staged, unstaged, and untracked files"
```

If using this skill from its installed plugin cache, resolve the helper relative to this `SKILL.md` as `../../scripts/claude-bridge.mjs`.

Useful options:

- `--model claude-sonnet-5` for the default ordinary review model.
- `--deep` only when the user explicitly requests a deeper Opus pass.
- `--timeout <duration>` to override the hard limit; the default is `10m0s`, `15m0s` for model names containing `opus`, or `20m0s` for model names containing `fable`.
- `--scope "<scope>"` to preserve the user's exact target.

The helper stores prompt, JSON, markdown, and logs under `.codex/claude-bridge/`.

## Result Handling

Preserve Claude's findings, evidence boundaries, uncertainty notes, and file/line references. Verify claims locally before acting on them. Discard unsupported findings even when they sound plausible. Do not count a failed Claude run as a completed review. After presenting review findings, stop and ask the user which issues, if any, they want fixed before touching files.
