---
name: wire-audit
description: Alias for /wiring-audit, the mandatory post-build integration gate. Use when user says /wire-audit, "wire audit", "check wiring", "what did we miss", or after any build completes.
---

# WIRE-AUDIT

This skill is an alias. Run `.claude/skills/wiring-audit/SKILL.md`.

Use `/wiring-audit` as the canonical skill name in specs, dispatch prompts, closeouts, and memories.

Required behavior is unchanged:

- Run `node scripts/wiring-audit.mjs`.
- Use `post_build_domain_matrix` to choose relevant domains.
- Run Page X-Ray on affected routes.
- Prove or fix Dinner Circles, Universal Rail, Priority Queue, Commitment UI, Menu Intelligence, PIE, Client Intelligence, communications, lifecycle, ledger, navigation, Remy, automation, and CIL wiring where relevant.
- Do not call a build done until high and medium relevance domains are wired, queued, or explicitly marked N/A.
