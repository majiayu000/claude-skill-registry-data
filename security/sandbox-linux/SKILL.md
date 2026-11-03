---
name: sandbox-linux
description: "Use when asked about agent confinement on Linux. In icloneOS v0.0.3 it is not available: the same five activity classes are planned on bubblewrap and Landlock, so on Linux commands run as the user with the permission mode as the only gate, and this skill says what to tell the owner."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
metadata:
  hermes:
    tags: [iclone-os, sandbox, confinement, linux, security]
    related_skills: [sandbox-macos, sandbox-windows, consent, docker-for-agents]
---

# Confinement on Linux — not in v0.0.3

## When to use
- The owner asks whether the agent's commands are confined on a Linux machine or server.

## What is true today
- icloneOS v0.0.3 confines the agent's terminal on **macOS only** (Seatbelt, see `sandbox-macos`). On Linux the
  terminal runs as the user; the **permission mode** (Manual, Automatic, Plan, Accept edits, Ignore permissions) is the
  gate, and the Containers window reads "not on this Mac".
- Planned for a later release, behind the same interface: bubblewrap (`bwrap`) for mount namespaces and Landlock for
  file-system rules, mapping the same five classes (research, project, build, offline, media).

## What to do
- Say plainly that commands are not confined on Linux in this version. Never claim otherwise.
- For isolation today on a server, a container is the honest answer (`docker-for-agents`): pinned image, non-root
  user, read-only root, only the project mounted.
- Keep the owner's secrets out of reach by never reading `~/.ssh`, `~/.aws`, `~/.config/gh` or `.env` files without a
  consent-door yes, exactly as the macOS profiles enforce.
