---
name: review
description: Architecture-aware review of the task's changes or a given scope, with severity-ranked verdict. Manual command.
argument-hint: "[scope; default: changes since state base]"
disable-model-invocation: true
---
Delegate to reviewer (Copilot `reviewer`, Claude Code `claude-reviewer`) with a pointer prompt: scope = text after the command, or `git diff <state.base>` if empty. Relay the reviewer OUT block unchanged; add nothing.
