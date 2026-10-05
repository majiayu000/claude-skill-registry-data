---
name: trend-identifier
description: "Reads a set of data points or a described data series and identifies the meaningful trends within it, expressed in plain, publication-ready language."
status: stable
category: research
subcategory: data-statistics
version: 1.0
eval_score: 4.2
tags: [trends, data analysis, journalism, statistics, reporting]
---
# Trend Identifier

## What This Skill Does
Reads a set of data points or a described data series and identifies the meaningful trends within it, expressed in plain, publication-ready language.

## When To Use This Skill
- You have a table, chart, or series of numbers and need to know what story they tell
- You are writing a data-driven piece and want to describe movement over time accurately without overstating or understating the pattern
- You need to explain a trend to a general audience without technical jargon
- You want to check whether a trend you have noticed in your data is statistically meaningful or could be noise
- A source has described a trend verbally and you need to assess whether the underlying numbers support that description

## What You Need To Provide
**Required:** The data series itself — paste the numbers, a description of the figures, or a summary table. Include what each value represents (e.g. percentage, count, rate per 100,000), the time period each corresponds to, and what geography or population it covers.
**Optional:** The publication format (news article, documentary script, data visualisation caption, broadcast voice-over); the audience (general public, specialist, policymakers); any hypothesis or angle you already have about the data; a note on the source of the figures.

## How the Assistant Approaches This
1. Maps the data as described — identifies what is being measured, the unit, the time span, and whether it is a complete series or a sample of data points.
2. Reads the direction and magnitude of change: whether values are rising, falling, flattening, accelerating, or reversing, and by how much in relative and absolute terms.
3. Identifies any notable sub-patterns: inflection points (where a trend changes direction), outlier years or periods, plateaus, and whether the trend is consistent or volatile.
4. Assesses the strength of the trend — is the direction clear and sustained, or is it marginal and potentially within normal variation? Flags where the data is ambiguous or where a stronger claim would require more data points.
5. Translates all findings into plain, publication-ready sentences at the level of precision the data actually supports — no overclaiming, no unnecessary hedging.

## Output Format
Two sections:

**Trend Summary** — 2–4 sentences describing the primary trend in plain language. Precise enough to quote directly in a story. Includes the percentage or absolute change where relevant, the time span, and one note on any meaningful caveat.

**Detailed Findings** — a bulleted list of 4–8 specific observations: the main trend, any sub-trends, inflection points, outliers, and an honest assessment of what the data does and does not allow you to conclude. Each bullet is one to two sentences.

Total length: 300–500 words. Tone: clear and direct — the language a senior editor would expect in a data memo, not a statistics paper.

## Quality Criteria
- [ ] The trend summary is specific enough to be published without editing — it names the direction, magnitude, and time period
- [ ] Relative change (percentage) and absolute change are both given where the data supports it
- [ ] Inflection points and outlier periods are identified separately from the main trend
- [ ] The output distinguishes between what the data shows and what it cannot prove
- [ ] No trend is described as "significant" without clarifying whether that is statistically or editorially significant
- [ ] The language is at a level any reader of a national newspaper could follow

## Example

### Input
Data: Annual road fatalities per million inhabitants, a mid-sized European country, 2010–2023.

2010: 68
2011: 61
2012: 57
2013: 54
2014: 50
2015: 49
2016: 47
2017: 46
2018: 45
2019: 43
2020: 37
2021: 41
2022: 44
2023: 43

Source: national road safety agency, administrative data.
Format: opening paragraph for a long-read magazine feature on road safety.
Audience: general public.

### Output

**Trend Summary**

Road deaths fell sharply over the first decade of this record — from 68 deaths per million people in 2010 to 43 in 2019, a reduction of 37% in nine years. The Covid-19 pandemic produced a dramatic one-year drop to 37 in 2020, as traffic volumes collapsed. But the recovery in driving has not been matched by a recovery in safety: fatalities rose in 2021 and 2022, reaching 44 — nearly erasing the gains of the previous four years — before edging back to 43 in 2023. The long-term downward trend has stalled.

**Detailed Findings**

- **Main trend (2010–2019):** Consistent, sustained decline averaging roughly 2.5 deaths per million per year. The direction is unambiguous across the full period.
- **Rate of improvement slowing pre-pandemic:** The steepest reductions came early (7 deaths per million between 2010 and 2011); by 2017–2019 the annual improvement had narrowed to 1–2 deaths per million. Progress was decelerating before Covid.
- **2020 outlier:** The fall to 37 in 2020 almost certainly reflects reduced traffic volumes during lockdowns rather than structural safety improvements. This year should be treated as an anomaly when describing the long-term trend.
- **2021–2022 reversal:** The two-year rebound to 44 is the sharpest upward movement in the entire series. This is a meaningful reversal, not noise — but the data alone cannot tell you whether it is driven by higher speeds, distracted driving, road freight increases, or changed enforcement.
- **2023 position:** The slight dip back to 43 does not re-establish the pre-pandemic downward trajectory. At current levels, the country is performing roughly as it did in 2018 — five years of progress have been lost.
- **What the data cannot show:** Whether the stall is permanent or a post-pandemic correction. A further three to four years of data would be needed to confirm whether the downward trend has genuinely ended.

## Known Limitations
- This skill interprets trends in data as described or pasted — it does not perform statistical significance testing. For formal analysis (confidence intervals, regression, seasonal adjustment), you need a data journalist or statistician to run the numbers directly.
- If the data series is short (fewer than five data points) or heavily rounded, the skill will flag that the trend description must be hedged accordingly — short series can mislead.
- The skill cannot account for changes in how data was collected over time; if the source methodology changed mid-series, that must be noted by the user, as the assistant will not know unless told.

## Related Skills
- [statistics-researcher](../statistics-researcher/SKILL.md)
- [statistical-report-summariser](../statistical-report-summariser/SKILL.md)
- [data-story-finder](../../../data-journalism/analysis/data-story-finder/SKILL.md)
- [data-outlier-finder](../../../data-journalism/analysis/data-outlier-finder/SKILL.md)
- [dataset-summary-brief](../../../data-journalism/analysis/dataset-summary-brief/SKILL.md)
