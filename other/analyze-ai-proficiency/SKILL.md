---
name: analyze-ai-proficiency
description: Set up and run the developer AI workflow proficiency analysis on local CSV or Excel exports. Use when asked to process AI usage and developer survey files, estimate workflow levels and probabilities, or rerun the AI proficiency specification.
---

# Analyze AI Proficiency

## Purpose

Execute the repository's AI workflow scope analysis from local files through checked outputs. Handle Python setup, file inspection, manifest creation, documented adapters, analysis, and result interpretation. The user should be able to supply a folder and get results without manually assembling commands or mappings.

## When to use and invocation

Use for local developer AI usage plus survey analysis under this specification. Arguments supplied by the user: `$ARGUMENTS`. Treat arguments as paths or requested options, never interpolate them as shell code.

```text
/analyze-ai-proficiency /path/to/exports
/analyze-ai-proficiency /path/to/manifest.json
/analyze-ai-proficiency setup
/analyze-ai-proficiency demo
```

With no path, use a path already supplied in the conversation. Otherwise ask one question for the folder containing the exports. Do not search unrelated directories for company records. `setup` installs dependencies and runs tests without needing data; `demo` runs only invented fixtures and clearly labels its output.

## Inputs and outputs

Inputs are the local exports and the [single authoritative specification](../../../prompts/ai-proficiency-spec.md). It defines the roster, identity, survey, telemetry, date, unit, and observation-coverage contracts. Read its overview and technical one-pager, then sections 4–10 for execution. The [runner](../../../tools/ai-proficiency/workflow.py) and analysis files ship with this skill in the same repository; do not copy just this skill folder to another machine.

Outputs are a reusable manifest, any documented derivative input files, and a new run directory with `developer_predictions.csv`, `report.md`, and supporting audits/metrics. Retain original exports unchanged. Keep company files and results local and outside tracked source files. Default runs go beside the manifest in `ai-proficiency-runs/` with a unique timestamped directory. Report absolute paths to the user.

## Steps

### 1. Locate the package and set up

Resolve the repository root from this skill's location: three parent directories above its folder. Confirm that `prompts/ai-proficiency-spec.md` and `tools/ai-proficiency/workflow.py` exist. If absent, explain that the full repository is required; do not recreate the statistical method from memory.

Use an available Python 3.11 or 3.12 interpreter. Check `python3.12`, `python3.11`, then `python3`; select one that satisfies the version requirement. If none exists, report the prerequisite instead of installing a system interpreter without an explicit request. Execute from the repository root, quoting actual paths safely:

```bash
python3.12 tools/ai-proficiency/workflow.py setup
```

The runner creates an isolated `.venv`, installs the declared dependencies when needed, and runs the tests. Use the selected interpreter in place of `python3.12` throughout. Dependency installation needs package-index access on first setup; data analysis itself is local. If setup fails, address the actual environment error before proceeding. For a setup-only request, report the successful setup and stop.

### 2. Inspect and construct a reusable manifest

For a folder, run:

```bash
python3.12 tools/ai-proficiency/workflow.py inspect /path/to/exports
```

This reports file/sheet names, headers, and row counts without printing row contents. Identify the roster, surveys, and authoritative telemetry sources. Inspect only the local field values needed to resolve dates, units, identity mappings, grain, and distinct survey options. Follow the specification's manifest example; create `manifest.json` alongside the inputs unless that name already exists. Reuse an existing manifest after checking its paths and declared windows.

Map clear headers directly. If April/August exports are separate, create local normalized derivative files with explicit wave/date columns only when those facts are established by export metadata or the user. Preserve source files and document transformations and original file hashes in a local `input-preparation.md`. Use narrow adapters for workbook headers, multiple sheets, or per-tool aggregation; write and run targeted checks for their joins and aggregation rules. Do not ask the user to hand-author JSON.

Ask one concise question bundling only unresolved facts that affect validity. Typical blockers are a missing full-company roster, unknown snapshot dates, overlapping token definitions, or unknown observation coverage. Never invent `ai_observed_days=30`, infer zero usage from absence, map “no AI coding” to Level 0, or fabricate retrospective telemetry. When coverage is unknown, explain that the spec's conservative missing-coverage path cannot release a level for those rows. Report contradictory coverage declarations rather than silently changing recorded activity.

### 3. Process the files

```bash
python3.12 tools/ai-proficiency/workflow.py run --manifest /path/to/exports/manifest.json
```

The runner sets up dependencies if needed, runs strict preflight, performs the frozen April-to-August analysis, and verifies output coverage and probability normalization. `--out /path/to/new/run` selects an output directory; it must not already exist. Never overwrite an earlier run to make a revised analysis appear to be the original holdout evaluation.

For `demo`, execute `workflow.py demo` and report that its invented data validate software operation only. Do not describe its classification accuracy as company evidence.

### 4. Interpret and deliver

Read `input_audit.json`, `analysis.json`, and `report.md`. Check the latest roster count, usable label counts, validation gate, abstentions, calibration, and selection sensitivity. A failed statistical gate is a completed analysis with insufficient evidence, not a reason to tune thresholds until they pass.

Add a short leadership interpretation to the local `report.md` when real data support it: the period and scope, whether the model distinguishes levels, response coverage, principal limitations, and the evidence-supported next step. Keep the generated numeric results intact. Provide the user links to the developer output, report, reusable manifest, and run directory. State whether a provisional level was released and why rows abstained; never paste the entire developer table into chat.

## Examples

- “Process this folder of exports.” Set up, inspect, construct the manifest, resolve only material unknowns, and run the package.
- “Rerun this manifest.” Reuse its mappings, create a new output directory, and report the new run's findings without retuning the held-out model.
- “Set this up before I have the data.” Run setup and tests; return the invocation for a future input folder.

## Non-goals and guardrails

- Survey workflow answers alone define and validate the labels. Retain separate self-selection and model prediction columns.
- Probabilities concern reported workflow scope, conditional on AI use; they do not establish true skill. Level 0 is unidentified by the current questions.
- Preserve developer-grouped fitting, independent temporal validation, class-support requirements, and abstention rules. No survey fields, spend, model prestige, or productivity counts enter the primary classifier.
- Do not inspect session contents to generate validation labels. Do not upload data, fetch company records from connectors, or commit/push inputs and outputs as part of running this analysis skill.
- This entrypoint requires the repository's scripts and specification. Project skill discovery and slash invocation follow the [Claude Code skill documentation](https://code.claude.com/docs/en/skills).
