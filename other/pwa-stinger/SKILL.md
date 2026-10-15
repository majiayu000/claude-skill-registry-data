---
name: "pwa-stinger"
description: "Implement browser PWA manifest, service-worker lifecycle and bounded public offline assets. Use for scoped PWA/offline changes. Read README.md for the guide map."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; real app and supported browser needed for runtime qualification."
metadata:
  hive-tier: specialist
  hive-drone: pwa-wasp-drone
  pair-drone: pwa-wasp-drone
  domain: pwa
  mode: development-focused
---

# PWA browser offline implementation

## Purpose

Implement approved browser PWA/offline behavior with an exact public static asset policy, generic offline fallback and tested update/install lifecycle. Preserve accepted app, authentication and design contracts; report actual browser proof and unrun gaps.

## When to use

- Add a browser PWA manifest and scoped service-worker integration.
- Implement a bounded public offline fallback and approved static cache.
- Fix PWA update/lifecycle or private-request cache exclusions.

## When not to use

- Framework selection, UI direction, native mobile application delivery or provider setup: selected owners retain those domains.
- Offline private data or a mutation queue without accepted authorization/idempotency/sync/conflict contracts.
- Security, privacy, performance or installability certification from source templates.

## Procedure

1. Read [README.md](README.md) and [boundaries](guides/01-define-offline-and-install-boundaries.md). Inspect the real app/worker/manifest and fill the accepted offline contract, secure-context/browser matrix and authorized files.
2. Follow [public cache and private bypass](guides/02-implement-public-cache-and-private-bypass.md). Use reviewed static asset hashes, omit credentials for precache, bypass private requests and keep mutation methods network-only.
3. Follow [qualification](guides/03-qualify-lifecycle-browser-and-handoff.md). Check actual worker install/control/update behavior, cache contents, browser installation, disconnected fallback, logout/account change and storage limits.
4. Report source/pure fixtures separately from browser/app/provider/native proof. Missing target/dependencies means NOT_RUN. Hand independent review to Security then Quality; parent owns Repository Health and authorized release.

## References map

- [Digest](references/research/distilled-pwa.md), ledger, exact locators: official grounding.
- [Contract](references/templates/offline-contract.md), [templates and fixture map](README.md): bounded fail-closed starters and evidence limits.
- [Negative cases](references/examples/negative-cases.md): disallowed unsafe substitutions.
- [Paired Drone](../../agents/pwa-wasp-drone.md): scope and delivery contract.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Related-owner resolution](README.md#related-owners-and-host-support) - Resolve framework, design, auth/data, provider and review owners.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.
