---
name: exact-evaluator-replica
description: "Build and validate a fast, exact local copy of a benchmark's official evaluator: same inputs, same counts, same score, proven by a differential fuzz test and a reproduced graded log. Use when the official judge is too slow, too memory-hungry or too opaque to sit inside the edit loop of an optimization campaign (circuits, provers, gas, proof size), when many candidates must be scored per day, or when a failure-rate estimate needs fresh samples the judge cannot give."
---

Paths such as `scripts/...`, `references/...` and `assets/...` are relative to this skill's folder.

# Doppelgängerli (exact-evaluator-replica)

A **replica** is a second implementation of the official evaluator (the **judge**) that prints the same numbers for
the same artefact, faster or in less memory. It is exact or it is nothing: a replica that is "close" is a proxy and
belongs to `calibrated-static-cost-proxy`. Every other loop in a campaign runs on this tool, so it is built first.

## Use it / leave it

- Use when a judge run takes more than a few minutes or more memory than the workstation has, when many candidates
  must be scored per day, or when a failure-rate estimate needs fresh samples.
- Leave it when the judge already runs in seconds.
- Leave it when the judge's source is not public. Then only a calibrated proxy is possible.
- Never use a replica number as the official one. The submission is scored by the official runner.

## Inputs

- The evaluator's source at a pinned commit.
- At least one artefact with an official graded log (the passing path).
- A machine that can run the official evaluator on small artefacts.

## Procedure

1. **Write the determinism map.** Read the evaluator end to end. For every random draw record its source, its order,
   and whether the amount drawn depends on what executed. Fill `assets/determinism-map.md`.
   Worked example: in the source benchmark all randomness is one SHAKE256 stream seeded by a hash of the artefact;
   the first 64 x 9,024 bytes make the inputs; every measuring op then reads 8 bytes per 64-sample batch whether or
   not its condition lets it execute, so batch b's bytes sit at offset 64*9024 + 8*M*b (M = measuring ops).
   Done when you can state, for any unit of work, the exact offset of its randomness.

2. **Choose the unit of parallelism from the map.** When offsets do not depend on execution, units are independent:
   one producer generates the stream in order and hands each unit its slice; workers simulate units. Bound the queue
   (depth 2 in the example) and recycle buffers, since the producer is the bottleneck and extra workers only add
   memory. When offsets depend on execution, stop: an exact parallel replica is not available. Report that finding
   and fall back to a serial replica with a compact representation, or to a proxy.
   Done when the unit and its offset formula are written in the map.

3. **Compact the representation.** Pack each record to the minimum the semantics need (20 bytes against the judge's
   56 in the example). Reserve index 0 of the condition table as an all-ones "no condition" word so the hot loop has
   no branch for it. Keep the judge's loader format, magic bytes and size limits unchanged.
   Done when the replica loads every artefact the judge loads and rejects every artefact the judge rejects.

4. **Print the judge's own lines.** Same labels, same rounding, same score formula, so outputs compare with `diff`.
   Add what the judge cannot give: totals even when samples fail, a per-sample failure count, the index of the first
   failing sample. Done when a passing artefact's replica output contains every judge line verbatim.

5. **Write a random-artefact generator.** It must cover every op kind, every condition form, nesting, and the
   malformed-but-accepted cases (closing a block at depth 0, measuring ops inside conditions). Start from
   `scripts/gensynth.py`: give it a JSON spec of the judge's op kinds and replace `encode()` for a binary format.
   Done when `--require-coverage` exits 0.

6. **Differential test.** For at least three seeds, run judge and replica on the same random artefact and compare
   every count and every average. Random artefacts fail every sample, so read the judge's averages from wherever it
   records them on failure (a results file it appends to, in the example) and restore that file afterwards:
   ```bash
   python3 scripts/difftest.py --gen '<gen> {out} {n} {seed}' --judge '<judge> {artefact}' \
     --replica '<replica> {artefact}' --field 'tested samples' --field 'wrong outputs' \
     --side-file results.tsv --side-col '3=avg executed cost' --n 200000 11 22 33
   ```
   The label and the column are your judge's own. For the bundled toy they are `'1=avg executed charged'`.
   Done when it prints `all seeds match`. This covers semantics, accounting and stream alignment only.

7. **Golden test on the passing path.** Reproduce at least one officially graded log to the last printed digit.
   Random artefacts never reach the passing path, so step 6 cannot stand in for this.
   Done when one graded log matches digit for digit with the code you will actually use.

8. **Add a salt switch.** An option that mixes a string into the seed gives a fresh, independent sample set for the
   same artefact. Print on every salted run that the score is not official. Failure rate = mean failing samples over
   several salts; standard error = sd / sqrt(runs).
   Done when two salts give different inputs and an unsalted run still matches the judge.

9. **Pin and re-gate.** Record the evaluator commit and the list of files whose change invalidates the replica
   (evaluator, simulator, input derivation, dependency manifest). Re-run steps 6 and 7 when any of them changes.
   Done when the pin and the file list are written next to the replica.

## Bundled scripts

All are Python 3 standard library. Each has `--selftest`.

| script | purpose |
|---|---|
| `scripts/difftest.py` | Differential test driver: generator, judge and replica commands in, labelled fields compared, side file snapshotted and restored, non-zero exit on any mismatch. |
| `scripts/gensynth.py` | Spec-driven random artefact generator with a coverage report. |
| `scripts/toy_bench.py` | A miniature benchmark: a scalar judge reading randomness from a cursor, and a bit-sliced parallel replica reading it by offset. Read it once as the worked example of steps 1 to 8. Its `--bug 1` and `--bug 2` switches inject the two classic defects (stream misalignment, wrong charge condition). |
| `assets/determinism-map.md` | Template for step 1. |

The toy uses a text format and 200 samples. For a real judge, write the replica in the judge's language against its
own crates or modules, and keep `difftest.py` and the generator as the gate.

## Checks that say it worked

- `all seeds match` on at least three seeds.
- One graded log reproduced digit for digit.
- Replica and judge agree on the first failing sample of a known-bad artefact.
- An injected defect in the replica makes the differential test fail (the gate has teeth).
- Memory and wall time written down next to the judge's (example: 1.24e9 ops in about 3 minutes and 33 GB, against
  about 69 GB for the judge).

## Failure modes

- **A passing-path bug hidden by random artefacts.** They always fail. Never skip step 7.
- **A dependency swap changes the stream.** The source campaign's first version used a different SHAKE
  implementation behind a self-test against the reference one. Keep such a self-test whenever a primitive is swapped.
- **Replica numbers reported as official.** Label every figure with the tool, salted or unsalted, and the pin.
- **The judge changes silently.** Step 9 is the guard.
- **An inherited golden test.** In the source campaign only one of four golden rows was re-checked with the
  published code. After any refactor, re-run the golden test.
- **A build of the artefact that still needs the judge's memory.** The replica fixes evaluation only; check whether
  the generator can stream its output.

## Transfer

- Gas races: a local meter differential-tested against chain receipts.
- Provers: a cell or memory counter tested against the official run.
- Proof-checking benchmarks: a local replay of the verifier's policy checks
  (see `evaluator-scoring-surface-audit` for a bound mismatch found that way).

## Evidence this pays

Citation key: `N:<id8>:<line>` is a public submission note of the source campaign (solver BitWonka, ecdsa.fail)
by id prefix; `T:` is a file in the public `ecdsafail-tools` repository. Numbers are quoted from those sources; none
was re-measured for this skill.

- Published 11 Oct 2026 (T: commit 9f92470). Every low-qubit row after it is scored with it
  (N:5fa63407:125, N:2d167363:12).
- The official run it replaced "thrashed in 72 GB... stopped after two hours" (N:ddd607c9:181).
- Four graded logs matched to the last digit (T:fasteval/README.md:68-75); one of the four with the published code
  (README:77).
- Five other solvers name the tool in their notes within five weeks. These are mentions, not verified independent
  use.
- Mechanism sources: T:fasteval/README.md:14-24 (stream layout), T:fasteval/fasteval.rs:63-66 (compact op),
  :414-470 (producer and workers), :154-157 (salt), T:fasteval/gensynth.rs:1-8, T:fasteval/validate.sh:23-58.
  The bundled scripts are independent generic implementations; no code is copied from that repository.
