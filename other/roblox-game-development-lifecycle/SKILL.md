---
name: roblox-game-development-lifecycle
description: Orchestrate the full Roblox game development lifecycle. Use as the umbrella entrypoint for broad requests like create a Roblox game, build a new game, continue development, what should we do next, take this from idea to launch, make this game profitable, plan the roadmap, manage production, or maintain a live Roblox game. Routes to the right Roblox specialist skills by GDLC phase.
---

# Roblox Game Development Lifecycle

## Goal

Keep Roblox development from drifting. For broad game-development requests, identify the current lifecycle phase, enforce the next useful gate, and route to the right specialist skills.

## Lifecycle Phases

Use this order:

1. Market and player research.
2. Concept and core loop.
3. Prototype.
4. Vertical slice.
5. Production.
6. Internal QA and security.
7. Soft launch or private testing.
8. Polish and balance.
9. Publishing and launch.
10. Live ops.
11. Maintenance and growth.

Do not scale content until the core loop, mobile usability, save/security basics, and retention signals are credible.

## Session Start

For an existing Roblox place:

1. Read project instructions and `ROADMAP.md` when present.
2. Use `roblox-studio-workflow` to connect to Studio.
3. Check the first incomplete roadmap item.
4. If no roadmap exists, create or propose one with lifecycle phases and approval gates.
5. Resume from the earliest phase whose exit criteria are not met.

## Phase Routing

Use these specialist clusters:

- Market and player research: `roblox-game-ideas`, `roblox-genre-patterns`, `roblox-growth-marketing`, `roblox-publishing-discovery`.
- Concept and core loop: `roblox-game-ideas`, `roblox-retention-monetization`, `roblox-economy-balancing`, `roblox-game-ux`.
- Prototype: `roblox-studio-workflow`, `roblox-luau-architecture`, `roblox-ui-implementation`, `roblox-world-level-design`, `roblox-asset-pipeline`.
- Vertical slice: `roblox-game-ux`, `roblox-animation-audio-feedback`, `roblox-datastore-persistence`, `roblox-quest-progression-systems`, `roblox-social-systems`.
- Production: `roblox-luau-architecture`, `roblox-combat-systems`, `roblox-quest-progression-systems`, `roblox-social-systems`, `roblox-datastore-persistence`, `roblox-security-economy`, `roblox-asset-pipeline`, `roblox-world-level-design`.
- Internal QA and security: `roblox-playtest-qa`, `roblox-mobile-playtest`, `roblox-performance-optimization`, `roblox-debugging-bugfix`, `roblox-security-economy`, `roblox-creator-store-security-audit`, `roblox-policy-compliance`.
- Soft launch or private testing: `roblox-analytics-instrumentation`, `roblox-playtest-qa`, `roblox-mobile-playtest`, `roblox-release-operations`, `roblox-community-ops`.
- Polish and balance: `roblox-economy-balancing`, `roblox-animation-audio-feedback`, `roblox-game-ux`, `roblox-performance-optimization`, `roblox-code-maintenance-refactor`.
- Publishing and launch: `roblox-publishing-discovery`, `roblox-growth-marketing`, `roblox-policy-compliance`, `roblox-release-operations`.
- Live ops: `roblox-liveops-roadmap`, `roblox-analytics-instrumentation`, `roblox-community-ops`, `roblox-quest-progression-systems`, `roblox-monetization-optimization`.
- Maintenance and growth: `roblox-debugging-bugfix`, `roblox-code-maintenance-refactor`, `roblox-admin-tools-observability`, `roblox-community-ops`, `roblox-growth-marketing`, `roblox-monetization-optimization`.

## Exit Criteria

Before advancing phases, check:

- Research: audience, genre, differentiator, and success metrics are clear.
- Concept: first 30 seconds and core loop are written and testable.
- Prototype: core action, reward, and next goal work in Studio.
- Vertical slice: one small section feels representative of final quality.
- Production: major systems are implemented with server authority and save/load.
- QA/security: mobile, performance, console, purchases, DataStores, remotes, and Creator Store imports are checked.
- Soft launch: analytics events exist and tester feedback is triaged.
- Polish: top retention leaks and balance problems are addressed.
- Launch: store page, policy, release notes, growth plan, and rollback plan are ready.
- Live ops: update cadence, events, analytics review, and community loop are active.
- Maintenance: bug triage, refactors, admin tooling, and growth iteration continue.

## Roadmap Discipline

- Create or maintain `ROADMAP.md` as the single source of next work.
- Use `[ ]` for not started.
- Use `[~]` for built and tested but awaiting human approval.
- Use `[x]` only after implementation, testing/playtesting, and explicit human approval.
- Append completion dates only after approval.

## Default Output

For broad planning requests, return:

- Current lifecycle phase.
- Phase evidence or missing evidence.
- Next milestone.
- Specialist skills to use next.
- Acceptance criteria.
- Playtest or validation plan.
- Risks before moving to the next phase.

For implementation requests, act on the current phase instead of only describing the plan.

## Next

Route to the specialist skills for the current phase (listed above). For anything you are about to build, pass it through `roblox-to-prd` → `roblox-to-issues` → `roblox-triage` first so it lands one playtestable slice at a time instead of all at once.

