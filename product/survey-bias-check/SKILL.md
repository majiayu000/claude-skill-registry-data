---
name: survey-bias-check
description: Requires Python 3.9+ for the bundled standard-library script; no account
  or API key for local use; an optional step applies accepted rewrites through QuestionPunk's
  remote MCP server after OAuth sign-in. Review a survey or questionnaire for leading,
  loaded, double-barreled and assumptive questions, double negatives, unbalanced scales,
  overlapping or gapped answer ranges, missing none or other options, and missing
  or overlong recall periods, with a rewrite for each problem question.
license: MIT
metadata:
  version: 0.2.1
  status: beta
  author: QuestionPunk
  source: questionpunk/research-skills
  requires-account: 'false'
  plugin: survey-design
---
# Survey bias check

Review a questionnaire before it is fielded. A script finds candidate problems by pattern; you judge each
candidate, read the questionnaire for what patterns cannot see, and write a rewrite for each problem
question.

## When to use

Use for requests such as:

- "Here is my 12-question onboarding survey, what is wrong with it?"
- "Check (audit, lint) these survey questions" or "review this feedback form".
- "Is this NPS or CSAT survey OK to send?"
- "Check this Google Form, Typeform or Qualtrics draft for leading questions."
- "Are these answer options OK?" (age or income ranges, rating scales, recall periods)
- "Is this survey too long?"

Do not use for (and what handles it instead):

- Writing a new survey from a goal: `survey-from-decision`.
- Converting a Qualtrics `.qsf` file: `qsf-convert` first, then this skill on its Markdown.
- Problems in collected answers (speeders, straight-liners, duplicates): `survey-data-cleaning`.
- An interview or discussion guide: `ai-interview-guide`.
- Indirect methods for a sensitive topic (list experiments, randomized response), screen-reader and
  contrast checks, or a translation check against the source: outside this skill. Say so, check the
  wording you were given, and point to the SB021 guidance in the rule catalogue for sensitive topics.

A skill named here may not be installed. If it is not, say so, do the part of the request this skill
covers, and for a `.qsf` file ask for the questions as pasted text or an export to Word or PDF.

## What to ask for

Ask at most one question: for the questionnaire, if it was not given. Everything else has a default.

| Input | Default when not given | Script flag |
|---|---|---|
| The questionnaire (file, export or pasted text) | none; ask for it | |
| Introduction text shown before question 1 | not checked; say so | |
| Audience | general public, so acronyms and trade terms count | `--audience expert` |
| Mode | self-administered online survey | `--mode phone` |
| Language | English; other languages are read by you, not the script | |
| Questions that must stay unchanged (validated scale, tracker) | none | `--keep Q7,Q9` |

State the defaults you used in the answer.

## Input format

The script reads Markdown or plain text, JSON, or the Markdown that `qsf-convert` writes (`### tag [type]`
headings; detected automatically, tags become the question IDs). It does not read form exports. In plain
Markdown: questions numbered at the start of a line, answer options as list items, grid rows as lettered
lines, the introduction as plain lines before question 1.

```text
This survey has 4 questions and takes about 1 minute.

1. How satisfied or dissatisfied are you with the app overall? *
   - Very satisfied
   - Neither satisfied nor dissatisfied
   - Very dissatisfied
2. Which features have you used in the past 30 days? Select all that apply. [multi]
   - Dashboards
   - None of these
3. How well does each word describe the app? [grid]
   a) Fast
   b) Stable
   - Very well
   - Not at all well
4. What should we improve?
```

- Question: `1.`, `1)`, `Q1.` or `Q1:`. A line right after it that is not an option continues the stem.
- With no numbers anywhere, each non-option line ending in `?` is read as a question and numbered in order.
- Option: a line starting with `-`, `*`, `+`, `( )` or `[ ]`. Grid row: `a)` or `a.`, followed by `-` options
  (the columns). Lettered lines with no `-` options, indented numbered lines (`   1) Very satisfied`) and two
  or more short unmarked lines after a question ending in `?` are read as options, with a warning.
- Required: `*` at the end, `(required)` or `[required]`. `(optional)` is removed from the stem.
- Type tag, optional, on the question line or a line of its own: `[single]`, `[multi]`, `[scale]`, `[grid]`,
  `[number]`, `[open]` or `[text]` (`[number, 0 to 3]` works too). Without a tag: lettered rows mean grid, no
  options means open (numeric entry when it asks how many, how much, how long, an age or a year), "select all that apply" means multi, anything else single.
- Skip-logic lines such as `(If 0, go to question 6.)`, closing lines starting "Thank you" and headings
  (`#`) are not read as question text; skip logic is listed in a warning.

JSON is also accepted: a list, or an object with `questions` and optionally `intro`, where each question has
`text` and optionally `id`, `type`, `required`, `options` and `rows`.

## Steps

1. **Convert the questionnaire** to the input format and save it to a file (`survey.md` below). A Google Form,
   Typeform or Qualtrics draft arrives as pasted text, a link's page text, a PDF or a CSV/JSON export: copy
   out the introduction, question text, options, required flags and order exactly as written, tag the types
   you can see (`[multi]`, `[scale]`, `[number]`, `[grid]`), and note any skip logic. For a `.qsf` file run
   `qsf-convert` (`to-md`) and pass its Markdown in unchanged. Never fix wording while converting. Then
   reconcile: the script's `questions` count must equal the questions in the source (a `qsf-convert` file
   also has `[info]` screens, read as the introduction); find any difference before going on.
2. **Run the linter.** Run every script by its path inside this skill's directory (shown here as
   `<skill-dir>`), from any working directory:

   ```bash
   python3 <skill-dir>/scripts/survey_bias_check.py survey.md --json
   ```

   With skip logic, add `--route-skip` with the questions off the longest route, so the length is that
   route's. `-` instead of a file name reads standard input. Exit code 0 means it ran, with or without findings; 2
   means the input could not be read (fix the format, do not guess). Options: `--mode phone`,
   `--audience expert`, `--keep Q7,Q9`, `--route-skip Q5,Q6` (questions off the longest route, for the
   length), `--language en|other` (override the per-question English check), `--ignore SB011,SB013`,
   `--strict` (exit 1 on findings), `--max-words`, `--max-options`, `--max-grid-rows`, `--max-open`,
   `--list-rules`. The linter is [`scripts/survey_bias_check.py`](scripts/survey_bias_check.py) (Python
   3.9+, standard library only). Use its length estimate; do not recompute it in the conversation.
3. **Judge every candidate.** For each finding decide: confirmed, or dismissed with a reason. The
   [rule catalogue](references/rules.md) lists, for each rule, what it matches and when to ignore it.
   Typical dismissals: "and" inside one concept, an acronym every respondent uses, a complete list with no
   need for "Other", a screener that must come first. Dismiss SB018 when the survey population is defined by
   the thing asked about (a member survey asking members about opening hours).
4. **Read the questionnaire for what rules miss** (catalogue section "What no rule checks"): assumptions in
   other wording, social desirability outside the word list, undefined terms, loaded wording outside the
   word lists, options that do not fit the audience, missing open-ended ranges, and order: general before
   specific, earlier questions that prime later ones (a specific behaviour or attribute before an overall
   rating), nominal lists that should be randomised with "Other" and "None" kept last, ordinal options in
   logical order. Also: "None of these" set as exclusive in a `[multi]`, required questions with no way out,
   intro claims (time, anonymity) that the questionnaire contradicts, and skip logic with dead ends. Add what you find with the
   rule column set to `judgment`.
5. **Handle what the script could not check.** Questions under `unchecked` (not English), any `warnings`,
   a missing introduction (`has_intro: false`) and skip logic need your own reading. Say so in the answer.
6. **Write a rewrite for each confirmed problem.** Keep the meaning and the measurement goal; change as
   little as possible; rewrite the options too when they are the problem. When a question asks two things,
   give both replacement questions. For a "keep as is" question, report the problem and what a change would
   cost in comparability instead of a rewrite. Two pack-wide defaults, shared with `survey-from-decision`:
   - A count or amount the respondent knows (visits, days, minutes, spend on one occasion) becomes an open
     number over a named recent period. Keep or write ranges only when the exact figure is sensitive
     (income), can only be estimated in bands, or the tool cannot take numbers; then make them exclusive and
     exhaustive, and for time or other continuous measures write "under N / N to under M / M or more".
   - A rebalanced scale keeps its number of points, so it still matches the survey's other scales (SB012).
     A new scale is fully labelled: 7 points when it has two opposite ends, 5 when it runs from none to a
     lot (a pack default; see sources.md).
7. **Give the verdict, the length and the pretest line** in the shape below.

## Rules

| ID | Finds candidates for | Severity |
|---|---|---|
| SB001 | Double-barreled: "and" / "or" joining two things | medium |
| SB002 | Leading or loaded wording (word list) | high |
| SB003 | Absolutes: always, never, everyone | medium |
| SB004 | Hypotheticals: "would you pay", "if we added" | medium |
| SB005 | Double negatives; a negation with yes/no or agree/disagree | high / medium |
| SB006 | Vague quantifiers: regularly, often, sometimes | low |
| SB007 | Undefined acronyms and trade terms | low |
| SB008 | Stem longer than 20 words | low |
| SB009 | Unequal numbers of positive and negative scale labels | high / medium / low |
| SB010 | Numeric ranges that overlap, leave a gap or are reversed; gaps in a continuous measure | high / medium |
| SB011 | No "None of these" (select-all), "Other" (lists) or "Not sure" (narrow) | medium / low |
| SB012 | Scale direction or length that changes between questions | medium |
| SB013 | More than 10 named options (5 by phone) | low |
| SB014 | Agree/disagree items and grids | low / medium |
| SB015 | Estimated length above 10 minutes (low) or 20 minutes (medium) | low / medium |
| SB016 | Sensitive or demographic questions first; required with no opt-out | low / medium |
| SB017 | No reference period; long recall window for a count | low |
| SB018 | Built-in assumption: no "Never" / "Does not apply" and no filter question | medium / low |
| SB019 | Options that do not answer the stem; one-sided stem over a two-sided scale | high / medium / low |
| SB020 | Numeric scale with no verbal labels | medium |
| SB021 | Sensitive or socially desirable behaviour (word list) | low |
| SB022 | Merged opt-outs such as "None / Other" | medium |
| SB023 | Mental computation: averages, percentages, totals | low |
| SB024 | Introduction that leads or gives no time estimate | medium / low |
| SB025 | More than 10 grid rows (5 by phone), more than 3 open questions, open question first | low |
| SB026 | Syntax load: conditions, exclusions, parentheticals, inline lists | low |
| SB027 | Even-point two-sided scale (a note, not counted) | info |
| SB028 | The same option twice | high |

The length estimate uses Versta Research points (single choice 1, grid row 1, two select-all options 1,
numeric entry 2, open question 3 for one expected sentence, 1 per three sentences of reading including the
introduction) at 8 points per minute, times 1.5 by phone. It counts every question unless `--route-skip`
names the questions off the longest route. Limits without a research source (10 options, 10 grid rows, 3
open questions) are conventions with a flag to change them. Sources for every rule and number:
[references/sources.md](references/sources.md). The catalogue also maps the 27 QAS-99 appraisal decisions
to these rules. For predicted reliability and validity of a single question, SQP (https://sqp.gesis.org)
complements this check.

## Output

Always this shape, in this order:

```markdown
## Survey bias check: <survey name>

Assumed: <audience>, <mode>, <language>. Checked <N> questions; <C> confirmed problems
(<H> high, <M> medium, <L> low); <D> rule candidates dismissed.

| Q | Problem | Rule | Severity | Rewritten question |
|---|---|---|---|---|
| 2 | Asks about speed and reliability in one question; 3 positive labels against 1 negative | SB001, SB009 | high | "How satisfied or dissatisfied are you with the speed of the app?" (Very satisfied / Somewhat satisfied / Neither satisfied nor dissatisfied / Somewhat dissatisfied / Very dissatisfied). Ask reliability as a separate question with the same options. |
| 5 | Assumes the respondent has contacted support | judgment | medium | Add a filter question first: "In the past 3 months, have you contacted support?" |
| 7 | Agree/disagree grid from a validated instrument | SB014 | medium | keep as is (changing it breaks comparison with the published norms) |

**Dismissed candidates:** Q4 SB001 ("terms and conditions" is one concept); ...

**Not checked by rules:** <unchecked questions, skip logic, missing introduction, anything not assessed>

**Verdict:** <Ready to field | Fix before fielding | Not ready>. <One or two sentences: the main reason.>

**Length:** about <minutes_rounded> minutes (<points> points at 8 points per minute<, times 1.5 by phone>;
<every question counted | longest route only>). <Under 10 minutes | Above 10 minutes, the median ideal length
web-panel respondents report | Above 20 minutes, their median maximum.> (The thresholds come from web
panels; by phone say so.)

**Pretest:** this is a desk review; try the questionnaire on a few people from the target group before
fielding.
```

- One row per question with a confirmed problem, in questionnaire order; grid rows as `11b`, the
  introduction as `intro`, a problem with the whole questionnaire (length, order, open-question count) as
  `survey`. Severity is the rule's (catalogue); for `judgment`, high when the answers would be unusable,
  medium when biased, low when only harder to answer. `<C>` counts confirmed problems, a row with two rules
  as two, `keep as is` rows not at all. An SB027 note goes under "Not checked by rules".
- Verdict: **Not ready** if any high-severity problem is confirmed; **Fix before fielding** if only medium
  ones are; **Ready to field** if only low ones or none are. Judgment findings take the severity you
  assign. Notes (SB027) and "keep as is" questions do not change the verdict.
- If nothing is confirmed, keep the table header with a single row "none" and still list the dismissals.
- Offer the full rewritten questionnaire only if the user asks for it.

## Checks before answering

- Did the script run, and did every candidate get a decision (confirmed or dismissed with a reason)?
- Is every confirmed problem described in plain words, not only by rule ID?
- Did you avoid calling a pattern hit a defect without reading the question?
- Did you read the whole questionnaire for assumptions, social desirability, order and undefined terms?
- Does each rewrite keep the original meaning and fix the options when the options were the problem?
- Is each rewritten count an open number, or are its ranges exclusive and exhaustive (with "N to under M"
  for continuous measures), so every respondent can answer?
- Does every rewritten frequency or count question name a short reference period and offer a zero answer?
- Did you leave validated or tracked questions unchanged and say what comparability a change would cost?
- Did you avoid adding "Don't know" to screeners and opinion questions without a reason?
- Are non-English questions, a missing introduction and other unchecked parts named as unchecked?
- Is the length reported as an estimate, with the script's numbers?
- Did you state the assumed audience and mode, and include the pretest line?

## Field it (optional)

To run this on QuestionPunk, connect its MCP server (`https://app.questionpunk.com/api/v1`, OAuth sign-in). Tools: `survey_list` and `survey_get` (find a survey and read its questions to check), `question_update_text` and `question_update` (apply the rewrites the user accepts), `question_create` (a filter question a rewrite adds). Ask the user before creating, changing or publishing anything. If a tool says a permission is missing, reconnect and approve the requested access.
