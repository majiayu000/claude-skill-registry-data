---
name: ecdsafail-fasteval
description: "Score an ecdsa.fail ops.bin exactly like the official eval_circuit (same Fiat-Shamir shots, totals, failure counts and score) in minutes, at about 20 bytes per op instead of 56. Uses BitWonka's fasteval. Use when a circuit is too big for eval_circuit on your machine, when you need an official-equivalent score before submitting, or when you need a circuit's failure rate from fresh salted shots."
license: MIT
---

# Schnällrichter (ecdsafail-fasteval)

*fasteval*

BitWonka's exact replica of the challenge's `src/bin/eval_circuit.rs`, from
[BitWonka/ecdsafail-tools](https://github.com/BitWonka/ecdsafail-tools) `fasteval/` (commit `9f92470`, 11 Oct 2026).
Clone it with `git clone https://github.com/BitWonka/ecdsafail-tools` and check out `9f92470`.
The tool's repository has no licence file, so use it from your own clone and do not redistribute its `.rs` files.

**Why it is exact while parallel.** `eval_circuit` draws everything from one SHAKE256 stream seeded by the op list's
Fiat-Shamir hash. The first 64 x 9,024 bytes make the shots; after that every `R`/`Hmr` op reads 8 bytes per 64-shot batch
whether or not it executes. So batch `b`'s measurement bytes always sit at `64*9024 + 8*M*b` (M = number of `R`/`Hmr`
ops). One thread squeezes the stream in order; worker threads simulate the 141 batches in parallel on 20-byte packed ops.

**Memory budget:** about `20 B x ops + 8*M B x (workers + queued batches)`, plus ~1 GB fixed for the loader's
4M-op chunks of 56-byte records (`CH = 1<<22`, two 3-deep channels), so the saving only shows on big circuits. The official evaluator holds 56 B/op, so a
1.24e9-op low-Q build needs ~69 GB there and ~33 GB here (fits on a 48 GiB Mac); 1.78e9 ops needs ~100 GB there.
This fixes the evaluation side only: the official `build_circuit` still collects `point_add::build()` into a `Vec<Op>`
at 56 B/op before streaming it to zstd (`src/bin/build_circuit.rs:92`), so producing a 1.24e9-op `ops.bin` still
needs ~69 GB (a big-RAM pod) unless the tree streams: BitWonka's low-Q trees honour `LOWQ_EXACT_STREAM_PATH=<file>`,
which streams ops to disk byte-identically to `write_ops` (his PR 624 note, lines 186-189). The official runner has
128 GB.

## Steps

1. **Bind to the checkout that built the circuit.** Copy the two sources into that checkout and build:
   ```bash
   T=<your ecdsafail-tools clone>/fasteval
   cp "$T"/fasteval.rs "$T"/gensynth.rs <checkout>/src/bin/
   cp "$T"/validate.sh <checkout>/
   cd <checkout> && cargo build --release --bin fasteval --bin gensynth --bin eval_circuit
   ```
   Keep these three files out of the submission commit; they are analysis tooling.
   Done when `target/release/fasteval` exists.

2. **Gate on the harness revision.** Run the differential test once per harness revision, and again whenever any of
   `src/bin/eval_circuit.rs`, `src/circuit.rs`, `src/sim.rs`, `src/weierstrass_elliptic_curve.rs`, `Cargo.toml`
   changes (check with `git log -1 --format=%h -- <those files>` on a full-history checkout, or
   `gh api "repos/Layr-Labs/ecdsafail-challenge/commits?path=<file>&per_page=1"`):
   ```bash
   bash validate.sh 200000 11 22 33
   ```
   It builds random `ops.bin` circuits (every op kind, nested conditions, `R`/`Hmr` under conditions), runs both
   evaluators, and compares the four correctness counts plus avg Toffoli, avg Clifford, qubits and op count from the
   `results.tsv` row (restored afterwards). Done when it prints `all seeds match`. Any `MISMATCH` means fasteval does not
   speak for this harness: stop using it here and report the diff.
   Random circuits fail on every shot, so this checks gate semantics, executed-gate accounting and measurement-stream
   alignment; the passing path was checked by BitWonka against four graded logs (732-739 Q, matched to the last digit).

3. **Score.**
   ```bash
   FE_THREADS=6 ./target/release/fasteval path/to/ops.bin
   ```
   Read `avg executed Toffoli`, `qubits`, the failure counts, `failing shots (any)` and the final score
   (`round(avg executed Toffoli) x qubits`, as `score.json` computes it). More threads mostly add memory: the single
   SHAKE producer is the bottleneck.

4. **Estimate the true failure rate** when lambda decides the row (the board's social norm since PR #419 is <= 18, later
   19.5, expected failing shots per 9,024). Run fresh salted shot sets and average `failing shots (any)`:
   ```bash
   for s in $(seq 1 20); do FE_SALT=$s ./target/release/fasteval ops.bin | grep 'failing shots'; done
   ```
   lambda = mean; standard error = sd / sqrt(runs). Salted scores are not the official score.

5. **Report with the label.** Write numbers as `fasteval (unsalted, harness <sha>)` or `fasteval FE_SALT x20`, never as
   the official score. The submission is scored by the official runner; fasteval is the local prediction.

## Differences from eval_circuit

- Prints totals even when shots fail (`eval_circuit` stops at the first failing batch), and adds
  `failing shots (any)` (wrong output, phase error or dirty ancilla; `eval_circuit` counts failing batches).
- Writes no `score.json` or `results.tsv`.
- One unsalted run uses the same 9,024 shots as the grader, so its pass/fail on those shots is the grader's.

## Verified here

24 Oct 2026, Layr-Labs/ecdsafail-challenge HEAD `6b0327d`: `validate.sh 200000 11 22 33` -> all seeds match
(200k ops, 700 qubits, avg Toffoli 26,775 / 27,583 / 27,368), 47 s wall including the build on a 16-core, 48 GiB Mac.
A full circuit, same day: a 10.1M-op, 1,156-Q `ops.bin` without a clean nonce
gave identical counts from both evaluators (13 classical mismatches, 10 phase-garbage, 0 ancilla, same first failing
shot 610 with the same got/exp points); fasteval 4.0 s / 1.29 GB RSS vs eval_circuit 13.5 s / 0.58 GB (fixed loader
overhead dominates at 10M ops). The billion-op memory claim (33 GB at 1.24e9 ops) is BitWonka's, not re-measured here.
BitWonka's own pin: harness `c672dda` (11 Oct). On `main` the five harness files last changed
22 Jun 2026 (`c66c958`: `eval_circuit.rs`, `Cargo.toml`; `circuit.rs`/`sim.rs` 29 May), so the pin and `6b0327d` run
the same evaluator.

## Sibling tool in the same repo

`dead-ccx-finder/`: a bit-sliced screen for CCX/CCZ that are charged but never fire (`cond & c1 & c2 == 0` on all
~9M inputs); removing them is value-neutral. Workflow and caveats: its `README.md`. After any op-stream edit, regenerate its index: a stale absolute index drops the
wrong ops (see `circuit-edit-integration-safety`).
