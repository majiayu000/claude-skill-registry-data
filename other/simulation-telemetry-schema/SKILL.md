---
name: simulation-telemetry-schema
description: Use this skill whenever writing any code that logs, emits, stores, exports, or processes simulation events in the Myelin platform. This defines the immutable event payload contract, the evidence export structure, and the KPI reproducibility rules. Do not invent field names, omit required fields, or generate telemetry shapes that deviate from this schema. Load this skill before writing any telemetry, logging, or analytics code.
---

This skill is the single source of truth for simulation telemetry in the Myelin platform. Every assessed event emitted by the simulator must conform exactly to the schemas defined here. KPI aggregates, evidence exports, and audit packs are all derived from these immutable logs. If the event shape is wrong, downstream reproducibility breaks.

---

## Core Principle: Immutable Event Log

Every assessed interaction produces an event. Events are append-only. Once written, an event record is never modified. KPI values are always recomputed from the raw event log — they are never stored as a source of truth in place of the events themselves.

No scenario may be enabled for a partner tenant unless its assessed steps map to at least one approved core curriculum outcome ID.

---

## Step Event Payload — `SimStepEvent`

Every assessed simulation step emits one event at the moment of pass or fail determination.

```json
{
  "eventType": "SIM_STEP",
  "schemaVersion": "1.0",
  "sessionId": "string — UUID v4, unique per learner session",
  "learnerId": "string — tenant-scoped learner identifier, never a raw email",
  "tenantId": "string — institution identifier",
  "scenarioId": "string — e.g. LOTO_7STEP_v1",
  "scenarioVersion": "string — semver of the scenario definition used",
  "scoringRulesVersion": "string — semver of the scoring rules applied",
  "stepId": "string — e.g. LOTO_STEP_02",
  "stepLabel": "string — human-readable, e.g. Isolate Energy Source",
  "curriculumOutcomeIds": ["string — e.g. FND-TT-01"],
  "attemptNumber": "integer — 1-based, increments on each retry of this step",
  "timestamp": "string — ISO 8601 UTC, e.g. 2026-03-12T09:45:00.000Z",
  "result": "PASS | FAIL",
  "measuredValue": "number — the actual physics value at moment of evaluation",
  "requiredThreshold": "number — the pass threshold from the scoring rules",
  "thresholdOperator": "LT | LTE | GT | GTE | WITHIN",
  "toleranceDelta": "number | null — for WITHIN operators, the ± tolerance",
  "inputMode": "POINTER | KEYBOARD | GAMEPAD | HAND_TRACKING",
  "performanceSnapshot": {
    "fps": "number — frame rate at moment of event",
    "frameTimeMs": "number — last frame duration in ms",
    "interactionLatencyMs": "number — input-to-visual latency at event time"
  },
  "demoMode": "boolean — true if this event belongs to a prospect demo session"
}
```

### Required fields

All fields above are required. No field may be null unless explicitly marked `| null`. The `curriculumOutcomeIds` array must contain at least one entry — an empty array is a schema violation.

### `demoMode` isolation rule

If `demoMode: true`, this event must be written to the demo analytics namespace. It must never be co-mingled with live tenant event logs. Query paths for learner dashboards, cohort reports, and KPI exports must always filter on `demoMode: false` unless explicitly in a demo analytics context.

---

## Scenario Completion Event — `SimCompleteEvent`

Emitted once when all required steps for a scenario pass and the completion interaction is registered.

```json
{
  "eventType": "SIM_COMPLETE",
  "schemaVersion": "1.0",
  "sessionId": "string",
  "learnerId": "string",
  "tenantId": "string",
  "scenarioId": "string",
  "scenarioVersion": "string",
  "scoringRulesVersion": "string",
  "curriculumOutcomeIds": ["string — all outcomes exercised in this scenario"],
  "completedAt": "string — ISO 8601 UTC",
  "totalDurationSeconds": "number — time from first step attempt to completion",
  "totalAttempts": "number — sum of all step attempt counts",
  "stepTrace": [
    {
      "stepId": "string",
      "result": "PASS | FAIL",
      "attemptNumber": "integer",
      "timestamp": "string"
    }
  ],
  "demoMode": "boolean"
}
```

The `stepTrace` array must contain one entry per assessed step event in session order. This is the reproducibility backbone for audit exports.

---

## Performance Metric Event — `SimPerfEvent`

Emitted on a fixed interval (every 5 seconds) during an active session and on any quality-scaling trigger.

```json
{
  "eventType": "SIM_PERF",
  "schemaVersion": "1.0",
  "sessionId": "string",
  "tenantId": "string",
  "timestamp": "string — ISO 8601 UTC",
  "fps": "number",
  "frameTimeMs": "number",
  "qualityTier": "MINIMUM | HD | HD_PLUS | UHD",
  "lodActive": "integer — 0 to 3",
  "memoryGeometryMB": "number",
  "memoryTexturesMB": "number",
  "memoryPhysicsMB": "number",
  "inputMode": "POINTER | KEYBOARD | GAMEPAD | HAND_TRACKING",
  "demoMode": "boolean"
}
```

Performance events are diagnostic only. They do not contribute to competency outcomes or KPI scores. They are retained for QA and optimization analysis.

---

## Institution Evidence Export Pack

The evidence export is generated on demand by admin or system trigger. It is always reconstructed from the immutable event log — never from cached aggregates.

### Top-level export envelope

```json
{
  "exportId": "string — UUID v4",
  "exportTimestamp": "string — ISO 8601 UTC",
  "exportRequestedBy": "string — admin user identifier",
  "tenantId": "string",
  "exportScope": {
    "scenarioIds": ["string"],
    "dateFrom": "string — ISO 8601",
    "dateTo": "string — ISO 8601",
    "includeInterventionMarkers": "boolean",
    "includeCurriculumMapping": "boolean"
  },
  "signedChecksum": "string — SHA-256 of the serialized export body"
}
```

### Learner competency trace (per learner per scenario)

```json
{
  "learnerId": "string",
  "scenarioId": "string",
  "scenarioVersion": "string",
  "scoringRulesVersion": "string",
  "curriculumOutcomeCoverage": [
    {
      "outcomeId": "string — e.g. FND-TT-01",
      "outcomeLabel": "string",
      "exercised": "boolean",
      "passed": "boolean",
      "passingStepIds": ["string"]
    }
  ],
  "completionStatus": "COMPLETE | INCOMPLETE | NOT_ATTEMPTED",
  "completedAt": "string | null",
  "totalAttempts": "number",
  "totalDurationSeconds": "number",
  "stepTrace": ["— same structure as SimCompleteEvent.stepTrace"]
}
```

### Cohort summary

```json
{
  "tenantId": "string",
  "scenarioId": "string",
  "cohortSize": "integer",
  "completionRate": "number — 0 to 1",
  "medianDurationSeconds": "number",
  "meanAttemptsToCompletion": "number",
  "interventionMarkers": [
    {
      "stepId": "string",
      "failureCount": "integer",
      "retryCount": "integer",
      "recoveryRate": "number — proportion who recovered to PASS after failure"
    }
  ]
}
```

### Intervention markers

An intervention marker is generated for any step where a learner fails and retries. It captures where learners struggled, how many retries were required, and whether recovery occurred. These markers feed the Cohort Risk Agent alert logic.

---

## Curriculum Outcome Mapping Requirement

Before any scenario event is logged for a tenant, the following must be validated:

1. The scenario's `curriculumOutcomeIds` array contains at least one ID from the tenant's approved outcome set
2. Each step's `curriculumOutcomeIds` maps to at least one scenario-level outcome ID
3. A `SCENARIO_OUTCOME_MAP` record exists in the tenant config referencing this scenario version and scoring rules version

If any of these conditions fail, the scenario must not be enabled for that tenant and no events may be written under their tenant ID.

---

## KPI Reproducibility Rules

- All KPI values displayed in dashboards must be recomputable by replaying the raw event log through the scoring rules version referenced in those events
- Changing a scoring rules version does not retroactively alter historical event records
- If a scoring rule changes, new events use the new version; historical KPIs are clearly labeled with their scoring rules version
- Cross-tenant aggregates are never permitted — every query is tenant-scoped

---

## Logging Implementation Notes

- Use append-only event store (database table with no UPDATE or DELETE on event rows)
- Index on: `(tenantId, scenarioId, learnerId, timestamp)` for efficient cohort queries
- Index on: `(sessionId, stepId)` for session-level replay
- Store `demoMode` as a non-nullable boolean column with a database-level constraint
- Never expose `learnerId` in client-side logs or browser console output
- Emit `SIM_STEP` events synchronously at the moment of evaluation — do not batch or defer assessed step events

---

## What Not To Do

- Do not omit `curriculumOutcomeIds` — an empty array is a schema violation
- Do not mix demo and live events in the same namespace or query
- Do not derive KPIs from cached aggregates instead of the event log
- Do not allow `learnerId` to be a raw email address in any event payload
- Do not write a `SIM_COMPLETE` event if all required step pass flags are not confirmed
- Do not modify or delete event records after write
