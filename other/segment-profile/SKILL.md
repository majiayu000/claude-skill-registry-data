---
name: segment-profile
description: >-
  Builds a data-based comparison profile of a subgroup (segment/persona) versus the rest
  of the sample from quantitative survey data (CSV): who they are, how they differ, what
  characterizes them. Result as Markdown to reports/. Use for personas, user types or
  audience characterization. Invoke with your request as the argument, e.g.
  /segment-profile <segment, e.g. "daily users" or "Industry=Retail">.
license: MIT
---

# Segment Profile

Goal: Characterize the **subgroup** described in the user's request with data and
**contrast it against the rest of the sample** — a basis for personas/audiences. Result as
Markdown in `reports/`.

## Tool

```
python3 scripts/survey.py <cmd> [...] [--file CSV]
```

Run these from the project root. If `scripts/survey.py` is not there, check `.claude/scripts/survey.py` or locate `survey.py` in the project.
- `profile` — column overview (always first).
- `freq COL [--filter "COL=VALUE"]` — distribution within the segment (filter) vs. overall.
- `freq COL --by SEGMENT_COLUMN --sig` — segment as a column against a trait, with the
  significance test, to separate real differences from noise.
- `text COL [--filter ...] [--sample N]` — verbatims from the segment.

`COL` = index (from `profile`) or an unambiguous name part.

## Survey context

If a context document sits next to the CSV (`<name>.context.md`, or `survey-context.md`
when the folder holds exactly one CSV), read it before defining the segment. Its **column
notes** often name the segments the business actually cares about and which column carries
them — check there before inventing your own cut. The glossary keeps the profile in the
organization's own vocabulary. Figures still come only from the engine.

The **"Who is missing"** section matters doubly here: a segment profile describes a
subgroup *of the respondents*, and if the recruiting route already excluded a group, the
profile silently describes a filtered population. Put that in the method section.
Expectations listed in the document are **something to test, never something to support** —
a persona must not be shaped to match what someone assumed it looks like. If no such
document exists, proceed as before and mention `survey-context` once at the end.

## Approach

1. **Define the segment.** Translate the description into a concrete filter (e.g. usage
   frequency = "Daily"). Determine the **segment size** (n and % of the sample).
2. **Profile** and pick characterizing traits (demographics, behavior, roles, tasks).
3. **Contrast.** For each trait: distribution **in the segment** vs. **overall/rest**. The
   interesting statements are the **deviations** ("above-average share of …"). Where
   possible, check with `--sig` whether the difference is reliable.
4. **Enrich qualitatively.** Segment free text for typical needs/quotes.
5. **Save the report** to `reports/` (`date +%F` + kebab title, never overwrite) and give a
   short characterization + path in your reply.

## Report format

```markdown
# Segment profile: <segment name>

**Data basis:** <file> · segment n = <…> (<…% of the sample>) · <date>

## Short characterization
2–3 sentences: who is this segment, what defines it?

## Traits compared
| Trait | Segment | Overall/rest | Notable |
|---|---:|---:|---|
| … | …% | …% | ↑ above average / ↓ / ≈ |

(Clear and, where checked, significant deviations first.)

## Behavior & needs
What the segment does (tasks/usage) and what it needs (free-text themes, 1–2 quotes).

## What this means in practice
Implications for product/communication/prioritization.

## Method
Segment definition (filter), traits compared, tests used, and — from the survey context —
which population the sample covers and who it does not.
```

## Rules
- Always report **relative**: segment vs. overall/rest — the segment's absolute numbers
  alone say little. Deviations are the story.
- State segment size; caution when n < ~30.
- Use significance to separate chance from real differences.
- Report language = language of the request (default English). Keep it short.
