---
name: gz-adr-sync
description: Use to reconcile an ADR end to end by discovering @covers evidence, reconciling OBPI ledger state and registering files.
category: adr-operations
compatibility: GovZero v6 framework
metadata:
  skill-version: "7.1.3"
  govzero-framework-version: "v6"
  govzero-author: "GovZero governance team"
gz_command: register-adrs
invocation: uv run gz register-adrs
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
model: haiku
---

# gz-adr-sync

End-to-end ADR governance sync. Absorbs `gz-adr-autolink` (Layer 1), `gz-adr-recon` (Layer 2), and the original `gz-adr-sync` (Layer 3) into a single operator-facing skill. Run after multi-session work, after importing pool ADRs, or before requesting ADR closeout.

## Modes

### Full sync (no ADR-ID)

Runs all three layers in trust order.

```bash
# Layer 1 — repo-wide @covers coverage (REQ/OBPI/ADR granularity)
uv run gz covers

# Layer 2 — global ledger reconciliation
uv run gz status --json

# Layer 3 — register and refresh
uv run gz register-adrs --dry-run
uv run gz register-adrs
uv run gz status
```

### Scoped (with ADR-ID)

Reconciles a single ADR and its OBPIs. Use when verifying evidence gaps or preparing a specific ADR for closeout.

```bash
# Layer 1 — discover @covers annotations for target ADR
uv run gz adr covers-check ADR-<X.Y.Z>

# Layer 2 — ledger reconciliation for target
uv run gz adr status ADR-<X.Y.Z> --json
uv run gz adr audit-check ADR-<X.Y.Z> --json

# After any doc updates, re-lint
uv run gz lint
```

## Notes

- `gz-adr-recon` and `gz-adr-autolink` are archived; this skill is their successor.
- The runbook prescribes full sync before closeout; scoped mode is for targeted investigation.
- Apply markdown table updates manually after evidence discovery, then run `uv run gz lint`.

## Archived predecessors

| Archived skill | Absorbed as |
|---|---|
| `gz-adr-autolink` | Layer 1 phase (evidence gathering) |
| `gz-adr-recon` | Layer 2 phase (ledger reconciliation) |
| `gz-register-adrs` | Layer 3 phase (registration) |

## References

- Command implementation: `src/gzkit/cli/`
- User docs: `docs/user/manpages/register-adrs.md`, `docs/user/manpages/adr-status.md`, `docs/user/manpages/adr-audit-check.md`
