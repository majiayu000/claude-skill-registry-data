---
name: html-to-pptx
description: Convert reviewed HTML pages or presentations into editable PPTX using measured canvas and native business text/shapes. Use by default at the final stage of Document Studio document production or for supplied-HTML conversion; planning and HTML design remain with their owners.
---

# Default HTML-to-PPTX export

Use actual supplied/reviewed HTML, final file requirements and existing context. This is the fixed default DEMO PowerPoint exporter under [authoring routes](../report-html-pptx/system/authoring-routes.md). An existing template, live use or native design-quality flag does not replace this path. A user-requested special output is handled as an export exception; HTML remains canonical. A bounded conversion does not restart intake.

Check the selected runtime once at export: Python 3.11+, requirements.txt dependencies, Playwright and Chromium. Reuse known runtime paths/configuration. Missing tools do not authorize a native rewrite, dependency installation or new preference interview. Finish the HTML/unaffected checks and state the genuine conversion boundary; ask only when an additional installation or changed deliverable requires a user decision.

## Convert and inspect

Use [v4 execution and outcome semantics](../report-html-pptx/references/workflow-execution.md). Read the persisted conversion-result.json: file creation, failed checks, unavailable rendering and delivery readiness are separate. A useful candidate remains available when checks fail; never call it complete. Snapshot pixels default to 2x; original-image bytes and native geometry remain preserved. Opt-in solid SVG line groups can become native connectors; unsupported SVG retains the existing snapshot path.

1. Read .config.local.toml if present. Defaults are font auto-install no, audit triage and cleanup keep. Missing/legacy ask values use these defaults. Honor a saved explicit review preference.
2. Run python <skill-dir>/convert.py <input.html> --out <output.pptx>. Preserve authored HTML; the converter's audited copy is for export-specific fixes only.
3. Check the generated `<output>_audit/text-fidelity.json` against the measured native text records: content/order, required spaces and text-box coverage must agree. A character-frequency count alone cannot prove order or spacing. Explicit authored line breaks must survive as native paragraph/soft-break boundaries at the same text offsets; a space replacing a semantic break is a fidelity failure. Read the resulting sentences and update their bounds after extra lines. Then inspect every output slide for a new full document, or affected/dense/warned slides and the sequence for revisions. Read Korean predicate/auxiliary endings, titles, table cells and notes in the actual PowerPoint/LibreOffice render. A contact sheet supports navigation; it does not complete paragraph review. Check structured findings, the sequence/contact sheet and actual dense/changed/warned output slides. Fix issues in one batch. Inspect media snapshots themselves when image-led pages are involved.
4. Reconvert dependent scope. Local audited-page edits can use --only-slides N,N only with unchanged shared styles, fonts, assets, page count/order and canvas. Authored HTML or shared-resource changes require a fresh audited copy/full conversion.
5. Retain caches for reuse. Cleanup is conditional on accepted/requested clean preference, not a required finishing stage.

Detect the natural page canvas before conversion. A4 cannot become 16:9. Use explicit data-pptx-slide roots and meta pptx-width/pptx-height for viewport-relative layouts. One PPTX has one page size; mixed canvases fail. [Office-print](../report-html-pptx/references/office-print-reports.md) owns physical A4 dimensions and print checks.

Keep actual text, quantities, labels, table cells, simple shapes and meaningful connectors editable. Rasterize unsupported decoration only. Tables traverse group/row/cell separately; editable cells are not necessarily a native table object. Mixed inline blocks, markers and line-flow details require actual render inspection.
For arrow-connected diagrams authored under [the item-centered design rule](../document-design/references/arrow-diagram-alignment.md), verify that first, middle and last item text remains centered in separate editable item bounds. Keep arrow lanes distinct. If the authored geometry is wrong, return the local fix to HTML design; do not infer alignment from left/middle/right position or globally center unrelated reviewed text.

Titles, business labels, official logos and footers stay separate from media snapshots; baking those sibling overlays into a background duplicates text and loses editability. Verify original PNG/JPEG bytes/alpha and the authored crop. Never substitute a full-slide bitmap. [DEMO typography](../report-html-pptx/references/demo-esg-typography.md) preserves purpose-specific report density, captions and small source detail; PPTX is not automatically a live deck.

Resolve local fonts from inline/linked CSS and bounded imports with URLs relative to each stylesheet. Actual browser appearance is not embedding proof: inspect found files, PPTX typefaces and embedded font resources. Font installation requires applicable authorization; remote CSS is not silently fetched.
For Korean/Japanese, prefer the bundled language-specific Pretendard source. Static per-weight faces preserve source outlines and actual Office style slots. Check actual renderer recognition and every final page; a font name or Embedded=true does not certify weight fidelity. If authorized for this host, install resolved static faces per user with --install-user-fonts. Reuse that located authorization and already verified installations; do not ask again per document. Preserve existing differing files and registrations. Never infer installation permission from silence or bundle a personal authorization into a distributed release. Installed matching faces are a separate proof path from embedded-only recognition; other machines still need verification.

On Windows, prefer actual PowerPoint PDF fixed-layout output rasterized with PyMuPDF for verification images. PowerPoint's direct Slides.Export(PNG) was observed to widen/clip CJK body text despite recognizing included fonts while its PDF glyphs/advances matched the source. This changes the QA renderer only: the delivered PPTX retains native text/shapes. If PDF raster support is unavailable, retain useful PNG/PPTX candidates but embedded-only PNG font rendering remains unverified and blocks completion. A valid PDF preview does not certify another computer's PowerPoint UI. Renderer-profile changes invalidate old preview reuse.

## Review boundary and repair

Inspect actual final PPTX renders through an available PowerPoint/LibreOffice renderer. If unavailable, complete HTML and structural checks, deliver a useful file as a review candidate with export visuals unverified, and keep the readiness gate blocked. A contact sheet/object count cannot certify glyph clipping, exact crop or small-text readability.

If the same element fails after two similar repairs, inspect the cause and change the export fix. Preserve the fixed HTML-to-PPTX route; do not automatically switch to native authoring. Content fixes belong to authored HTML; conversion-only fixes belong to the audited copy. Keep natural wrapping by default. If only PPTX splits a meaningful phrase (for example 정리해 / 줘), inspect the cause and apply `data-pptx-text-flow="measured"` only to the affected paragraph in the audited copy when its browser lines have been verified. Do not freeze all body lines. Rerender the changed PPTX pages. Register the audited input as a dependency of the export so an export-only fix cannot retain stale QA. Bind [project-state](../report-html-pptx/system/project-state.md) only to actual produced/inspected artifacts; QA and user acceptance are distinct.

## Load detail for a real issue

- Failure/configuration/renderer/cache: [full workflow](references/full-workflow.md).
- CSS mapping: [supported CSS](references/supported-css.md).
- Specific font/text regression: search [lessons](references/lessons-learned.md) for the symptom; historical preferences do not override this entrypoint.
- Converter implementation: [methodology](references/methodology.md).
- DEMO dependency/export integration: [PPTX production](../report-html-pptx/references/pptx-efficient-production.md).

## DEMO project contract at conversion

For full DEMO document production, conversion checks the independently resolved use/canvas, actual design measurement and current HTML editorial/visual QA through [production contract](../report-html-pptx/references/production-contract.md). Preserve its choice and reference packet; PPTX is not a ratio. Fix pending decisions or evidence at the owning stage. Only an explicitly bounded conversion of already reviewed HTML may use --reviewed-html-only; never use it to skip new-document requirements. Corrected .audited.html needs current checks unless byte-identical to the reviewed source. Keep actual PPTX render/editability/native-line-flow checks after conversion.
