---
name: copying-to-clipboard
description: Copies requested text to the laptop clipboard over ssh via tmux OSC 52. Use for "copy that to my clipboard".
allowed-tools: Bash(~/.claude/skills/copying-to-clipboard/scripts/clip.sh *)
---

# Copying to clipboard

Pipe the exact text the user asked for through a quoted heredoc, so `$`,
backticks, and quotes arrive literally (BigQuery table names use backticks):

```bash
~/.claude/skills/copying-to-clipboard/scripts/clip.sh <<'EOF'
<the text, verbatim>
EOF
```

- "That" means the most recent code block or text you produced, copied as-is.
  Don't fill in placeholders unless asked.
- The script reports the char count and first line. It cannot see the laptop's
  clipboard, so tell the user to paste to confirm, and name any placeholders
  they still need to replace.
