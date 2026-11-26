---
name: quantum-record-mining
description: "Mine existing circuit records for overlooked measured gains, process-blocked candidates and mechanisms missing across arithmetic families, before new paper-driven work."
---

# Goldwäscher (quantum-record-mining)

Run before paper exploration. This is read-only triage; it does not reopen lanes or submit rows.

1. Snapshot the official board and mechanically extract Q×T mentions from the authorized ledgers, lane mailboxes, result files and notes. Use `scripts/frontier_mine.py`; inspect missed formats and preserve source/line provenance. Mentions are leads, not measurements.
2. Compare each lead with `C(q)=min(T_i:Q_i<=q)`, using [benchmark semantics](../quantum-structural-lanes/references/benchmark-facts.md). A row dominated by a lower-width result has no new frontier value. Refresh before any promotion.
3. Search `verifier|HOLD|blocked|killed|closed|parked`. Separate process blockers (missing review/delivery) from correctness/economic rejection. Recover primary receipts and current ownership; a blocked result is not permission to duplicate it.
4. Build a compact **lever × architecture** matrix from notes **and active source**: present, absent, incompatible or unverified, with function/hash references. Older-tree savings often disappear on newer trees; re-price the actual composition.
5. Rank measured unreviewed gains first, then source-supported cross-family transfers and one-qubit cliffs. For a cliff, name every binding phase and use the distinct Pareto and product budgets. Hand off a five-line proposal under the [shared contract](../quantum-structural-lanes/references/lane-contract.md).

Example, from this skill directory:

```sh
python3 scripts/frontier_mine.py board.json --q 796 825 --notes ledger.md results.md --out mining.json
```

The script uses explicit local files only. Review all prospective gains against complete logs; it neither certifies exactness nor changes campaign state. Stop when a lead is already owned, dominated, unsupported by receipts or killed without a changed premise.
