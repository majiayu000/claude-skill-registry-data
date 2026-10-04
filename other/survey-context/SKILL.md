---
name: survey-context
description: >-
  Captures the context of a survey — purpose, subject, recruiting, who is missing, audience
  and expectations — in a short interview and stores it as a Markdown document next to the
  CSV (<name>.context.md). Every other survey skill reads it when present, so reports state
  the study design instead of guessing it. Use before the first analysis of a new data set,
  to update an existing context document, or to turn an existing briefing into one. Invoke
  with your CSV path or briefing text as the argument, e.g. /survey-context [CSV path].
license: MIT
---

# Survey Context

Goal: record **what the data cannot say about itself** — why the survey ran, whom it asked,
how people were recruited, who is therefore missing, and what decision is pending. The
result is one short Markdown document next to the CSV. All other skills in this toolkit
read it when it exists, so their reports describe the actual study instead of a plausible
generic one.

This is an **interview**, not a form. Keep it short and never guess an answer on the
user's behalf.

## Where the document lives

Next to the CSV it describes, named after it:

```
kundenumfrage.csv  →  kundenumfrage.context.md
```

The suffix is `.context.md` in every language — only the contents are written in the
user's language. If the folder holds exactly one CSV, a plain `survey-context.md` is
accepted too (that is the name to use when writing one by hand without a data file yet).

The file is ignored by `.gitignore` on purpose: it can be more sensitive than the CSV,
because it names pending decisions, strategy and internal metrics. Mention this once at
the end.

## Tool

```
python3 scripts/survey.py profile [--file CSV]
```

Run from the project root. If `scripts/survey.py` is not there, check
`.claude/scripts/survey.py` or locate `survey.py` in the project.

`profile` gives n, the column list with indices and types, and fill rates. Use it so the
interview never asks for anything the data already state.

## Workflow

1. **Find the CSV.** A path in the user's request wins; otherwise the CSV in the current
   folder. With several CSVs and no path given, ask which one — the document is bound to a
   specific data set.
2. **Check for an existing document.** If `<name>.context.md` already exists, read it,
   summarize in two lines what it already covers, and continue at the first section that
   is empty or marked as not stated. Never silently overwrite answers that are already
   there; ask before changing an existing section.
3. **Run `profile`.** Note n, the number of columns and the question wordings — they tell
   you a lot about the subject already.
4. **Was a briefing supplied?** If the user's request (or a file they point at) already
   contains project background, take everything you can from it, write the document, and
   then only ask about the sections that stayed empty. The interview fills the format; it
   is not the only way to produce it.
5. **Create the document immediately**, with the header and empty sections, before asking
   anything. Then ask the six questions **one at a time**, and **update the file after each
   answer**. An interview abandoned after question three must leave a usable document
   behind.
6. **Ask the six questions** (below). Say up front that it is six questions, roughly two
   minutes, and that anything can be skipped. Show progress ("Question 3 of 6"). If an
   answer is skipped, write `Not stated.` into that section — an explicit gap is
   information; silence is indistinguishable from "there is no limitation here".
7. **Finish**: give the path, note that the file is gitignored, and say in one sentence
   that the other skills will use it from now on.

## The six questions

Ask them in this order, in the user's own words, one message each. The parenthetical notes
are for you, not to be read out.

1. **Purpose.** Why did this survey run, and which decision depends on it?
2. **Subject.** What is the product or topic in a sentence or two — and which terms or
   abbreviations in the column names would an outsider not understand?
   *(You have the column wordings from `profile`; ask specifically about the ones that look
   like internal shorthand.)*
3. **Recruiting.** Whom did you want to survey, and how did participants get in?
   *(Then follow up once: **who is systematically missing as a result?** This is the single
   most valuable sentence in the document. If the user does not see a gap, offer what the
   recruiting route implies — an in-app banner cannot reach churned users, a customer
   newsletter cannot reach non-customers — and let them confirm or correct it.)*
4. **Fieldwork.** When did the survey run, and did anything happen shortly before or during
   it that shapes the answers — a release, a price change, an outage, press coverage?
5. **Audience.** Who reads the reports, and what should they do with them?
6. **Expectations.** What do you expect the data to show?
   *(Say plainly what happens with the answer: it goes into the document as a list of
   things to test, and a report that refutes an expectation is doing its job. Do not
   press if the user has none — an empty expectations section is fine.)*

## Document format

```markdown
# Survey context: <short title>

**Data set:** <file.csv>
**Sample:** n = <responses> · <number> columns
**Fieldwork:** <period, as stated by the user>
**Context recorded:** <date>

## Purpose and pending decision
Why the survey ran and what is to be decided from it.

## Subject and glossary
What the product/topic is. Terms, abbreviations and internal names that the column
wordings do not explain.

## Sample and recruiting
Target population and how participants were recruited.

## Who is missing
Which groups the recruiting route cannot reach, and what that means for the findings.
This section belongs in the limitations of every report.

## Circumstances during fieldwork
Events during or shortly before fieldwork that may have shaped the answers.

## Column notes
Which column is the lead question, which items belong together, which columns carry the
segments the business cares about. Free prose, no fixed notation.

## Audience and use
Who reads the reports and what they decide with them.

## Expectations (to be tested)

**These are prior expectations of the people who ran the survey. They are something to
test, never something to support.** Do not cite an expectation as evidence, do not let it
influence which analyses are run or how a finding is worded. Report an expectation only
where the data actually answer it, and then with an explicit verdict — including "the data
do not show this".

- <expectation 1>
- <expectation 2>
```

Every section stays in the document even when unanswered; write `Not stated.` underneath.

## Rules

- **Record, do not invent.** Everything in the document comes from the user or from
  `profile`. If an answer is vague, ask once for a concrete detail, then write down what
  was actually said — not a tidied-up version of it.
- **Keep facts and expectations apart.** Nothing from question 6 may end up in any other
  section. If an answer mixes them ("we surveyed our power users, and they are surely
  happier"), split it and say that you did.
- **Short beats complete.** Two to four sentences per section. This is a briefing note, not
  a study protocol.
- **No personal raw data** — no respondent names, ids or identifying quotes.
- **Do not answer analysis questions here.** If the user asks what the data show, point
  them at `survey-report` and finish the interview first.
- Document language = language the user speaks (default English).
