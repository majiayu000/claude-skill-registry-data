---
name: reference-model-as-instrument
description: "For a new algorithmic design, write the exact classical reference model first and make that one model serve as test oracle, parameter-table generator, failure-class predictor, failing-case replayer and seed scanner. Use when starting a new design in a benchmark-optimization campaign (circuit, prover trace, contract, proof term) or when adopting a rival's design you will modify; not for post-passes or retunes of a design whose model already exists."
---

Paths such as `scripts/...`, `references/...` and `assets/...` are relative to this skill's folder.

# Stimmgable (reference-model-as-instrument)

A **reference model** is an exact, classical, integer-level description of what the artefact computes and what
every register holds at every step. Built first, it replaces five separate tools: the oracle for gate tests, the
generator of fitted tables, the predictor of failure rate by class, the replayer of the judge's own inputs, and the
scanner for seeds.

## Use it / leave it

- Use when starting a new algorithmic design, or when adopting a rival's design that you will change.
- Leave it for stream-level post-passes and for retunes of a design whose model already exists.
- The model cannot see properties outside its level (in a reversible circuit: phase and scratch cleanliness). Those
  need gate-level tests and the judge.

## Inputs

- The specification of the computation.
- The judge's input derivation, so the model can regenerate the judge's exact inputs from an artefact.
- An exact evaluator (the judge or a replica; see `exact-evaluator-replica`) for step 7.

## Procedure

1. **Two-level model.** Level one is the integer specification of the algorithm. Level two is a layout model that
   tracks what every register, lane or slot holds at every step, including windows and truncations. Test level two
   against level one at every step. Keep the model's code separate from the artefact generator: a model that shares
   code with the generator cannot disagree with it.
   Done when the layout model equals the specification on every non-failing input of a random sample.

2. **Gate tests climb a ladder against the layout model.**
   1. one step forward, including finished and stalled inputs;
   2. forward then inverse, with every side property the judge checks (phase, scratch);
   3. a whole inner routine inside its real shell;
   4. a whole traversal and back.
   Done when each rung passes at reduced scale and names the model function it compares against.

3. **Generate every fitted table from the model** by a named, re-runnable target with the sample count and seed in
   the command. No table is edited by hand. Worked example: an envelope target ran 200,000 model walks and wrote the
   window table file.
   Done when regenerating from scratch reproduces the committed file (`diag.py envelope --n 200000 --check env.txt`).

4. **Failure classes.** The model reports why an input fails (ran past the slot count, overflowed a window, left a
   window), with a rate per class and a standard error. Convert to expected failing inputs per judge run.
   Done when the rate table sums to the total and each class names the table entry that causes it.

5. **Replay the judge's inputs.** A diagnostic regenerates the judge's exact inputs from an artefact and runs them
   through the model. Use it on the first judge failure. Worked example: the first full build failed one sample;
   the replay showed the walk needed more rows than the envelope allowed for its slot; the next build passed.
   Done when a judge failure is reproduced by index and explained by class.

6. **Seed scan on the model, with prefix-hash reuse.** When the artefact's bytes seed its inputs and candidates
   differ only in a suffix: absorb the fixed prefix once, copy the hasher, feed only the tail per candidate, and
   stop at the first failing input.
   Done when the scan lists clean candidates and a full evaluation confirms each one used.

7. **Measure the model's blind spot.** On shared salts or seeds, compare model-predicted failures with the exact
   evaluator's failures. The remainder is what the model does not see. Worked example: 0.81 and 0.69 failing samples
   per seed were "not predicted" against a total near 8.7. When the blind spot is not small against the total, scan
   with a copy of the evaluator instead of the model, and check that scanner on the parent artefact's known clean
   and dirty seeds.
   Done when the blind-spot share is written down and the scanner choice follows from it.

8. **Keep one profile switch** that prints cost per named section and changes no output.
   Done when the artefact hash is identical with the profile on and off.

## Bundled script

`scripts/diag.py` (Python 3 standard library) implements the four entry points plus the blind-spot comparison
against a small model interface, with a toy model built in (Euclid's algorithm in fixed slots with per-slot
quotient-width bounds):

```bash
python3 scripts/diag.py envelope  --n 200000 --out env.txt          # run first: writes the table; --check to compare
python3 scripts/diag.py rate      --n 200000 --table env.txt        # rate per class with standard error
python3 scripts/diag.py replay    --artefact art.bin --table env.txt
python3 scripts/diag.py scan      --artefact art.bin --start 1 --want 3 --table env.txt
python3 scripts/diag.py blindspot --model predicted.txt --replica observed.txt
```

Pass `--model-file my_model.py` to plug in a real model; the docstring lists the ten names the module must define.
In a compiled codebase, port the same four entry points as test targets driven by environment variables
(`N`, output file, artefact path, start and want); the Python file is then the specification of their behaviour.

## Checks that say it worked

- Layout model equals specification at every step.
- The model's predicted failing set equals the exact evaluator's on the judge's own inputs at some seed.
- A table regenerated from scratch reproduces the committed file.
- The first judge failure of a new build was explained by a replay, not by a guess.

## Failure modes

- **Shared code between model and generator.** Then a bug appears in both and the oracle agrees with it.
- **Tables fitted on too few samples.** A width fitted on 30,000 samples failed in the source campaign and was
  refitted on 200,000. The script's self-test shows the same effect on the toy model.
- **Trusting the model for properties it cannot see.** Phase and scratch in a circuit; gas refunds or memory
  expansion in a contract model that tracks only storage.
- **A missing predicate.** The source campaign published an erratum after a missing check made two inputs look
  clean. Step 7 is how such a miss is found.
- **A model-only scan when the blind spot is large.** It passes dirty seeds.

## Transfer

- Provers: a trace-shape model that generates column schedules and predicts padding.
- Gas: a storage and opcode model that replays the benchmark's transactions.
- Proof benchmarks: a size model of a proof term that predicts where a bound is exceeded.

## Evidence this pays

Citation key: `N:<id8>:<line>` is a public submission note of the source campaign (solver BitWonka, ecdsa.fail)
by id prefix; `T:` is a file in the public `ecdsafail-tools` repository. Numbers are quoted; none was re-measured
for this skill.

- One design went from model to a graded 825-qubit row through five listed intermediate builds, all passing after
  the one failure that the replay diagnosed (N:39ef23e2:164-176).
- Model against specification at every step, and the test ladder: N:39ef23e2:216-224. Table target: :237-239.
  Failure classes: :192. Replay diagnostic: :226-227. Profile switch: :242.
- Predicted failing set equal to the replica's: N:5764884a:90-91.
- Blind spot and the move to an evaluator-based scanner: N:2d167363:82, :86. The note does not state the reason for
  the move; linking the two is an inference.
- Prefix-hash reuse: T:dead-ccx-finder/find_dead_ccx.rs:73-117. Erratum: N:ebf0b736:118.
- Six other solvers name the design in their notes. These are mentions, not verified independent use.
- The model source itself is described in notes only; the bundled script is an independent implementation of the
  pattern.
