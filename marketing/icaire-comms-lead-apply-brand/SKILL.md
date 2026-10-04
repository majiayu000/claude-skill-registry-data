---
name: icaire-comms-lead-apply-brand
description: Apply ICAIRE brand assets, lockups, and color guidance to reports, decks, web content, social visuals, and other designed outputs. Use when adding brand assets, updating visual templates, or checking ICAIRE design consistency.
---

# ICAIRE Comms Lead: Apply Brand

Use this skill when an ICAIRE deliverable needs to use the approved visual
identity consistently. This covers reports, decks, website copy with visual
notes, newsletters, social visual briefs, templates, and generated assets.

## Contract

- Use ICAIRE's primary brand color `#4A9549` as the main accent unless an
  approved campaign or product-specific design system says otherwise.
- Use approved local lockups before downloaded or chat-attached files.
- Use the report-ready lockups for rendered documents when they are available
  as local untracked assets.
- Include the ICAIRE and UNESCO lockups at the top of formal reports when
  space allows.
- For decks or other designed outputs with colored, gradient, or image
  backgrounds, verify that lockups have real alpha transparency before placing
  them. If a canonical PNG renders with a white box, create a transparent
  working copy or apply an intentional matching image background/panel in the
  artifact builder instead of accepting the boxed logo.
- Verify rendered outputs visually before treating them as ready.

## Local Assets

The report-ready lockups should be available locally when a report or deck needs
them, but they are not git-tracked assets:

- `assets/brand/report/icaire-lockup.png`
- `assets/brand/report/unesco-lockup.png`

Use `assets/brand/report/` for PDFs and white document backgrounds. For
non-white deck backgrounds, check the alpha channel before embedding these
assets; if needed, create temporary transparent copies in the artifact
workspace, or add a deliberate background color treatment behind the image that
matches the slide design, and use that in the generated output. Do not commit
downloaded originals, generated media, QR codes, or other binary assets to the
skills repo.

## Workflow

1. Identify the deliverable type: report, deck, website, newsletter, social
   visual brief, or another designed output.
2. Inspect the relevant template, renderer, or skill guidance before editing.
3. Apply the lockups and `#4A9549` consistently with the document hierarchy.
4. Keep layouts quiet and institutional: clear spacing, readable type, and
   restrained use of full-strength green.
5. Render or preview the output.
6. Visually check the first page or frame, plus any dense pages, for clipping,
   overlap, checkerboard backgrounds, boxed logo backgrounds, low contrast, or
   logo distortion.
7. Update the relevant skill guidance if the brand behavior should recur.

## Guardrails

- Do not stretch or crop lockups.
- Do not use the blue UNESCO color as ICAIRE's primary accent.
- Do not paste transient downloaded logo paths into reusable templates.
- Do not claim a PDF, deck, or visual asset is ready without visual
  verification, unless you clearly state that verification was not possible.
- Do not push ICAIRE brain updates through a local clone when the task requires
  the remote ICAIRE MCP.

## Output Expectations

Return:

- the files or templates updated
- the brand assets used
- the verification performed
- any remaining source or design limitations
