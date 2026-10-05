---
name: render-html-intent
description: Turn a natural-language request, loose product idea, content brief, wireframe description, or UI prompt into a rendered standalone HTML/CSS/JS artifact. Use when Codex should infer the user's intent and produce a browser-viewable HTML page, mockup, dashboard, explainer, report, prototype, landing page, interactive widget, or visual composition from prose rather than editing an existing app.
---

# Render HTML Intent

## Workflow

1. Infer the artifact type from the user's wording: page, app-like tool, dashboard, report, diagram, comparison, form, gallery, timeline, or interactive prototype.
2. Map the intent to a small component plan before writing HTML. For vague or app-like prompts, read `references/json-render-pattern.md` and use the flat UI tree pattern internally.
3. Choose the smallest deliverable that satisfies the intent, but make it rendered and complete: a self-contained `index.html` unless the user explicitly asks for a framework project.
4. If the request is ambiguous, make reasonable product and content assumptions in the output. Stop for clarification only when missing information would make the artifact materially wrong; otherwise represent ambiguity as choices or defaults inside the rendered UI.
5. Use `assets/standalone-template.html` as a starting point when creating a fresh artifact. Replace all placeholders and remove sections that do not fit.
6. Implement semantic HTML, scoped CSS, and small vanilla JS only when interaction is needed. Avoid external build steps for one-off rendered artifacts.
7. Validate the file with `scripts/validate_html_artifact.py <path-to-index.html>`.
8. Render-check the HTML in a browser when possible. For local files, use a `file://` URL or serve the directory if browser restrictions affect behavior.
9. Return the absolute path to the HTML file and, when available, a screenshot or local browser URL.

## Interpretation Rules

- Treat the user's natural language as a product brief, not as literal copy to dump onto the page.
- Preserve explicit requirements first: audience, data, content, tone, layout, colors, components, interactions, dimensions, and output location.
- Invent plausible labels, sample data, and microcopy only where needed to make the rendered result coherent.
- Prefer real interface surfaces over explanatory pages. For example, "budget tracker" should open on the tracker UI, not on a marketing page about trackers.
- Match visual density to the domain. Operational tools should be compact and scannable; editorial pages can be more expressive; technical reports should foreground evidence and hierarchy.
- If the user asks for a single component, render it centered in a realistic viewport with enough context to inspect states.
- For "generate UI from prompt" requests, build the first screen as a two-pane workbench only when that is the product itself: prompt input, generation controls, suggestion chips, preview, debug/status, and code/view toggles.
- For action-command style prompts, model the flow as unified input -> auto-analysis -> clarification or selection -> execution state -> results and feedback.

## HTML Quality Bar

- Include `<!doctype html>`, `<html lang="en">`, charset, viewport, title, and a visible body.
- Keep the artifact self-contained unless the user asks for external assets or a framework.
- Use responsive layout constraints so text and controls do not overlap on mobile or desktop.
- Use accessible names for controls, visible focus states, and sufficient contrast.
- Use stable sizes for fixed-format UI such as boards, grids, counters, cards, controls, and canvases.
- Avoid placeholder text, TODO markers, lorem ipsum, broken image references, and hidden primary content.
- Keep CSS in one `<style>` block for standalone artifacts. Use CSS variables for a small palette.
- Keep JavaScript minimal and defensive. The page should still communicate its purpose if JS fails.

## Resources

- `assets/standalone-template.html`: Copy when starting a new standalone page.
- `references/interpretation-rubric.md`: Read when the prompt is vague or the best artifact type is unclear.
- `references/json-render-pattern.md`: Read when the request resembles prompt-to-UI generation, structured rendering, component catalogs, or the json-render playground pattern.
- `scripts/validate_html_artifact.py`: Run before returning a generated HTML file.
