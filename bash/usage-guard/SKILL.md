---
name: usage-guard
description: Subscription usage limits for Claude Code, Codex CLI and Antigravity CLI (agy). Use when the user asks how much usage or quota is left, or asks you to guard a task against the limit (pause until reset instead of failing mid-task).
license: MIT
compatibility: Requires python3 (3.9+) on macOS or Linux, a subscription login in Claude Code, Codex CLI or Antigravity CLI, and network access to api.anthropic.com, chatgpt.com or *.googleapis.com.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/usage_guard.py *) Bash(sleep *)
---

# Usage Guard

All usage data comes from one script, which reads the credentials itself and never prints tokens:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/usage_guard.py <provider> [--gate]
```

If `${CLAUDE_SKILL_DIR}` is not expanded in your environment, use the directory that contains this SKILL.md.
`<provider>` is `claude` (Claude Code), `codex` (Codex CLI), `agy` (Antigravity CLI) or `all`.
Leave credential files and keychains to the script, so tokens stay out of your context.

If a check fails with `network error` and your shell runs in a sandbox, rerun it outside the sandbox, asking for approval if needed.

## Report

When the skill is invoked without a task, or the user asks how much usage is left: run the script with the provider the user named, or `all`. Show the output verbatim in a code block, without commentary. Exit status 1 only means a provider failed, and its line already says so.

## Guard

When the user gives you a task and asks you to guard it (for example "keep /usage-guard in mind").

Guard only the CLI you are running in: Claude Code (or the Claude Agent SDK) → `claude`, Codex → `codex`, Antigravity → `agy`. For `agy`, add `--group <key>` with the model group you run on, such as `gemini_models` or `claude_and_gpt_models`; a wrong key returns an error listing the valid ones.
If you are none of these CLIs, say so once and continue the task unguarded.

Every guard message you write is one line.

1. Run `<provider> --gate` before you start, and then at the natural breaks in your own work: when you finish an item of your plan or todo list, after a test or build run, and before a commit. Run the check on its own, once the work before it has finished. Results are cached for 5 minutes, so checking often costs nothing.
2. Act on the first word of the line it prints:
   - `continue`: keep working silently.
   - `pause`: tell the user you are pausing until the reset shown, then **wait** (below).
   - `stop`: end the task with a message quoting the line.
   - `error`: say once that usage is not being guarded, continue, and retry at the next break.

### Wait

Repeat until `--gate` prints `continue`, then resume exactly where you left off:

1. Run `sleep N`, with N taken from the `sleep N` at the end of the `pause` line (at most 540 seconds). Set the shell tool timeout above it; in Claude Code use 600000 ms. If the shell refuses a foreground sleep, run it in the background and wait for it to finish. If a sleep is killed by a timeout, halve N.
2. Run `--gate` again. `stop` ends the task as above. `error` means sleep again and retry.

Each sleep costs one model turn, which is why the script picks long sleeps and ends the wait after 6 hours. While waiting, the only commands you run are the sleep and the check.
