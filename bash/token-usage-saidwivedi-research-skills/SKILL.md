---
name: token-usage
disable-model-invocation: false
user-invocable: true
description: >
  Show per-session token usage breakdown. Run /token-usage or /token-usage 30 to see usage over N days.
version: latest
category: utility
tags:
  - usage
  - tokens
  - tracking
---

# Token Usage Tracker

Run the token usage summary script and display results to the user.

```bash
python3 ~/.claude/skills/token-usage/show-usage.py $ARGUMENTS
```

If no argument is provided, default is 7 (last 7 days).

Show the full output table to the user exactly as printed.
