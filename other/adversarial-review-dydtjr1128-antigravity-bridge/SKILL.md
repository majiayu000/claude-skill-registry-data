---
name: adversarial-review
description: Use when Codex should ask the Antigravity agy CLI for an adversarial challenge review that pressure-tests implementation direction, design choices, assumptions, tradeoffs, and failure modes. Trigger on requests such as ask Antigravity for adversarial review, challenge this design with agy, pressure-test with Antigravity, or get a hostile/critical Antigravity pass.
---

# Antigravity Adversarial Review

Use `agy` for a review-only challenge pass. This is not a normal defect sweep; it should question whether the approach should ship.

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

- Use `Gemini 3.8 Flash (High)` for routine adversarial review.
- Use `Gemini 3.1 Pro (High)` with `--deep` only with explicit user intent for a deeper review.
- Use `Claude Opus 4.6 (Thinking)`, `GPT-OSS 120B (Medium)`, or any additional provider only with explicit user intent.

## Adversarial Prompt

```text
You are an adversarial software reviewer.
Scope: <same exact scope the user gave>
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

Try to find the strongest reasons this should not ship yet.
Prioritize data loss, corruption, migrations, schema drift, concurrency, rollback, idempotency, trust boundaries, stale state, and missing tests.
Report only material findings grounded in files, line numbers, or command output.
Return in Korean unless the user requested another language.
Start with Findings ordered by severity. If no actionable finding, say so clearly.
Then give a short structural verdict: solid parts, fragile parts, and top 3 improvements.
```

## Preferred Helper

```powershell
node .\scripts\antigravity-bridge.mjs adversarial-review --scope "all current uncommitted changes, including staged, unstaged, and untracked files"
```

Use `--deep` or `--model "Gemini 3.1 Pro (High)"` only when the user explicitly requests a deeper pass.

The helper stores prompt, stdout, stderr, Antigravity log, metadata, and markdown result under `.codex/antigravity-bridge/`.

Verify every claim with static file and line inspection before reporting it as true. Preserve inference and uncertainty labels. Do not retry a failed run, add another reviewer or provider, or let Antigravity edit files without explicit user intent. After presenting findings, stop and obtain explicit user intent before fixing any issue.
