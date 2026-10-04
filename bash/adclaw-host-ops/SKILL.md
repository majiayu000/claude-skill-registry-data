---
name: adclaw-host-ops
description: "Use when the user asks to inspect AdClaw Host operators, customers, containers, sandbox statuses, stuck runtime alerts, backups, runtime reconcile, or safe admin actions."
---

# AdClaw Host Ops

Use the deterministic CLI first:

```bash
adclaw-host-ops summary
adclaw-host-ops alerts
adclaw-host-ops user <user_id>
adclaw-host-ops reconcile --dry-run
```

Mutating actions require explicit confirmation:

```bash
adclaw-host-ops reconcile --confirm
adclaw-host-ops sleep <user_id> --confirm
```

## Credential Boundary

The CLI loads:

```text
/root/.env
/root/adclaw/CF/worker-adclaw/.env.operator
```

It must never print secret values. It prints only presence/missing diagnostics
for required variables.

Canonical local operator env:

```text
/root/adclaw/CF/worker-adclaw/.env.operator
```

This may be a symlink to a legacy file. Do not depend on old `.env.phase4-*`
filenames in new workflows.

## Safety

- `summary`, `alerts`, `user`, and `reconcile --dry-run` are read-only.
- Do not use preview/runtime URLs as health checks.
- Do not start or wake sandboxes for monitoring.
- If a `stuck_runtime` alert already has `reconcile_idle_timeout ok=true` and
  current user status is `sleeping`, classify it as self-healed.
- If `runtime_mode=keep_warm`, do not recommend sleep unless entitlement/add-on
  state is invalid.
- Confirmed `/api/admin/reconcile` is global within the requested limit, not
  per-user. Verify every dry-run candidate before confirming.

## Project Docs

If more detail is needed, read:

```text
/root/adclaw/CF/docs/admin/operator-access-inventory.md
/root/adclaw/CF/docs/admin/runtime-alert-response.md
/root/adclaw/CF/OPERATIONS-RUNBOOK.md
```
