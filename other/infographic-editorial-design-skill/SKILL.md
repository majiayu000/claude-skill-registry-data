---
name: infographic-editorial-design
description: Research-led infographic and editorial design system for turning evidence, datasets, archival material, semantic maps, timelines, and source-led arguments into auditable visual pages, posters, dashboards, essays, and web interfaces. Use when Codex needs to design, critique, or implement an infographic, editorial data story, visual essay, source ledger, evidence map, word-history page, research poster, methods page, or information design interface with strong hierarchy, grid discipline, claim boundaries, responsible attribution, and designer-informed visual rules.
---

# Infographic Editorial Design

## Overview

Use this skill to convert research material into an editorial information system: a page, poster, deck, dashboard, or web artifact where the design structure makes the evidence, uncertainty, rights, and interpretive decisions legible.

The reference model is not a single project style. It is a reusable information-design practice: grid discipline, research-led visual hierarchy, restrained typography, explicit source boundaries, and infographic work that treats layout as an argument rather than decoration.

## Quick Start

When a user asks for an infographic/editorial design, first produce or infer these five decisions:

1. Subject: the word, dataset, event, archive, policy, object, or system being explained.
2. Claim: what the artifact is allowed to say.
3. Evidence: source families, data transforms, interpretation layers, and rights limits.
4. Sequence: the reader's path from subject to proof to synthesis.
5. Grid: the structural system that makes comparison, sequence, and absence legible.
6. Style provenance: region/school, historical period, medium, and drawing bias.
7. Form: web page, static poster, presentation, report section, dashboard, or design critique.

If the user asks for code or a design implementation, apply the workflow directly in the target files. If the user asks for strategy, return a compact design spec.

## Core Workflow

1. Identify the claim.
   - State what the artifact can show and what it must not imply.
   - Separate measured data, curated interpretation, contextual evidence, and rights or licensing notes.
   - If the source material is incomplete, design a visible absence instead of filling the gap decoratively.

2. Build the evidence contract.
   - Define the evidence columns or layers before designing visuals.
   - Prefer a compact schema such as: signal, attestation, variant, context, boundary, rights.
   - Attach every visual mark to a source type, transform, confidence label, or editorial decision.

3. Choose the editorial sequence.
   - Start with the subject as the first-viewport signal.
   - Follow with panel progress, entry note, major chart sections, synthesis, source ledger, methods, and boundaries where appropriate.
   - Use section rhythm to make the reader move from assertion to inspection, not from spectacle to footnote.

4. Choose the grid system.
   - Select manuscript, column, modular, baseline, timeline, map/spatial, constellation/network, or evidence-lane grids according to the evidence task.
   - Explain what the grid makes comparable, sequential, separate, or visibly absent.
   - Preserve the grid argument across responsive states.

5. Position the style.
   - Identify the relevant region/school, historical period, medium, and drawing bias before rendering.
   - Use references as method, not costume. Borrow structural logic, not a finished identity.
   - Match style to evidence fit: diagrammatic, cartographic, typographic, technical, pictorial, archival, expressive, or minimal.

6. Design the visual programme.
   - Treat color, type, spacing, grid, and motion as rules.
   - Use color tokens consistently for source families, emphasis, confidence, warnings, and domain branches.
   - Use neutral sans typography when the visual system should carry research rather than personality.
   - Set readable type sizes before adding visual density; source labels and caveats must remain legible.

7. Make interpretation auditable.
   - Label transforms as index, relative signal, visual intensity, rank, or curated grouping.
   - Never let a frequency chart imply cultural importance, universal usage, causation, or legal/clinical meaning unless the sources actually support that claim.
   - Put caveats close to the visual element they qualify.

8. Verify the page as an editorial object.
   - Check hierarchy, source traceability, responsive behavior, text size, text fit, and visual contrast.
   - Confirm that data-dense modules remain readable at rest and become more inspectable through hover, focus, tabs, toggles, or drilldown.
   - Confirm that empty states, sparse data, restricted sources, and pending checks remain visible.

## Task Modes

- New design: define the evidence contract, page spine, visual programme, modules, and verification checklist.
- Redesign: preserve the user's content, then repair hierarchy, evidence traceability, contrast, rhythm, and claim boundaries.
- Critique: lead with problems that affect meaning, proof, accessibility, or comprehension; then suggest concrete changes.
- Implementation: prefer existing local components and tokens. Add new abstractions only when the pattern repeats or removes real complexity.
- Publication packaging: keep the skill generic enough for other projects, and keep project-specific visual identity in external references or examples.

## Design Rules

- Treat legibility as a hard constraint. Body text, captions, chart labels, source labels, and caveats must meet readable size thresholds before the design is considered complete.
- Use a modular grid as an argument. Columns should correspond to evidence categories, comparison groups, or reading lanes.
- State the grid rationale. A reader should be able to understand why elements sit where they sit.
- State the style provenance. The design should know whether it is drawing from Swiss systems, Dutch public information, Japanese dense editorial design, British explanatory graphics, American science communication, or another relevant tradition.
- Keep cards for repeated records, modals, and framed tools. Do not put cards inside cards or style every section as a floating card.
- Use dense but calm editorial hierarchy: large subject title, compact metadata table, monospace eyebrows, strong section titles, and readable body notes.
- Use borders, rules, tables, and small color chips as information-bearing structure.
- Use motion sparingly for reveal, selection, or flow. Motion must clarify relation or state.
- Prefer diagrams that expose data transformation over decorative illustrations.
- Use visual silence deliberately: an empty column, faded lane, dashed rule, or low-opacity record should mean incomplete, unsupported, pending, or secondary.

## Reference Files

Load only the reference needed for the current task:

- `references/design-principles.md` for design lineage, evidence model, color/type logic, and claim boundaries.
- `references/grid-system.md` for grid selection, evidence-lane structure, responsive grid rules, and grid QA.
- `references/legibility-standards.md` for minimum type sizes, line heights, dense-chart label rules, and mobile/print readability checks.
- `references/pattern-library.md` for reusable page patterns, evidence modules, data-led editorial structures, interaction rules, and responsive checks.
- `references/style-positioning.md` for country/school, historical period, medium, and drawing-style bias.
- `references/prompt-recipes.md` for external-user prompt examples.
- `references/evaluation-rubric.md` for reviewing a design before shipping.
- `references/publication-boundaries.md` for attribution, adaptation, and open release boundaries.

## Output Expectations

For design planning tasks, return:

- A concise concept statement.
- The evidence contract and source hierarchy.
- The editorial sequence.
- The grid system and rationale.
- The style positioning brief: region/school, period, medium, drawing bias, and what to avoid.
- The visual system: type, palette, interaction, and data marks.
- Legibility standards for body text, labels, captions, source notes, and responsive states.
- Claim boundaries and caveats.
- A verification checklist.

For critique tasks, return:

- Findings ordered by severity.
- Why each issue affects comprehension, evidence, or editorial integrity.
- Specific fixes for layout, data mapping, copy, interaction, or source labeling.
- Remaining risks after the fixes.

For implementation tasks, edit the local files directly and preserve the host application's existing component style. Prefer local components, design tokens, datasets, and section rhythm before inventing new abstractions.

## Anti-Patterns

- Do not present raw data and curated interpretation with the same visual authority.
- Do not hide uncertainty in footnotes when the chart itself is uncertain.
- Do not turn every research page into a marketing landing page.
- Do not use decorative gradients, abstract blobs, stock-like imagery, or oversized hero composition when the subject is evidence inspection.
- Do not let a chart's beauty exceed its proof.
- Do not shrink evidence text, source notes, caveats, or chart labels below readable thresholds to make a layout fit.
- Do not clone a project-specific visual identity when the task calls for a transferable method.
- Do not strip attribution when a design lineage, method, or provided example materially informs the output.
