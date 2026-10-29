---
name: dataset-generation
description: Build the evidence pack that carries a designed stump. Covers scope, the input gates (10+ files, 3+ formats, a 25,000-row file or a large database, 2+ distractors), file roles, calibration and context artifacts where a strategy needs them, rung exactness, authentic Layer 1 mess and the realism gate, governing documents, provenance and metadata.json, the generator's assertions, the independent verifier and byte-identical rebuilds. Use at the build stage once precut.py passes the design note, when repairing a pack, or when a number does not reproduce. Never build data before the ladder exists.
---

# Building the evidence pack

> The prompt names the decision; the pack is the task. Every rung reproduces to zero drift from the
> bundle, and every rival dies to a fact in the bundle. A golden number the pack cannot recompute does
> not exist.

**Prerequisites.** The card is registered clear of BLOCK (`fingerprint`), and `DESIGN_NOTE.md` passes
`stumping/precut.py` (pairing, default path, stump sentence, ladder, semantic fork table, closure table,
ask sheet). Read its `## Tried and rejected` first.

## 1. Scope, and the evidence the objective needs

One client domain, one task type, one of the eight Axis 1 objectives
(`guide-to-prompt/references/domains/README.md`); house domains stay valid only for cards on file. If the
stump needs evidence from a second sector, the stump is wrong. Framing rule: the entity is a platform, the
public dataset the market it sells into. The pack carries the raw material the task type's own analysis
runs on (§7.1, R1): a pack whose deciding computation is a sort, filter, join or stated score over shipped
columns makes the domain a backdrop, and goes back to design.

| Objective | The pack must ship (fails when) |
|---|---|
| Descriptive | row-level records at the decision grain, real volume (only summaries ship) |
| Anomaly | baseline history, seasonal structure, the ops log separating artifact from event (a spike with no baseline) |
| Root-Cause | two or more drivers correlating in aggregate, and the separating evidence (one driver) |
| Opportunity Sizing | the addressable pool at row level and the evidence taking it to the realisable (one number, or retaggable as forecast) |
| DQ Monitoring | the pipeline's own records (deliveries, arrivals, counts, schemas, checks, incidents, routing) beside the published (a business metric dressed up) |
| Experiment & Causal | assignment records, outcome at the pinned horizon, the confounder as a column (arm summaries) |
| Forecasting | history to fit and hold out, the regime break in the series, settled outcomes where a back-test chooses (every method agrees, or the horizon is unpinned) |
| ETL | three or more genuinely disagreeing sources with crosswalks, id maps, dated FX or unit tables (cosmetic differences) |

## 2. Sourcing

A **real public spine** (authenticity, volume, real mess, clean licence), **real publisher documentation**,
and a **constructed operating layer** (extracts, ledgers, configs, memos) where the stump lives. A fully
constructed pack passes when every derived file is declared and behaves like a real export.

**Blocking:** never fabricate, corrupt, pad or truncate to make difficulty; never ship a long generated
PDF, DOCX or PPTX (constructed documents are two to four pages of operational content); AI may write
transforms, never create the empirical source evidence. **The spine:** the market the entity sells into,
10^3 to 10^6 rows, a natural key, shippable documentation, genuine mess (non-response, vintage code
changes, revisions), a dimension the decision grain can differ from. Check the volume gate here.

## 3. Roles and the input gates

| Role | Count | Note |
|---|---|---|
| Spine | 1-4 | near raw; split only where real |
| Publisher documentation | 0-1 | genuine; disclaimed if not decisive |
| Operating extracts | 2-4 | real cadence, a `pull_date`-style column; the stump lives here |
| Context artifact | 0-2 | §5 |
| Calibration corpus | 0-1 | §4, only where the strategy needs it, then built first |
| Governing document | 1-2 | §8, the pin |
| Voices | 0-1 | §8.4 |
| Lookup tables | 3-6 | small, boring, force joins |

**No shipped file describes the data.** A data dictionary, field notes, a schema or column description, a
readme, an extract manifest, a notes sheet or a "how to read this" tab: any file or sheet whose job is to
tell the analyst what the data is, what a column means or how the files fit together is a leak, because it
hands over the structure the analyst is paid to find and sets its definitions beside the very columns the
decisive step joins. task144's first architecture shipped field notes defining the feed surface a few lines
from the follower count, and an extract manifest giving every file's role; both portal responses built the
decisive cascade from them and landed the call. Each file carries its own conventions the way the producing
system writes them: a timestamp with its zone or offset, a column named for its grain or unit (`day_utc`,
`amount_eur_thousands`), a code crosswalk that maps codes and says nothing about them, a header the export
really carries. What the organisation itself defines (an estimand, an eligibility rule, a window) goes in a
governing document (§8) as a filed fact about the world, never as a gloss on a column. Provenance lives in
`metadata.json` outside `target/` (§9). Assert it in the generator: no readme, dictionary, notes or
manifest file or sheet under `target/`, by name or by content.

**Input gates, asserted in the generator:** 10 or more files (10 to 19 typical); 3 or more formats (4
target); a 25,000-row file in any format or a large database whose real tables must be queried (never an
empty wrapper); two or more distractors in `metadata.json` (§8.3); nothing LLM-shaped. Give the bulk file
the format the source would export, not CSV by habit. Every file does work; padding is checkable. Name
files as real exports (`settlement_extract_fy24.csv`), never after the stump (`known_issues.txt`).

## 4. The calibration corpus, only where the strategy needs it

Settled outcomes the decision does not cover but the method must explain (a settled ledger, a counterparty
acknowledgement, a pilot log, the book with actuals, a retry log). It confirms a **filed** criterion (C2,
`determinism-check` §3), never recovers an unfiled rule, never refutes the naive read; shipped every
build, it is a template.

- **Fittability:** records first, every outcome row computed from them; a row no rule reproduces is a
  fabricated intermediate and pushes solvers to read the file ordinally. Never patch a row without its records.
- **Outcomes from the correct basis** with realistic noise (R^2 1.000 reads synthetic); rivals fail hard;
  a near rival means change the mechanism, never the tolerance. Confounders controlled by construction.
- **Gap targets:** 0.92 against 0.59, not 0.88 against 0.84; exact against no match; all against none;
  every filed decision reproduced.
- **Twin pair** where lookup transfer threatens: two cases identical on every visible field and in every
  document, outcomes about 2x apart, driven by the decisive mechanism. Back-test the whole family (N of N
  within x, every rival misses one by y, count stated). Run lookup transfer yourself: it lands on a wrong rung.
- **Blind to the decisive move** for a stated structural reason. Quiet: never named in the prompt, never the
  largest or most prominent file.
- **Threshold-free,** with a floor: nothing between zero and a level above any de minimis, so every
  threshold files one figure (task44, nothing between 0 and 13 per cent); assert the floor.
- **No convention column** (`projection_convention`): it makes the rung a lookup. Close the parameter by
  filing it at authority or by C1/C3, never by deletion alone.
- **A window past the pull:** the driver for the uncovered span ships as a silent operating file (a plan
  published before each freeze, generated from the process). Assert its error on every scorable horizon,
  the share of the figure the span carries, and that dropping it moves a bin (task47, 12.5 per cent).

## 5. The context artifact

**Never build a file that computes the naive answer to the decision question.** A ranking of the
candidates on the decision basis that gets it wrong fails Gate G at any depth; the one exception is a
declared wrong-basis distractor (§8.3). Rung 0 is engineered in the data and asserted, never written.

A context artifact answers another question correctly (a monitoring export of a past quantity, an ops log,
a register, a published series, a capacity report, a close-out), never a scorecard, filed model,
prior-review memo or method note answering the decision wrongly. Computed by script from the shipped
files, diffed at zero tolerance, internally flawless, with one in-file line naming its question
("Capacity as of cycle open; does not net committed volume") and a version, refresh date and owner.

## 6. Rung exactness

**6.1 Compute forward.** Data first, then every rung, rival-killer and graded figure by script. A number
fixed first and records reverse-engineered to it drifts and fails Gate A.

**6.2 Separation.** Each rung names a different candidate or figure, asserted by name and re-run after
every parameter change (a tuned parameter routinely hands the last rung to the candidate below). For a
which-of-N ladder: answer 4th or 5th on rung 0, never 1st on an intermediate rung, 2nd on at most one (by
1.20x); no rung margin under 1.15x; final margin 1.2x or more, target 1.5 to 2x.

**6.3 Dominance.** `edge(winner, decisive axis) >= 1.2 x advantage(decoy, carried axis)`, both computed and
asserted. When it fails, widen the decisive spread or shrink the carried advantage.

**6.4 Construct the disagreement.** A rung on two axes disagreeing (date against label, row against
entity, gross against net, cohort against calendar) needs the correlation built per candidate, asserted
both ways; independent draws make it inert. Add inert instances too, or the field is the giveaway (task60).

**6.5 Grain statements** live where the producing system or the organisation states them, never in a file
written to explain the pack: a column named for its grain, a header the export really carries, or a
governing document's flat definition ("Recipients are distinct within [entity], [program] and [period]";
"[Status] is account-level and survives a lapsed subscription"), never advice (§3).

## 7. Authentic mess and the realism gate (Layer 1)

`references/layer1-messiness.md` is the library (eight universal techniques, eight per domain); the card's
`layer1` lists those the pack carries. Real exports are spread across files, grains, versions, calendars,
identifiers and partial cuts. A model may trip on it; the stump never rests on it, and nothing is a
defect placed to be caught. Test: would the organisation's export look exactly like this if nobody had
designed a task? The design note names each mess and the system that produces it.

**A governing document's definition says what a row is, never what it explains.** That is the line between
a decisive organ Gate B requires and an announcement the leak reader finds, and no file ships whose job is
to describe columns at all (§3), because explaining a column is what such files feel like they are for. A
policy may define a movement as a patient's transfer between cost centres on a date; nothing may say
that complications arise at transfers. The grep that settles it runs over every csv, txt and pdf in the
pack for the decisive relation's vocabulary, and a hit is innocent only where it states a fact about the
world (a service reconfigured, a unit closed) rather than a relation between the organ and the outcome.
task194's architecture 6 passed it with two hits, both of that innocent kind, and with both governing PDFs
clean. Note what makes the pass meaningful there: the shipped record attributes the outcome at the easy
route's unit and nothing points past it.

**A contradiction between two files is only a contradiction at a grain where both sides measure the
same thing, so establish commensurability before believing one.** The cheap join is almost always
the wrong one, because the two files date different events: an item is published on one date and
delivered on another, a case is advised in one month and closed in another. task199's stage 4 reader
reported that 2,587 of 6,773 day-municipality pairs cited more items than the filter had retained,
which would be impossible, and the orchestrator reproduced it at 2,740 of 22,075 with its own join.
Both had matched the citation's publication date against the delivery log's send date. At the one
grain where the two sides are commensurable, municipality totals over the whole window, cited runs
at 40 to 70 per cent of retained and **no municipality exceeds it at all**. The impossibility did not
exist, and acting on it would have repaired data that was correct. The check costs one computation:
before reporting that two files cannot both be true, aggregate both to the coarsest grain the claim
still has meaning at, usually the entity over the whole window, and see whether the contradiction
survives. A reader's or a judge's structural finding is a hypothesis with a join or a base rate inside it, and the
assumption is the part most likely to be wrong. Two fell this way in one night: a cited-against-retained
impossibility that matched a publication date to a delivery date, and a withdrawal-window placement claim
resting on a quarter of periods carrying an episode when the episodes cover 1.22 per cent of the span by
duration, 20 times out. Reproduce the finding before repairing anything, and when it does not reproduce,
record that it did not rather than building for it.

**Measure the version the finder saw, not the version in front of you.** A third claim in that same night
was dismissed as unreproducible and was correct: a judge reported that a notification feed's row count and
its distinct-reference count forked, the orchestrator measured the pack on disk and found them identical,
and told the builder to leave the figures alone. The builder had already repaired the defect, a
four-digit reference suffix drawn with replacement, so the pack on disk no longer had it. Checked out at
the judged bundle's own commit, the feed held 956 rows over 951 references with five repeats, exactly the
series the judge gave. A finding is about a state, so the check is against that state: unzip the bundle
the finder's own md5 names, or check it out at the commit that shipped it. Dismissing a true finding
costs more than chasing a false one, because the dismissal is filed as settled.

**Two files that observe the same events need two detection logics, and matching bounds are a
causal impossibility rather than a realism nit.** Where a pack carries the same real-world events as
seen by different parties, the natural way to generate it is to cut both from one event list, and that
leaves every derived record bounded exactly by the artefact it was derived from. No physics explains
it, so there is no argument available at review: the pack simply shows how it was made. task197 shipped
a provider archive whose 1,756 deviation recordings each began and ended on the exact second of one of
the system operator's 666 published extracts, 1,756 of 1,756 on both bounds, and two of its nine sites
held byte-identical bound sets, 184 recordings with the same starts, the same ends and the same mean
duration of 162.4 seconds at the same standard deviation of 26.8. Three determinism judge passes read
Gate G and Gate H as PASS over that pack, one of them deriving before it read the answers, because they
were checking whether the figures recompute and not whether the records could exist. The stage 4 reader,
asked directly whether the series looked generated and to give the spreads it used, found it in one
pass. So each observer gets its own trigger: its own threshold, its own pre-roll, its own release
condition with hysteresis and hold-off, and real independence, meaning no two observers share a bound
set and each sometimes records an event the others miss. The generator check is one line and belongs in
`checks.py`: count the derived records whose bounds coincide with a published bound, and assert no two
producers share a bound set. Ask of every pair of files describing one event stream, before it is cut,
who detected this and with what, and whether that party could know the other's boundaries.

**An organ's realism is measured by its variance, not by its genre, and uniformity is the tell.** The file
the decisive step needs is the one most likely to be built to exactly the shape that step needs, and a
solver reads that shape as the instruction even when no sentence says anything. task197's archive held 695
recordings, every one exactly 241 seconds long and every one starting exactly 30 seconds before a
quarter-hour boundary, carrying nothing but the ramp the decisive reconstruction wants: the stage-4 reader
quoted them as having one use and as looking built for the analyst, and landed the call. A real archive's
recordings vary in length, in start offset and in completeness, exist for several reasons (alarms, tests,
disturbances, operator captures) and include some that are truncated, some that overlap and some that are
missing where they should exist. So give the organ its genre's spread, and make the subset the decisive
step uses a minority of what the file holds rather than the whole of it. The check is one line of code on
the cut pack: take the distribution of length, offset and reason over the organ's rows, and if the rows the
decisive step reads are the file's only rows, or are identical on every dimension but their timestamps,
the organ announces the step. Varying it moves no graded figure, so there is no trade to weigh.

**Governing rule:** if a messy choice could flip the answer, cut it. The one exception is a **ledgered ask
device** (`supplemental-stumping`): it moves only its named asks by the stated deltas, with zero rows in
the main call's declared population, asserted by count. **Clean-data test:** with every file clean, the
task is still hard; a chain of defect corrections fails Gate G like one. **Inverse pack** (legal): the
headline is correct and legitimate things look like defects (real repeats, a documented decommissioning,
an honest eligibility widening), each established by a shipped document, the reconciling artifact
balancing only unadjusted; sweep every adjustment combination.

**Good mess:** re-pulls with a later `pull_date`; catch-up transfers; null-measurement records;
block-structured non-response (ship a rollup that reconciles only with blanks left blank); mixed date
formats; schema drift on a dated effective date; parent rows with unpriced children; placeholder ids and
visible sentinels; key casing and whitespace at a realistic rate. **Bad mess:** corruption, unparseable,
truncated or protected files, filler, a table split to inflate the count, decorative documents.

**Realism:** no placeholder identities (John Doe, Acme, Company A); real vocabularies (NAICS, SOC, HS,
ISO, FIPS, agency series codes), geography, naming, release calendars and revision behaviour; data near
raw. **The realism sweep** is asserted in `checks.py` before any reader sees the pack: no identical counts
across periods, sites or entities; no round headline totals, shares or rates; no constant stream or
repeating block; no free text recurring beyond a real rate; every persona from `guard.py names`; containers
scrubbed (`reduce-house-fixes` H1); timestamps coherent (§9). A tell the leak reader still finds is a
generator fix before the judge.

### 7.1 The three rules, executed

The generator holds the clean truth (the world before any mess is applied or any document written), so the
client's three rules are asserted, not argued: one block in `checks.py`, every label starting `R1`, `R2` or
`R3`, run on every build and every repair.

- **R1, the field's raw material ships.** The pack carries what the task type's estimator runs on, at the
  grain the field works at (paired readings, censored durations, a triangle's claims, assignment records,
  microdata with its weights), never the deciding quantity precomputed and never a list to sort. Assert that
  the golden's decisive computation reads those rows and that no shipped column holds the deciding quantity.
- **R2, every mess item is real and neutral.** The design note's Layer 1 inventory names each item, the
  system that writes it, the file it sits in and its natural mishandling. Per item, the golden method run
  with that item mishandled leaves the call and every critical component where they were, or moves only its
  ledgered asks (§7); one assertion per item.
- **R3a, the analyst test.** The easy route (the default path) run on the clean truth, every filed rule
  applied, files the named wrong answer. If executing the stated rules reaches the golden, the decisive step
  is rule application.
- **R3b, the decisive step alone.** The easy route with only the decisive step changed files the golden;
  each lower rung's single correction leaves it on a wrong answer.
- **R3c, no plant.** None of the client's plant kinds ships: a copied or backfilled block, a swapped or
  reversed series, a hidden year-to-date column, a decoy memo or staff draft, a stakeholder figure wrong only
  so the task can overturn it. The realism sweep's repeated-block check covers the first two by assertion.

A failing R assertion is a design failure: back to `stumping`, never patched in the data.

## 8. Governing documents

**8.1 The pin.** One sentence, a filed fact, in the highest-authority document that carries it; never
repeated, explained or justified. Authority: the prompt (no pin ever) > governing standard > charter,
SOW, terms > decision memo > method notes > thread (no dictionary ships, §3). Grep for counter-pins
at or above it and for restatements (a repeated pin is a signpost). To keep a rung out of one file, split
it: the rule in one, the layout fact it operates on in another.

**8.2 No licensed wrong basis.** No document files, endorses or gives an advocate to a wrong basis, metric
or procedure (an official decoy, blocked at the draw). A rival method arrives as the analyst's shortcut.
File the rules a real organisation has; the decisive step is analysis they leave open.

**8.3 Distractors.** Two or more files the solution never reads that **look relevant** enough to weigh:
same organisation, keys or period; a neighbouring measure, a prior cycle's working file, a related
programme's report, an out-of-scope register. Assert the golden and every ask unchanged with each deleted.
An unrelated file does not count. Named only in `metadata.json` by bundle path
(`{"distractor_files": [...]}`); `leak.py` fails "distractor" under `target/` or in a name.
A **wrong-basis distractor** answers the decision or a graded quantity with reproducing arithmetic on a
basis wrong by record (outdated vintage or unit, superseded rule, changed definition), never a planted
error. Licensed only if: never the stump (the build stumps with it deleted); ruled out by one quotable
shipped fact named in the design note; declared in `metadata.json`; its answer neither the golden nor
rung 0's and outside the golden's bin, asserted. The context artifact (used) and a disclaimed background
document (nothing to weigh) are never distractors.

**8.4 Voices.** Optional, never a roll call: at most two people holding beliefs, as real correspondence.
Nobody quotes a ranking of the candidates or endorses a quantity. **8.5 Tone:** a busy operator's,
concrete, dates reconciling with the data; never a generator's voice or a task summary.

## 9. Provenance and hygiene

- **Provenance in `metadata.json`** in the task folder, outside `target/`: per file its source, date,
  licence, what it covers and how it was made, beside the distractors and the portal's keys. Nothing under
  `target/` describes the pack (§3).
- **Timestamps:** every mtime normalised to one in-fiction export date after the latest record.
- **Identifiers** structured (blocks, check digits, prefixes), never `id_001`; **scale** varies naturally.
- **A forced-implausible parameter** is stated in the design note with its arithmetic and mitigation.
- **Never ship** an answer-key column (`is_correct`, `should_exclude`), a README, a data dictionary,
  field notes, an extract manifest or any file or sheet that describes the data (§3), or a file name
  broadcasting the stump.

## 10. Build order

1. Read the design note: rungs (candidate, killing fact, carrying file), ask sheet (pool, device, path).
2. Spine (§2). 3. Calibration corpus if needed (§4), records first, twin pair from the start.
4. Operating extracts. 5. Lookup tables, each file's own conventions in its own form (§3, §6.5).
6. Compute every rung; assert separation, dominance, disagreement (§6).
7. Context artifact (§5), distractors (§8.3), `metadata.json`. 8. Governing document and voices (§8).
9. Mess (§7), then step 6 again: nothing moves. 10. Provenance in `metadata.json` (§9). 11. Verify (§11).

After any later data edit, re-run step 6 in full.

## 11. Verification

**Asserted paths:** every rung and rival-killer reproduces from the bundle; the default path lands on its
named wrong answer; each intermediate rung on its own; the correct path on the answer from shipped
evidence alone; the fork grid cell by cell, each losing cell mapped to the sentence it violates (maturity
and censoring included); mess neutrality per complication; the cracker sheet (`supplemental-stumping`)
outside every ask's bin.

**`checks.py`, 40 or more assertions:** the three-rules block (§7.1, R1 to R3c); rung winners by name and margins; position table; dominance;
disagreement both ways; calibration back-test and swept count; fork grid and every `SF` row; mess
neutrality; each graded figure's distance to its bin edge; every figure a voice quotes; no round totals,
shares or uniform counts; each load-bearing fact in exactly one file; the input gates; the realism sweep;
each distractor's deletion test.

**Independent verifier** (`generator/verify.py`): reads only the bundle, no generator state, on its own
code path, and recomputes every rung, rival-killer, calibration outcome and graded figure. The generator
writes `generator/figures.json` for `figures_check.py` (`determinism-check` §5).

**The verifier reads back every format the pack ships.** One assertion per format, and one per document
that carries a filed sentence, a graded figure or a convention the call leans on, through the verifier's
own extractor with the positive control on the same code path. A format only `checks.py` can read is
asserted by the hand that wrote it: the writer and the check share a variable, so a later edit to the
document's text leaves every gate green. Fourteen shipped builds in one lane were surveyed and six ship
PDFs their verifier never opens; one ships four PDFs that no script in its generator reads back at all,
so every authority clause in them rests on the writer's own string. The judge recomputes from the pack
and is the stronger check, but it runs once, after the pack is cut, and it is not a gate the build can
re-run on its own.

**Nothing in the pack may be procedurally assigned, and five shapes are measured rather than eyeballed.** A
generator's own arithmetic is the commonest realism failure a reader finds, and it is pack-wide rather than
local. Assert each of these in the realism sweep, per column and per document.
1. **No id, code or number column is an arithmetic sequence.** One build shipped plan site ids whose
   consecutive differences were exactly one value across every site (10437, 10474, 10511 at a step of 37),
   with licence numbers at 23 and street numbers at 53. A single sorted difference exposes the generator.
   Assert that no id-like column has one constant step.
2. **No ordering follows the alphabet or any other mechanical rule.** The same build's twelve service areas ran
   Ammerly, Bexhollow, Crannock through Lowenbrook in exact code order, so the names in code order were the
   names sorted. Assert the two orders differ.
3. **Entity names take more than two shapes.** Every site in that pack was "<Locality> Dialysis Center" or
   "<Locality> Infusion Center". Real registers mix a unit, a suite, a clinic, a named building, an operator's
   own brand on some rows, the odd abbreviation. Assert more than two distinct name shapes.
4. **No attribute is dealt round-robin.** An operator column cycled eight names in fixed order through forty
   sites and produced names contradicting what the sites did. Draw per row, give the counts an uneven spread,
   and assert both no fixed period in the sequence and no name that names one service while its rows deliver
   another.
5. **A document never states a position later than its own file date**, and a document's producer is the body
   that issued it: a regulator's fee schedule carrying the plan's name as Producer is a defect, and so is
   `Application` "Microsoft Excel" beside the writing library's own `AppVersion`. Assert both per document
   against its issuer.

**Byte-identical rebuilds:** two consecutive runs give identical `target/` bytes (fixed seeds, one RNG
stream per period, fixed mtimes, scrubbed metadata). A pack that does not rebuild has a broken generator.

## 12. Repair directions (data side; diagnosis is `stumping`)

| Symptom | Repair |
|---|---|
| Answer reads off at once | a rung below rung 0, in the data, never an artifact |
| Every insight reached, another answer defended from a file | raise the pin, cut the counter-pin, relabel the artifact |
| Wrong answers on an undesigned candidate | a second reading: close it by pin or convergence |
| Shallow scatter | cut idle complications; each rung on a plain join |
| Caught from one file | discriminator behind a join; evidence split over two documents |
| Rung does not reproduce, or flips under a variant | rebuild forward (§6.1); widen the margin |
| Decoy reached with no decisive step | twin pair, or break the over-determining flag |
| Adjacent rungs share a candidate; last rung idle | separation (§6.2); dominance (§6.3) |
| Axes show one profile | build the correlation (§6.4) |
| Name agreed, figure split | unpinned parameter: file it or converge it first |

Never repair with noise, removed evidence, arbitrary thresholds or harder parsing; never by deletion alone
(replace a deleted signpost with a filed pin or a convergence in the same edit); ship both halves of every
patch.

## 13. Anti-clone at the data level

- No spine (entity and grain, or real source) from a recent build; `guard.py check` enforces it.
- No context-artifact type, calibration form or extract shape repeated in consecutive builds; distractor
  types and wrong-basis kinds (vintage, unit, superseded rule, definition) rotated; pack size and format
  mix varied.
- Strip numbers and names: spine, artifact type and calibration form all repeating is the same pack.
- After the cut, `python3 .claude/skills/fingerprint/guard.py surface taskNN`; a promoted pair is renamed
  or regenerated.

## 14. Checklist

- [ ] Pairing in the design note; the objective's evidence ships; input gates asserted
- [ ] The three-rules block passes on the clean truth: R1 raw material, R2 per mess item, R3a analyst test, R3b decisive step alone, R3c no plant
- [ ] Every file does work; nothing broadcasts the stump; no answer key
- [ ] Calibration only where needed, confirming a filed criterion, records behind every row
- [ ] No artifact ranks the candidates wrongly (declared distractor excepted); context artifact reproduces
- [ ] Rungs forward-computed, separated, dominant; fork grid and `SF` rows asserted; pin once, at authority
- [ ] Mess real and neutral; clean-data test and realism sweep pass; every graded figure mid-bin
- [ ] 40+ assertions, verifier green from the bundle, byte-identical rebuild, `figures.json`, `guard.py surface`

## An assertion must measure what its own name claims

Two assertions in one day passed while measuring something else, and both would have shipped. One read "a sheet number alone does not identify a sheet" and was true only because a global id sequence was shorter than the row count, so numbers repeated for a reason unrelated to the claim, while the filed sentence saying each issuer has its own series was contradicted by every row. The other read "no single primary lifts a response to a third of the ask weight" and measured the solver's whole total rather than the lift, so it tracked a number its name does not mention.

The test is mechanical and costs one reading: cover the detail string and ask what the name promises, then ask what the code computes. If a different quantity would satisfy the code, the assertion is measuring the wrong thing even while it passes, and a passing assertion of this kind is worse than a missing one because it buys false confidence at a gate. Write the assertion so that the claim fails when the claim is false: for an identity claim, assert the key's parts are each insufficient AND the whole is unique; for a lift, assert the difference and not the level. When an assertion like this is rewritten, check that whatever it used to measure is still gated somewhere, and say in the report which assertion now carries it.

## An assertion that searches a document proves it read the document

A check that greps a shipped file for a string reports the same "not found" whether the string is
absent or the file was never readable, and three builds in one wave passed gates that had never run.
task195's `checks.text_of` could not decompress a golden PDF, so a whole assertion block passed by
never executing. task190's `_sweep` read every shipped file as raw bytes and so never saw inside its
three PDFs' Flate streams, which is exactly where the authority sentences live: every claim about
those documents, in every hand-back, rested on a sweep that could not see them. The same shape
catches a sheet read from the wrong workbook tab, a CSV opened under the wrong encoding, and a zip
member read without decompression.

**Every absence assertion carries a positive control.** Before asserting that a document does not
contain something, assert that it does contain a sentence you know is in it, taken from the writer's
own text, and fail the build when that control is missing. A search that cannot find what is there
has not shown that anything is absent. Where a format needs decoding, decode through the same helper
the verifier uses, so the bundle is read one way and only one way; and assert the extracted length is
non-zero per file, since an empty extraction satisfies every absence check in the build.

**The control runs through the same code path as the check, not merely the same file.** Proving the
bytes are readable proves nothing about the search that matters: task190's first control scraped a
reliability table with a generic number regex and matched version and clause numbers, so it would
have passed on text the real check never reached. Call the same extractor and the same parse the
absence assertion calls, and assert the control's own match, so a control that passes means that
search, on that text, found what is there.

## Document control dates are a consistency surface

Every date a document states about itself (approved, issued, refreshed, reviewed, superseded, a revision
row) has to be checked against the window of the data that document covers and against every event it
mentions. Adding owners, issue histories and review dates to make a file read as the organisation's own
record creates this surface where there was none, so the check runs after the addition, not before.
Measured instances in one wave: a model card refreshed two days before the run it reported completed; a
handbook approved in one year describing a code reissue from the next; a dictionary at issue 4 dated
February listing files that cover March to May; an extract stated as pulled on one date carrying 1,291
release dates after it; a protocol approved in February naming a June pull date and a May window; and four
tracker entries opening before the products they track were marketed. Assert it: no document's stated date
precedes an event it describes, and no extract carries a date after its own pull.

## Generator cost, where it decides what gets measured

A generator that takes minutes per run makes the sweeps that settle a draw unaffordable, and the draw then
rests on one world rather than on a measured range. The cheapest win is to collapse the record to its
distinct shapes before any iterative fit: a likelihood over interval-censored rows depends only on the
distinct intervals and their counts, so aggregating first reaches the same fixed point to the last decimal.
Measured on one build at 88 times faster, 100 seconds to 1.14, which is what made its nudge and floor sweeps
possible at all. The same holds wherever an iteration reads a row only through a key a thousand rows share.
