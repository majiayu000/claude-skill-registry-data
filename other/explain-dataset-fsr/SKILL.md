---
name: explain-dataset-fsr
description: >
  Helps users of the Timefold Field Service Routing (FSR) model understand an optimized route
  plan by fetching and interpreting the dataset via the API. Use this skill whenever someone
  asks why visits are unassigned, why a specific vehicle is assigned to a visit, what the travel
  efficiency or SLA compliance looks like, where the coverage gaps are, or what they should do
  to improve their plan. Also invoke when the user says things like "explain my route plan",
  "what's wrong with my routing", "help me understand this dataset", "why can't this visit be
  scheduled", "interpret my FSR results", or when they share a dataset ID and want help making
  sense of it.
---

# Model context: Field Service Routing (FSR)

## Terminology

| Generic term | FSR term |
|---|---|
| Work item / work unit | visit |
| Resource | vehicle |
| Resource sub-unit | vehicle shift (a vehicle can have multiple shifts) |
| Mandatory work | mandatory visit |
| Optional work | optional visit |
| Required capability | skill (`requiredSkills`) |
| Capacity constraint | shift time window (`maxEndTime`), max visits, max travel time |

## Model-specific configuration

Always set these before running any script.

```bash
MODEL=field-service-routing
MODEL_API_URL=https://app.timefold.ai/api/models/field-service-routing/v1
COLLECTION=/route-plans
OPENAPI_URL=https://app.timefold.ai/openapis/field-service-routing/v1
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
$PY $SCRIPTS/resource_metrics.py      --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID [--sort overtime|travel|visits|name]
$PY $SCRIPTS/work_details.py          --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID --work-ids "visit-001"
$PY $SCRIPTS/work_details.py          --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID --resource "VAN-12"
$PY $SCRIPTS/score_violations.py      --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID [--type hard|medium|soft]
$PY $SCRIPTS/score_justifications.py  --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID [--samples 3]
$PY $SCRIPTS/score_justifications.py  --model-api-url $MODEL_API_URL --model $MODEL --dataset-id ID --resource "VAN-12"
```

`$SHARED` also carries the version stamp and, in a plugin install, `$PLUGIN_ROOT` carries the
plugin manifest. The report metadata needs both. Keep the two variables set.

## API

```
Base URL : https://app.timefold.ai/api/models/field-service-routing/v1
Auth     : X-API-KEY: {token}
Collection path: /route-plans
OpenAPI spec: https://app.timefold.ai/openapis/field-service-routing/v1
```

## Documentation

- User guide: https://docs.timefold.ai/field-service-routing/latest/
- Metrics and KPIs: https://docs.timefold.ai/field-service-routing/latest/metrics-and-optimization-goals

## FSR-specific notes

- **Unassigned visits** are in `modelOutput.unassignedVisits` (an explicit list of visit IDs),
  not inferred from a null field like in ESS.
- **Vehicles have shifts**: a vehicle wraps one or more `vehicleShift` objects that each have
  their own itinerary, time window, and metrics. Per-vehicle aggregate metrics are in
  `vehicle.metrics`; per-shift detail is in `vehicle.shifts[].metrics`.
- **Travel metrics** are a core KPI: total travel time, distance, average per visit, and time
  breakdowns (depot-to-first, between visits, last-to-depot).
- **SLA**: if `percentageVisitsInSla` / `absoluteVisitsInSla` are present, call them out.
  They directly measure service quality.
- **Mandatory vs optional is not a fixed tag or priority range.** By default, this is automatic
  and implicit: a visit is mandatory if its time window falls within the current planning
  window, and optional if its time window ends outside it. The `priority` field can override
  this default: built-in priorities `1`-`10` use the automatic `AUTO` behavior above
  (overridable dataset-wide via `defaultAssignmentType: MANDATORY`), `opt-1`-`opt-10` are
  always optional, and custom priority names can set an explicit `assignment` of `AUTO`,
  `MANDATORY`, or `OPTIONAL`. Read the dataset's own priority configuration rather than
  assuming a fixed threshold. See
  [Priority visits and optional visits](https://docs.timefold.ai/field-service-routing/latest/visit-service-constraints/priority-visits-and-optional-visits).

## Full instructions

Read and follow: `$SHARED/SKILL.md`
