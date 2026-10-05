---
name: rebuild-scientific-poster-ppt
description: Rebuild a scientific poster, graphical abstract, dense one-page slide, or reference slide image as a high-fidelity editable PowerPoint while using an accompanying paper or PDF as the authority for scientific figures and claims. Use when the user supplies a PNG/JPG/PDF visual reference plus a manuscript, asks for editable PPT/PPTX, requires paper figures to be split and restored with imagegen, or requires render comparison and independent subfigure auditing.
---

# Rebuild Scientific Poster as Editable PowerPoint

## Contract

Treat the inputs as two authorities:

- The reference image controls canvas ratio, layout, cropping, spacing, hierarchy, and overall appearance.
- The paper controls scientific figures, captions, variables, units, legends, data relationships, and claims.

Never trade scientific accuracy for a visually plausible image. Do not use external OCR, recognition APIs, third-party conversion services, or a full-page screenshot as the editable slide. Do not develop a new image-to-PPT program.

Deliver:

- an editable `.pptx`;
- independent scientific and complex visual assets;
- an exact-size rendered preview, overlay, and difference image;
- structural and clean-artifact validation;
- independent per-subfigure scientific audit results.

## Required companion workflows

Use the available PDF, imagegen, faithful editable-PPT, and clean-artifact skills. Let the faithful editable-PPT workflow own manifest/build mechanics; this skill owns scientific evidence mapping and acceptance gates.

Before image generation, read [references/imagegen-prompts.md](references/imagegen-prompts.md). Before delegating scientific review, read [references/scientific-audit.md](references/scientific-audit.md). Before final delivery, read [references/delivery-contract.md](references/delivery-contract.md).

## Workflow

### 1. Inventory the page

Inspect the reference image visually before reconstruction. Record:

- source pixel dimensions and intended PowerPoint ratio;
- every visible text block, panel, arrow, card, icon, plot, legend, colorbar, and conclusion band;
- which objects are ordinary design elements and which are scientific evidence;
- the required final audience and the forbidden internal content.

Create a task-local output directory. Preserve the original inputs unchanged.

### 2. Build the paper-evidence map

Extract or render the paper figures at their native quality. Locate every referenced figure, subfigure, caption, and supporting body paragraph.

Create an internal mapping:

| Poster region | Paper figure/panel | Caption/body evidence | Exact symbols/claims | Display treatment |
|---|---|---|---|---|

Transcribe every displayed equation, acronym definition, conclusion claim, axis, unit, and special symbol into the map. Record and resolve every paper-versus-poster conflict in favor of the paper. Do not infer an unmatched scientific plot. Mark it unverified and ask only when the missing mapping materially blocks accuracy.

### 3. Choose the object strategy

Use:

- PowerPoint text boxes for ordinary text, panel labels, axis text, units, legends, and annotations that can be separated safely;
- PowerPoint shapes for cards, bars, arrows, lines, markers, and simple diagrams;
- SVG for simple regular icons;
- one sparse imagegen asset sheet for complex icons or illustrations, followed by independent transparent assets;
- one imagegen job per scientific subfigure or safely separable scientific region.

Do not generate a multi-panel paper figure as one asset merely because the paper stores it as one image. Split `a`, `b`, `c`, and repeated regime/condition panels when their boundaries are safe. Keep each panel independently replaceable.

### 4. Restore scientific assets

Inspect every local input before editing it with imagegen. Generate serially and save each accepted result immediately into the task workspace.

Create a scientific-provenance ledger before assembly. It must contain one row per scientific figure region requiring imagegen with: panel identity, authoritative paper source, imagegen job ID, generated output, audit status, and any post-attempt fallback. A direct paper crop or poster crop is not an imagegen restoration and is forbidden as the initial asset strategy.

For each subfigure:

1. Pass the authoritative paper panel first.
2. Pass the poster display region second when composition guidance is needed.
3. State the exact panel identity, axes, ranges, variables, units, legends, colors, curves, markers, and forbidden changes.
4. Import only the explicitly returned image.
5. Inspect it at original resolution before assembly.

Reject any result that adds, removes, shifts, relabels, or merges scientific objects.

If a quantitative panel fails:

1. Write an explicit object inventory with approximate numeric endpoints, peak positions, row order, marker counts, and axis ranges.
2. Retry imagegen with that inventory and the paper panel as sole authority.
3. For a text-only error, perform a targeted imagegen edit that changes only the incorrect string.
4. If imagegen still changes simple quantitative geometry, preserve the imagegen-restored non-data surround but replace affected bars, curves, markers, labels, or paper-pixel regions with authoritative native or paper-derived elements. Record this only as a post-attempt exception with the failed imagegen job and audit evidence. Never ship altered data merely to claim an all-imagegen result.

Before assembly, verify the coverage invariant:

`required scientific figure-region count = accepted scientific imagegen jobs + documented post-attempt exceptions`

Every exception must still have at least one recorded scientific imagegen attempt. Zero-attempt source-preserved scientific assets fail the workflow.

Do not count a native PowerPoint equation, native label, SVG, or paper-derived formula-only overlay as a separate scientific figure region. Record it as a component of its parent panel and verify it against the exact-symbol ledger.

Verify panel isolation at original resolution. Each asset must contain the complete scientific viewport and every label, axis, tick, legend, or annotation that cannot be separated safely, while containing no neighboring panel label, axis fragment, legend fragment, or stray border pixels. Panel labels and other safely separated text may instead be native PowerPoint objects; the ledger must name those companion objects so the complete panel can still be audited.

### 5. Assemble the editable slide

Use the faithful editable-PPT manifest as the authoritative build source.

- Keep all geometry in source-image coordinates.
- Preserve the supplied slide size and content box.
- Prevent duplicate titles, axes, legends, or colorbars when combining native text with scientific assets.
- Record provenance for every image.
- Keep major wording native and editable.
- Use mathematical fonts or rendered formulas without changing symbols, superscripts, or subscripts.
- Replace any reference-image equation, acronym definition, or conclusion wording that conflicts with the paper authority. Check it character by character against the evidence map.

### 6. Render and compare

Build the PPT, then render it.

Create:

- a preview resized to the exact source dimensions;
- a 50% overlay with the reference image;
- a pixel-difference image;
- a contact sheet showing source and preview.

Inspect panel boundaries, main-element centers and sizes, cropping, text wrapping, spacing, and final-size readability. Structural validation alone does not prove visual fidelity.

Record explicit pass/fail fields for title weight, subtitle style, conclusion wrapping, every axis title, every legend, panel isolation, and slide-edge overflow. Do not mark visual QA passed while any text or scientific content is clipped, overlapped, or outside its container.

### 7. Run independent scientific audit

Use a fresh subagent as an evaluation surface. Give it the raw paper, captions/body text, reference image, independent assets, and final preview. Do not give it expected answers or prior diagnoses.

Require `通过`, `需要修正`, or `无法确认` for every subfigure. Any explicit scientific blocker must trigger correction and re-audit. Reuse the same reviewer for targeted re-audits so it can verify the failed item without weakening the gate.

Give the reviewer the exact-symbol/claim ledger and require paper authority to override conflicting poster content. If two independent reviews disagree on an equation, claim, unit, crop, or data object, treat the item as `无法确认` until the conflict is resolved against the paper and re-audited.

### 8. Finalize and clean

Finalize only when:

- structural validation passes;
- exact-size visual QA passes;
- the scientific-provenance coverage invariant passes and has no zero-attempt asset;
- every scientific subfigure passes independent audit;
- no missing/added scientific object, incorrect legend, wrong unit, altered trend, or malformed symbol remains;
- final PPT/XML/text contain no prompts, temporary paths, TODOs, review notes, or production instructions.

Package only the final PPT, independent assets, preview/overlay/difference, audit report, and clean validation report.

## Hard blockers

Do not deliver when any of these remain:

- missing or added curve, interval, marker, peak, legend item, or subfigure;
- changed peak/valley/turning-point order or relative magnitude;
- wrong axis range, tick, variable, unit, superscript, subscript, Greek letter, or color mapping;
- unreadable or clipped scientific text at final slide size;
- clipped, overlapping, or out-of-container title, subtitle, conclusion, legend, or axis text;
- a scientific asset without a recorded imagegen attempt, or an undocumented source-preserved fallback;
- neighboring-panel fragments or missing self-labels/axes inside an independent asset;
- an unresolved paper-versus-poster equation, acronym, unit, or claim conflict;
- mismatched panel order or incorrect cropping;
- failed structural validation or failed independent audit;
- a full-page raster used as the editable slide.
