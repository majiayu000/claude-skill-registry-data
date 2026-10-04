---
name: linkedin-visual
description: >-
  Use when deciding whether an approved LinkedIn post needs a visual and, when
  useful, creating an Ahsan-style PDF carousel or requested image export with
  an editable PPTX source when needed. For M Ahsan Izhar, reproduce the
  canonical designs in examples/design as the visual target; do not improvise
  a generic tech-carousel style. Preserve approved claims and do not publish
  or schedule posts.
license: MIT
---

# LinkedIn visual

Create a visual only when it improves comprehension, credibility, or
scanability. Preserve the approved source's claims, certainty, attribution,
disclosures, and audience.

For M Ahsan Izhar, **visual fidelity to the supplied design references is a
non-negotiable requirement**. The goal is not merely to use the same colors and
fonts. The generated pages must preserve the reference layouts, proportions,
negative space, utility chrome, engineering motif, and single-cobalt focal
language.

## Ahsan visual source of truth

When the visual is for M Ahsan Izhar, read these in this order before
rendering:

1. [references/ahsan-local-design-system.md](references/ahsan-local-design-system.md)
2. [references/visual-selection.md](references/visual-selection.md)
3. [references/design-selection.md](references/design-selection.md)
4. [references/visual-fidelity.md](references/visual-fidelity.md)
5. the exact canonical PNG(s) in `examples/design/` for the selected template(s)
6. [references/presentation-execution.md](references/presentation-execution.md)
7. [references/pptx-workflow.md](references/pptx-workflow.md)
8. [references/text-fit-and-collision.md](references/text-fit-and-collision.md)

Then read the remaining references only as needed for narrative, selection,
accessibility, platform constraints, or QA.

**Canonical visual-reference directory:** `examples/design/`

The directory also contains three approved alternate design systems under
`examples/design/carousel-options/`: `evidence-ledger`, `dark-signal`, and
`modular-index`. The baseline templates remain the default. When the user asks
to compare or use an alternate option, apply
[references/design-selection.md](references/design-selection.md), then read
that option's README and rendered `slides/` PNGs. Choose one complete option
and keep the carousel consistent; do not mix options or invent a fourth visual
system.

Do not use the old/nonexistent path `examples/designs/`.

## Conditional capability routing

This skill is harness-neutral. Use the following neighboring capabilities only
when the active harness exposes them; their absence must not block the local
source-and-export workflow. Do not treat an installed skill file as evidence
that its runtime capability is available.

### Allowed design paths

Before authoring any visual, inspect the active harness's exposed tool list for
connected Inkscape MCP and GIMP MCP capabilities. Do not infer availability
from an installed application, plugin, or configuration entry. Check both
graphics MCP paths before selecting the fallback.

Use the first suitable path after that probe:

- **Inkscape MCP:** when exposed, use it for editable vector explorations,
  diagrams, option references, SVG inspection, and geometry evidence. When the
  deliverable is an editable presentation, translate the approved result into
  native PPTX objects before final export.
- **GIMP MCP:** when exposed and the page needs raster work, use it for image
  preparation such as cropping, retouching, or image-only treatments inside an
  approved image frame. Do not use a rasterized GIMP page as the canonical
  source, and do not flatten authored text, diagrams, or page chrome into a
  bitmap.
- **Native editable PPTX:** use it when neither graphics MCP is exposed, when
  neither is suitable for the requested page, or when an editable source is
  needed. It is the canonical authoring source for the carousel or standalone
  visual; the final handoff is still a PDF unless an image is explicitly
  requested.

Routing order:

1. If Inkscape MCP is exposed and the page needs vector, diagram,
   option-reference, or geometry work, use it.
2. Otherwise, if GIMP MCP is exposed and the page needs raster image work, use
   it.
3. Otherwise, call the native PPTX/presentation capability and author the
   visual there.
4. If no permitted path is available, preserve the approved page outline and
   mark rendering as blocked or unverified.

Keep the editable PPTX as the source when it is used, even when Inkscape MCP or
GIMP MCP contributed during design preparation. Export a PDF by default; export
an image only when explicitly requested. Do not hand off PPTX as the final
deliverable unless the user explicitly asks for it. Do not switch to a web
design editor, generic image generator, or unapproved design integration.

- `brand-guidelines`: apply and audit the approved identity tokens, fonts,
  assets, provenance, accessibility constraints, and usage restrictions before
  authoring. It does not authorize asset generation or publishing.
- `ui-design-system`: use only when creating or auditing the reusable Ahsan
  visual system itself. Do not invoke it for every post-specific page, and do
  not let neutral system advice override the approved Ahsan references.
- `diagram-design`: use when a page contains a flow, architecture diagram,
  chart, or other technical schematic. Load only the relevant diagram type and
  semantic guidance, then translate the result into native editable PPTX or
  Inkscape objects; do not substitute an HTML/SVG deliverable unless requested.
- `apple-design`: use when the user requests an Apple-inspired direction,
  interactive preview, swipe/transition behavior, or motion study. For static
  carousels, apply only its transferable principles of clarity, restraint,
  progressive disclosure, continuity, and directness; never import Apple
  branding, colors, materials, or typography, and never let motion guidance
  override the Ahsan tokens, static composition, or editability contract.
- `presentations`: when available, use it for native PPTX authoring,
  structural inspection, and application-aware checks. If unavailable, use the
  local editable presentation path and mark application-specific checks as
  unverified.
- `pdf:pdf`: when available, use it to render and inspect the matching PDF.
  The PDF is an export and QA artifact, never a replacement for the editable
  PPTX source.
- `verification-before-completion`: before reporting completion, map each
  claim to fresh evidence and report verified, partial, blocked, and
  unverified checks separately.

The existing `copywriting` and `humanizer` routing remains conditional and
limited to eligible prose. These editorial capabilities do not authorize any
additional design tool or external mutation.

## Priority when instructions conflict

Use this order:

1. user-approved source content and factual constraints;
2. canonical PNG composition for the selected template;
3. `visual-fidelity.md`;
4. exact token/type rules in `ahsan-local-design-system.md`;
5. generic guidance elsewhere in this skill.

The PNG decides visual composition. The written design system decides exact
colors, fonts, dimensions, editability, and QA requirements.

## Non-negotiable visual contract

For the Ahsan system:

- portrait pages: exactly `1080 × 1350 px` / 4:5;
- square standalone cards: exactly `1080 × 1080 px`;
- `paper #F7F7F4`, `ink #16181D`, `accent-cobalt #2540D9`,
  `gray #5F6472`, `line #D9DAD4`, `panel #ECECE8` only;
- `DM Sans 700/400`; `JetBrains Mono`, with `Space Mono` only as fallback;
- left-aligned editorial composition by default;
- one dominant idea per page;
- at most one cobalt focal idea per page;
- reproduce the canonical lower-right engineering motif and utility rail at the
  reference scale;
- portrait footer identity: `M. Ahsan Izhar - ahsanizhar.com`;
- portrait page counter: `NN / NN`;
- no generic full-width footer divider on ordinary pages;
- no gradients, glow, neon, robots, brains, circuit-board art, glassmorphism,
  stock illustrations, arbitrary icons, or drop shadows;
- do not use the reference PNG as a slide background or flatten authored slide
  content into one image.

## Boundaries

- Start from an approved post/brief or explicitly approved source.
- Do not invent claims, metrics, testimonials, personal results, evidence,
  citations, screenshots, or identity details.
- Do not change the post thesis simply to fit a template.
- Do not publish, schedule, or claim LinkedIn acceptance.
- Use the local editable presentation path for the source when presentation
  authoring is selected.
- Default final output is a PDF. Produce a PNG/JPG image only when explicitly
  requested; do not make PPTX the final handoff by default.
- Keep authored text, rules, shapes, connectors, diagram nodes, bars, and panels
  native/editable whenever the presentation capability supports it.
- A supplied screenshot/photo may remain raster content inside a designated
  image frame; a complete slide may not.

## Visual selection

Choose one result:

- `none` — text is stronger without a visual;
- `image` — one standalone technical visual is enough;
- `document` — the reader benefits from a multi-page sequence.

Do not create a carousel merely because the skill can. Do not add filler pages
to reach a preferred count.

## Workflow

### 1. Resolve source

Resolve the exact approved source, revision/hash when available, audience,
claim boundaries, evidence/caveats, and approved CTA.

### 2. Select visual form

Use [references/visual-selection.md](references/visual-selection.md). If the
result is `none`, record that decision and stop.

For an Ahsan carousel, then use
[references/design-selection.md](references/design-selection.md) to choose the
baseline or one alternate design system. Record the selection receipt before
opening reference PNGs. Content-fit selection is the default; random selection
requires an explicit exploration request.

### 3. Build the page sequence

For a document, turn the approved source into the smallest useful sequence.
Every page gets one reader job. Use
[references/narrative-frameworks.md](references/narrative-frameworks.md) only
when it makes the argument clearer; do not force a framework.

Create a source-to-slide ledger before rendering factual or attributed content.
If `copywriting` is available, use it only to tighten eligible prose without
changing claims. Use `humanizer` only on prose that benefits from it; do not
apply it to numeric labels, code, citations, or diagram text.

### 4. Map pages to the selected design system and templates

Choose the closest canonical template for each page. The mapping is defined in
[references/visual-fidelity.md](references/visual-fidelity.md).

If the user selected one of the alternate systems in
`examples/design/carousel-options/`, use that system's rendered page PNGs as
the composition target for the whole carousel. The alternate option changes
composition and motif language, but does not relax the approved Ahsan tokens,
native editability, text-fit, collision, or export requirements.

**Open the exact PNG for every selected template before authoring it.** Do not
reconstruct the style from memory. If the active environment cannot inspect the
PNG, preserve the page outline and source-to-slide ledger, then mark rendering
and canonical-template fidelity as blocked or unverified. Do not finalize the
visual as reference-verified.

For a reusable template-system request, create templates 1–4 first and stop for
user review before extending the system. For a post-specific request, use only
the templates the post needs.

### 5. Author against the reference

Follow
[references/presentation-execution.md](references/presentation-execution.md).
Treat the chosen PNG as a composition target:

- keep major anchor positions and negative-space pattern;
- preserve the reference hierarchy and relative scale;
- reproduce shared chrome and engineering motif;
- replace example copy with approved copy rather than redesigning the template;
- shorten or split copy before shrinking it below readable reference scale.

If the environment can code PPTX directly, use the deterministic `100 px = 1
inch` mapping defined in `visual-fidelity.md`.

### 6. Render and compare incrementally

After each page is authored, render it and compare it side-by-side with the
canonical PNG at the same thumbnail size. Fix composition drift immediately.
Do not wait until the whole carousel is finished.

If rendering or image inspection is unavailable, do not claim visual or
canonical-fidelity checks passed. Preserve the local source and record those
checks as blocked or unverified.

Reject and rework pages with any of these problems:

- template silhouette is no longer recognizable;
- missing or oversized engineering motif;
- missing right-side utility rail where the reference has it;
- centered generic composition;
- excess panels/cards;
- multiple cobalt focal elements;
- wrong footer identity or missing counter;
- generic full-width footer rule on ordinary pages;
- text shrunk to rescue an overloaded page;
- decorative AI imagery not present in the canonical system.

### 7. QA editable source and export

Run the verify → fix → re-verify loop in
[references/pptx-workflow.md](references/pptx-workflow.md),
[references/text-fit-and-collision.md](references/text-fit-and-collision.md),
and [references/pdf-qa.md](references/pdf-qa.md).

Check at minimum:

- dimensions/orientation;
- exact six-token palette;
- font/fallback disclosure;
- mobile readability;
- text bounds, clipping, overflow, and reserved-region collisions;
- text-to-text and label-to-detail collision checks;
- one-accent rule;
- template/reference fidelity;
- shared chrome;
- native editability of authored elements;
- page count and PDF structure when exported.

Do not export or claim readiness while any text-fit or collision check is
failed or unverified. Do not claim checks that were not performed.

### 8. Save final files

Save a new editable PPTX source revision when presentation authoring is used,
then export the matching PDF. Export a PNG/JPG instead only when explicitly
requested. Do not silently overwrite an existing source. Record the source
path, final export path, selected canonical references, page count, dimensions,
font fallbacks, QA state, and any remaining deviation.

## Workspace integration

When the shared Content Library / Visual Assets workflow is actually available:

- read the exact approved Content Library source/hash;
- generate and QA the local editable source plus the final PDF or requested
  image first;
- before any Drive or Sheet mutation, identify the exact selected folder,
  workbook, and intended asset-row changes, then confirm that the user has
  authorized that target and operation;
- upload the final PDF, or the requested image, to the selected Drive visual
  folder;
- upload the editable PPTX source only when the user explicitly requests source
  archival or the selected workspace contract requires it;
- create a `linkedin-pdf` or requested-image Visual Assets entry, plus an
  `editable-source` entry only when the PPTX source is uploaded;
- use the verified PDF or image Drive link as `Primary Visual Link`;
- re-read Drive metadata and Sheet rows before marking the visual ready.

If Drive/Sheet access is unavailable, keep the local files as valid unsynced
outputs. Do not block local generation and do not claim an upload occurred.

## References

Core visual references:

- [references/ahsan-local-design-system.md](references/ahsan-local-design-system.md)
- [references/visual-fidelity.md](references/visual-fidelity.md)
- [references/presentation-execution.md](references/presentation-execution.md)
- [references/pptx-workflow.md](references/pptx-workflow.md)
- `examples/design/README.md`

Supporting references:

- [references/visual-selection.md](references/visual-selection.md)
- [references/design-selection.md](references/design-selection.md)
- [references/carousel-brief.md](references/carousel-brief.md)
- [references/narrative-frameworks.md](references/narrative-frameworks.md)
- [references/slide-spec.md](references/slide-spec.md)
- [references/brand-and-layout-guidelines.md](references/brand-and-layout-guidelines.md)
- [references/color-schemes.md](references/color-schemes.md)
- [references/layout-archetypes.md](references/layout-archetypes.md)
- [references/visual-system-and-accessibility.md](references/visual-system-and-accessibility.md)
- [references/pdf-qa.md](references/pdf-qa.md)
- [references/text-fit-and-collision.md](references/text-fit-and-collision.md)
- [references/platform-specs.md](references/platform-specs.md) when current
  LinkedIn limits matter.

## Completion report

Report the source used, `none/image/document` decision, selected canonical
reference files, editable source path when present, final PDF or requested
image path, QA state, any unverified checks, and sync/approval state when
workspace integration was used. Do not publish or schedule.
