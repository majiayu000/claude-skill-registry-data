---
name: icaire-reportify
description: Turn ICAIRE evidence and source material into audience-fit reports and visually integrated PDF deliverables. Use when preparing analyses, executive updates, decision briefs, operational handoffs, partner reports, policy briefs, or missing-information reports.
---

# ICAIRE Reportify

Design and render an evidence-led ICAIRE report whose structure follows the reader's decision, not a fixed template.

## Contract Checklist

- Identify the audience, reporting period, decision need, and confidentiality before choosing a structure.
- Choose a report archetype as a starting point, then change it when the evidence requires a different reading order.
- Separate confirmed facts from assumptions, inference, causal claims, risks, and open questions.
- Place every useful visualization next to the claim it supports, with an analytical caption.
- Treat figures the user identifies as essential as required report content.
- Prefer the ordered-block JSON model for new reports; preserve legacy JSON only when maintaining an existing report.
- Render a polished PDF, inspect the first page plus every dense or figure page, and fix clipping, illegibility, or orphaned captions.
- Use the ICAIRE green `#4A9549` and local untracked ICAIRE/UNESCO lockups when available.
- End with specific source limits or missing information when the evidence is incomplete.

## Workflow

1. Define the report job:
   - capture audience, period, confidentiality, decision or update need, expected depth, and required deliverables
   - select an initial archetype: `analysis`, `executive_update`, `decision_brief`, `operational_handoff`, `external_brief`, or `custom`
   - treat the archetype as a design prompt, not a mandatory section list
   - Anti-patterns: defaulting every report to executive summary and risks, choosing structure before the decision need, treating an archetype as a locked template
2. Gather and verify evidence:
   - use material supplied by the user, then BigBrain or the ICAIRE connector when ICAIRE facts, meetings, initiatives, or prior language are missing
   - extract claims, metrics, uncertainty, milestones, decisions, risks, dependencies, asks, and source limits
   - distinguish operational source data from dashboard summaries and retrieve the authoritative record when feasible
   - Anti-patterns: inventing KPI values or approvals, treating a dashboard as ground truth without reconciliation, hiding source gaps
3. Select the story and visual evidence:
   - decide the smallest set of claims the reader must understand
   - choose tables or figures only when they materially clarify a comparison, sequence, distribution, uncertainty, or decision
   - place each figure immediately after the claim or question it answers
   - write captions that state the takeaway, measure, window, and important uncertainty rather than merely naming the chart
   - Anti-patterns: adding decorative charts, putting all figures in an appendix by default, separating a figure from its interpretation, omitting a user-required visualization
4. Storyboard ordered blocks:
   - arrange headings, paragraphs, bullets, figures, tables, callouts, rules, spacers, and page breaks in reader order
   - use callouts for a central finding, risk, decision, or causal boundary
   - allow a figure to lead a section when it is the clearest entry point
   - Anti-patterns: translating evidence into the legacy schema before storyboarding, forcing empty sections, duplicating the same claim across summary and body
5. Draft with calibrated status language:
   - explain what changed, why it matters, what remains uncertain, and what action follows
   - use effect sizes and uncertainty for analytical claims when the data supports them
   - call observed post-treatment movement an association or post-intervention progression unless a valid comparison identifies causal lift
   - Anti-patterns: implying causality without a control, burying material risks, using external-facing certainty for internal unknowns
6. Encode the preferred ordered-block JSON:
   - keep `title`, `audience`, `period`, and classification metadata at the top level
   - set `schema_version: 2`, an optional `archetype`, optional `highlights`, and an ordered `blocks` array
   - use relative figure paths when the images travel with the report JSON; they resolve from the JSON file directory
   - if `blocks` is present it is authoritative; do not also populate legacy body fields
   - Anti-patterns: mixing ordered blocks with legacy sections, using unresolved image paths, shrinking figures below legibility to avoid a page break
7. Render and inspect:
   - run `python3 scripts/render_report_pdf.py report.json report.pdf`
   - use the Codex bundled Python runtime when local ReportLab is unavailable
   - render pages to PNG with Poppler when available
   - inspect the first page, every figure page, and dense pages for image scale, caption proximity, page breaks, spacing, clipping, and legibility
   - Anti-patterns: delivering without opening the PDF, checking only the first page, accepting an orphaned caption or distorted figure
8. Verify and deliver:
   - reconcile headline values with the source data and confirm sensitive claims are supported
   - verify every required figure appears in the final PDF at readable size
   - report the PDF path, included figures, concise findings, source limits, and visual-verification result
   - Anti-patterns: claiming final when evidence is incomplete, reporting a source image as included without checking the PDF, omitting remaining decision gaps

## Preferred JSON v2

Ordered blocks provide the report's reading order:

```json
{
  "schema_version": 2,
  "archetype": "analysis",
  "title": "Applied Ethical AI Quiz Reminder Experiment",
  "audience": "ICAIRE Educate leadership",
  "period": "First 24 hours",
  "classification": "Internal",
  "prepared_for": "ICAIRE Educate",
  "prepared_by": "ICAIRE",
  "highlights": [
    {"label": "Progressed", "value": "49 (12.9%)"}
  ],
  "blocks": [
    {"type": "heading", "text": "What happened", "level": 2},
    {"type": "paragraph", "text": "A concise evidence-grounded finding."},
    {
      "type": "figure",
      "path": "stage-conversion.png",
      "caption": "Figure 1. Progression was highest among learners already near completion; lines show 95% intervals.",
      "width_mm": 160,
      "max_height_mm": 180,
      "page_break_before": false,
      "keep_with_caption": true
    },
    {
      "type": "table",
      "headers": ["Stage", "Delivered", "Progressed"],
      "rows": [["0 passed", "297", "7.4%"]],
      "column_widths_mm": [70, 40, 53]
    },
    {
      "type": "callout",
      "tone": "teal",
      "heading": "Causal boundary",
      "body": "This is observed progression, not incremental lift."
    },
    {"type": "page_break"},
    {"type": "bullets", "items": ["Decision or next action."]},
    {"type": "rule"},
    {"type": "spacer", "height_mm": 4}
  ]
}
```

Supported ordered block types are `heading`, `paragraph`, `bullets`, `figure`, `table`, `callout`, `page_break`, `rule`, and `spacer`. Figure paths may be absolute or relative to the report JSON. Images preserve aspect ratio and scale down to the requested maximum; they are never cropped.

## Legacy v1 Compatibility

When `blocks` is absent, the renderer continues to accept `executive_summary`, `sections`, `risks`, `decisions_needed`, `missing_information`, `assumptions`, and `sources` in the established order. Use this only for existing reports that depend on that structure.

## Brand And Rendering

- Primary accent: `#4A9549`.
- Optional untracked lockups:
  - `assets/brand/report/icaire-lockup.png`
  - `assets/brand/report/unesco-lockup.png`
- Render command:

```sh
python3 scripts/render_report_pdf.py report.json report.pdf
```

- Visual inspection when Poppler is available:

```sh
pdftoppm -png report.pdf report-page
```

## Anti-Patterns

- Using the same Executive Summary, Risks, Decisions, and Missing Information sequence for every report.
- Treating report structure as data entry rather than information design.
- Placing all visualizations at the end when they explain earlier claims.
- Omitting a user-required figure or replacing it with prose.
- Mixing legacy body fields with ordered blocks and duplicating content.
- Distorting, cropping, or over-shrinking a figure.
- Inventing facts, dates, owners, approvals, partner positions, or KPI values.
- Hiding causal, measurement, or data-quality limitations.
- Delivering a PDF without visual verification.

## Output

Return:

- the final PDF path;
- a concise findings summary appropriate to the audience;
- the captions or names of figures included in the PDF;
- source, causal, and missing-information limits;
- confirmation that the first, figure, and dense pages were visually inspected;
- any remaining blocker or deliberate omission.
