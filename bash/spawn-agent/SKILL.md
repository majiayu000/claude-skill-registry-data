---
name: spawn-agent
description: >-
  Spin off a fresh Claude Code agent in a new iTerm2 split pane to work a task in parallel,
  after silently tightening the request into a clear, self-contained prompt. Use whenever the
  user wants to hand a sub-task to a parallel/side agent — "spin off an agent", "spawn a new
  claude", "kick off an agent to do X", "open another claude in a split", "have a second agent
  handle Y while I…", or delegating work to a separate session — even if they don't say
  "iTerm2". Requires iTerm2 on macOS. Do NOT use for in-process subagents (the Agent tool) or
  for cloning the current session (that's the `branch` skill); this opens a brand-new,
  independent agent seeded with one improved prompt.
---

# Spawn Agent

Hand a task to a brand-new Claude Code agent running in its own iTerm2 split, so it works in
parallel while you keep your current session. Before launching, the task is **silently** refined
into a tight, self-contained prompt — because the new agent starts with **zero** context from
this conversation, so whatever it's handed has to stand entirely on its own.

## Requirements
- macOS + **iTerm2** (the current session must be running inside iTerm2).
- First run triggers a macOS **Automation permission** prompt (iTerm2 controlling iTerm2) — approve it.
- `claude` on PATH.

## Steps

1. **Capture the task.** Take the user's initial ask (the skill argument, or the task they just
   described) as the raw prompt.

2. **Silently refine it (light prompt-engineering).** Do this in one pass — **no questions to
   the user, no printed analysis.** Rewrite the raw ask into a prompt a *context-less* fresh
   agent can act on. Apply this light checklist:
   - **State the goal** explicitly and unambiguously — one clear task.
   - **Inject the missing context** the new agent cannot see: the working directory, the
     relevant file paths, any decisions already made in this session that bear on the task, and
     where to look. *This is the most important move* — the new agent has none of our history,
     so an instruction like "continue the refactor" is useless without the specifics.
   - **Name the constraints** and what *not* to do.
   - **Specify the deliverable** and a done-criterion.
   - **Cut vagueness;** keep it self-contained and tight — "light" means a focused prompt, not
     an essay. Infer reasonable defaults instead of asking.

   For a genuinely gnarly prompt you can consult `prompt-engineering:improve-prompt` for a
   deeper pass, but keep it silent and quick by default — the point is a fast, unobtrusive
   tightening, not a full interactive analysis.

3. **Write the improved prompt to a temp file** using the Write tool (it handles multi-line and
   special characters cleanly — never try to pass the prompt as a shell argument). For example
   write it to `/tmp/spawn-agent-prompt.md`.

4. **Launch the split** by running this skill's bundled script with the temp file path:
   ```bash
   bash scripts/spawn_in_split.sh /tmp/spawn-agent-prompt.md vertical
   ```
   Direction is `vertical` (side-by-side — the default) or `horizontal` (stacked).

5. **Confirm briefly** — one or two lines noting the agent was spawned, and show the improved
   prompt it received so the user knows exactly what was dispatched and can steer the new pane.

## Notes
- The new pane is a **fresh, independent** `claude` session seeded with the improved prompt — it
  is *not* a clone and does **not** share this conversation's history (that's why step 2 injects
  context).
- It inherits the **current working directory**, so it operates on the same project.
- Run while iTerm2 is the active application so the split lands in the intended window.
- The script passes the prompt to the new session via a file, never as a shell/AppleScript
  argument, so prompt content with quotes, `$`, backticks, or newlines is safe.
- The new agent launches through your **interactive shell wrapper** — a `claude` fish
  function/alias if present — so your usual flags (`--append-system-prompt-file`,
  skip-permissions, etc.) and user-scoped MCP all apply, not a bare `claude` binary. Falls back
  to a plain `claude` if no wrapper is found.
- Splitting uses AppleScript (no iTerm2 Python API needed). On iTerm2 3.7 betas, use
  fully-qualified inline session refs — a captured `current tab` variable throws "Can't get tab 1".
