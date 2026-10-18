---
name: roblox-analytics-instrumentation
description: Plan Roblox analytics instrumentation and event logging. Use for retention funnels, first-action timing, tutorial drop-off, economy events, monetization conversion, session milestones, progression analytics, A/B test planning, and live game KPI review.
---

# Roblox Analytics Instrumentation

## Goal

Measure whether the game is fun, understandable, and profitable. Instrument the core loop before optimizing it.

## Core Events

Track:

- Session start, spawn complete, and first playable action.
- Tutorial step shown, completed, skipped, or abandoned.
- Core loop start, success, fail, and reward claim.
- Currency earned, spent, purchased, and sunk.
- Upgrade viewed, purchased, unaffordable, and equipped.
- Quest accepted, progressed, completed, abandoned, and claimed.
- Social invite, party join, group join, trade started, trade completed.
- Shop opened, product viewed, purchase attempted, purchase completed.
- Death, retry, teleport, zone unlock, level up, prestige, and churn-risk exits.

## Funnel Checks

Prioritize:

- First action within 10-30 seconds.
- First reward within the first loop.
- First upgrade or meaningful progress in session one.
- Day 1, Day 3, and Day 7 return hooks.
- Mobile-specific control or UI friction.

## Event Design

- Use stable event names and versioned payloads.
- Include player segment, platform, session age, current zone, level, and economy state when useful.
- Avoid sending personally sensitive or noisy data.
- Log server-authoritative economy and purchase events from the server.
- Keep high-frequency events sampled or aggregated.

## Output

Return:

- KPI goals.
- Event list and payload fields.
- Funnel questions each event answers.
- Server/client ownership.
- Validation plan after implementation.

## Next

Act on what the data shows: tune with `roblox-economy-balancing` or `roblox-retention-monetization`, and schedule the follow-up work with `roblox-liveops-roadmap`.

