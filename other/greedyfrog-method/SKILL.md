---
name: greedyfrog-method
description: BitWonka's greedyfrog process, reconstructed so we can repeat it. Use when redesigning a reversible traversal or inversion (ecdsa.fail Euclid / GCD walk) so the state carries its own reverse decisions instead of a history stack, when building, porting or moving greedyfrog rows (825 / 815 / 849 trees, cap-dependent family), or when asked how greedyfrog was invented.
---

# Gumpifrosch (greedyfrog-method)

Greedyfrog (BitWonka, ecdsa.fail, 27-28 Oct 2026) replaced froghop-one's inversion traversal inside an unchanged
point-add shell: 903 slots plus a quantum quotient stack became 254 uniform slots and no stack. First row 825 x
6,107,471; same-width refinement 825 x 5,485,974 (-10.2 %). The leading word of the method is **self-describing
state**: pick the forward step and the register layout together so that the state after a step already contains the
instruction for undoing it. Fast forward step without that = you still pay for history; stackless reverse without a
fast step = you still pay for alignment. Greedyfrog has both halves.

The mechanism, concretely: state (A, tA), (B, tB) with invariant `A*tB + B*tA = p`, start (p, x', 0, 1). Each step
keeps A and B top-aligned, subtracts the largest power-of-two multiple of B that fits (`e = bl(A) - bl(B)`,
`d = [(B << e) > A]`, `A -= B << (e-d)`, `tA += tB << (e-d)`), renormalises, swaps if 0 < A < B. Within one Euclid
level `tA = t0 + Q*tB`, so the last applied digit is `lowest_set_bit(floor(tA / tB))`: the growing cofactors encode
the history. The inverse reads 28-bit cofactor windows, runs up to 21 non-restoring division rows and finds the last
set row. Inputs are reflected (`x' = min(dx, p - dx)`) to kill the first-quotient-1 ambiguity (75 % shot failure
without it). Classical X-measurement records remain for phase repair only.

## Steps (each ends on its output; do not start the next without it)

1. **Freeze the baseline and the component boundary.** Rebuild the parent row from its commit with an empty
   environment until its `ops.bin` sha256 matches the note; find the active dispatcher for the component you will
   replace. Output: byte-exact baseline stream + the interface the new component must satisfy.
2. **Cost the structure, not the constants.** Split the component's cost into useful arithmetic, alignment /
   routing, stored decisions, inverse cleanup, peak workspace. Output: a one-sentence bottleneck with a measurable
   prediction ("~900 alignment slots and the quotient stack dominate width and Toffoli").
3. **Design forward and reverse rules together.** Search for an invariant, monotone quantity or cofactor that
   identifies the previous operation; choose a layout that makes the forward step local and the reverse decision
   cheap; enumerate ambiguity cases now. Output: recurrence + invariant + decoder + preconditions, checked by an
   unwindowed integer script exhaustively on small primes (e.g. all inputs mod 101 and mod 65,537) and on a few
   thousand random secp256k1 inputs, zero assertion failures.
4. **Keep two executable models.** An integer model (`Spec`) and a physical lane model (`Lanes`: markers,
   wrap-around, control bits), compared after every step. Output: a per-step equality test passing on >= 200 walks,
   able to name the first divergent step.
5. **Census the walk before fixing the schedule.** Per-slot active fraction, operand lengths, rotations, row counts
   and tails from 200,000 walks (fit), then a fresh corpus (test). Derive windows and per-slot row budgets from the
   census; keep generator version, seed and margins. Output: a committed envelope file + a categorised fresh-input
   failure estimator (greedyfrog: 70 failing divisions / 200,000 walks -> about 6.3 failing shots per 9,024).
6. **Build the smallest checkable cell.** One forward slot against the lane model, then forward/inverse round
   trip with zero phase and clean scratch, then borrowed lanes randomised and restored. Output: cell tests that
   catch a deliberately wrong forward mutant (a round trip alone hides a wrong forward function).
7. **Integrate through the shell interface and replay concrete failures.** Run the trusted evaluator; replay
   every failing shot's exact inputs through the model (his first full build failed shot 7806: too few division
   rows in one slot; fixed for ~180k Toffoli). Output: each failure classified as recurrence bug, implementation
   mismatch, or window exit.
8. **Profile the binding phase.** Per-section live high-water marks and Toffoli; cut width where it binds
   (greedyfrog 815: inverse decode on idle passenger lanes via borrowed-lane ANDs). Output: a before/after section
   table with the new peak.
9. **Parameterise by the cap.** Clean pools where room exists, borrowed lanes or recomputation where it does not,
   carry pools only while used. Output: one emitter that builds at >= 3 caps (his G3 / G4 are one-line cap changes
   of G2: 849, 815, 825).
10. **Price the error budget explicitly.** Every emitter shortcut gets a predicate in the predictor (his G1
    `act_const` shortcut was not added to the predictor: the gap to avoid). Output: a fixed-input A/B against the
    parent where the shots that fail outside the predicted set number zero.
11. **Prescreen nonces on the exact stream, then bind the real evaluator.** Finalise the gate list first; the
    scanner hashes the prefix once and varies the 48-bit identity tail (96 X ops). Output: first clean value in scan
    order, trusted `eval_circuit` all 9,024 OK, an independent twin build with the same sha256.
12. **Write the note as mechanism + limits.** Invariant, layout, census provenance, profile, constants, results at
    several caps, what is not proven. Output: a note another worker can reproduce from, >= 5,200 bytes, in our
    own words (never paste inherited notice blocks).

## Working on greedyfrog trees

Sources (Layr-Labs/ecdsafail-challenge; all five are validator snapshots with the same parent `2120d8a2`; code
lineage is SnehalRaj's shell `ab98dd15` / commit `38bf9d65`, a +3,265 / -11 line delta ignoring line endings):

| row | Q x T | commit | ops.bin sha256 (note) |
|---|---|---|---|
| G0 `39ef23e2` | 825 x 6,107,471 | [7e5e7712](https://github.com/Layr-Labs/ecdsafail-challenge/commit/7e5e77120238d805e2e55ed06e193e97e07790d9) | 26a667bf...b516b6 |
| G1 `ec1e870b` | 815 x 6,792,761 | [4cd9e8da](https://github.com/Layr-Labs/ecdsafail-challenge/commit/4cd9e8da2666c904df3744d47ebf4ab5c66aa9b3) | f7a8573b...50cd41 |
| G2 `954016db` | 849 x 4,918,479 | [7e0933a1](https://github.com/Layr-Labs/ecdsafail-challenge/commit/7e0933a1b6a525c795e19cb6290c2ddaa1e02aed) | 9778ab2b...fc86d5 |
| G3 `73799fca` | 815 x 6,360,721 | [2885dc51](https://github.com/Layr-Labs/ecdsafail-challenge/commit/2885dc5100da4bd3c5c3d9a0e5a5a84131552ac3) | 968ff62c...43b5b2 |
| G4 `1d06c635` | 825 x 5,485,974 | [a5f1fa59](https://github.com/Layr-Labs/ecdsafail-challenge/commit/a5f1fa59e879ad9a018d4d5e4903e720097072bf) | 4b00ddad...250006 |

Fetch with `git fetch origin <commit>` in a challenge checkout. New files: `greedyfrog.rs`, `greedyfrog_model.rs`,
`greedyfrog_diag.rs` (predictor + nonce scanner, test-only), `greedyfrog_data/env.txt`, `pointadd_greedyfrog.rs`.

Entry points (tests live in `--bin build_circuit`; the expensive bodies return early unless their variable is set,
so a green `cargo test ... greedyfrog_` does not prove they ran):

| purpose | command / setting |
|---|---|
| gate-level suite (13 tests, ~1 s) | `cargo test --release --bin build_circuit greedyfrog_` |
| whole traversal | `GREEDYFROG_TRAV=1` + `greedyfrog_traversal_gate_level` |
| section profile | `GREEDYFROG_PROF=1` (+ `GREEDYFROG_SLOTS`) |
| G2-family caps in tests | `GREEDYFROG_TEST_CAP=583 / 593 / 617` for shell caps 815 / 825 / 849 (232 below) |
| fresh failure rate | `GREEDYFROG_DIAG_N=200000` + `greedyfrog_diag_rate` |
| replay the emitted packet | `GREEDYFROG_DIAG_OPS=<ops.bin>` + `greedyfrog_diag_shots` |
| nonce scan | `GREEDYFROG_SCAN_OPS=<ops.bin>`, `GREEDYFROG_SCAN_START/MAX/WANT` + `greedyfrog_nonce_scan` |

Measured on his trees (our own scout lane, 28 Oct 2026):
- 815 = rings 2 x 258 + passenger 256 + LA, LB 2 x 9 + reflection 1 (791 base) + 24 slot scratch; binders: late
  inverse sweep / rows undo 815, cofactor ladder 814, value ladder and swap decode 813, shell products
  777 + c0 + k + pool >= 34 = 813.
- Gotchas: upstream files are CRLF (patch tools turn them LF: harmless, mention it); `FH_CK` only prints;
  `greedyfrog_env.txt` is a test output, not read by the build; the default model test decodes with (32, 22), the
  circuit with (28, 21); A/B phase-only one-sided shots appear in both directions because measurement words follow
  each circuit's own measurement count.

## What the evidence does not show

The private chronology, prompts, Python prototypes (`greedyfrog1.py`, `greedyfrog2.py`, `prefilter-shadow/
predict_fast.rs` are named in comments, not published), the human / model split, and any use of loop-engine or
fasteval for this design. State these as unknown; resemblance to Stein, plus-minus or Brent-Kung is ours, not his.

## Sources not bundled

The forensic report behind this skill (timeline, diffs per refinement, citations, nonce table) is a campaign
record and is not part of this copy. The commits and notes it cites are public: see "Sources" above.
