---
name: chart-to-message-mapper
description: Turns a raw chart into a message-driven exhibit by adding the action title, the one highlight, the labels that matter, and removing everything that does not serve the point.
---

# Chart-to-Message Mapper

## When to use
Use this when you have a correct chart that does not communicate, for example a default Excel chart pasted onto a slide. Use it when a reader has to study a chart to find the point. Use it after exhibit selection, to finish the exhibit so the message is unmissable.

## What it does
It transforms a neutral chart into a persuasive exhibit. It attaches the message as a title, directs the eye to the single insight, labels only what matters, and strips the chart junk so the data carries the argument by itself.

## Method
The principle is that an exhibit should make its point in under five seconds, with no narration needed.

1. Write the takeaway as the chart title. The chart gets the action title, not "Revenue by region". The title states the conclusion the chart proves.

2. Pick the one thing to see. Decide the single element the reader must notice, one bar, one inflection, one gap. Everything else exists only as context.

3. Use color as a pointer, not decoration. Mute the whole chart to one neutral tone and apply a single accent color to the one element that carries the message. Do not give every series a different bright color; that hides the point.

4. Label directly. Put data labels on the elements that matter and remove the rest. Replace a legend with labels placed next to the lines or bars they name. Direct labels beat a legend the reader must decode.

5. Add the reference line. Draw the benchmark, target, or prior period as a thin line so the audience sees the comparison, not just the level.

6. Annotate the insight. Add one short callout near the highlight that states the so-what in a few words, with a thin leader line to the element. One annotation, not five.

7. Strip chart junk. Remove gridlines (or fade to faint), remove the chart border, remove redundant axis titles, drop decimal places that do not matter, remove 3D and shadows. Keep the axis the reader actually needs.

8. Order for meaning. Sort bars by value unless time order is the point. An unsorted bar chart wastes the reader's effort.

9. Re-read against the title. Cover the title and ask whether the chart still implies it. If not, the highlight or the data is not doing the job.

## Inputs
- The raw chart or its underlying numbers.
- The intended message (the action title).
- The benchmark or comparison to show.

## Output format
Return a finishing spec: the chart title, the element to highlight and in which accent, which labels to keep and which to drop, the reference line to add, the one annotation text, and the list of chart junk to remove. If the chart cannot support the title, say so.

## Example
Raw: a multicolor clustered bar chart of cost per unit across eight sites, full legend, gridlines.
Mapped: title "Two sites cost double the network average"; all bars gray except the two outliers in accent; average drawn as a thin reference line; data labels only on the two outliers; legend removed; gridlines faded; one annotation "Both are pre-2010 plants".
