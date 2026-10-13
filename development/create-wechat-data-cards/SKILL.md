---
name: create-wechat-data-cards
description: Create precise, branded Chinese data cards for WeChat Official Account articles. Use when turning agricultural, commodity, trade, USDA, EIA, price, stocks-to-use, policy, scenario, or other quantitative evidence into mobile-readable portrait PNG cards; revising an existing card; matching the Ag Commodity Research visual identity; or preparing ordered article figures with verified units, sources, forecasts, and calculations.
---

# Create WeChat Data Cards

Create reproducible chart cards with code so numbers, Chinese text, units, and labels remain exact. Use image generation only for decorative imagery, never for analytical charts or text-heavy cards.

## Workflow

1. Inspect the article, source data, existing cards, and requested narrative before designing.
2. Verify every displayed value, unit, period, denominator, growth rate, and forecast status. Recalculate derived figures independently.
3. Read [visual-system.md](references/visual-system.md) and [chart-selection.md](references/chart-selection.md).
4. Choose one claim per card. Put the answer or tension near the top, then use the chart as evidence.
5. Build the card with Python/Pillow, matplotlib, or another deterministic renderer. Reuse [card_framework.py](scripts/card_framework.py) for the canvas, typography, logo, panels, and footer.
6. Export a PNG plus the source script and input data/spec used to generate it.
7. Inspect the PNG at original resolution. Iterate until all text, labels, lines, and sources are legible on a phone.

## Data and Narrative Rules

- Preserve official statistical categories. Split a category only when a source supports the split and label any author estimate explicitly.
- Distinguish levels from increments. Write “占预测增量的9.4%”, not “占需求的9.4%”, when the denominator is a year-over-year increase.
- Distinguish historical values, current estimates, official forecasts, and author scenarios with labels, color, line style, or notes.
- Do not visually imply that announced capacity is already operating. Show the commissioning date and avoid highlighting a near-term forecast increment when production begins later.
- Avoid false precision. Match decimal places to source quality and the analytical purpose.
- State the source organization, dataset/report, data vintage, and unit on every card.
- When a claim depends on a model, disclose the sample, equation or method, fit statistic when useful, and that the result is not an official forecast.

## Required Visual Standard

- Default to a 1080 px wide portrait card. Use 1080×1360 or 1080×1440 for most analytical cards.
- Keep a warm neutral outer background and an off-white rounded inner card.
- Place the transparent Ag Commodity Research logo at the upper right without a white rectangle. Use `assets/ag-commodity-logo-transparent.png`.
- Use dark green for the main conclusion, gold for benchmarks or highlights, orange for downside/risk, and gray for secondary text.
- Use Chinese fonts with reliable CJK coverage. On Windows prefer Microsoft YaHei; otherwise use Noto Sans CJK.
- Minimum practical sizes at 1080 px width: title 40 px, section heading 27 px, body 19 px, axes 16 px, and source 14 px. Increase them when labels are dense.
- Keep the top area compact. Do not leave large blank space between the subtitle and the first analytical panel.
- Limit legends and labels. Direct-label important series and emphasize only the number that advances the narrative.
- Make cards usable independently of the article: include a clear title, unit, time period, and source.

## Chart QA

- Check that axes begin at a defensible value and that dual axes are clearly labeled and color-matched.
- Check stacked totals, percentage denominators, sign direction, chronological ordering, and whether marketing years are written consistently.
- Check that labels do not overlap points, lines, plot boundaries, the logo, or one another.
- Check forecast transitions and scenario shading in the legend and the footnote.
- Check the final rendered file with an image viewer at original resolution; code review alone is insufficient.

## Output Convention

Store final files in a topic-specific output folder and number them in article order: `01_结论短语.png`, `02_结论短语.png`, and so on.

Keep the final PNG, task-local rendering script, and source data/spec together. If the user also asks for an article package, hand the ordered PNGs to `$create-wechat-publish-package`.