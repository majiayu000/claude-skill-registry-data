---
name: forge-registry
description: Builds the global, opt-in, read-only Forge Project Registry across all projects. Use when the owner wants a bird's-eye view of status, last run, tickets, and ports.
---

# forge-registry — global project registry (opt-in, read-only)

An **opt-in** aggregate across every Forge project on this machine. It never runs automatically and never
changes any project — it only reads and writes one global index.

## When to use
- The owner asks "show me all my Forge projects" / "which projects have open tickets / failing tests".
- Before a portfolio-wide sweep, to see status/ports/last-run at a glance.

## How to run
```
node .claude/forge-bin/forge-registry.cjs scan            # scan ~/Documents, write the registry
node .claude/forge-bin/forge-registry.cjs scan --json     # also print the aggregate to stdout
node .claude/forge-bin/forge-registry.cjs scan --root <dir> --run <run_id>
```
Outputs (global):
- `~/.claude/forge/registry/projects.json` — machine-readable index.
- `~/.claude/forge/registry/index.html` — a self-contained home-view (open it directly in a browser; data
  is inlined, no server needed).

Each record: `project_id, name, path, stack, status, last_run_id, last_run_status, last_run_at,
open_tickets, test_status, port`. `test_status` reads a run's `doctor.json` (from Forge Doctor) when present.

## Hard rules (isolation + honesty)
- **Reads** other projects' `.claude/` read-only (that is the opt-in aggregation job); it **NEVER writes**
  into any scanned project. The only thing written is the global registry dir.
- Every record is secret-redacted before writing (defense in depth) — never persists a raw key.
- Real `DASHBOARD_STATE.json` / `run.json` data only; a missing/malformed file yields honest defaults
  (`unknown`), never a fabricated status. (v2.9.0: the retired per-project server.cjs that used to write
  `DASHBOARD_STATE.json` is removed, so a project synced since then will simply never have one — the same
  honest-default path a project that never started that old dashboard already went through.)
- Opt-in only: it never runs on `require`, only via the `scan` command.
