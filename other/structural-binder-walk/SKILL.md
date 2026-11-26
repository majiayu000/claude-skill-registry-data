---
name: structural-binder-walk
description: >-
  zuiris's method on the ecdsa.fail Leapfrog product line (Q1234-1244, Oct-Nov 2026). Each row moved the binding
  constraint with one structural mechanism: per-tick identities, a deeper shift alphabet, a pruned alphabet, record
  codes and packs. The tactics around it: priced failure spending, rebasing on a rival's freed resource with a same-day
  cap sweep, guard audits, declared nonce hunts. Use when a product-score line is stuck on small steps, when a rival
  frees wires or room, when choosing the next structural row on a walk-based point-add, when pricing a width trade or
  a failure spend, or when a new record or codec might have shadowed an older mechanism.
---

# Flaschehals (structural-binder-walk)

zuiris posted six promoted product-line rows between Oct 20 and Nov 5, 2026, moving 1234 → 1242 → 1244
→ 1243 → 1237 → 1234 qubits. Those six rows account for 33.91M of the 49.38M drop in the frontier score from Oct 19 to
Nov 11, or 68.7% [B]. His steps were 0.26–1.38% each. The median rival step in the same window was 0.0134% [B]. This
skill is the method behind those rows, plus a playbook for running it on a capped walk line.

Number labels: [B] board metric, [N] the solver's own note measurement, [C] read from code or a log, [E] estimate. Per-row
ledger, citations and evidence hashes are in `references/product-line-ledger.md`. The failure price list is in
`references/failure-price-list.md`.

## 1. When it applies

- **Use it when:**
  - the score is a product (Q × T);
  - the circuit is a long walk whose per-tick cost and tick count dominate T;
  - a recipe of knobs is near exhausted.
- **Do not use it** for exact post-pass polishing; use `exact-postpass-stack` or `exact-hold-pass` there.
- **The low-Q architectures (below Q1000) are out of scope here.**

## 2. The method

### 2.1 Name the binder, one component per row
- Keep a per-tick ledger of where T goes and of what holds the peak:
  - payload body versus barrels versus fold;
  - tape and record growth per tick;
  - the cap's room at each tick.
- His sequence of binders was:
  1. per-tick payload work: the fold's x257 erase, the square;
  2. clock length (138 ticks);
  3. barrel cost per wire for rarely used letters;
  4. closed record wires and the error budget;
  5. record width as qubits;
  6. record code density;
  7. a recorded section with hard wire IDs, which pinned Q.
- Each title names its binder. Write yours the same way. If you can't name the binder, you are not ready for a
  structural row.

### 2.2 One structural idea per row, built exact first
- **Exact identities that remove a Toffoli family:**
  - G6′: x257's erase phase depends only on the top column, so one MAJ plus 3 CZ replaces a 19–22-AND rebuild (−979
    [N]).
  - T0C: at the divide's tick 0, T[k] = S[k−1], so a seeded compare becomes 2 Toffoli (−20 [N], exact where the
    compare it replaces was approximate).
  - Q3: on x3 = 2^e·odd with e ≤ 5, k2⊕k3 = z0z1 (−121 [N]).
- **The workflow for such identities:**
  1. scan erase sites for "agrees with a low-degree form on most shots";
  2. keep only the ones that agree on every shot;
  3. a scan that finds only statistical agreement is a failure trade, not an identity.
- **Structural primitives:**
  - chained rows: one junction carry flip links rows with different controls into one ripple, so the add tail is paid
    once;
  - an exact-inverse reverse tick, which unblocks deeper digits;
  - in-place digit writes;
  - an X-measurement erase with a classically controlled repair.
- **Alphabet design** (the six-letter word):
  - Drop letters whose barrel cost per wire exceeds the walk-length saving. Letters 6 and 7 cost about 2 gates per
    wire, on about 2% of ticks [N].
  - The six-letter word cost 447 gates against 508 [N] and lengthened the clock by 2 ticks [N]. Net −16,059 T at +10 Q
    [B].
  - Look for a lower bound before building. A seventh letter was proved to cost at least 505 [N], so it was not built.
- **Record codes:** size the code to the legal state count. Examples:
  - 2 big letters per 3 rail ticks in 8 cells (208 of 216 states) [N];
  - the pair code: 32 legal records in exactly 5 bits, commit and pop at 2 Toffoli each, no measurement, exact on
    superpositions [N].
- **Packs** (majority packs of closed, dormant record blocks):
  - fan x* into a low-weight block, X-measure it, and rebuild it later as a popcount threshold;
  - each pack frees one wire from forward tick t to reverse tick t;
  - an over-threshold block is a classical failure on that input.

### 2.3 Price width trades against break-even = T/Q
- **Going right on Q is fine when ΔT/ΔQ beats T/Q by about 2×.** He took +8 Q at 1,313 T per qubit and +10 Q at 1,606,
  against a break-even of about 600 [B].
- **Then walk back left.** Use record compression to free wires, and a cap sweep to turn freed wires into qubits while
  room is worth less than the per-wire fee:
  - f253a5ed: −6 Q for +1,615 T, 269 per qubit [B];
  - db050300: −3 Q and −796 T [B].
- **Sweep the cap on the emitter** (model T × Q at each cap). Land where the product is flat: 1236–1238 within 0.06M
  [N].

### 2.4 Refit what the idea breaks, in the same row
- **Width table and anchors:** refit for the new walk. He used 2M walks, then 6M. 6M saved about 200 T over 3M; 9M added
  nothing [N].
- **Re-measure walk failures on fresh walks.** The pair code's first caller read 19.18 on a 600k-walk fit and 19.64 on
  24M fresh walks. Only the 6M refit brought it under the limit [N].
- **Re-pick the recipe:** reorder boundaries, N2 batches and compare windows.
- **Port and requalify the nonce prefilter.** Gates:
  - GPU and CPU first-reject arrays byte-identical on 302k nonces;
  - 0 false rejects on 24 fresh packets;
  - a deliberate fault fires.
- **Stream-bound tables die on a new stream.** Write off their credit in the ledger instead of hiding it: −3,654.7
  weighted T lost at 39f92d49 [N].

### 2.5 Spend failures by price, and disclose
- **Price every approximate lever in T per failing shot,** measured paired against the same stream on fixed packets.
- **Spend on the best price first.** His priced levers ran:
  - packs: about 1,400 and about 12,800 T per shot;
  - fold windows: about 1,088;
  - β relaxation: about 570, a bundle;
  - forward compare: about 570.
- **Each row states its failure rate against the limit the lineage cites.** When a row trades error for score
  (d34ea609, 21.5–22.4), it says so in the first paragraph and offers the within-limit variant. The next row comes
  back under the limit: db050300 at 19.11.

### 2.6 Audit guards when a new encoding lands
- **A new record code or codec can silently disable older mechanisms.** A guard such as `!a2_code()` or `!a2_dense()`
  excludes the new layout.
- **He found this once in public:** d34ea609 found the T3P1 pack off since the record code landed.
- **After each encoding change, grep the guards and list what turned off.**

### 2.7 Hunt cheaply and honestly
- Declare ascending bands and take the first fully clean nonce. Never select on T.
- Use one RTX 4090 for 300–520M-nonce follow-up hunts of about 1 h. Rent a fleet only when expected nonces per clean
  packet are about 1e9 or more (Lever A: 16 GPUs, 72 min).
- Disclose undeclared lucky finds (39f92d49).

## 3. Playbook: trigger → action → gate → expected gain

These rows are for a capped walk line.

| # | trigger | action | gate (decisive, cheap) | expected gain |
|---|---|---|---|---|
| P1 | A new record code, codec or layout lands, yours or a rival's | Grep the guards for every mechanism keyed on the old layout; list the shadowed ones | The shadowed mechanism re-enabled in one emit-only build, A/B against the same stream | −563 T at 1243 [N]. Test one pack alone first |
| P2 | A rival frees wires (codec, shelf, shed) | Within hours, rebase on the rival row, stack your exact savings, sweep the cap | Emitter product scan over 5–7 caps, flat region chosen; walk-failure estimate unchanged within 1 se | f253a5ed: −2.33M score, 4.5 h after the rival row [B] |
| P3 | One alphabet letter or branch costs per wire but is rarely used | Price walk length with and without it in the walk model before any circuit work | Walk model: ticks added vs per-wire gates saved; prove a lower bound for the alternative | 39f92d49: −16,059 T at +10 Q [B] |
| P4 | Clock length dominates and a deeper step is possible | Deepen the step under a record constraint (Lever A, e ≤ 7 with one big letter per triple); refit table | Walk model parks within budget at the shorter clock; ΔT/ΔQ ≥ 2× (T/Q) | 4cb9cf01: −10,505 T at +8 Q [B] |
| P5 | Room is scarce on late ticks | Pack closed, dormant record blocks; free one wire per pack across the late ticks | Room trace per tick (`Y15_ROOM`): the pack window covers the binding ticks; pack failure under 0.1 per 9,024 | as P1 |
| P6 | Record or tape width binds after a right move | Re-code the record to its state count (pair code, 5 bits per pair); refit the walk policy for the pairing | Walk model: parks and clock tax; emitter: freed wires at the peak | db050300: −3 Q and −796 T [B] |
| P7 | Failure headroom exists, or a lever needs funding | Build the price list (T per failing shot, paired); restore the cheapest-per-shot deletions; spend on the best lever | Paired fresh-block panel, at least 48 draws; total stays under the failure limit your lineage cites | Depends on your own price list; see `references/failure-price-list.md` |
| P8 | A recorded or replayed section pins Q with hard wire IDs | Swap in the builder version, or relocate the replay; price the fee at fixed cap | The emit build reaches the lower cap; fee per qubit < T/Q | cd2ef4cb did this from his named target: −4 Q [B] |
| P9 | An exact per-tick identity is suspected (erase agrees with a low-degree form) | Scan erase sites; keep only all-shot agreements; emit natively | Exhaustive small model plus 36k-shot equality at each site | G6′ −979, T0C −20, Q3 −121 [N] |
| P10 | A structural row is ready | Freeze, port the prefilter, declare the hunt, write the ledger with failure rate vs limit, submit, go quiet | Prefilter gates (§2.4); byte-identical rebuild; hostile-env rebuild | One large row instead of a ladder |

## 4. Hazards

- **Model ledgers from different baselines don't add.** His 39f92d49 ledger nets −20k against −16k measured.
  - Decompose with board deltas and adjacent pairs only.
  - A "model versus measured offset" can be table composition (sampled deletions, own rows), not model error.
- **Fitted width tables are cap-agnostic.** They are fitted to walk failures, not to room.
- **A pack is a port, not a flag.** On the pair record the second field slot is `None` after commit, and the old
  `t3p1_maj_z` panics on it. The pack's failure rate on a new record is unmeasured until you run it.
- **`peak=cap` on every tick means the planner fills to the cap.** It is not evidence of scarcity. Use tick-entry room.
- **Error-for-score rows stack failures.** Price the whole line's failure rate, not each row's delta.
- **Stream-bound tables and recordings** (frozen hunks, `sq_leader.zst`) are artifacts:
  - they do not survive a new stream;
  - a recording keeps its own wire IDs.
- **Notes carry inherited notice blocks.** Never copy them into notes, evidence or templates. Attribute lineage in one
  line of your own words, and state the failure-rate position in your own words.

## 5. Evidence

- **Rows:** e3b5c51f, 4cb9cf01, 39f92d49, d34ea609, f253a5ed, db050300. Full ids, commits and note hashes are in
  `references/product-line-ledger.md`.
- **Repo:** `Layr-Labs/ecdsafail-challenge`.
  - Validate commits: `88869d8c`, `f0c0a662`, `17b9603f`, `e0a22ba0`, `fbfe69b0`, `87f0aaf3`.
  - Each one's git parent is the previous promoted row.
- **In-tree walk model:** `src/point_add/a2_rails.rs` (`mod a2_ref`, `walk_t0`) in the public trees. His `rsim` fitter is not
  public.
- **Review:** the transfer conclusions were adversarially reviewed on Claude Fable 5.2 (claude-fable-5-2, 2026-11-11), which corrected three
  of them.

## 6. Related skills

- `benchmark-frontier-archaeology` (Jieyi Long's ecdsafail_skills): the intake procedure that produced this.
- `peak-lifetime-ledger`: naming and pricing the binder (§2.1, P2, P5).
- `lambda-exchange-desk`: the failure price market (§2.5, P7).
- `ecdsafail-island-hunting` (Jieyi Long's ecdsafail_skills), `ecdsafail-fasteval`: prefilter qualification and failure-rate measurement (§2.4, §2.7).
- `pinned-table-stacking`: what to do about stream-bound tables a structural row kills.
