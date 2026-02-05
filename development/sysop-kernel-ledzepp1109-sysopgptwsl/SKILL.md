---
name: sysop-kernel
description: Run the SYSopGPTWSL operator kernel (repeatable sysop pipeline + diffable report + learning ledger). Use when asked to run sysop checks, collect Windows/WSL snapshots, benchmark, or produce the operator report.
metadata:
  short-description: Run sysop operator kernel
---

# SYSop Operator Kernel

## Do Now
1) Read `AGENTS.md`, then `sysop/README_INDEX.md` (index-first).
2) From repo root, run: `./sysop/run.sh all`
3) Return:
   - Report path: `sysop/out/report.md`
   - Short excerpt of “Top bottlenecks” (if present)
   - Latest `learn/LEDGER.md` entry excerpt (3–8 lines)

## Safety
- No destructive ops (`rm -rf`, `git reset --hard`, `git clean -fdx`).
- No writes outside the repo or to `/etc`.
- No internet fetches.

For details and rationale, see `references/OPERATOR_KERNEL.md`.

