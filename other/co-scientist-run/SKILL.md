---
name: co-scientist-run
description: Bootstrap an existing Co-Scientist run directory from Codex.
---

# co-scientist-run

Goal:

- Bootstrap one existing Co-Scientist run and continue with the canonical pipeline.

Expected input:

- one run directory such as `runs/test1`
- or one compatibility config path such as `runs/test1/config.yaml`

Execution steps:

1. Resolve the run directory or config path relative to the repository root.
2. Run:

   ```bash
   python -m tools.host.project_cli run <run-target> --skill co-scientist-pipeline
   ```

3. Read `runs/<run_id>/state/HOST_AGENT_HANDOFF.json`.
4. Read the CLI JSON result and the run-local dashboard receipt artifacts:
   - `runs/<run_id>/dashboard/LINKS.md`
   - `runs/<run_id>/dashboard/LINKS.json`
5. If the CLI JSON contains `dashboardLinks`:
   - If `dashboard.status` is `running`, return `dashboardLinks.dashboard` as the primary dashboard URL and include the deep links.
   - If `dashboard.status` is `starting`, immediately run:

   ```bash
   python -m tools.host.project_cli dashboard <run-dir>
   ```

   - Read the refreshed CLI JSON result plus `runs/<run_id>/dashboard/LINKS.md`.
   - If `runtime.status` is now `running`, return the refreshed `links.dashboard` URL as the primary dashboard URL and include the deep links.
   - If `runtime.status` is still `starting`, tell the user that the dashboard is still booting, point them to `runs/<run_id>/dashboard/LINKS.md`, and include the retry command:

   ```text
   $co-scientist-dashboard <run-dir>
   ```

6. Open `skills/co-scientist-pipeline/SKILL.md` and the shared references listed by the handoff.
7. Continue from the canonical repository-local workflow instead of inventing a parallel flow. If the refreshed routing plan returns `run_configuration`, execute `research-config` and validate `research_plan/RESEARCH_PLAN.json` before any generation work.
8. After major phase writes, run:

   ```bash
   python -m tools.validation.contract_validation runs/<run_id> --skill co-scientist-pipeline
   ```

Rules:

- Use persisted artifacts as the source of truth.
- Do not skip `research-config` when routing requires `run_configuration`.
- The first active stage may be `Configuration` rather than `Generation`; do not skip it when the routing plan requires `run_configuration`.
- Treat `skills/` as canonical and `.agents/skills/` as the installed Codex discovery surface.
- Treat `runs/<run_id>/dashboard/LINKS.md` as the human-readable dashboard receipt and `runs/<run_id>/dashboard/LINKS.json` as the machine-readable receipt.
- Under `completion_driven + auto`, continue until the routing plan reaches overview, a configured checkpoint, or a blocking validator/safety state.
- If you must stop before convergence or a terminal route, tell the user the run is paused, current convergence has not been reached, persisted state is resumable, and the next recommended action is continue evolution through `$co-scientist-resume <run-dir>` or an explicit continue request.
