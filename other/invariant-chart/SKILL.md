---
name: invariant-chart
description: "Stop storing register bits that an algebraic relation already determines, and rebuild them where they are read. Two recipes from bulengerk's ecdsa.fail left moves: residue charts from the extended-Euclid relation (mod 4, mod 8), and a joint code for two size registers with a proven sum range. Use when the next qubit must come off an extended-Euclid or size-register binder."
---

# Schatzchärtli (invariant-chart)

A **chart** is a cheap map from live state to bits you stopped storing, justified by an algebraic relation of the
arithmetic. `ecdsafail-lowq-playbook` and `ecdsafail-scratch-diet` already cover proving known bits, derived-size
storage, lane loans and re-encoding; this skill adds two concrete recipes bulengerk used for left moves on ecdsa.fail,
plus a stricter proof gate. Cites: [EVIDENCE.md](EVIDENCE.md).

## Recipe 1: residue charts (extended Euclid)

His notes state the relation `t x r + u x v + q x t x v = p` for the extended-Euclid state (source-stated, not
independently re-derived here). With p fixed (secp256k1: p = 3 mod 4, p = 7 mod 8), low residues of one rail follow
from the others, so one low rail can be omitted per rung. Q795 -> Q794 omitted the second low Work1 rail via the
mod-4 view (+38% T); Q794 -> Q793 omitted the third via a mod-8 chart (+44%). Verified in source: Work1 = 257 lanes
+ 2 omitted markers (`q794_lifecycle.rs:15`), then 256 + 3 (`q793_lifecycle_r03.rs:15`).

## Recipe 2: sum-domain code (two size registers)

When two size registers' sum is confined to a narrow range at the points where the code is used, store a joint code.
Q660: E = Y - 1 (7 bits) and S = Z + Y - 226 (5 bits) replace 16 raw size owners with 12; all 4,096 code words are
valid (`sum_size.rs:3-7`). Q666 used a five-bit SZ + SY - 226 code on 231 <= Z + Y <= 257: that range is the inherited
domain observed at completed post-stage-2 boundaries, not a proof for every input. Predicates on the coded registers
are MAJ-carry tapes with their CCX cost in the doc comment (20 CCX, `direct_size_predicates.rs:30-34`). The freed
owners paid for wider heads and windows.

Related moves he used, owned by other skills: the one-hole payload (PRE omits hole 257 - bl(t); POST normalizes
P[bl(r)] and omits it; PH stays lent as logical P[258] through digit and transition and must be returned before any
phase or activity reader: `splice258.rs:3-11`, `direct_payload.rs:9-11`; never count PH as spare while it is lent);
virtual constant lanes and lockstep cuts of tied peaks (Jieyi Long's `peak-qubit-reduction` skill in
[jieyilong/ecdsafail_skills](https://github.com/jieyilong/ecdsafail_skills); his Q774 -> 772 -> 771 -> 770 rungs cut
the pool constant 21 -> 19 -> 18 -> 17 with 2, then 3, then 4 consumed multiplier bits).

## Steps

1. **List the relations at the binding instant.** For each binder register write the relations that hold where it is
   read (an arithmetic identity such as extended Euclid, a fixed modulus residue, a range proven at specific
   boundaries), each with its source (proof, citation, or measured-only). Done when every binder register has its
   list and every entry is labelled proved, cited or measured.
2. **Price each chart from a build.** Recovery cost = executed Toffoli at every read site, measured on an instrumented
   build, against qubits freed. On the Pareto board any validated left move counts; on the product board one qubit is
   worth breaking even only when the T increase stays below T/(Q-1) (T/Q is the marginal approximation). Done when each
   candidate chart has a measured recovery cost and a freed-qubit count.
3. **Prove it against an independent specification.** A chart followed by its own inverse passes even when it computes
   the wrong answer, so test against separate encode/decode and transition specifications: reachable-support closure,
   arbitrary dirty passengers, guards disabled, phase and restoration checks, negative controls (a deliberately broken
   chart must fail), and emitted wire-id width. Exhaustive tests over code words (e.g. all 4,096) do not prove caller
   support by themselves. Done when every check passes and the negative controls fail as expected.
4. **Build beside the old layout, then replay whole.** Put the chart in a new module behind a baked switch so the old
   layout still builds byte-identical to the parent stream for A/B counts. Done when both build, the new one at the
   lower peak, and a full trusted 9,024-shot replay passes on all three channels. A lower allocator peak or a flipped
   admission constant is not evidence by itself.
5. **Land it as a beachhead** (`beachhead-ratchet`): the measured recovery cost is the purchase to grind back.

## Sources

[EVIDENCE.md](EVIDENCE.md), which cites bulengerk's public submission notes by submission id and note line.
