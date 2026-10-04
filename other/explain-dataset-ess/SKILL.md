---
name: explain-dataset-ess
description: >
  Helps users of the Timefold Employee Shift Scheduling (ESS) model understand an optimized
  schedule by fetching and interpreting the dataset via the API. Use this skill whenever
  someone asks why shifts are unassigned, why a specific employee was assigned to a shift,
  what the bottlenecks or coverage gaps are, how to read the optimization score, or what
  they should do to improve their schedule. Also invoke when the user says things like
  "explain my results", "what's wrong with my plan", "help me understand this schedule",
  "why can't this shift be filled", "interpret my ESS dataset", or when they share a
  dataset ID or score string and want help making sense of it.
---

# Model context: Employee Shift Scheduling (ESS)

## Terminology

| Generic term | ESS term |
|---|---|
| Work item / work unit | shift |
| Resource | employee |
| Mandatory work | mandatory shift |
| Optional work | optional shift |
| Required capability | skill (e.g. `C300`, `PM`) |
| Capacity constraint | employment contract (max hours/week) |

## Model-specific configuration

Always set these before running any script.

```bash
MODEL=employee-shift-scheduling
MODEL_API_URL=https://app.timefold.ai/api/models/employee-scheduling/v1
COLLECTION=/schedules
OPENAPI_URL=https://app.timefold.ai/openapis/employee-scheduling/v1
```

## Scripts

Scripts live in the sibling skill `explain-dataset-shared`, in its `scripts/` directory.
Anchor every path on this skill's own directory, not on the working directory. The working
directory is the user's project, and these skills are installed somewhere else.

In Claude Code, `${CLAUDE_SKILL_DIR}` is substituted with this skill's directory. If your agent
leaves the placeholder unresolved, replace it with the absolute directory that holds this
`SKILL.md`.

`$PY` is the Python runner that the shared skill's runtime check selects (`uv run`,
`python3`, or `python`). Run that check before the first script call.

```bash
SKILL_DIR=${CLAUDE_SKILL_DIR}
SHARED=$SKILL_DIR/../explain-dataset-shared
SCRIPTS=$SHARED/scripts
PLUGIN_ROOT=${CLAUDE_PLUGIN_ROOT:-$SKILL_DIR/../..}

$PY $SCRIPTS/summarize.py             --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID [--tenant ID]
$PY $SCRIPTS/list_unassigned.py       --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID [--recommendations]
$PY $SCRIPTS/resource_metrics.py      --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID [--sort unprefs|overtime|hours|visits|name]
$PY $SCRIPTS/work_details.py          --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID --work-ids "shift-001"
$PY $SCRIPTS/work_details.py          --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID --resource "EMP-001"
$PY $SCRIPTS/score_violations.py      --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID [--type hard|medium|soft]
$PY $SCRIPTS/score_justifications.py  --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID [--samples 3]
$PY $SCRIPTS/score_justifications.py  --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID --resource "EMP-001"
```

`$SHARED` also carries the version stamp and, in a plugin install, `$PLUGIN_ROOT` carries the
plugin manifest. The report metadata needs both. Keep the two variables set.

## Documentation

- User guide: https://docs.timefold.ai/employee-shift-scheduling/latest/
- Metrics and KPIs: https://docs.timefold.ai/employee-shift-scheduling/latest/metrics-and-optimization-goals

## ESS-specific notes

- **Mandatory vs optional is not a tag on the shift.** Each shift has a `priority` (1-10), and
  whether a given priority counts as mandatory or optional is set per dataset in
  `globalRules.unassignedShiftRule.priorityWeights`, which maps priority levels to a
  `MANDATORY` or `OPTIONAL` assignment. When you need to tell which unassigned shifts are
  actually mandatory (a real bottleneck) versus optional (expected leftover capacity), read
  that mapping from the dataset's own input rather than assuming a fixed priority threshold.
  See [Mandatory and optional shifts](https://docs.timefold.ai/employee-shift-scheduling/latest/shift-service-constraints/mandatory-and-optional-shifts#_mandatory_and_optional_shifts).

## Full instructions

Read and follow: `$SHARED/SKILL.md`
