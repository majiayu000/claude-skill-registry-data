---
name: claude-agent
description: Run Claude Code CLI headless as an independent coding agent for implementation, investigation, planning, or review in a local workspace. Use when asked to delegate work to a separate Claude session, capture a Claude session ID, or resume and continue an earlier headless Claude run.
---

# Claude Agent

Run `claude -p` from the intended workspace, give it a bounded outcome,
monitor it at the task's time scale, and preserve its session ID when
follow-up work is likely.

Read `/cross-provider-agent` first and apply its doctrine to the whole
dispatch; this skill is only the Claude transport.

## Check the CLI and authentication

Treat installed help as authoritative because Claude Code evolves:

```bash
claude --version
claude --help
```

If a run fails with an authentication error, ask the user to run `claude`
interactively and `/login`. Never display, copy, or embed authentication
files or tokens.

## agent permissions

Use the least authority that completes the task. Default analysis, planning,
and review to `--permission-mode plan`; for authorized implementation drop it
and grant the task's specific needs with `--allowedTools`. Never add
`--dangerously-skip-permissions` merely to make a run unattended.

## Start a worker

Run from the intended workspace directory — the working directory is the
workspace.

```bash
cd /absolute/path/to/workspace && claude -p --output-format json \
  --permission-mode plan \
  "[message]"
```

## Capture the session ID

When the ID must be known even if the first turn is interrupted, allocate it
up front and pass it with `--session-id "$(uuidgen)"`. Otherwise read
`session_id` from the terminal result object.

## Resume a session

Resume with `--resume "$claude_session_id"`. Use `--continue` only when
continuing the most recent conversation is unambiguous. Add `--fork-session`
when the follow-up must not extend the original session's history.

## Monitor and verify

On completion require a zero exit status and `"is_error": false` in the
result object; the `result` field contains the worker's response.

## Profiled dispatch

```bash
cd /absolute/path/to/workspace && claude -p --output-format json \
  --settings /absolute/path/to/claude-agent/profiles/github-pr-reviewer/settings.json \
  --setting-sources "" \
  --plugin-dir /absolute/path/to/skills-repo \
  "REVIEW_TASK"
```

`--setting-sources ""` keeps pre-existing configuration from widening the
child's authority, but also unloads installed skills, so `--plugin-dir` loads
the skills repository root — always the repo that provides this adapter,
never the workspace under review. Cite skills by namespaced name
(`skills-repo:code-review`); the bare name resolves to Claude's bundled
code-review, which rejects model invocation.

### available profiles
**github-pr-reviewer** : `profiles/github-pr-reviewer/settings.json` encodes
the profile from `/cross-provider-agent` as pure permission rules: `dontAsk`
default mode (auto-denies anything not pre-approved, so a headless run never
stalls on a prompt), narrow allows for workspace reads and the profile's `gh`
surface, and explicit denies for the nearby writes.
