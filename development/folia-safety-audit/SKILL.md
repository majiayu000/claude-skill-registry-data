---
name: folia-safety-audit
description: Systematic audit of Bukkit/Paper plugin code for Folia (regionized threading) safety — region ownership of entity access, scheduler selection, start/cancel races on scheduled tasks, safe publication of shared state, and off-thread Bukkit API calls. Use when adding folia-supported:true to a plugin, reviewing or debugging a plugin that already claims Folia support, investigating Folia-only crashes/IllegalStateExceptions, or whenever teleport/countdown/scheduler code is touched in a Folia-capable plugin.
---

# Folia thread-safety audit

Folia has no main thread: the world is split into regions, each ticked by its own thread, and
every entity is *owned* by exactly one region at a time. Code that was "obviously fine" on
Paper crashes or silently corrupts on Folia. This audit is a grep-driven pass over the five
failure classes, ordered by how often they produce real bugs.

**Mindset:** for every line, ask *"which thread runs this, and who owns the data it touches?"*
The answer must never be "whichever thread happened to call it".

## Class 1 — Cross-region entity access (the big one)

Any read/write of entity state is legal only on the owning region's thread: `.location`,
`.teleport()`, `.health`, inventory, `.showTitle`-with-position, velocity, etc.

Audit steps:
1. Grep every `.location` / `getLocation()` — for each, determine whose thread runs it.
   **A command handler runs on the *sender's* region thread; any other player it touches
   (target of /tpa, /msg, /heal) may be in another region.** This is the most common bug.
2. Watch for *hidden* location reads: `player.playSound(player.location, …)` reads location —
   use the entity-emitter overload `player.playSound(player, sound, vol, pitch)`.
   Same for particle/effect helpers that take a `Location` derived from another player.
3. Fix pattern: hop to the owner — `entity.getScheduler().run(plugin, task, retiredCallback)` —
   and snapshot what you need there (`location.clone()`), then continue.
4. Safe from any thread (don't "fix" these): Adventure `sendMessage`/`showTitle`/action bar;
   `Bukkit.getPlayer(uuid)` lookup itself; reading immutable data (name, UUID);
   `teleportAsync(...)` invocation (it handles the cross-region hop internally).

## Class 2 — Scheduler selection

There is no `BukkitScheduler` main thread on Folia. Every scheduled task must pick the right
scheduler; grep all scheduling calls and classify:

| Work | Correct Folia scheduler |
|---|---|
| Touches one entity | `entity.getScheduler()` — also auto-stops when the entity retires |
| Global bookkeeping (shared maps, broadcasts) | `GlobalRegionScheduler` |
| A specific block/location | `RegionScheduler` (at that location) |
| I/O, HTTP, heavy compute | `AsyncScheduler` — never a region thread |

Red flags: `Bukkit.getScheduler()` anywhere in a Folia code path; `runTaskLater` for
entity-related delays (use the entity scheduler so the task dies with the entity);
**blocking I/O in `onEnable`** (stalls startup on every platform — always async).

## Class 3 — Start/cancel races on scheduled tasks

Paper's single main thread serializes "start countdown" and "cancel countdown" for free.
On Folia they can run on different region threads *simultaneously*. Audit any
state-machine-with-a-task pattern (countdowns, warmups, combat tags, timed abilities):

1. **Registration gap** — between `stateMap.put(id, data)` and `taskMap.put(id, task)`,
   a cancel from another thread finds no task handle: the state is gone but the task ticks
   on ("ghost task") and completes an action that was cancelled.
2. Fixes, in order of strength:
   - **Serialize on the owner**: dispatch the entire start sequence to the entity's scheduler,
     so it can't interleave with that entity's events (move-cancel etc.).
   - **Stale-task guard**: first thing each tick, verify identity —
     `if (stateMap.get(id) !== myData) { task.cancel(); return; }`. Cancel *the running task
     itself* via its own handle/parameter; do NOT remove from the task map blindly (the map
     may already hold a *newer* task you'd be killing).
3. Check `runAtFixedRate` return values: entity schedulers return **null for retired
   entities** — handle it or you leak the state entry forever.

## Class 4 — Safe publication of shared state

With many threads, "it's just a field" stops working:

- [ ] Config values written by a reload command and read from other threads → `@Volatile`.
- [ ] Cached objects rebuilt on reload (parsed messages, settings snapshots) → `@Volatile`
      reference swap of an immutable object. Never mutate a shared object in place.
- [ ] All shared collections → `ConcurrentHashMap` (its weakly-consistent iterators are safe
      to remove from while another thread iterates). Key by **UUID, never `Player`**.
- [ ] `computeIfAbsent` caches: never cache a *failed* lookup (e.g. "Unknown" for an offline
      player) — if the cleanup hook already ran for that player, the poison entry leaks forever.
- [ ] `FileConfiguration` is not thread-safe: metric callbacks, executor jobs, and async hooks
      must read cached volatile fields, never `plugin.config`.

## Class 5 — Off-thread Bukkit API calls

Executor/async code must be Bukkit-free. Grep executor and async-scheduler lambdas for
`Bukkit.`, `player.hasPermission`, world access. Fix patterns:
- **Snapshot at creation**: capture permission-derived booleans and names on the command
  thread, store them in the state object (the sweep then needs no Bukkit calls).
- **Compute-then-dispatch**: do the pure computation off-thread, then hand results to the
  global region scheduler (Folia) / main thread (Paper) for the Bukkit-touching part.

## Runtime verification

Static review is necessary but not sufficient — the races need distance:

1. Folia only spins up separate region threads when players are **far apart** (thousands of
   blocks / different dimensions). Two players at spawn share a thread and hide every bug.
2. Test the cross-region versions of core flows: command sender and affected player in
   different regions; cancel-triggering action (movement, damage) fired at the exact moment
   an action starts.
3. Folia fails loudly (thread-check `IllegalStateException`s) for guarded accessors, but
   races and unsafe publication fail *silently* — they need the adversarial scenarios above,
   not just "it didn't crash".

A clean Paper run tells you nothing about any of this. If the plugin declares
`folia-supported: true`, a live Folia pass belongs in the release checklist.
