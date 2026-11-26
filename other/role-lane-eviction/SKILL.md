---
name: role-lane-eviction
description: >-
  Remove an entire scratch/role lane from a width-pinned reversible circuit by
  rewriting every site that touches it with bespoke per-context constructions,
  instead of pooling the role. From jackylee0424's ecdsa.fail Q658 row
  (a6098537, Nov 2026): the third scalar lane of a 659 tree evicted on all four
  traversals, paying +8.8% T for the -1 qubit width record.
whenToUse: A width cut is blocked because a role/scratch lane is shared everywhere and every cheap knob is dead; per-site knobs measure dead (pool liveness is simultaneous) but a per-context rewrite program is affordable; you accept a T-for-width trade
---

# Zwangsrüümig (role-lane-eviction)

When a census says "the role pool is live everywhere, no knob frees it" (the dead-knob
wall), the remaining move is to stop pooling: rewrite every *site* that uses the lane
with a construction that uses lanes provably free *at that point*, then drop the lane
from the allocator (`alloc_n(3) -> alloc_n(2)`), and make any residual use a build-time
panic (`Toggle::Evicted` panics on use).

## How jackylee0424 did it (ecdsa.fail a6098537)

- **Split by regime first.** No-payload traversals (T2/T3): the evicted role binds to
  boundary-clean payload words (P0/P1) and a second scratch loan — cheap, even a T win
  (-28.6M emitted T there). Payload traversals (T1/T4): 13+ named rewrite families
  (witness-free records, FF/FFSW/PAIR forms, E5 prepared compare, K2C/K2D ladders,
  INV3 under a digit-sign premise, exact full-complement sign queries, hosted maps
  with schedule bounds, endpoint hosts on named Q lanes, ...).
- **Every host must be proved free by layout or schedule, never observed-zero.** The
  candidate host that was "refuted for c146-202" is the discipline: a host that is
  merely *usually* zero kills the row.
- **Pay for it honestly.** +8.8% executed T for -1 qubit. On a q x T board this is a
  Pareto move only where the exchange rate (T/qubit at the margin) favors width.
- **Schedule-bound shortcuts:** hosted maps carry a "counter < 64" schedule bound;
  nonfixed middles replace fixed middles where the fixed form needs a third host.
- **Bake the switches.** Each stage gate was an env knob baked on in mod.rs with an
  off-switch for A/B (C658_T23, C658_WP1..5, C658_DROP).

## When a census "kill" is not dead

A census of the Q658 tree had proved every *register knob* dead (the pool needs its lanes
simultaneously). The eviction answer routed around the census entirely: not "free a
bit from the pool" but "delete the pool". Rule: a knob-level kill does not bound a
site-level rewrite program. When you park a width, say which of the two you measured.
