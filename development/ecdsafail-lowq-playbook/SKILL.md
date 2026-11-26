---
name: ecdsafail-lowq-playbook
description: "Cut qubits off a low-Q ecdsa.fail stream (about 670 to 950 Q) the way BitWonka's 25 low-qubit rows did in October 2026 (940 down to 671 Q). Census the binding instant, pick the cut, refactor equivalence-first, budget lambda against the clean-nonce supply, and gate on the exact replica. Use when a precision or lane cut raises lambda, or when porting a rival's low-Q cut onto your tree."
---

# Schmalhans (ecdsafail-lowq-playbook)

The loop BitWonka (with Claude Opus 5.5 in Claude Code) ran to take the board's lowest graded Q from 792 to 671 in
twelve days. Every number below is from his public submission notes, cited `prN.md:line`, where `prN` is pull request N in
[Layr-Labs/ecdsafail-challenge](https://github.com/Layr-Labs/ecdsafail-challenge/pulls). Lines, mechanisms and dead ends in full:
[`references/bitwonka-ecdsafail-digest.md`](references/bitwonka-ecdsafail-digest.md) (read its section 2 before
porting any of his trees; section 4 before re-trying a cut).

**Vocabulary.** Q = peak qubits. T = average *executed* Toffoli as graded; emitted T = Toffoli in the op stream.
lambda = expected failing shots per 9,024. The **binding instant** is the op range where every lane is live.
A **clean nonce** is one whose 9,024 shots all pass.

## The loop

1. **Bind and reproduce.** Build the parent from a clean checkout of `main` + `src/point_add` with an empty
   environment, twice; require byte-identical ops (SHA-256), since the Fiat-Shamir shots are fixed by the bytes
   (pr624.md:157-158; pr663.md:246-248). Score it with `ecdsafail-fasteval` and match the parent's graded T to the
   digit before trusting anything you change. Billion-op low-Q builds: stream with `LOWQ_EXACT_STREAM_PATH=<file>` when
   the tree has it (byte-identical to `write_ops`, pr624.md:186-189).
   Done when your parent build reproduces the graded row.

2. **Census the binding instant.** Replay ~2,048 shots and record, per op, which lanes are nonzero on any shot
   (pr653.md:144-148). Locate the ops at the peak and the stage that owns them. If all Q lanes are live together
   (at Q730: ~2,400 ops in AND-ladder and carry-chain bursts), relabelling and parking cannot help: the qubit must
   come from a shorter register. Done when you can name the register the next qubit comes from.

3. **Pick the cut** by what the census says:
   - **Precision knob** (a register whose width is a margin: estimate heads K/KP, digit or quotient width). Change
     only the constant, keep derived offsets consistent (N = 258 + K), evaluate every setting on the *same* paired
     shot sets (60 x 9,024 x 2 divisions), and walk to the knee: lambda roughly doubles per bit, then collapses
     (K 28 -> 23 took lambda 0.72 -> 4.98; K < 23 collapses, pr653-654). Check the second knob's slack first
     (KP 30 -> 24 was flat, pr656-658).
   - **Lend a provable lane.** Bits fixed on every active shot by an identity (the leading one of a size-normalised
     value, always-zero tops, flags constant on parking shots): prove by construction, confirm with a census across
     all columns, gather the bit with a swap tree on its size register, flip to 0, lend, restore (pr697, pr699).
     Store derived quantities instead of registers: a gap instead of two sizes, a counter in a register's known-free
     top lanes (pr550, pr624).
   - **Executed-T harvest** (when T is the price of the Q cut). X-measure a temporary and run its phase fix-up under
     the classical outcome: half the oracle in expectation (a 32-bit compare cleanup 33 -> 16 T, x 1,404 cleanups =
     -23,868 T, pr598.md:67, Codex). Chunked carry banks on clean lanes below the
     peak; signed-digit Horner so adders drop their quantum control; deferred erasure across mirrored forward and
     inverse walks (pr598/601 are Codex inputs, pr602, pr606, pr628). Test with forced measurement outcomes (all 0,
     all 1, mixed) and assert exact executed counts.

4. **Refactor equivalence-first.** Implement the restructure at the old constants and require the same failing
   inputs on fixed hunt seeds (16,384 divisions, 4,096 point adds) and the predicted failure count at the old nonce;
   A/B the switch with identical state at every column boundary on two seeds; add a negative control (remove the
   new piece, confirm the targeted replay fails). Only then apply the cut, keeping a monotone emitted-T ledger per
   stacked change (pr656.md:124-127; pr699.md:74-75, 145-146). Done when old-constant behaviour is bit-identical.

5. **Budget lambda against clean nonces.** Keep a classical integer-model predictor with one failure class per
   approximation, hashed like `eval_circuit`; calibrate it until its predicted failing-shot set equals the replica's
   at some nonce (set-equal in pr697, pr815, pr818). Estimate lambda over >= 1-4M shots with its standard error and
   per-class split. Clean-nonce supply is about `positions x e^-lambda`: lambda 7.1 at 718 positions leaves ~0.6
   clean nonces, which is why KP = 23 was rejected (pr658.md:136-137). When supply drops below ~2, widen the nonce
   from one X-pair to a CX pair `CX(c,t)` applied twice (Q x (Q-1) choices, pr663.md:286-289), or drop the cut.
   The nonce selects a shot set; it leaves true lambda unchanged, so report lambda, not the lucky set.
   Done when a clean nonce is found by scan and confirmed by the replica.

6. **Gate and disclose.** Final number from `ecdsafail-fasteval` (unsalted, harness sha); the note states every
   error trade with numbers, measured versus modelled values, and the PR 419 limiting contract (lambda <= 18, no
   direct error-for-score trades). Publish an erratum when a later predictor finds a miss (pr699.md:129-134 revised
   682's lambda 2.51 -> 2.71).

## Sub-agent split that worked

Split by subsystem, merge in the main session: products / walk / inverse walk (pr602), quotient engine / size
registers and payload / crossing parks (pr697); one design or lane-research agent for a new scheme (pr547, pr699).
His last two entries (pr815, pr818) were single-agent.

## Where his last tree stopped

672/671 Q (pr815/818, base jackylee0424 676 plus odinfree's ring-258 cut). The 664 floor needs one of: a crossing
middle on fewer than 4 spare lanes, R lanes not taken from sx, or an overshoot repair that fits (pr815.md:119-123).
