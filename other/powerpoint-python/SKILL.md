---
name: powerpoint-python
description: >-
  Use for writing, reviewing, debugging, testing, or optimizing Python code
  that inspects, edits, extracts, validates, preserves, or generates Microsoft
  PowerPoint Open XML presentations, primarily .pptx, using python-pptx,
  PresentationML/OOXML, Pillow, or supporting Python libraries. Trigger on
  slides, masters, layouts, placeholders, shapes, text, pictures, tables,
  charts, notes, themes, hyperlinks, embedded objects, macros, preservation,
  geometry, rendering verification, and presentation package inspection. Do
  not use for .ppt binary files, PowerPoint UI automation, VBA execution,
  slideshow execution, or presentation advice with no Python or file boundary.
argument-hint: "[presentation task, template/preservation requirements, and output contract]"
---

# PowerPoint Python

Engineer a presentation as a semantic and visual artifact built on a multipart
PresentationML package. A file that saves and reopens can still be visually
wrong or can have lost required unsupported behavior.

## Boundary

Use python-pptx for supported `.pptx` creation, inspection, and minimal editing.
Use ZIP/XML inspection for package and preservation risk. Treat `.pptm` as
inspection-first and preservation-sensitive. This skill never executes VBA,
actions, media, linked programs, add-ins, or OLE objects.

Stop and require an authorized PowerPoint-runtime path for `.ppt`, native
open/save or PDF export, native rendering, font-substitution diagnostics,
animations/transitions whose behavior matters, media playback, accessibility
checker evidence, macro execution, add-ins, UI automation, or exact unsupported
feature copying. Read [boundaries and routing](references/boundaries.md).

## Choose the implementation from the operation

| Intent | Mechanism | Gate |
|---|---|---|
| Create ordinary deck | python-pptx | Use a verified template contract. |
| Populate approved template | python-pptx placeholders | Resolve layout and placeholder identity first. |
| Inspect semantics | python-pptx plus package inventory | Unsupported parts require ZIP/XML evidence. |
| Edit existing content | Smallest supported python-pptx mutation | Preflight and semantic diff are mandatory when preservation matters. |
| Change unsupported OOXML | Narrow tested lxml helper | Stop unless exact part ownership and preservation can be proven. |
| Render or execute behavior | External renderer or PowerPoint runtime | python-pptx is not a renderer or application runtime. |
| Calculate metrics | Domain/data layer | Pass resolved content to the renderer. |
| Complex analytical chart | Approved plot renderer to image | Use native chart only when editability is contractual. |

Inspect installed versions and required signatures with `python
scripts/inspect_powerpoint_env.py`; read [API grounding](references/api-grounding.md).

## Ordered workflow

1. Recover the presentation contract: audience, objective, decision/takeaway,
   source/provenance, slide roles and order, template, aspect ratio, editable
   versus static elements, notes, fonts, accessibility, preservation, renderer,
   visual QA, destination, and delivery evidence.
2. For an existing file, preserve the source and run `python
   scripts/inspect_presentation.py SOURCE`. Inventory macros, timing,
   transitions, SmartArt/diagrams, comments, external links, actions, OLE,
   embeddings, unusual media, custom XML, notes, and unknown parts before save.
3. Run `python scripts/inspect_template.py TEMPLATE`. Resolve layouts by
   discovered semantic name and verified placeholder `idx`, type, and geometry;
   never assume a layout or placeholder position.
4. Resolve analysis and content into typed objects, then build a semantic
   `DeckSpec`-like model. Low-level shape calls consume that model; they do not
   invent narrative or business calculations. Read [presentation
   contracts](references/presentation-contract.md).
5. Render from the approved template using its masters, layouts, placeholders,
   theme, and typography. A generic bundled template is allowed only when the
   request explicitly permits a generic blank presentation.
6. Save to a temporary sibling, never over the source by default. Reopen the
   output independently.
7. Run `python scripts/validate_presentation.py OUTPUT --contract CONTRACT.json`
   when a machine contract exists. For edits, also run `python
   scripts/diff_presentations.py BEFORE AFTER` and explain every difference.
8. If a renderer is available, render every consequential slide and perform
   visual QA. If fidelity is mandatory and no acceptable renderer exists, stop.
9. Report only evidence actually established: `GENERATED`, `REOPENED`,
   `PACKAGE_VALIDATED`, `SEMANTICS_VALIDATED`, `PRESERVATION_VALIDATED`,
   `RENDERED`, `VISUAL_QA_PASSED`, `POWERPOINT_NATIVE_OPENED`,
   `POWERPOINT_NATIVE_RENDERED`, and `ACCESSIBILITY_CHECKED`.

## Template, geometry, and text invariants

- Prefer template-native placeholders over freeform shapes. A slide inherits
  from a layout, which inherits from a master; placeholder `idx` connects the
  slide placeholder to its layout definition. Read [templates, layouts, and
  placeholders](references/templates-layouts-placeholders.md).
- Derive slide dimensions. Centralize `Point`, `Size`, `Rect`, margins, grid,
  gaps, split, alignment, distribution, containment, and intersection helpers.
  Reject negative/zero geometry, off-slide content, accidental overlap,
  title/body/footer collisions, distorted images, and unexplained alignment or
  layering drift. Mark intentional overlap explicitly. Read [geometry and
  layout](references/geometry-layout.md).
- Preserve text formatting at the narrowest paragraph/run level. Do not use
  `shape.text = ...` when it would destroy meaningful formatting. Inherit theme
  typography; do not hard-code fonts everywhere. Treat overflow as a content or
  layout failure: shorten, split, or restructure before using `fit_text()` and
  never shrink below the presentation contract. Read [text and
  typography](references/text-typography.md).
- Treat fonts available locally, font references inspected, and PowerPoint
  substitution checked as different states. Local rendering with a corporate
  font does not prove recipient fidelity.

## Content objects

- Images require semantic role, source, target rectangle, `fit`/`fill`/`contain`/
  `cover` crop policy, resolution policy, and accessibility intent. Never
  stretch by supplying arbitrary width and height. Read [images](references/images.md).
- Use native charts when recipients must edit data; otherwise prefer an
  externally rendered image for exact analytical layout. Chart inputs, order,
  units, number formats, axes, labels, and embedded workbook are contractual.
  Read [charts](references/charts.md).
- Tables communicate a bounded comparison, not arbitrary dataframes. Aggregate
  elsewhere, make units explicit, align numbers, distinguish totals, and keep
  pagination widths identical. Read [tables](references/tables.md).
- Preserve notes and inspect hyperlinks, actions, relationships, media, and
  embedded objects without following or activating them. Read [notes, links,
  and media](references/notes-links-media.md) and [security](references/security.md).

## Existing-presentation preservation

Mutate the smallest supported region and save to a new destination. Directly
inspect parts and relationships for masters/layouts/themes, notes, charts,
embeddings, media, comments/people/tags, diagrams, timing/transitions, VBA,
custom XML, properties, and unknown relationships. Unknown or required
unsupported content blocks a blind round-trip. Read [OOXML preservation](references/ooxml-preservation.md)
and [existing presentations](references/existing-presentations.md).

For `.pptm`, detect the macro-enabled content type and `vbaProject.bin`, hash it
before and after, preserve the macro-enabled format, and never execute it.
Report `VBA_PRESENT`, `VBA_HASH_VERIFIED`, or
`VBA_PRESERVATION_UNVERIFIED`; never report `VBA_EXECUTED`.

Do not copy slides between presentations by cloning slide XML. Slides own
relationships to layouts, media, charts, notes, workbooks, links, and diagrams.
Reconstruct supported semantic content in the destination or use an authorized
PowerPoint-native operation when exact copying is required.

## Accessibility and rendering evidence

Use meaningful unique titles, logical object creation/order, alt text for
meaningful visuals, decorative classification where supported, understandable
links, simple tables, adequate contrast, and non-color-only encoding. A narrow
tested OOXML helper is allowed when the public API cannot express a required
property. Never claim Microsoft's checker passed unless it ran. Read
[accessibility](references/accessibility.md).

After rendering, inspect clipping, overflow, minimum font size, overlap,
canvas bounds, image distortion, alignment/margins, wrapping, orphan labels,
chart labels/legends, hierarchy, footnotes/footers, title placement, fonts, and
blank space. Visual diffs diagnose regression but do not prove semantic
equivalence. Read [rendering and visual QA](references/rendering-visual-qa.md).

## Completion

Do not declare a consequential task complete until the correct template and
dimensions were used; layout/placeholder identity is proven; slide roles,
titles, order, notes, charts/tables, images, geometry, and active-content policy
match the contract; the source remains intact; required package parts and hashes
survive; the output reopens; structural and semantic checks pass; rendering and
visual status are explicit; and project tests pass or skipped checks and their
consequences are reported. Read [validation and testing](references/validation-testing.md),
[performance](references/performance.md), and [evaluated recipes](references/recipes-core.md).

## Runtime helpers

- [Inspect environment](scripts/inspect_powerpoint_env.py)
- [Inspect template](scripts/inspect_template.py)
- [Inspect presentation](scripts/inspect_presentation.py)
- [Validate presentation](scripts/validate_presentation.py)
- [Diff presentations](scripts/diff_presentations.py)
