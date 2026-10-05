---
name: flow-audit
description: Enable, record, query, summarize, or verify the opt-in PWDEV Flow semantic audit trail. Use when the user asks what Flow actions occurred, wants audit integrity checked, or needs a portable JSONL record of workflow gates and artifacts.
---

# Operate the PWDEV Flow Audit Trail

Read [audit](../../references/audit.md), [safety](../../references/safety.md), and [artifacts](../../references/artifacts.md). Resolve [flow_audit.py](../../scripts/flow_audit.py) from this installed plugin and pass its absolute path to `python3` with the active repository root.

## Route

- `enable` updates only `.planning/flow/config.json` after an explicit request and preserves unknown configuration fields.
- `summary` reports counts by action, skill, and phase.
- `events` returns the latest valid semantic events, optionally filtered by an allowed action.
- `verify` checks every non-empty JSONL line and returns integrity errors without repairing them.
- `record` appends one event only after the described semantic action actually occurred.

Use the helper rather than parsing or appending JSONL with ad hoc shell commands.

## Procedure

1. Confirm the repository root and inspect `.planning/flow/config.json` without reading secrets.
2. For `enable`, require explicit intent, set `audit` to `true`, preserve unknown fields, and run `verify`. Do not create a synthetic historical trail.
3. For queries, run the matching helper command and report invalid-trail failures before any counts.
4. For `record`, choose one allowed action from the audit contract, a canonical `flow-*` skill, and only the smallest non-sensitive structured detail needed. Record after the gate, write, decision, archive, migration, or phase outcome succeeds.
5. Report helper exit status and whether a write occurred. Recording while disabled is a successful no-op, not an audit event.

## Constraints

- Never include prompts, environment variables, file contents, secrets, credentials, tokens, or private-key paths.
- Do not promise complete runtime telemetry: this trail records semantic Flow events only and uses no hooks.
- Do not repair, truncate, reorder, or replace an invalid trail without a separate explicit instruction.
- Audit failure must be visible but does not retroactively invalidate the workflow event it attempted to record.

## Output

Return `MODE`, `AUDIT_ENABLED`, command result, integrity status, event count when applicable, limitations, and `NEXT`.
