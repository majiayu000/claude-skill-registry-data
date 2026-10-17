---
name: founder-os-pain-dream-fix-checker
description: FounderOS Pain-Dream-Fix checker. Tags each paragraph of an e-bomb, sales page or email as pain, dream or fix with Laya, flags premature pitching (the product showing up before the reader's pain), and gives paragraph-by-paragraph feedback. Triggers when a founder shares a draft and asks "does this follow Pain-Dream-Fix", "am I pitching too early", or "review my e-bomb".
plugin: behalfbot-founder-os
enabled_when: "chassis.config.yaml modules.founder-os.enabled == true"
type: auditor-skill
stage: 6
question_set: pain-dream-fix
---

# Pain-Dream-Fix checker

Pain-Dream-Fix is Amy Hoy's structure (30x500). Credit her and point the
founder to her writing on it. The reader should first recognise their own pain
in their own words, then see what life looks like without it, and only then
meet the fix.

## When to run

- On a draft the founder is about to publish or send: an e-bomb, a landing
  page, a sales email.
- Save it first as an artifact so labels have a row to hang on:
  `add_artifact(founder_id, stage=<current stage>, kind="ebomb"|"sales_page"|"email", body=<draft>)`.
  Paragraphs are separated by blank lines. A heading joins the paragraph under it.

## Laya pass

```bash
python3 "$FOUNDER_OS_DIR/scripts/audit.py" pain-dream-fix \
  --founder-id <founder_id> --artifact-id <artifact_id> --lang <en|pt|...> --record
```

The output has `paragraphs[]` (`n`, `text`, `section`, `section_probabilities`,
`pitches_product`, `label_ids`) and a `summary`:

- `sequence`: the section of each paragraph in order.
- `premature_pitch`: paragraphs that are a fix, or mention the product, before
  any pain paragraph.
- `findings`: any of `no_pain`, `no_dream`, `no_fix`, `premature_pitch`,
  `fix_before_dream`, `mostly_fix`.

No accuracy has been measured on this set yet. Check each paragraph's section
yourself before you rely on it.

## Claude pass

Give feedback by paragraph number:

1. **The structure in one line**, e.g. "fix, pain, dream, fix: the product
   arrives before the reader's problem does".
2. **Premature pitching.** Every paragraph in `premature_pitch`, and what to
   move or cut.
3. **The pain.** Is it in the reader's own words, the kind that turns up in a
   Sales Safari log, or the writer's summary of it? Offer a line from the
   founder's own `pains` log if one fits.
4. **The dream.** Is it concrete and about the reader's day, with no product in
   it? If `no_dream`, draft one sentence as a starting point for the founder
   to rewrite.
5. **The fix.** One clear next step, not a feature list.

Keep the founder's voice. Suggest edits; do not rewrite the whole draft.

## Without Laya

If `mode` is `claude-only`, paragraphs come back numbered with `section` null
and no summary. Tag each paragraph pain, dream or fix yourself, note which ones
mention the product, apply the same premature-pitch rule (any fix or product
mention before the first pain paragraph) and give the same feedback. Say in
one line that Laya was unavailable. Write no labels.

## Label capture

Ask the founder to confirm the sections you disagreed with, and record every
tag they accept or reject:

```bash
python3 "$FOUNDER_OS_DIR/scripts/labels.py" accept --founder-id <id> --by <founder_id> <label_id> ...
python3 "$FOUNDER_OS_DIR/scripts/labels.py" reject --founder-id <id> --by <founder_id> <label_id> --value '"dream"'
```

A rejected `section` needs the right answer as `--value`. A rejected
`pitches_product` flips. The cross-founder export is operator-only.

## Ledger writes

- The `artifacts` row for the draft, before the audit. A revised draft is a
  new version of the same kind, never an overwrite.
- Labels from `audit.py --record`; corrections from `labels.py`.
- One `audits` row with your verdict:
  `record_audit.py --table artifacts --id <artifact_id> --auditor claude --check pain_dream_fix --verdict pass|flag|fail --findings "<paragraph numbers and what to change>"`.
