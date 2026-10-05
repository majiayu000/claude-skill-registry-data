---
name: copilot-fetch-x
description: Fetch the content of an X (Twitter) post using Copilot Plus. Use when the user shares an x.com or twitter.com URL and wants its text or context. Requires an active Copilot Plus license.
license: Copilot Plus
metadata:
  copilot-enabled-agents: opencode, claude, codex
  copilot-builtin-version: "6"
---

# Copilot fetch X

Fetch the content of an X (Twitter) post through Copilot Plus.

## How to run

Find the absolute path to this SKILL.md file on disk, then run the script next
to it that matches the operating system. No extra runtime is needed — `sh`
(macOS/Linux) and `cmd`/PowerShell (Windows) are always present.

On macOS or Linux:

```bash
sh "/absolute/path/to/this/skill/directory/fetch-x.sh" "<x-or-twitter-url>"
```

On Windows, run the `.cmd` wrapper. In PowerShell you must prefix it with the
call operator `&` (PowerShell treats a quoted path on its own as a string and
won't run it); from cmd, run the quoted path without the `&`:

```powershell
& "/absolute/path/to/this/skill/directory/fetch-x.cmd" "<x-or-twitter-url>"
```

Both print the result to stdout.

## If Copilot Plus is not active

If the script exits saying Copilot Plus is unavailable, do NOT retry it. Do what
the message says: fall back to your own equivalent built-in capability to handle
the request when you have one (otherwise tell the user it's unavailable) — never
refuse or block the user. Only mention upgrading or renewing Copilot Plus when
the script's message explicitly invites it, and keep any such note short and
friendly.

