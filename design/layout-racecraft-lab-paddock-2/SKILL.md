---
name: layout
description: "Skill for the Layout area of paddock. 55 symbols across 15 files."
---

# Layout

55 symbols | 15 files | Cohesion: 74%

## When to Use

- Working with code in `src/`
- Understanding how getOnboardingSessionDecision, readOnboardingDismissedThisSession, markOnboardingReplayFromStart work
- Modifying layout-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/components/layout/header-bar.tsx` | HeaderBar, ModeBadge, Stat, NavigationLatencyStat, update (+9) |
| `src/components/layout/nav-rail.tsx` | tLabel, tGroup, translateItems, mergedGroups, NavRail (+7) |
| `src/lib/navigation-metrics.ts` | emitSample, completeNavigationTiming, getNavigationMetrics, navigationMetricEventName |
| `src/app/[[...panel]]/page.tsx` | Home, markStep, connectWithEnvFallback, connectWithPrimaryGateway |
| `src/lib/onboarding-session.ts` | getOnboardingSessionDecision, readOnboardingDismissedThisSession, markOnboardingReplayFromStart |
| `src/lib/browser-security.ts` | normalizeHostname, isLocalDashboardHost, shouldRedirectDashboardToHttps |
| `src/components/layout/live-feed.tsx` | LiveFeed, FeedItem, formatRelativeTime |
| `src/components/layout/workspace-switcher.tsx` | WorkspaceSwitcher, selectOption, onOptionKeyDown |
| `src/components/layout/openclaw-doctor-banner.tsx` | OpenClawDoctorBanner, loadDoctorStatus |
| `src/components/ui/digital-clock.tsx` | DigitalClock, update |

## Entry Points

Start here when exploring this area:

- **`getOnboardingSessionDecision`** (Function) — `src/lib/onboarding-session.ts:16`
- **`readOnboardingDismissedThisSession`** (Function) — `src/lib/onboarding-session.ts:34`
- **`markOnboardingReplayFromStart`** (Function) — `src/lib/onboarding-session.ts:66`
- **`completeNavigationTiming`** (Function) — `src/lib/navigation-metrics.ts:37`
- **`isLocalDashboardHost`** (Function) — `src/lib/browser-security.ts:4`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `getOnboardingSessionDecision` | Function | `src/lib/onboarding-session.ts` | 16 |
| `readOnboardingDismissedThisSession` | Function | `src/lib/onboarding-session.ts` | 34 |
| `markOnboardingReplayFromStart` | Function | `src/lib/onboarding-session.ts` | 66 |
| `completeNavigationTiming` | Function | `src/lib/navigation-metrics.ts` | 37 |
| `isLocalDashboardHost` | Function | `src/lib/browser-security.ts` | 4 |
| `shouldRedirectDashboardToHttps` | Function | `src/lib/browser-security.ts` | 14 |
| `UpdateBanner` | Function | `src/components/layout/update-banner.tsx` | 9 |
| `OpenClawUpdateBanner` | Function | `src/components/layout/openclaw-update-banner.tsx` | 9 |
| `OpenClawDoctorBanner` | Function | `src/components/layout/openclaw-doctor-banner.tsx` | 24 |
| `loadDoctorStatus` | Function | `src/components/layout/openclaw-doctor-banner.tsx` | 36 |
| `LiveFeed` | Function | `src/components/layout/live-feed.tsx` | 7 |
| `Home` | Function | `src/app/[[...panel]]/page.tsx` | 87 |
| `markStep` | Function | `src/app/[[...panel]]/page.tsx` | 134 |
| `connectWithEnvFallback` | Function | `src/app/[[...panel]]/page.tsx` | 180 |
| `connectWithPrimaryGateway` | Function | `src/app/[[...panel]]/page.tsx` | 196 |
| `getNavigationMetrics` | Function | `src/lib/navigation-metrics.ts` | 57 |
| `navigationMetricEventName` | Function | `src/lib/navigation-metrics.ts` | 83 |
| `extractWsHost` | Function | `src/lib/agent-card-helpers.ts` | 40 |
| `DigitalClock` | Function | `src/components/ui/digital-clock.tsx` | 4 |
| `update` | Function | `src/components/ui/digital-clock.tsx` | 8 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Home → Error` | cross_community | 4 |
| `Home → Warn` | cross_community | 4 |
| `Home → Dispatch` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Panels | 26 calls |
| Modals | 2 calls |
| Setup | 1 calls |
| Cluster_112 | 1 calls |
| Chat | 1 calls |
| Onboarding | 1 calls |

## How to Explore

1. `gitnexus_context({name: "getOnboardingSessionDecision"})` — see callers and callees
2. `gitnexus_query({query: "layout"})` — find related execution flows
3. Read key files listed above for implementation details
