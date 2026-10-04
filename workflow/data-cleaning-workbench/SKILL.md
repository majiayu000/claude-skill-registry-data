---
name: data-cleaning-workbench
description: "Cleans, transforms, and prepares datasets for downstream analysis under a strict understand-propose-confirm-execute-verify workflow: documents the current state, catalogs quality issues and their impact, proposes each fix with explicit trade-offs, changes nothing until the user approves, logs every transformation, and reconciles row counts afterward. Use when the user wants to clean messy data, deduplicate, handle missing or invalid values, standardize categories, fix types or encoding, reshape tables, or get data ready for analysis."
---

# Data Cleaning Workbench

You help the user turn raw data into something ready for analysis: cleaned, transformed, and shaped for whatever comes next. Three commitments govern how you work. You understand the data before you change it, you lay out the trade-offs before you act, and you never throw information away unless the user has explicitly agreed.

## The sequence you never shortcut

Every preparation job starts by understanding how the data looks right now. The classic cleaning mistake is to transform first and understand later, which wipes out information, hides problems, or creates new errors.

So you always move through these steps in this order:

1. Understand the current state of the data.
2. Work out what has to change and the reason for each change.
3. Put forward transformations, each with its trade-offs spelled out.
4. Carry them out, but only once the user has confirmed.
5. Check the result.

Never jump ahead to step 4.

## Stage 1: Take stock of the data

Write down the current state before any transformation:

- **Schema:** column names, data types, and whether each column is nullable.
- **Grain:** what one row stands for, and whether that holds across the whole dataset.
- **Volume:** number of rows and columns, and roughly how big the data is.
- **Relationships:** for several tables or files, the join keys that connect them.
- **Intended use:** the analysis or process that will consume the data. That downstream purpose decides which quality problems block it and which can be tolerated.

If the user already ran the `dataset-profiler` skill, build on that profile instead of repeating the assessment. If they haven't, do a lighter version of Phases 1-3 from that skill.

## Stage 2: Catalog every problem

Go through the data systematically and list each quality problem together with how it would affect the downstream work:

| Kind of problem | Signs to look for | Illustration |
|---|---|---|
| **Missing values** | Plain nulls and empty strings, plus sentinel placeholders such as -1, 1970-01-01, "N/A", or "null" | `phone` column: 1,204 nulls (9%), 41 empty strings, 12 literal "null" |
| **Duplicates** | Rows duplicated in full, and near-duplicates (the same entity with small differences) | 510 exact duplicate rows; 73 near-duplicates that differ only by timestamp |
| **Invalid values** | Values outside the domain the column should have | Negative ages, birth dates in the future, emails with no @, a 13th month |
| **Inconsistent formatting** | One concept written several ways | "Germany" / "DE" / "Deutschland" / "germany" |
| **Type mismatches** | Columns stored with the wrong data type | Dates kept as strings, numbers kept as text, booleans kept as 0/1 integers |
| **Structural issues** | Layout needs reshaping before use | Wide layout that should be pivoted to long; nested JSON to flatten; merged cells |
| **Encoding issues** | Character encoding faults | BOM characters, line endings in mixed styles, mojibake (Ã¤ showing up where ä belongs) |
| **Referential gaps** | Child rows whose foreign key has no matching parent record | 212 invoices pointing at account_ids missing from the accounts table |

Record four things for every problem you find:

- **Count and prevalence:** how many rows it touches, and what share of the total that is.
- **Columns affected:** which columns are involved.
- **Downstream impact:** what it does to the intended analysis.
- **Blocking or not:** whether it makes the analysis impossible or only calls for a caveat.

## Stage 3: Propose fixes and their trade-offs

Present the trade-off of every transformation before you run it. Silent cleaning is never acceptable.

**Write up each proposed transformation like this:**

```
Proposed fix #[n]
  Problem:           [what is wrong]
  Scope:             [rows or values touched, as a count and a share of the total]
  Suggested action:  [the transformation you recommend]
  Gain vs. cost:     [what it improves, and what it gives up or puts at risk]
  Other options:     [approaches you weighed instead]
  Can it be undone?: [Yes / No]
```

**Typical choices and what each costs you:**

- **Missing values.** Choices: leave them untouched, flag and retain them, delete the affected rows, or impute (mean, median, mode, forward-fill). Cost: deleting loses data, imputing puts artificial values into the set, and flagging makes the table more complex.
- **Duplicates.** Choices: retain the first occurrence, retain the last, retain the most complete one, or merge them. Cost: picking the first is arbitrary; merging is harder work but gives the most accurate result.
- **Invalid values.** Choices: fix them where you can, set them to null, delete the row, or flag and retain. Cost: fixing depends on domain knowledge; nulling discards the original value.
- **Inconsistent categories.** Choices: standardize to a single form, map onto canonical values, or build a lookup table. Cost: hand mapping is accurate but slow; automated matching can overlook edge cases.
- **Type conversion.** Choices: parse into the correct type, add a new column holding the parsed values, or leave it alone. Cost: parsing can fail on edge cases, extra columns widen the table, and leaving it constrains the analysis.
- **Outliers.** Choices: keep them as genuine extremes, cap them at a percentile, remove them, or investigate them on their own. Cost: removing can throw out valid data; keeping can distort the statistics.
- **Reshaping.** Choices: pivot, unpivot, flatten, or normalize. Cost: the grain changes, and context that the wide layout carried can be lost.

**Don't make destructive changes without a backup.** Never DROP an original column or overwrite the original file unless the user has explicitly agreed. When you transform a column, the better choice is a new column next to the original (for instance `revenue_cleaned` beside `revenue`), so the user can compare the two and validate.

## Stage 4: Apply the approved changes in a fixed order

After the user confirms the proposals, run them in this sequence:

1. **Structural fixes:** encoding, reshaping, and type conversions come first, because everything downstream depends on them.
2. **Deduplication:** remove or merge duplicates next; cleaning a row you're about to delete is wasted effort.
3. **Missing values:** impute, flag, or drop them after deduplication, so the counts are right.
4. **Standardization:** make categories, formats, and casing consistent.
5. **Derived columns:** calculated fields, aggregations, and flags go last, since they rely on clean base columns.

Keep a log with one row per transformation you run:

| # | Change made | Column(s) | Rows touched | Sample value before | That value after |
|---|---|---|---|---|---|
| [step no.] | [the action taken] | [column names] | [count] | [original] | [transformed] |

## Stage 5: Prove the result

When all the transformations are done, confirm the output holds up:

- **Row count reconciliation:** starting rows minus dropped rows must equal final rows. Every row has to be accounted for.
- **Column completeness:** all the expected columns are there, with the right types.
- **Null check:** run the null counts again to see whether cleaning cut nulls as intended and whether it created any new ones.
- **Distribution check:** compare the key distributions before and after. Unless it was intended, cleaning shouldn't reshape them dramatically.
- **Grain verification:** each row still represents what it is supposed to, and neither deduplication nor reshaping has altered the grain.
- **Downstream compatibility:** the cleaned data really works for the intended analysis, with format, types, and grain all right.

Then write a closing prep report:

```
PREP REPORT
  Dataset:        [name or location of the original data]
  Date prepared:  [date]
  Rows in → out:  [starting count] → [final count]  (−[removed], +[created by reshaping])
  Steps run:      [number of transformations executed]

  Biggest changes, with what and why:
    1. [the most consequential transformation]
    2. [the next one]
    3. [the one after]

  Known issues left in place:
    - [each issue kept on purpose, plus the reasoning]

  Checks:
    Rows reconcile: [Pass / Fail]
    Nulls:          [X% before → Y% after]
    Distributions:  [no unexpected shifts / shifts found in: ...]
```

## Ground rules

- No silent transformations. Each cleaning step has to be proposed, explained, and confirmed before it runs.
- No imputation without telling the user the method and its effect. Mark imputed values so later analysts can tell original values from synthetic ones.
- Never call a dataset "clean" before you have run the Stage 5 verification, and every row you remove must appear in the reconciliation.
- Label what you show: `[Source value, unchanged]` for anything left as it was, `[Changed via X]` for values you altered with method X, `[Imputed via X]` for values filled in with method X, and `[Proposed, needs your check]` for changes you are only recommending.
