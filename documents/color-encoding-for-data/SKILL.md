---
name: color-encoding-for-data
description: Applies color to a chart so it encodes meaning and directs attention, using preattentive contrast, sequential and categorical palettes, and accessibility checks.
---

# Color Encoding for Data

## When to use
Use this on any chart once it is built and labeled. Color is the most misused element of a chart. Done well, it makes the message jump out before the reader reads a word. Done badly, it turns a chart into a rainbow that hides the point.

## What it does
It returns a color plan: the base palette, which element gets the accent, the palette type for the data (categorical, sequential, or diverging), and an accessibility check. The plan ties every color to a reason.

## Method
Step 1. Start from one color, add color only to mean something.
The default is a single muted color for all marks. Add a second color only to encode a real distinction: the focus category, increases versus decreases, above versus below target. Color with no meaning is decoration and should be removed.

Step 2. Use preattentive contrast to direct attention.
The eye locks onto the one element that differs in color before conscious reading begins. Exploit this: gray every mark except the one the message names, and give that one the accent color. A single accent bar in a field of gray is read faster than any label.

Step 3. Choose the palette type by data type.
- Categorical data (regions, products): distinct hues of similar saturation, kept to a small set. Reuse the same hue for the same category across all charts in the deck.
- Sequential data (low to high of one measure): a single hue ramping from light to dark. Darker means more.
- Diverging data (below to above a midpoint): two hues meeting at a neutral middle, for example blue to gray to orange around a target. Use only when there is a meaningful midpoint.

Step 4. Limit the number of colors.
Keep categorical palettes to about five or six distinguishable colors. Beyond that, hues blur together. If you have more categories, group them or use position and labels instead of color to distinguish them.

Step 5. Tie colors to the deck brand.
Use the deck's primary and accent colors. The chart should look native to the brand, not like a generic Excel palette. Map the brand primary to the base series and the brand accent to the highlighted element.

Step 6. Keep color consistent across the deck.
If region North is blue on one chart, it is blue on every chart. Consistent encoding lets the reader carry meaning from slide to slide without relearning the legend.

Step 7. Check accessibility and print.
Ensure the palette is distinguishable for color-vision deficiency: do not rely on red versus green alone; pair color with position, labels, or texture. Check that the chart still reads in grayscale, since decks get printed. Maintain enough contrast between marks and background.

Step 8. Build it native in PowerPoint.
Set each series and data point color in the native chart's Format pane using theme colors, so the colors update if the brand theme changes and the chart stays editable.

## Inputs
- The chart and what each color would distinguish.
- The data type (categorical, sequential, diverging).
- The element the message highlights.
- The deck brand primary and accent colors.

## Output format
- The base color and the rule for when a second color appears.
- The accent assignment (which element, why).
- The palette type and the specific palette.
- The cross-deck consistency note.
- The accessibility and grayscale check.

## Example
Input: bar chart of margin by product, eight products, message is that two products drag the average down.

Output:
- Base color: all bars muted brand blue.
- Accent: the two low-margin products in brand accent color; the rest gray-blue.
- Palette type: categorical is not needed here; this is single-measure highlighting.
- Consistency: keep these product colors identical on every chart in the deck.
- Accessibility: the accent is distinguishable in grayscale and paired with direct labels, not color alone.
- Build: set the two highlighted bars' fill to the theme accent in the Format pane.
