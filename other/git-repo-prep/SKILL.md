---
name: git-repo-prep
description: Routes between prepare (full lifecycle) and review (standalone audit) for open-source release workflows. Use when making a repo public, open-sourcing a project, auditing for secrets or missing documentation, preparing for public release, or reviewing a repo for openness.
---

# Git Repo Prep

## Overview

Prepares codebases for public release and reviews them for openness.

**Two sub-skills:**
- **prepare** — Full lifecycle: audit, clean, document, harden, ship
- **review** — Standalone audit, re-runnable anytime, conversational

## Routing

**Prepare signals:** "prepare", "open source", "make public", "get ready for release", first-time release
**Review signals:** "review", "audit", "check", "what's missing", "gaps", already partially prepared

- Preparing for first-time release → `git-repo-prep:prepare`
- Reviewing/auditing existing repo → `git-repo-prep:review`
- Ambiguous → AskUserQuestion: "Full preparation" vs "Review/audit"

Invoke via Skill tool, then hand off. Router's job is done.
