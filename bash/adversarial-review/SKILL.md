---
name: adversarial-review
description: Use when Codex should ask Claude CLI for an adversarial challenge review that pressure-tests implementation direction, design choices, assumptions, tradeoffs, and failure modes. Trigger on requests such as ask Claude for adversarial review, challenge this design, pressure-test with Claude, or get a hostile/critical Claude pass.
---

# Claude Adversarial Review

Use Claude CLI for a review-only challenge pass. This is not a normal defect sweep; it should question whether the approach should ship.

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

Executable validation, Opus, `--deep`, retries, and fixes each require explicit user intent. Do not infer that intent from risk, difficulty, a failed review, or an adversarial review request.

Normalize shorthand only after the user explicitly selects a model:

- `sonnet5` or `sonnet-5` -> `claude-sonnet-5`
- `opus` or `opus5.5` -> `claude-opus-5-5`; `fable` or `fable5.1` -> `claude-fable-5-1`
- Explicit `opus5` / `claude-opus-5` and `fable5` / `claude-fable-5` remain pinned to version 5
- `opus4.8` or `opus 4.8` -> `claude-opus-4-8`

Use Fable 5.1 only when the user explicitly requests Fable.

## Model Selection

- Use `claude-sonnet-5` for the default challenge review.
- Use `claude-opus-5-5` only when the user explicitly asks for Opus or `--deep`.
- Do not add reviewers or change models after a failure unless the user directly requests another pass.

## Adversarial Prompt

```text
You are an adversarial software reviewer.
Scope: <same exact scope the user gave>
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

Try to find the strongest reasons this should not ship yet.
Prioritize data loss, corruption, migrations, schema drift, concurrency, rollback, idempotency, trust boundaries, stale state, and missing tests.
Report only material findings grounded in files, line numbers, or command output.
Return in Korean unless the user requested another language.
Start with Findings ordered by severity. If no actionable finding, say so clearly.
Then give a short structural verdict: solid parts, fragile parts, and top 3 improvements.
```

## Preferred Helper

```powershell
node .\scripts\claude-bridge.mjs adversarial-review --scope "all current uncommitted changes, including staged, unstaged, and untracked files"
```

If using this skill from its installed plugin cache, resolve the helper relative to this `SKILL.md` as `../../scripts/claude-bridge.mjs`.

Use `--deep` or `--model claude-opus-5-5` only when the user explicitly requests Opus. The default timeout is `10m0s`, `15m0s` for model names containing `opus`, or `20m0s` for model names containing `fable`; an explicit `--timeout <duration>` overrides it.

The helper stores prompt, JSON, markdown, and logs under `.codex/claude-bridge/`.

Verify every claim locally before acting on it. Preserve inference and uncertainty labels. Do not let Claude edit files during this review. After presenting findings, stop and ask the user which issues, if any, they want fixed before touching files.
