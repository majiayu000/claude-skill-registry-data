---
name: "nuxt-stinger"
description: "Implement Nuxt apps, SSR/data integration, Nitro routes, request state and cache/auth boundaries. Use for accepted Nuxt builds or changes. Read README.md for the guide map."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; actual Nuxt app dependencies required for app verification."
metadata:
  hive-tier: specialist
  hive-drone: nuxt-wasp-drone
  pair-drone: nuxt-wasp-drone
  domain: nuxt
  mode: development-focused
---

# Nuxt implementation

## Purpose

Build or extend an authorized Nuxt app when its accepted rendering/content requirements justify Nuxt. Deliver scoped framework integration and actual acceptance evidence, preserving backend/auth/data contracts, Vue ownership and Impeccable direction.

## When to use

- Build a Nuxt app with an accepted framework choice.
- Implement Nuxt routing, SSR reads, useAsyncData/useFetch and hydration integration.
- Add a Nitro server endpoint, session adapter integration or bounded routeRules/cache policy.

## When not to use

- Choosing the framework: Web Stack Selection owns the decision.
- Vue component/reactivity architecture or design direction: Vue and Impeccable own those.
- Provider/auth/data protocol changes, CMS installation, native app work, security certification or release actions: selected owners retain those boundaries.

## Procedure

1. Read [README.md](README.md), [fit/boundaries](guides/01-fit-rendering-and-boundaries.md) and the actual app versions/config. Define accepted rendering/backend/session/DTO contracts and authorized files before changes.
2. Use [data/state](guides/02-data-state-and-hydration.md) for request isolation, keyed reads, hydration and principal-change clearing.
3. Use [server/auth/config/cache](guides/03-server-auth-config-and-cache.md) for validated Nitro endpoints, server permission checks, private config and no-private-cache defaults.
4. Follow [build/handoff](guides/04-build-qualify-and-handoff.md) and exercise actual project checks plus the negative cases. Report source/static evidence separately from app/provider/native proof, marking unmet prerequisites NOT_RUN.
5. Submit Security then independent Quality evidence; parent owns repository health and authorized release. Never infer commit/push, install, credential, settings or provider authority from this implementation request.

## References map

- [Digest](references/research/distilled-nuxt.md), ledger, claim locators: official grounding and version limits.
- [Rendering contract](references/templates/rendering-contract.md), [integration templates](README.md): bounded starters, not built app evidence.
- [Negative cases](references/examples/negative-cases.md): required rejection and acceptance boundaries.
- [Paired Drone](../../agents/nuxt-wasp-drone.md): scope and delivery contract.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Related-owner resolution](README.md#related-owners-and-host-support) - Resolve actual selected Vue, design, backend/auth/data, provider and independent review owners.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.
