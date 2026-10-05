---
name: copilot-web-fetch
description: Fetch and read the full contents of a specific web page (URL) as clean Markdown using Copilot Plus. Use when the user shares a link or asks you to open, read, or summarize a particular page — not for an open-ended web search. Requires an active Copilot Plus license; without it, use your own fetch tool instead.
license: Copilot Plus
metadata:
  copilot-enabled-agents: opencode, claude, codex
  copilot-builtin-version: "6"
---

# Copilot web fetch

Fetch a web page's contents as Markdown through Copilot Plus.

## How to run

Find the absolute path to this SKILL.md file on disk, then run the script next
to it that matches the operating system. No extra runtime is needed — `sh`
(macOS/Linux) and `cmd`/PowerShell (Windows) are always present.

On macOS or Linux:

```bash
sh "/absolute/path/to/this/skill/directory/web-fetch.sh" "<url-to-fetch>"
```

On Windows, run the `.cmd` wrapper. In PowerShell you must prefix it with the
call operator `&` (PowerShell treats a quoted path on its own as a string and
won't run it); from cmd, run the quoted path without the `&`:

```powershell
& "/absolute/path/to/this/skill/directory/web-fetch.cmd" "<url-to-fetch>"
```

Both print the result to stdout.

## If Copilot Plus is not active

If the script exits saying Copilot Plus is unavailable, do NOT retry it. Do what
the message says: fall back to your own equivalent built-in capability to handle
the request when you have one (otherwise tell the user it's unavailable) — never
refuse or block the user. Only mention upgrading or renewing Copilot Plus when
the script's message explicitly invites it, and keep any such note short and
friendly.

## Self-Host mode

Self-Host search providers do not provide a common full-page fetch contract. If
the script reports that Self-Host mode is active, never use an agent-native web
fetch tool. Use `copilot-web-search` when search results can answer the request;
otherwise tell the user that fetching the page is unavailable.

