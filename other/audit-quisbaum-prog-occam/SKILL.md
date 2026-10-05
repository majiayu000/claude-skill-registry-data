---
name: audit
description: Show where this machine's Claude Code tokens went - cost by token type, context tax per tool, biggest tool outputs.
argument-hint: "[days, default 7]"
disable-model-invocation: true
---
Run `python3 ../../tools/audit.py --days <days>` from this skill's base directory (days = the argument, default 7). Show its output unchanged in a code block, then add at most three one-line observations about the biggest levers. Nothing else.
