---
name: mail
description: Send emails via macOS Mail app. Use when the user asks to send an email.
---

# Mail Skill Guide

```bash
scripts/imail.sh "<recipient>" "<subject>" "<body>"
```

Constraint: Use `AskUserQuestion` to confirm with the user before sending.

Note: Requires Accessibility permissions for Terminal.
