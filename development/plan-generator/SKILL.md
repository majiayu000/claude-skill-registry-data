---
name: plan-generator
description: Generates 14–21 day running plans tailored to onboarding data and recent performance.
metadata:
  short-description: Drafts personalized training blocks with safe load progression and rationale.
---

## When Codex should use it
- After onboarding completion or goal updates.
- When the user requests a new plan or calendar export.

## Invocation guidance
1. Load shared contracts from `_index/references/contracts.md`.
2. Inputs must include `UserProfile`, `TrainingHistory`, and optional `RecentRunTelemetry[]`.
3. Enforce rest distribution and load caps from deterministic rules (`v0/lib/plan-complexity-engine.ts`, `v0/lib/periodization.ts`).
4. Return JSON matching `Plan` + `rationale`.

## Input schema (JSON)
```ts
{
  "profile": UserProfile,
  "trainingHistory": TrainingHistory,
  "startDate": "2025-01-01",
  "preferences": { "indoorOk": true, "rookieChallenge": true }
}
```

## Output schema (JSON)
```ts
Plan & { rationale: string; safetyFlags?: SafetyFlag[] }
```

## Integration points
- API: `v0/app/api/generate-plan/route.ts`
- Logic: `v0/lib/planGenerator.ts`, `v0/lib/plan-templates.ts`
- UI: Today and Plan screens (Dexie data via `v0/lib/db.ts`)

## Safety & guardrails
- No medical diagnosis; if pain/dizziness flags are present, reduce load and advise consulting a professional.
- Hard-cap weekly volume deltas via `plan-complexity-engine.ts`.
- Emit `SafetyFlag` for load spikes or missing critical data.

## Telemetry
- Emit `ai_skill_invoked` and `ai_plan_generated` with `plan_version`, `fallback_used`, `safety_flags`.
