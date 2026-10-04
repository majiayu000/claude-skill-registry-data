---
name: work-loop
type: Skill
title: work-loop — operate the durable autonomous task fleet
description: "Operating guide for the durable Autonomous Work Loop task fleet. Use when adding work to, coordinating, or working an Autonomous Work Loop campaign, or when calling the work_loop MCP tool."
tags: [automation, codex, queue, qa, agents]
timestamp: 2026-08-30T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/work-loop/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Work Loop

Canonical contract:
`/Users/armanisadeghi/code/common-docs/systems/architecture/work-loop/STATE.md`.

## Coordinator

1. Call `work_loop(action="status")`; database state is truth.
2. Reclaiming is automatic on claim. Fill every free slot, up to three workers,
   by calling `claim` with a unique stable holder and giving each worker the
   returned contract unchanged.
   When dispatching a known follow-up such as an independent verifier, pass its
   exact `canonical_key` to `claim` and assert the returned key and role before
   dispatch. A mismatch is a coordinator error: release it without work and do
   not substitute another pending item.
3. Wait for the first worker. Settle through `complete`, `retry`, or `defer`,
   then fill the slot again. Continue while claimable work exists.
4. Add newly supplied tasks through `add_items`; stable keys make re-adding safe.
   When a new contract/rule version replaces an older claimable key, atomically
   claim the exact older key and settle it with `supersede`, naming the existing
   replacement key and reason. Never leave both versions claimable, reset the
   old attempt count, or disguise supersession as human deferral.
5. Never spend a work turn repeating inventory or producing a report while a
   claimable item exists. Coordinator success is queue advancement.

## Worker

Read the entire claimed contract. Claim ownership is permission to perform all
ordinary reversible work inside its scope: inspect, reproduce, edit, test,
commit, push, deploy where the repo contract allows, authenticate with the
preauthorized test identity, repair fixtures/tooling, and verify live.

Use the isolated in-app Browser for application testing. Never use the user's
browser. Close every tab you create.

On a shared Browser host, Browser ownership is valid only while the same holder
owns an `in_progress` Work Loop lease. Settling, releasing, losing, or
interrupting that claim releases the Browser lane immediately; a pending,
deferred, failed, or succeeded item can never reserve it. The coordinator must
reconcile durable claim state before every Browser handoff. Record tab ids/URLs
created under each lease. If a worker is interrupted or cannot clean up, the
coordinator closes those recorded campaign tabs before the next grant, without
touching tabs that predated the campaign.

The Browser and the machine-wide managed preview are one exclusive live lane.
The same active claim holder owns both or owns neither. A static/code worker may
prepare a clean worktree but cannot start or retain the managed preview. Before
each grant, stop/release the prior campaign preview, start only the repository's
canonical managed preview from the recorded checkout, and record its checkout
SHA/root beside the tab inventory. Parallel/raw dev servers are not evidence.

**There are no routine blockers.** Missing login state, stale tokens, broken
preview, missing fixtures, failing tests, server/tool failures, deployment lag,
unfamiliar code, and dirty unrelated files are problems to investigate and
repair or work around. A bug found during QA becomes part of the claimed work:
fix the root cause and retest it. Do not return a diagnosis or admin report as
completion.

Heartbeat before half the lease elapses and around any long test/build/deploy.
If the heartbeat says ownership was lost, stop writing and do not claim success.

Complete only with concrete evidence. The service will create the independent
verifier. A verifier starts from fresh state, assumes the work is wrong, and
returns `passed` or `rejected`; rejection automatically creates repair work.
The coordinator claims that verifier by its exact returned follow-up key; queue
priority alone is never identity.

`defer` is legal only for one named human-only boundary from the contract. It
parks that item; the coordinator immediately continues other work. Never turn a
single deferred item into a stopped campaign.

## Adding items

One item is one independently claimable outcome. Include exact target,
objective, source refs, required tools, verification checks, evidence, priority,
and any true dependencies. Put general campaign rules in the campaign default;
put exceptions and special authority in that line item's engagement contract.

Use lower priority numbers for active regressions/retests, 100 for ordinary
backlog, and higher numbers for opportunistic work. Do not create one schedule
per item; one coordinator drains the shared campaign.
