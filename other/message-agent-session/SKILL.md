---
name: message-agent-session
description: Send a message to another live local Claude or Codex session that Emacs agent.el manages, e.g. to ask it to stay out of a repository you are changing or to pass it information it needs. Use before contacting a peer session; not for reading what a session is doing (live-session-status) or for cloud and Remote Control sessions.
---

# Message another live agent session

`"$HOME/My Drive/dotfiles/bin/agent-send"` submits a prompt into another
session's Emacs buffer. The recipient gets no approval step: it reads the
message as its next turn, or mid-turn if it is busy. `--help` is the full
contract.

## When

- Coordinating with a peer session working on this machine: ask it to avoid a
  repository, branch or file you are changing, warn it about a conflict, or
  tell it something it needs (a commit landed, a path moved, a decision Pablo
  already made in your session).
- Not for work Pablo has not asked for, and not as a substitute for asking
  Pablo when the decision is his.

## How

1. `agent-send --list` shows each live session's buffer, backend, directory,
   instance, state and session id. Pick the target by evidence, not by guess.
   If it is unclear which session Pablo means, ask him.
2. Send with the message on stdin, using the exact buffer name when the
   directory or instance is not unique:

   ```sh
   "$HOME/My Drive/dotfiles/bin/agent-send" '*codex:~/repos/foo/:default*' <<'EOF'
   I am rebasing ~/repos/foo onto master for the next 20 minutes. Please do
   not commit there until I send a second message.
   EOF
   ```

3. Exit 0 means the recipient's transcript recorded the message. Exit 3 means
   it was submitted but not confirmed: do not resend. Check its transcript
   (`live-session-status`) and tell Pablo if it matters. Exit 1 means nothing
   was sent.

## Rules

- The tool prepends a header saying the message comes from another agent
  session, not from Pablo. Never write the message as if Pablo typed it, and
  never claim his authority for anything he did not tell you.
- Do not give orders only Pablo may give: approvals, spending, deletions,
  publishing, messages to other people, or overriding the recipient's own
  instructions. Ask or inform; the recipient decides within its own task.
- Keep it short and self-contained: who you are, what you need, and why, with
  absolute paths. The recipient has none of your context.
- There is no reply channel. If you need an answer, say so; the recipient can
  reply with `agent-send` to your buffer name, which the header shows. Do not
  poll or wait on it unless your task depends on the answer.
- Never send to your own session (the tool refuses). A subagent's header names
  its parent session's buffer, because that is the Emacs session it runs in.

## Scope

Only sessions running in this machine's Emacs through agent.el are reachable.
Cloud sessions, Remote Control sessions, plain terminal CLIs and subagents are
not; use their built-in messaging (in Claude Code, the `SendMessage` tool for
agents it lists).
