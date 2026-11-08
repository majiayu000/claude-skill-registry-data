---
name: canvas
description: Create a durable, self-contained HTML canvas for standalone analyses, structured findings, and data exploration. Use when the artifact itself is the deliverable, not for incidental debugging output or work requested in another tool.
---

# Canvas

A canvas is a standalone visual artifact the user can open outside the conversation, revisit, and share. Produce a self-contained HTML file that works in an ordinary browser without an IDE, proprietary SDK, build step, or server. This workflow applies equally to a primary agent or a subagent assigned to produce the artifact.

## When to use a canvas

Choose based on user intent, not the shape of the response. Use a canvas when new analytical output benefits from being a durable standalone artifact:

- Quantitative analyses, metrics breakdowns, and usage trends.
- Account investigations or cross-system analyses with structured findings.
- Security audits or architecture reviews with categorized findings.
- Large tables the user wants to revisit, filter, or compare.

Do not substitute a canvas for a requested tool or deliverable: a dashboard in another service, a drafted message, a code fix, or a PR. Preserve an existing artifact's format when editing it. Targeted debugging, intermediate tool results, short factual answers, and visuals that belong only in the conversation do not need a canvas.

## Build the artifact

### Location and format

- Honor the user- or parent-agent-specified output path. Otherwise use the project's artifact directory, or `artifacts/canvases/` under the working directory when there is no convention. Create the directory if needed.
- Use a descriptive kebab-case filename ending in `.html`. Avoid overwriting an unrelated artifact; update an existing canvas when that is the task.
- Write the actual file, not just a code block or proposed path.
- Keep each canvas in one HTML file with inline CSS, optional inline JavaScript, and embedded data. Use semantic HTML and inline SVG for charts; no package installation, framework runtime, remote fonts, CDN assets, network calls, or runtime file reads.
- Use native controls for useful interactions such as filtering, sorting, and expanding details. Keep the main findings readable without interaction, and make controls keyboard-accessible with visible labels and focus states.
- Treat embedded source text as data: escape it for its HTML, script, or attribute context. Insert dynamic text with `textContent`, not unsanitized `innerHTML`.

### Content and evidence

Show real content. Omit sections and chart frames with no underlying data; do not fill them with placeholders or invented values. A measured zero is valid data, not an empty state. If all required data is missing, explain what is missing instead of creating an empty canvas. A user-selected filter with no matches can show a concise message and a way to reset it.

Make the artifact understandable without the conversation:

- State the question, principal finding, and relevant limitations.
- Identify sources and time ranges, including timezone when it changes the interpretation. Distinguish observed values, estimates, and assumptions.
- Give each chart a title naming its specific metric, axis labels with units where applicable, and a legend when multiple series appear. Preserve source series names or explicitly explain renamed labels.
- Label transformations such as means, percentiles, normalization, and smoothing. Use table headers that specify units and scope just as clearly as chart labels.
- Include a compact source/time-range caption near each chart or table; shared provenance can sit above a clearly grouped set of visuals.

## Design

Use a flat, restrained composition that serves the content. Give the main finding the strongest visual emphasis and supporting detail less space. Mix open sections, tables, and grouped surfaces instead of wrapping every section in identical cards.

Define a small palette with CSS custom properties for background, surface, text, muted text, borders, and accent. Use neutral colors for most content, accent for emphasis, and consistent semantic colors across charts. Do not rely on color alone to convey meaning.

Avoid decorative gradients, emoji icons, box shadows, rainbow coloring, oversized display text, and decorative colored borders. Honor an explicit user-supplied visual style over these defaults. Keep text readable and contrast sufficient. Check chart labels at their actual rendered size: shrinking an SVG to fit a narrow column also shrinks its text. Reflow charts or use local horizontal scrolling instead of making labels illegible; keep wide tables locally scrollable too.

## Verify and hand off

Before delivery:

1. Check displayed values, units, calculations, and source captions against the supplied evidence. Confirm missing data was not silently treated as zero.
2. Confirm the file is self-contained and does not depend on host APIs or external assets.
3. If browser or preview tools are available, open the saved file, inspect its layout at wide and narrow widths, and exercise any controls. Fix rendering or interaction failures. Otherwise perform a static review and disclose that rendering was not verified.
4. Check visual hierarchy, chart labels, keyboard usability, and absence of placeholder sections.

Completion means the file is saved, its content is checked, and the recipient has its location and validation status. Link the artifact using its absolute file path with a short descriptive label. Say it can be opened in a browser; do not promise a host-specific preview or automatic IDE detection. If a canvas was not explicitly requested, briefly explain why the standalone format helps.

When acting as a subagent, return the absolute artifact path, a concise summary of findings, checks performed, and any unresolved limitations to the parent agent. Do not assume access to the parent's chat UI or that the parent has inspected the file.
