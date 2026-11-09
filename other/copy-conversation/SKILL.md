---
name: copy-conversation
description: "Copy this session's conversation to the clipboard: render the Claude or Codex transcript unwrapped, trim it as tth does, and put it under a line holding the tab title and a colon, then an empty line. Optional YYYYMMDD date and --title."
user-invocable: true
argument-hint: "[YYYYMMDD] [--title \"<text>\"]"
allowed-tools:
  - Bash("${CLAUDE_SKILL_DIR}/copy_conversation.bat" *)
  - Bash(${CLAUDE_SKILL_DIR}/copy_conversation.bat *)
---

Result: !`"${CLAUDE_SKILL_DIR}/copy_conversation.bat" $ARGUMENTS`

The copy already ran while this skill loaded. Reply with the result line above,
unchanged, then stop: run no command and read no file. If no result line is
shown, read and follow [the canonical instruction](../../../instructions/copy-conversation.md).
