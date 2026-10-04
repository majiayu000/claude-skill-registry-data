---
name: bmc-dashboard-audit-runner
description: >
  Runs the full BMC Dashboard audit at depth. Ensures stack is up, executes
  run_audit.sh, probes all API endpoints, and writes report + handoff to
  .cursor/bmc-audit/ for the Debug Reviewer. Use when user asks for bmc audit
  a fondo, full dashboard audit, or run audit completo.
---

# BMC Dashboard Audit Runner Skill

**Before working:** Read `docs/team/knowledge/AuditDebug.md` if it exists.

Coordinates the Audit Runner Agent to execute a thorough BMC Dashboard audit.

## When to Use

| Trigger | Action |
|---------|--------|
| "run audit a fondo" | Execute full audit |
| "bmc audit completo" | Same |
| "full dashboard audit" | Same |
| Before Debug Reviewer | Audit Runner must complete first |

## Execution Checklist

1. **Start stack** if API (3001) not responding
2. **Run** `bash .cursor/skills/super-agente-bmc-dashboard/scripts/run_audit.sh --output=.cursor/bmc-audit/latest-report.md`
3. **Probe** all endpoints (health, cotizaciones, proximas-entregas, pagos-pendientes, kpi-financiero, audit, calc/catalogo)
4. **Write** handoff.json to `.cursor/bmc-audit/`
5. **Emit** "AUDIT RUNNER COMPLETE. Invoke bmc-dashboard-debug-reviewer."
6. **Update** `docs/team/PROJECT-STATE.md` (Cambios recientes) con resumen del audit.

## Output Paths

| File | Purpose |
|------|---------|
| `.cursor/bmc-audit/latest-report.md` | Full report from run_audit.sh |
| `.cursor/bmc-audit/handoff.json` | Metadata for Debug Reviewer |
| `.cursor/bmc-audit/endpoint-probe.json` | Optional: raw endpoint responses |

## One-Shot Script (Audit + Debug)

To run both Audit Runner and Debug Reviewer sequentially:

```bash
bash .cursor/skills/bmc-dashboard-audit-runner/scripts/run_audit_then_debug.sh
```

Requires API running on 3001. Output: `.cursor/bmc-audit/`

## Reference

- [super-agente-bmc-dashboard/SKILL.md](../super-agente-bmc-dashboard/SKILL.md) — base audit steps
- [super-agente-bmc-dashboard/reference.md](../super-agente-bmc-dashboard/reference.md) — endpoints, commands
