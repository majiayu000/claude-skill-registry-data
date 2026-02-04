---
name: plan-adjuster
description: Recomputes upcoming workouts based on recent runs and user feedback. Use when recent performance deviates from plan, user provides negative feedback, or recovery signals indicate adjustment needed with deterministic safety caps.
metadata:
  short-description: Adaptive adjustment of future sessions with change logs and recovery tips.
---

## When Claude should use this skill
- Nightly job or immediately after a run is logged
- When the user reports fatigue/injury or requests easier/harder weeks
- When performance data indicates plan adjustment is needed

## Invocation guidance
1. Load `Plan`, `Workout`, `TrainingHistory`, and `RecentRunTelemetry[]`.
2. Apply deterministic ceilings from `v0/lib/planAdaptationEngine.ts` and `v0/lib/plan-complexity-engine.ts` before calling the model.
3. Return `Adjustment[]`, optional `RecoveryRecommendation`, and `confidence`.

## Input schema (JSON)
```ts
{
  "profile": UserProfile,
  "currentPlan": Plan,
  "trainingHistory": TrainingHistory,
  "feedback": { "rpeTrend"?: number, "soreness"?: string, "sleepQuality"?: string }
}
```

## Output schema (JSON)
```ts
{
  "appliedAt": string,
  "updates": Adjustment[],
  "recovery"?: RecoveryRecommendation,
  "confidence": "low" | "medium" | "high",
  "safetyFlags"?: SafetyFlag[]
}
```

## Integration points
- API: `v0/app/api/plan/adjust` (to add), or chat-triggered adjustments.
- Logic: `v0/lib/planAdjustmentService.ts`, `v0/lib/planAdaptationEngine.ts`.
- UI: Plan/Today screens (badge adjusted sessions) and notifications via `v0/lib/email.ts`.

## Safety & guardrails
- Never rewrite completed history; adjust only future sessions.
- If fatigue/injury signals present, lower intensity/volume and consider rest-day insertion.
- Emit `SafetyFlag` on unsafe load proposals; clamp to deterministic caps.

## Telemetry
- Emit `ai_skill_invoked` and `ai_adjustment_applied` with `adjustments_count`, `confidence`, `safety_flags`.
