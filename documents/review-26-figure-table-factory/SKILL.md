---
name: review-26-figure-table-factory
description: Build high-quality flowcharts, pathway/workflow SVG diagrams, BioRender/Figma redraw plans, graphical abstracts, and Excel-ready evidence tables for medical SCI reviews. Use when planning figures and tables, generating editable SVGs, preparing BioRender or Figma instructions, adapting published figures, making Excel tables, or linking figure/table content to references. Mechanism diagrams are disabled by default unless the user explicitly requests one.
---

# Review 26 Figure Table Factory

## Overview

Use this skill after the manuscript outline and evidence matrix exist. The goal is to turn evidence into review-grade figures and tables without adding unsupported mechanisms or copying published artwork improperly. For this workbench, default diagrams are flowcharts, pathway maps, workflows, evidence frameworks, decision trees, PRISMA-style flow diagrams, and graphical abstracts. Do not create molecular/cellular mechanism diagrams unless explicitly requested by the user in the current turn.

For Chinese users, discuss plans in Chinese. Keep labels, figure panel names, and final figure text in English when the target manuscript is English.

## Relationship To Other Skills

- Use `review-13-figure-table-planner` for the initial figure/table plan.
- Use this skill for production: SVG, BioRender blueprint, Figma edit plan, Excel sheets, table formatting, figure legends, and source tracing.
- Use `svg-tech-diagram` for editable SVG generation.
- Use `review-23-reference-curator` for references behind each panel or table row.
- Use `review-17-citation-audit` before submission.

## Recommended Review Package

For a full medical SCI narrative review, aim for:

- 4-6 figures.
- 2-3 tables.
- 1 graphical abstract if the target journal benefits from it.
- 1 supplementary evidence table when the main tables become crowded.

Suggested figure types:

1. Field landscape or timeline.
2. Pathway map or workflow figure.
3. Clinical or translational workflow.
4. Bioinformatics or multi-omics pipeline.
5. Therapeutic/diagnostic strategy map.
6. Future directions or integrated model.

Suggested table types:

1. Key studies/evidence matrix.
2. Pathways, biomarkers, diagnostic strategies, or clinical applications comparison.
3. Optional table for datasets, tools, or trials.

## Figure Production Modes

### Original SVG

Use when the figure is conceptual, workflow-based, pathway-based, or evidence-framework-based and can be created from text evidence.

Requirements:

- Use editable SVG elements, not raster images.
- Keep all labels as text elements.
- Use arrows for sequence, referral, decision, evidence flow, feedback, or dependency. Do not use activation/inhibition arrows for molecular mechanisms unless the user explicitly requested a mechanism diagram and the evidence matrix supports each relation.
- Keep a source reference for every panel.

### BioRender Redraw Plan

Use when the user wants BioRender-style biomedical visuals.

Because direct BioRender API access is usually unavailable, produce:

- figure purpose
- panel layout
- element list
- BioRender search terms
- labels
- arrow relationships
- color code
- source references
- redraw notes

Then the user can redraw or polish in BioRender.

### Figma Edit Plan

Use when SVG needs polishing, layout adjustment, or social/video conversion.

Prepare:

- SVG file path
- layer names
- font and color rules
- panel spacing
- export targets: SVG, PDF, PNG, TIFF if needed

### Adapted Published Figure

Use only when the source figure is necessary.

Requirements:

- Cite the source.
- Mark whether it is reused, adapted, or redrawn from scratch.
- Check permission requirements.
- Prefer original redraw based on concepts rather than direct copying.

## Table Production

Prefer Excel-compatible outputs:

- `.xlsx` for editable tables and multi-sheet workbooks.
- `.csv` for simple import/export.
- Markdown table only for small previews.

Recommended workbook sheets:

- `evidence_matrix`
- `included_studies`
- `figure_sources`
- `table_sources`
- `citation_audit`
- `pdf_status`
- `journal_requirements`

Table rules:

- Use three-line table style for manuscript display.
- No vertical lines.
- Units in headers, not repeated in cells.
- Keep one concept per column.
- Include PMID/DOI or reference number for every evidence row.
- Do not extract numbers from papers without full text.

## Quality Gates

Before a figure or table is considered ready:

- Every panel or row has a source.
- Every source has DOI/PMID or documented exception.
- Figure labels match manuscript terminology.
- No unverified mechanism is drawn as established fact; in the default workbench, mechanism diagrams are not produced unless explicitly requested.
- Permissions or redraw status are recorded.
- Captions state what the figure/table shows without overclaiming.
- Excel values, units, and references are internally consistent.

## Output Format

Return:

1. Figure/table inventory.
2. Recommended production mode for each item.
3. Source and permission table.
4. SVG/BioRender/Figma prompt or blueprint.
5. Excel workbook schema or table draft.
6. Risk list before final submission.

## Reference File

Read `references/figure-table-gates.md` when producing figures, tables, SVG diagrams, BioRender prompts, Figma edit plans, or Excel evidence matrices.
