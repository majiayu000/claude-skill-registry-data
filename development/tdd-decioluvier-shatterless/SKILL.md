---
name: tdd
description: >
  ShatterLess Technical Design Document — the repo's engineering law. Read for any
  code change. Obey it over generic Godot patterns and over the `godot` router
  skill. Covers: Godot 4.7 + Forward Plus + D3D12, GDScript-not-C# decision,
  Rapier3D + netfox addons, the NetworkTime/NetworkRollback/NetworkEvents
  autoloads, feature-folder repo layout, typing/naming conventions, and the
  determinism rules for P2P deterministic lockstep with rollback (no
  wall-clock, no un-seeded RNG, full state save/restore, simulation on the
  network tick). Trigger keywords: TDD, architecture, determinism, rollback,
  lockstep, netfox, RollbackSynchronizer, _rollback_tick, netcode, Rapier3D,
  GDScript, autoload, conventions, banned API.
---

Read the reference that matches the task before designing or implementing. This skill overrides anything here on implementation detail.

| Reference | Read it when |
|---|---|
| `references/01-architecture-and-stack.md` | Engine + language decision, addons, autoloads, repo layout, typing/naming conventions, build/run. |
| `references/02-determinism-and-netcode.md` | The determinism rules in full (tick, save/restore, banned wall-clock/RNG APIs, Rapier, floats) + the known-violations fix table. |