---
name: verbatim-themes
description: >-
  Systematically codes open-ended free-text answers from a survey CSV: theme clusters with
  frequency, pain points vs. praise, representative quotes. Analyzes ALL answers (not just
  a sample). Result as Markdown to reports/. Use for qualitative analysis of open
  questions / verbatims. Invoke with your request as the argument, e.g. /verbatim-themes
  <column/question> [+ focus].
license: MIT
---

# Verbatim Theme Analysis

Goal: **Systematically code** the open-ended answers of the question/column named in the
user's request — build themes, count their frequency, back them with quotes. This
is about qualitative depth over the **full** dataset. Result to `reports/`.

## Tool

```
python3 scripts/survey.py <cmd> [...] [--file CSV]
```

Run these from the project root. If `scripts/survey.py` is not there, check `.claude/scripts/survey.py` or locate `survey.py` in the project.
- `profile` — column overview; identifies FREETEXT columns (always first).
- `text COL [--filter "COL=VALUE"]` — print **all** answers of the column (no `--sample`,
  so nothing is missed). `--json` for clean downstream handling.
- `text COL --filter ...` — free text of a subgroup (e.g. daily users only).

`COL` = index (from `profile`) or an unambiguous name part.

## Survey context

If a context document sits next to the CSV (`<name>.context.md`, or `survey-context.md`
when the folder holds exactly one CSV), read it before coding. The **glossary** is the
practical gain here: respondents write in internal shorthand, feature names and
abbreviations, and without the glossary you will either misread them or split one theme
across several. The **fieldwork circumstances** explain spikes — a release or an outage
during the field period shows up as a theme and should be labeled as such, not read as a
standing complaint.

Code **bottom-up regardless**: themes come from the answers, never from the context
document's vocabulary or from what someone expected to hear. Expectations listed there are
**something to test, never something to support** — never inflate a theme because it was
anticipated, and never drop one because it was not. Carry the recruiting limits (**"Who is
missing"**) into the method section. If no such document exists, proceed as before and
mention `survey-context` once at the end.

## Approach

1. **Profile**, pick the target free-text column. Note the fill rate (how many answered? the
   non-answerers are part of the truth).
2. **Load all answers** with `text COL` (no `--sample`). With very many answers, read in
   several passes/chunks so none is lost.
3. **Code (bottom-up).** Build recurring themes/codes, merge synonyms. An answer can map to
   several themes. **Count mentions per theme** (approximate frequency, clearly flagged as
   an estimate).
4. **Structure.** Order themes by frequency; where useful split into pain points
   (problems/wishes) vs. praise/valued aspects vs. neutral/behavior.
5. **Back it up.** Per theme, 1–2 **verbatim** short quotes (unaltered, trimmed with […] if
   needed).
6. **Save the report** to `reports/` (`date +%F` + kebab title, never overwrite) and give
   the top themes + path in your reply.

## Report format

```markdown
# Verbatim themes: <question>

**Data basis:** <file> · answers n = <filled> of <total> · <date>

## Overview
2–3 sentences: what dominates? overall tone (positive/critical/mixed)?

## Themes (by frequency)
### 1. <theme> — ~<N> mentions
Short description. Evidence: "<verbatim quote>" · "<quote 2>"

### 2. …

## Pain points vs. valued aspects
Compact contrast of the main criticism/wish themes and praise themes.

## Implications
What follows for product/UX/prioritization?

## Method
Column analyzed, base population, coding logic, and — from the survey context — who was
surveyed and who could not be reached. Mention counts are qualitative estimates (answers
can belong to several themes).
```

## Rules
- **Completeness over convenience**: review all answers, not just a sample.
- Use quotes **verbatim** (no smoothing/inventing); trim only with […].
- Report mention counts honestly as approximations — this is qualitative coding.
- Mention non-answerers and low fill rate (bias risk).
- Don't expose personal details in quotes that could identify an individual.
- Report language = language of the answers (default English).
