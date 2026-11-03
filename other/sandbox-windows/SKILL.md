---
name: sandbox-windows
description: "Use when asked about agent confinement on Windows. In icloneOS v0.0.3 it is not available: commands run as the user with the permission mode as the only gate; this skill says what is planned and what to tell the owner meanwhile."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
metadata:
  hermes:
    tags: [iclone-os, sandbox, confinement, windows, security]
    related_skills: [sandbox-macos, sandbox-linux, consent]
---

# Confinement on Windows — not in v0.0.3

## When to use
- The owner asks whether the agent's commands are confined on Windows.

## What is true today
- icloneOS v0.0.3 confines the agent's terminal on **macOS only** (see `sandbox-macos`). On Windows the terminal runs
  as the user and the **permission mode** is the gate; the Containers window reads "not on this Mac".
- A later release may map the same five classes (research, project, build, offline, media) onto AppContainer or a
  Windows Sandbox / WSL2 container behind the same interface. Nothing is promised yet.

## What to do
- Say plainly that commands are not confined on Windows in this version.
- Keep to the project folder, ask through the consent door before writing elsewhere, installing software or using the
  network, and never read credential stores (`%USERPROFILE%\.ssh`, the Windows Credential Manager, `.env` files).
