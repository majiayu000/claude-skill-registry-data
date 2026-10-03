---
name: caption-writing
description: Write or revise figure, table, and algorithm captions using recipes distilled from dissecting top ML researchers' papers. Use when adding or editing any caption, when a new exhibit enters a paper, or when a caption fails to stand on its own. Applies the name-decode-claim structure, the flagship-claims/workhorse-describes split, self-containment over deduplication, paired-number discipline, and mechanical checklists.
---

# Captions (master method)

Follow `caption-guide.md` in this folder, the complete plain-English method.
This file is the operating summary.
## Process

1. **Name the exhibit.** Open with a verbless noun phrase that names what the
   reader is looking at, then a period, never "This figure shows." The opener
   is a bare label of the object; the expansion follows it. The claim, when
   present, is the closer, not the opener.
2. **Decode the reading keys.** Key every mark on the canvas exactly once,
   every color, panel, line, bar direction, axis, symbol, and bold cell, as a
   short "label: meaning" fragment. Expand every abbreviation on first caption
   use, and state the scale direction of any ordinal axis that could be misread
   ("lower is better", "brighter is higher").
3. **State the claim with its numbers glued.** On a flagship, land the takeaway
   as the closing sentence, carrying only the one or two headline numbers. Every
   number travels in a pair and is glued to its exact object; a lone number
   tells no story, and the full results row stays in the cells.
4. **Close on caveats.** Fold provenance in as a terse pointer, never a sentence
   of its own beyond the cross-reference. Carry the setup constants and local
   caveats that live nowhere else, the reproduce-me numbers, the as-is
   unfinished counts, what the bold cells mark.
5. **Self-containment beats deduplication.** A caption is read by a skimmer who
   may never touch the running text, so restate the body freely; the repeat is
   deliberate, not a mistake. Spend the caption's unique real estate on the
   decode and the setup constants that appear nowhere else.
6. **Flagship exhibits must carry the verdict.** Rank each exhibit before
   writing: the flagship (headline table or chart) states the verdict outright
   as its closer; the workhorse (per-item table, diagram) only describes and
   takes no verdict. Let caption length track this role, not the Figure/Table
   label, the method-carrying figure earns the fullest caption; a scoreboard
   earns a three-sentence label.
7. **Check claim direction against the data.** Before shipping, verify the
   takeaway's direction matches the scale you decoded, if "lower is better,"
   the winner must hold the lower number. Confirm each number is still glued to
   the object it measures and that no two distinct rates were rounded into one.
## Core rules

- Open with a verbless noun phrase naming the object; never "This figure shows."
  Order every caption name -> decode -> claim; the verdict is the closer.
- Rank the exhibit first: flagship captions claim (verdict last), workhorse
  captions only describe.
- Decode every mark exactly once, no color, line, bar, panel, symbol, or bold
  cell left undefined; expand every abbreviation on first caption use; state the
  scale direction of any ordinal axis that could be misread.
- Self-containment beats deduplication: a caption may restate a body conclusion,
  and the flagship captions should, a reader who sees only the exhibit must get
  the finding.
- Spend the caption's unique real estate on the reading key and the setup
  constants that appear nowhere else.
- Carry only the one or two headline numbers that make the point; leave the full
  results row in the cells. Numbers travel in pairs, each glued to its object.
- Present tense, active voice, a named agent; fragments for legends, full
  sentences for narrative; provenance folded in as a terse pointer.
- Never a hyperparameter, p-value, statistical test, equation-to-solve, or hedge
  in a caption; a formula may name a quantity, never invite a derivation.
- Never survey the literature or discuss future work; name a rival only as a
  compared system, never argue against it.
- Prose axioms: sentences <= ~28 words, subject and verb early, zero
  "can"/"could", no bare This/These, no em dashes; ration semicolons to a true
  antithesis.
## Figure-text exactness (the exhibit is one unit)

A figure, its caption, and the table it corresponds to are ONE exhibit; audit
them together, not in isolation.
- One vocabulary per exhibit: legend, bar, and colorbar labels use the caption's
  terms; when the caption says values correspond to a table, the labels match
  that table's row names word for word. Mismatches mean regenerating the figure,
  not wording around it.
- Legend entries parallel: every entry fills the same slots ("model during
  training, items scored" / "final model, items never scored"), never a time
  beside a thing.
- State the one shared comparison first; each mark type then carries only its
  differences, decoded with one shared verb phrase.
- Anchor each inference to the datum that proves it: the nearest-named example
  in a lesson sentence must not be the counterexample.
- Explain visible anomalies where the eye lands (a filled circle right of its
  open circle gets its plain-terms explanation inside the caption).
- Check figure claims against the run data, not memory; never silently change a
  printed number.
- Full method and worked rules: Part 8 of `caption-guide.md`; the sentence-level
  pass lives in the `sentence-audit` skill.
## Reference file

- `caption-guide.md`: full guide: term translations, the name -> decode -> land
  recipe, the fill-in template, the checklist, the five judgment calls where the
  dissected authors diverge, the semicolon addendum, the assembly order, worked
  examples (a figure, a table, and an algorithm caption) on a toy system, and
  the figure-text exactness rules (Part 8).
