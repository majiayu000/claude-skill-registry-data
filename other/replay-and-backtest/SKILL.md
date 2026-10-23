---
name: replay-and-backtest
description: Validate every rule change on deterministic replay fixtures through the same code path as live paper before it may touch a ticket.
bots:
  - bot-08-signal
  - bot-06-exit
gates:
  - G-2
required_tools: []
required_data: []
permissions:
  max_side_effect: read
  network: true
  filesystem: var
fixtures:
  - tests/fixtures/replay/smoke
---

# Replay and Backtest

## L1 - Summary

No rule change reaches a ticket without first surviving replay. Run `pumpgrok run --mode paper --replay tests/fixtures/replay/<dataset>` to execute the candidate rule against recorded history through the same code path as paper trading. Replay ledgers live under `var/replay/<dataset>/` with `source=replay` and never feed live metrics.

```
rule change -> replay on fixtures -> metrics match bar -> paper trial -> ticket flow
rule change -> replay fails        -> rule stays out
```

## L2 - Method

1. S1 - Pick the dataset: use the fixture set matching the market regime under test (default `tests/fixtures/replay/smoke` for the smoke path). Recorded fixtures only; never replay against live endpoints.
2. S2 - Run the identical path: `pumpgrok run --mode paper --replay <dataset>` drives the supervisor, the rule, and the paper adapter with a fixture clock, so ids and fills reproduce byte-for-byte.
3. S3 - Read replay-only metrics: confirm the replay ledger at `var/replay/<dataset>/ledger.sqlite` carries `source=replay` rows. A ledger mixing replay rows into paper metrics fails the run.
4. S4 - Compare against the bar: the candidate must beat the pinned baseline on the dataset's scorecard (fills, drawdown, halt behavior) before SIGNAL or EXIT may propose it for paper.
5. S5 - Promote explicitly: a passing replay earns a paper trial with a fresh ticket series, receipted per `verification-receipts`. Skipping replay is not a shortcut CHIEF or RISK will approve.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| Replay passes, paper fails | Fixture regime drift or a live-only code path | Pin the divergence; add a fixture covering it before re-promoting |
| source=replay rows in paper metrics | Ledger path misconfiguration | Fail the run; replay ledgers never feed the live gate |
| Non-deterministic replay | Wall-clock, uuid, or unseeded randomness in the path | Remove the nondeterminism; every id comes from the seeded factory |
| Missing dataset | Fixture set deleted or never recorded | Record or restore the dataset; never substitute live traffic |

## References

- Runner: `pumpgrok run --mode paper --replay tests/fixtures/replay/<dataset>`
- Fixtures: `tests/fixtures/replay/smoke` (smoke dataset plus manifest)
- Gate G-2: backtested rules still need approval before paper
- Companion skills: `desk-strategy-lab` (rule experiments), `momentum-signals` and `position-monitoring` (signal and exit rules under test)
