---
name: executive-summary
description: >-
  Distills a question/topic from quantitative survey data (CSV) for leadership: a
  one-pager with a TL;DR, 3–5 key findings each with a number and an implication, and next
  steps. Result as Markdown to reports/. Use when results need to be condensed for an
  executive / stakeholder audience. Invoke with your request as the argument, e.g.
  /executive-summary <question/topic>.
license: MIT
---

# Executive Summary

Goal: For the **topic** named in the user's request, produce a
**decision-oriented one-pager** for leadership/stakeholders — condensed, implication-led,
without methodological ballast. Result as Markdown in `reports/`.

## Tool

```
python3 scripts/survey.py <cmd> [...] [--file CSV]
```

Run these from the project root. If `scripts/survey.py` is not there, check `.claude/scripts/survey.py` or locate `survey.py` in the project.
- `profile` — column overview (always first).
- `freq COL [--by COL2] [--filter "COL=VALUE"] [--sig]` — distribution/cross-tab (+significance).
- `text COL [--filter ...] [--sample N]` — free text for one crisp verbatim quote.

`COL` = index (from `profile`) or an unambiguous name part.

## Survey context

If a context document sits next to the CSV (`<name>.context.md`, or `survey-context.md`
when the folder holds exactly one CSV), read it first. Two parts of it matter most here:
the **audience** (who reads this and what they decide with it — pitch the one-pager at
them) and the **subject/glossary** (so the summary uses the reader's own words, not the
column wordings). Figures still come only from the engine.

This format has no method section, which makes it the easiest place to lose the study
design — so keep one thing: if the recruiting route materially qualifies the message (the
**"Who is missing"** section), say so in **half a sentence** where it belongs, not in a
separate block. "Among active users surveyed via the app, 71% …" costs four words and stops
a leadership audience from reading a partial picture as the whole one.

Expectations listed in the document are **something to test, never something to support** —
a summary must not become the confirmation someone was hoping for. If no such document
exists, proceed as before and mention `survey-context` once at the end.

## Approach

1. **Profile**, then translate the topic into the 2–4 most telling analyses — that count
   is on top of `profile`, which is the mandatory first step, not one of them.
2. **Analyze** and pull the most important numbers. Less is more — one solid number per
   key finding.
3. **Condense to implications.** For each finding ask: "So what? What does it mean for the
   business/product/users?" That is what goes into the summary.
4. **Save the report** to `reports/` (`date +%F` + kebab title, never overwrite) and give
   the TL;DR + path in your reply.

## Report format (max one page)

```markdown
# <topic as a meaningful heading>

**Data basis:** <file> · n = <…> · <date>

## TL;DR
2–4 sentences carrying the central message. Most important first.

## Key findings
1. **<finding>** — <number absolute + %>. *Implication:* <what it means>.
2. …
(3–5 findings, each a number + implication, one line each)

## Recommendation / next steps
2–3 concrete, prioritized steps.

<optional: one crisp verbatim user quote if it reinforces the message>
```

## Rules
- **Short and implication-oriented** — leadership reads messages, not tables. One screen max.
- Every key finding carries a concrete number (absolute + %). No vague statements.
- Drop jargon and method detail (at most one line "Basis: n=…").
- Claim nothing the data doesn't support; note uncertainty in half a sentence — including
  who the survey could not reach, when that changes how the message should be read.
- Report language = language of the request (default English).
