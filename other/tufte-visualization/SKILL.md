---
name: tufte-visualization
description: Use as an evidence-design overlay to create, revise, or critique charts, dashboards, analytical figures, visual tables, maps, KPI displays, evidence-rich diagrams, and decision-grade reports. Governs truthful comparison, uncertainty, documentation, restraint, accessibility, and rendered QA while medium-specific skills own implementation mechanics. Do not use for generic frontend or marketing design, decorative graphics, analysis without visual output, or diagrams without an evidentiary claim.
---

# Tufte Visualization

Design evidence displays that help a capable reader compare, question, verify,
and think. Preserve data resolution and useful context; remove decoration that
competes with them. This is a Tufte-inspired reasoning standard, not a recipe
for imitating a recognizable Tufte aesthetic.

Derive principles. Do not copy protected book pages, proprietary examples, or
another designer's finished visual artifact.

## Stable Requirements

- **EV-01 Metric contract**: Preserve the metric definition, unit, grain,
  population, numerator, denominator, and time window that materially govern
  interpretation.
- **EV-02 Named comparison**: Name the comparator, why it is valid, and the
  conclusion the comparison can support.
- **EV-03 Magnitude**: When base effects matter, show the base values and
  absolute delta as well as relative change. Distinguish percent change from
  percentage-point change and statistical detectability from practical or
  decision significance.
- **EV-04 Evidence status**: Distinguish observed, estimated, modeled,
  forecast, scenario, imputed, and causally identified quantities.
- **EV-05 Qualification**: Preserve material uncertainty, missingness,
  selection, exclusions, sensitivity, data freshness, and partial or
  provisional periods.
- **EV-06 Default-view integrity**: Keep interpretation-critical evidence out
  of hover-only, narration-only, or export-excluded states.
- **QA-01 Final artifact**: Inspect the exact artifact at delivery size.
- **QA-02 Required states**: Inspect every required viewport, analytical
  state, sibling composition, and export.
- **QA-03 Repair loop**: Re-render and re-inspect after every visible-defect
  repair.
- **QA-04 Equivalent state**: Verify that captions, text equivalents, copied
  links, screenshots, and static exports describe the same analytical state.
- **STOP-01 Causality**: Do not imply unsupported causality.
- **STOP-02 Comparability**: Do not encode incompatible definitions,
  populations, periods, denominators, units, or aggregation levels as though
  they were comparable.
- **STOP-03 Completion grade**: Do not claim a completion grade whose gates
  were not demonstrated.

## Evidence Display Contract

Before implementing a non-trivial display, record this compact contract. It may
remain internal for routine work; include it in the handoff for decision-grade
or publication-grade work.

```text
Mode: exploratory | explanatory | operational | reference
Reader: audience, viewing distance, ambient conditions, expected reading time, decision or action
Question or supported claim: one sentence
Unit of analysis: meaning of one row, point, line, interval, area, or node
Metric: definition, unit, numerator, denominator, population, grain, time window
Comparison: comparator, validity, supported conclusion
Magnitude: base values, absolute delta, relative delta, threshold significance
Scale: baseline, domain, indexing, normalization, smoothing, aggregation
Evidence status: observed | estimated | modeled | forecast | scenario | imputed
Qualification: uncertainty, exclusions, gaps, sensitivity, missingness
State: filters, data vintage, update lag, partial or provisional periods
Delivery: medium, dimensions, viewports, interaction states, static fallback
Verification: data checks, rendered inspections, accessibility, text equivalent
```

Choose mode independently from visual genre:

- **Exploratory** reveals structure and alternatives. Use a neutral question or
  metric title and avoid prematurely asserting a takeaway.
- **Explanatory** foregrounds one supported conclusion. Use a proportional
  claim title and focused annotation.
- **Operational** supports repeated scanning, exception detection, and action.
  Show state, freshness, comparator, target, and data quality.
- **Reference** optimizes lookup, completeness, stable ordering, and durable
  documentation.

## Evidence Disclosure Layers

Keep the default view complete without forcing the full audit trail into the
mark layer.

1. **Default evidence view**: question or supported claim, units and scale,
   named comparator, material denominator, active analytical state, and any
   uncertainty or missingness that could change interpretation.
2. **Immediately adjacent documentation**: concise source and vintage, metric
   definition, consequential filters or exclusions, interval definition,
   caveats, and a short caption or note.
3. **Recoverable audit trail**: full lineage, query or notebook,
   transformation log or commit, extensive methods, detailed sensitivity, and
   an accessible table or long description.

Nothing in Layers 1 or 2 may be hover-only or disappear from export. Layer 3
may be linked or disclosed when it remains durable and discoverable. Prefer
direct labels or embedded keys when they reduce decoding burden; use a compact
legend when it is clearer.

## Workflow

### 1. Frame The Reading Situation

- Complete the Evidence Display Contract and name the unit of analysis.
- Inspect the host publication, product, or report. Preserve its established
  typography, palette, and chart conventions unless they compromise integrity,
  comparison, legibility, or accessibility.
- Select a visual genre and finish bar from the reading situation: academic
  plate, technical atlas, operational monitor, presentation figure, or
  interactive analytical view. Read `references/principles.md` for genre,
  composition, typography, color, table, and annotation guidance.

### 2. Audit The Evidence And Comparison

- Check sources, column meanings, definitions, units, date range,
  denominators, filters, missing values, duplicates, outliers, joins, and
  transformations before drawing.
- Apply `references/comparison-integrity.md` whenever values, groups, periods,
  rankings, targets, or scenarios are compared.
- Distinguish counts, rates, percentages, percentage points, indexed values,
  ranks, residuals, estimates, predictions, and modeled values.
- Do not fabricate production data. If data is unavailable, provide the needed
  schema and comparison architecture; use clearly labeled synthetic data only
  when the user explicitly asks for a mockup.

### 3. Choose The Comparison Architecture

- Read `references/chart-selection.md` when selecting a chart form or replacing
  a weak one.
- Use the smallest set of encodings that answers the thinking task. Prefer
  position and length over area, volume, angle, or decorative metaphor.
- When the form is ambiguous or the stakes are high, sketch materially
  different architectures and compare what each reveals, hides, and asks the
  reader to decode.
- Choose a table when exact lookup, mixed units, or many values matter more than
  shape. Choose no visualization when prose or a few numbers answer the task
  more honestly.

### 4. Compose From Evidence Outward

Build in this order: data marks, scales and units, reference values, direct
labels or compact key, uncertainty, annotations, documentation note, title,
then polish.

- Make data marks stronger than scaffolding.
- Define color roles before choosing hues: ink, context, focus, uncertainty,
  exception, and interaction state. Use color only when it encodes,
  distinguishes, or emphasizes.
- Build hierarchy through position, scale, measure, spacing, annotation, and
  rule weight before boxes, shadows, or ornament.
- Design print, desktop, mobile, and presentation outputs as sibling
  compositions when their constraints differ. Preserve the same analytical
  state and evidence contract instead of shrinking one layout.
- Make an interactive default intelligible before motion or disclosure. Provide
  reduced-motion and static paths; never gate evidence on animation.

### 5. Apply The Anti-Reflex Taste Check

- If typography, palette, or composition could have been chosen from the word
  "Tufte" before inspecting the evidence, restart the styling pass.
- Do not simulate seriousness with cream paper, prestige serif typography,
  hairline rules, marginalia, tiny mono labels, or a muted accent by reflex.
- Do not substitute novelty, maximalism, or brand theater for analytical
  distinctiveness. A display should be memorable because the evidence became
  unusually clear.
- Avoid card grids and generic box-and-arrow posters when alignment, grouping,
  sequence, brackets, small multiples, or direct annotation carry the
  relationship more precisely.

### 6. Verify The Rendered Artifact

Treat rendered QA as a hard gate.

- Render or export the exact deliverable at its intended size. Inspect pixels,
  pages, required interactive states, and sibling compositions rather than
  relying on source validity or successful export.
- Apply `references/critique-checklist.md`. For diagrams, also apply
  `references/evidence-diagrams.md` at native-resolution connector crops.
- Check scale, units, state, missing intervals, uncertainty, contrast, reading
  order, clipping, overflow, label collisions, small-multiple consistency,
  documentation placement, and text-equivalent parity.
- A visible defect blocks completion. Repair it, re-render, and re-inspect the
  same mark class.
- If rendered inspection is impossible, state that limitation, perform the
  best static check, and do not claim reviewed, decision-grade, or
  publication-grade completion.

## Coordination And Authority

### Requirement Precedence

When requirements conflict, apply this order:

1. Truth and non-deception.
2. Accessibility and actual-size legibility.
3. The reader's analytical task and named comparison.
4. Evidence completeness and auditability.
5. Host conventions and brand identity.
6. Aesthetic refinement and implementation convenience.

Medium-specific skills own implementation mechanics, runtime behavior,
integration, and format-specific validation. This skill owns the semantic
design contract: named comparison, visual magnitude, scale meaning, evidence
hierarchy, material uncertainty, visible analytical state, and documentation.
A medium-specific adaptation may change geometry but must not silently change
those semantics.

## Completion Grades

Use the highest grade whose requirements have actually been demonstrated:

- **Provisional**: source identified, provisional question stated, unknowns
  visibly labeled, and no completeness claim.
- **Reviewed**: metric and comparison contracts complete, computation checked,
  chart form justified, and final-size render inspected.
- **Decision-grade**: reviewed requirements plus denominators, material
  uncertainty or sensitivity, provenance, data vintage, visible active state,
  accessible text equivalent, and reproducible query or specification.
- **Publication-grade**: decision-grade requirements plus editorial and
  citation review, inspection of every target size and export, format-specific
  accessibility verification, and no unresolved visible defects.

Polish, source quality, and successful export do not establish a grade.

## Reference Routing

Read only the references implicated by the Evidence Display Contract. Do not
load the entire reference set by default.

- `references/principles.md`: genre, taste, composition, typography, color,
  tables, dashboards, maps, and annotations.
- `references/comparison-integrity.md`: comparisons, magnitude, temporal
  alignment, aggregation, significance, freshness, and active state.
- `references/chart-selection.md`: chart form, redesign, and data sufficiency.
- `references/uncertainty.md`: estimates, samples, models, forecasts, rankings,
  causal claims, sensitivity, or material measurement error.
- `references/evidence-diagrams.md`: connectors, bounded nodes, causal or
  system maps, technical atlases, networks, and flows.
- `references/critique-checklist.md`: review and final rendered QA.
- `references/accessibility.md`: public, interactive, or durable artifacts.
- `references/captions-alt-text.md`: final artifacts, captions, documentation
  notes, or text equivalents.
- `references/citations.md`: public source and provenance map.

## Stop Rules

- Stop or reframe when a common scale would conceal an invalid comparison.
- Do not silently connect across missing intervals, hide excluded groups, or
  present selected examples, partial periods, or top-N subsets as the whole.
- Do not imply causality with arrows, sequencing, fitted lines, color, or
  annotation unless the evidence supports a causal claim.
- Stop and change form when the display cannot preserve required comparison,
  uncertainty, documentation, state, or legibility.

## Output Contract

For routine creation or revision, return:

- the artifact path or exact changed file
- one sentence naming the comparison architecture and rationale
- any material data or interpretation caveat
- the final size, viewport, pages, or states actually inspected

For decision-grade or publication-grade work, also return the full Evidence
Display Contract, completion-grade evidence, semantic color roles,
accessibility proof, and verification manifest.

For critique, classify findings as:

- **Blocker**: materially false, misleading, or unsupported
- **Major**: impairs comparison, interpretation, accessibility, or auditability
- **Minor**: craft defect that does not change the conclusion

Lead with blockers, then majors, and report the highest-consequence findings
instead of narrating every checklist item.
