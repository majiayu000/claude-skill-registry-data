---
name: tools-creusot-coq-install
description: Add Coq 8.20 as an additional prover to an existing Creusot installation, for verification conditions that SMT solvers cannot discharge
argument-hint: (no arguments needed)
---

## When do you need this?

Creusot's SMT solvers (alt-ergo, z3, cvc5, cvc4) handle the vast majority of
verification conditions automatically. Coq is needed only for goals that fall outside
their decidable fragment — most commonly **modular arithmetic with a variable divisor**,
e.g. proving `(a - b) % n = 0` given `a % n = 0` and `b % n = 0` for a runtime `n`.

Coq does not replace the SMT solvers — it complements them for the rare hard goals.
Run `tools-creusot-install` first if Creusot is not yet installed.

---

## Prerequisites

- Creusot already installed (`cargo creusot version` succeeds)
- opam switch at `~/.local/share/creusot/_opam` exists (created by the Creusot installer)

---

## Installation Steps

All steps run inside the existing Creusot opam switch — no separate switch needed.

### Step 1 — Activate the switch

```bash
eval $(opam env --switch=/home/cornel/.local/share/creusot --set-switch)
```

### Step 2 — Install Coq 8.20.1

```bash
opam install coq.8.20.1 -y
```

Takes 10–20 minutes — Coq compiles from source against the switch's OCaml 5.x.
Verify: `coqtop --version` should print `The Coq Proof Assistant, version 8.20.1`.

### Step 3 — Compile Why3's Coq support libraries

Why3 ships Coq `.v` source files for its integer/modular arithmetic theories.
They must be compiled against the installed Coq before Why3 can use them.

```bash
WHY3_COQ_SRC=~/.local/share/creusot/_opam/.opam-switch/sources/why3/lib/coq
WHY3_COQ_DST=~/.local/share/creusot/_opam/share/why3/coq

find $WHY3_COQ_SRC -name "*.v" \
  | grep -v "real/Truncate\|real/Trigonometry\|ieee_float\|floating_point" \
  | sort \
  | while read f; do
      rel=${f#$WHY3_COQ_SRC/}
      dir=$(dirname $rel)
      mkdir -p $WHY3_COQ_DST/$dir
      (cd $WHY3_COQ_SRC && coqc -R . Why3 "$rel" 2>/dev/null \
        && cp "${rel%.v}.vo" "$WHY3_COQ_DST/${rel%.v}.vo" 2>/dev/null)
    done

echo "8.20.1" > $WHY3_COQ_DST/version
```

Expect ~51 `.vo` files compiled. The floating-point theories are excluded because
they require the Flocq library which is not needed for our proofs.

### Step 4 — Register Coq in `~/.config/creusot/why3.conf`

This is the config file `cargo creusot` uses. Add the following block (after the
existing `[partial_prover]` entries):

```ini
[prover]
command = "/home/cornel/.local/share/creusot/_opam/bin/coqtop \
           -batch -R /home/cornel/.local/share/creusot/_opam/share/why3/coq \
           Why3 -l %f"
driver   = "/home/cornel/.local/share/creusot/_opam/share/why3/drivers/coq.drv"
editor   = "coqide"
in_place = false
interactive = false
name     = "Coq"
shortcut = "coq"
version  = "8.20.1"
```

Also change `memlimit = 1000` to `memlimit = 0` in the `[main]` section.
**Why:** OCaml 5.x (used by Coq 8.20) reserves ~64 GB of virtual address space
for its GC at startup. Why3's default 1 GB memory limit kills the process before
it starts. Setting `memlimit = 0` disables the limit; physical RAM usage remains low.

### Step 5 — Add Coq to the verification crate's `why3find.json`

```json
"provers": [ "alt-ergo", "z3", "cvc5", "cvc4", "Coq@8.20.1" ]
```

### Step 6 — Verify

```bash
eval $(opam env --switch=/home/cornel/.local/share/creusot --set-switch)
WHY3_COQ=~/.local/share/creusot/_opam/share/why3/coq
echo "Require Import Why3.BuiltIn. Check True." \
  | coqtop -batch -R $WHY3_COQ Why3
```

No output = success. Coq is now available as a prover.

---

## Writing a hand-written Coq proof

Coq in this setup runs in **batch replay mode** — it does not discover proofs
automatically. A human writes the proof once using Coq tactics; why3find then
replays it on every subsequent `cargo creusot` run.

For goals where you want automatic proof discovery, consider installing
**CoqHammer** (`coq-hammer` via the coq-released opam repo + E-prover).
CoqHammer calls external ATPs and reconstructs proofs automatically.

### Workflow

1. **Generate the `.v` file** Why3 would produce for the failing VC:
   ```bash
   WHY3=~/.local/share/creusot/_opam/bin/why3
   WHY3_DRV=~/.local/share/creusot/_opam/share/why3/drivers/coq.drv
   $WHY3 prove --driver $WHY3_DRV --output /tmp/coq_goals my_theory.why
   ```

2. **Fill in the proof** between `Proof.` and `Qed.` using Coq tactics:
   - `lia` — linear integer arithmetic (handles `+`, `-`, comparisons)
   - `ring` — ring equalities, rearrangement with `*`
   - `unfold <def>; lia` — unfold a definition, then discharge with lia
   - See `tools/creusot/certus-segment-verif/coq/mod_sub_lemma.v` for a full example

3. **Verify** the proof compiles:
   ```bash
   coqtop -batch -R $WHY3_COQ Why3 -l my_proof.v
   # No output = proof accepted
   ```

4. **Bridge into Creusot** via a `#[trusted]` lemma:
   ```rust
   // Proved by hand in Coq — see coq/my_proof.v
   #[trusted]
   #[logic]
   #[requires(n@ > 0)]
   #[requires(a@ % n@ == 0)]
   #[requires(b@ % n@ == 0)]
   #[ensures(result)]
   fn lemma_mod_sub(a: usize, b: usize, n: usize) -> bool {
       pearlite! { (a@ - b@) % n@ == 0 }
   }
   ```

5. **Call the lemma** at the point in the proof where the fact is needed:
   ```rust
   proof_assert!(lemma_mod_sub(remaining, length, ss));
   ```

### What `#[trusted]` means

`#[trusted]` tells why3find to assume the postcondition without discharging a VC
for the function body. It is not a cheat — the Coq `.v` file is the evidence.
This is the standard practice in hybrid SMT + ITP verification workflows.
