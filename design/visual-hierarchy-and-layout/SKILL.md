---
name: visual-hierarchy-and-layout
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P028
  - P053
  - P056
  - P058
  - P061
  - P074
  - P099
  - P100
  - P102
  - P110
  claims:
  - C00023
  - C00024
  - C00047
  - C00048
  - C01332
  - C01333
  - C00594
  - C00595
  - C00631
  - C00632
  - C00733
  - C00737
  - C01341
  - C01342
  - C00385
  - C00386
  - C00390
  - C00391
  - C01355
  - C01356
  - C01363
  - C01364
  authored_from_digest: 284a013f0d25b872226f53302881cfd0e9701714cac2cfebe73515900aaaece8
---

# Visual Hierarchy and Layout

Rank and group elements so the interface communicates what matters at a glance.

## When this applies

- Multiple UI elements compete for attention or the page feels noisy (P001).
- A large viewport or canvas tempts the design to widen forms, text, or sections unnecessarily (P028).
- Encoding information and importance in a visual layout (P053).
- Choosing an organizational model and encoding for data (P056).

## Procedure

Apply these principles to the situation under review; for each, name the user goal at stake and the trade-off the choice carries.

1. Establish a clear visual hierarchy by ranking controls and data from scenarios into instantly-needed, secondary, and by-exception, then distinguishing levels with hue, saturation, value, size, and position so the most important elements are larger and higher-contrast; adjust with restraint (often one property suffices, and prefer turning the less-important element down over turning the important one up), knowing a good hierarchy goes unnoticed while its absence causes glaring confusion. (P001)
2. Size content and sections to their optimal width instead of stretching them just because space exists; use grids as aids and prefer fixed or max-width sizing where content has a natural width. (P028)
3. Convey meaning through the similarity and contrast of visual properties — users assume objects sharing properties are related and attend to the item of greatest contrast — choosing the property deliberately: size reads automatically as a hierarchy of importance and draws attention, shape best signals what an object is but is costly to attend to, hue must be used with a limited palette (never as the sole vector, given color-blindness), and texture is weak for differentiation but a strong affordance cue. (P053)
4. Choose the data's shape from its inherent structure and encode classes and dimensions with preattentive variables (color, size, position, shape) and layering, because preattentive features are found in near-constant time while reading text is linear. (P056)
5. Give a form strong vertical flow (aligned inputs, consistent spacing, top-aligned labels for responsive designs), group long forms into titled sections or show/hide sequences, and use descriptive labels and help while avoiding placeholder text that looks pre-filled. (P058)
6. Organize questions into meaningful visual groups using the minimum visual information needed—excess contrast and non-functional elements create noise that impedes scanning—and use initial capitals for group titles. (P061)
7. Group, align, and lay out with structure: group related elements by proximity and whitespace rather than heavy bounding boxes, align every element with as many others as possible on a modular grid whose spacing is multiples of one atomic unit, structure an efficient top-to-bottom left-to-right path for the eye with balanced visual weight, and use the squint test to reveal hierarchy, grouping, and balance problems. (P074)
8. Control perceived importance with size, position, color, contrast, density, and rhythm; make small but important items stand out by placement (top, left, upper-right), contrast, and whitespace, remembering sought controls stand out by meaning. (P099)
9. Apply the Gestalt principles deliberately: proximity and similarity to group related items (and isolate distinct ones), continuity and closure to imply relationships through alignment, applying uniform treatment only to genuinely comparable things. (P100)
10. Pursue visual simplicity and eliminate noise: avoid over-dimensional elements, heavy separators, insufficient whitespace, and overuse of color, texture, and contrast; use simple geometric forms, a restricted mostly-neutral palette with a few high-contrast accents, and one or two typefaces at a few sizes; treat unnecessary variation as the enemy by making near-equal sizes exactly equal and justifying every visual difference; and test each element's contribution by removing things until the design breaks, then restoring the last one. (P102)
11. Follow information-design principles for data displays: enforce visual comparisons, show causality and multiple variables, integrate text/graphics/data in one display, show states adjacent in space rather than stacked in time, and never de-quantify quantifiable data (show the actual numbers alongside trend graphics); above all ensure the quality, relevance, and integrity of shown content, and do not display information merely because it is technically possible, because poor-quality information damages user trust. (P110)

## Principles applied

- **P001** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P028** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P053** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P056** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P058** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P061** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P074** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P099** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P100** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P102** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P110** (high) — grounded in claims/evidence and chunk anchors in `sources/`.

## Provenance

Grounded in principles P001, P028, P053, P056, P058, P061, P074, P099, P100, P102, P110, their backing claims and evidence records, and paragraph-level source anchors under `sources/anchors/`. Every cited id resolves into this package's distilled spine; see `provenance-ledger.md` and `reports/faithfulness-report.yaml`.
