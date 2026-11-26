---
name: evaluator-scoring-surface-audit
description: "Read a benchmark's evaluator, verifier and scoring source line by line for gaps between what is counted, what is checked and what is only assumed, then turn each gap into a priced lever, a tool, or a report to the organisers. Use when joining a benchmark, after any evaluator change, or when the leaderboard moves in a way your cost model does not explain."
---

# Chliidruckts (evaluator-scoring-surface-audit)

The **scoring surface** is the set of quantities the score reads and the set of properties the verifier checks. A
**gap** is a place where the two differ: something counted that can fall without touching a checked property, or a
check whose bound differs from the scorer's. The audit lists both sets with line references, crosses them, and
classifies every gap before anything is built.

## Use it / leave it

- Use when joining a benchmark, after every evaluator or verifier commit, and when a rival's score moves in a way
  your cost model cannot explain.
- Do not use it to look for ways around the stated rules. A gap that contradicts the benchmark's written intent is
  reported to the organisers and not used. The source campaign flagged its own such observation in the submission
  note that used an executed-count lever.
- It does not replace reproducing the metric. Build or obtain an exact local evaluator first
  (`exact-evaluator-replica`).

## Inputs

- Evaluator, verifier and scoring source at a pinned commit, including the official runner's wrapper script.
- The written rules.
- Two or three recent top submission notes.

## Procedure

1. **List every quantity the score reads.** For each: the exact line that increments it and the condition under
   which it increments. Read the code, not the README.
   Worked example: the charged-gate term is the average *executed* count over the sample, not the emitted count; and
   the counter increments by executed samples even when the gate's controls are never both set.
   Done when every term of the score formula has a file:line and an increment condition in `assets/surface-table.md`.

2. **List every check.** Value, phase or side-effect cleanliness, scratch, size caps, allowed imports, time and
   memory limits. For each: its line, its bound, and its sampling (all inputs, a sample, or none).
   Done when every reason the verifier can reject is a row.

3. **Cross the two lists.**
   - For each counted quantity: can it be lowered without touching any checked property?
   - For each check: is its bound the same as the scorer's bound for the same quantity?
   - For each written rule: is there a line that enforces it?
   Worked example of a bound mismatch: a verifier capped a claim file at 128 bytes, which limited a claimed constant
   to 122 digits, while the scorer accepted values below 10^295. The fix raised the cap to 302 bytes and added a
   boundary test at 10^295 - 1 and 10^295.
   Done when each cell of the cross has "no gap" or a named gap.

4. **List every source of randomness and what seeds it.** When the artefact's own bytes seed its test inputs, a
   no-op edit re-rolls the sample. That fact turns every sampled check into a search problem and must be in the
   table. Done when each random draw has a seed source and a statement of who can influence it.

5. **Classify each gap.**
   | class | meaning | action |
   |---|---|---|
   | exact lever | value-preserving on all inputs | price it, then build |
   | sampled lever | value-preserving on the verifier's sample only | needs a failure-rate budget and a disclosure; see `inert-op-screen-to-structural-rule` |
   | harness defect | the harness contradicts itself (bound mismatch, crash, wrong accounting) | report with a patch and a test |
   | intent conflict | legal by the code, against the written intent | report, do not use |
   Done when no gap is unclassified.

6. **Price the top three** with one ten-minute experiment each before building anything. An experiment is the
   smallest edit that moves the counted quantity, scored by the judge or the replica.
   Done when three gaps have a measured price or a measured zero.

7. **Write the audit as a table** in the campaign repository, pinned to the evaluator commit. Re-run steps 1 to 3 on
   every evaluator commit and diff the tables.
   Done when the table is committed with the pin in its header.

## Checks that say it worked

- Every score term has a line reference.
- At least one gap is confirmed by an experiment, or the audit states "none found" with both lists attached.
- Every harness defect has a failing test before the fix and a passing one after.
- Both evaluator paths were read: the local command and the official runner.

## Failure modes

- **Treating a sampled lever as exact.** "Never fires on the sample" is not "never fires".
- **Using an intent conflict silently.** State the observation in the note and tell the organisers.
- **Auditing the README instead of the code.** The README says what was meant; the line says what is counted.
- **Missing a second evaluator path.** The local command and the official runner can differ in limits, flags or
  versions.
- **A stale audit.** The table is valid for one evaluator commit.

## Transfer

Direct to every benchmark with public scoring code: circuit cost, prover time or cells, gas, proof size. The same
four classes apply. On a benchmark with exact verification the "sampled lever" class is empty and every candidate
lever needs a proof.

## Evidence this pays

Citation key: `N:<id8>:<line>` is a public submission note of the source campaign (solver BitWonka, ecdsa.fail)
by id prefix; `T:` is a file in the public `ecdsafail-tools` repository; `E:` is a commit in that solver's evm.fast
fork. Numbers are quoted; none was re-measured for this skill.

- Executed against emitted count: conditional replay moved 1,452,820 emitted to 1,404,058 executed at 1,300 qubits
  (N:4b7d7272:8-14). The construction is credited to Codex (OpenAI) in that note (:12). The same note flags that
  scoring on emitted count may match the intended cost model better (:10).
- Charged but inert ops: one line of evaluator behaviour (T:README.md:15) is the basis of the inert-op drop, which
  the tool's README describes as a reimplementation of a lever already in the field.
- Stream layout: one line (T:fasteval/README.md:19) is what makes an exact parallel replica possible.
- Bound mismatch: E:7523d379 is a two-file harness fix with a boundary test and no score evidence.

The record shows the pattern paying under this account, with mixed authorship: three findings with a score or tool
effect and one harness fix without score evidence. It does not show that one person ran it as a single procedure;
the seven steps are a generalisation.
