---
name: ada-tracker
description: "Builds an accessibility compliance checklist for a project in two passes: scoping, meaning how many of each element must be accessible, and technical, meaning what each accessible element must measure. Trigger on \"accessibility checklist\", \"ADA check\", \"accessibility compliance\", \"accessible parking count\", \"accessible toilet count\", \"barrier free check\", \"ada-tracker\", or a pasted program with counts of parking, units, or toilet rooms. Works with any accessibility standard. The user names the standard and supplies both the scoping rule and each technical dimension, by typing them, pasting the clause, or naming a file to read. The skill never supplies an accessibility value from memory or from web search, and every row it could not source is reported as unverified rather than filled in. Writes a CSV checklist and appends to a project index."
license: MIT
metadata:
  title: "Accessibility Tracker"
  summary: "Build an accessibility compliance checklist for a project"
  discipline: "code-life-safety"
  tags: "Compliance"
---

# Accessibility Tracker

Accessibility compliance is two questions asked in order. How many of these must
be accessible, and what must each accessible one measure. This builds the
checklist for both. The questions are the same everywhere. The answers are not,
so the answers come from you.

## Scope and limits — read first

**What this does.** Takes your program, works through the scoping question for
each element type, then the technical question for each accessible element, and
writes a CSV where every row carries the clause you cited. Rows you could not
supply a value for come out as `unverified` and are counted, so a partial
checklist never reads as a complete one.

**What this does not do.**

- **It does not know any accessibility requirement.** No scoping tables, no
  dimensions, no ratios, no counts. Every value comes from you. That is the
  design, not a gap.
- **It does not calculate a required count from a rule it knows.** You give the
  rule, in your standard's words; it applies that rule to your numbers and shows
  the arithmetic.
- It does not read your drawings. Element counts come from you.
- It is not a one-time review. `code-compliance-review` checks accessibility as one axis of
  a dated review document; this builds the checklist you carry through the
  project and update as elements land.
- It does not check an existing building against what is readily achievable, and
  it does not do a barrier removal survey.
- It does not layer a local amendment over a base standard on its own. If two
  documents apply, you say which governs each row.
- It does not replace the Architect of Record and does not anticipate the
  authority.

**What you need before starting.** The governing accessibility standard and its
edition, your program counts, and the clause text for whichever rows you want
checked.

## Workflow

### Step 1. Bootstrap if needed

Check whether `docs/ada/index.md` exists. If not:

```bash
python scripts/init_workspace.py
```

If the project has no `docs/` folder at all, confirm before creating one.

### Step 2. Establish the standard

Ask, in one message:

> 1. Which accessibility standard governs, and which edition?
> 2. Is a second document layered on top, from a state, province, or city? If
>    so, which one governs where they differ?
> 3. Which element types are in scope: parking, entrances, routes, doors, ramps,
>    toilet rooms, dwelling or sleeping units, seating, signage, others?
> 4. How will you supply values? Type them, paste the clause, or name a file.

Record the standard and edition. They print on every row of the checklist,
because a dimension without its standard is not a citation.

### Step 3. Collect the program

For each element type in scope, ask for the totals the scoping question needs.
Typically the total count provided, and the facility characteristic the standard
keys the rule to.

Never guess a count and never infer one from the project type.

### Step 4. Scope, one element type at a time

For each element type:

1. Ask for the scoping rule, in your standard's words. Accept a typed rule with
   its clause, a pasted table to read it out of, or a file to read.
2. Apply it to the total, and **show the arithmetic**:

   ```
   Total provided        <n>
   Rule, as supplied     <written out>   [cited as ...]
   Required accessible   <arithmetic>    = <n>
   ```

3. If no rule arrives, the row is `unverified` and no count is produced.

Do not round on your own initiative. Ask whether the rule rounds up, down, or to
the nearest, and cite the answer.

### Step 5. Build the technical checklist

For each accessible element, ask for the dimensional requirements that apply.
Same three routes, same rule: nothing arrives, the row is `unverified`.

Write a row per requirement:

| Item | Required | Cited section | Source | Status | Remarks |
|------|----------|---------------|--------|--------|---------|

- **Required**: the value as supplied, in the units supplied. Quote the clause
  wording where it was pasted rather than paraphrasing it.
- **Source**: where it came from, as a file and line, a pasted clause, or the
  user directly.
- **Status**: `cited`, `computed` (a scoping count, with the arithmetic above),
  or `unverified`.

### Step 6. Write the checklist file

Read `assets/ada-checklist-template.csv` and fill it. Filename:

`docs/ada/<project-slug>-accessibility-checklist.csv`

Slug rule: lowercase, `[^a-z0-9-]` removed, max 40 characters. Write a markdown
preview alongside it with the first fifty rows.

The head of the file carries the standard and edition. The foot carries the
unverified count.

### Step 7. Update the index

```bash
python scripts/append_to_index.py \
  --project <slug> \
  --jurisdiction "<as supplied>" \
  --standard "<standard and edition, as supplied>" \
  --row-count <n> \
  --csv <filename>.csv \
  --preview <filename>.md
```

Always pass `--standard` explicitly. The script has a default, and a checklist
that inherits a default standard is a checklist nobody can trace.

### Step 8. Report

Counts: rows cited, rows computed, rows unverified. The unverified list with
what each one needs. Then:

> Every requirement in this checklist came from you. I applied your rules to
> your numbers and supplied no accessibility values. Unverified rows were not
> checked at all.

## Rules

- **Never supply an accessibility value.** Not a count, not a ratio, not a
  dimension, not a clearance. There are none in this file and none bundled with
  it.
- **Show the arithmetic on every scoping count**, so a wrong rule is visible
  rather than buried in a number.
- **Ask how the rule rounds** rather than choosing.
- **Quote clause wording where it was pasted.** A paraphrased accessibility
  requirement loses the exception that mattered.
- **Print the unverified count on the file**, every time.
- Where two documents apply, the user says which governs each row; never merge
  them.

## Anti-patterns

- Filling a clearance, a width, or a required count from recall because the
  figure is a familiar one. These are the most familiar numbers in the whole
  catalog and therefore the most dangerous to recall.
- Searching the web for a scoping table and applying what comes back.
- Producing a required count without showing the rule and the arithmetic.
- Dropping unverified rows so the checklist reads clean.
- Merging a base standard and a local amendment without being told which governs.
- Bundling a scoping table or a dimensions file into this skill later. It had
  those once; they were removed on purpose, along with the script that computed
  counts from them.

## Resources

- `assets/ada-checklist-template.csv` — the checklist columns.
- `assets/ada-index-template.md` — the project index structure.
- `scripts/init_workspace.py` — creates `docs/ada/` and an empty index.
- `scripts/append_to_index.py` — appends a row to the index.

No reference files. The requirements come from your standard, not from here.
