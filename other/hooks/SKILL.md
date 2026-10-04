---
name: hooks
description: "Skill for the Hooks area of Securacy. 16 symbols across 6 files."
---

# Hooks

16 symbols | 6 files | Cohesion: 73%

## When to Use

- Working with code in `securacyfrontend/`
- Understanding how getSecurityControlsOptions, startQuestion, getProgress work
- Modifying hooks-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `securacyfrontend/hooks/use-questionnaire.ts` | getSecurityControlsOptions, startQuestion, getProgress, getSummary, getDomainSpecificOptions (+3) |
| `securacyfrontend/services/privacyquestions.ts` | respondPrivacyQuestion, getPrivacyQuestionnaireProgress, getPrivacyQuestionnaireSummary |
| `securacyfrontend/lib/questions.ts` | getQuestionnaireProgress, getQuestionnaireSummary |
| `securacyfrontend/lib/api_call_config.ts` | apiCallGet |
| `securacyfrontend/context/LoadedThreatContext.tsx` | LoadedThreatProvider |
| `securacyfrontend/app/home/(bots)/privacy/page.tsx` | handleNextPrivacyQuestion |

## Entry Points

Start here when exploring this area:

- **`getSecurityControlsOptions`** (Function) — `securacyfrontend/hooks/use-questionnaire.ts:39`
- **`startQuestion`** (Function) — `securacyfrontend/hooks/use-questionnaire.ts:96`
- **`getProgress`** (Function) — `securacyfrontend/hooks/use-questionnaire.ts:306`
- **`getSummary`** (Function) — `securacyfrontend/hooks/use-questionnaire.ts:337`
- **`getQuestionnaireProgress`** (Function) — `securacyfrontend/lib/questions.ts:510`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `getSecurityControlsOptions` | Function | `securacyfrontend/hooks/use-questionnaire.ts` | 39 |
| `startQuestion` | Function | `securacyfrontend/hooks/use-questionnaire.ts` | 96 |
| `getProgress` | Function | `securacyfrontend/hooks/use-questionnaire.ts` | 306 |
| `getSummary` | Function | `securacyfrontend/hooks/use-questionnaire.ts` | 337 |
| `getQuestionnaireProgress` | Function | `securacyfrontend/lib/questions.ts` | 510 |
| `getQuestionnaireSummary` | Function | `securacyfrontend/lib/questions.ts` | 586 |
| `apiCallGet` | Function | `securacyfrontend/lib/api_call_config.ts` | 158 |
| `respondPrivacyQuestion` | Function | `securacyfrontend/services/privacyquestions.ts` | 88 |
| `getPrivacyQuestionnaireProgress` | Function | `securacyfrontend/services/privacyquestions.ts` | 217 |
| `getPrivacyQuestionnaireSummary` | Function | `securacyfrontend/services/privacyquestions.ts` | 293 |
| `LoadedThreatProvider` | Function | `securacyfrontend/context/LoadedThreatContext.tsx` | 67 |
| `handleNextPrivacyQuestion` | Function | `securacyfrontend/app/home/(bots)/privacy/page.tsx` | 857 |
| `getDomainSpecificOptions` | Function | `securacyfrontend/hooks/use-questionnaire.ts` | 53 |
| `toTitleCase` | Function | `securacyfrontend/hooks/use-questionnaire.ts` | 69 |
| `getDomainFromResponse` | Function | `securacyfrontend/hooks/use-questionnaire.ts` | 76 |
| `respondQuestion` | Function | `securacyfrontend/hooks/use-questionnaire.ts` | 117 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `PrivacyBot → DecodeJwt` | cross_community | 8 |
| `AppsecBot → DecodeJwt` | cross_community | 8 |
| `OnboardingPage → DecodeJwt` | cross_community | 7 |
| `HandleNextQuestion → DecodeJwt` | cross_community | 7 |
| `HandleNextQuestion → DecodeJwt` | cross_community | 7 |
| `HandleNextPrivacyQuestion → DecodeJwt` | cross_community | 6 |
| `SubscriptionPanel → DecodeJwt` | cross_community | 6 |
| `AppSidebar → DecodeJwt` | cross_community | 6 |
| `UsageSection → DecodeJwt` | cross_community | 6 |
| `RespondQuestion → DecodeJwt` | cross_community | 6 |

## Connected Areas

| Area | Connections |
|------|-------------|
| _components | 2 calls |

## How to Explore

1. `gitnexus_context({name: "getSecurityControlsOptions"})` — see callers and callees
2. `gitnexus_query({query: "hooks"})` — find related execution flows
3. Read key files listed above for implementation details
