---
name: cli-control
description: Verify terminal-hosted CLI or TUI behavior with repeatable local evidence. Use for output, prompts, interactive input, signals, hangs, resizing, startup, exit status, or terminal restoration; not for browser, desktop, or Electron interfaces, which belong to ui-control.
---

# CLI Control

Gather reproducible evidence from a terminal-hosted interface without changing production behavior.

## Workflow

1. Identify the command, the working directory, the terminal conditions, and the observable contract.
2. Choose the method. Run ordinary output and exit-status checks directly or through the repository's tests. A command run through a pipe has no terminal, and many programs then skip prompts, colors, or line editing, so piped output does not prove terminal behavior. Use a pseudo-terminal for prompts, interactive input, signals, resizing, hangs, or restoration.
3. Bound every run with the host's command timeout or `timeout`, so a hang becomes evidence instead of a stuck session.
4. Prefer an existing trusted harness. Otherwise use `tmux` as the pseudo-terminal:

   ```sh
   tmux new-session -d -s probe -x 120 -y 40
   tmux set-option -t probe remain-on-exit on
   tmux respawn-pane -k -t probe '<command>'
   tmux capture-pane -t probe -p          # read the screen
   tmux send-keys -t probe 'text' Enter   # type; C-c sends SIGINT
   tmux resize-window -t probe -x 80 -y 24
   tmux display -p -t probe '#{pane_dead} #{pane_dead_status}'   # exit status
   tmux kill-session -t probe
   ```

   Wait for a state by polling `capture-pane` for the expected text with a bounded number of attempts, not by fixed sleeps.
5. Drive one action at a time, and capture the smallest transcript or measurement that proves or disproves the behavior.
6. Check interrupts, cleanup, exit status, hangs, and terminal restoration only where they matter to the contract.
7. Clean up only the sessions, processes, and files that this workflow created.

Keep verification read-only unless the parent task separately authorizes implementation. Use `behavior-implement` and `test-design` for fixes or regression tests. Do not send credentials or destructive commands, keep sensitive transcripts, or leave one-off harness code in the repository.

## Result

Report the command and conditions, the observed output and exit status, the evidence, and any blocker or limitation.
