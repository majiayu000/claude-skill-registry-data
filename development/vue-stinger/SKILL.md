---
name: vue-stinger
description: "Build Vue application slices with SFCs, composables, typed props/events, state, forms, routing and delivery evidence. Use after Vue is chosen; hand Nuxt SSR to its selected owner."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; application checks require the existing Vue toolchain."
metadata:
  hive-tier: specialist
  hive-drone: vue-wasp-drone
  domain: vue-application
---

# Vue Stinger

## Purpose
Implement the assigned Vue application slice using its accepted toolchain, backend contract and design direction. Deliver owned SFCs, composables, client routes/forms/state integration and honest application evidence. Read [README](README.md) before work.

## When to use
Use when Vue is selected and an application, feature slice or Vue component integration needs implementation or repair. This skill owns Vue-native reactivity and application structure.

## When not to use
Framework choice goes to Web Stack Selection; React implementation stays with React. Nuxt SSR/server routing/hydration needs the selected SSR owner. Provider configuration, backend contracts, security acceptance and design direction retain their owners. Missing owners are gaps, never fabricated substitutes.

## Procedure
1. Read all skill context, the assignment, active ownership, installed toolchain and accepted PRODUCT.md/DESIGN.md/surface brief. Follow [architecture](guides/01-shape-application.md).
2. Implement owned SFC/composable boundaries through [components](guides/02-build-components.md): typed props/events, pure computed values, synchronous watchers, cleanup and safe data.
3. Connect the real accepted routes/forms/state and API through [flow](guides/03-connect-flow.md). No implicit dependency installs, provider calls, credentials or settings changes.
4. Follow [verification](guides/04-prove-delivery.md), [negative cases](references/examples/negative-cases.md) and [evidence template](references/templates/delivery-evidence.md). Preserve separate static/pure/component/browser/provider proof.
5. Report exact changed files and PASS/FAIL/NOT_RUN results. Resolve medium-or-higher findings in ordered Ship Gate reviews before requesting separately required commit/push authorization.

## References map
[Templates](references/templates/README.md), [component spec](references/templates/RecordForm.spec.ts), [digest](references/research/distilled-vue.md), ledger, [paired Drone](../../agents/vue-wasp-drone.md), [envelope checker](scripts/check-envelope.py).

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Related-owner resolution](README.md#related-owners-and-host-support): resolve selected Impeccable, framework/backend/security owners through trusted Core and the source catalog.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.
