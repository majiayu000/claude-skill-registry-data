---
name: rescue
description: Use when Codex should ask the Antigravity agy CLI for a rescue-style investigation, second opinion, debugging pass, or explicitly requested follow-up fix. Trigger on requests such as ask Antigravity to rescue this, have agy investigate, use Antigravity to debug, ask Antigravity for a fix plan, or let Antigravity try a constrained fix.
---

# Antigravity Rescue

Use `agy` for investigation or follow-up rescue work from Codex. Unlike `review` and `adversarial-review`, this skill can support implementation only when the user explicitly asks for a fix or patch. Otherwise keep Antigravity in investigation and plan mode.

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

## Mode Selection

- Use `Gemini 3.8 Flash (Medium)` by default for investigation, debugging, log interpretation, and fix planning.
- Use `Gemini 3.1 Pro (High)` with `--deep` only with explicit user intent for a deeper investigation.
- Use Claude, GPT-OSS, or any additional provider only with explicit user intent.
- If the user only asks for rescue/investigation, ask Antigravity for findings and a plan, not edits.
- If the user explicitly asks Antigravity to fix, constrain the scope and verify the resulting patch yourself before reporting completion.

## Investigation Prompt

```text
You are a rescue engineer giving Codex an external second opinion.
Scope: <exact user request and relevant files, logs, or diff>
Do not edit files unless the user explicitly requested a fix.
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
Return actionable findings, likely root cause, and the smallest safe next step.
If proposing a fix, include files and line references.
```

## Preferred Helper

```powershell
node .\scripts\antigravity-bridge.mjs rescue --scope "<user request and relevant context>"
```

Use `--deep` or `--model "Gemini 3.1 Pro (High)"` only when the user explicitly requests a deeper investigation.

Treat Antigravity output as advisory. Preserve observed facts, inferences, open questions, and next steps. Verify code claims and proposed fixes with static file and line inspection unless the user explicitly requests execution. If Antigravity was not successfully invoked, report the failure; do not retry, add another reviewer or provider, invent a substitute answer, or make fixes without explicit user intent.
