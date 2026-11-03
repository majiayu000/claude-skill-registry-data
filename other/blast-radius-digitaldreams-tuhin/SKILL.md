---
name: blast-radius
description: >
  Trace the full impact of a proposed change or deletion before anything is edited. Use whenever
  the user says "blast radius", "possible impact", "what does this touch", "what breaks if",
  "is X orphaned", "safe to delete", "find interconnected classes", or asks to change a shared
  model, service, event, enum, or config value. Read-only: produces an impact table plus ranked
  solution options with a recommendation. Never applies the change itself. Required before any
  modification to code used by more than one feature.
---

# Blast Radius — Impact Analysis

You map everything a change touches, then hand the operator options. **No edits.** Evidence over guesses: every claim carries a `file:line`.

## Phase 1 — Pin the Target

State precisely what is changing: class, method, column, enum case, event, config key, view partial — and the nature of the change (signature, behavior, rename, deletion).

## Phase 2 — Sweep for Dependents

Grep and read; check every category, report "none" when empty:

1. **Direct callers** — imports, static calls, container resolutions, method calls.
2. **Events** — if the target fires or is fired by events: every producer and every listener.
3. **Jobs & schedulers** — dispatch sites, `Bus::chain`/`Bus::batch` membership, scheduler entries.
4. **Database** — migrations, model casts/fillable, factories, seeders touching affected columns.
5. **UI** — views, components, and JS reading the affected data or routes.
6. **Tests** — every test exercising the target; note which will break vs which protect the change.
7. **Config & env** — config keys, env variables, feature flags referencing the target.
8. **Serialized/stored references** — queued payloads, cached values, string-stored class names, static-analysis baselines (renames rot baselines).

## Phase 3 — Classify

Sort every hit into three buckets:

- **Breaks** — will error or misbehave if the change ships as-is.
- **Needs update** — keeps working but becomes wrong/stale (docs, seeders, tests, views).
- **Unaffected** — verified safe; say why in a few words.

## Orphan Mode

When asked "is X orphaned / safe to delete": prove zero live references across all Phase 2 categories before endorsing deletion. One live reference = not orphaned; show it. Include soft references (views, config, seeders, docs). Verdict is binary: **safe to delete** (with the reference-free proof) or **not orphaned** (with the list).

## Output Contract

1. **Target** — what changes, one line.
2. **Impact table** — dependent → category → bucket → `file:line`.
3. **Options** — 2–3 ways to make the change, each with effort and risk, ranked. Mark one **Recommended** and say why in one sentence.
4. **Test plan** — which existing tests gate the change; which new tests the winning option needs.

Stop there. Implementation is a separate, explicit request.
