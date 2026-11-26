---
name: route-compare-probe-discipline
description: "Compare baseline and candidate on identical input vectors before blaming one call for ecdsa.fail residual or eval dirt. Use when a structural edit changes the op stream, because Fiat-Shamir sampling then tests the two circuits on different shots and can create or hide failures."
---

# Öpfel-und-Bire (route-compare-probe-discipline)

## Job

Prevent false localization when a circuit edit changes `ops.bin`. `residual_probe`
and trusted `eval_circuit` derive test vectors from the op stream. If the edited
route changes op count, op order, nonce tail, or targets, then the baseline and
candidate are usually tested on different Fiat-Shamir samples. A dirty candidate
screen can be an actual bug, a sample-shift exposure of pre-existing dirt, or both.

Use this skill before claiming a specific call, row, carry, codec window, or fold
override is semantically dirty.

## Hard rules

- Same-vector compare is a localization tool, not a submission gate.
- Never claim `BEAT`, a clean route, or a submit-ready package from route-compare alone.
- Promotion still requires fresh build, full 9024 trusted/residual zero
  classical/phase/ancilla garbage, then official benchmark score below frontier.
- If the baseline is dirty under fixed vectors, report the compare as relative
  evidence only: it can falsify a blamed call but cannot prove the candidate clean.
- Rebuild `ops.bin` before every residual/eval screen; do not trust stale streams.

## When to use

Use when any of these are true:

- A per-call env gate appears clean for some calls and dirty for adjacent calls.
- `residual_probe` changed after adding/removing only a few ops.
- A local toy proof passes but full-circuit residual gets mixed classical/phase dirt.
- The candidate changes op hash, op count, or tail nonce placement.
- You need to decide whether to localize inside the edit or first clean the baseline.

## Probe pattern

Create or reuse a diagnostic binary that:

1. Builds baseline ops and candidate ops in the same source tree.
2. Clears only the candidate env knobs for the baseline build.
3. Sets exactly the candidate env knobs for the candidate build.
4. Derives one deterministic input vector set independent of candidate hash, or
   deliberately uses `baseline_fs` / `candidate_fs` modes and labels the result.
5. Runs both routes on the same point-add inputs.
6. Reports:
   - baseline classical/phase/ancilla failures,
   - candidate classical/phase/ancilla failures,
   - output diff count between baseline and candidate,
   - phase diff batches,
   - first useful divergence mask.

Recommended command shape:

```bash
ROUTE_COMPARE_SHOTS=512 \
ROUTE_COMPARE_CANDIDATE_ENV='TLM_FFG_CY0_PARK_CALLS=182' \
cargo run --release --bin route_compare_probe
```

For values containing commas, separate env edits with semicolons:

```bash
ROUTE_COMPARE_CANDIDATE_ENV='TLM_FFG_CY0_PARK_CALLS=178,180,181;TLM_FOLD_CALL_CODE_OVERRIDES=248:5,265:5' \
ROUTE_COMPARE_SHOTS=2048 \
cargo run --release --bin route_compare_probe
```

## Interpretation

- `output_diff=0` and candidate failures match baseline failures:
  - The edit is not locally blamed by this sample.
  - If residual was dirty, suspect op-hash sample drift, baseline dirt, or later
    composition.
- Candidate has new classical failures vs a clean baseline:
  - Value bug. Localize inside the edit before widening.
- Candidate has phase-only failures:
  - Classify phase source before nonce search. Do not submit.
- Candidate has ancilla-only failures:
  - Lifetime/reclaim bug. Check host was truly zero at loan and restored at reclaim.
- Baseline is dirty:
  - Move the probe to a cleaner checkout or treat the finding as falsification only.

## Report line

```markdown
## HH:MM route-compare localization
Candidate=<name> baseline=<tree/hash> candidate_env=<env>.
Same-vector compare=<shots> base=<c/p/a> cand=<c/p/a> output_diff=<n> phase_diff_batches=<n>.
Interpretation=<local-edit-falsified|value-bug|phase-bug|baseline-dirty>.
Gate=no winner/no submit; next=<bounded action>.
```

## Park conditions

- Same-vector compare is dirty and the failing route has no clean local toy proof.
- The baseline itself is dirty and no cleaner baseline can be produced quickly.
- The route saves peak qubits but Toffoli headroom cannot beat the refreshed frontier.
- A 9024 trusted/residual run is not zero classical/phase/ancilla.
