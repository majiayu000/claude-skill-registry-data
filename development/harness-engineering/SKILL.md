---
name: harness-engineering
description: >-
  Refactor a repo's watchdogs, drift checkers or cron scripts into self-contained modules and a thin
  runner. When maintenance scripts sprawl or checks multiply, consolidate duplicate machinery and
  tie each check to an owner decision. Not for agent-harness-settings-parity.
metadata:
  revision: "6"
  areas: "software-development"
  targets: "runtime-agnostic"
  summary: "restructure and design harness scripts: self-containment, obligations bound to owner decisions, pure checks plus one thin runner, net-negative line budget"
  summary_zh: "重构与设计 harness 脚本：自包含、检查绑定 owner 决策、纯函数检查加薄 runner、净减行数"
  kind: "entry"
---

# Harness Engineering

Redesign a repository's scheduled checks or operational control plane around real consumers.
Keep it self-contained: reuse modules within the repository, without creating a runtime
dependency on another repository's harness. A domain pipeline is a tenant, not a drift gate.

## Inventory and decide

1. Inventory source roots, scheduled jobs and call sites. Count reachable code without caches,
   archives or rollback copies. Trace runtime path resolution, registrations and both import
   forms before calling a file dead or superseded; similar names and unused-looking symbols
   prove nothing. Measure actual code overlap before proposing deduplication.
2. Classify live jobs as drift checks, observability, domain pipelines or gated execution.
   Read-path checks, write gates and a single delivery path serve the same drift-control goal;
   observability delivers findings.
3. For each check, record its evidence, the owner decision it can change, and keep/drop/move.
   Propose retirement when no decision depends on it. Move only to a confirmed consumer.
   Compare declarations to live state; zero use, newer upstream HEAD and prose counts are not
   proof of drift. Get owner approval for removals and schedule changes.

## Design and land

4. Keep checks pure: `(declarations, live_state) -> findings`. Read-only adapters obtain state;
   one bounded runner owns cache, delivery, TTL and deduplication by stable identity/severity.
   Register `intent_ref`, `decision` and `ttl`; validate at load time. Notification state must
   rebuild from zero. Trace actual I/O before trusting check/dry-run/JSON flags. Keep repair,
   installs and destructive maintenance outside detectors. Preserve independent execution,
   inputs and verdict ownership for producer/verifier pairs.
5. Replace reachable code on a net-negative line budget. Stage replacement and failure
   fixtures, then switch approved callers and schedules together without dual effects or
   coverage gaps. Keep rollback artifacts, with timestamped backups for files outside Git.
   Roll back affected definitions, not shared-state snapshots.
6. Prove the healthy path is silent and injected failures reject rather than report success.
   Run the repository's documented gates and check that test discovery did not lose cases.
   Before first authorized destructive retention, prove on real paths that a no-op run selects
   only the exact prefix and completion marker and deletes nothing; fail closed if no complete
   generation exists. Verify actual wiring with an approved end-to-end run on a maintenance
   surface; have an independent reader verify the artifact. Report first scheduled proof
   separately if pending. Do not invent a soak period or repeated approval gate.

For large extractions or failures involving commit gates, test discovery or draft promotion,
see [2026-11-21 implementation notes](references/2026-11-21-implementation-notes.md).
