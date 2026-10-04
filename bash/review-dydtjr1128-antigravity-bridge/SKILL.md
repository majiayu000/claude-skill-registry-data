---
name: review
description: Use when Codex should ask the Antigravity agy CLI for an independent ordinary read-only code review, second-pass review, or sanity check. Trigger on requests such as ask Antigravity to review, run agy review, get an Antigravity pass, use Antigravity Bridge review, or compare Antigravity findings against Codex findings.
---

# Antigravity Review

Use the local `agy` executable as an external reviewer. Treat Antigravity output as advisory and verify findings against the repository before editing or reporting them as true.

## Execution and Time Policy

Do not execute project code or validation commands unless the user explicitly and directly requests that execution. This includes tests, builds, package managers, scripts, servers, applications, CI, deployment, release, and workflow automation. A review or investigation request alone is not permission to execute them.
Read-only repository inspection commands required to obtain the requested scope are allowed, including `git diff`, `git status`, `git show`, `git log`, `git blame`, and `git ls-files`.
When the scope is current uncommitted work, include staged, unstaged, and untracked files; enumerate them with read-only Git inspection before reviewing only those changes.
Do not use shell commands for any other purpose, and do not run commands that modify files, the index, refs, configuration, or other repository state.
Complete one bounded pass within five minutes.
Do not retry, add reviewers, expand the scope, or switch to a deeper model automatically.
If the available time or evidence is insufficient, return the supported findings and state the remaining gap.
Start with the exact diff or named files in scope and inspect only directly relevant dependencies needed to support a concrete finding.
Do not perform repository-wide discovery, recursively follow references, or pursue speculative context.
Once a finding has enough static evidence, report it; if evidence remains insufficient, state the uncertainty and remaining gap instead of continuing to investigate.

Use static file and line inspection only by default. `setup` remains available as an explicit diagnostic command, but run it or otherwise validate the `agy` executable only when the user explicitly requests executable validation.

## Model Selection

- Use `Gemini 3.8 Flash (Medium)` by default for ordinary reviews.
- Use `Gemini 3.8 Flash (High)` only when the user explicitly requests that model.
- Use `Gemini 3.1 Pro (High)` with `--deep` only with explicit user intent for a deeper review.
- Use `Claude Opus 4.6 (Thinking)` or any additional provider only with explicit user intent.

## Review Prompt

Use this shape and preserve the user's scope:

```text
You are an independent code reviewer.
Scope: <exact diff, branch, files, or user-provided scope>
Do not edit files.
Do not execute project code or validation commands unless the user explicitly and directly requests that execution. This includes tests, builds, package managers, scripts, servers, applications, CI, deployment, release, and workflow automation. A review or investigation request alone is not permission to execute them.
Read-only repository inspection commands required to obtain the requested scope are allowed, including `git diff`, `git status`, `git show`, `git log`, `git blame`, and `git ls-files`.
Do not use shell commands for any other purpose, and do not run commands that modify files, the index, refs, configuration, or other repository state.
Complete one bounded pass within five minutes.
Do not retry, add reviewers, expand the scope, or switch to a deeper model automatically.
If the available time or evidence is insufficient, return the supported findings and state the remaining gap.
Start with the exact diff or named files in scope and inspect only directly relevant dependencies needed to support a concrete finding.
Do not perform repository-wide discovery, recursively follow references, or pursue speculative context.
Once a finding has enough static evidence, report it; if evidence remains insufficient, state the uncertainty and remaining gap instead of continuing to investigate.
Use static file and line inspection only to ground findings.
Prioritize correctness bugs, behavioral regressions, security risks, and missing tests.
Return findings first, ordered by severity, with file/line references.
If there are no actionable findings, say that clearly and mention residual test gaps.
```

## Preferred Helper

Prefer the bundled helper over hand-rolled `agy` calls:

```powershell
node .\scripts\antigravity-bridge.mjs review --scope "all current uncommitted changes, including staged, unstaged, and untracked files"
```

Useful options:

- `--model "Gemini 3.8 Flash (Medium)"` for the default ordinary review model.
- `--deep` to prefer `Gemini 3.1 Pro (High)` only when the user explicitly requests a deeper review.
- `--scope "<scope>"` to preserve the user's exact target.
- `--dry-run` to inspect the generated prompt without calling `agy`.

The helper stores prompt, stdout, stderr, Antigravity log, metadata, and markdown result under `.codex/antigravity-bridge/`.

## Result Handling

Preserve Antigravity's findings, evidence boundaries, uncertainty notes, and file/line references. Verify claims with static file and line inspection before reporting them as true. Discard unsupported findings even when they sound plausible. Do not retry a failed run or add another reviewer or provider without explicit user intent. After presenting review findings, stop and obtain explicit user intent before fixing any issue.
