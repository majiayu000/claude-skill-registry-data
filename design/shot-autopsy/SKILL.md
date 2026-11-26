---
name: shot-autopsy
description: "When a candidate fails shots its parent passes, find the structural cause before any nonce search. Reconstruct the exact failing shot, localize the first divergence, repair it by paying precision, and keep the case as a permanent regression. Learned from bulengerk's ecdsa.fail rows. Use when an edited candidate fails shots its parent passed, or when counts drift between builds."
---

# Liicheschau (shot-autopsy)

An **autopsy** turns a candidate-only failing shot into a named defect and a permanent regression case before anyone
reaches for a new nonce. bulengerk's lanes were exact transformations on an inherited approximate circuit: his notes
keep the base's approximations and its historical modeled lambda (2.52) and disclaim universal correctness. Within that
frame his notes report no nonce search: he inherited the base's nonce literally (4 on frogdrop, CX(5,2) on jackylee's
line) and repaired the failing shots he met (Q772 shot 7926; Q770 shots 614, 5732, 7689; Q660 cases 63, 4543, 5284),
growing a regression set from 256 to 320 cases. Cites: [EVIDENCE.md](EVIDENCE.md).

## Use it / leave it

- Use when an edited candidate fails shots its parent passes, or a fixed-input A/B (identical inputs to parent and
  candidate) shows failures only the candidate has: that is a structural bug, approximate circuit or not.
- Leave failures the parent shares (the circuit's designed lambda) to nonce screening and lambda budgeting
  (`ecdsafail-lowq-playbook` step 5); the runtime wall and op budget to `ecdsafail-pareto-ratchet` §5.

## Steps

1. **Separate candidate-only failures first.** Run a fixed-input A/B of parent and candidate on the same inputs
   (`FE_FIXED`-style shots). Done when every candidate failure is tagged "shared with parent" or "candidate-only".
   Only candidate-only failures continue here.
2. **Capture the whole failing shot.** Record the stream and evaluator hashes, the canonical field encoding, the index
   of the accepted input, the batch and lane, the XOF continuation and the measurement draws
   (`eval_circuit.rs:248-295`, `sim.rs:140-153`). Inputs alone do not reproduce a phase failure. Done when a standalone
   run reproduces the failure and its channel (classical, phase or ancilla).
3. **Localize the first divergence.** For classical failures, replay against an independent integer model per column
   or step. For phase and ancilla failures, add a phase and ancilla trace; an integer model cannot see them. Done when
   the divergence is named: stage, bound, register.
4. **Repair by paying precision.** Widen the bound that failed (his examples: head 24 -> 25, crossing head 32, window 32
   -> 33) or add exact repair arithmetic; record the T paid. Done when the captured shot passes.
5. **Keep it forever, then requalify.** Append the case to a permanent fixed regression set and confirm the runner
   actually executes it (a negative control: the unrepaired build must fail it). Run the regression set and component
   checks before any expensive run, then a full 9,024-shot replay on all three channels. One passing nonce shows that
   packet is clean; it does not show equivalence or that lambda is preserved. Done when the regression set passes, the
   negative control fails, and the full replay passes.

## Why the full rerun is never optional

Any edit changes the Fiat-Shamir validation population even when the literal nonce is unchanged (his ed89218e note).
His June note shows the trap: dead gates appeared inactive on 512 sampled shots, and the modified stream failed after
reseeding.

## The submission note as a record

State the executed mean as exact sum / 9,024, emitted vs executed T, the immediate parent's id and commit, the
inherited nonce, three SHA256s (source manifest, stream, archive), and the negative claims ("no nonce or seed search",
"no new lambda estimate"). Copy the inherited limiting contract (PR 419 terms 1-4) verbatim. Submission stays closed
until the live gates pass; a clean nonce grants nothing on its own.

## Sources

[EVIDENCE.md](EVIDENCE.md), which cites bulengerk's public submission notes by submission id and note line.
