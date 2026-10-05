---
name: topprismwiki-status
description: Inspect watermarks, batches, document families, isolates, candidates, and formal-store health. Internal child module of $topprismwiki.
---

# Status and batch dashboard

Use the status ledger and generated projections. Distinguish `accepted`,
`no_change`, `quarantined`, `blocked`, `partial`, and `rolled_back`. A failed
or quarantined unit does not advance its watermark.

```bash
python3 scripts/topprismwiki.py status --project /path/to/wiki
python3 scripts/topprismwiki.py batch list --project /path/to/wiki
python3 scripts/topprismwiki.py dashboard build --project /path/to/wiki
```

The HTML dashboard is a read-only local projection. It may expose only
configured aliases and relative paths.

## Execution contract

`status` reads the private batch ledger and reports batch counts and formal page
counts. `batch list` filters by source or state; `batch show` returns one stored
summary; `dashboard build` writes a self-contained HTML projection under
Workspace or the explicitly requested output path. The dashboard never executes
an action and must not contain raw evidence, credentials or absolute user paths.

The reference Runner stores batch-level state. Durable per-session watermarks,
source version families and attachment retry queues remain responsibilities of
the external production adapter until the corresponding capability is marked
`built-in`. A failed or quarantined unit must not be reported as a successful
formal update. For diagnosis, run `diagnose --batch-id <id>` before editing any
ledger. See [batch-schema.md](../../references/batch-schema.md) and
[troubleshooting](../../../../docs/zh-CN/troubleshooting.md).
