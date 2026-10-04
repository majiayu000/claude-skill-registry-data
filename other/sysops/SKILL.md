---
name: sysops
description: Invoke the sysops subagent for VPS maintenance. Use when the user runs /sysops with an optional argument like "status", "update Pulse", or "update my servers".
---

# Sysops

If the first word of the argument is `log` or `learnings`, handle it directly — do NOT delegate to the sysops subagent.

## /sysops log

Parse the argument:
- `/sysops log` → show last 10 entries across all deployments
- `/sysops log <Deployment>` → show last 10 entries for that deployment (case-insensitive match)
- `/sysops log <Deployment> --last <N>` → show last N entries for that deployment

Run this command, substituting `<deployment>` (omit `--deployment` entirely if no deployment was given) and `<N>` (default `10`):

```bash
trimkit-sysops-log-search --human [--deployment "<deployment>"] [--last <N>]
```

If `trimkit-sysops-log-search` is not on PATH, tell the user:
> `trimkit-sysops-log-search` is not installed. Run `install.sh` from your trimkit directory to set it up.

If `trimkit-sysops-log-search` is found but exits non-zero, show the user the error output and suggest checking file permissions on `~/.claude/sysops/audit.jsonl`.

---

## /sysops learnings

Parse the argument:
- `/sysops learnings` → show all stored learnings across all deployments (deduplicated)
- `/sysops learnings <Deployment>` → show learnings for that deployment only (case-insensitive match)

Run this command, substituting `<deployment>` (omit `--deployment` entirely if no deployment was given):

```bash
trimkit-learnings-search --human [--deployment "<deployment>"]
```

If `trimkit-learnings-search` is not on PATH, tell the user:
> `trimkit-learnings-search` is not installed. Run `install.sh` from your trimkit directory to set it up.

If `trimkit-learnings-search` is found but exits non-zero, show the user the error output and suggest checking file permissions on `~/.claude/sysops/learnings.jsonl`.

---

Otherwise, delegate to the `sysops` subagent using the Agent tool.

Pass the user's argument directly as the prompt. If no argument was given, default to a status check across all deployments.

Examples:
- `/sysops` → prompt: "Check the status of all my servers"
- `/sysops status` → prompt: "Check the status of all my servers"
- `/sysops update Pulse` → prompt: "Update Pulse"
- `/sysops update my servers` → prompt: "Update all my servers"

Do not add any preamble or explanation — just invoke the subagent immediately.
