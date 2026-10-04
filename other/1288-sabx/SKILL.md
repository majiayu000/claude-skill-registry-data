---
name: sabx
version: 0.1.11
description: Manage SABnzbd queues, history, NZBs, priorities, limits, RSS feeds, schedules, and server state through sabx.
metadata:
  short-description: SABnzbd CLI for download automation
  compatibility: claude-code, codex-cli
---

# SABnzbd CLI

Use `sabx` for SABnzbd reads and changes. Start with the requested operation;
check installation, authentication, or connection settings only when a command
fails for that reason. Search [references/commands.md](references/commands.md)
for exact flags and less common commands.

## Common reads

```bash
sabx status
sabx queue list
sabx history list
sabx server list
sabx rss list
sabx schedule list
```

Prefer `--json` when another tool will consume the result. Use `--profile NAME`
only when the user selects a non-active profile.

## Changes

Resolve the queue item, history item, category, server, feed, or schedule entry
before changing it. Commands that add an NZB, reorder or delete items, clear
history, pause or resume processing, change limits, edit feeds/schedules, or
enable/disable servers change SABnzbd state.

- Follow the user's authorization for the concrete change.
- Do not interpret "clean up" as permission to delete queue items or all
  history; ask what should be removed if the target is not explicit.
- After an ambiguous timeout, read back queue/history/server state before
  retrying a mutation.
- Never expose the SABnzbd API key in output, logs, commands, or messages.

Typical operations:

```bash
sabx queue add url URL
sabx queue item pause NZO_ID
sabx queue item resume NZO_ID
sabx queue item priority NZO_ID 2
sabx speed limit --rate 10M
```

Use the command reference before deletion, RSS, scheduler, server, or
configuration changes.

## Connection diagnosis

If a command reports no configuration, authenticate with the supported config
flow. If it reports connection refused, verify the selected profile URL and
that SABnzbd is running. If it reports authentication failure, replace the key
through the secure config command; do not print the current key. Do not disable
TLS verification unless the user explicitly chooses that risk.

For repository development and release checks, use `CLAUDE.md`.
