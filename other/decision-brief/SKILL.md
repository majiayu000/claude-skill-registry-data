---
name: decision-brief
description: >-
  Builds a structured decision brief (decision memo) from quantitative survey data (CSV):
  situation, options with pros/cons backed by data, a reasoned recommendation, risks and
  assumptions. Result as Markdown to reports/. Use when a decision is due that should be
  grounded in research evidence. Invoke with your request as the argument, e.g.
  /decision-brief <decision / question>.
license: MIT
---

# Decision Brief (Decision Memo)

Goal: For the **decision** named in the user's request, build an actionable brief
in which **every option is backed by data** and a **clear recommendation** is given. For
decision-makers, not analysts. Result as Markdown in `reports/`.

## Tool

```
python3 scripts/survey.py <cmd> [...] [--file CSV]
```

Run these from the project root. If `scripts/survey.py` is not there, check `.claude/scripts/survey.py` or locate `survey.py` in the project.
- `profile` — column overview (always first).
- `freq COL [--by COL2] [--filter "COL=VALUE"] [--sig]` — distribution/cross-tab,
  `--sig` for significance + effect size (single × single).
- `text COL [--filter ...] [--sample N]` — verbatims/free text as evidence.

`COL` = index (from `profile`) or an unambiguous name part.

## Survey context

If a context document sits next to the CSV (`<name>.context.md`, or `survey-context.md`
when the folder holds exactly one CSV), read it first — this skill benefits from it more
than any other, because it names the pending decision and the audience the brief is for.
Take the situation, the subject and the glossary from it; the figures still come only from
the engine. Its recruiting route and **"Who is missing"** section belong under risks and
assumptions: an option that looks strong among the people who answered may look different
among those the survey never reached. Expectations listed there are **something to test,
never something to support** — never let one decide which option wins. If no such document
exists, proceed as before and mention `survey-context` once at the end.

## Approach

1. **Sharpen the decision.** What exactly is being decided? Which options are plausible?
   If not given, derive 2–4 realistic options (include "status quo / do nothing" as a
   baseline).
2. **Profile** and find the decision-relevant variables.
3. **Gather evidence per option.** For each option, query the data that argues for or
   against it (distributions, cross-tabs, significance where relevant, free-text needs).
   Also quantify the size of affected user groups (impact).
4. **Weigh and recommend.** Compare options on the evidence, give a reasoned
   recommendation. Expose trade-offs, don't hide them.
5. **Save the report** to `reports/` (`date +%F` + kebab title, never overwrite) and state
   the recommendation + path in your reply.

## Report format

```markdown
# Decision brief: <decision>

**Data basis:** <file> · n = <…> · <date>

## Recommendation
Clear statement in 1–2 sentences: which option, and why.

## Situation
Why is the decision due? Relevant data context in 2–4 sentences.

## Options compared
| Option | For (data) | Against (data) | Affected (impact) |
|---|---|---|---|
| A … | … (number) | … (number) | … % of users |
| B … | … | … | … |
| Status quo | … | … | … |

## Rationale
Why the recommended option wins the trade-off — with the decisive numbers.

## Risks & assumptions
What must hold? What could go wrong? Data gaps/uncertainties, including whom the survey
could not reach (from the survey context) and what that could mean for the recommendation.

## Next steps
2–4 concrete, prioritized steps.

## Method
Columns/filters/tests used, in one paragraph.
```

## Rules
- **Every** option needs data (pro *and* con) — no gut calls.
- State the recommendation unambiguously, but make trade-offs and uncertainty transparent.
- Use significance/effect size where group differences drive the decision.
- Quantify impact (how many users / what share affected).
- Report language = language of the request (default English). Decision-maker tone: short,
  concrete.
