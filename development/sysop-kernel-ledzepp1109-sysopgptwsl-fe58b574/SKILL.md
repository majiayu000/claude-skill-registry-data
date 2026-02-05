---
name: sysop-kernel
description: >-
  WSL2 system health checks and Windows-specific hardening operator kernel for
  SYSopGPTWSL: run a repeatable sysop pipeline (preflight, WSL healthcheck,
  drift check, Windows snapshot via PowerShell, perf bench), produce a diffable
  report, and append evidence to `learn/LEDGER.md`. Use for sysop/health checks,
  drift/baseline verification, or when debugging Windows/WSL interop pitfalls
  (UNC cwd, UTF-8 BOM in PowerShell JSON, `/mnt/c` performance) and for
  Windows-side hardening/performance signals (power plan, power throttling,
  storage/volume inventory, WSL status/version). Use Plan-first execution and
  explicit verification reporting.
short-description: WSL2 sysop health/drift/baseline checks
triggers:
  - sysop
  - system check
  - health check
  - drift check
  - baseline
version: 1.0.0
codex-version: ">=0.76.0"
metadata:
  short-description: Run sysop operator kernel
---

# SYSop Operator Kernel

Follow `AGENTS.md` (Plan-first; worktrees per task when parallel; verification required; auditable notes).

## Plan mode (no writes yet)
1) Read `AGENTS.md`, then `sysop/README_INDEX.md` (index-first).
2) Restate the operator goal (health/drift/snapshot/bench/report).
3) Define “done means…”:
   - fresh artifacts under `sysop/out/` (at least `sysop/out/report.md`)
   - if `./sysop/run.sh` is executed: a new entry appended to `learn/LEDGER.md`
4) Hypotheses (when something fails):
   - Windows interop unavailable (for example `powershell.exe`/vsock errors)
   - UNC cwd issues (Windows commands must run from `/mnt/c`)
   - `systemctl` bus blocked in the Codex runner (expected)
5) Minimal evidence (read-only) to gather as needed:
   - `./sysop/preflight.sh`
   - `./sysop/healthcheck.sh`
   - `command -v powershell.exe || command -v pwsh.exe` (if Windows snapshot is requested)
6) Propose the exact `./sysop/run.sh ...` command(s) and STOP for approval:
   - `./sysop/run.sh all` (writes under `sysop/out/` and appends to `learn/LEDGER.md`)
   - Optional (repo-scoped auto-fix + script generation): `./sysop/run.sh all --apply-fixes`

## Execution mode (after approval)
- Run the approved `./sysop/run.sh ...` command(s) from repo root.
- Return results using the repo output format (see `AGENTS.md`), including:
  - report path: `sysop/out/report.md`
  - “Top bottlenecks” excerpt (if present)
  - latest `learn/LEDGER.md` excerpt (3–8 lines)

## Safety
- No destructive ops (`rm -rf`, `git reset --hard`, `git clean -fdx`).
- No writes outside the repo or to `/etc`.
- No internet fetches.

For details and rationale, see `references/OPERATOR_KERNEL.md`.
