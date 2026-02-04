---
name: plan-generator
description: Generates 14–21 day personalized running training plans with safe load progression. Use when user completes onboarding, requests a new plan, updates their running goals, or wants to export a training calendar.
metadata:
  short-description: Drafts personalized training blocks with safe load progression and rationale.
  agent: cursor
---

## When Cursor should use this skill
- After onboarding completion or goal updates
- When the user requests a new plan or calendar export
- When user asks to create/regenerate/export their training schedule
- When implementing plan generation features or debugging plan creation

## Invocation guidance
1. Load shared contracts from `running-coach-index/references/contracts.md`.
2. Inputs must include `UserProfile`, `TrainingHistory`, and optional `RecentRunTelemetry[]`.
3. Enforce rest distribution and load caps from deterministic rules (`v0/lib/plan-complexity-engine.ts`, `v0/lib/periodization.ts`).
4. Return JSON matching `Plan` + `rationale`.
5. Always validate against safety thresholds before returning plan.

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
- **API**: `v0/app/api/generate-plan/route.ts` - Main plan generation endpoint
- **Logic**: 
  - `v0/lib/planGenerator.ts` - Core plan generation logic
  - `v0/lib/plan-templates.ts` - Fallback template plans
  - `v0/lib/periodization.ts` - Training load periodization
  - `v0/lib/plan-complexity-engine.ts` - Safety caps and thresholds
- **UI**: Today and Plan screens (Dexie data via `v0/lib/db.ts`)
- **Database**: Plans stored in IndexedDB `plans` table with workouts in `workouts` table

## Safety & guardrails
- No medical diagnosis; if pain/dizziness flags are present, reduce load and advise consulting a professional.
- Hard-cap weekly volume deltas via `plan-complexity-engine.ts`:
  - Weekly volume: max +20-30% increase
  - Long run: max +10-15% increase
  - Beginner cap: 30km/week maximum
- Emit `SafetyFlag` for load spikes or missing critical data.
- Always include at least one rest day per week.
- Progressive loading: easier first week to establish baseline.

## Deterministic rules to enforce
- **Rest distribution**: minimum 1 rest day per week, prefer 2 for beginners
- **Long run placement**: Sunday or Saturday preferred
- **Easy run proportion**: 70-80% of weekly volume should be easy pace
- **Interval frequency**: max 2 hard sessions per week
- **Recovery time**: minimum 48h between hard sessions

## Telemetry
- Emit `ai_skill_invoked` and `ai_plan_generated` with:
  - `plan_version`
  - `fallback_used` (true if template was used instead of AI)
  - `safety_flags` (any warnings or caps applied)
  - `workouts_count`
  - `user_id` (hashed)
  - `latency_ms`

## Common edge cases
- **No training history**: Generate conservative beginner plan, emit `SafetyFlag` for `missing_data`
- **Inconsistent history**: Reduce volume target, add extra recovery
- **Injury flags**: Lower intensity, increase rest days, emit `SafetyFlag` for `injury_signal`
- **Race goal without date**: Request race date before generating plan
- **Unrealistic goal**: Adjust timeline or volume, explain rationale in plan

## Testing considerations
- Mock `UserProfile` with various experience levels
- Test with empty/sparse `TrainingHistory`
- Verify load caps are enforced
- Check SafetyFlag emission for edge cases
- Validate JSON schema compliance
- Test fallback to template plans when AI fails
