---
name: reduce-house-fixes
description: The register of defects the author has had to fix by hand after a build was already called finished. Each entry carries the general form of the defect rather than the incident, what it costs when a reviewer finds it, and the check that would have caught it before the bundle shipped. Use as the last pass before a bundle is declared ready, when a house fix comes back from submission and has to be recorded, and alongside the stumping pre-ship checklist, which routes here.
---

# House Fixes

A house fix is a defect caught after the build was called finished: cheap to prevent, invisible to the
build's checks. They sit in the artifact being *what it claims to be*, not in the analysis.

- **When.** Last block of the build stage, before the leak and duplicate checks, beside `golden-realism`
  (this register owns the container, H1, and the write-up prose, H2 and H3).
- **Wire every check into a verifier** (`verify_pack.py`, the submission verifier); eye checks lapse.
- **Reading is delivery, writing is bookkeeping.** New entries only after hand-over, for surfaced defects.
- **When the check and the defect share a blind spot** (a tolerant reader, a regex missing a unit class),
  the check certifies the defect.

Entries: **Defect**, **Cost**, **Line** (where the rule stops), **Check**, **Repair**.

---

## H1. A generated binary carries its writer's name and the build clock
- **Defect.** Writers stamp their name (`dc:creator`, `<Application>`, `/Producer`, PNG chunks) and a
  real-clock timestamp into metadata, unseen by text checks.
- **Cost.** The signature says generated; the timestamp contradicts the setting, both ways (`python-docx`
  stamps 2013). Assert a band, not a ceiling.
- **Line.** Signatures: scrub inputs; a script-made golden may keep its own. Timestamps: scrub every shipped
  file whose body states a date, goldens included. Scrubbing both everywhere is the cheap way out.
- **Check.** Sweep the pack and the deliverables (two generators): no writer name, no stamp outside the
  band. Wire OOXML, PDF and image branches even before a file of that kind ships.
- **Repair.** Byte-level, never a re-save (it re-stamps). OOXML: repack same entries in order, change only
  `docProps/`, assert every other CRC unchanged. PDF: equal byte length (xref offsets), surplus as
  whitespace between tokens, never padding inside the value; substitute after the `%` of a comment line,
  never the marker. Verify with zero logged parser errors (`pypdf` degrades silently). Scrub after each
  save in the generator; prove it by regenerating into scratch and matching the shipped file.
- **Tooling.** `scripts/scrub_producer_metadata.py <dir>` audits; `--apply --producer "<fiction org>"
  --stamp <fiction date>` repairs (restores on failure). Without `--floor`/`--ceiling` from the fiction it
  reports stamps unjudged. A retrofit, not the generator scrub.

## H2. A figure in the write-up whose derivation is not on disk
- **Defect.** A supporting figure (enumeration count, margin) came from a scratch search script over unbuilt
  configurations, not the verifier; nothing on disk reproduces it.
- **Cost.** One failed reproduction taxes the whole write-up.
- **Line.** Derived figures must recompute. Parameters (a band edge, a schedule) are choices and must only
  be consistent with the file that states them.
- **Check.** List numeric claims in every document **and the design note** by unit class (integer, %,
  ratio, count, decimal) and name what sweeps each. Read enumeration claims by hand ("which script prints
  this?"); re-derive a grid's axis list from the bundle (six binary moves are 64 cells). State the thinnest
  margin and name the wrong cell, its reading and value.
- **Repair.** Measure (it usually strengthens the claim). If it cannot be re-derived, restate to a weaker
  supportable claim, never reconstruct. Grep the figure, not the sentence, and fix every copy.

## H3. The prose around a computed figure is the part nothing checks
- **Defect.** Verified digits, drifting words: count word, comparator, population, keying parameter (a
  file date restated by memory, worst bounding a window), unit, label, rounding path, distance to a rival,
  stated reason, a bound (an extremum, printed floor for "at least", ceil for "at most"), a statistic's
  referent, the pack's own rounding rule, a "twin" claim.
- **Line.** Two roundings of one quantity are fine when the document says which is which.
- **Check.** Ask of each figure sentence: how many, against what, of whom, in what unit. Better, emit the
  words from the objects that made the number (`len`, the divisor variable, the source file named).
- **Repair.** Fix every restatement; when deriving prose, confirm prose-free artifacts are byte-identical.

## H4. What ships is not the asset list that was declared
- **Defect.** More (a second archive copy, an enclosing folder, OS entries), less (graded content only in
  stdout), or unopened (a visual nobody looked at).
- **Cost.** Copies often differ (diff them and run the golden on both before deleting one); stdout-only
  content scores zero for a grader that does not execute.
- **Check.** Archive members equal the declared list by name; no enclosing folder, no OS entries; open every
  visual; name the shipped file carrying each block of rubric points.
- **Repair.** Name the byte-identical invariants before editing a generator and assert them after; if
  something that should not move moves, revert and redo.

## H5. The rubric grades one reading of an ask that licenses two
- **Defect.** A criterion the golden fails (a band excluding its own restatement, a value no file states),
  an ask licensing two readings (denominator, term count, date convention), or label/criterion wording drift.
- **Cost.** Discrimination: correct work on a licensed alternative scores wrong. Visible as several distinct
  filed answers across runs.
- **Line.** An incoherent reading is not a licensed one; say in one clause why the golden is the reference.
- **Check.** Per ask, list every reading and its value; pin or accept both. Band within the measured
  margin to the nearest wrong answer. Punctuation can split one criterion in two when counted.
- **Repair.** Before grading, close the reading with one clause in the ask. After grading the prompt and
  inputs are frozen: fix in the criterion and record why.

## H6. A rule stated in the golden that the record does not obey
- **Defect.** The load-bearing rule omits a qualifier (start date, regime, population, precedence); it
  answers forward correctly and mispredicts rows already in the pack.
- **Cost.** Reviewers back-test the rule first; mispredictions kill its authority.
- **Line.** A narrow rule is fine; an unstated narrowing is the defect.
- **Check.** Run every stated rule over every observation; target zero mispredictions. The exceptions'
  cluster names the missing qualifier; confirm it is evidenced in the pack.
- **Repair.** Add the qualifier everywhere the rule is stated (components, steps, shipped document), re-run
  to zero, say whether the answer moved.

## H7. A shipped archive that disagrees with the tree it was cut from
- **Defect.** Any rebuild after the cut leaves the zip stale. A nondeterministic writer (PDF `/ID` and
  `/CreationDate`, image stamps, archive mtimes) makes every rebuild byte-different, so staleness is
  permanent and regressions are invisible.
- **Line.** Content must agree; metadata the fiction never fixed need not, until reproducibility rests on it.
- **Check.** Compare archive to tree by content, never mtime (`dataset-generation` §9 normalises mtimes).
  Run the generator twice and assert byte-identical output.
- **Repair.** Pin nondeterministic fields by equal-length substitution from a fiction-derived value. Cut the
  archive last and let a freshness assertion, not build order, guarantee it.

## H8. A citation that outlived the thing it cites
- **Defect.** A clause, file or field cited by name was renamed or renumbered; the citation points at
  nothing.
- **Cost.** Reads as fabrication; in a golden, a Gate A finding.
- **Line.** A citation to a deliberately withheld document recorded in the design note is design.
- **Check.** Resolve every reference in goldens, submission and shipped scripts: clauses against documents,
  file names against the archive, fields against headers. Run after any rename.
- **Repair.** Grep the old address to zero and re-derive the artifacts rather than editing them in place.

## H9. A file in the pack whose job is to describe the pack
- **Defect.** A data dictionary, field notes, an extract manifest, a readme or a notes sheet ships under
  `target/`: it tells the solver what each column means and how the files join, beside the very columns
  the decisive step reads, and as a hand list it also misses the file added late.
- **Cost.** task144's first architecture came back FAILED_TO_STUMP: its field notes defined the feed
  surface a few lines from the follower count and its manifest named every file's role, and both portal
  responses built the decisive cascade from them.
- **Line.** A code crosswalk, lookup table or governing document the organisation really keeps is data; a
  file whose job is to explain the pack is not. Provenance lives in `metadata.json` outside `target/`.
- **Check.** The generator asserts no readme, dictionary, notes or manifest file or sheet under `target/`,
  by name and by content, and that each convention a solver needs is carried by the file's own form
  (zones in its timestamps, grain or unit in its column names, codes in a crosswalk without glosses).
- **Repair.** Delete the file; move each convention into the producing file's own form, or into a
  governing document where the organisation itself defines it; rebuild and re-run every fork assertion,
  since a reading the register used to close is now closed only by the data.

## H10. A rival-killer whose every miss the pack's own rules can excuse
- **Defect.** A calibration corpus refutes rivals by raw miss count, but the pack files a discretion rule
  (one slot per period, a materiality floor, a deferral) that charitably excuses every miss.
- **Cost.** Gate C `competing_defensible_answer` on a green back-test; the fix is a data recut.
- **Line.** The discretion is load-bearing fiction; the defect is asserting refusal by an excusable count.
- **Check.** Score each rival under the most charitable reading of every filed discretion: at least one
  inexcusable miss per rival at every bar, asserted by case name with margins, in generator and verifier.
- **Repair.** Plant refusals where the discretion cannot reach, opposite to the open question's mechanism;
  re-assert the whole corpus after the recut.

## H11. A superseded write-up left readable in the task tree gets graded as the live one
- **Defect.** An archived failed version under the task folder holds a second `submission.md` or
  `prompt.txt`; any consumer that discovers by name (judge glob, uploader) can grade the dead one.
- **Cost.** A review cycle lost to `solution_incorrect` on figures the live write-up never states.
- **Line.** Dead builds live as lines in `## Tried and rejected`; dot-prefixed folders do not hide copies.
- **Check.** Exactly one `submission.md` and one `prompt.txt` under the tree; no `prompt.md` beside
  `prompt.txt`; no markdown outside the task root and bundle; no superseded-build directory.
- **Repair.** One line per dead end in the design note, then delete the trees (never rename or zip). If a
  review ran on the stale copy, say so in the resubmission.

## H12. A prompt whose precision pins read as a grading sheet
- **Defect.** A rounding tag on every clause turns the request into a checklist of graded figures.
- **Line.** Pins are Gate E load-bearing; only counts of discrete things need none.
- **Check.** `voice-check.py` rounding-at-the-close rule: rounding words only in the last sentence, each rule
  naming its figures. Classify every figure as natural integer or derived; every derived one is covered.
- **Repair.** One closing rounding sentence; each dropped tag's figure is integer by construction or named
  there.

## H13. A prompt whose committed call reads as one output among several
- **Defect.** Equal paragraphs per deliverable, the call buried, the lead clause a series of figures.
- **Cost.** First-pass rejection as a collection of outputs, and solvers spread effort evenly.
- **Line.** The supporting layer stays; the defect is hierarchy, not inventory (except H18).
- **Check.** `voice-check.py` question-first rule: the call is a direct question in the first two
  sentences; each file tied to the quantity it stands up; the committing file leads with exactly one
  quantity.
- **Repair.** Lead with the call as a question, demote other figures to the file sentences, rounding to
  the close; re-check every moved pin.

## H14. An estimation domain the golden picked silently, that the data then argues against
- **Defect.** Unit and rounding get pinned; the grain of every rate does not. A finer cut gives another
  answer. The generator often causes it: a quota filled by a prefix of a list blocked by an attribute gives
  every later block a degenerate outcome, worst when the attribute is rare in history and common forward.
- **Cost.** Gate C against the strongest solver, and a data recut. Re-argue stump power after: the old
  wrong answers came from the fork.
- **Line.** Some grains are the intended correction; pin at the boundary of the quantity the attribute
  governs, never the attribute outright.
- **Check.** For every rate, compute the answer at every grain the data allows; a different committed answer
  is an open fork. Keep the finer estimator as a live verifier assertion. Assert no subgroup has a
  degenerate outcome rate, judged on cases at risk.
- **Repair.** Data first: permute labels inside each outcome group (aggregates untouched), spread with a
  carry keyed to the rival's pooling. Then pin positively in a file the naive path opens, scoped to its
  quantity, never naming the attribute or forbidding a required projection. Name invariants first.

## H15. A referee that only arbitrates downstream of a hazard
- **Defect.** A corroborating file confirms the governing input only on the population left after a device
  (archived block, duplicate, scope rule) is solved; on the raw data it backs neither, or the wrong one.
  The governing rule sits in one register cell unreachable from where the question arises.
- **Cost.** A false stated basis lands `competing_defensible_answer` on a forced answer.
- **Line.** Keep the hazard and the candidates; change only what the pack declares.
- **Check.** Compute every claimed corroboration on the pre-hazard population as well as the golden's;
  assert both. Assert every governing rule is reachable from the file whose semantics raise the question,
  and stated exactly once.
- **Repair.** Declare the dependency in the sibling rows' voice; route to the authority without
  restating; make the basis sentence true as written and name the rival's value.

## H16. A pack whose internal dates run ahead of the documents that cite them
- **Defect.** Generated offsets push record dates past the extract date in the manifest and the memo date.
- **Cost.** An in-fiction contradiction, worst on a load-bearing "latest" column.
- **Line.** Forward-looking records (plans, validity windows) go on a file-by-file allow-list, never a
  pattern.
- **Check.** Files with dates past the export date equal the allow-list; each extract column's max is on or
  before that extract's registered date.
- **Repair.** Shift the offset uniformly, never clamp (ties change "latest" winners); recompute every fed
  figure; check the range's lower end too.

## H17. A batch of prompts that are individually fine and collectively one prompt
- **Defect.** The same opening, verbs and file set across a batch, invisible per pair, usually prescribed by
  a skill.
- **Cost.** A client note on the whole batch.
- **Line.** The contract repeats (first person, one call, one to three files, units, rounding); the carrier
  must not.
- **Check.** `voice-check.py` bare over the window: no question form over a third, no repeated six-word
  phrase, a format mix more than one row deep. Read the counts, not self-report.
- **Repair.** Forward only: rewrite the prescription (worked example, checklist line) that taught the
  skeleton. `clone-check` Track A adjudicates.

## H18. A supporting ask that passes the hierarchy reads and is still a second decision
- **Defect.** An ask built outward from a device lands on a quantity someone wants for another decision
  (next cycle, a compliance exposure); it is tied to the call only by grammar.
- **Cost.** First-pass rejection as multiple independent outputs; no reordering fixes it.
- **Line.** Independent difficulty is fine; independent decision is not. The answer must be a component, a
  qualifier (sensitivity, flip condition, reconciliation) or the audit trail of the call.
- **Check.** Each ask's line in the ask ledger names how its answer enters the call; one naming another
  decision, window or owner is independent. Read the ledger, not the prompt.
- **Repair.** Retire it; win criteria back inside the decision (a second measure per candidate, an input's
  audit trail, a reconciliation, on rows outside the main call, `supplemental-stumping` Part 1.3). A grain
  split inherits the main trap. Re-derive the pair ceiling; regenerate golden, verifier and answers together.

## H19. A sibling build's archive attached under this build's name
- **Defect.** Identically named archives across a batch; the wrong one is uploaded and every on-disk check
  still passes.
- **Cost.** A full determinism failure on an unexamined build.
- **Line.** If this build's own archive lacks a named input, it is H4.
- **Check.** Print each archive's size, member count and digest at ready time; compare with the upload.
  Assert the write-up's inputs are in the target archive and the golden archive is exactly the deliverables.
- **Repair.** Re-attach, change nothing, quote the review's file description as evidence, name archives
  with the build number, ask the author to re-test.

## H20. A build whose domain fit is established everywhere except the prompt
- **Defect.** The registers carry the institution; the prompt, trimmed for leaks, does not.
- **Cost.** Rejection on the tag, inviting the wrong repair (redrawing the domain).
- **Line.** No explanatory sentence, nothing on the ban list (standard acronym, eligibility rule, deciding
  metric, rate basis, population). Licensed: who decides and what is released.
- **Check.** Read the prompt cold and name the domain. Assert the subdomain's institutional nouns (literal,
  from this fiction) appear in the prompt, paired with a leak assertion limited to ban-list phrases.
- **Repair.** Inside existing sentences, with nouns from the bundle: qualify the deciding body, say what is
  released, give the requester's organisation its adjective. Re-run verifiers and voice check.

## H21. An invented name that sits a few letters from a real organisation, school or place
- **Defect.** Exact-match checks pass names one or two letters from a real one, or containing its
  distinctive word (saints, townlands, venue words, staffing brands).
- **Line.** Generic geography (river, bay, county) is texture; the distinctive remainder is the test.
- **Check.** Normalise invented and reference-register names (case, accents, punctuation, generic org words
  dropped); fail at edit distance two or less or containment; no retired name survives a rename.
- **Repair.** Rename in the generator, rebuild, confirm figures unchanged; prefer descriptive names.

## H22. Constructed records inside a file the pack presents as a real download
- **Defect.** Fictional organisations added to a real public file in its layout while provenance says
  "used as published".
- **Line.** A declared constructed layer is normal; the silent mixture is not.
- **Check.** For every file provenance calls a download, compare rows and keys with the kept raw download;
  fail unless provenance declares additions.
- **Repair.** Move constructed records to their own files, or declare additions and construct more
  organisations than the ladder needs so "constructed" does not mark the decisive ones; re-check
  camouflage.

## H23. An ask whose wording presupposes what the data holds
- **Defect.** An ask requests a count with a property of the counted items, or names a subset or a direction
  of change as given ("how many of them and what they cost", "the sites where it fell"), so the prompt states
  a fact about the data before a file is opened.
- **Cost.** The client's prompt review fails the prompt on it alone, as a leak; where a rung or device depends
  on the presupposed fact, the step is also handed over.
- **Line.** A fact the requester knows before any analysis (their own sites, the cut-over date) is furniture;
  a fact only the analysis establishes (a count is non-zero, a subset exists, a figure moved one way) fails.
- **Check.** Read every ask about a subset with "none" as its answer; flag
  `how many[^.]* and (what|which|how much) (they|their|those|it|its)` unless the sentence carries "whether" or
  "if so".
- **Repair.** Make "none" grammatical and keep every figure, unit, rounding and per-unit structure, so the
  criteria count does not move; never delete or fold the ask. Where a unit's answer is zero, golden and
  write-up say "none".

## H24. A provenance record that steps outside the fiction
- **Defect.** Every file reads as the organisation's own record except the provenance or licence file, which
  says in the author's voice that the files were constructed, invented or made for an exercise.
- **Cost.** The client's input-asset review fails the pack on authorship, blocking on its own; it is often the
  first file opened and the review stops there.
- **Line.** Who compiled the folder and when, the licence, each file's source and pull date, and real names used
  descriptively stay. Any statement that the world is constructed goes to the design note, the card and the
  portal's provenance field, never under `target/`.
- **Check.** Sweep `target/` for a sentence saying the pack was built ("constructed for this exercise", "are
  invented", "are fictional"); read the bare words "fictional", "fictitious" and "this exercise" in documents.
- **Repair.** Rewrite it in the generator as the organisation's own compile note (a team the pack already uses,
  the pack's export date), rebuild, confirm every other file, the golden and the write-up byte-identical (H7).
- **Tooling.** `leak.py` sweep 2: the built-pack sentence is LEAK in any file, the bare words REVIEW in
  documents; it cannot tell an in-world "fictitious vendor" from a tell.

## H25. A shipped document validated by the same permissive reader that wrote it

- **Defect.** A document under `target/` is unreadable to a parser a solver would reach for, while the
  generator's own "the text is unchanged" assertion reads it with the lenient reader of the library that
  produced it, so the defect ships green. The decisive rule can sit in that document, which puts the whole
  build out of reach on the commonest route into it.
- **Cost.** A solver on the ordinary route cannot read the governing clause at all, so the response is
  graded against a call the pack never showed it. It also reads as a corrupted pack in the input review.
- **Line.** A document a writer library emits is fine; what is not fine is an in-place byte substitution in
  a structured container. Patching a `/Info` string, a sheet name or a container header by offset moves the
  bytes that the cross-reference table or the escaping depends on. Re-serialise through a library that
  rewrites the structure instead.
- **Check.** Open every shipped document with every reader a solver is likely to use, not one, and assert
  the decisive sentences are present in each: for a PDF, a lenient reader and a strict one and at least one
  independent text extractor. Assert the strict reader's text equals the lenient reader's. Assert any string
  the generator rewrote is still a balanced, correctly escaped literal.
- **Repair.** In the generator, re-serialise the document rather than patching bytes, then confirm the
  rebuild is byte-identical twice and the golden that shares the code path is fixed by the same change.
  Normalising through a second library also drops the writer library's header and trailer comments, so the
  toolchain signature goes away rather than being overwritten in place (H1).
- **Tooling.** `leak.py` sweep 10 reads the container's writer signature and sweep 7 reads hidden content;
  neither opens the document twice, so neither can see this. The assertion belongs in `checks.py`.

---

## H26. A gate whose "nothing found" and whose "nothing to look at" print the same

**The defect.** A check reports a clean result for a build it could not actually examine, and the clean
result is indistinguishable from a real pass. The measured instance: a retired scoring gate identified the
committed answer by a `call.` key prefix, so on a build that files its call at the top level under its own
name (`plants_over_amber`, `sectors_over_tolerance`, `referred_count`) it found no call figure, printed
`call figures 0 of 0 hit`, and exited 0 with `PASS the call missed`. Three of the six builds in one audit
batch key the call that way, so a third of that audit would have recorded a pass for a call nobody scored,
on exactly the builds an audit exists to catch.

**What it costs.** More than a missed finding, because a false pass is banked as evidence and argued from
later. The four builds measured before this was found were scored correctly only because they happened to
nest their call under `call.`; nothing in the output said which of the two situations it was reporting.

**The check.** A gate that can be inapplicable says so and exits non-zero. Give every such gate a third
outcome beside pass and fail: it found the thing and the thing was clean, or it could not find the thing to
check, and the second is an error with the fix in its own message, printing what it looked for and what it
found instead. Read any gate whose quiet output is a zero count and ask whether a zero means clean or means
absent.

## H27. A draw-time gate run on an already-drawn build, reporting its successors as collisions

**The defect.** A gate that screens a *proposed* draw against the cards a reviewer would read beside it is run
again later on the finished build, and by then the cards filed after it are in the comparison set. It reports
axis bans and structural repeats against builds that did not exist when the draw was made, so a shipped build
accumulates BLOCKs as its neighbours register, and none of them is a finding about it.

**The measured instance.** `guard.py heart` on a build drawn 13 October returned three BLOCKs: an axis ban
against a card registered later the same day and the two structural tests against cards drawn on the 15th and
the 16th. The build's own card had not been touched, so the verdict was identical before and after the work
being gated. `cmd_check` filters the comparison set by draw order for a filed card; `heart` runs the full check
and that filter did not reach these rules.

**What it costs.** It makes a mandatory gate unpassable for any older build, so a repair that must run it either
stops on a false finding or learns to ignore the gate, and the second is worse: the next real BLOCK is ignored too.

**The check.** Before acting on a BLOCK from a draw-time gate on a build that is already drawn, read the
colliding cards' `drawn` dates against the build's own. A collision with a later card is an artifact: record it
with the dates and carry on. A gate meant to run at two different times says which comparison set it used.

## H28. A measurement whose denominator is whatever the generator happened to file

**The defect.** A score is reported as a fraction of "the figures", where the denominator is every key in a
generator's own figures file rather than the figures the rubric grades. Builds file their provenance there
beside the graded answers, so the denominator and the numerator both swell with things no rubric scores, and
the percentage says more about a build's filing habits than about the build.

**The measured instance.** A retired scoring script reported a build as leaking 24 of 49 ask figures, 49 per
cent, and the build was sent for a rubric repair on that number. **Twenty of the twenty-four hits were the pack's own row
counts, the governing standard's stated constants and the window's dates**: a response that counts 111,454 rows
in a file and repeats a published 49.920 Hz threshold has shown nothing. Re-scored with those excluded the
layer sat at 4 of 29, under the bar, and the build needed no repair at all. The real leak was two figures,
which the same output had buried among twenty-two irrelevancies.

**What it costs.** A whole repair aimed at the wrong build, and the right finding, two figures with a named
cause, hidden inside a number that looked decisive. It also cuts the other way: a build that files little
provenance is scored harshly beside one that files a lot.

**The check.** State a score's denominator before reading the score, and make the instrument print what it
excluded so the exclusion can be argued with (the cracker and pair-ceiling scripts in `checks.py` included).
More generally: when a measurement decides work, read one
case's rows by hand before trusting the fraction.

## H29. A bound rounded to nearest, so the write-up claims a margin the pack does not hold

**The defect.** A figure the write-up states as a bound ("at least N per cent clear", "no more than N days",
"a margin of at least N") is computed by rounding to nearest. Rounding to nearest moves a bound outward half
the time, so the sentence asserts a margin no row in the pack meets, and the judge recomputes the worst case
and finds the claim false.

**The measured instance.** A build claimed every unit sat "at least 12 per cent clear of the standard" under
all four licensed estimates. The worst case was **11.54 per cent**, and two of thirteen units sat under 12.
`int(round(11.54))` printed 12, the write-up quoted it, and `figures_check.py` passed because the write-up and
the figures file carried the same wrong integer. Nothing in the chain compares the printed bound with the
quantity it bounds.

**What it costs.** A Gate A finding on a graded Critical Components claim, found by whoever recomputes rather
than by the build. The figure is correct to the rounding its own line states and false as a sentence, which is
why every gate reads it clean.

**The line.** A quantity reported *as* a level rounds to nearest. A quantity reported as a bound rounds
**toward the bound**: floor a lower bound, ceiling an upper one. The write-up's own verb decides which it is,
so read the sentence, not the key name.

**The check.** Two assertions per bound, not one. The usual floor assertion (the bound clears its gate) misses
this entirely, because 12 passes a `>= 11` test. Add the comparison the sentence makes: the printed bound is
at or inside the worst case the pack holds, asserted against the recomputed extremum in `checks.py` and again
in the verifier. Where a write-up sentence states a bound over a family of methods, the extremum runs over
every member of the family the records license, not over the shortlist the generator happens to assert.

## H30. A scope gate whose "nothing moved" cannot tell a clean repair from no repair

**The defect.** A gate that proves a targeted repair stayed in scope does it by comparing graded figures
before and after. When the repair's whole point is to change what the natural pipeline finds while the right
answers stay put, every figure is unchanged and the gate reports that nothing graded changed, which reads as
"this repair did nothing". The cleanest possible repair and the empty one print the same line.

**The measured instance.** An ask layer was rebuilt on three new devices: a re-sent settlement file, a
notification channel that loads monthly rather than daily, and a recovery route the scheme remitted centrally.
The pack changed in four files and gained a fifth; the natural read moved on 55 of 55 graded figures. Not one
golden answer moved, because each device changed where the evidence sits rather than what it sums to. The
scope gate passed with "ask figures that moved: 0" and a WARN saying nothing graded had changed.

**What it costs.** Nothing, if the author reads the warning and answers it; a repair redone or abandoned if
anyone reads the gate's output as the verdict. It also cuts the other way: a repair that moves many ask
figures looks productive on this gate whether or not any device got harder.

**The line.** Scope is "did the frozen side move", which the gate does measure. Effect is "did the natural
read move", which it does not. An unmoved ask figure is evidence about scope and says nothing about effect.

**The check.** Read the forcing measurement beside the scope gate, never instead of it: the per-figure gap
between the natural read and the golden on the cut pack, with its own rounding beside it, asserted in the
generator and printed by the ceiling script. Where a repair moves no graded figure, the design note says so
in those words and names the files that did move, so the next reader is not left inferring from a WARN.

## H31. A corpus gate cleared, then the corpus moved before the push

**The defect.** The anti-repeat gates compare a build against every other card on file, so their verdict is
true only against the corpus they read. A session that clears one, then pulls, then pushes has shipped against
a clearance the pull invalidated. The same holds across a day: a build that passed months ago can go BLOCK
without anyone touching it, because the collision arrives from a sibling or another author's draw.

**The measured instances.** Two in one session. One build's duplicate check was cleared with a differentiation
line, and a later pull brought in a card that fired a **different** similarity test on the same build, so the
build was pushed carrying a BLOCK its own repair had already answered once. Another build's gates were
recorded at ship as a WARN with one promoted pair; re-run four days later the verdict was BLOCK on three axes
and the surface screen promoted three pairs, two of them new. In both cases the driver text was never the
cause (nearest neighbour 0.06), so nothing about the build had changed.

**What it costs.** A shipped build whose identity collides with a neighbour the reviewer holds, which is the
exact failure the gates exist to stop, and an author who reads a stale PASS in the state file and believes it.

**The line.** A gate that reads only the build (prompt voice, figure reproduction, byte-identical rebuilds) is
settled when it passes. A gate that reads the build **against the corpus** is settled only as of a commit. The
state file records the verdict with the date and the corpus it was read against, never as a bare PASS.

**The check.** Re-read every corpus-comparing gate after the final pull and immediately before the push, not
when the repair is finished, and re-read them on any build being resumed rather than trusting its state file.
Clear a similarity finding with a differentiation line, never by relabelling an axis; an axis ban is cleared
only by redrawing the axis, and when the ban arrives from a build registered **after** this card, that is
still a redraw and not an exemption. Read the verdict line rather than the exit code where a tool prints both.

## H32. A gate that reads a block's form and never its content

**The defect.** A gate checks that a required block is present, that its labelled lines exist and that each
carries more than a word. It never reads what the lines say. So a design note whose own text records that the
build FAILS its own rules passes the gate, and a reviewer reading the exit status sees a compliant build.

**The measured instances.** Two builds in one day. One rewrote its thirteen labelled lines to the measured
truth, with five of them opening on the word FAILS, and its gate still printed "51 checks, 0 FAIL, 0 WARN",
including a PASS on a `Lesson:` line whose text begins "as drawn there is none a model can take". The same gate
printed PASS for "decisive rung silent" by reading the verdict word out of the note's own table while all three
readability tells were measured firing. A second build's rework was refused on measurement and its state file
still satisfied every field the resume gate tests, so the board offered it as freely resumable.

**What it costs.** A refused architecture reads as compliant, and the refusal has to be rediscovered by whoever
next picks the number up. It also cuts the other way: an author who writes the honest failure gets the same
green as one who writes to pass, so the gate gives no reason to be honest.

**The line.** Presence is checkable mechanically and is worth checking. A verdict is content, and a gate that
cannot read content should not print a verdict about it. Where a line's own text carries the answer, the gate
reports what it read rather than a PASS.

**The check.** Two cheap ones, both additive and neither blocking. Scan each labelled line's content for a
leading failure verdict (FAILS, dead, spent, none, not drawable) and emit a WARN naming the line, so the exit
status stops disagreeing with the prose. And have the resume gate test the note's verdicts rather than the
existence of its fields, so a build refused on measurement cannot read as resumable. Until a gate does that,
read the note before trusting the gate: on a rework the note is the record and the exit status is a formality.

## Adding an entry

An entry is a **class** a future build could repeat with other nouns; anything else goes in the design
note. Order: Defect, Cost, Line (if a legitimate twin exists), Check (a wireable assertion), Repair (its
own failure modes), Tooling (only if a tool exists; say what it refuses to decide). No dates, file names
or incident numbers.

## H33. A build that reproduces its pack but not its gate, because a second entry point writes the figures

**The general form.** A generator has more than one entry point, and the obvious one builds the pack while a
second one ENRICHES `generator/figures.json` before writing the submission. Rebuild from the obvious entry
point alone and the pack is byte-identical, every hash matches what is committed, and `figures.json` is
quietly SHORTER than the committed copy, so the build passes a pack audit and fails a gate audit at the same
moment. Measured on a shipped build: `build.py` alone cut 23 lines from `figures.json` (a `constants` block
plus two count keys) while `target.zip` still matched at `ce23c1aa6f4a57e9`, and `figures_check.py` went
from 91 of 91 to **4 absent**, naming figures the shipped write-up cites in its own steps (a site-episode
pair count, a qualifying threshold and its dwell, a dead band, a span, a tolerance). Running the second
entry point restored the file to the committed bytes exactly and the gate to 91 of 91.

**What it costs when a reviewer finds it.** Worse than the defect: it invites a Gate A challenge on figures
the write-up states and the generator appears not to emit, on a build that is actually sound. It also costs
the author the audit itself, because the first reading of the evidence is that a shipped build has regressed.

**The check.** A rebuild audit runs EVERY generator entry point that writes `figures.json`, in order, not
just the one named `build.py`; enumerate them first (the modules carrying a `__main__` guard) rather than
assuming one. And the clean-tree test is the cheap tell: after a full rebuild `git status` must be empty for
the task folder, so a `figures.json` left modified is the signal that an entry point was missed, not that
the build moved. Where a build does have two steps, its own record names them in order so the next audit
does not have to rediscover it.

## H34. A measuring script that scores nothing reports a pass

**The defect.** A gate script computes a rate over the rows it managed to score and prints its verdict on
that rate, so a run that scored no row at all divides into an empty set, reports zero per cent and passes.
The failure is invisible in exactly the case that matters: the build whose evidence never arrived looks
identical to the build that earned the verdict.

**What it cost.** A shipped build carried a passing ask-layer line on a run that scored zero of its ask
figures, because all twenty ask keys had left the denominator. The line was read
as evidence in two later sessions and quoted into a design note.

**The check.** Every script that prints a verdict on a rate refuses to print one when its denominator is
empty, and says which empty it was: nothing to measure, or nothing that could be matched. A guard on one
axis is not a guard on the next: the same script already refused a run with no call figure for this exact
reason and still passed one with no ask figure. When a rate is computed, grep the script for every
`if ... else 0` fallback on its denominator and give each one a refusal.

## H35. An isolated thread's brief that names the answer

**The defect.** A brief for an isolated thread (the leak reader, the judge's thread) carries identifiers drawn
from the artifact being checked, so an identifier can carry the answer. A key path with one component per
member of the committed set enumerates that set, and enumerating it beside the non-members is what the pack
does; enumerating it alone is handing it over.

**What it cost.** A retired scored read was briefed with a key list holding one path per slot of the committed
slate, eight of the week's forty-two, and named that list as its reason for choosing the method; the verdict
had to be withdrawn. The leak reader is exposed the same way (`leak-check`, the sweep lines kept out of its
brief).

**The check.** Brief the leak reader with the prompt and the pack only, never figure keys or figures. Where a
brief must carry identifiers, drop any identifier whose own components name the answer, defined mechanically:
a component is distinguishing when every sibling at its position is a member of the answer.

## H36. A tolerant comparison placed ahead of the exact one

**The defect.** A comparison routine grows a tolerant branch for a real case (a prose answer that should
match when the responder spells it with a qualifier) and the branch is written as the first test, keyed on
type rather than on content. Everything the tolerant branch can parse then takes it, including values the
exact branch below was written for, and the routine reports agreement where there is none. It fails open, so
nothing downstream notices.

**What it cost.** A scoring script matched the first three words as a substring whenever either side was
string-typed, before any numeric compare. Generators file a rounded share or rate as a string to keep its
trailing zeros, so a golden `"0"` matched a reader's 90, 50 and 40 alike, because `"0"` occurs in each. One
build's seven brand shares scored six hits where one was right, and five builds' ask-leak figures were
reported to the author inflated before the re-score.

**The second half of the same defect.** The repair was to put the exact compare first, and that over-corrected:
a one-member golden list stopped matching a reader that answered the member itself, which turned a landed
call into a held one on another build. A tolerant branch exists for a reason, so narrowing it needs its own
cases.

**The check.** Order comparison branches exact first, tolerant last, and gate each tolerant branch on the
content it was written for rather than on a type that a stricter case also satisfies. Then write the table
of cases out and run it: both directions of every tolerance (a one-member set against its member, a set in
another order, a string-typed figure against a number, a prose name with a qualifier) with the wanted verdict
beside each, as a test the script keeps.
