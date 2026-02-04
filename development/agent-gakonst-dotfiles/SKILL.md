---
name: agent
description: Use for PR/code reviews and any task that benefits from a dedicated tmux sub-agent with per-task git worktrees; default path for reviewing diffs (read diff → summarize → run checks/tests) with automated monitoring.
---

# Agent Control Panel (tmux + monitor)

## Overview
Use your current Codex window as the operator console. From here, create a dedicated tmux **session on the default tmux server (no custom socket)** that hosts sub-agent panes. You stay outside tmux as the driver—only the sub-agents run inside tmux windows—and you poll their output to know when to step in. This keeps the control session visible alongside your existing tmux workflow. **You are the hub; no separate “hub” window is spawned.** Default for any code review request: assume “full agent review” unless the user explicitly opts out.

## When to Use
- You need parallel sub-agents (e.g., multiple tasks/PRs) managed from one Codex session.
- Long-running interactive tools (debuggers, REPLs) where you want passive monitoring.
- Any scenario where Codex should only step in when a pane is stuck or asks a question.
- **Code reviews / PR reviews:** always choose this skill first; do not default to `web` for GitHub PRs.

## Core Pattern
1) **Session on the default tmux server (driven from THIS Codex window):**
   ```bash
   SESSION=control
   tmux new -d -s "$SESSION"
   ```
2) **Create a per-task git worktree (keeps tasks isolated):**
   ```bash
   task=feat-xyz
   git worktree add .worktrees/$task -b $task   # or checkout existing: git worktree add .worktrees/$task origin/$task
   ```
3) **Launch a sub-agent window (one task each; you remain outside):**
   ```bash
   tmux new-window -t "$SESSION" -n task-a
   tmux send-keys -t "$SESSION:task-a" -- 'cd .worktrees/task-a' Enter
   tmux send-keys -t "$SESSION:task-a" -- 'codex --dangerously-bypass-approvals-and-sandbox' Enter
   tmux send-keys -t "$SESSION:task-a" -- 'You are the sub-agent. Wait for a single natural-language prompt from the operator; you will execute all actions yourself. Do not ask the operator for confirmations.' Enter
   ```
   After Codex starts, **only send text prompts** (no shell commands) into this pane. The sub-agent handles execution inside its own Codex.
4) **Monitor loop (flag panes needing input; run from this control panel):**
   ```bash
   monitor_once() {
     for tgt in $(tmux list-panes -a -F '#{session_name}:#{window_name}.#{pane_index}'); do
       OUT=$(tmux capture-pane -p -J -t "$tgt" -S -120)
       NEED=$(printf "%s\n\nIs this pane waiting for operator input? Reply YES or NO only." "$OUT" \
         | codex exec --system "You are a detector. Reply YES if the pane asks a question/choice or is stalled; NO otherwise.")
       [ "$NEED" = "YES" ] && echo "$tgt"
     done
   }
   while true; do
     NEEDS=$(monitor_once); [ -n "$NEEDS" ] && { echo "Input needed: $NEEDS"; break; }
     sleep 10
   done
   ```
5) **Intervene minimally (from this Codex pane):** map the flagged pane to its tmux target (e.g., `control:task-a.0`) and send exactly one concise answer with `tmux send-keys -t <target> -- '...response...' Enter`; then restart the monitor loop.
6) **Tell the user how to attach/monitor** right after creating sessions and again when wrapping up:
   ```
   tmux attach -t control
   tmux capture-pane -p -J -t control:<window>.0 -S -200
   ```
7) **Cleanup:** `tmux kill-session -t "$SESSION"` (or `tmux kill-server` if dedicated). Remove worktrees when done: `git worktree remove .worktrees/task-a`.

## Default Code Review Flow (use this unless the user specifies otherwise)
1) Ensure repo/PR exists locally (clone if missing to `~/github/<owner>/<repo>`; create `.worktrees/pr-<num>` and `gh pr checkout <num>`).
2) Read the PR diff first and post a concise summary of changes/risks before running anything.
3) Run the standard checks for the stack (fmt/lint/tests) after summarizing unless the user opts for a lighter pass.
4) Deliver review findings ordered by severity with file/line refs; include any failed checks; suggest next steps.
5) Only deviate (skip tests, partial review) if the user explicitly requests it.

## Session Convention
- Use the default tmux server so the control session shows up alongside your existing tmux work (`tmux ls`, `tmux switch -t control`).
- Keep session/window names short and slug-like (`task-a`, `debug`, `ci`).

## Targeting & User Monitor Commands
- Pane target format `{session}:{window}.{pane}`, default `:0.0` if omitted.
- Keep a mapping of task → window name; set `TARGET="<session>:<window>.0"` before sends to avoid misrouting. Always include `-t "$TARGET"` on every `send-keys` and `capture-pane`.
- Immediately after starting any session/window, print both commands for the user:
  - Attach: `tmux attach -t control`
  - One-time capture: `tmux capture-pane -p -J -t control:<window>.0 -S -200`

## Sending Input Safely
- Prefer literal sends to avoid shell splitting: `tmux send-keys -t target -l -- "$cmd"` then `Enter`.
- For inline commands use single quotes or ANSI C strings: `tmux ... send-keys -- $'python3 -m http.server 8000' Enter`.
- Control keys: `C-c`, `C-d`, `C-z`, `Escape`, etc.
- After sending the natural-language prompt, **verify the model actually started**: capture the pane; if you still see the CLI welcome plus your prompt with no model output, send a single bare `Enter` (`tmux send-keys -t target Enter`) and re-check. Do not resend the full prompt unless the pane is empty.

## Watching Output
- Capture recent output: `tmux capture-pane -p -J -t target -S -200`.
- For continuous monitoring, rely on the monitor loop; avoid `tmux wait-for` (doesn’t watch pane text).

## Synchronizing / Waiting for Prompts
- Poll for prompts before sending commands, e.g.:
   ```bash
   ./tools/wait-for-text.sh -t "$SESSION":0.0 -p '^>>>' -T 15 -l 4000
   ```
- For long-running tasks, poll for completion strings (“Program exited”, etc.) before proceeding.

## Spawning Processes (defaults)
- Debugging: prefer `lldb` unless user requests otherwise.
- Python REPL: set `PYTHON_BASIC_REPL=1`; start with `python3 -q`; wait for `^>>>`; send code with `-l`; interrupt via `C-c`.

## Interactive Recipes
- **Python REPL:** `tmux ... send-keys -- 'PYTHON_BASIC_REPL=1 python3 -q' Enter`; wait for prompt; send code; `C-c` to interrupt.
- **gdb:** `tmux ... send-keys -- 'gdb --quiet ./a.out' Enter`; `set pagination off`; `C-c` to break; `bt`, `info locals`; exit `quit` then `y`.
- **Other TTY apps** (ipdb, psql, mysql, node, bash): start app, wait for prompt via `wait-for-text`, then send literal text + Enter.

## Cleanup
- Kill session: `tmux kill-session -t "$SESSION"`.
- Kill all agent sessions (if dedicated server not used): `tmux list-sessions -F '#{session_name}' | grep '^control$' | xargs -r -n1 tmux kill-session -t`.
- If you did start a dedicated server manually, kill it with `tmux kill-server`.
- Remove worktree when done: `git worktree remove .worktrees/<task>`.

## Tips
- Keep socket under `${TMPDIR:-/tmp}/agent-tmux-sockets`; names short (`task-a`, `task-b`).
- Use git worktrees under `.worktrees/<task>` so sub-agents never clash; point each Codex session at its worktree immediately.
- Use literal `send-keys -l`, `capture-pane -J`, `wait-for-text.sh`, and set `PYTHON_BASIC_REPL=1` before Python REPLs. Always print attach/capture commands for the user.
- Poll with `capture-pane -J` to avoid wrap artifacts; limit history to ~200 lines for speed.

## Quick Reference
- Start control session: `tmux new -d -s control`
- Launch agent window: `tmux new-window -t control -n foo; tmux send-keys -t control:foo -- 'codex ...' Enter`
- Monitor: loop over panes → `codex exec` classifier YES/NO → intervene → resume
- User attach: `tmux attach -t control`
- Cleanup: `tmux kill-session -t control`
- Helpers available: `tools/find-sessions.sh`, `tools/wait-for-text.sh` (copied locally). `find-sessions.sh` supports `-S SOCKET`, `-q filter`, or `--all` to scan socket dir; `wait-for-text.sh` supports `-t target -p regex [-F] [-T timeout] [-i interval] [-l lines]`.

## Red Flags
- Spawning a separate socket; the intent is to share the default tmux server so navigation is easy.
- Not printing attach/capture commands for the user.
- Letting multiple tasks share one pane (one task per window).
- Spamming multiple inputs before re-running the monitor loop.
- Sending input without an explicit `-t <target>` (risk of driving the wrong sub-agent).

## Prompting & Brainstorming Workflow
- **Always brainstorm with the user first** using the `brainstorm` skill to agree on the prompt content and success criteria before dispatching anything to a sub-agent.
- When ready, send a single, clear natural-language prompt into the sub-agent Codex pane (no shell commands). The sub-agent executes and reports back in that pane; you monitor and relay only when needed.
- Avoid running additional bash commands inside the sub-agent pane after Codex starts; keep interactions textual prompts/responses to maintain separation of concerns.
