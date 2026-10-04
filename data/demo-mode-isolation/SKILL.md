---
name: demo-mode-isolation
description: Use this skill whenever writing any code that touches the prospect demo path — demo session initialization, demo data loading, demo analytics, demo navigation flow, demo KPI views, or any flag/condition that switches between demo and live contexts. This defines the data isolation contract, the deterministic walkthrough sequence, and the boundary rules that prevent demo and live data from ever co-mingling. Load this skill before writing any demo-mode logic.
---

This skill defines the demo mode isolation contract for the Myelin platform. The prospect demo must be indistinguishable in structure and interaction quality from a live learner session — but it must be completely isolated from live tenant data, real learner records, and operational alerts. These two requirements are non-negotiable and must both hold simultaneously.

---

## Core Isolation Principles

### Principle 1: Demo data never enters the live namespace

Every database write, every analytics event, every transcript entry, and every telemetry payload generated during a demo session must carry `demoMode: true` and must be written to the demo namespace. There is no exception.

Live-namespace queries must always include an explicit filter: `WHERE demo_mode = false`. This filter must be present even in queries where demo data is "obviously" absent — it is a structural safeguard, not a best-effort measure.

### Principle 2: Live data never enters the demo surface

No real learner identifier, real institution name, real cohort data, real operational alert, or real assessment outcome may appear in any demo view. All signals surfaced in the demo — learner names, scores, completion rates, intervention markers, KPI values — are synthetic and sourced exclusively from the demo dataset.

### Principle 3: Demo mode does not reduce platform fidelity

The demo must present the same UI surfaces, the same interaction patterns, the same feedback structures, and the same evidence views as a live session. The only differences are the data source (synthetic vs live) and the session namespace. Feature degradation in demo mode is not acceptable.

### Principle 4: Demo mode does not relax safety rules

All agent safety guardrails (see `agent-safety-guardrails` skill) apply identically in demo mode. The agent narrates the demo journey using the same policy-compliant response patterns. No guardrail is bypassed or weakened because the audience is a prospect rather than a learner.

---

## Session Initialization

A demo session is initiated when:
- A prospect accesses the demo entry point (unauthenticated or using a demo credential)
- The system detects no valid tenant-scoped learner session

Demo session bootstrap sequence:

1. Generate a `demoSessionId` (UUID v4) — this is the namespace key for all events in this session
2. Load the demo dataset from the demo data store — do not query live tenant tables
3. Set `demoMode: true` in the session context object — this flag must be propagated to every component, every API call, and every event emitter for the duration of the session
4. Initialize the simulation with LOTO scenario using demo geometry and demo learner state
5. Initialize the agent with demo narration mode enabled

The `demoMode` flag must never be toggled mid-session. It is set at initialization and is immutable for the session lifetime.

---

## Demo Dataset Specification

The demo dataset is a fixed, version-controlled synthetic data package. It must not be generated at runtime from live data. It is stored separately from live tenant data and updated only through a deliberate content update process.

### Required demo data objects

```json
{
  "demoDataVersion": "string — semver",
  "demoLearnerId": "demo-learner-001",
  "demoInstitutionName": "Myelin Demo Institution",
  "demoCohortLabel": "Demo Cohort 2026",
  "simulationState": {
    "scenarioId": "LOTO_7STEP_v1",
    "scenarioVersion": "string",
    "currentStep": 1,
    "stepPassTrace": [],
    "attemptHistory": []
  },
  "syntheticKPIs": {
    "completionRate": 0.84,
    "medianDurationSeconds": 432,
    "meanAttemptsToCompletion": 2.1,
    "interventionMarkers": [
      {
        "stepId": "LOTO_STEP_03",
        "failureCount": 38,
        "retryCount": 41,
        "recoveryRate": 0.93
      },
      {
        "stepId": "LOTO_STEP_06",
        "failureCount": 22,
        "retryCount": 24,
        "recoveryRate": 0.87
      }
    ]
  },
  "syntheticCurriculumCoverage": [
    {
      "outcomeId": "FND-TT-01",
      "outcomeLabel": "Apply LOTO procedures in accordance with ISO 14118",
      "exercised": true,
      "passed": true
    },
    {
      "outcomeId": "FND-IW-01",
      "outcomeLabel": "Demonstrate safe isolation and energy verification",
      "exercised": true,
      "passed": true
    }
  ]
}
```

All synthetic values must be plausible and representative of a real pilot cohort. They must not be obviously round numbers (e.g. 100%, 0 retries) that undermine credibility in a sales context.

---

## Deterministic Demo Walkthrough Sequence

The demo follows a fixed, non-branching narrative path. The prospect cannot accidentally deviate into an incomplete or broken state. Every waypoint must be reachable in order.

### Waypoint 1 — Core Curriculum Simulation

- Prospect enters the LOTO 7-step simulation
- Full interactive simulation with real physics, real feedback, and real step gating
- Agent narrates each step in real time: explaining the learning objective, the competency outcome being assessed, and the safety rationale
- All audio, visual, and haptic feedback operates identically to a live session
- On completion, emit a `SIM_COMPLETE` event with `demoMode: true`

### Waypoint 2 — Learner Feedback View

- Display the post-simulation results panel using the demo learner's step trace
- Show: steps passed, attempt count, duration, and curriculum outcomes exercised
- Agent provides a sample debriefing message in QTB format
- Intervention marker for Step 3 and Step 6 are surfaced as example coaching prompts

### Waypoint 3 — Instructor Copilot View

- Transition to the instructor-facing cohort panel
- Display synthetic cohort KPIs (completion rate, median duration, mean attempts, intervention heatmap)
- Agent provides a sample intervention recommendation for the Step 3 failure cluster
- Clearly labeled as demo data throughout — do not obscure the synthetic origin

### Waypoint 4 — Evidence and Governance View

- Display the sample evidence export pack using demo data
- Show: curriculum outcome coverage table, step-level competency trace, intervention markers, and export envelope metadata
- Agent explains the audit and KPI reproducibility model: "Every KPI you see here is recomputable from the raw event log"
- Offer to generate a sample export pack download in demo context

### Waypoint 5 — Handoff

- Present a clear transition out of the demo: next steps for pilot discussion
- Do not transition the prospect into a live tenant view, a real learner session, or any authenticated context without a deliberate login flow
- Log a `DEMO_COMPLETE` event to the demo analytics namespace

---

## Demo Analytics Schema

Demo sessions produce analytics events that are structurally identical to live telemetry (see `simulation-telemetry-schema` skill) with the following additions and constraints:

- All events carry `demoMode: true`
- All events use `demoSessionId` as the session identifier
- All events use `"demo-learner-001"` or equivalent synthetic identifier as `learnerId`
- All events use `"demo"` as `tenantId` — never a real tenant identifier
- Demo events are written to a `demo_events` table or equivalent namespace — never to the live `events` table

Demo analytics are used for product analytics only (funnel tracking, demo completion rates, prospect engagement). They are never used as input to live KPI computations, learner dashboards, or institution evidence packs.

---

## UI Labeling Requirements

Every UI surface in the demo must carry a visible label indicating it is a demo view. This label must not be dismissible. It must not be hidden behind a tooltip.

Required label text: `"Demo Mode — Synthetic Data"` or equivalent clear phrasing.

Placement: persistent element in the navigation header or a fixed banner. It must be visible on every waypoint without scrolling.

Purpose: prevent a prospect from misinterpreting synthetic KPIs as real institution performance data.

---

## Feature Flag and Access Control

Demo mode is accessed through:
- A public demo entry point (unauthenticated) — no tenant credentials required
- OR a demo credential issued explicitly for prospect walkthrough purposes

Demo access must never:
- Grant access to any live tenant dashboard
- Grant access to any real learner record
- Grant access to admin configuration or tenant management views
- Persist beyond the demo session into an authenticated production context without an explicit logout and re-authentication

If a demo credential is reused across sessions, each session must initialize a fresh `demoSessionId` and a fresh demo dataset load. Demo sessions do not accumulate or share state.

---

## Code Pattern Requirements

Every function, component, or API handler that has different behavior in demo mode must implement the following pattern:

```javascript
function handleSessionContext(context) {
  if (context.demoMode) {
    return loadDemoDataset(context.demoSessionId);
  }
  return loadLiveTenantData(context.tenantId, context.learnerId);
}
```

Do not use inline ternaries that obscure the demo/live branch. Keep the branches explicit and readable. The demo branch must always load from the demo dataset — never from a filtered view of live data.

API endpoints must validate `demoMode` server-side from the session token. Client-provided `demoMode: true` flags that are not confirmed by the server session must be rejected.

---

## What Not To Do

- Do not query live tenant tables during a demo session under any condition
- Do not display real institution names, real learner names, or real cohort data in any demo view
- Do not allow `demoMode` to be toggled mid-session
- Do not store demo events in the live events table even temporarily
- Do not relax agent safety guardrails in demo mode
- Do not allow a demo session to persist into an authenticated production context without explicit logout
- Do not use round-number synthetic KPIs that undermine credibility (100% completion, 0 failures)
- Do not omit the persistent demo mode label from any UI surface
- Do not accept a client-provided `demoMode` flag without server-side session validation
- Do not let demo analytics feed into live KPI computations
