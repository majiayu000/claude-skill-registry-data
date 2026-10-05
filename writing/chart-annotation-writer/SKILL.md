---
name: chart-annotation-writer
description: "Writes the annotation text for a data chart — axis labels, callout boxes, trend labels, source lines, and explanatory notes — so that a reader can understand the chart's key finding without reading the surrounding article."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 4.2
tags: [data, charts, annotation, callouts, data-journalism, visualization, writing]
---
# Chart Annotation Writer

## What This Skill Does
Writes the annotation text for a data chart — axis labels, callout boxes, trend labels, source lines, and explanatory notes — so that a reader can understand the chart's key finding without reading the surrounding article.

## When To Use This Skill
- You have a finished chart and need the annotation layer written before handing to a designer or data visualisation editor
- Your chart shows a clear data story but you are not sure how to phrase the callout that highlights the key moment or outlier
- You are producing a chart that will be shared as a standalone image on social media and needs to be fully self-explanatory
- You need consistent annotation style across a series of charts in the same report or data package
- You are writing a methodology note or source line for a chart and want it to be precise without being jargon-heavy

## What You Need To Provide
**Required:** A description of the chart — what type it is (bar, line, scatter, map, etc.), what the axes represent, what the data shows, and what the key finding or data story is; the topic and publication context
**Optional:** The specific data point or moment you want highlighted as a callout; any secondary patterns worth noting; the publication's annotation style (brief labels vs. full explanatory sentences); character or word limits imposed by the design template; whether the chart will appear in print, on screen, or as a standalone social graphic

## How the Assistant Approaches This
1. Identifies the one primary data story the chart is built to show — the trend, the outlier, the crossover point, or the comparison — and writes the main callout around that single finding, not a summary of all the data
2. Writes axis labels that are specific and honest: units are stated, time periods are clear, and any index or percentage base is explained in a note rather than assumed
3. Constructs callout text to answer the question a first-time reader would ask when they see the highlighted data point: "What happened here, and why does it matter?" — in no more than two short sentences
4. Writes a source line that names the data source, the year or date range of the data, and any significant caveat about coverage or methodology, without making it so long it clutters the chart
5. If the chart covers a complex or contested topic, adds a brief methodology note (one to three sentences) separate from the main callout, covering how the data was collected or calculated
6. Delivers all annotation elements as clearly labelled components — main callout, axis labels, source line, methodology note — so a designer can apply each to the correct layer without ambiguity

## Output Format
Structured output with clearly labelled components:

- **Chart title:** 6–12 words, declarative (states the finding, not just the topic)
- **Subtitle / deck:** 1 sentence, provides the "so what" or the time frame context
- **X-axis label:** concise, with units
- **Y-axis label:** concise, with units
- **Main callout text:** 1–2 sentences, max 30 words, placed at the key data moment
- **Secondary callout (if applicable):** 1 sentence, max 20 words
- **Source line:** data source, date range, and one significant caveat if needed — under 25 words
- **Methodology note (if applicable):** 1–3 sentences for complex or contested data

All annotation text is written in plain English at a general-audience reading level. Avoid jargon in axis labels. Source lines should be factual and specific, not vague ("various sources" is not acceptable).

## Quality Criteria
- [ ] Chart title states the finding, not just the topic ("Rents rose fastest in mid-sized cities" not "Rental market trends")
- [ ] Main callout targets a single data moment — not a general description of the whole dataset
- [ ] Callout text is under 30 words and written for a reader who has not read the article
- [ ] Axis labels state units explicitly (%, $m, years, index 2010=100)
- [ ] Source line names the specific dataset or organisation, not just a category ("World Bank" not "international data")
- [ ] Methodology note is present when data is indexed, modelled, or seasonally adjusted
- [ ] All components are clearly labelled so a designer can place them without interpretation

## Example

### Input
Chart type: Line chart
What it shows: Monthly average residential rental prices (indexed to January 2019 = 100) for three city tiers — large capitals, mid-sized regional cities, and small towns — from January 2019 to December 2023
Key finding: Mid-sized regional cities saw the steepest rental increase of the three groups, overtaking large capitals in mid-2021 and maintaining the lead through the end of the period
Data source: National housing price registry, annual release, 2024
Secondary observation: Small town rents remained nearly flat until early 2022, then rose sharply
Publication: General-interest digital news outlet

### Output

**Chart title:** Mid-sized cities now have the fastest-rising rents — overtaking capitals in 2021

**Subtitle:** Monthly average residential rents, indexed to January 2019 = 100, across three city tiers

**X-axis label:** Month (Jan 2019 – Dec 2023)

**Y-axis label:** Rent index (Jan 2019 = 100)

**Main callout text (placed at mid-2021 crossover point):**
Mid-sized cities overtook large capitals here and have not looked back. By December 2023, their indexed rents were the highest of any city tier.

**Secondary callout (placed at early 2022 for small towns):**
Small town rents rose sharply from early 2022 — a delayed catch-up after two years of near-stagnation.

**Source line:**
National housing price registry, 2024 annual release. Data covers registered tenancy contracts; private informal rentals are not included.

**Methodology note:**
Prices are indexed to January 2019 = 100 for each city tier separately. Index values show relative change within each group, not absolute price comparisons between groups.

## Known Limitations
- Callout text is written from the data story you describe — the assistant does not have access to the actual dataset and will not generate or verify specific numbers for callouts; any figures in callouts must be verified by the journalist against the source data
- Chart titles that state a clear finding ("rents rose fastest") may face editorial pushback in outlets that prefer neutral descriptive titles; adjust the title register to match your publication's style guide
- For charts covering politically sensitive topics (elections, economic inequality, immigration), the framing of the callout can itself be contested — run callout text past your editor before publication
- This skill does not produce chart design specifications or layout coordinates; it delivers text only, for a designer to position

## Related Skills
- [chart-description-writer](../../../data-journalism/visualization/chart-description-writer/SKILL.md)
- [alt-text-writer](../../../magazine-journalism/writing/alt-text-writer/SKILL.md)
- [sidebar-fact-box-writer](../../../magazine-journalism/writing/sidebar-fact-box-writer/SKILL.md)
