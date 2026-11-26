---
name: paged-walk-descent
description: >-
  Akashneelesh's method on ecdsa.fail (17 rows, Jun-Nov 2026; Q765 from 128.7M to 48.4M Toffoli in 37 hours): take a
  cheaper public walk a few qubits wider and buy the qubits back with a page of low bits whose fourth word is implicit
  in the walk's invariant, narrow end machines shipped as checked gate lists, a staged build where switch-off rebuilds
  the parent, and a census failure budget. Use when a public walk k qubits wider costs a fraction of your line; when a
  two-ring Euclid walk must lose wires; when a stream is assembled from modules built by separate agents; when summing
  a failure budget term by term; or when you review a row built this way.
---

# Blätterteig (paged-walk-descent)

Akashneelesh took the Q765 point on 12 Nov 2026 with `ae715bcf`, 765 x 48,420,475 [B], 47.8 % under his own previous
row and 46 % under ours. He did not improve his walk: he left it. The row is the public 773-qubit marker walk
(`d4dd7eb1`, 773 x 28,432,616 [B]) brought down eight qubits for +20.0M Toffoli, 2.5M per qubit. The same family's own
descent 773 -> 770 on the board costs 4.1M per qubit and rising [B]. This skill is that move, the build and budget
discipline around it, and what we measured when we took such a row apart.

Labels: [B] board metric, [N] his notes, [C] read from his code, [M] measured by us on 13 Nov 2026, [E] our estimate or
inference. Disclosed reference:
- `references/q765-page-row.md`: lane map, Toffoli by part, the dial, failure budget, executed pipeline, our measurements.

His notes are public: fetch one with `ecdsafail submission-note <id>`.

## 1. When it applies

- **Section 2** when a public walk at W+k costs a fraction of your line at W, or when any walk that keeps two Euclid
  rings (value over the other value's cofactor) must lose wires. Only k = 8 has been built [B].
- **Section 3** for any stream assembled from modules built by different agents.
- **Section 4** for any approximate row.
- **Section 6** when you review a row built this way.
- Exact post-pass shadows of a fresh rival row are `ecdsafail-pareto-ratchet`; evicting one helper lane per stage is
  `role-lane-eviction`; a product-score walk line is `structural-binder-walk`.

## 2. The move

### 2.1 Price the wider walk first
- **Do the buy-back sum on every wider public walk before the first row of a sprint, and keep it running beside the
  sprint.** The marker walk stood at 28.6M at 773 for five days [B] while he posted six rows on a tree costing 4.5
  times as much [B]. His notes price the public family's own dial at 765 three times and find it too dear (a 771 - D
  estimate needing D >= 6, then D = 9 ending up to 7 lanes short) [N]; the page of section 2.2 is what closed the sum.
  One case, so no threshold is supported [E].
- **Reproduce the parent before the first edit**: same `ops.bin` sha256 where the parent publishes one, else Toffoli
  to the digit and the op count, with your own sha recorded as the baseline. Three of his rows state byte identity, a
  fourth a score match by his validator [N]. Done when your build prints the parent's figures.
- **Rows are bundles.** He posts a row every 4 to 11 hours, each with 2 to 6 levers priced separately in the note
  [N]. He also measures options he rejects (one product lane -9.3M, one pool lane +6.0M) [N]. His logged pre-build
  prices missed by up to a factor 2 [N]: re-measure on the shipped emitter (section 3, item 6).
- **Take public levers above a threshold, credit them by row id.** He ported a 0.57 % exact lever from a rival's row
  and declined a 0.05 % peephole that needed hooks in two build paths [N].

### 2.2 Page plus implicit word
- **The invariant pays for the wires.** In a two-ring extended-Euclid walk the four words satisfy A*tB + B*tA = p.
  Keep the low D bits of three of them on a fixed page of explicit lanes; the fourth low word is implicit.
- **The implicit word is rebuilt in place, on the page lanes of the B word, inside each step** [C]. Do not allocate it:
  that costs the D lanes the page was meant to save. The cofactor paired with an odd value is the one reconstructed
  [N]. Whether the identity is used only mod 2^D is open [C, not determined].
- **One step sandwich per act slot keeps the page consistent**: apply the step's quotient to the page in one of two
  branches chosen by a parity bit (subtract on the explicit words, or divide the cofactor for the implicit one);
  quotient 0 is the identity [N]. Its fixed half costs 2,014 CCX per call at D = 16, two calls per sandwich, 396
  sandwiches per pass [M]; his 1.2k figure is for D = 10 [N].
- **Width accounting** [E, from his lane map; C for the frame]: the rings return 4D, the page keeps 3D plus a format
  flag and a clean AND lane, and his row adds a wait bit and five lanes the ends use: 773 + 8 - D, so budget
  D = k + 8. A paged frame with native ends is WIDER than the parent, 773 + 4D + 2 [N, M]; the width drops only when
  both end modules run on the narrow map. Between the cuts the frame itself occupies 776 - D lanes [M], 760 at D = 16.
- **Name every lane.** His map lists each range and role and sums to 765 [N]. A map that does not sum to the target
  is not a design yet.
- **Price.** At D = 16 the frame costs 8.62M list CCX per pass, 3.12M of it the sandwich [M]. One unit of D is about
  1.7M Toffoli over the stream near D = 16 at fixed cuts, less when the cuts move in (table in the reference) [M,
  graded on wide maps with native ends]. Ends at any D other than 16 have not been built by anyone.

### 2.3 Ends as separate narrow machines
- **The page needs every value and cofactor at least D bits long**, so the first and last slots of each walk run on
  a different machine: a narrow running-window walk on the short numbers plus a hand-over (an exact in-place multiply,
  an inversion gadget, a gated 2-adic stream) that ends directly in the paged form [N].
- **Cost**: 1,886,393 and 1,562,503 CCX per list, four hand-overs each, 13.8M as raw lists, 28 % of the stream [M].
- **Cuts**: 448/64 at D = 10, 432/80 at D = 16 [N]. A cut one step too early costs the whole budget: his start-cut
  term is 0.40 failing shots per 9,024 at cut 448 with D = 16 [N].
- **Done test for an end module**: equal to the native walk's state at the cut on 100,000+ walks and forced cases,
  checked by an agent that did not write it; then graded inside the stream alone, with the other end native, before
  the full assembly [N].
- **Truncate nothing whose errors correlate with the walk.** A 32-lane carry tail priced at 2^-32 per add failed 176
  of 200,000 walk ends because walk states correlate the dropped carries; he made the multiply exact [N].

## 3. Build protocol: staged splice

1. **Every mechanism behind a source constant; defaults select the submitted stream; all off rebuilds the parent
   sha.** His log shows the parent-sha check ten times up to the D = 16 frame [N].
2. **Stage on wide maps, one new thing per graded stream.** His order [N]: page the frame at D = 10 on 813 to 816
   lanes; splice start and tail, each unpaged, into the native frame on side branches; join the product stage on the
   native frame; narrow the rings; go to D = 16; frame levers; the paged start alone on 839 lanes.
3. **Grade each stage on its own draw and on salted suites, and log every stream, failed ones included**, with
   commit, width, Toffoli and cause. His integration log: 46 streams in 5 h 10 min, 10 failed [N]; the design predates
   it. An own-draw pass is not a gate: two of those streams passed their draw and failed only a salted suite [N].
4. **Modules are gate lists on the physical lane map, hash-checked when loaded** [C].
5. **When a grade fails, trace against the native walk at every boundary** (64 shots at all 510 boundaries for the
   page; 262,144 walks for the narrowing) [N]. The trace names the slot; the grade does not.
6. **Price levers on the emitter that ships.** His flag ladders kept 20 % of the saving measured on the plain emitter,
   because the shipped builder's cancel pass already removed most of those pairs [N].
7. **Archive each list's generator, inputs and test vectors beside the list.** His public tree ships the lists
   without generators [C], so nobody else can turn the dial.

Check these first-build bug classes [N]: junk left by an all-zero test page; an act literal read from a lane its own
row writes; a quotient digit taken as an implicit 1 for big classes; a flag erase without its top-zero literals; a
label re-point that lands on a live label; a splice in logical ring order where physical labels were needed; a layout
bug at about 1 failing shot per 9,024 with zero mismatches, which looks like budgeted failure.

## 4. Failure budget

- **One table, one row per approximation**: the census or model behind it, its rate, expected failing shots per 9,024.
  His 765 row sums to 0.08 [N]. He states a cap of 0.40 from f3251665 on, and shipped that row with a measured
  interval reaching above it [N].
- **Read the sum as a census with wide intervals.** One of his terms is carried at 0 with a 95 % bound of 0.039, one
  rests on 6 events, one class is omitted by his own statement [N]. The gap to the cap is not spendable room [E].
- **Set every window, cap and allotment from a census on disjoint seeds, never from an official draw** [N].
- **A census on the wrong population is not a bound.** A tier term carried at 0.0073 let a salted shot through on a
  staging stream; cap 27 -> 29 cost +28,132 Toffoli and the shot was re-proved [N]. Find the channel, widen it by one
  priced step, re-prove the shot.
- **No nonce and no re-roll.** Each stream is graded once; a failed stream is logged and the next one changes the
  failing channel [N].
- **Suites needed**: two clean suites of 9,024 cannot exclude a rate up to 1.5 per 9,024 at 95 % [N]; eight exclude
  0.375; confirming 0.08 needs 38 [E]. His three earlier rows ran 12 to 28 [N]. Two suites per stage catch bugs, not
  budgets.

## 5. Team

Builders by module (frame, start module, tail module, multiply, layout, checks, integration); every gate list checked
by an agent other than its author; models, censuses and the lane map from a second model family until its quota ran
out [N]. Five rows (b297b7cd to 3b2dae6d) were rebuilt before submission by a validator session with its own stream
reader; the last two went out before or without it [N]. Copy the first habit.

## 6. Reviewing a row built this way

Run R1 to R8 in order on the public source of the row; each ends when its cell is filled with a measured figure.
We ran them on `ae715bcf` on 13 Nov 2026; the figures are in `references/q765-page-row.md`.

| Step | Do | Ends when |
|---|---|---|
| R1 | Reproduce the stream hash and the Toffoli count from the row's commit | both equal the graded row |
| R2 | List the post-pass chain that actually runs, and the source files that are never compiled | every pass has a line in the build log, or is marked dormant |
| R3 | Run the tree-agnostic exact passes on the final stream | each pass has a paired, exact delta |
| R4 | Ledger the width: which ids are used, where the peak sits, in what share of ops | the binding instants are listed |
| R5 | Check whether generators ship for the stored modules | yes or no, per module |
| R6 | Census the Toffoli by part and by pass | the parts sum to the graded count |
| R7 | Toggle each lever and each clean-lane choice in a count build | each has a counted delta |
| R8 | Compare each module's lane footprint with the row's width | idle lanes per module are known |

**The clean-lane premise.** A lever that borrows a lane another module returns to zero by data, not by an uncompute,
is not exact until audited: a census, directed inputs from the parent's own failure classes, and the count of shots
where the parent passes and the lever fails. On this row the spare lanes are such a register: nonzero at the cut on
9 of 20,000,000 random inputs and on every one of 1,694 directed inputs (large early Euclid quotients, tiny dx, dx
near p), and the parent stream fails every one of those shots too [M].

## 7. What not to copy

- **The final assembly in one jump.** His first 765 stream brought in the 765 tail list, a regenerated start list,
  label re-pointing and id compaction together, 839 -> 765, none of them graded apart [N].
- **Two salted suites for the submitted stream** (section 4).
- **Submitting before the independent validator reports** (f3251665) [N].
