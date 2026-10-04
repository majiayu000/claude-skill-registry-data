---
name: hypothesis-check
description: >-
  Tests a stated hypothesis against quantitative survey data (CSV) and delivers a verdict:
  confirmed / partly confirmed / refuted — including a Chi-square significance test,
  effect size and a counter-check. Result as Markdown to reports/. Use when the user wants
  an assumption, claim or hunch verified/falsified. Invoke with your request as the
  argument, e.g. /hypothesis-check <hypothesis>.
license: MIT
---

# Hypothesis Check

Goal: Rigorously test the **hypothesis** in the user's request against the data
and give an **evidence-backed, directional verdict** — not just describe, but test. Result
as Markdown in `reports/`.

## Tool (shared analysis engine)

```
python3 scripts/survey.py <cmd> [...] [--file CSV]
```

Run these from the project root. If `scripts/survey.py` is not there, check `.claude/scripts/survey.py` or locate `survey.py` in the project.
- `profile` — column overview (index, type, fill). **Always first.**
- `freq COL [--by COL2] [--filter "COL=VALUE"] [--top N] [--sig]` — distribution/cross-tab.
  **`--sig`** (single-choice × single-choice only) returns Chi-square, p-value, Cramér's V
  and a warning when expected cell counts are too small.
- `text COL [--filter ...] [--sample N]` — free text for qualitative evidence.

`COL` = index (from `profile`) or an unambiguous name part. `--json` for machine-readable.

## Survey context

If a context document sits next to the CSV (`<name>.context.md`, or `survey-context.md`
when the folder holds exactly one CSV), read it before testing. It carries the subject, the
glossary and the study design; use it for framing and terminology, never for figures. Its
recruiting route and **"Who is missing"** section belong in this report's limitations — a
hypothesis can hold in the sample and still fail for the population the sample cannot
reach, and that is worth a sentence.

Its **expectations** section deserves particular care here, because this is the skill most
exposed to it:

- If the user gave **no** hypothesis, you may take one from the expectations list — say
  which one you picked and that it came from the context document.
- If the user's hypothesis **matches** a listed expectation, that changes nothing at all
  about how hard you test it. Do not treat the expectation as prior support, do not soften
  the counter-check, do not let it tip a borderline verdict.
- A refuted expectation is a **result, not a failure**. Say so plainly: "this was expected;
  the data do not show it." That is the most valuable report this toolkit writes.

If no such document exists, test as before and mention `survey-context` once at the end.

## Approach

1. **Operationalize the hypothesis.** Break it into testable statements: which
   variable(s)? expected direction? which comparison groups? State it as a testable claim
   (implicit null hypothesis: "no difference / no relationship").
2. **Profile** and identify the relevant columns.
3. **Test — direction-aware.**
   - Relationship of two categoricals → `freq X --by Y --sig`: significance (p) answers
     "real or chance?", Cramér's V answers "how strong?". **Judge both together** — a
     significant but negligible effect does not practically confirm the claim.
   - Distribution/share as the claim → `freq` and check the asserted magnitude.
   - Qualitative claim → `text`, count and quote themes.
4. **Counter-check (actively try to falsify).** Find at least one analysis that could
   *contradict* the claim (alternative explanation, confounder, subgroup where it fails).
   A researcher tries to disprove their own hypothesis.
5. **Reach a verdict:** **CONFIRMED** / **PARTLY CONFIRMED** / **REFUTED** /
   **UNDECIDABLE** (e.g. sample too small, variable missing).
6. **Save the report** to `reports/` (`date +%F` + kebab title, never overwrite) and state
   the verdict + path in your reply.

## Report format

```markdown
# Hypothesis check: <claim in one sentence>

**Data basis:** <file> · n = <…> · <date>

## Verdict
**CONFIRMED / PARTLY / REFUTED / UNDECIDABLE** — 1–2 sentences of reasoning.

## Test
- Operationalization: which variables, expected direction.
- Evidence with numbers + test: "Chi2(df)=…, p=…, Cramér's V=… (effect: …)".
- Plain-language reading: is the difference real and relevant?

## Counter-check
What was tested to disprove the claim? Result.

## Limitations
Sample/subgroup sizes, small-expected-cell warnings, confounding, causality
(correlation ≠ causation!), and the limits of the study design from the survey context
(who the recruiting could not reach).

## Method
Columns, filters, tests used — reproducible in one paragraph.
```

## Rules
- Interpret **significance AND effect size** together; p alone is never enough.
- On the "expected frequency < 5" warning, explicitly qualify the result.
- Chi-square shows **association, not causation** — never phrase causally without a caveat.
- Only claim what the outputs support. Flag small subgroups (n < ~30).
- **Test the hypothesis, never argue for it** — including, and especially, when the survey
  context shows someone expected it to hold.
- Report language = language of the hypothesis (default English). Keep it short.
