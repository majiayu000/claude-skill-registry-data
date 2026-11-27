---
name: tmux-agent-control
description: >-
  Take over or monitor an interactive coding agent in a tmux pane. When asked to send the next
  prompt after the current turn, find the process and pane, read its terminal state and wait until
  the TUI is idle before sending the whole instruction. Not for launching a headless coding CLI.
metadata:
  revision: "5"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "drive a live TUI agent in tmux: find the pane, prove idle, send one complete instruction"
  summary_zh: "在 tmux 中驱动运行中的 TUI agent：定位 pane、证明空闲、一次发出完整指令"
  kind: "entry"
---

# Control an interactive tmux agent

Monitor an existing TUI; use `gdd-route-omp` or the supported headless route
for unattended one-shot work. Sending, starting a new session, or restarting
an agent needs explicit authority. Do not send into a shared composer or
start a second writer in the same checkout.

1. Find the intended live agent by process, matching cwd, repo and its tmux
   pane. The pane PID can be its parent shell: establish the relationship
   to the actual agent. Record the pane ID and PID, not just the session name.
2. Capture visible state and verify a clean composer, no modal, no busy
   indicators and stable captures across a real interval. Check current
   harness state for exit, restart, retry or continuation; an unchanged
   redraw is not proof of idle. If any evidence is unavailable, monitor
   without sending.
3. Re-resolve the same pane identity before pasting and again before Enter.
   Paste the complete instruction, read the composer back, and submit only
   on an exact match. For multiline text use an authorized, uniquely named
   tmux paste buffer and bracketed paste, not literal newlines in send-keys.
   Never auto-dismiss a modal. If either send fails, leave the state intact
   and report it; do not retry into a draft or an uncertain turn.
4. Save captures and command statuses. After submission require new turn
   evidence and a return to verified idle. Inspect output, actual changes and
   the repo's gates before calling the task done. Compare per-item claims
   with aggregate results and verify alleged baseline failures separately.

For one-line submissions use [watcher configuration](references/watcher.md).
For Linux and OMP-specific diagnostics or restart recovery, read
[harness internals](references/harness-internals.md).
