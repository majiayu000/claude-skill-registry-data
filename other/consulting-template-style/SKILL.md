---
name: consulting-template-style
description: Use when creating, restyling, or reviewing PowerPoint slides, executive decks, board presentations, charts, tables, dashboards, or analytical pages that should use MBB, McKinsey-informed, Bain-informed, or BCG-informed consulting design grammar. Applies claim titles, house-style typography, restrained palettes, proof-first layouts, chart emphasis, footnotes, and slide-level quality checks without copying proprietary slides or presenting the output as an official firm template.
---

# Consulting Template Style

Apply one coherent consulting visual system to an analytical artifact. Treat the bundled rules as design grammar distilled from reference decks, not as official brand guidelines.

## Reference Loading

Read `references/house-styles.md` before selecting or applying a style.

Read `references/layout-catalog.md` when mapping content to slide archetypes or redesigning a page.

Read `references/style-tokens.json` when exact fonts, colors, slide sizes, and density settings are needed.

Read `references/quality-checklist.md` before delivering a deck or slide.

Read `references/source-analysis.md` when the user asks how the rules were derived or how confident to be in a specific pattern.

## Style Selection

Choose exactly one house style for an artifact unless the user explicitly requests a comparison.

| Style | Choose it for | Primary visual signal |
| --- | --- | --- |
| McKinsey-informed | Executive synthesis, board pages, sparse recommendations | High whitespace, editorial headline, navy/blue proof |
| Bain-informed | Commercial diligence, market analysis, benchmarking, dense chart books | Red top rule, grey analytical base, red answer |
| BCG-informed | Corporate strategy, transformation, process, portfolio, operating model | Green title/rule, structured process, green takeaway |

If the user says only "MBB style," select based on the communication job and state the choice. Do not blend Bain red chrome with BCG green chrome.

## Formatting Workflow

1. Define the communication job.
   - Identify the audience, decision, central takeaway, and evidence.
   - Rewrite topic titles as claims before styling.

2. Audit the source.
   - Inventory slide size, masters, layouts, fonts, colors, charts, tables, footers, and page markers.
   - Preserve a user-supplied deck's native structure when editing it.
   - Identify accidental inconsistency separately from intentional emphasis.

3. Select a house style.
   - Match the style to the deck's purpose and evidence density.
   - Use the style's font and accent consistently.
   - Keep non-answer information neutral.

4. Map each page to an archetype.
   - Use `references/layout-catalog.md`.
   - Give each slide one narrative job and one primary proof object.
   - Prefer a chart, table, matrix, process, map, or decision tree over decorative panels.

5. Apply the hierarchy.
   - Claim title first.
   - Proof object second.
   - Implication or recommendation third.
   - Source, notes, and page number last.

6. Format evidence.
   - Use grey for context and one accent for the answer.
   - Direct-label data when practical.
   - Highlight one comparison, segment, scenario, or path.
   - Remove chart junk, redundant legends, heavy borders, and decorative shadows.

7. Run visual and structural QA.
   - Use `references/quality-checklist.md`.
   - Render every slide and inspect it at full size and thumbnail size.
   - Correct clipping, overlaps, broken hierarchy, inconsistent titles, and unsupported brand claims.

## PowerPoint Execution

When creating or editing a PowerPoint deck, also use the available presentation-authoring skill and its required rendering workflow.

For an existing deck:

- Preserve its slide size unless the user requests conversion.
- Edit inherited placeholders instead of covering them with parallel text boxes.
- Preserve functional masters, layouts, page numbers, and source rails.
- Shorten copy or choose a better layout before shrinking text.

For a new deck:

- Default to 16:9 unless the user needs a source deck's original dimensions.
- Build original slides from the distilled system; do not import logos or proprietary source pages.
- Use authentic client branding only when the user supplies it and has authority to use it.

## Output Contract

For a style recommendation, return:

```markdown
## Selected style
<House style and rationale>

## Page system
- Slide size:
- Title treatment:
- Body typography:
- Accent logic:
- Footer/source treatment:

## Layout map
| Slide | Narrative job | Archetype | Proof object | Emphasis |
| --- | --- | --- | --- | --- |

## Deviations
- <Any intentional departure and reason>
```

For a completed deck, provide the edited file and summarize the selected style, material deviations, and QA result.

## Guardrails

- Do not claim the output is an official McKinsey, Bain, or BCG template.
- Do not publish or redistribute source decks, firm logos, client data, or slide screenshots without explicit permission.
- Do not copy distinctive slide content, wording, charts, or page compositions from a proprietary source.
- Do not mix house styles within one artifact unless the user explicitly requests a comparison.
- Do not use brand color on every object; reserve it for the answer.
- Do not use framework diagrams as decoration or substitute a named framework for analysis.
- Do not omit sources from evidence-heavy pages.
- Do not sacrifice legibility to imitate dense source material.
