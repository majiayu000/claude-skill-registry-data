---
name: schedule-tail-truncation
description: Cut identical end-padding columns from a fixed walk schedule (Euclid/GCD column tables, fixed-length loops) and price the cut as a declared failure-rate trade. Use when a circuit runs a fixed-length schedule whose last columns are byte-identical padding, when a width-frontier row needs millions of T without a new construction, or when porting a column cut onto a rival's row.
---

# Wurschtzipfel (schedule-tail-truncation)

A fixed schedule sized for the worst case pays full price for its last columns on every shot, though only rare inputs need them. Truncation drops those columns, and "walk needs more than k columns" becomes a declared failure. It is a **failure-rate trade**, never an exact cut, and ships with its measured lambda disclosed.

Proven on ecdsa.fail, 8 Nov 2026 (two odinfree rows):
- 660: f5e8aeac, 660 x 461,395,887. k = 190 of 203 columns; -11.24M vs its exact parent 9b0fcff2. Measured total lambda 0.25 +- 0.11 per 9,024 shots: the lineage's ~0.125 plus a modelled +0.21 from the cut.
- 659: c7997b07, 659 x 558,136,207. The same cut on 506e8a66, -11.42M; measured total lambda 0.19 +- 0.10.
- Gates that decided both: a code census of every length consumer, the boundary falsifier (step 6) and 16 salts. Claude Fable 5.1 reviewed both. The 660 review left the boundary open until the falsifier closed it, and at 659 a hard `assert_eq!(len, 203)` in `k4_complete.rs` had to be relaxed first. A review is evidence, not the gate.

## Steps

1. **Find the padding.** Profile emitted T per column; on frogdrop this was F1_PROGRESS summed over the four traversals. Diff the schedule lines. Done when you have the list of byte-identical trailing columns with each one's cost. On frogdrop: `sched_frogdrop.txt` lines 186-203, ~0.9M emitted T each, the last ~0.45M.
2. **Census every length consumer.** Every reader of the schedule length must go through one loader; on frogdrop that is `frogdrop_sched::from_text`, where the knob truncates `cols`. Grep for hard-coded lengths (203, `assert_eq!(len, ...)`), parity flags and counter-bound asserts. Done when each consumer is listed and shown to cancel, fail closed or be range-checked.
3. **Price the failure rate before building.** Run the tree's classical envelope check, or any exact walk-length model, on >= 1M fresh walks per candidate k. Convert to **added** lambda per 9,024 shots (walks per shot x shots), and keep it apart from the lineage's existing lambda. Done when you have a (k, added lambda, total lambda, T cut) table. Pick the largest cut whose total stays well under the kill line; ~2.5 per 9,024 was ours, set by nonce cost.
4. **Add the knob, bake it, check the off switch first.** Add an env knob (A1_NCOL=k) in the loader with a range assert, and bake the chosen k as the default, because the grader is env-less. Run the knob-off check now, before step 5: with A1_NCOL at full length and the downstream tables disabled, the build must reproduce the parent stream byte for byte. Once tables are regenerated for k, the full length panics at their guards, so a shipped tree has no parent off switch. Done when the knob-off build matches the parent sha.
5. **Regenerate every op-index-bound artifact.** The cut moves every later instruction, so rebuild hold tables, certified cut-lists (SIMPLIFY) and fingerprint tables on the truncated stream. A live SIMPLIFY pass can exceed the 45-minute grader envelope; bake a regenerated certified table instead. Done when each table is regenerated and checked on the truncated stream.
6. **Run the boundary falsifier.** Choose inputs whose walk length L is at and just under the cutoff (k-1 and k, plus a few smaller values) and inputs at k+1. Run them on the candidate and on the full-schedule control with identical coins, comparing every SHOT field. Done when every L <= k shot is identical to the control and every L = k+1 shot fails as declared. At 660, all 745/745 L = 191 shots failed classically, and many also carried ancilla or phase garbage; record all channels. No other failure class may appear.
7. **Measure, gate, disclose.**
   - Run 16 FE_SALT draws for the measured total lambda (mean +- SE), the negative control, a twin build, and the stock `benchmark.sh` under `env -i`.
   - **Classify any failing shot before a nonce retry.** Run that shot's input on the parent/control under fixed coins. Only "the parent fails it too" is a lineage-class failure that a new nonce may route around. A shot only the candidate fails is a new implementation class, and it stops the fire.
   - Holds and regenerated tables are error sources too (hash-label premises, op-index binding), which is why the paired, twin and negative gates exist.
   - The note states the trade plainly: the cut k, the declared failure class, the measured total lambda with its added part, and "not exact".

   Done when every gate passes, every failing shot is classified, and the note carries those items.

## Hazards

- **The cut is public once it lands.** A rival can port it onto their newest row at any time. nasqret built his 659 rows on our trees the same day but had not taken the cut (119047a6 runs all 203 columns).
- **Disclosure.** A rate-raising row is never "exact": measure it (16+ salts) and state the trade in the note.
- **CI envelope.** Truncation shortens the stream, but regenerated tables and extra passes can lengthen the build. Time it against an accepted row of the same family on the same box.

Related: `exact-postpass-stack`, `ecdsafail-pareto-ratchet` (shadow a rival row the same day), `exact-hold-pass`, `shot-autopsy` (classify a failing shot).
