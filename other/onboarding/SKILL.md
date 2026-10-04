---
name: onboarding
description: "Skill for the Onboarding area of Securacy. 4 symbols across 2 files."
---

# Onboarding

4 symbols | 2 files | Cohesion: 67%

## When to Use

- Working with code in `securacyfrontend/`
- Understanding how fetchUser, OnboardingPage, loadProfile work
- Modifying onboarding-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `securacyfrontend/app/onboarding/page.tsx` | hasChanges, OnboardingPage, loadProfile |
| `securacyfrontend/services/userService.ts` | fetchUser |

## Entry Points

Start here when exploring this area:

- **`fetchUser`** (Function) — `securacyfrontend/services/userService.ts:61`
- **`OnboardingPage`** (Function) — `securacyfrontend/app/onboarding/page.tsx:114`
- **`loadProfile`** (Function) — `securacyfrontend/app/onboarding/page.tsx:145`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `fetchUser` | Function | `securacyfrontend/services/userService.ts` | 61 |
| `OnboardingPage` | Function | `securacyfrontend/app/onboarding/page.tsx` | 114 |
| `loadProfile` | Function | `securacyfrontend/app/onboarding/page.tsx` | 145 |
| `hasChanges` | Function | `securacyfrontend/app/onboarding/page.tsx` | 44 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `OnboardingPage → DecodeJwt` | cross_community | 7 |
| `Load → DecodeJwt` | cross_community | 6 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Hooks | 1 calls |
| Context | 1 calls |

## How to Explore

1. `gitnexus_context({name: "fetchUser"})` — see callers and callees
2. `gitnexus_query({query: "onboarding"})` — find related execution flows
3. Read key files listed above for implementation details
