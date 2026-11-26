---
name: lever-switches-and-break-controls
description: "Land each optimization lever behind a default-on constant with an inert development override and a set of numbered deliberate breakages that the test suite must catch, so stacked levers stay separable and every check is shown to have teeth. Use when stacking more than two levers on one generator-built artefact (circuit, prover, contract, proof), when porting a lever from another tree, or when a lever's correctness rests on an invariant and not on an identity."
---

Paths such as `scripts/...`, `references/...` and `assets/...` are relative to this skill's folder.

# Sicherigschaschte (lever-switches-and-break-controls)

A **lever** is one optimization with one name. A **switch** turns it off and must reproduce the parent exactly. A
**break control** is a numbered, deliberate violation of one obligation the lever relies on; a named test must fail
when it is set. A control that the test does not catch is disclosed as **not claimed**.

## Use it / leave it

- Use when stacking more than two levers on one tree, when porting a lever from another tree, and for any lever
  whose correctness rests on an invariant ("these lanes are zero here") and not on an algebraic identity.
- Leave it for one-constant retunes: the constant is already its own switch.

## Inputs

- A generator-built artefact (the generator's source decides every op).
- A gate-level or unit test at reduced scale that runs in seconds to minutes.
- A cost counter (the judge, a replica, or a calibrated proxy).

## Procedure

1. **One lever, one name.** A compile-time constant `<NAME>` (default on once accepted) and a development override
   read from the environment under a fixed prefix, for example `DEV_<NAME>=0`. The official build reads nothing
   from the environment. State and test that the override is inert in an empty environment: build once with
   `env -i`, once normally with no overrides set, and compare artefact hashes.
   Done when both builds give the same hash and the lever table lists the constant and its override.

2. **Off-switch equivalence, before measuring any gain.** With the lever off, the build reproduces the parent's
   counts exactly. Worked example: with one lever switched off the tree reproduced the parent's two traversal
   counts (479,037 and 874,106) at the parent's parameters.
   Done when lever-off equals the parent on every counted quantity. A difference means the lever leaks outside its
   switch; fix that first.

3. **Write the break controls.** List the obligations the lever relies on. For each, add `<NAME>_BREAK=n` that
   violates exactly that obligation and nothing else. Worked example for one lever: 1 = no frame flip, 2 = decode not
   gated by the flag, 3 = swap flag not gated, 4 = counter lanes unprotected; for another: 1 = repair omitted, 3 = one
   receipt dropped. Break controls are development switches like the override and are equally inert in an empty
   environment.
   Done when every obligation in the lever's correctness argument has a number.

4. **Run them and read the table.**
   ```bash
   python3 scripts/run_breaks.py --name <NAME> --max <n> --state breaks.tsv \
     --expect '<text of the named test failure>' -- <test command>
   ```
   The script first runs the test with no break set; that run must pass. Then each control must fail the named
   test. `--expect` keeps a build error from counting as a catch.
   Done when every control is `caught` or handled by step 5.

5. **Disclose controls that pass.** A break the test does not catch is written into the note as not claimed, with
   its number. Then either add a stronger test, or raise the scale until it bites, or mark the obligation
   unverified. Record the scale a control needs. Worked examples: one control "passes at this gate, so it is not
   claimed"; another passes on 64 default samples and fails only with forced long runs at n >= 2,000.
   Done when the note lists every control as caught (with scale) or not claimed.

6. **Re-run inherited controls after every new lever.** A later lever can make an earlier test blind. Keep the
   state file in the repository; `run_breaks.py` exits non-zero when a control recorded as caught now passes.
   Worked example: the last note of the source campaign re-runs twelve control families.
   Done when all families were re-run on the current source and no regression is reported.

7. **Keep the ledger.** One table row per lever in build order: name, switch, cost after it, delta, controls
   caught, controls not claimed. Costs in one stated unit at one stated scale.
   Done when the ledger's last row equals the artefact's measured cost.

8. **Write down what the gate does not see.** List the properties the reduced test cannot check (peak resource use
   in the worked example: a peak one over the cap was found by the full build, not by the gate test). Assign each to
   a later full-scale check.
   Done when each unseen property names the check that covers it.

## Checks that say it worked

- Every lever has an off-switch run that equals the parent.
- Every lever has at least one caught break control.
- The full build in an empty environment equals the stamped artefact byte for byte.
- `run_breaks.py` reports no regression on the full set of inherited families.

## Failure modes

- **Overrides leaking into the official build.** The empty-environment rebuild is the guard. Finish it before
  submitting; do not submit while it is still running.
- **A break that changes more than one thing.** It can fail for the wrong reason and hide a blind spot. One
  obligation per number.
- **A failure that is not the named test.** A compile error or an unrelated crash is not a catch. Use `--expect`.
- **Controls run once and never again.** Step 6.
- **A passing control quietly dropped from the note.** It is the most useful line in it.

## Bundled script

`scripts/run_breaks.py` (Python 3 standard library): baseline run, loop over `NAME_BREAK=1..N`, table of caught,
not caught and other failures, a state file for regressions, `--strict`, `--accept`, `--selftest`.

## Transfer

- Any codebase with feature constants.
- Proof benchmarks: delete one hypothesis or one case and the proof must fail to check.
- Gas work: remove one guard and a named test must revert.
- Provers: drop one constraint and a named soundness test must accept a bad witness.

## Evidence this pays

Citation key: `N:<id8>:<line>` is a public submission note of the source campaign (solver BitWonka, ecdsa.fail)
by id prefix. Numbers are quoted; none was re-measured for this skill.

- Three consecutive rows stacked about a dozen levers in two days, 2,998,475 to 2,843,602 charged gates at 825
  qubits (N:2d167363, N:b5ea9819, N:390668eb).
- The override "inert in an empty environment": N:2d167363:29. Off-switch reproduction: N:2d167363:75. Numbered
  controls: N:2d167363:74. Ledger: N:390668eb:27-44.
- The gate tests forced four design corrections before submission (N:2d167363:52).
- Disclosed blind spots: N:b5ea9819:81 (a control that passes, "not claimed"); N:390668eb:82 (a control that needs
  real long runs); N:390668eb:76 (the gate test does not check peak).
- Limit of the evidence: no note reports a defect that only a break control exposed. The evidence supports the
  practice as a whole (switch, gate test, controls, ledger), not controls alone.
