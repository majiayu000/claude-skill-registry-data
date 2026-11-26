---
name: accepted-proof-exact-retune
description: "Extract the exact integer dependency model of an accepted Proximity Prize proof, search for the smallest strict 0.01 score step with replayable arithmetic, and formalize only the deltas that survive an independent exact check."
---

# Schrüblidräier (accepted-proof-exact-retune)

Use this skill when the current accepted proof architecture is fixed and the remaining question is whether a source-faithful integer parameter change can gain at least one centibit. It is not a license to treat proof constants as independent knobs.

## Snapshot the accepted proof

Refresh and pin the accepted source before modeling. Then capture the actual `Solution.lean` import closure:

```bash
python3 scripts/snapshot_accepted_proof.py \
  --project-root /absolute/path/to/accepted-checkout \
  --entry ProximityPrize/SubmissionLower/Solution.lean \
  --submission-dir ProximityPrize/SubmissionLower \
  --output /absolute/path/to/accepted-proof-snapshot.json
```

The snapshot records Git state, exact score and radius, proof root, imported file hashes, direct imports, literal inventories, and simple integer bindings. A lexical literal inventory is not the mathematical model; use it to find the source of each equation and constraint.

## Build the exact model

Create a JSON model following [references/model-schema.md](references/model-schema.md). Every constant, parameter, derived expression, constraint, and objective needs a `file:line` source anchor inside the captured proof closure.

Model the accepted parameter point first. The helper rejects the model unless its baseline objective equals both the snapshot score and `accepted_score_centibits`. Use integers only. `/`, floating-point literals, approximate logarithms, and unbounded calls are rejected.

## Search the first strict step

```bash
python3 scripts/exact_retune.py search \
  --spec /absolute/path/to/model.json \
  --snapshot /absolute/path/to/accepted-proof-snapshot.json \
  --output /absolute/path/to/retune-receipt.json
```

For a maximizing track, the search chooses the smallest score at or above `accepted + required_step`, then the smallest exact L1 parameter distance from the accepted point. It enumerates the declared finite domain and fails before work begins if the case limit is exceeded.

Replay before using a result:

```bash
python3 scripts/exact_retune.py check \
  --receipt /absolute/path/to/retune-receipt.json
```

## RCI loop

1. **Inspect:** accepted source, proof closure, exact baseline evaluation, and first qualifying cell.
2. **Critique:** find one missing coupling constraint, stale source anchor, truncated division, or parameter declared free despite being derived.
3. **Improve:** add the smallest source-backed correction to the model.
4. **Verify:** replay the exact receipt and independently recompute the winning cell.

If a correction removes the win, preserve the failed receipt and close that retune. Do not tune the model to recover the desired result.

## Promotion boundary

An exact retune receipt is exploration evidence. Only after it survives replay should a proof author change the accepted source. Then use `$fast-lean-proof-loop` for the edit cycle and `$lean-arklib-proofs` for the full target build, axiom audit, source policy, and evaluator gate. Formalize the smallest successful delta; do not pre-build a family of speculative Lean variants.

