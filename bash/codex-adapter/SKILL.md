---
name: codex-adapter
description: Route ONE bounded, mechanical task to the Codex CLI as a non-Claude executor, under the same review-before-merge gate as any other agent-produced diff. Use when the user explicitly asks to hand a task to Codex, or names OpenAI Codex / a non-Claude executor for a mechanical change (rename a symbol across files, add a config entry, apply a scripted find/replace). Not for open-ended or strategic work -- that stays with the operating Claude session.
allowed-tools: Read, Bash
user-invocable: true
triggers:
  - route this to codex
  - use codex for this
  - hand this to codex
  - run this through codex
  - codex exec
  - non-claude executor
---

# Codex Adapter

This is aigent-OS's first (and currently only) non-Claude executor: a thin wrapper around `daemons/codex-adapter.sh` that runs a single bounded, mechanical task through the [Codex CLI](https://developers.openai.com/codex)'s non-interactive `codex exec` mode.

## Scope -- what "bounded and mechanical" means

Good fits: a scripted rename, a config/gitignore entry, a repetitive multi-file edit with a clear before/after, a lint-fix pass. The task prompt you hand it should be checkable by a human (or you) glancing at the resulting diff -- if you can't describe in one sentence what "done" looks like, it's not bounded enough for this adapter; do it yourself instead.

Not a fit: architecture decisions, anything requiring judgment about tradeoffs, anything touching credentials/secrets/production config, anything the user hasn't explicitly asked to route to Codex.

## Before you invoke it

1. Confirm the Codex CLI is actually available: `command -v codex` (or whatever `AIGENT_CODEX_BIN` is set to). If it isn't installed, tell the user instead of guessing at a path.
2. State the bounded task in one sentence, and the target directory. If either is unclear, ask -- don't invoke on a guess.

## Invocation

```bash
bash daemons/codex-adapter.sh "<bounded task prompt>" --dir <path> [--sandbox <mode>]
```

- `AIGENT_CODEX_BIN` (env, default `codex`) -- path or name of the Codex CLI binary. Never hardcode a machine-specific path in the invocation; set the env var if the binary isn't on `PATH`.
- `--dir <path>` -- working directory the task runs in. Default: current directory.
- `--sandbox <mode>` -- passed through to `codex exec --sandbox`. Default `workspace-write` (Codex may read/write inside `--dir`, nothing wider).

Example:

```bash
AIGENT_CODEX_BIN=codex bash daemons/codex-adapter.sh \
  "Add a .gitignore entry for *.tmp files" --dir .
```

## After it runs -- the review gate

The adapter **never commits or pushes**. It writes:

- `.aigent/codex-runs/<timestamp>/output.log` -- the raw Codex CLI transcript
- `.aigent/codex-runs/<timestamp>/review.diff` -- a working-tree diff (tracked changes + a synthetic diff for any new untracked files) if `--dir` is a git repository
- `.aigent/codex-runs/<timestamp>/status.txt` -- `git status --porcelain` for the same tree

Read `review.diff` before doing anything else. Treat a Codex-produced change exactly like a sub-agent's diff: verify it does what was asked, then decide whether to stage/commit it yourself. If `--dir` isn't a git repository, the adapter says so explicitly and you review the files directly instead.

## What this is not

Not a general multi-LLM router -- it's one task class routed to one executor. Extending this to route by task type, or to wire additional CLIs (Gemini CLI, opencode, etc.) behind the same interface, is future work, not something to imply is already live.
