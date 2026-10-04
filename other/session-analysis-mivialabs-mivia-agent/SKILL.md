---
name: session-analysis
description: Read-only metadata-only analysis of chat sessions in the durable SQLite chat ledger, mirroring the harness's own catalog path. Validated process-quality findings; default window last 24h.
triggers:
  - analyze sessions
  - session analysis
  - chat session report
  - process quality report
  - analyze the chat ledger
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - run_command
argument-hint: "Time frame (optional): 24h|7d|ISO range; default last 24h"
short-description: Read-only analysis of chat sessions in the ledger
user-invocable: true
---

This skill is defined in `.agents/skills/session-analysis/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
