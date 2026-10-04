---
name: multi-agent-review-gate
description: Run a structured review gate before merging multi-agent outputs. Use when multiple agents have produced work packets that need quality checks, conflict detection, and approval before integration.
---

# Multi Agent Review Gate

## Overview

Enforces a quality and consistency gate after parallel agents complete their work packets, ensuring outputs are compatible, correct, and safe to merge.

## Review Checklist

1. **Completeness** — Every work packet meets its `done_criteria`.
2. **Conflict scan** — No two packets modified the same file in incompatible ways.
3. **Interface check** — Cross-packet APIs, types, and contracts are consistent.
4. **Test validation** — All packet-level and integration tests pass.
5. **Style & standards** — Code follows project conventions (linting, formatting, naming).
6. **Security scan** — No new secrets, injection vectors, or unsafe patterns introduced.

## Gate Decisions

| Decision | Meaning |
|----------|---------|
| **APPROVE** | All checks pass — safe to integrate |
| **REQUEST_CHANGES** | Issues found — return to packet owner with specific feedback |
| **BLOCK** | Critical conflict or failure — escalate before proceeding |

## Conflict Resolution

- If two packets touch the same file, diff both changes and determine if they're additive or conflicting.
- Additive changes can be merged in dependency order.
- Conflicting changes require one packet owner to rebase on the other's output.

## When to Use

- After a multi-agent-orchestrator run completes all packets
- Before committing or pushing multi-agent work
- When integrating outputs from agents that worked in parallel on related code
