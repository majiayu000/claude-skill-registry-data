---
name: pinned-table-stacking
description: >-
  Author declarative circuit-edit tables that are pinned to an exact gate list by
  length and hash, applied by an applicator that refuses any other stream, frozen and
  qualified as individual rungs, and stacked in call order before the nonce tail.
  Includes the portfolio-vs-exact labeling test (identical wrong-output and aligned
  failing-shot sets) and the "tables as durable assets" rule: a table above today's
  strict gate ships unchanged later inside a bigger stack. From jackylee0424's
  spookyfrog series on ecdsa.fail.
whenToUse: Authoring or auditing hash-pinned edit tables on a shared circuit tree; stacking several tables without re-deriving parents; labeling a candidate exact vs portfolio
---

# Tällerturm (pinned-table-stacking)

Distilled from jackylee0424's public ecdsa.fail notes (spookyfrog 22/23,
ba8ad256 / 2120d8a2, Oct 2026): his rows are tiny, safe, and constant — because the
safety lives in the table format, not in reviewer heroics.

## The table format is the safety mechanism

- Each table is a **separate declarative artifact** (his: `affine_followup.txt`,
  `union_followup.txt`) whose header pins the exact gate list it applies to: the
  operation count and hash of the stream it expects.
- The applicator (`source_edits`) **refuses to run on any other gate list**. A table
  can never silently mis-apply after a parent change; it either matches the pinned
  stream or fails closed.
- Tables apply in **call order** from the build file, after every inherited table and
  before the unchanged nonce tail. Inherited tables are kept **byte for byte** — you
  only ever add later tables.

## Rungs, not commits

- Build each table on the current tree, then freeze it, qualify it, and get it
  independently reviewed **as a rung of its own** before it joins a stack.
- A rung whose price is above the board's strict gate is **not deleted and not
  resubmitted alone — it ships unchanged later** inside a bigger stack that clears
  the gate. Tables are durable assets that wait for a stack to carry them.
  (spookyfrog 23's first table was built on spookyfrog 22, re-bound after an inline
  table landed, and shipped a cycle later, unchanged.)

## Portfolio vs exact — label honestly

- **Exact** means: identical wrong-output sets and aligned failing-shot sets against
  the parent on the tested inputs, with no measurement added or removed (his test:
  336 inputs in both frames; first-table rows on 24 packets).
- A table that trades anything statistically is labeled **portfolio, not exact**,
  and the note says so in the first paragraph. The paired failing-shot deltas ship
  with uncertainties (`+0.020 ± 0.081`), not bare zeros.

## Devices worth farming as rows

Live-product rows, two-wire parity rows, held ANDs, and swap holds with relays —
including holding a two-AND square term in place of a single-AND hold it displaces.
Allocate each device jointly with the table's slot over storage shown clean **without
trusting any inherited sampled table**.

## Scorekeeping honesty

Report the board score immediately before submission and the exact improvement
(his: −19,744, 0.002%), the ground nonce, the failing-shot rate with its paired
comparison to the parent, and the Toffoli gate with headroom. Tiny accepted
increments at a strict gate compound: his October run is ~1M score/day.
