---
name: data-ink-reducer
description: Strips non-data ink from charts and slides using the data-ink ratio principle, so the remaining marks all carry meaning and the slide reads cleaner.
---

# Data-Ink Reducer

## When to use
Use this when a chart or slide looks busy, heavy, or cluttered without being more informative. Use it on inherited templates loaded with gridlines, borders, fills, and shadows. Use it as the last pass on any exhibit before review.

## What it does
It removes every mark that does not carry information, raising the share of ink that actually represents data. The result is lighter, faster to read, and more credible, because nothing distracts from the numbers.

## Method
The data-ink ratio is the proportion of a graphic's ink devoted to data rather than decoration. The goal is to maximize it without erasing useful context.

1. Inventory the ink. List every visual element on the exhibit: bars, lines, gridlines, borders, fills, shadows, legends, axis titles, tick marks, background, icons. Mark each as data ink (represents a value) or non-data ink (decoration or redundant structure).

2. Erase non-data ink first. Remove drop shadows, 3D effects, gradient fills, heavy borders, and background fills. These never carry information and always add visual weight.

3. Erase redundant data ink. If the same value is shown twice, keep one. A bar already shows magnitude, so the axis can be light and the data label can replace gridlines. Choose either gridlines or data labels, rarely both.

4. Lighten what remains. Fade gridlines to a faint tone or remove them. Thin the axis lines. Reduce tick marks to the few the reader needs. Use a single muted palette plus one accent.

5. Cut decimal noise. Round numbers to the precision that matters. "12 percent" beats "12.3847 percent" on a slide.

6. Replace legends with direct labels. A legend forces a lookup. Label series in place.

7. Reduce, do not amputate. Keep the reference line, the one annotation, and the labels that carry the message. The goal is clarity, not minimalism for its own sake. An exhibit that is too bare loses the comparison the reader needs.

8. Compare before and after. Hold the cleaned version against the original. The point should now be faster to find. If anything got harder to read, restore that element.

## Inputs
- The chart or slide to clean.
- The message the exhibit must preserve.

## Output format
Return two lists: ink to remove (with why), and ink to lighten or keep (with why). Then return a one-line statement of what the cleaned exhibit now lets the reader see faster. Note any element that must stay despite looking like decoration.

## Example
Original: column chart with dark gridlines, gray plot background, blue gradient bars, drop shadow, legend, axis titles on both axes.
Remove: gridlines, plot background, gradient, shadow, redundant y-axis title.
Lighten: keep one faint reference line, replace legend with direct labels, round labels to whole numbers.
Result: the reader sees the rising trend and the one outlier immediately, with no decoration competing for attention.
