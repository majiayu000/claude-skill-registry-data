---
name: codex-doctor
description: Analyze local Codex session telemetry and produce privacy-safe efficiency reports with actionable workflow recommendations. Use when the user asks to run Codex Doctor, inspect Codex productivity, diagnose context bloat, repository exploration, validation or retry patterns, compare recent sessions, or interpret a codex-efficiency-report HTML/JSON file. Default to local telemetry-only analysis; use the optional compact AI diagnosis only when the user explicitly requests AI interpretation.
---

# Codex Doctor

Analyze Codex usage from local session data, separate evidence from interpretation, and turn recurring patterns into small workflow changes.

## Choose the analysis mode

- Use telemetry-only mode by default. It is local, deterministic, strict-privacy, and does not invoke a model.
- Use AI mode only when the user explicitly asks for AI diagnosis or a deeper interpretation. It makes one compact `codex-cli` diagnosis call and may consume Codex usage.
- Never use the `openai` provider unless the user explicitly requests it and provides the required authorization. Do not use paid production APIs, production credentials, or real user data for this analysis.

## Locate and run the analyzer

1. Resolve the analyzer directory in this order:
   - a path supplied by the user;
   - `CODEX_DOCTOR_DIR` if set;
   - the current workspace when it contains `bin/codex-insights.js` and the Codex Doctor package;
   - a narrowly scoped local path the user has already mentioned.
2. If no analyzer directory is available, ask for its path. Do not scan the whole home directory or install dependencies without a reason.
3. Run from the analyzer directory and write output and, when needed, cache data to dedicated temporary or user-selected directories. If the default cache location is not writable, pass an explicit `--cache-dir`.

Telemetry-only example:

```bash
node ./bin/codex-insights.js report \
  --telemetry-only \
  --days 14 \
  --limit 20 \
  --no-open \
  --cache-dir <report-directory>/cache \
  --out-dir <report-directory>
```

AI diagnosis example:

```bash
node ./bin/codex-insights.js report \
  --ai \
  --provider codex-cli \
  --days 14 \
  --limit 20 \
  --no-open \
  --cache-dir <report-directory>/cache \
  --out-dir <report-directory>
```

Do not combine `--ai` with `--telemetry-only`. Preserve the generated JSON and HTML paths in the result. Read JSON for facts and use HTML for the human-readable report; do not treat the HTML layout as the data source.

## Interpret the result

1. Report the analysis mode, date range, session count, output paths, and whether AI ran.
2. Treat deterministic telemetry as the numeric source of truth. Treat AI output as advisory and evidence-bound.
3. Check sample size, data quality, estimated fields, and trend direction before drawing conclusions.
4. Separate observations, inferences, and recommendations. Do not turn a heuristic score into a claim about exact cost, quality, or time saved.
5. Rank no more than three actions by expected benefit and effort. For each action, state the evidence, the smallest behavior change, and how to verify improvement.
6. Distinguish recommendations that belong in global rules, project rules, a reusable Skill, or a one-off task handoff. Keep raw metrics and project-specific paths out of global rules.

Pay particular attention to these signals:

- context bloat and long sessions;
- exploration that does not converge on an affected boundary;
- validation repeated beyond the changed risk surface;
- repeated failures and retries without a changed hypothesis;
- trends that worsen in recent sessions rather than isolated outliers.

## Convert findings into action

Prefer operational changes over more prompt text:

- At a phase boundary, summarize the current objective, completed evidence, unresolved risks, and next step before starting an independent sub-goal.
- Before broad exploration, name the initial files, commands, and acceptance conditions; expand only when evidence requires it and record why.
- Route validation by the changed boundary and risk. Keep low-risk feedback small and reserve integration, security, build, release, and production checks for the boundaries that require them.
- After repeated failures, classify the failure and change the command, environment, input, or strategy instead of replaying the same attempt.

Do not automatically edit `AGENTS.md`, install Skills, commit changes, open or merge PRs, or change production state from a report. Present the recommendation first and make those changes only when the user explicitly requests them.

## Completion report

Finish with:

- conclusion first;
- analysis mode and scope;
- top findings with supporting evidence;
- up to three concrete next actions;
- what is already covered by existing rules or Skills;
- unverified areas, data-quality limits, and any environment blocker;
- exact report paths.

After a workflow change, rerun the telemetry-only report after a meaningful sample of new sessions and compare trends rather than one absolute score.
