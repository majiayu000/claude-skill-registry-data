---
name: legacy
description: "Apply this opinionated workflow when modernizing legacy systems: strangler fig pattern, branch by abstraction, characterization tests, incremental monolith decomposition, framework upgrades, feature-flagged migration with rollback."
---

# Legacy Modernization

Incremental migration of running systems. The constraint that shapes every decision here: the system is in production and must keep working while it changes.

## The sequence

Order matters more than the individual techniques — each step exists to make the next one safe.

1. **Characterize before changing.** Write tests that pin current behaviour, bugs included. You are not testing what the code _should_ do; you are recording what it _does_, so a behaviour diff becomes visible. When an assertion looks wrong, that is the point — write it down and say so:

   ```python
   def test_domestic_lightweight():
       order = {"weight": 5, "destination": "domestic", "priority": False}
       # Current behaviour: nothing charged under 10kg. Looks like a bug —
       # pin it here, fix it as its own change after the migration lands.
       assert calculate_shipping_cost(order) == 0.0
   ```

   Golden-master or approval tests (approvaltests, syrupy) get coverage over gnarly code fastest, because they capture output wholesale instead of requiring you to understand it first.

   Then check the net actually holds: run a mutation tester over the code you are about to change. Characterization suites routinely look thorough and still miss the exact branch you're about to touch — surviving mutants tell you where, before an incident does.

2. **Insert a seam.** Branch by abstraction: introduce an interface over the thing you're replacing, and route all callers through it while it still delegates to the old code. This is a no-op change you can ship and verify on its own.
3. **Build the replacement behind the seam,** dark or flagged off. It isn't serving traffic yet, so it can be wrong.
4. **Shift traffic incrementally** with a flag — internal users, then a percentage, then all. Each step is reversible in the time it takes to flip the flag, which is the property that makes this safe. Name the rollback trigger as a metric and a threshold _before_ each ramp ("error rate above 0.5% for five minutes → back to the previous percentage"). Deciding what counts as bad while it is happening is how a ramp turns into an argument instead of a rollback.
5. **Delete the old path only after the new one has run clean in production** for long enough to cover its slow cases — month-end jobs, seasonal peaks, the annual report. Deleting early is how you discover a code path nobody remembered.

## Conventions

- **No big-bang rewrites.** A rewrite competes with a moving target: the old system keeps shipping features while the new one catches up. Every successful modernization in this playbook is incremental for that reason.
- **Every step ships and is reversible.** A migration that only works when fully complete has no safe abort point — and something always interrupts a long migration.
- **Parallel-run before cut-over for anything computing money or state.** Run old and new against the same input, compare outputs, log divergence, keep serving the old result. Divergence you can see beats divergence a customer reports.
- **Strangler fig for the overall shape:** a facade in front, routing per-feature to old or new, moving one route at a time until nothing reaches the old system and it can be removed.
- **Preserve behaviour by default, including bugs.** Something downstream depends on the odd ones. Fix them as separate, visible changes — never folded into a migration, where a behaviour change is indistinguishable from a migration defect.
- **Database migrations expand and contract:** add the new column, dual-write, backfill, switch reads, then drop the old — each phase deployable on its own, each compatible with the version of the code running beside it.
- **New code written against the legacy system still meets current standards.** Matching the surrounding style "for consistency" is how a modernization ends with more legacy code than it started with.
