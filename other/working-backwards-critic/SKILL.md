---
name: working-backwards-critic
description: Stub for an independent Working Backwards critic in Cursor. Products own the lock and hook. Use when reviewing a press release, FAQ, or requirements package.
title: "Working Backwards Critic"
kind: "platform-adapter"
domain: "platforms"
status: "draft"
owner: "APT"
last_updated: "2026-09-06"
source_paths: ["apt-principles-agents/platforms/cursor/source/skills/working-backwards-critic/SKILL.md"]
---

# Working Backwards Critic

This is an adapter stub. Product repos may replace it with a local skill and hook. Do not overwrite a drifted product copy on sync.

Canonical sources (do not fork into `apps/`):

- `templates/working-backwards/critic-rubric.json`
- `templates/working-backwards/agent-role-contracts.md`

## Rules

- Independence is a **new session**, not a different model. The drafting chat must not issue `PASS`.
- The critic writes only verdict files (`critic-review.md`, session state). It does not edit writer artifacts.
- Hooks may guard or remind. Hooks must never write `PASS`.
- Products keep their own lock-file and edit-guard hook. See `apt-commerce` `.cursor/skills/working-backwards-critic/` as a reference implementation.

## Procedure

1. Load the versioned rubric and include the version in the verdict.
2. Read the package in stage order.
3. Score required dimensions. Unwritten later stages stay `PENDING`.
4. Distinguish `[OPEN]` from `[BLOCKER]`.
5. Return verdict, failing dimensions, evidence, and suggested fixes. Do not revise the artifacts.
