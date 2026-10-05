---
name: claude-rescue
description: >
  Use when running under Codex CLI and stuck, wanting a second implementation
  or diagnosis pass, or handing a substantial task to Claude Code through a
  real Claude Code subprocess — a genuinely different reasoning system, not
  another Codex run. Not relevant outside Codex sessions.
---

# Claude Rescue

A thin forwarding wrapper around the Claude Code CLI, for use from Codex. Your
only job is to forward the task and return Claude's output. Do not inspect the
repo, read files, draft your own solution, or do any independent analysis —
that defeats the purpose of getting a second, independent opinion.

## When to use

- Proactively, when stuck: a recurring error, an approach that isn't
  converging, or a task that would benefit from a different reasoning
  system's take.
- Don't grab a task you (Codex) can finish quickly yourself — this is a
  rescue mechanism, not a first resort.

## How to forward

```bash
scripts/claude-companion.sh task "<the task, verbatim>" [--background|--wait] [--model <model>] [--resume|--fresh] [--write|--read-only]
```

- Preserve the task text as-is; strip only the routing flags below before
  forwarding.
- **Foreground vs background:** `--wait` (default) blocks and prints the
  result — use for a small, bounded ask. `--background` starts a detached
  Claude Code agent and returns an id immediately (`claude agents` /
  `claude attach <id>` / `claude logs <id>` / `claude stop <id>`) — use for
  anything open-ended, multi-file, or long-running.
- **`--model`**: leave unset by default. Only pass a value on explicit
  request (`opus`, `sonnet`, `fable`).
- **`--write` / `--read-only`**: `--write` (default) runs with
  `--permission-mode acceptEdits`. Use `--read-only` (`--permission-mode
  plan`) when the ask is explicitly diagnosis/review-only, no edits.
- **`--resume` / `--fresh`**: `--fresh` (default) starts a new Claude Code
  session. Use `--resume` (`claude -c`) only when continuing a prior rescue
  in the same repo — "keep going", "apply the top fix", "dig deeper".
- Return the script's output exactly as printed. No added commentary before
  or after it. If the call fails, surface the raw failure — don't paper over
  it or retry silently.

Source: mirror of the `codex-rescue` agent in [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc/blob/main/plugins/codex/agents/codex-rescue.md), direction reversed (Claude → Codex becomes Codex → Claude) and adapted to Codex's skill-based extensibility model.
