---
name: tmux
description: Use when starting servers or ongoing processes, running commands the user requested, or inspecting existing terminals, tmux panes, sessions, or logs. Find and reuse the relevant pane, and manage temporary terminal work in the shared Codex window.
---

# Tmux

Use tmux as shared terminal state.

When the user refers to a running terminal, pane, session, logs, dev server, or "what I have open", proactively inspect tmux instead of waiting for an exact pane target. Treat pane contents as first-class task context.

## Workflow

1. Discover panes first.
   - If discovery reports a socket permission error or `Operation not permitted`, rerun the same read-only helper command with sandbox escalation. A socket failure is not evidence that tmux is stopped or has no sessions.
   - Treat an empty result as authoritative only when the helper exits successfully; the helper intentionally surfaces tmux connection failures.
2. Read recent scrollback from likely panes.
3. Choose a target pane from cwd, command, title, and recent output.
4. Write only after the target is clear.
5. Capture the pane again after writing to confirm the result.

Use the helper script:

```bash
$HOME/.codex/skills/tmux/scripts/tmux_helper.py list
$HOME/.codex/skills/tmux/scripts/tmux_helper.py snapshot --lines 60
$HOME/.codex/skills/tmux/scripts/tmux_helper.py search "strava"
$HOME/.codex/skills/tmux/scripts/tmux_helper.py capture main:3.1 --lines 120
$HOME/.codex/skills/tmux/scripts/tmux_helper.py send main:3.1 --text "npm test" --enter
$HOME/.codex/skills/tmux/scripts/tmux_helper.py setup-codex --cwd "$HOME/Code/sandbox"
```

## Reading Rules

- Inspect tmux automatically when it is plausibly relevant.
- Expect the user's default tmux server to be long-running at the normal per-user socket. Codex app sandboxing may block that socket even when the server is attached.
- Start with `snapshot` for broad context when the target pane is unclear.
- Use `search` when the user references a string, error, branch, port, command, or secret that may be visible in scrollback.
- Use `capture` for deeper history once a pane is selected.
- Prefer the pane whose cwd, running command, title, or recent output matches the user's request.

## Writing Rules

- If the user does not specify a write target, default to the dedicated Codex pane.
- Write to non-Codex panes when the user explicitly asks, or when it is clearly required to continue the task.
- Before writing to a pane, capture a short tail so you do not stomp on unexpected state.
- For a newly created pane, expect shell startup prompts or plugin prompts to consume the first keystrokes. Capture first, then clear or answer the prompt intentionally before sending the real command.
- Use literal text plus optional `Enter` for normal commands.
- Avoid sending interrupts, control keys, navigation keys, or editor commands unless the user clearly asks for that level of control.
- Treat full-screen TUIs such as `vim`, `nvim`, `lazygit`, `less`, `man`, `htop`, and similar tools as risky targets. Prefer a shell pane or the Codex pane unless the user explicitly wants interaction inside that TUI.

## Codex Pane Convention

- Reserve a tmux window named `codex` for shared work.
- Reuse it if it already exists.
- Treat the first pane in that window as the default Codex-owned pane.
- Set the pane title to `codex` during setup.
- When writing to another pane, state the exact tmux target in commentary.

## Window limits and pane cleanup

- Hard cap: nine windows per session, including user-owned windows. Count existing windows before creating one. Never create a tenth window or close a user-owned window to make room.
- Reuse an available pane first. Prefer splits over new windows when another process needs its own pane.
- Run temporary commands, experiments, retries, and offshoot work in splits within the `codex` window. A new command or task alone does not justify a new window.
- Create a new window only for a persistent workflow that needs multiple panes. State the concrete reason before creating it, check the cap, and reuse an existing workflow window whenever possible.
- Record the stable pane IDs of temporary panes you create. Close those panes as soon as their work is finished and their useful output has been captured. Do not leave idle shells behind after a task.
- Keep a pane open while it runs a process the user still needs. Inspect it before cleanup. Do not close user-owned panes or panes created by another active task without authorization.
- Keep the default `codex` pane available for reuse. When an agent-created workflow is finished and no longer needed, close its panes and window.

Create or reuse the dedicated workspace with:

```bash
$HOME/.codex/skills/tmux/scripts/tmux_helper.py setup-codex --cwd "$HOME/Code/sandbox"
```

## Target Resolution

The helper accepts:

- Exact tmux targets such as `main:3.1` or `%12`
- Window names such as `codex`
- Pane titles such as `codex`
- Unique substrings from pane cwd or current command

If a fuzzy target matches multiple panes, inspect with `list` or `snapshot` and choose explicitly.

## Output Discipline

- In commentary, say which pane you are reading or writing when it matters.
- After a write, show the confirming tail or summarize the effect.
- If no plausible pane matches the request, say so and fall back to normal shell work.
