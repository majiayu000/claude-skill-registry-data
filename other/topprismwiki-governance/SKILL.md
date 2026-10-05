---
name: topprismwiki-governance
description: Manage explicit source approval, exclusion, readmission, retry, and batch validation for Topprismwiki. Internal child module of $topprismwiki.
---

# Governance

Source approval and readmission require an explicit user instruction. Keep all
governance records in Workspace. Apply exclusion precedence as:

1. explicit readmission;
2. permanent SHA-256 denial;
3. scoped path or version-family rule;
4. approved source registry.

Missing originals preserve historical formal knowledge and are marked
`source_unavailable`; they are not silently deleted. Use `retry` only for a
specific failed or isolated unit and `validate` for read-only audit.

## Execution contract

`source approve`, `source exclude` and `source readmit` are governance writes to
the private registry and require an explicit user instruction plus a non-sensitive
reason for exclusion or readmission. `retry` marks a recorded batch or retryable
unit as queued; it does not re-run an adapter or write the formal Vault.

Use the following read-only checks before a governance action:

```bash
python3 scripts/topprismwiki.py source list --project /path/to/wiki
python3 scripts/topprismwiki.py batch show <batch-id> --project /path/to/wiki
python3 scripts/topprismwiki.py diagnose --batch-id <batch-id> --project /path/to/wiki
```

The public Runner records governance events but does not claim full production
precedence enforcement for private deny lists, version families or readmission
authorization. Keep the event ledger and source hashes for audit. See
[capability-matrix.md](../../references/capability-matrix.md) and
[troubleshooting](../../../../docs/zh-CN/troubleshooting.md).
