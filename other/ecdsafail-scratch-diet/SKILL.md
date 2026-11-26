---
name: ecdsafail-scratch-diet
description: "Exact qubit cuts for low-Q ecdsa.fail trees. Run a known-bit census, then replace every clean-scratch use at the binding instant with a borrowed lane, a literal or a re-encoding, or move a register into another register's provable gap. Built from gnuchev's October cuts and our own public 793-to-791 and 815-to-811 rows. Use when the next qubit must come off, or when a stage panics with 'scratch pool exhausted'."
---

# Hungerkur (ecdsafail-scratch-diet)

Every one of these cuts is **exact** (same function, lambda unchanged) and costs Toffoli; on the Pareto board that is the
right trade whenever the next point to the left sits far higher in T. Evidence: gnuchev's notes, digested with cites in
[`references/gnuchev-oct-lowq-digest.md`](references/gnuchev-oct-lowq-digest.md). "Our" rows are odinfree's public submissions
Q792 `904784f8`, Q791 `5b3426f9` and Q814-811 `e34a920c`, `5dd48c43`, `e46c4469`, `106eabd8`; their notes carry the details.

## 1. Known-bit census (before any cut)

Replay the stream (or the integer model) on 2,048-8,192 shots and, per step entry and per **shot class**, list:

- **all-shot constants**: bits classical for every shot in a slot (e.g. pi's low bit = the slot parity): take them out of
  the register (gnuchev: store h = pi >> 1, 794 -> 793 and T *fell* at every width);
- **envelope-zero lanes**: |0> on every shot that is still on-model in a column envelope: host AND-carries or decoder
  levels there (a shot outside the envelope already fails, so no new error);
- **selected-shot-clean lanes**: |0> only on the shots a gate selects: host decoder levels or masks only under that gate;
- **spare codes**: joint codes of the bookkeeping lanes that no class uses at a step (our 791: AL, RT and DONE shots all
  carry depth 0, so p0 p1 p2 dep0..4 have spare codes at every step).

Then name the binding instant(s) (every op range where all lanes are live) and the register the next qubit must come
from. If no lane is free at **every** binding occurrence, relabelling cannot help.

## 2. The diet catalogue (pick per site; keep the cheap form when the pool allows it)

| site needs a clean lane for | exact replacement | seen in |
|---|---|---|
| decoder prefix levels | multi-controlled X on *borrowed* dirty passenger lanes (restored) | gnuchev 799->794 |
| an adder's carry wire | Takahashi-Tani-Kunihiro in-operand ripple; carry-out XOR'd into the top lane via one borrowed lane | gnuchev 799->794; our 793->792 (masked TTK ladders) |
| a flag held across a step | XOR sum of AND terms (po = CO ^ CO.A ^ CO.B ^ CO.A.B), never stored | gnuchev |
| a counter update under a flag | inclusion-exclusion: literal-controlled increments | gnuchev; our 791 (S4) |
| a conditional involution's control | hold it in a borrowed qubit of unknown value: (g?R); g^=F; (g?R); g^=F, valid when R preserves F | gnuchev 775->774 (flag-free modular add); our 791 (SC scan, S5 swap) |
| a mask lane per ladder | permute the bookkeeping lanes before the ladder so one lane is 0 on exactly the classes whose result the ladder uses | our 791 (E2/E3/E6/E8 codes) |
| a decrement that may wrap | do it unconditionally, then repair the wrapped shots with a swap reachable only for them | gnuchev |
| a constant-0 lane | re-host each use on a lane that is idle and |0> at that moment | gnuchev 775->774 |
| a stack or counter register | relocate into another register's provable headroom (gap), one-hot scans over per-slot windows sized on 1M simulated divisions; move counters into registers dead for terminated shots | gnuchev 843->819, 839->818 |
| a long decoder held through a slot | short retained decoder (n-2 prefix lanes + one CCX toggle); addends formed just in time | our 815->813 |

Make every step **pool-aware**: the base's cheap form when its free-pool threshold is met, the diet form otherwise. The
pool size then becomes a dial (see `ecdsafail-pareto-ratchet`, band sweep) and larger pools still emit the earlier rows
bit for bit.

## 3. Gates (all of them, every row)

1. **Equivalence first:** with the old pool the new source reproduces the parent's ops sha256 bit for bit.
2. **Small-size exhaustive** check of each replacement kernel against the original (all inputs, all call shapes), then a
   **slot-level integer-model test** of the traversal at every slot boundary (registers, phase, dirty lanes restored) on
   many seeds; plus forward-inverse identity and an end-to-end run.
3. **Negative controls:** one mutation per rewrite site must make the model test fail.
4. **Fixed-input A/B** vs the parent (48 seeds x 9,024 identical inputs): no shot fails only on the candidate. State
   lambda paired, and any invariant a rewrite relies on (which classes reach a step, which lanes are zero there): those
   make "no new failure source" a measured bound, not a theorem.
5. Two `env -i` builds with identical ops; nonce = first clean count.

## 4. Price list (Toffoli per qubit removed)

gnuchev froghop-double pool 7->2: +1.37M, +4.69M, +6.49M, +7.96M, +11.31M (cumulative +183 %). frogdrop 775->774:
+10.5M, then won back -3.3M per traversal by Gidney AND-carries on known-zero lanes and a consume-on-use product.
Gap-resident stack 843->819 / 839->818: +11-14 %. Ours: 792->791 +17.5 %; 815->814 +0.13 %, 814->813 +0.8 %,
813->812 +1.7 %, 812->811 +1.9 %. pi >> 1: negative cost.

## 5. Floors are claims

Each line's author wrote a floor sentence ("793 is this machine's floor"; "814 is blocked: the traversal runs out of
scratch"). Both fell the same day to the catalogue above. Re-run the census before believing a floor; record the exact
witness when one holds.
