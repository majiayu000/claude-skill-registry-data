---
name: docs-only-convo
description: Mark the current thread as only intended for updating documentation. Invoke only when explicitly called by user.
user-invocable: true
disable-model-invocation: false
---
# Docs Only Convo

## Context for This Conversation

This conversation is for reviewing, defining, or updating technical specifications, requirements, feature files, or other documentation only.
No code changes are to be made unless explicitly directed.

Treat a code change that seems necessary as a finding to report, not as work to perform.
Say what would need to change and why, then wait for direction.

## Discover the Repository's Rules First

Find and follow the repository's own instructions rather than assuming a layout.
Read whichever of these exist, and prefer what they say over the defaults below:

- Agent instruction files at the repository root or in a tool directory, such as `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, or rule files under `.cursor/`.
- A project meta or overview document, such as `meta.md` or `README.md`.
- Documentation standards, usually indexed from a docs directory.
- Contribution guidance, such as `CONTRIBUTING.md`.

Report which of these were found and which were absent, so it is clear what the session is operating under.

## Working Rules

- `touch` new files before editing them.
- Write reports and working notes to the repository's own development-docs location, discovered rather than assumed; common locations are `docs/dev_docs/` or `dev_docs/`.
  Ask where they belong when the repository has no such location.
- Write temporary files to the repository's scratch location, commonly a root `tmp/` directory, and only when it is ignored by version control.
  Ask rather than creating a new directory at the repository root.
- Discover the available task-runner recipes before running anything, for example with `just --list` or `make help`.
- Use task-runner recipes instead of calling the underlying scripts directly when a suitable recipe exists.
- Do NOT modify task-runner files such as `justfile` or `Makefile` unless explicitly told to do so.
- Do NOT modify or adjust linter rules, exceptions, or thresholds unless explicitly told to do so.
- Use appropriate skills whenever possible, including the repository's own documentation and specification authoring skills.

## Follow-On Instructions

- Confirm your understanding, state what repository rules were found, and await further instructions.
