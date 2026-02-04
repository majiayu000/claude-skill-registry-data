---
name: harness
description: Automated quality check loops with escalation and fix sub-agents
---

# Harness

Automated fix loops. Each harness runs a make target, spawns sub-agents to fix failures, commits on success, reverts on exhaustion.

**Pattern:** `.claude/harness/<name>/run` + `fix.prompt.md`

**Escalation:** sonnet:think → opus:think → opus:ultrathink

**CLI:** `.claude/scripts/check-<name>` symlinks to harness run scripts

**Commands:** `/check-<name>` runs the corresponding harness with `--no-spinner`

**Quality:** `quality/run` orchestrates all harnesses in sequence until stable
