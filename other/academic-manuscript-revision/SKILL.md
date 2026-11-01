---
name: academic-manuscript-revision
description: Revise an academic manuscript in response to peer review and write the point-by-point response letter. Use when the user has received reviewer comments, referee reports, or an editor's decision letter and wants to revise a paper, plan a revision, answer reviewers, write a rebuttal or response-to-reviewers letter, produce a marked-up copy, or work through revision items one by one. Covers consolidating comments into ordered work items, maintaining a revision plan, triaging requested experiments, editing .docx files safely, keeping numbered citations in first-appearance order, and building the response letter as the work lands.
---

# Manuscript revision

A revision round has two deliverables that must stay in step: the revised manuscript and
the response letter. The letter quotes the manuscript, so it can only be finished as the
manuscript is finished, and it goes stale whenever the manuscript changes.

## Standing rules

These hold throughout and override any local convenience.

1. **Propose before editing.** Show before and after text and wait for approval before
   touching a .docx. Every time, however small the change.
2. **Use the academic-writing skill for all new prose**, in the manuscript and in the
   letter. Invoke it rather than writing from general instinct.
3. **Never overwrite the author's hand edits.** They edit responses in Word. Mirror those
   edits back with `sync_letter.py --write`.
4. **Update the plan as each item lands**, not at the end, with `plan_status.py`.
5. **Verify numbers against their source**, not against another part of the manuscript.
6. **One item at a time.** Finish, record, then start the next.
7. **Every change lands in every parallel copy** — manuscript, supplementary, and the
   anonymised copy of each — in the same session.
8. **Answer reviewers directly.** Each response leads with the answer to the concern
   behind the comment, keeps only the details that carry it, and uses short paragraphs,
   never lists or tables. See `references/response-letter.md`.

## Setup, once per revision round

```bash
S=<this skill>/scripts
python $S/revision_config.py --init <revision folder>   # then edit revision.json paths
python $S/revision_config.py                            # confirm every path resolves
```

`revision.json` holds the paths, the citation style and the letter's font and colour.
Every script reads it, so nothing is hard-coded to a project.

List **every** .docx the round edits under `documents`, each with the working copy and the
submitted file it will be compared against. A round often carries more than two: a
manuscript, a supplementary file, and an anonymised copy of each. Every change goes into
all of them in the same session; deferring the parallel copy to later is how they diverge.

Set `citation_style` to `numeric` or `author-date`. It decides whether the reference
ordering check applies at all.

Copy `assets/REVISION_PRINCIPLES.md` into the revision folder and edit it for the project.
Ask the author to confirm it, since it records their standing preferences.

**Flatten citation fields before any editing**, once:

```bash
python $S/flatten_endnote.py --working --write
```

Reference-manager citations are Word fields. Editing prose around them breaks them, no
reference can be added without returning to the manager, and edits can land inside field
code where they are invisible.

## The workflow

### 1. Read the reviews and build the plan

**If this is not the first round, read the previous round's plan and letter first.** What a
reviewer objects to now is often the shape of the previous answer: evidence added where
depth was wanted, material moved to the supplementary to protect the length, a claim
softened into vagueness. Ask explicitly whether the new reviews are a verdict on the
previous round's *strategy*, and say so in the plan's overview if they are, because it
changes what this round is for. Note also which reviewers are new and which recommendations
have shifted; a reviewer who accepted last time may not read the paper again.

Read every comment and give each a stable id, `R2.4` for reviewer 2's fourth comment. Ids
are used everywhere afterwards and are never renumbered.

Write the plan from `assets/REVISION_PLAN_TEMPLATE.md`. Consolidate comments into items
ordered easy to hard: local fixes, claims calibration, new evidence, framing, close-out.
Framing comes last because it describes evidence that does not exist yet.

Read `references/revision-plan.md` for the plan's structure, the consolidation rules and
what belongs in a record.

Before scheduling anything, **verify each comment against the current text**. Some are
already answered, some rest on a misreading worth answering differently, and a reviewer
arriving late may be asking for work already done.

Surface anything only the author can decide as an open decision, with the options and the
cost of each. Resolve it before starting the item that depends on it.

Where reviewers ask for new runs, analyses or artifacts, triage them in the plan before
scheduling any: run it, rebut it, or answer it from data already on disk. Read
`references/new-evidence.md` — it carries the triage table, the provenance rules for
reported numbers, and how to handle runs that are executed and then withdrawn.

### 2. Scaffold the letter

```bash
python $S/scaffold_letter.py comments.md --write
```

Write `comments.md` with a `# Editor` or `# Reviewer N` heading per section, the reviewer's
overall assessment as plain paragraphs, and `## R1.1` per comment. This produces the letter
with every comment verbatim and a placeholder for every response, plus an `answers.py`
stub. Read `references/response-letter.md` for structure and formatting.

### 3. Work the items

For each item, in plan order:

1. Read what the manuscript currently says. Quote it back to the author.
2. Draft the replacement with the **academic-writing skill**. Propose before and after.
3. On approval, apply it with the `docx_util` helpers. Read `references/docx-editing.md`
   first; every trap in it has cost real time.
4. Write the response into `answers.py`, then `python $S/fill_responses.py --write`.
5. Record the item: `python $S/plan_status.py --done C7 --record-file note.md --write`.
6. Re-run the checks below.

When a comment asks for clearer contribution or significance, the fix is usually structural:

- **Related Work** organized around what prior work did, what it did not, and the gaps
  the contributions answer. Do not put sentences about the authors' own system inside it,
  and do not compare against systems nobody asked about.
- **Discussion** that separates scientific meaning (what the approach enables, where errors
  arise, who uses it) from engineering explanation, under descriptive headings.
- **Conclusions** that state findings as answers without restating the numbers already in
  the abstract and Results. Confirm this with the author, since some prefer the numbers.

Apply every change to **all** the documents in `revision.json` in the same session, not
just the one being read. Never revise the manuscript and leave its anonymised copy for
later.

For an item that produces new evidence, the artifact comes first and the prose cites it.
Follow `references/new-evidence.md`: verify the number against the run that produced it,
commit any code change separately from the manuscript edits, and record in the plan
whether that change affects a reported number.

When the author says they edited the letter, run `sync_letter.py --write` before anything
else, so their wording is what gets built on.

### 4. Checks, after every item

```bash
python $S/manage_references.py --check     # numeric styles only; see below
python $S/verify_letter.py                 # every quoted passage exists
python $S/sync_letter.py                   # letter and answers agree
```

If a reference was added or removed under a numeric style:

```bash
python $S/manage_references.py --renumber --write
```

Renumbering changes markers the letter may quote, so run `verify_letter.py` afterwards.

**Under an author-date style the reference scripts do not apply.** There is no
first-appearance order to keep and nothing to renumber: the list is alphabetical and
in-text citations carry names. Set `"citation_style": "author-date"` and drop
`manage_references.py` from the per-item checks. What replaces it is a check the scripts
cannot do: that every citation still resolves and that nothing was left as a placeholder.

### 5. Re-audit when figures, tables or numbering change

A change late in the round can falsify a response written early. After any change to a
figure, a table or a number, re-read the responses that mention it. `verify_letter.py`
catches stale quotes; it cannot catch a claim that is now untrue.

Inserting or deleting a numbered object shifts everything after it. Treat the shift as its
own pass and sweep all four places:

1. **Captions** in the document the object lives in.
2. **Every cross-reference** in the body, including the supplementary and any that fall
   inside a passage the letter quotes.
3. **External artifacts** that name the number: a reproduction guide, a data deposit
   README, a repository README. List these in the plan at the start of the round.
4. **The letter.** Say the old number once per reviewer thread, at the first mention,
   as "(previously Table 5)". The reviewer is reading against the version they reviewed,
   and reviewer comments keep their original numbering.

An object left uncited by the shift is a finding, not a tidy-up: decide whether it is
removed or whether a citation to it went missing.

### 6. Close out

1. Language, numbering and markup pass: equation, table and figure numbering against their
   cross-references; abbreviations at first use; leftover markers; consistent ranges and
   spacing. Include a concision pass for wordy "of" chains and participial tails, then
   re-sync every letter quote.
2. **Sweep the supplementary as its own document.** After restructuring the main text,
   check its references to main-text sections, its claims against the data, and its
   formatting: headings with leftover direct formatting, empty paragraphs, merged short
   paragraphs. Check that each main-text pointer describes what the supplementary actually
   contains ("Table S1 characterizes the single-turn queries", not "each suite").
3. **Audit the manuscript after the author's own pass.** The author reads the whole
   document at the end and edits it in Word, for concision, language, or length. That pass
   is not tracked and it deletes things. Walk the plan item by item and confirm each item's
   recorded text is still in the manuscript. In a live round this is what caught a sentence
   a reviewer had specifically asked for having been cut, along with two dropped clauses
   and two cross-references left pointing at the old numbering. Then re-sync the letter:
   `verify_letter.py` will report every quote the pass reworded. Run the audit after **any**
   author pass, not only the last one, and record what it recovered.
4. Write the editor page and the per-reviewer summaries, last, against the finished
   manuscript. Each summary says what the revision does for *that reviewer's* comments.
5. Produce the comparison baselines and hand over:

```bash
python $S/flatten_endnote.py --baseline --write
```

Then the author runs Word's Compare, original `*_plaincite.docx` against the working copy.
Compare cannot be scripted; it is the author's step.

## Scripts

| Script | Does |
|---|---|
| `revision_config.py` | finds and validates `revision.json`; `--init` writes a template |
| `docx_util.py` | run-safe reading and editing helpers; import, do not run |
| `letter_io.py` | reads letter blocks, rewrites `answers.py`; import, do not run |
| `flatten_endnote.py` | `--working` flattens citation fields; `--baseline` makes comparison copies |
| `scaffold_letter.py` | builds the letter and `answers.py` from `comments.md` |
| `fill_responses.py` | writes answers into placeholders only |
| `sync_letter.py` | mirrors hand edits from the letter back into `answers.py` |
| `verify_letter.py` | every quoted passage must exist in the manuscript |
| `manage_references.py` | `--check` and `--renumber` for first-appearance ordering |
| `plan_status.py` | marks an item applied and files its record |

Every script prints what it would do and needs `--write` to act. Each backs up to `.bak`
before writing.

## What to hand back to the author

- Anything that needs their judgment, as a question with options and costs, not a guess.
- Any error found in their own work, plainly, with how it was verified.
- The steps only they can do: typing equations in Word, running Compare, placing figures,
  and confirming any value that could not be read from a source they hold.
