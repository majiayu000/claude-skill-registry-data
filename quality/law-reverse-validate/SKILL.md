---
name: law-reverse-validate
description: >
  Performs a hallucination check on machine_readable sections by verifying every
  element traces back to the original legal text. Use this skill proactively when:
  machine_readable sections have been generated or modified, after /law-generate
  completes, when reviewing corpus YAML files for legal accuracy, or when user
  mentions "validate", "verify", or "hallucination check" for law YAML files.
  Activate automatically after editing machine_readable sections in corpus
  regulation YAML files.
allowed-tools: Read, Edit, Bash, Grep, Glob
user-invocable: true
---

# Law Reverse Validate, the hallucination check

Verifies that every element in a `machine_readable` section traces back to the
legal text of its own entry. This catches invented logic, phantom
conditions and bindings to outputs that do not exist.

The text is the standard. A model that reaches the evidently intended outcome by
a route the words do not describe is a finding, and one that survives review
longest, because the answer looks right.

## Scope, both directions

Each `machine_readable` interprets ONLY the text of its own entry. Two opposite
failures follow, and the second one gets missed more often.

**Leaked in.** A condition, threshold or value from another provision,
reimplemented here instead of referenced. Flag it: the correct mechanism is an
`input` with `source.regulation` or `source.output`, an `open_term` for a value
the law leaves open, or `hooks`/`overrides` for reactive interaction. Also flag a
`legal_character` that does not match what the entry does, such as `BESCHIKKING`
on a norm article that only sets an amount.

**Left unconnected.** An output that restricts an entitlement and that nothing in
this file reads. A restriction nothing reads does not restrict.
A scope violation makes a model too strict in the wrong place, a dangling
restriction makes it too generous everywhere, so the two rank equally.

Check it by listing every boolean output whose name starts with `geen_`, `niet_`,
`is_uitgesloten`, `voldoet_aan`, or that a `markings.target` entry names, and
finding its reader. An `overrides` block counts as a reader only when its
`article` field is the `number` of the producing entry exactly as this file
writes it. In round 3 four of five overrides pointed at `"2"`, `"3"` and `"7"`
while the producers are stored as `2.1`, `3.1` and `7.3`, so nothing fired and
the halving in article 2, fourth lid never happened.

## Procedure

1. Read the target law YAML.
2. For every entry with a `machine_readable`, read the `text` field first: that
   text is the scope. Then check every element against it:
   - each `input`, `parameter` and `definition`: is it in this text?
   - each `action` and operation: does this text describe this logic?
   - each comparison value: does this text state this threshold or amount?
   - each `source`: does this text refer to that law or that article, and does
     the binding resolve (see below)?
   - each `open_terms` entry: does this text leave the content open?
   - each `markings` entry: see the marking checks below.
   - each `overrides` entry: does this text say "in afwijking van", "onverminderd",
     "blijft buiten toepassing" or "met dien verstande"? A second sentence that
     adds a ground is not a derogation.
   - each `hooks` entry: does this text describe a rule triggered by a lifecycle
     event ("na bekendmaking", "bij bezwaar")?
   - each `declares` entry: does this text fix that document property?
   - each `endpoint`: is there a reason for external callability?

3. Classify:

| Traceable in THIS entry's text? | Needed for logic? | Action |
|---------------------------------|-------------------|--------|
| YES | YES | Keep |
| YES | NO | Keep (informational) |
| NO, but in another provision | YES | **Scope violation**: refactor to a `source` reference |
| NO | YES | Report as assumption |
| NO | NO | **Remove** |
| Produced here, restricting, read by nothing | (any) | **Dangling restriction**: bind it from the entry whose outcome it restricts |

4. Remove what has to go, collect the assumptions for the report.
5. Re-run `just validate <file>` after any removal. Removing an element can break
   a required field or leave a dangling `$variable`. Fix that before reporting.

## Cross-law binding check

A `source:` binding is a factual claim: the target regulation produces this
output. A binding to an output that does not exist is a hallucination of the same
kind as a fabricated article reference, and it hides better, because the YAML is
schema-valid and the name looks plausible.

For every `source: { regulation, output }`:

1. Does the target law YAML exist in `corpus/regulation/nl/...`?
2. Does the named output really occur there, as an `- output:` in some entry?

A dangling binding is a modelling error, never an engine limitation. Fix the
output name, or add the output to the target law on the entry that should own it.
Never downgrade the binding to a plain parameter to make the error disappear:
that hides the gap instead of closing it.

**A binding to a law that has not been harvested yet is not a finding.** The
binding is correct and it says where the answer has to come from. Whether the
regulation is in the corpus is a state of the corpus, tracked by the resolve step
(RFC-029), and it does not belong in the law file. Report it as harvest work, not
as a defect in the model.

## Marking checks

Markings say the format cannot express a construct. Five things go wrong.

**A marking standing in for an open term.** "Zo spoedig mogelijk", "onverwijld",
"redelijkerwijs", "in bijzondere gevallen": the language expresses these fine and
the content is filled by an implementing regulation or by the competent authority
in the individual case. They are `open_terms`. A marking here sends the file to
whoever extends the engine, where nobody can act on it.

**A marking standing in for a binding.** A value another law produces is an
`input` with a `source`. In round 4, 43 of 101 gaps were cross-law references
written up as gaps.

**A marking standing in for a model.** Check what the entry contains besides the
marking. An entry that stays empty behind a marking is a defect: the marking then
measures the gap far larger than it is and every rule that was derivable is lost.
Ask which single word could not be filled in and what remains when that word is
left as an open value. If the answer is "quite a lot remains", the entry is
unfinished.

**A `target` that is not true.** Every name in `markings.target` must be absent
from that entry's actions; a value the entry computes anyway contradicts its own
marking. And a marking whose `target` is empty asserts that the entry stays
executable, so check that it does. Both halves fail today: `blocks`, the
predecessor field, is empty in 39 of 39 markings, and of the 72 values marked as
blocked not one is left out.

**A reason that diagnoses nothing.** `reason` says why the construct does not
fit, in terms of what the format does have: it names the shape or the operation
that comes closest and says where it falls short. "Het model kent alleen
toepasselijkheid van een hele wet" is a diagnosis; "dit past niet in het model"
is the claim of the marking written out again. So is a reason that restates
`about`, and so is one that repeats `resolved_by`. The order runs one way: the
change follows from the reading, and from the change alone the reading cannot be
recovered. Without a diagnosis a gap somebody worked through reads like a gap
nobody opened, which is exactly what this validation has to tell apart.

Also verify `legal_text_excerpt` occurs in this entry's own `text`, and that
`resolution` is `operation` (the operation does not exist) or `model` (the format
has no shape for the construct at all).

## Workaround detection

Signs that a construct was approximated instead of marked:

- an `IF` with more than eight cases, which is usually an inlined table lookup
- arithmetic that approximates rounding, such as a `MULTIPLY` followed by a
  `DIVIDE` by a power of ten. The engine has `ROUND`, `CEIL` and `FLOOR`, so
  where the law says "afgerond" the model uses one of those, and where the law
  says nothing the model does not round
- hardcoded values that this text does not mention, which may be pre-computed
  results of a calculation the translator could not express
- a boolean where the text says "voor zover", which loses the partial case,
  always to the citizen's disadvantage
- a derived constant: `days: 28` for "vier weken", `0.9` for "ten minste tien
  percent lager", a division by 12 for "naar tijdsgelang herrekend"

Extract the construct to a `markings` entry, keep everything that does fit,
re-run `just validate`, and report it.

## Operation correctness

Verify none of these appear: `when`/`then`/`else` on `IF` (must be
`cases`/`default`), `SUBTRACT_DATE` (must be `AGE` or `DATE_DIFF`), `CONCAT`
(must be `ADD`), `NOT_EQUALS`, `IS_NULL`, `NOT_NULL`, `NOT_IN` (must be `NOT`
around the positive operation), `SWITCH`. `FOREACH` was removed at v0.5.0 and
restored at v0.5.7 (RFC-016); do not flag it, and do not flag `type: array` inputs.

## Report

```
Reverse Validation for {LAW_NAME}

  Entries checked: {COUNT}

  Fully grounded: {N}
  Contains assumptions: {N}
  Elements removed: {N}

  Scope violations:
  - {entry}: {condition pulled in from where}

  Dangling restrictions:
  - {entry}: {output} restricts nothing, should be read by {entry}

  Dangling bindings:
  - {entry}: {regulation}.{output} is produced nowhere in the target law

  Marking findings:
  - {entry}: {about}, should be an open term / a binding / modelled
  - {entry}: target names {value}, which the entry computes anyway

  Assumptions requiring review:
  - {entry}: {assumed element}

  Harvest work (not defects):
  - {regulation} is bound but not in the corpus
```
