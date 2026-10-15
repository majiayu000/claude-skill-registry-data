---
name: nextjs-stinger
description: "Implement Next.js App Router features: server/client boundaries, reads, actions, handlers, private data, cache contracts and build/provider handoffs. Read README.md for guides."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; application execution needs compatible existing Next.js dependencies."
metadata:
  hive-tier: specialist
  hive-drone: nextjs-wasp-drone
  pair-drone: nextjs-wasp-drone
  domain: nextjs-implementation
  mode: development
---

# Next.js implementation

## Purpose

Implement a scoped App Router feature using the accepted backend and selected owners. Produce app code, explicit server/client and cache/private-data contracts, actual build/request evidence and a provider handoff. Read [README.md](README.md) first.

## When to use

- Build or change Next.js App Router pages, server reads, Server Actions or Route Handlers.
- Resolve framework rendering/cache/private-data behavior during implementation.
- Qualify a Next.js build and prepare its selected provider handoff.

## When not to use

- React-only component architecture: React owner. Visual design: Impeccable owner.
- Security auditing: existing NextJS Security plus Core Security. Pages Router migration: needs separately defined scope.
- Provider/account setup, credential entry, deployment or publishing without explicit authorization.

## Procedure

1. Read installed versions, router/config, ownership and accepted backend/auth contracts. Record boundaries in [the record](templates/boundary-record.md). Refresh official facts for that installed version.
2. Implement [server/client boundaries](guides/01-build-server-client-boundaries.md) and [reads/actions/routes](guides/02-implement-loads-actions-and-routes.md) only in assigned paths.
3. Declare and exercise [cache/private-data isolation](guides/03-isolate-cache-and-private-data.md). Keep identity verified at each entry and private reads uncached unless a reviewed cache contract says otherwise.
4. [Qualify build and handoff](guides/04-qualify-build-and-provider-handoff.md), using existing dependencies and actual production-mode requests. Mark unavailable proof NOT_RUN.
5. Review [negative cases](examples/negative-cases.md). Route independent Security then Quality and parent repository health. Approval precedes authorized commit/push and external effects.

## References map

- [Source digest](references/research/distillation.md): current official claims and version caveats.
- [Reference index](references/REFERENCE.md): bounded starter, validation and scope.
- [Paired Drone](../../agents/nextjs-wasp-drone.md): source delegation contract.
- [Starter](templates/starter/README.md): NOT_RUN adaptation sketch, not a complete app.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [React](../react-stinger/SKILL.md) - Component architecture and state ownership.
  - [Impeccable](../impeccable-stinger/SKILL.md) - Frontend visual design.
  - [Related-owner resolution](README.md#related-owners-and-host-support) - Selected auth/data/provider and independent security owners.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.
