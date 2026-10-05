---
name: source-reviewer
description: Reviews public source notes and produces a bounded summary.
---

# Source Reviewer

This is a descriptor-only generated adapter. It does not install or execute resources.

Boundary:
- descriptor-only
- do not install or execute
- no lifecycle hooks are trusted
- no user agent configuration is written
- target: codex-skill

## Command: summarize-public-source
Profile: review
Mode: summarize
Aliases: summarize

Summarizes public source notes with no execution.

Read the provided public notes and produce a concise summary with open questions.
