---
name: co-scientist-dashboard
description: Resolve dashboard links for one Co-Scientist run from Codex.
---

# co-scientist-dashboard

Goal:

- Resolve the ready dashboard runtime for one run directory and return the current run links to the user.

Expected input:

- one run directory such as `runs/test1`

Execution steps:

1. Run:

   ```bash
   python -m tools.host.project_cli dashboard <run-dir>
   ```

2. Read the CLI JSON result.
3. Read `runs/<run_id>/dashboard/LINKS.md` and `runs/<run_id>/dashboard/LINKS.json` when present.
4. Use the CLI JSON result as the canonical ready-link resolution surface for this run.
5. Return `links.dashboard` as the primary dashboard URL, include the deep links under `links.*`, and point to `runs/<run_id>/dashboard/LINKS.md` as the human-readable dashboard receipt.
6. If `runtime.status` is still `starting`, tell the user that the dashboard is still booting, point them to `runs/<run_id>/dashboard/LINKS.md`, and include the retry command:

   ```text
   $co-scientist-dashboard <run-dir>
   ```

Rules:

- Treat `LINKS.md` as the human-readable receipt and `LINKS.json` as the machine-readable receipt.
- Do not fabricate dashboard URLs when the dashboard runtime is not available.
- This skill is the ready-link follow-up when `start`, `run`, or `resume` only returned background bootstrap status.
- This skill only resolves dashboard runtime availability and exposes run-local links; it must not perform main pipeline reasoning.
