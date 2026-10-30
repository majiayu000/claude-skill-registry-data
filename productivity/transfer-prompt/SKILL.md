---
name: transfer-prompt
description: >-
  Draft a self-contained, paste-ready prompt for handing work off to another Claude Code session. Use when the
  user wants to brief a parallel session, transfer a task to a fresh session, codify a multi-step workflow as
  a reusable prompt, or coordinate work across multiple sessions or machines. Trigger phrases include "draft
  a handoff prompt", "prepare a transfer prompt", "write a paste-block for another session", "I need to brief
  another session", "prompt for another session".
license: Apache-2.0
metadata:
  author: Marc Taccolini
  version: 1.1.0
---

# Transfer Prompt

Draft a prompt another Claude Code session can pick up cold, with zero context from this conversation.
The receiving session orients itself in its repository on its own, so the prompt supplies the task, not
the environment.

## Required structure (in order)

1. **Model and effort, first line, both stated:** `Run this at model: <tier>, effort: <level>.` The
   receiving session cannot choose these well because it has not seen the work. Model follows blast radius,
   effort follows inference depth, and the two are set separately. The card is
   [`MODEL-AND-EFFORT.md`](../../MODEL-AND-EFFORT.md).
2. **Target tree, absolute.** The repository or worktree the session runs in, as a full path, plus the
   machine when there is more than one. A tree named only in the prompt's title or filename is lost the
   first time someone renames the file.
3. **Locked goal.** One declarative sentence: "I need you to do X." Not a question, not a menu.
4. **Context.** Recent decisions, related artifacts, and the why. Point at the changelog and decision
   records instead of re-narrating them.
5. **State, each line with its check.** Every claim about current state carries the command or query that
   established it and when it ran: `PR 412 is merged (gh pr view 412, 2026-10-20 14:05 UTC)`. The receiving
   session re-runs any check older than a day before building on it. A state line with no check is marked
   unverified and re-derived before use.
6. **Pre-reads.** Numbered file paths the session must read first, each with a one-line purpose.
7. **Numbered work items.** In order, each self-contained.
8. **Scope.** How deep to go and what not to expand into.
9. **"Do NOT" holds.** What the session might assume is in scope and is not.
10. **Report-back spec.** What the session returns when done, in what shape, and where it writes it.

## Voice

- Direct. No throat-clearing, no "I think", no menus.
- Self-contained. Assume the receiver has no memory of this conversation.
- Paths absolute or repository-rooted, never "the spec file".
- Tell, do not ask. The receiver is being briefed, not consulted.

## Process

1. Hear what the other session should do.
2. Find what it needs: files, prior decisions, conventions, target paths, and the current state with the
   check behind each line.
3. Set model and effort separately, and state both.
4. Draft the ten elements. Show the draft as one fenced code block, paste-ready.
5. Tighten on pushback.

## Anti-patterns

- **No model line, no effort line.** The commonest defect, and invisible, because the prompt still works at
  whatever the receiving seat defaults to.
- **No target tree.** The session starts in the wrong repository and does the work there.
- **State without a check.** "The deploy ran" from memory. The receiver builds on it and it was false.
- **Vague goal**, such as "help with the project".
- **No "do NOT" holds.** Scope leaks and you find out at the end.
- **Restating environment knowledge** (tool schemas, API references) the receiver fetches for itself.
