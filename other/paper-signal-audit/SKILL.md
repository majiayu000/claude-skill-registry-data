---
name: paper-signal-audit
description: >-
  Inspect and diagnose minimal-zine posters, photo restyles, editorial images, and social-card series for subject preservation, factual and text integrity, composition, paper realism, print-process coherence, color signal, anti-AI craft, platform fit, and series continuity. Use when the user asks whether an image has高级感, feels AI-generated, matches Paper Signal or gc-minimal-zine quality, needs improvement, or should be regenerated. Returns evidence-based findings and a targeted correction prompt; regenerates only when the user also asks for a fix.
---

# Paper Signal Audit

Judge the image that exists, not the prompt that intended it.

## Load the audit basis

Read from `../paper-signal/`:

1. `references/subject-routing.md`
2. `references/visual-language.md`
3. `references/quality-contract.md`
4. `references/restyle-contract.md` for edits

Read the project prompt, manifest, preservation record, outline, and evidence ledger when available.

## Audit workflow

1. Inspect every local image with `view_image` at original detail.
2. Identify the delivery route, subject route, and intended composition mode from artifacts; infer them explicitly when artifacts are missing.
3. Compare the raster against protected subject details, exact text, factual claims, and requested aspect ratio.
4. Inspect at full size for identity, geometry, paper, image integration, type, print defects, and AI artifacts.
5. Inspect at thumbnail size for subject recognition, chromatic signal, hierarchy, and series recognition.
6. For a series, compare the whole sequence for material continuity, composition variety, pacing, and cloned-layout drift.
7. Rank findings by severity and give one correction path per failed image.

## Report format

Lead with the verdict:

- `Pass` — ready to use
- `Pass with refinements` — usable; small craft changes would improve it
- `Regenerate` — one or more blocking failures

Then report only observed issues:

| Severity | Image | Observation | Why it matters | Targeted correction |
|---|---|---|---|---|

Separate:

- blocking: subject drift, false/wrong text, wrong ratio, unreadable essential content, missing output
- major: generic template composition, weak subject scale, incoherent print process, pseudo-language, muddy hierarchy
- minor: slightly weak signal, texture repetition, edge or safe-zone refinement

Do not praise or criticise with unsupported adjectives. Point to visible evidence.

## Anti-AI diagnosis

Check specifically for:

- meaningless microtext or faux Asian characters
- generic birds, moons, stairs, doors, flowers, and registration marks unrelated to content
- uniformly applied vintage noise
- beige template plus clean modern typography
- perfect vector spacing under fake paper texture
- waxy faces, altered identity, impossible hands, warped buildings, or invented product details
- random collage fragments with no visual thesis
- empty space that creates no direction or tension

## Correction policy

Correct one failure class per regeneration. Preserve accepted subject features, text, material choices, and crop. Save the correction prompt and output as versioned siblings.

When the user asks only for review or diagnosis, stop after the report and correction prompt. Generate or edit the image only when the user explicitly asks to fix, remake, or produce it.

Never patch generated text or composition with code.
