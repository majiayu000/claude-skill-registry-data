---
name: action-title-writer
description: Rewrite topic-label slide titles into headline action titles that state the so-what. Use when titles name the subject instead of delivering the message.
---

# Action Title Writer

## When to use
Use this when slide titles read like file names: "Q3 Revenue", "Market Overview", "Competitive Landscape". They tell the reader what the slide is about but not what it says. You need every title rewritten as an action title, a full sentence that states the slide's single message, so a reader who reads only the titles still gets the whole argument.

## What it does
It converts each topic-label title into an action title: a complete declarative sentence carrying the slide's so-what. Read top to bottom, the action titles alone form the storyline of the deck. The body of the slide becomes proof of the title rather than a place to hunt for the point.

## Method
An action title states the conclusion of the slide, not its contents. The test is the "title-only read": if someone reads only the titles of every page, they should reconstruct the argument. Topic labels fail this test; action titles pass it.

1. Find the one message. For each slide, ask what single thing this page proves. If it proves two things, it is two slides, or one of the two is really backup. The action title carries that one message and nothing else.

2. Write it as a full sentence with a verb. "Revenue" becomes "Revenue grew 12 percent, but all of it came from one account". A label has no verb and no claim. An action title has both. The verb is where the so-what lives, so choose a real one (grew, fell, shifted, concentrated, lagged), not a placeholder (relates to, concerns).

3. State the conclusion, not the data. The chart shows the data; the title states what the data means. "Three competitors entered the segment" is closer to a label. "Competitor entry has commoditised the segment, so we cannot win on price here" is the conclusion the slide exists to support.

4. Make it specific and falsifiable. A good action title is a claim someone could dispute. "We are well positioned" is vacuous. "We hold the only distribution network with national coverage, which is the one advantage rivals cannot copy this year" can be argued with, which means it says something.

5. Keep it to one readable line. An action title is a headline, not a paragraph. Aim for a single line. If it needs two clauses, make sure both serve the one message; cut any qualifier that hedges rather than informs.

6. Check the title-only read. Lay the action titles in sequence and read just them. They should flow as a coherent argument that matches the governing thought. Where the flow jumps, a slide is missing or out of order. Where two titles say the same thing, two slides are redundant. This check doubles as a storyline audit.

7. Align the body to the title. After rewriting, confirm the slide body actually proves the title. A sharp action title over a body that argues something else is worse than a label, because it promises and does not deliver.

## Inputs
- The current slide titles (and ideally the slide contents or a one-line description of each).
- The governing thought, so the title-only read can be checked against it.

## Output format
Return, per slide: the original title, the rewritten action title, and a one-line note on whether the slide body supports it. Then the full title-only read as a numbered sequence, with a note on any gap, jump, or redundancy it reveals.

## Example
Original: "Customer Segmentation"
Action title: "Two segments drive 80 percent of profit, so the growth plan should concentrate there, not spread across all five."

Original: "Pricing Analysis"
Action title: "We hold pricing power only in the enterprise segment, which is where any price increase should be taken."

Title-only read (excerpt): 1) Growth has stalled and the old model has peaked. 2) Two segments drive most of profit. 3) We hold pricing power only in enterprise. Note: the sequence flows; consider whether a slide on the mid-market loss belongs between 2 and 3.
