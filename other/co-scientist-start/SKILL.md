---
name: co-scientist-start
description: Start one Co-Scientist run from Codex using a research goal or imported brief.
---

# co-scientist-start

Goal:

- Create a Co-Scientist run, bootstrap the canonical host-agent pipeline, and continue from the repository workflow skills.

Expected input:

- a natural-language research goal
- or a brief path
- or no explicit arguments, which should trigger a short guided intake

Execution steps:

1. If the user only invokes `$co-scientist-start`, ask only for the missing high-level run inputs: goal, exploration preference, iteration policy, and optional brief path.
2. Convert high-level controls into explicit CLI flags. Do not pass free-form `key: value` text when a real flag exists.
3. Before creating files, run:

   ```bash
   python -m tools.host.project_cli start --goal "<goal>" --skill co-scientist-pipeline --summary-only
   ```

   Use the equivalent `--brief <path>` command for imported briefs.

4. Show the returned summary and wait for user confirmation.
   - Tell the user that the run-local dashboard receipt will be written to:
     - `runs/<run_id>/dashboard/LINKS.md`
     - `runs/<run_id>/dashboard/LINKS.json`
   - Tell the user that `$co-scientist-dashboard <run-dir>` is the ready-link follow-up when the background bootstrap has not finished yet.
5. After confirmation, run:

   ```bash
   python -m tools.host.project_cli start --goal "<goal>" --skill co-scientist-pipeline
   ```

6. Read the emitted `runs/<run_id>/state/HOST_AGENT_HANDOFF.json`.
7. Read the CLI JSON result and the run-local dashboard receipt artifacts:
   - `runs/<run_id>/dashboard/LINKS.md`
   - `runs/<run_id>/dashboard/LINKS.json`
8. If the CLI JSON contains `dashboardLinks`:
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

9. Open `skills/co-scientist-pipeline/SKILL.md` and the listed shared references from the handoff.
10. Continue execution from the canonical repository-local workflow. If routing returns `run_configuration`, run `research-config` and validate `research_plan/RESEARCH_PLAN.json` before generation.
11. After major phase writes, run:

   ```bash
   python -m tools.validation.contract_validation runs/<run_id> --skill co-scientist-pipeline
   ```

Rules:

- Use `tools.host.project_cli`; do not call the Claude-specific CLI from Codex entry skills.
- Treat `skills/` as canonical and `.agents/skills/` as the installed Codex discovery surface.
- Do not invent run artifacts. Read the CLI JSON and run-local receipts.
- Treat `runs/<run_id>/dashboard/LINKS.md` as the human-readable dashboard receipt and `runs/<run_id>/dashboard/LINKS.json` as the machine-readable receipt.
- Fresh runs normally pass through the explicit `Configuration` stage first so `research-config` can materialize `research_plan/RESEARCH_PLAN.json`.
- Under `completion_driven + auto`, continue until the routing plan reaches overview, a configured checkpoint, or a blocking validator/safety state.
- If you must stop before convergence or a terminal route, tell the user the run is paused, current convergence has not been reached, persisted state is resumable, and the next recommended action is continue evolution through `$co-scientist-resume <run-dir>` or an explicit continue request.
