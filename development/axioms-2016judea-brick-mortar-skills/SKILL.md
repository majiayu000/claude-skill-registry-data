---
name: axioms
description: Turn beliefs about a dataset into falsifiable laws. Take a body of data back to its equations, state each as an axiom with a pre-registered threshold, test it, try to disprove it, restate it, and confirm the restatement on held-out data, until the boundaries of what the data supports are mapped. Use when you say "prove it", "what are the laws of this data", "is that number actually true", "where does this break", or before any product, claim or rule rests on an assumed regularity in your data.
---

# Axioms

**A world is the set of statements its data cannot falsify.** This skill turns
"we believe X about this market" into an equation, a threshold, a test and a verdict,
and keeps the dead versions so nothing is re-believed by accident. Bring the ratio,
not the adjective.

Keep a ledger per dataset ("instance"): `LEDGER.md` written from a `ledger.json`
your harness emits.

## The objects

| Kind | Form | A failure means |
|---|---|---|
| **Identity (I)** | exact equation the record must satisfy by construction (`total = land + bldg`) | a **data defect**, never a discovery. Find the rows, fix the source. |
| **Law (L)** | statistical equation + pre-registered threshold (`median(assessed/price) in [0.90,1.10]`) | the law is false *as stated*. Go to disproof. |
| **Boundary (B)** | a law plus the domain it holds on (`depreciation holds for 1940-2009 stock`) | the boundary is drawn wrong. The edge itself is the finding. |
| **Theorem (T)** | derived from 2+ accepted statements by algebra or logic, then tested on its own | at least one premise's *domain* is wrong. The theorem is the cheapest audit of its axioms. |

Every statement carries: `id`, `equation`, `threshold`, `n`, `measured`, `verdict`
(HOLDS / FALSIFIED / ERROR / UNTESTABLE), and for v1 laws a `disproof` block.

## The loop

    state -> equation -> pre-register threshold -> test -> DISPROVE -> diagnose -> restate (') -> confirm on held-out -> ledger
                                                             ^                                                    |
                                                             +-------- a restatement is a new axiom --------------+

1. **State** in words a customer would recognise, then as an equation over named columns.
2. **Pre-register** the threshold in code *before* the first run. Use the field's
   standard where one exists (IAAO for assessment ratios, Nigrini for Benford) and cite it.
3. **Test** on the full population. Report n.
4. **Disprove, always, even on a pass.** Stratify by every axis the data offers
   (place, size, age, time, source, the edge between two jurisdictions) and look for the
   stratum where it breaks. A law no one tried to break is not proven, only unattacked.
5. **Diagnose every failure as exactly one of:** *instrument* (my query is wrong),
   *data defect* (the record is wrong), *form* (wrong equation: confounded, inverted,
   wrong functional shape), *domain* (true only somewhere). Name which.
6. **Restate** as a new id (`L1 -> L1'`). Instrument fixes may bring the query *to* the
   named standard; they may not move the threshold.
7. **Confirm** the restatement on both halves of a deterministic split (`hash(key) % 2`).
   It must hold on each half separately.
8. **Ledger.** Both versions stay.

## Rules (each with its why)

1. **The threshold is written before the number is seen, and never moved.** A threshold
   chosen after the result is a description, not a test. A law that misses its margin by
   0.0001 is recorded FALSIFIED, not rounded up.
2. **An identity failure is a bug ticket, not a finding.** Example: an identity "failed" on
   thousands of parcels because one county wrote `-9999` for null, and a downstream script
   read that as "building worth under 15% of value, so teardown". Treat identities as the
   data's unit tests; fix at the source.
3. **Check the instrument before believing a falsification.** Common instrument errors:
   computing a ratio upside down relative to the standard's definition, or a filter that
   selects exactly the cases under test (e.g. keeping only integer rates selects the round
   ones). Instrument errors look identical to discoveries.
4. **Diagnose on one half, confirm on the other.** Any restatement drawn after looking at
   the data overfits it. **Fix the hash function and record it**: two different hash splits
   can land either side of a tight gate, and a free choice of split is a free choice of verdict.
5. **Stratify by the predictor, never by the outcome.** Binning sales ratios by sale price
   manufactures regressivity out of regression to the mean; IAAO bins by assessed value.
   General form: never condition on the variable whose error you are measuring.
6. **A confound is a theorem waiting to be written.** Example: land value proportional to
   area^beta can give a negative beta citywide because small lots sit in expensive places.
   Holding location fixed (zip fixed effects) recovers a sane beta. When two laws interact,
   write the interaction down as its own statement.
7. **A capped or selected sample can't test a law about tails.** A pull capped per entity,
   or a list you chose yourself, cannot test a Pareto law. Mark it UNTESTABLE on this
   instrument, or say what population it describes.
8. **Never generalise a scoped number.** A reply rate measured on one channel on one day is
   not a blended rate. A number keeps the scope it was measured on.
9. **Every number in a product or rule must trace to a HOLDS row.** If copy or a rule rests
   on a FALSIFIED or untested regularity, that is the next axiom to run.

## The harness

Write one small script per instance (`prove.py`): each axiom is a function that queries
the store, computes the measured value, compares it to a threshold set in code, and calls
`record(id, equation, threshold, n, measured, verdict, disproof=...)`. A restatement is a
second function with a `p` suffix (`L6p` -> id `L6'`) that runs on `halves(key)`. Emit the
JSON to stdout and a one-line verdict per axiom to stderr. Open every store read-only.
Snapshot the JSON as `ledger-<instance>-<date>.json` next to the ledger.

**A new instance** (another city, another dataset, another business): copy the harness,
swap the store paths, keep the statements whose equations still parse. A law that held in
instance #1 and fails in instance #2 is the most valuable row either ledger holds: it is
where your model stops generalising.
