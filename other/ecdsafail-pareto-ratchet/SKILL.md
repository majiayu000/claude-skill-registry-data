---
name: ecdsafail-pareto-ratchet
description: "Hold rows on the ecdsa.fail Pareto board the way gnuchev did (167 submissions, 152 of them left moves). Shadow a fresh rival row at the same qubit count with exact cuts that work on any tree, turn one structural move into a band of rows with a single width dial, order the band by contention, and never lose a row to the validator. Use when a rival posts a row you can rebuild, or before submitting a billion-op row."
---

# Rätschi (ecdsafail-pareto-ratchet)

How gnuchev holds most of the low-Q and mid-band Pareto frontier. Every number is from his public submission notes
(fetch them with `ecdsafail submissions`; cited `<Q>/<id4>:<line>` in
[`references/gnuchev-method-digest.md`](references/gnuchev-method-digest.md); the low-Q October detail is in the sibling
skill `ecdsafail-scratch-diet`). The **ratchet**: every move is exact, keeps the parent's lambda, and lands as a row; rows
only ever go left or down.

Where his rows come from (73 measured mid-band rows): 27 % exact post-passes on a rival's fresh row at the same Q, 25 % a
one-parameter sweep after a composition, 11 % cap or pool moves priced against the lambda contract, 11 % grafts of two
public trees, 14 % his own structural changes. Actual qubit cuts are rare (five in October, all exact); most of the left
distance is Toffoli bought at a fixed width.

## 1. Shadow (same-Q, hours)

Trigger: a rival posts a non-dominated row on a tree your toolchain can rebuild; strongest within 12 h of the post.

1. `ecdsafail reset <submission-id>` (works on rejected rows), rebuild `env -i`, and confirm the parent's ops sha256 and
   its T **to the digit** before touching anything.
2. Apply the exact tree-agnostic cuts in a fixed order, recording T after each (an ablation table goes in the note):
   Boolean tables to a fixed point (`truth_simplify`), nine-atom tables (`classical_wide`), conditional-AND
   (`cond_pass` m/f/s; r adds measurements: re-scan the nonce), classical-control passes, stream-bound proved-cut tables.
   Then cheap exact arithmetic edits (carry on a clean flag, chunk-boundary carries erased by measurement).
   **Check the `cond_pass` option string first.** gnuchev's froghop/frogdrop trees call `cond_pass::run_with(ops, "mfs")`
   (his 839 note a45bcccd: "Options u and r (which add measurements) are not used"). On the froghop-one tree, `"mfsr"`
   lowers Toffoli at unchanged width: on our Q818 row it saved 4,173 avg T with 9,024/9,024 clean at nonce 0 (reported in
   our public Q817 note `59359890`). The cost is measurement overhead: +4,180 Hmr ops and classical bits, +12,540 ops. Three mfs/mfsr twins
   received official metrics on 24 Oct (status "rejected: score did not improve current best", the normal status for
   a Pareto row): Q817 59359890 at 9,760,184 (-4,193 vs a655e5d9), Q816 b58b2f57 at 9,804,552 (-4,229 vs 717be455), Q815
   c3aca03a at 9,817,058 (-4,165 vs its mfs build). Rows 813/814 were built with mfsr from the start. The levers keep values by construction
   (cond_pass checks its premises), but equivalence to the evaluator is only sampled. Before nonce selection, run the
   paired fixed-input A/B (step 3) and a trusted-evaluator check, and keep the diagnostic switches (`SL_COND_FAULT`,
   `SL_COND_ALIGN`, `SL_COND_NOGUARD`) off. Grep any tree for `run_with(ops, "mfs")` before you build anything else.
3. Fixed-input A/B against the parent (identical inputs to both circuits): the candidate's failing-shot set must equal
   (or be a subset of) the parent's. Salted rates use different inputs per stream and are only a coarse check.
4. Take the first clean nonce in a pre-declared range, state the failing ones, submit with a templated note (parent,
   edits, delta table, error pairing). When the rival improves the row, run the same cuts on their new tree.

## 2. Transplant harvest (many trees, one session)

Trigger: you hold an exact cut that does not depend on the tree (post-passes, a peephole or cancel index, erasure-box
deferral, a math bound) and rival frontier rows exist across a band, even week-old ones. His 22 Oct morning turned three
cut types into 8 rows across 5 trees; one session submitted 37 rows.

For each row: rebuild the base to its published sha and T, apply the cuts one at a time and together, keep deferral only
for box kinds that stay phase-clean on that lineage, re-pick the nonce (the op stream changed), validate with the
replica, queue it.

## 3. Band sweep (one move, N rows)

Trigger: a new composition or layout has a monotone Q-for-T dial (cap, scratch or carry-pool width, prefix cut, per-step
room).

1. Make every step pool-aware: a cheap form when k free qubits exist, a borrowed form otherwise; expose one constant
   (`CAP`, `POOL_D`) plus count-build env overrides that the official build ignores.
2. Build and measure every width (never project from static counts); stream billion-op count builds
   (`LOWQ_EXACT_STREAM_PATH`). Keep only strictly decreasing rows: a flat dial yields noise, not advances.
3. Pre-register disjoint nonce blocks per row; one source per series (rows differ only in the dial constant and the
   nonce); notes from one template with a per-row "what changed".
4. **Contested first:** submit the widths that beat a rival's live row before your own extensions (21 Oct: 798 first,
   which beat edi3on's 798 from that morning; then 796; then the new floor 793). Stop where the census says the next
   structure binds.

## 4. Lambda ledger

Lambda = failing shots per 9,024, measured over >= 8 pre-fixed corpora with an SE and **paired against the parent on
identical inputs**; pool lambda across a series (one row's 8-corpus figure is noise). Price every approximate or
value-dependent lever, cap move or knob in lambda; buy error back (wider envelopes, exact low-room constructions,
reverting a base's error-for-score knobs) before spending it on width; size a nonce grind as e^lambda tries; copy the
PR 419 contract text verbatim into every note on a line that carries it (term 4).

## 5. Validator envelope preflight

Trigger: any row above ~0.5e9 ops, a parent with pinned drift asserts, or a build outside Linux.

- Raw grader bytes = 56 x ops; keep GBs of margin under the runner's memory (six of his 11 failures sat at 56-58 GB;
  identical artifacts later passed on resubmission). bulengerk's notes show rows of 1.90-2.03e9 ops validating and
  rows of 2.06-2.25e9 ops timing out at the 45-min wall; a local 9,024-shot self-test near 40 min predicts a timeout.
- Turn the parent's `assert_eq!` op/T/width pins into `<=` ceilings (one failure crashed on them); everything-off must
  rebuild the parent byte for byte; two `env -i` builds with identical ops; LF line endings in harness scripts; measure
  post-emission passes on the live emit path, not on count-only builds.
- On "job interrupted" or "agent-compose failed", resubmit the identical artifact once; cancel only to fix a note.

## 6. Throughput

His cadence was ~3 min per row in a series (11 rows in 27 min on 22 Oct). As of 24 Oct the platform allows **one
in-flight submission at a time**, so a series is limited by validation time (~10-15 min per small row, ~40 min per
billion-op row): run one serial queue with a lock and a live-frontier gate before each submit, and stage with
`rsync -c` (a quick-check copy can skip same-size files and resubmit the previous archive).

