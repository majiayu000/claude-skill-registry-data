---
name: kit-migrate
description: Install or upgrade the guardrails kit into a project with an existing CLAUDE.md by executing MIGRATE.md exactly. Use when asked to migrate a CLAUDE.md, install the kit, or retrofit guardrails into a project.
---

Read MIGRATE.md and execute it exactly, phase by phase, starting at Phase 0 (idempotency check).
- docs/guardrails/MIGRATION-PREP.log present? MIGRATE.md's script-prepped entry applies: spot-check the snapshot hash, start at M1, use `scripts/migrate.sh <KIT> apply` at M6a.
- Never paraphrase kit text — migration is transport, not authorship.
- Print every `Verify:` line's actual output; an unprinted verify counts as FAILED.
- STOP at the M5 user checkpoint and wait for explicit approval.
