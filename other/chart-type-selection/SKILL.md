---
name: chart-type-selection
description: Picks the right chart type for your data and your message using a decision tree, so the chart proves the point instead of just showing numbers.
---

# Chart Type Selection

## When to use
Use this skill first, before you build anything. You have a table of numbers and a point to make, but you are not sure whether it should be a bar, a line, a scatter, a waterfall, or something else. Run this skill to convert "what data do I have" plus "what am I trying to say" into one defensible chart type.

## What it does
It returns a single recommended chart type, a short reason tied to your message, and two runner-up options with the trade-offs. It also flags when a chart is the wrong tool and a table or a single number would land better. The output is structured so you can drop the recommendation straight into the build step.

## Method
The skill runs a message-first decision tree. The driving question is never "what does the data look like" alone. It is "what is the one sentence the audience should remember, and which encoding proves that sentence fastest."

Step 1. State the message in one sentence.
Force the message into a single declarative claim, for example "European margin fell while volume held" or "two segments drive eighty percent of revenue." If you cannot write the sentence, stop. The chart cannot be chosen until the claim exists.

Step 2. Classify the claim into one of six message types.
- Comparison across categories (which is bigger, ranking).
- Change over time (trend, growth, inflection).
- Composition (parts of a whole, mix shift).
- Relationship (correlation between two measures).
- Distribution (spread, concentration, outliers).
- Bridge (how a start value became an end value through additions and subtractions).

Step 3. Map the message type to an encoding using the tree.
- Comparison across categories: horizontal bar, sorted by value. Use a column only when the category is naturally ordered left to right.
- Ranking with many categories: horizontal bar, sorted, top items only.
- Change over time, continuous: line. Few periods and emphasis on level: column.
- Composition, single point in time, few parts: hundred percent stacked bar or a labeled breakdown. Avoid pie beyond three slices.
- Composition, change in mix over time: hundred percent stacked column or a set of stacked columns.
- Relationship between two measures: scatter. Add a third measure as bubble size only if it earns its place.
- Distribution: column histogram or a sorted dot plot.
- Bridge: waterfall.

Step 4. Apply the "can the eye decode it" filter.
Position along a common axis is the most accurate visual channel, followed by length, then angle and area. Prefer charts that use position and length. Treat area and angle (pie, bubble, treemap) as last resorts, and only when the message is "roughly how big," not "exactly how much."

Step 5. Run the disqualifiers.
- More than five lines on one chart: switch to small multiples.
- More than seven stacked segments: regroup into an "other" bucket or switch to a sorted bar of the top items.
- Two numbers being compared: a sentence or two large numbers beat any chart.
- A single value versus a target: a labeled bullet bar or one number with context, not a gauge.

Step 6. Confirm the chart restates the title.
The chosen chart must make the one-sentence message obvious within five seconds. If it does not, return to Step 2.

## Inputs
- The dataset (paste the table or describe the columns and a few rows).
- The one-sentence message, or enough context for the skill to draft it.
- The audience and the setting (board, internal working session, client read-out).
- Any constraint, for example "must fit one quadrant of a busy slide."

## Output format
A short structured recommendation:
- Message restated in one sentence.
- Message type (one of the six).
- Recommended chart type, with a one-line reason.
- Two alternatives, each with a trade-off.
- Any disqualifier that was triggered and how it was resolved.
- A note on whether a chart is even the right format.

## Example
Input: "Revenue by region for the last fiscal year. North America 120, Europe 80, Asia 60, Latin America 18. I want to show that North America dominates."

Output:
- Message: North America generates the majority of regional revenue.
- Message type: comparison across categories.
- Recommended: horizontal bar, sorted descending, North America on top, value labels at the bar ends.
- Alternative 1: column chart. Trade-off, region names get cramped or rotated.
- Alternative 2: hundred percent stacked bar. Trade-off, it shifts the message to share of total rather than absolute size.
- Disqualifier check: only four categories, so no "other" bucket needed.
- Note: a chart is justified because the audience should compare four values at a glance.
