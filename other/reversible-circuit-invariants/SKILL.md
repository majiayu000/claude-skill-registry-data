---
name: reversible-circuit-invariants
description: Executable invariant checkers for space-efficient reversible arithmetic circuits, derived from eprint 2026/2014 (Jo & Lee, exact in-place modular inversion with 3n/2+o(n) qubits). Use before an ecdsa.fail build/eval/submit, when porting a low-qubit layout (four-hole / omitted-rail ports), when deciding whether an in-place erase relation is a legal permutation, when pricing spooky-pebbled uncomputation offline against a lane budget, or when auditing a candidate circuit's peak/Toffoli/clean-ancilla structure from ops.bin. Fires on "rci", "check the layout", "is this erase legal", "price the pebble", "ops.bin census", "omitted rail audit", "exceptional set".
---

# Ruckwärtsgang (reversible-circuit-invariants)

Turns five checkable claims from **eprint 2026/2014** (Jo & Lee, *Quantum
Discrete Logarithms on Elliptic Curves with 5n/2+o(n) Logical Qubits and
Õ(n²) Toffoli Gates*) into commands you can run **before** spending a build,
an eval, or a submission.

The paper is **asymptotic**: it explicitly leaves concrete constants open
("concrete estimates at cryptographic sizes would require optimizing the
polylogarithmic factors ... and are left open"). So **no numeric result in it
is quotable at n=256**. What transfers is the *invariant structure* — the
lemmas are exact statements at every finite size, and those are what this tool
runs.

## The five atoms

| Atom | Paper | What it decides |
|---|---|---|
| In-place legality | Lemma 5(3), Fig 6 | Is a proposed `x ↦ y` erase relation a legal permutation, and what is the gate recipe? |
| Capacity bounds | §4.1, §4.2, eq (7), (24) | How many lanes does a layout actually need at each lifecycle point? |
| Pebble economics | Lemma 4 | Does recompute-instead-of-store pay at this T/S? |
| Exceptional set | Lemma 12, 13 | Which inputs need the correction path, and how big is it? |
| Exactness / clean ancillas | Definition 1, eq (9) | Do all ancillas return to \|0⟩, and is the branch scalar input-independent? |

## Commands

```bash
rci.py census  <ops.bin>                     # ops, kind histogram, Toffoli, peak Q
rci.py holes   <ops.bin> --lanes 255,256,257,258   # omitted-rail audit  (§2.3/§4.1)
rci.py simulate <ops.bin> [--set q,q] [--max-ops N]  # X/CX/Swap/CCX bit sim
rci.py inplace --A A --B B --C C --m m       # Lemma 5(3) classify + brute-force prove
rci.py capacity --n 256 --b 8 [--u U --v V]  # eq (7) sizes + combined-length bounds
rci.py pebble  --T T --S S [--max-blowup 4]  # Lemma 4 cost + viability verdict
rci.py exceptional --p P --a A --b B --u U --v V   # exceptional set, |E| <= 8
```

Hex accepted everywhere (`--p 0xFFFF...`). Exit **0 = pass, 1 = FAIL**.

`ops.bin` is the challenge format: magic `QECCOPSZ`, `u64_le` op count, zstd
body of 56-byte records. Needs the `zstd` CLI on PATH.

### Real op streams go through `rci_scan`, not the Python loaders

A full ecdsa.fail circuit is **~1.23e9 ops / ~69 GB decompressed**. The Python
`census` / `holes` / `simulate` paths read the stream into memory and will OOM on a
real build — they are for small/synthetic streams and for the lemma math. For anything
real, build the native scanner once and pipe:

```bash
rustc -O --edition 2021 -o rci_scan rci_scan.rs
tail -c +17 ops.bin | zstd -d -c | ./rci_scan --lanes 255,256,257,258
```

It streams, has zero dependencies, and is validated identical to the Python path on a
synthetic stream. `tail -c +17` skips the 16-byte magic+count header.

## The four things this is for

**1. Omitted-rail audit (the four-hole class of bug).** When a low-qubit layout
omits tail rails (`work1[255..258]`), every downstream function must be
*unaware* of them. The campaign hit exactly this: `four_hole()` was wired into
5 functions and ~15 core functions still indexed `W1[255]`. `holes` mechanizes
the detector over the *emitted* stream, so it catches every toucher at once
instead of one panic per rebuild.

**2. Erase-relation legality (the −49% T question).** The claim "we can erase
the second EEA traversal using a linear relation" lives or dies on whether
`x ↦ y` under `Ax + By = C` is a permutation. `inplace` builds the paper's
recipe and **brute-force proves or refutes it** at small `m`:
- both coefficients odd → `x ← B⁻¹(C − Ax) mod 2^m`
- only B odd → y₀/D₀ detour, **rotate LEFT by α**, XOR y₀
- only A odd → x₀/D₀ detour, **rotate RIGHT by β**, then odd affine
- `2^ν ∤ C` → no integer solutions, identity permutation

The rotation gadget is the transferable part: it handles a power-of-two
valuation **without extending the target register**. Note eq (12) is an
*integer* relation, not a congruence — reading it as `mod 2^m` is the trap.

**3. Pebbling priced offline.** Lemma 4: `T²/S + T` Toffoli with `O(S)`
ancillas. The whole trade is `T/S` — the program is recomputed ~`T/S` times.
Use this **before** proposing "spooky-pebble that structure to save qubits".
At campaign scale this is usually a KILL: a 335M-op traversal with ~257
working bits has `T/S ≈ 1.3e6`, i.e. a 1.3-million-fold Toffoli blowup.
Pebbling pays only when a working bit is reused few times.

**4. Pre-submit certificate.** `census` + `simulate` recompute peak Q and
Toffoli from the ops stream independently of the builder's own report, and
report any qubit still \|1⟩ at the end — the paper's Definition 1, made
executable for X/CX/CCX streams. Cheap insurance against an invalid submit.

## Guardrails

- **`census` gives EMITTED counts. The scored metric is EXECUTED. These differ.**
  `eval_circuit` scores `round(avg executed Toffoli) × qubits`
  (`src/bin/eval_circuit.rs:361` computes `toffoli_gates / n_shots`; `:434` rounds and
  multiplies). A static scan counts every emitted CCX, including ones whose control is
  0 and which therefore never execute. Measured on the Q793 stream: emitted CCX
  **680,867,466** against the board's scored **671,273,994** — a **1.41%** gap.
  Consequences to hold onto:
  - **Never claim a T saving from `census`.** Only a 9024-shot eval produces the scored
    number, and it is shot-dependent (`round()` of an average with real variance).
  - **A whole class of lever is invisible here**: one that changes *which* CCX execute
    without changing how many are emitted shows a **zero** delta in `census` while moving
    the score. Absence of a delta is not absence of an effect.
  - What `census` *does* give soundly: **peak qubit id** (the Q axis, exact and static —
    792 → Q793 matched the board exactly) and the **op count** against the `MAX_OPS` cap.

- **Omitted-rail audit watches id `4294967295`, not 255–258.** `omitted_lane_marker()`
  sets `id: u32::MAX` (`circuit.rs:29-31`), distinct from `NO_QUBIT = u64::MAX`
  (`circuit.rs:94`). Watching low ids checks ordinary pool qubits and proves nothing.
  A clean result also falls out for free: if **peak qubit id < 4,294,967,295**, no op in
  the stream can reference a marker. Use `--lanes 4294967295`.

- `simulate` is sound **only** for X/CX/Swap/CCX streams; it reports
  unsupported kinds rather than silently mis-modelling them. Do not read a
  `sound: true` as a correctness proof — it is a *clean-ancilla* check, and a weaker one
  than the evaluator's, which tests every non-register qubit on every live shot
  (`eval_circuit.rs:340-357`). Use the evaluator as the authority.
- `inplace` brute-forces, so it is capped (`--max-bits`, default 12). A pass at
  `m=12` is evidence for the recipe, not a proof at m=257; the recipe itself is
  what the paper proves, the tool is a transcription check.
- **No number from the paper is quotable at n=256.** `capacity` bounds are
  exact but asymptotic in their slack constants (`8b + 16`). Treat outputs as
  *structure*, and price any actual lever with the campaign's own measured
  estimator.
- Never report a saving as measured until it is measured on 9024 or
  byte-identical ops.

## Provenance

Paper: eprint 2026/2014, Jo & Lee (Georgia Tech / QED Audit), approved
2026-09-14. Its ref [19] is the ECDSA.Fail autoresearch paper — this is
downstream literature responding to the same benchmark.
