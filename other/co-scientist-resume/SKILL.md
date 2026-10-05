---
name: co-scientist-resume
description: Resume an interrupted Co-Scientist run from Codex.
---

# co-scientist-resume

Goal:

- Resume one interrupted Co-Scientist run from persisted artifacts.

Expected input:

- one run directory such as `runs/test1`

Execution steps:

1. Resolve the run directory relative to the repository root.
2. Confirm that `input.md` and `state/` artifacts exist.
3. Run:

   ```bash
   python -m tools.host.project_cli resume <run-dir> --skill co-scientist-pipeline
   ```

4. Read `state/PIPELINE_STATE.json`, `state/CURRENT_STAGE.json`, and `state/HOST_AGENT_HANDOFF.json`.
5. Read the CLI JSON result and the run-local dashboard receipt artifacts:
   - `runs/<run_id>/dashboard/LINKS.md`
   - `runs/<run_id>/dashboard/LINKS.json`
6. If the CLI JSON contains `dashboardLinks`:
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

7. Run the resume validator before continuing:

   ```bash
   python -m tools.validation.contract_validation <run-dir> --resume --skill co-scientist-pipeline
   ```

8. Resume only incomplete phases. Do not restart completed phases when their artifacts remain valid.
9. Continue from `skills/co-scientist-pipeline/SKILL.md` and the route recorded in persisted state. If the persisted route returns `run_configuration`, resume or rerun `research-config` and validate `research_plan/RESEARCH_PLAN.json` before any generation work.

Rules:

- Resume decisions must be artifact-driven.
- Preserve manifest history and dashboard links.
- Treat `runs/<run_id>/dashboard/LINKS.md` as the human-readable dashboard receipt and `runs/<run_id>/dashboard/LINKS.json` as the machine-readable receipt.
- Treat validator failures as blocking until they are understood and fixed.
- If `research_plan/RESEARCH_PLAN.json` is missing or invalid, expect resume routing to return `run_configuration` instead of skipping directly to generation or evolution.
- Obey the persisted route exactly during resume: `run_review` resumes only review, `run_insights` resumes only insights, `run_proximity` resumes only proximity, `run_ranking` resumes only ranking, and `continue_evolution` may create at most one child before closing that child through review, proximity, ranking with ranking update receipt coverage, convergence, and one appended round receipt.
- Do not synthesize placeholder hypotheses, reviews, tournaments, proximity receipts, embeddings, or evolution-round receipts to make progress.
- If the required sub-skill or canonical tool cannot be executed, stop and report a resumable blocked state instead of writing low-information artifacts.
- A completed evolution round must be replayable from exactly one router decision, one evolved child, one review bundle, one proximity receipt, completed ranking artifacts with ranking update receipt coverage, one convergence update, and one appended round receipt.
- Round receipt tournament refs must be child-owned and duplicate-free; do not copy later opponent-side lifetime refs from `HYPOTHESIS.json` into an earlier `EVOLUTION_ROUNDS.jsonl` record.
- Under `completion_driven + auto`, continue until the routing plan reaches overview, a configured checkpoint, or a blocking validator/safety state.
- If you must stop before convergence or a terminal route, tell the user the run is paused, current convergence has not been reached, persisted state is resumable, and the next recommended action is continue evolution through `$co-scientist-resume <run-dir>` or an explicit continue request.
