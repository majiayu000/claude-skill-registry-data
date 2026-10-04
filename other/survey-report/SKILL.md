---
name: survey-report
description: >-
  Answers a question about quantitative survey data from a CSV and writes a short,
  evidence-backed report as Markdown to reports/. Works with any survey CSV (column types
  are auto-detected). Invoke with your request as the argument, e.g. /survey-report <your
  question>. Use when the user wants an analysis, numbers, a count, a cross-tab, or a
  claim checked on survey data.
license: MIT
---

# Survey Report

Goal: Answer the **question** the user asked from a survey CSV with facts, and save a
**short report as Markdown** to `reports/`.

The user's question is the request they made when invoking this skill. If it contains a file path/name,
use that CSV; otherwise use the CSV in the current folder.

## Tool

All numbers come from the shared engine — **never estimate or count "in your head".**
Standard library only, no pandas required.

```
python3 scripts/survey.py <cmd> [...] [--file CSV]
```

Run these from the project root. If `scripts/survey.py` is not there, check `.claude/scripts/survey.py` or locate `survey.py` in the project.

- `profile` — overview: n, every column with **index**, detected type (META / SINGLE /
  MULTI / FREETEXT), fill rate. **Always run first.**
- `freq COL [--by COL2] [--filter "COL=VALUE"] [--top N]` — frequency distribution;
  `--by` = cross-tab; `--filter` repeatable (subset). For MULTI columns the percentages
  sum to > 100% (correct — explain it in the report).
- `text COL [--filter ...] [--sample N]` — free-text answers for qualitative themes.

`COL` = column index (from `profile`) **or** an unambiguous part of the column name.
Every command accepts `--json` for machine-readable output.

## Survey context

If a context document sits next to the CSV (`<name>.context.md`, or `survey-context.md`
when the folder holds exactly one CSV), read it before writing. It carries the subject, the
glossary, the audience and the study design. Use it for framing and terminology — the
figures still come only from the engine. Whatever in it limits the findings, above all the
**"Who is missing"** section, belongs in this report's interpretation and method. Any
expectations listed there are **something to test, never something to support**: never cite
one as evidence and never let one shape how a finding is worded. If no such document
exists, analyze as before and mention `survey-context` once at the end of your reply.

## Workflow

1. **Profile.** Run `profile` to learn n, column indices and types.
2. **Translate the question into analyses.** Pick the right column(s) and run the fitting
   commands:
   - "how many / what share / distribution" → `freq` on the target column.
   - "does X differ by Y / relationship / comparison" → `freq X --by Y`.
   - "… for group Z" → `--filter "Z-column=value"`.
   - "why / what do they value / typical workflow / wishes" → `text` on a free-text column;
     with many answers use `--sample 40–60`, cluster themes, back them with ~2–3 short
     verbatim quotes.
   Usually 2–4 analysis commands **in addition to** `profile` — a bare distribution is
   rarely the whole answer. For open questions combine angles (distribution + relevant
   cross-tab + free-text themes).
3. **Write the report** (see format); numbers exactly as the engine returned them.
4. **Save** to `reports/`. Create the folder if needed. File name:
   `YYYY-MM-DD_short-title.md` (date via `date +%F`, title kebab-case from the question).
   If a file already exists, append `-2` etc.; never overwrite.
5. Tell the user the **key takeaway** briefly in your reply and give the report path.

## Report format (keep it short)

```markdown
# <question as a concise heading>

**Data basis:** <file> · n = <responses> · report of <date>

## Key takeaway
1–3 sentences answering the question directly.

## Results
- Supported points with **numbers (absolute + %)**. Tables for distributions/cross-tabs.
- For multi-select, note: multiple answers possible, sum > 100%.

## Interpretation
What does it mean? Notable patterns, relationships, caveats (e.g. low fill rate of a
column, small subset after filtering, limits of the study design from the survey context).

## Method
Columns and filters used, in one sentence, so it's reproducible. If a context document was
used, name the recruiting route and who it cannot reach.
```

## Rules
- **Accuracy over volume.** Only claim what the outputs support. Percentages relate to
  the *respondents who answered* the column (the engine states this).
- Compute aggregates ("positive overall", top-2-box) from the **absolute counts**, never
  by adding the engine's rounded percentages: 73 of 140 is 52.1%, not 13.6% + 38.6%.
- Statistics in plain text (`Chi² = 12.094`, `p = 0.438`, `Cramér's V = 0.17`), no LaTeX.
  Pass on the engine's reliability warnings rather than dropping them.
- Flag small filtered subsets (n < ~30) as weakly reliable.
- Report language = language of the question (default English).
- No personal raw data (e.g. individual ids/timestamps).
- Keep it a **short** report, not a full study.
