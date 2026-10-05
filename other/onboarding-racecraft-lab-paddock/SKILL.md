---
name: onboarding
description: "Skill for the Onboarding area of paddock. 41 symbols across 7 files."
---

# Onboarding

41 symbols | 7 files | Cohesion: 81%

## When to Use

- Working with code in `src/`
- Understanding how parseCompletedSteps, nextIncompleteStepIndex, shouldShowOnboarding work
- Modifying onboarding-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/components/onboarding/onboarding-wizard.tsx` | modeColors, OnboardingWizard, StepWelcome, StatusChip, StepInterfaceMode (+8) |
| `src/components/onboarding/runtime-setup-modal.tsx` | HermesSetup, syncOauthScrollState, resetOAuthState, fetchStatus, installHook (+3) |
| `src/app/api/onboarding/route.ts` | scopedOnboardingKey, getOnboardingSetting, setOnboardingSetting, readUserOnboardingSetting, writeUserOnboardingSetting (+2) |
| `src/lib/onboarding-state.ts` | parseCompletedSteps, nextIncompleteStepIndex, shouldShowOnboarding, markStepCompleted |
| `src/components/onboarding/security-scan-card.tsx` | SecurityScanCard, copyFix, runScan, runFix |
| `src/lib/onboarding-flow.ts` | getWizardSteps, clampWizardStep, stepIdAt |
| `src/lib/onboarding-session.ts` | readOnboardingReplayFromStart, markOnboardingDismissedThisSession |

## Entry Points

Start here when exploring this area:

- **`parseCompletedSteps`** (Function) — `src/lib/onboarding-state.ts:2`
- **`nextIncompleteStepIndex`** (Function) — `src/lib/onboarding-state.ts:24`
- **`shouldShowOnboarding`** (Function) — `src/lib/onboarding-state.ts:34`
- **`markStepCompleted`** (Function) — `src/lib/onboarding-state.ts:42`
- **`GET`** (Function) — `src/app/api/onboarding/route.ts:55`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `parseCompletedSteps` | Function | `src/lib/onboarding-state.ts` | 2 |
| `nextIncompleteStepIndex` | Function | `src/lib/onboarding-state.ts` | 24 |
| `shouldShowOnboarding` | Function | `src/lib/onboarding-state.ts` | 34 |
| `markStepCompleted` | Function | `src/lib/onboarding-state.ts` | 42 |
| `GET` | Function | `src/app/api/onboarding/route.ts` | 55 |
| `POST` | Function | `src/app/api/onboarding/route.ts` | 91 |
| `readOnboardingReplayFromStart` | Function | `src/lib/onboarding-session.ts` | 57 |
| `getWizardSteps` | Function | `src/lib/onboarding-flow.ts` | 26 |
| `OnboardingWizard` | Function | `src/components/onboarding/onboarding-wizard.tsx` | 66 |
| `markOnboardingDismissedThisSession` | Function | `src/lib/onboarding-session.ts` | 43 |
| `finish` | Function | `src/components/onboarding/onboarding-wizard.tsx` | 171 |
| `skip` | Function | `src/components/onboarding/onboarding-wizard.tsx` | 185 |
| `onKeyDown` | Function | `src/components/onboarding/onboarding-wizard.tsx` | 219 |
| `clampWizardStep` | Function | `src/lib/onboarding-flow.ts` | 30 |
| `stepIdAt` | Function | `src/lib/onboarding-flow.ts` | 37 |
| `completeStep` | Function | `src/components/onboarding/onboarding-wizard.tsx` | 163 |
| `goNext` | Function | `src/components/onboarding/onboarding-wizard.tsx` | 196 |
| `SecurityScanCard` | Function | `src/components/onboarding/security-scan-card.tsx` | 84 |
| `copyFix` | Function | `src/components/onboarding/security-scan-card.tsx` | 101 |
| `runScan` | Function | `src/components/onboarding/security-scan-card.tsx` | 119 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Panels | 11 calls |
| [id] | 4 calls |

## How to Explore

1. `gitnexus_context({name: "parseCompletedSteps"})` — see callers and callees
2. `gitnexus_query({query: "onboarding"})` — find related execution flows
3. Read key files listed above for implementation details
