---
name: recall-gate
description: Run the retrieval recall gate with dead-gold triage and the binary A/B regression test. Required before release tags; use after any retrieval-adjacent merge.
---

# Recall Gate

Answers one question with evidence: **did retrieval change?** Numbers moving is NOT the answer — fixture drift and corpus drift both move numbers without any retrieval change. Classify before believing.

## 1. Run both splits

```bash
CQS_NO_DAEMON=1 cqs eval evals/queries/v3_test.v2.json 2>/dev/null | grep OVERALL
CQS_NO_DAEMON=1 cqs eval evals/queries/v3_dev.v2.json  2>/dev/null | grep OVERALL
```

Aggregate = mean of the two (equal n=109). Compare against the latest recorded gate in `~/training-data/research/eval.md` — NEVER against numbers from memory. Run-to-run noise is ±1pp with an active daemon.

**Pin the substrate.** Eval numbers depend on WHICH index computed them — a bare `cqs eval` relays to the daemon's RESIDENT index (`index_substrate: "resident"` in `--json`), while `CQS_NO_DAEMON=1` forces a fresh CLI-side build (`"fresh-built"`). The two differ within the ~1pp HNSW-reconstruction noise, so comparing a resident run against a fresh-built baseline manufactures a phantom delta. Either pin `CQS_NO_DAEMON=1` on every run (as above — fresh-built always) OR assert the `--json` `index_substrate` marker is uniform across every run you compare (including the recorded baseline). The recorded gate must note which substrate it was taken on.

## 2. If any metric dropped: check dead golds FIRST

The matcher is `(origin, name)` — file moves, splits, renames, and deletions kill golds and cap R@K, looking exactly like a recall regression:

```python
# per split: for each q['gold_chunk'], does the index hold a chunk with that (origin, name)?
sqlite3 .cqs/slots/gemma/index.db "SELECT 1 FROM chunks WHERE origin=? AND name=?"
```

Re-pin dead golds: moved function → same name, new origin. Deleted function → re-point to the nearest current equivalent that genuinely answers the query text (read the query!), and record a `repinned_<date>` note in the query's metadata. Re-run step 1.

## 3. If a delta survives re-pinning: same-corpus binary A/B (definitive)

```bash
git worktree add /tmp/cqs-ab <baseline-tag>
cd /tmp/cqs-ab && CARGO_TARGET_DIR=$HOME/.cargo-target/cqs-ab cargo build --release --features cuda-index
CQS_NO_DAEMON=1 $HOME/.cargo-target/cqs-ab/release/cqs eval <fixture>   # both splits
CQS_NO_DAEMON=1 cqs eval <fixture>                                       # both splits, new binary
```

Pin BOTH sides to `CQS_NO_DAEMON=1` (daemon vs CLI path differences pollute the comparison). Bit-identical output = zero retrieval change; the inter-capture delta is corpus drift — say so and pass the gate. A real difference = regression; bisect the suspect PRs ("no ranking change" claims with pins are where to start). Clean up the worktree + target dir after.

## 4. Record and sync

- Append the gate block to `~/training-data/research/eval.md` (table, verdict, re-pins).
- On release gates, sync the three public surfaces to the new snapshot: README TL;DR line, `Cargo.toml` description, `gh repo edit --description`.
- Fixture re-pins commit with the gate (release branch or a docs PR).
