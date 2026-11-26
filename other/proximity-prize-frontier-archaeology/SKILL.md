---
name: proximity-prize-frontier-archaeology
description: "Compare each newly accepted Proximity Prize proof with its accepted predecessor only. Bind the source and the public note, inspect proof-root and module changes, and isolate the lever that transfers, without contaminating clean-room lanes."
---

# Scherbehuufe (proximity-prize-frontier-archaeology)

Use this skill after an accepted better.codes frontier move or when comparing a competitor's promoted proof with its immediate accepted predecessor. This is incumbent-history research. Never place its source, receipts, conclusions, route hints, or terminology in a clean-room re-descent packet.

## Bind the accepted pair

1. Refresh the live benchmark and record the accepted score, accepted source commit, benchmark ID, track, and observation time.
2. Resolve the immediately preceding accepted source from the benchmark or repository lineage. Do not substitute a convenient older checkpoint.
3. Work in a read-only clone containing both commits. Confirm the benchmark contract tree and editable submission path.
4. Save the public PR or submission note locally when one exists. Preserve its URL and retrieval time in the surrounding campaign receipt; the helper binds the exact note bytes.
5. Run:

```bash
python3 scripts/frontier_archaeology.py capture \
  --repo /absolute/path/to/repo \
  --older PREDECESSOR_COMMIT \
  --newer ACCEPTED_COMMIT \
  --submission-dir ProximityPrize/SubmissionLower \
  --note-file /absolute/path/to/public-note.md \
  --output /absolute/path/to/frontier-delta.json
```

The command fails if the pair is non-ancestral, if another score-changing commit lies between the two, or if the newer ref is not itself the next score promotion. Use a separately reviewed explicit lineage receipt for histories that cannot satisfy those checks; do not weaken the default.

## Inspect the mechanism

Read the receipt and the exact diff, then answer in this order:

1. What score and radius changed?
2. Did `Solution.lean` switch proof roots or only retune the same root?
3. Which imported modules, theorem providers, and constants changed?
4. What does the public note claim, and which changed lines actually support it?
5. What is inherited infrastructure, what is the new lever, and what is packaging or cleanup?
6. Can the lever transfer to the current accepted tree without importing a dead route or falsified assumption?

Treat generated `transfer_review` fields as an audit form, not an automatic conclusion. Fill each claim with file-and-line evidence. A module name, commit subject, or PR prose alone does not establish the mechanism.

## RCI loop

Run one bounded loop per promoted pair:

1. **Inspect:** direct-predecessor receipt, exact diff, proof root, public note, and live campaign obstruction ledger.
2. **Critique:** name the smallest unsupported mechanism claim, lineage ambiguity, or hidden inherited dependency.
3. **Improve:** narrow the claim or isolate one executable falsifier for the alleged lever.
4. **Verify:** replay the receipt and run the falsifier against both predecessor and accepted source.

```bash
python3 scripts/frontier_archaeology.py check \
  --receipt /absolute/path/to/frontier-delta.json
```

Only route a lever onward when the evidence distinguishes it from accompanying churn. Record `TRANSFERABLE`, `SOURCE-BOUND`, `FALSIFIED`, or `UNRESOLVED`; never silently convert `UNASSESSED` into a strategy recommendation.

Read [references/receipt-and-review.md](references/receipt-and-review.md) before publishing a lineage conclusion or dispatching a lever to another lane.

