---
name: supplemental-stumping
description: Design the asks (55 to 60 per cent of the rubric) and their data-quality devices so the top two responses average 60 or less against a bar of 70. Use after stumping fixes the ladder and before data is cut, and to revise a returned task's asks.
---

# The Ask Layer

Three to five wide, criteria-dense, decoupled asks on silent realistic mess, hard through span, device mass and ladder depth, fixed on paper before data is cut and worded last against the golden. Evidence: `references/proven-in-production.md`.

## Part 0. The pair arithmetic

The landed call scores `C = 38 + 7 + 55 Lc`, the best miss `S = r + 7 + 55 Ls`, so `(C + S) / 2 <= 60` when `55 (Lc + Ls) <= 68 - r`. `L` is the ask weight kept, `r` the recommendation weight a wrong call keeps (about 5, from the generated rubric). That budget is about 63 of 110 ask points, a little over half each; build to **two fifths each**, which puts the pair near 51 and keeps the margin under 60 for the portal's regrade. Build for one response on the call (the cracker): only devices hold it. With none on it the construction layer costs the pair everything and devices are margin. Two on it is a ladder failure: the pair then reaches 60 only if each keeps about a quarter of the ask weight (`55 (Lc + Lc') <= 30`), so the ladder carries one response off the call and the asks are never counted on to rescue a landed pair. The ten points under 70 are bought here, since the ladder's margin goes to determinism. Levers: references A1, A2.

**The pair ceiling cannot validate the ladder it assumes, so check the premise before believing the
number.** The arithmetic above takes one response onto the call and one off it. A script that
constructs the mirror as a response stopping at a wrong rung is therefore structurally incapable of
reporting that the second-best real response lands the call: every figure in it can be honest and the
number still mean nothing. And the failure is not recoverable by ask work, because a response on the
call banks about 45 before any ask, so if both top responses land it the pair reaches 60 only with every
ask held to about a quarter, a layer no lane has shown it can build. task190 was retired on exactly this. Its measured pair of 38.1 was
`(56.0 + 20.1) / 2` with the 20.1 a response that misses the call, while its judge's blind enumeration
had already matched the golden on every graded figure. Four passes went into driving that number down, and the premise had been falsified
before the first of them.

**So the ladder is checked before the asks are priced.** The ladder is argued on paper (`precut.py`, the
readability screen, the deletion tests) and read by the judge's Gate F line: where Gate F finds the call
landable, the pair ceiling is not evidence, the finding is in the ladder, and no ask work is worth doing
until the ladder holds. A design whose ladder leaves both responses on the call needs a redesigned decisive
step, not a fourth device. No solver, scored reader or probe is run to check either (`CLAUDE.md`, the STOP
block); the portal is the only measurement.

**Where a whole lane actually bled, measured across thirteen builds: the ask layer, not the call.** An
in-house audit of thirteen FAILED_TO_STUMP builds found the ask figures at **61,
61, 64, 80, 92, 93, 95 and 98 per cent solved** against this part's target of two fifths each, one and a
half to two and a half times the target. Run the pair arithmetic on those numbers and the cause is
unambiguous: with one response on the call the pair is `28.5 + 27.5 (Lc + Ls)`, so the audited ask layers
put the pair at **62.0 to 82.3**, over the build target of 60 in every case and over the bar of 70 in five,
while the SAME call with the asks at their own spec puts it at **50.5**. Every one of the eight would have
cleared the bar on its existing call if this layer had met the spec.

Two things follow. **The ask layer is not margin, it is the pair**: the call contributes a fixed 45 against 12
on the miss side, and everything that moves the average past 60 is ask weight. And **a weak ask layer is a
systemic failure, not thirteen accidents**: the same author produced all thirteen, so when a lane's pairs come
back high, measure `Lc` before redesigning a single decisive step. The ask layer is also the one layer no
closure argument reaches, because 2.1 licenses an ask to turn on semantics or rule application, which the
rules that close a main call's decisive step do not touch.

**Measured across a whole lane of thirteen builds, the ask leak ran
42.9, 46.4, 55.6, 57.6, 68.4, 74.0, 86.4, 86.7, 92.5, 93.3, 93.6, 97.7 and 100.0 per cent, a median of 86.4
against this part's target of two fifths.** Three of those are builds whose call was missed,
so the devices had every chance to bite and bit nothing. Read together with Part 3's hygiene-battery record, which
is the same result from the other side, the law is: **an ask figure a competent reader computes straight
from the pack has no device on its path at all.** Something near the ceiling is the measured default for
an ask built out of the pack's own quantities, not a bad outcome among good ones, and it is not repaired by
re-wording the ask or by adding a device the book already lists as executed. **The floor of that range is
where to look for what works:** the two builds at 42.9 and 46.4 per cent are the lane's best ask layers by
a wide margin, and both of them route the ask through a reconstruction the solver has to get right before
any figure appears (an annex of per-quarter operational counts behind a recording-completeness correction,
and a per-regulation delay attribution over flights that operated). Read those two before designing a new
ask layer. The device has to sit where
the solver's own route runs, which is why 1.1's cracker sheet is drawn from the cracker's path and not from
the ask list.

**1.0 A device whose discovery and whose remedy are the same act is not a device.** One build's ask leaked
21 of 21 litres figures, and its pack also carried a line in the extract notes narrating two of that ask's
hazards. Cutting the narration moved nothing: the hygiene battery alone finds the primary, lists all eight
reissued survey references by number, and matches returns on the site address rather than the reference
("references were reissued, and the name is the owner or operator, not the brand"). So the narration was not
what handed the device over. The device was
reachable, because **noticing that eight references each serve two stations IS noticing that the join must go
through something else, and the only other identifier on the row is the address**: discovery and remedy
collapse into one act, and the hygiene battery's unmatched-join and key-uniqueness sweeps perform the
discovery.

**1.0b The remedy must be a reconstruction, never an estimator.** 1.0 asks for work left after the
discovery, and Part 5 asks for one determinate answer. A remedy that is a **choice among estimators** cannot
satisfy both, and the proof is `../stumping` 1.1c read one layer down: either the data separate the
estimators, so the solver reads the fit and takes the better-supported one and nothing is left to get wrong,
or they do not, so two defensible routes give two answers and the ask is forked. Measured when a grossing
device was designed for a leaking ask and then refused before any code: with the frame a stratified sample
and the stratum populations published so the factor had to be rebuilt, a Horvitz-Thompson grossing and a
post-stratified grossing were both defensible, because the register lists every station and its brand, and
they differ. Closing that by construction needs single-brand strata, which is degenerate.

A **reconstruction** satisfies both, because it is a definition applied to records and has one correct form:
a state rebuilt over time from an event log, a deduplication under a key that has to be worked out, an
allocation whose weight is recorded. The work is real and can be done wrong (a gap in the log, a revision, a
key handed over mid-series), and exactly one answer is right. So when a device needs replacing, ask what
KIND of thing the remedy is before asking how well hidden it is.

Contrast the two ask layers this lane measured lowest, at 42.9 and 46.4 per cent. In both, the solver has to
**build** something after the discovery (a weekly profile fitted to interval-censored windows, a
per-regulation delay attribution over flights that operated), and the building is where it goes wrong. So
the test to apply at design time, alongside readability test 7: **after the solver has noticed the problem,
is there still work to do, and can that work be done wrong?** If noticing settles it, the device is a work
order however well hidden, and hiding it better does not help: this one was measured both ways.

## Part 1. Design against the careful solver's path

**The cracker is a model of the opponent, so draw it from the careful solver's route, never from the ask
list.** Its stops are the author's guesses at that route. One build's cracker priced three asks at nought of
six each while two of its devices were "seen, reflex repair wrong" devices sold as silent ones: a register's
year-to-date convention falls to a tie check (passed plus held against the cumulative total) and a
two-meaning blank to a cross-tab of increments against reasons. **So screen every device against the hygiene
battery (1.1e) and re-device from the silent list (Part 3)** rather than re-pricing the cracker.

**1.1 The cracker and mirror sheets**, on paper before any device. The **cracker** landed the call, ran the hygiene battery (key uniqueness, exact duplicates, unmatched joins, fan-out, count ties), executed every filed rule it points at and matched every control and published figure. Score each ask figure and chart criterion, a hit within half a unit of the stated rounding: **every row misses** or the ask is rebuilt. The **mirror** stops at the most attractive wrong rung and keeps **under 50 per cent of ask weight** (target two fifths), no ask whole. A figure differing between sheets is coupled: re-route or drop it.

**1.1b The blind-response test, run at the draw.** For the widest graded component, ask what a response
that applies one obvious rate to one obvious size column would score, before any file exists. task190's
eight-segment table was 7 of 8 reproducible from a flat 0.82 per cent of each segment's deposit count, and
6 of 8 at 0.91 per cent with the headline landing on exactly the golden, so a response doing none of the
analysis banked most of the rubric's widest component. Also score the constant response (one value in every
cell) and the all-nil response. More than about a quarter of the cells recoverable that way means the
component measures the data's shape rather than the solver's analysis, and the ask's shape has to change,
not its wording.

**1.1d A cracker row is measured only on the pack it ran on, and re-siting a device voids it.** A build
carried two ask rows forward still labelled measured after re-siting both devices, and its pair arithmetic
described a pack that no longer existed. So stamp each row with the pack digest it was computed on, and
re-run the cracker script on the re-cut pack before the row is read as a gate.

**1.1e The hygiene battery a careful solver runs unprompted.** Past builds measured it: every one of these
repairs is applied by reflex, so a device resting on any of them is seen, never silent, and keeps nothing:
- exact or near-exact duplicate rows, and a repeated total on every line of a bulk receipt;
- a second series repeating the first one interval early (a check meter), dropped as a duplicate;
- a clock in UTC or standard time, found from a missing DST gap or an hour profile, and converted;
- carried-over or re-keyed records matched across two systems, and rows after a system's close;
- consecutive spells merged across a one-day gap;
- an estimate row dropped where its actual reading exists;
- a rescinded or reversed row removed by its rescind or credit;
- a code or phase field contradicted by a parcel, plat or schedule, re-derived from the finer key;
- a visible rate code or half-price line read as the discount;
- a comment column ("incl. outreach") read for what it says.

The devices that held in past builds (task169's one order per hearing, task177 v2's credit lines on bills raised before acceptance, task177 v1's day-cut pairs and the vendor desk) shared one property: the repair needed a judgment the hygiene battery does not make, about which records are one event, taken from a cardinality or an identity in the data, with no field, comment or code announcing it. Screen every primary device against the list above before cutting the pack.

**1.1c Three tells that hand an ask over, screened before the pack is cut.** A device a solver meets
announced or finds by inspection is absent from its path, not weak, and the repair is to re-site it (another
file, another grain, another join in the resolution chain), never to re-word the ask, widen a bin or add a
second device beside the first. task190's `## Ask sheet` claimed the cracker missed all three asks at a pair
ceiling of 28.5 while every ask figure was reachable, for three causes: a release note that tells the solver a
later extract stands above the published column announces the device (Part 3's law 3); two devices whose
arithmetic is exact enough to find by inspection, five December values at about fourteen times a month and
five rollup rows each summing to exactly three members, are seen, not silent (law 4 aimed, but landing on a
round multiple is a marker); and a device whose two handlings both tie hands the ask to whoever notices
either.

**A fork is not a device, and this is the commonest way an ask layer fails.** A device is found only by an
internal inconsistency; a fork is resolved by reading a sentence. So closing the fork hands the ask to every
response that reads it, and leaving it open is a determinism finding against the build. Two builds in one
sitting lived in that gap: one ask's primary became a filed rule the moment the determinism judge required
the grain pinned, and the measured pair ceiling went from 28.5 to 38.3, with 48.1 if both responses read the
pinned clause and 67.8 with a second such ask also found, against a build target of 60; the other build's whole ask
layer was the call's own construction over the call's own population, so the cracker kept 26 of 26 criteria
and the pair measured 65.5. **Test every ask against the pin the call needs:** if filing what the call must
file resolves the ask, the ask is sited wrong, and no device can repair it in place, because an ask over the
call's own population may carry no device rows at all (Part 2.1). Re-site it onto quantities the call never
reads.

**1.2 Four bans.**
1. **No filed rule adjudicates a device on the ask's path, and nothing narrates one**: only an internal inconsistency finds it (a wrong cardinality, an impossible row, a rollup above its parts), as a filed rule gets executed; a filed sentence may exist but never adjudicates.
2. **No marker**: no batch id, source value, load stamp, flag or single column isolates device rows; blend benign rows into every batch touched, give each classifier column a benign twin.
3. **No oracle**: no control tying only under the golden or only on the wrong read (references Part 2); no identity, total, name agreement, confirming round number or column the answer inverts from. One byte-clean referee arbitrates a designed disagreement without handing over a level; all else ties under every handling.
4. **No ask keyed to the call or its construction**: "for the option you recommend", a split or sensitivity of the committed figure, the ladder's population walk, a chart ordered, labelled or titled on the decision quantity.

**1.3 Decoupled in computation, inside the decision.** H18 (`reduce-house-fixes`): each ask is a component of the call's case, a reconciliation or an audit trail: a measure every candidate carries that the call does not turn on; the trail from an input the call consumes, through device rows it never reads, to its control total; an input reconciled to another system's total, the gap made of devices; all on rows outside the main population. Inheriting asks only when the author asks: narrow, device-free, swept so the set cannot be solved back for the decisive constant. If only inheriting asks pass H18, redraw.

## Part 2. Legality and the two layers

**2.1 Legality.** An ask is free of the main call's rules: it needs no filed rule, its golden may go against the procedure where records support it, and its device may turn on data semantics or rule application (banned only as the call's decisive step). Realism binds (`dataset-generation/references/layer1-messiness.md`): no corruption, truncation, decoy figure or planted defect. Would the real export look exactly like this with no task in mind?

**The corollary, and it is a draw-time screen: an ask computed over the call's own population can
carry no primary.** The separation line puts zero device and hazard rows inside the main call's
declared population, so if an ask's quantity is computed over exactly the rows the call's own
comparison is computed over, every device for it is dead before it is drafted. task194 proved it by
exhaustion: a cross-source duplication on a candidate sits in the main population; the same on an
embedded unit still shifts the network's own stratum frequencies and so moves the call; a partial
extract or an unresolvable attribution makes the truth unrecoverable, which law 6 forbids. Four
drafts, one conclusion, and the conclusion was about the ask's population rather than about any
device. So screen each ask at the draw by asking which rows its quantity reads and whether the call
reads them too. Where it does, re-site the ask before building anything: the fix is a quantity over a
wider or adjacent population, the care types, periods or entity classes the call never touches, where
the rows a device needs are rows the call does not see.

**The separation line.** Zero device and hazard rows in the main call's declared row population (files, columns, window, entities), asserted by count; the main path mess-neutral, never pristine. No document the call reads carries an ask's organ. Delete every device and the call stays hard. On an ETL build, primaries avoid the ladder's families. A device that moves the call is the gravest finding.

**2.2 Two layers.** Construction: the decisive construction's output on a segment the stakeholder wants anyway (region, tier, period, runner-up and gap), so a wrong unit, population or method fails every figure; the cracker has it, so it never stands alone. Device: one primary on rows outside the main population plus at least one shared hazard.

**2.3 The silent-mess rule.** Top responses run the battery and execute the filed rule it points at: mess it finds is a work order; mess that scores completes and reconciles on the wrong path wherever habitually checked, visible only at a cross-file or cross-grain cut nothing invites. Loud failure is texture. **Stacking:** a device moves every figure in its ask; primary families never repeat; three to five hazards each move several asks, with per-ask deltas; no subset of mishandlings composes back inside the bin.

**2.4 The use test.** A device ask needs a user, the stakeholder's words (analyst words leak devices) and its file's genre; else take the quantity the decision needs that crosses the device, or move the device.

## Part 3. The device book

**The nine laws.** 1 **Unflagged** (ban 1). 2 **Split evidence**: a column the wrong path never reads plus a corroborating file, neither enough alone. 3 **Silent** (2.3). 4 **Aimed**: each mishandling and mis-repair lands on a stated value outside the bin. 5 **Interior**: ship the genuine population blanket exclusion destroys. 6 **Fair**: one handling reproduces truth exactly, asserted; unrecoverable truth is cut. 7 **No marker** (ban 2). 8 **No oracle** (ban 3). 9 **Shared real causes**: one cause may feed several devices; the pack never reads as sabotage.

**Fair means a grader can verify it, and silent means the solver is not told it.** A device must leave an inconsistency that a grader who checks consistency, knowing the golden figure, can find and confirm; the golden's handling of every silent device is then named in a block 3 step (`submission-writeup`), which only the grader reads. task165's double weighings left nothing to find: two judges, each told the gap to the golden, searched cutoff rules and never tested the trucks' round trips, and the third reproduced every figure once a step named the handling. **Withdrawing the evidence a device rests on opens a fork rather than silencing it:** with the loader log and the controller columns removed so a reader could not shortcut the arterial cells, nothing filed said whether the older controllers' mass included the brine, and the judge called it a live fork at the ask's rounding.

Families: D1 duplication, D2 version, D3 units and meaning, D4 absence, D5 scope, D6 grain, D7 keys, D8 clocks, D9 self-validation.

The client's rigor cards (`../stumping/references/client/layer2-rigor-patterns.md`) that turn on the data's own structure rather than on a method (vintages and reporting lags, point-in-time universes, censored young cohorts, exposure denominators, incomplete recent periods, event-level quantities on every line) are ask-device seeds in the D2, D5, D6 and D8 families: an ask may turn on them because rule 3 binds the call only (2.1). The seed is the structure, never the card's pin; the device still obeys the nine laws, and a grader must be able to verify the handling (the law 6 note above).

**Silent, the primaries** (no habitual sweep sees it, or every tie passes wrong):
- D1 a replay under fresh ids, key kept, beside genuine same-day pairs
- D1 the same records under two key schemes or sources
- D1 a resubmission that opens no second case
- D2 a vintage change with invariant totals
- D2 the record is the latest accepted, not latest delivered
- D2 an attribute at the wrong vintage: a label stored before a silent switch, a rename, a later snapshot, a type-2 row read current
- D2 a superseded cut that looks final: a polished tab, a replacing restatement, a withdrawn document
- D3 units or scale set per source, date or pack; a missing currency read as the house's
- D3 a per-row quote convention that passes the identity check
- D3 dates that misparse silently; two columns one word apart
- D4 a reporter or channel absent, or drained down in stages
- D4 absence as the signal, evidenced in a file no habitual join reaches
- D5 a silently partial extract; out-of-scope rows known only by structure
- D5 a review filter the naive read ignores; a category crossed by collateral or label
- D5 a population inflating every control equally
- D6 an event's quantity on every line it covers, grain unstated
- D6 a ledger at another grain than its name; an allocation at the wrong weight
- D7 codes reissued to other entities: raw join and current-code filter both wrong
- D7 the true key elsewhere: another field, a reference string, a prior-id chain
- D7 an as-of join hiding the far edge; multi-hop crosswalks with retired codes
- D7 records billed to another holder after a transfer; a field overwritten later
- D8 a clock against a filed cutoff; a DST watermark overlap
- D8 a settlement or upload date for the event date; amendments by period, not filing
- D8 periods off month end; a holiday-delayed run
- D8 an anchor on the current record, not the first; a misparse resolving to the prior row
- D9 totals invariant under the device; a control true only in its scope; name agreement lying both ways
- stated non-additivity: a count that does not sum, the deliverable saying why

**Seen, reflex repair wrong**, a primary only with its over-cleaning half:
- D1 keys recycled across entities, so a global dedup deletes real records
- D1 repeated keys with opposite meanings; near-duplicates one field apart; casefold twins
- D2 a withdrawn correction a diligent response applies (at most one per build)
- D4 blanks missing not at random or meaning nobody filed; sentinels in several forms
- D5 a repair right for one population only; orphans to value, not drop
- D6 a log read as a roster
- D7 dirty keys with one collision punishing global normalisation

**Seen, repaired right** (hazards or texture): exact duplicates, re-sent batches, reprints · roll-ups and summaries inside detail · displaced fields, drifted fixed-width layouts, sign overpunch · key formats, padding, case, invisible characters, mis-keys · join fan-out.

**Measured as executed by the hygiene battery** (seven in-house rounds across 228 to 230, each a work order the solver ran, never a primary): repeated-row dedup; minutes logged per session; change files over base lists; unit conversions; closed days; effective-dated maps; UTC against contract zones; latest reviews; band and indexation rules; keeping the copy that was worked, or the one not closed as a duplicate of its twin, among a report's copies (task162, four readers of four across three copy mechanisms). The one device set that held (230 design 2) rode a domain effect the solver never modelled.

## Part 4. The ask ladder and the span floor

Each ask is a ladder of three to five stops, complete competent pipelines at distinct values outside the bin: the natural read, the half-handled device, the over-corrected read, the right rule on the wrong population, the answer. The golden sits mid-bin; a miss inside the bin needs more device mass. The ladder file comes from the golden's code and never ships. Every figure is separately gradable, a quantity, never a treatment or device word.

**The span floor:** eight or more files and ten to fifteen columns on the golden's causal path, each file moving the ask when misread. Split the quantity across sources, route through the resolution chain (fact, correction, register, crosswalk, standard), separate the antidotes: hub and spoke, fixed before the spine is cut. No two asks share primary device and path.

## Part 5. Determinism and the audit

**Price the determinism closure before the ask is designed, because on the ask side determinism and difficulty trade against each other one for one.** An ask whose device is a reconstruction the records support two ways is a Gate C fork, and the closure that settles it (naming the record, the set and the boundary in the asking sentence) files the reconstruction as a rule, so the device becomes documented rule application and its share of the ask weight transfers to the solver. Measured on task157, closing three such forks on one ask moved the cracker's keep from 0.040 to 0.240 of the ask weight, the landing response from 58.2 to 66.3, the pair ceiling from 36.2 to 45.7 and mirror leakage from 4.0 to 24.0 per cent, with no graded figure moving and the main call frozen. Nothing was done wrong: the fork was real and the closure was right. The lesson is that a device resting on which record establishes a state is worth what it costs to close, so design the ask so the device survives being pinned (it rides rows the sentence can name without naming their handling) or expect to pay the whole ask when a judge finds the fork at stage 4. Two devices built this way cost one ask; the third should be a different family.


Every ask answer recomputes from the bundle, forced by the records: enumerate the wording's readings and prove convergence (align the data so every licensed reading selects the same rows) or pin the wording; band by the margin you own; the records, never the ask, force the device; assert disjointness wherever a breakdown could count two ways.

**The reconciliation ask is where determinism dies, and the asking sentence is the only place it can be
saved.** A bridge between two totals has as many licensed readings as there are bases that could define
either total, so a reconciling ask that names neither its basis nor its grain is underspecified however
clean its arithmetic. Two builds in one night lost a judge pass to exactly this, each on its own
supplementary ask while its main call was forced and Gates F, G and H all passed. task196's advice
detail carried 35 rows whose settlement month precedes their advice, all of them that case's first
advice month, leaving two licensed readings under which all sixteen graded figures differ and 486,513
moves between quarters. task199 asked for a line per reconciling item and the pack supports three
bridges: an annual one closed by two lines, a three-line set in which one item closes nothing on the
delivered basis, and a quarterly one needing five, which is the grain the ask's own table already uses.
So the asking sentence carries the basis (which date or event defines each side) and the grain (the
level at which the two sides must balance), the reconciliation is at the same grain as the table it
reconciles, and `checks.py` asserts the closure at that grain, each side minus the other equalling the
sum of its lines. Enumerate the bases before writing the ask, not after a judge enumerates them for
you: the count of plausible bases is the count of readings, and one is the only acceptable number.

**A pin is paid for, not free.** A pin says what to compute; it never makes computing it correctly hard,
and the reading it closes was often carrying the ask's difficulty. So every pin added to close a fork is
paired with a silent primary underneath it, and the pair is **measured** afterwards, never assumed: run
the cracker's path on the cut pack and require every row to miss, and put the measured pair ceiling and
mirror leakage in the sheet. Two builds in one window paid for this rule. One had its determinism pins
written into a release-notes handling block, which the leak reader then named as a file existing only to
help the analyst; the fix was to move each pin into the document and voice the organisation would state
it in, keeping its force. The other had three pins close the two readings its devices rode on, and the
measured pair ceiling came out at 83.5 against a paper 35.1 with mirror leakage at 100 per cent, so the
ask paths were re-cut with silent primaries while the call stayed byte-identical (`freeze.py check
--mode rubric`). Pins and devices are not substitutes: a pinned convention with a silent device under it
is the shape that holds. Two rigorous readings splitting means a missing organ: fix it, never harden the ask. Assert every stop and delta, recompute every ask in the verifier, and sweep: lazy, necessity matrix (whatever moves nothing comes out; rerun after every parameter change), pair simulation on the cut pack, over-cleaner, oracle, wrong-path battery, separation count, and a grep for each device's words and any organ stated twice. Repair one device at a time, organ and records together; never delete an organ.

**A filed sentence's scope is stated before it is written, and its wording is approved before it ships.**
Three pins ordered in one session each leaked something different: handling notes became a solver checklist
in a release-note file, pins closed the readings an ask's devices rode on, and a clause added to state a
band's role also said where to build the counterfactual, which is the method. The instruction has to name
what the sentence may say and what it may not, and the wording comes back for a read before the pack is
cut. "State the band's role and let the exclusion follow" produced "that has to come from the segment's
trade outside the band", and the second half is the stump.

## Part 6. The returned-task revision

**Call held, asks scored** (`/fix-rubric`, proved by `freeze.py check --mode rubric`): change the ask paths' data first (devices, their rows, ask goldens and assertions); the card, ladder, main rows and the `target/` documents the call reads stay, bar a field description for a new column in an ask-only file. An ask's wording in the prompt changes only when no device can hold it as worded, every figure, unit and rounding kept; the call sentence never. `checks.py` asserts against the shipped commit that files the call reads and no ask touches are byte-identical, shared files keep the main rows and gain no column, and every main-call figure recomputes unchanged; a device needing more is dropped. Per device: one asserted line (the natural read lands outside the bin), an ask-sheet line, a `## Tried and rejected` line. **Call fell too:** the ladder first (`stumping`), then the asks against the new cracker sheet.

**The cracker sheet is code, run on the cut pack, and the sheet names the script.** A prose sheet
systematically describes the wrong solver: the cracker is defined by what it *does* execute, so a row
reasoning about a solver who reads none of the pack's filed sentences is describing the mirror, and the
sheet then reports the mirror's misses as the cracker's. Two builds in one wave shipped that error and both
measured a pair ceiling of 83.5 when the code was finally written, against paper figures of 35.1 and 39.4.
`precut.py` reads the sheet rather than computing it, so the sheet carries a `Measured by:` line naming a
script that exists in the build, and the gate fails without it. Re-run the script after every change, not
once at the end: a determinism repair that closes a reading can spend the device that rode on it, which is
measurable the moment the sentence is filed and invisible in prose.

**A device a shipped document resolves moves the mirror and never the cracker, and both are worth having.**
The cracker reads every governing document and runs the battery, so it executes every documented handling
and finds everything the five sweeps find; a device resolvable from a filed sentence or caught by an
unmatched join is therefore free to it (and no dictionary ships to document one, `dataset-generation` §3). task190 built two good devices, a revenue sample sitting on
the capital testing paper under its own prefix and a release date against the paying run's date, and
measured both: the mirror's leakage fell 51.2 to 26.8 and the cracker kept 41 of 41 either way. Those
are mirror devices, they are legitimate, and they are what buys the leakage bar. They cannot be the
primary. Stated as the builder put it: a pin tells you what to compute, a documented device tells you
how to handle it, the cracker executes both, and only an undocumented inconsistency costs it
anything. So budget the two classes separately. The mirror bar is bought with documented mess and
battery-visible mess; the cracker's rows are bought only with an inconsistency nothing in the pack
invites, which in practice means a grain or a self-validation shape: a rollup above its own parts, a
control total true only in its own scope, a paper row covering several ledger lines, a count that does
not sum. Each of those is found by reconciling amounts across grains, which no column description asks
for and no sweep performs.

**A device that is draftable but moves the call is held, not built.** The same build drafted a grain
device whose paper rows identify the tested item by invoice reference, covering two or three payment
lines each, and stopped: as drafted it changed which lines the paper identifies as tested, and that
moves the main call. It wrote the safe construction into `## Tried and rejected` instead, which is to
have the invoice-level rows cover lines already in the tested set so the set is unchanged, and to
measure that before cutting rather than after. That is the right order. A device moving the call is the
gravest finding in the book, and the cost of holding one for a pass is nothing beside the cost of
finding it in a verdict.

**Measure the forcing before the pack is cut, and state it as a number.** The difference between a
device and a fork is not how good the inconsistency is, it is whether you can say what makes the wrong
reading wrong. task193's chain ask stopped being a fork the moment it could report that the chains' own
log ties to the extract in all 148 chain-months under one reading and fails in 144 of them by 56,626
lines under the other; its dose ask the moment nine package rows contradicted their column's own
documented formula while the other 49 satisfied it. task182's air ask had an argument of the same kind
and no number of that kind, and a judge then found a number pointing the other way: the third meter's
rate was a constant fraction of the header's in every week, always below 1, which reads as that meter
sitting inside the header rather than beside it. An argument loses to an arithmetic pattern. So for
each ask device, compute the figure that makes the wrong reading wrong, assert it on the cut pack, and
where no such figure exists, replace the ask rather than ship it.

**A stopping rule has to check its fallback is shippable.** Four ask passes into task182 the author set
one: another fork and the ask layer is cut back to what the records force, shipping on a weaker layer
rather than spending more passes. The judge's own figures then showed the fallback did not exist, since
pinning the two open quantities kills both devices and a response that lands the call banks about 45
plus most of the ask weight, putting the pair near 70. A weaker ask layer is not always a shippable
one. Before setting a limit that ends in "ship it as it stands", price what shipping it as it stands
actually measures.

**An internal inconsistency makes a device findable; it does not make the figure forced. A device
needs both.** This is the half of law 1 that two builds in one wave got wrong in the same way. The
inconsistency is what lets a careful analyst discover the device without being told; the asking
sentence's own words are what stop a different analyst computing a defensible figure that never meets
the inconsistency at all. task182's replacement devices each had a real inconsistency behind them, a
counter standing still while its own rate channel read above zero, and both were still judged open
forks: "the blower air delivered" has a column literally named for the blowers' air that holds two
machines of three, and "the quarter hours the historian did not record the plant's state in" is
satisfied by the absent rows alone, since a row that repeats the one before did record something, just
not the state. Both readings are coherent, nothing shipped closes either, and a solver taking them
never looks at the rate channels.

Two fixes, and neither is a pin. **Take the lazy answer's handhold away:** where a column name matches
the ask's words, rename the channels after what the instrument measures rather than after what the ask
asks for, so there is nothing to grab and the analyst has to work out which machines feed which meter.
**And word the quantity so the device's rows are inside it by construction:** not "the quarter hours
the record does not cover", which the absent rows satisfy, but a phrase that a held value also fails,
so finding the held rows is the work rather than the question. A term that admits a figure reached
without the inconsistency is a fork however good the inconsistency is.

**A device that rides on an undefined term is a fork, not a device, and determinism will collect it.**
task182 carried an ask whose device was that the plant records the same facts at two grains, and the
device worked only while "the minutes of its assessment period" and "runs reached into it" were
undefined. Its judge failed Gate A, C and E on exactly those terms, defining them was the only repair
available, and defining them put every figure in those asks inside a filed rule: the measured pair
went from a claimed 39.1 to 75.2 with the cracker keeping 70 of 70. Nothing was lost in the repair,
because there was nothing legal there to lose. The test at design time: write each ask's terms out
fully defined, as a judge will force you to, and ask whether the device still bites. A device that
survives every term being defined rides on the data; one that does not was the ambiguity, and shipping
it buys a determinism return and an ask layer at once.

**Cutting a free figure is a correctness check as well as a ceiling lever.** A figure no device can
reach is banked by every strong response and dilutes every criterion beside it, so cutting it raises
the share the devices hold: task190 cut a plain quarterly run count and folded twelve monthly counts
into four quarters of payment, and the pair fell 51.0 to 47.6 while the mirror fell too, which moved
its own target from ten of 41 to twelve of 29. The cut also pays a second way. A redundant figure
sitting beside a device-touched breakdown of the same rows means the breakdown's basis is never
exercised on its own, so a bug there can pass for as long as the plain figure absorbs it. With the
plain count gone, that build's quarter-basis assertion began failing and exposed a real defect: a run
released at 01:30 the day after its run date was compared against the following morning's clock, so
the quarter's latest run scored as its earliest and every overnight release counted as inside the
cut-off. It would have been a Gate A finding. Sort the figures the cracker keeps into those a drafted
device reaches and those free by construction, cut or fold the second group, and re-run the assertions
afterwards rather than before: what fails is what the cut figure was hiding.

**The ceiling is computed on Part 0's weights, not on a legal point inside the permitted bands.**
`CLAUDE.md` allows 30 to 40 per cent for the recommendation and critical components, 5 to 10 for
instruction-following and 55 to 60 for the asks, so a script can sit anywhere in those ranges and
still be legal. Part 0's arithmetic is the one the 40 bar was calibrated on, and a script that takes
the bottom of the recommendation band with the top of the ask band minimises what landing the call
banks and maximises what the asks give back: task190's `ceiling.py` did exactly that, at 0.12 and
0.18 against 38 and 7, giving a landed call a floor of 40.0 instead of 45.0 and flattering the pair
by 2.5 points in the field the gate reads. Nobody chose that; it drifted, which is not better than
choosing it. Compute on 38, 7 and 55 so builds are comparable, and where a build wants other weights
it shows both numbers and says which the gate takes. **Solve the target count with the script rather
than on paper**, by sweeping the cracker's keep count and printing the pair at each: changing the
weights moves the mirror's score too, so an analytic recomputation that holds the old mirror while
substituting new weights mixes the two and lands wrong, which is how a target of 10 was argued as 8
and as 12 in the same afternoon.

**The honest number goes in the gated field.** Where two crackers are measured, the one that counts is
the one Part 1.1 defines, which executed every filed rule it points at; a weaker response's score is
not the ceiling. task182 measured 39.1 for a response that skipped the filed rules and 75.2 for the
cracker, and wrote 39.1 into `Pair ceiling:` so `precut.py` would stay green while the real figure sat
in prose below. task190, the same day, measured 67.8 and left the gate failing. The second is the
practice: the gated field carries the worst honest measurement, the gate fails until it is true, and a
green gate bought with the favourable of two numbers is the same defect as the prose sheet the gate was
written to catch.

**Two ways the ceiling script fakes its second column, and they look identical in the output.** The
first is task190's: the two responses were meant to take different ask readings and the script passed
one response's stops to both rows, so the ask band, 0.60 of the rubric, was one reading counted twice.
The second is task193's: the asks were properly decoupled, so the two rows agree by construction, and
the script computed the same call twice and printed the result as two measurements. The second is not a
measurement error, because for decoupled asks the two columns should agree; it is evidence that is not
evidence, because the skill's own coupling test, a figure differing between the sheets is coupled and
is re-routed or dropped, cannot be performed by comparing a list with itself. Where the asks consume
nothing the call's construction produces, say that in the output and point at the separation
assertions that prove it, rather than printing a duplicate row. Where they do consume something,
compute both paths for real.

**An assertion that reads a generator flag is not an assertion about the shipped pack.** task193's
separation check asked whether an ask's rejection device could move a patient's earliest observed
receipt, and it read the generator's own `is_first`, which no prevalent user's first line in the
extract carries. The check passed and the hazard was live: a path, however narrow, from an ask device
into the call, which is the gravest finding there is. Recompute the property from the shipped rows,
earliest day per entity from every line in the file, and assert that. A flag the generator wrote
knows what the generator meant; the pack is what the solver reads.

**The ceiling script is read, not just run.** `precut.py` checks that a script is named and exists;
nothing checks that it measures what it says, and three ways of getting that wrong have now been found
in one build's `ceiling.py`. It scored both responses on the same ask readings, passing the cracker's
stops to the mirror's row as well, so the whole ask band, 0.60 of the rubric, was one reading counted
twice and both rows printed the same 9 of 41. It hardcoded one ask's contribution to zero for both
rows, so that ask's fourteen figures sat in the denominator and were never scored, which flatters the
build. And it named the two responses the other way round from this skill, which is how the first two
survived being read at all. So: the script prints one row per response with the two scored from
different readings, every ask contributes a scored figure to both rows, the response that lands the
call is the cracker and its ask row reads 0 of N, and the author reads the scoring lines rather than
the summary. Where the printed cracker keeps ask figures while the note's table says every row misses,
the code is right and the asks need more device mass.

**A pin's scope has two halves, and the second is which neighbouring convention it must not reach.** A
conventions sheet is read as a list, so a row that fixes one table's basis is read against the row beside
it. task192's route table needed its window pinned while the partner table one row below stayed keyed to
the action date, and the pin had to name the route figures so the two read as the two different things
they are; written loosely it would have moved the partner figures too. Before writing a pin, name the
figures it governs and the figures sitting next to it that it must leave alone, and assert both.

## Part 7. The ask sheet

`## Ask sheet` is the device ledger `dataset-generation` builds against and `precut.py` reads. Per ask: figures, H18 home, use, primary device and hazards, file path and column count, stops and lazy delta, realism sentence, any reused device. Then the main population's zero-counts, the hazard table (asks moved, per-ask deltas), the referee, the cracker sheet (a table whose header names the cracker, every row ending `miss`), `Mirror leakage:` under 50 per cent, `Pair ceiling:` at or under 60, rerun from the generated rubric. Reuse is legal re-skinned, measured devices first (references Part 3); a device in consecutive builds or a repeated set is a template finding, and demoting a retired main mechanism is reuse.
