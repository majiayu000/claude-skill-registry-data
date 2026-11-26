---
name: send-to-claude-fable
description: "Send a bounded task or review packet to the local Claude Code CLI on the Fable model and bring back its verdict. Use when you want an independent second opinion from a different model."
---

# Märlitante (send-to-claude-fable)

Use this skill when the user explicitly asks to send, delegate, or obtain a review from Claude Fable through the local `claude` CLI.

## Dispatch

1. Verify the local interface with `command -v claude`, `claude --version`, and only the relevant help when its flags are uncertain.
2. Build a self-contained prompt containing:
   - the concrete task and expected verdict or deliverable;
   - exact source, artifact, or conversation bindings needed to work independently;
   - the user's current authorization and prohibitions;
   - a request to label measured evidence separately from inference.
3. Redact secrets, credentials, personal data, provider identifiers, and unrelated private context.
4. Invoke Fable non-interactively and wait for its answer:

   ```bash
   claude -p \
     --model fable \
     --effort high \
     --permission-mode dontAsk \
     --allowedTools 'Read,Grep,Glob' \
     --disallowedTools 'Write,Edit,NotebookEdit,Bash' \
     --no-session-persistence \
     --output-format text \
     "<bounded prompt>"
   ```

   These are safe defaults for review and discovery work. `dontAsk` is intentional: Claude's `plan` mode may create a file under `~/.claude/plans`, even when the task is otherwise read-only. Adjust tools or permission mode only when the user explicitly authorizes the corresponding mutations. Never use `--dangerously-skip-permissions` merely to avoid a permission boundary.
5. If the command yields a running session, poll it normally and do not signal or kill it unless the user explicitly asks.
6. Return Fable's actual verdict, clearly attributed to Claude Fable. Keep Codex's own assessment separate, and report CLI/authentication failure rather than fabricating a handoff.

## Boundaries

- Sending a task does not expand its authority. Carry forward all no-edit, no-provider, no-spend, no-submit, and other active restrictions.
- Do not use `--continue` or `--resume` unless the user asks to enter an existing Claude conversation.
- Prefer `--no-session-persistence` for one-shot reviews. Use background agents only when the user explicitly asks for a persistent or background Claude task.
- A successful CLI launch is not a successful review. Wait for and report the terminal response.
