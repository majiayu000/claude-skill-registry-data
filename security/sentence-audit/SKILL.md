---
name: sentence-audit
description: Sentence-by-sentence precision pass for paper prose, divide a paragraph into sentences, test each against the first-time-reader defect list, rewrite minimally, condense aggressively; plus the LaTeX editing invariants (wrapping, per-paragraph commits, layout checks) that keep an edit pass safe. Use when polishing a section or caption for submission, when a paragraph reads wrong but the fault is unclear, or when auditing a figure-caption-table exhibit as a unit.
---

# Sentence audit (precision pass)

The refinement mode for near-final paper prose: take one paragraph (or
caption) at a time, divide it into sentences, test each against the defect
list, rewrite minimally, condense aggressively, verify, commit.
## The defect list (test every sentence against all of these)

1. **Wrong ontology.** The subject does something its type does not do:
   "states occurred" (states are visited), "the model increases to 0.93" (its
   score does). Name the true actor.
2. **Tautology.** The sentence is true by definition, so it informs nothing:
   "the replay reproduces the recorded trajectory." Report the CHECK'S
   OUTCOME instead: "every frame matches for 22 of the 25 tasks."
3. **Unowned objects.** A frame, number, or artifact with no stated source:
   "the recorded output" (recorded by whom, when?). Assign every object an
   owner: "the output the engine returned during the original run." When two
   sessions or systems produce the same kind of object, say now-vs-then
   explicitly.
4. **Wrong emphasis.** Scaffolding written like a finding. If a step only
   certifies inputs for the real measurement, open with the real
   measurement's purpose ("To run these comparisons ... we first ...") and
   demote the step's result.
5. **Definition assembled by the reader.** A colon followed by clauses with
   shifting subjects. Use one pattern instead: name the term, then a single
   subject-verb definition ("A pair is previously unobserved when ..."),
   mirroring the paper's other definitions verbatim in form.
6. **Undefined jargon.** A term the paper never defined, or defined only
   after use. Replace with the self-evident form or define at first use.
7. **Quantifier garden paths.** "fail at most tasks" parses as the
   quantifier "at most." Reword ("fail at most of them").
8. **Metaphor in a decode.** Captions and definitions take literal words
   only: "the model the agent learned while solving that task," never "the
   model its run leaves behind."
9. **Count and number mismatches.** A stated count must equal the list that
   follows and the table it summarizes. Recompute from the table or source
   data before trusting either side. NEVER silently change a printed number:
   verify against ground truth, then flag the change to the author.
10. **Redundant re-derivation.** The same mechanism explained twice on one
    page. Say it once where the reader needs it (usually the caption decode)
    and reference the term elsewhere.
11. **Non-parallel decodes.** Sibling items (table rows, list entries)
    described with different verbs force the reader to re-derive each one.
    Fix with one verb frame reused verbatim, only the slots varying.
12. **House prose axioms.** Sentences <= ~28 words, subject and verb early,
    zero can/cannot/could, no bare This/These, no em dashes, numbers glued
    to their objects and traveling in pairs, semicolons rationed to a true
    antithesis.
## The rewrite recipe

- Lead with purpose or claim; procedure follows.
- One subject doing one thing per clause.
- Reuse established terms verbatim; never coin a synonym for an existing
  term ("unseen" beside "unobserved" is a split, unify).
- Condense without fear: if the caption now carries a definition, the body
  sentence that repeated it dies. Target 20-30% shorter per pass.
- Captions are self-contained (a caption-only reader decodes every term,
  column, exclusion, and mark) and follow name -> decode -> land (the
  caption-writing skill).
## Figure-text exactness

A figure, its caption, and the table it corresponds to are ONE exhibit; audit
them together, not sentence by sentence in isolation.
1. **One vocabulary per exhibit.** Figure-internal labels (legends, bar
   names, colorbars) use the caption's terms, and when the caption says "the
   values correspond to Table N," the labels match Table N's row names word
   for word. Mismatched vocabularies mean regenerating the figure, not
   patching the caption around it.
2. **Legend entries are parallel.** Every entry fills the same slots. "at
   evaluation time, items scored" (a time) beside "final model, items never
   scored" (a thing) is a defect; "model during training, ..." / "final
   model, ..." is the fix.
3. **State the shared comparison once, up top.** When one comparison
   underlies every mark, say it first; each mark type then carries only its
   differences, decoded with ONE shared verb phrase. Defining each mark from
   scratch re-derives the machinery differently each time, that is why
   caption patches keep failing until the exhibit is restructured.
4. **Anchor every inference to the datum that proves it.** Before attaching
   a lesson clause ("exact replay does not guarantee generalization"), check
   the chart: the nearest-named example must be the one that proves the
   lesson, never a counterexample where both quantities agree.
5. **Explain visible anomalies where the eye lands.** If the author pauses
   on a mark pattern, a first-time reader stops dead: the caption explains
   the pattern in plain terms at that exact spot. Author-stumbles predict
   reader-stumbles, always.
6. **Timing and coverage in plain words.** "One prediction before every
   action" replaces modifier stacks like "precommitted evaluation-time
   predictions on pairs observed during the run."
7. **Check figure claims against the run data, not memory.** Per-item
   numbers live in the experiment's result files; pull them before asserting
   or fixing any figure-adjacent number.
## Verification questions that beat arguing

When the author (or a reviewer) disputes a factual direction, check the
artifact, not the prose: the experiment's README, the scripts that produced
the numbers, the table column sums. A claimed measurement direction is
settled by asking which results would be impossible if the other reading
were true.
## Editing invariants (hard rules for the pass)

1. **Hold until approved.** Present the audit + rewrite; apply only on the
   author's go-ahead (the natural flow: the author pastes a paragraph, then
   says "do the same" for the next).
2. **One commit per paragraph alteration**, descriptive message, so the
   history reads as a change log.
3. **Wrap LaTeX source at ~78 columns.** Never let a wrapper break
   hyphenated tokens (set `break_on_hyphens=False` or equivalent), and
   repair any broken-token damage before rewrapping. Atomic writes only
   (temp file + rename); a truncate-write mid-build corrupts the compile.
4. **Single writer builds.** Never run a build watcher while the author's
   editor has its own; check for running `latexmk`/`pdflatex` before any
   manual build. Corrupted aux files mean stale collision state; fix with a
   clean rebuild, not source edits.
5. **Layout invariant.** After every edit: rebuild, render the changed pages
   to images, READ them, and confirm the pages before and after did not
   reflow (page count + spot-render). Text extraction is not a layout check;
   "looks good" is judged on the rendered page, never inferred from a clean
   compile.
6. **Float discipline.** No forced page breaks to fix layout; reorder source
   so text fills columns and float numbering follows page order.
7. **Value or removal.** Every sentence is audited alone for clarity, logic,
   and the value it adds; a sentence that adds none is removed, not
   reworded. Between sentences the paragraph must flow and sound like
   natural, interesting human speech, not stacked declarations.
8. **No AI artifacts in any shipped file.** No em dashes, no trailing
   ellipses, no boilerplate connectors; the rule covers LaTeX, markdown,
   captions, and figure text alike.
9. **Author's wording wins.** When the author supplies a sketch (often as
   `%` comments, which are preserved verbatim), refine their sentences in
   their voice and order; never derive replacement prose from scratch.
10. **Layout gates.** Sections and appendices start at the top of their page
    or column; white space is minimized; zero formatting errors on the
    rendered page.
## Worked before/after specimens

- "the state occurred during the run, but the action was never applied from
  that exact state" -> "A pair is previously unobserved when the agent
  visited its state during the run but never took its action from that
  state."
- "We found that the system recreates the ground truth trajectory for 22 of
  the 25 tasks" -> "The replay is exact for 22 of the 25 tasks." (actor
  fixed, tautology killed)
- "Replay compares the final model with the recorded output" -> "*Replay*
  feeds each previously observed state-action pair to the model and grades
  its predicted output against the output recorded during the original run."
- A 38-word subordinate opener -> "Excluding the one order-sensitive task,
  the final models predict the complete output exactly for 68.6% of
  previously unobserved pairs."
