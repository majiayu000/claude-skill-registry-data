---
name: github-readme-visuals
description: Create or refresh screenshot-led product hero images, localized interface captures, and image-led README sections for GitHub repositories. Use whenever a user asks to make a GitHub README show a GUI product visually, add software screenshots, design a README hero image, reproduce a screenshot-collage reference, or prepare repository-bound visual documentation. For GUI applications, default to the deterministic product-proof split hero with real software screenshots unless the user explicitly requests another visual direction.
---

# GitHub README Visuals

Create a fast, trustworthy visual explanation of the product without replacing its factual README content.

## Runtime Copy And Default Profile

Before production, identify the resolved Skill path. A path inside a sibling directory ending in `-workspace/skill-snapshot` is an evaluation baseline, not a production Skill. Do not use it to create repository assets. Resolve and load the canonical installed or source copy instead. If no canonical copy is available, stop and report that the Skill installation must be synchronized.

For any GUI desktop or web application, use the **Product-proof split v1** profile unless the user explicitly requests a different direction after seeing or naming it. Read [the complete profile specification](references/product-proof-split-v1.md) and start from the bundled [deterministic HTML template](assets/product-proof-split-v1.html).

This default is intentionally screenshot-led: the left side explains the product and the right side proves it with complete, real interface captures. A request to “use `github-readme-visuals`”, “replace the current hero with the Skill”, or “make it consistent with the established README visual style” selects this profile and supersedes an earlier unreviewed moodboard, illustration, or concept-art proposal.

Do not silently reinterpret the default as editorial artwork, a decorative cover, or a generated scene. Pure illustration is an opt-out path that requires an explicit user request such as “use an abstract/conceptual hero” or a non-GUI product for which real interface evidence does not exist.

## Workflow

1. Inspect the repository before designing.
   - Read the README, product notes, local instructions, existing assets, and available screenshots.
   - For application repositories, prioritize real product screenshots as proof. Do not present generated UI as a real screen.
   - Determine how to run or open the real application and list four to six distinct, user-relevant states to capture. The first/default screen is always the primary state unless the user names another workflow.
   - Record screenshot provenance, locale, dimensions, and whether the complete application window is visible in `docs/readme-visuals/visual-manifest.json` using the schema in the profile specification.
   - Identify the user journey a first-time visitor should understand in one glance.
   - Build a visual-claim ledger before writing hero copy: every product, pricing, privacy, credential, provider, and deployment claim must be supported by the README, source, or user-confirmed facts. Omit ambiguous claims instead of guessing.

2. Establish visual direction.
   - When Creative Production is available, use its style intake before generating a new direction. Use `moodboard-explorer` when the user asks for multiple visual territories or concept options.
   - Do not use Creative Production intake to replace the default Product-proof split v1 profile when the user simply asks for a README hero. Use intake only when the user explicitly requests exploration or a different visual territory.
   - If the user does not choose a direction, use Product-proof split v1. Preserve its 2560×1280 canvas, left/right allocation, equal screenshot frames, rotation, overlap, clipping, triangle orientation, logo treatment, and text hierarchy. Change only repository-specific copy, verified branding, palette accents, and real screenshot files.
   - Directly inspect every supplied reference before production. Record its canvas ratio, major spatial split, dominant visual, screenshot count, overlap, rotation, off-canvas clipping, shadows, typography blocks, and decorative motifs.
   - When the user explicitly requests a layout or style match, preserve the reference's composition grammar and visual hierarchy while replacing its UI, logo, copy, branding, and assets with material from the target repository.
   - Measure repeated screenshot frames instead of estimating them independently. If the reference uses equal-size frames, define one canonical width and aspect ratio for every screenshot; create hierarchy through position, overlap, off-canvas clipping, rotation, contrast, and z-order rather than arbitrary scaling.
   - When the brief says one-to-one, exact, or fully replicated, create a pixel geometry table before editing. Record canvas size; each screenshot's four corners, frame width and height, rotation, off-canvas clipping, and z-order; distances between adjacent frames; and each decorative shape's orientation and anchor point.
   - Derive CSS positions from measured corners and rotation. Do not substitute a visually similar arrangement or independently eyeball each frame.
   - Do not start final production from a moodboard or verbal summary alone when an exact reference image is available.

3. Produce assets.
   - Use deterministic composition for every GUI software hero. Copy `assets/product-proof-split-v1.html` unchanged into `docs/readme-visuals/product-proof-split-v1.html`, copy the example data file to `docs/readme-visuals/hero-data.js`, and populate only the data file. Keeping the template byte-identical preserves the approved geometry across repositories and conversations.
   - Do not use image generation to create the final GUI hero. Image generation may create optional background texture only when the user explicitly asks, but it must never invent, redraw, obscure, or replace product UI.
   - Use real captured screenshots for implementation, settings, privacy, or workflow proof. Review each one for secrets, personal data, and legibility.
   - Make the repository's real screenshots the dominant visual. Product-proof split v1 uses six distinct captures by default and permits four or five when the product genuinely has fewer useful states. Never fill a slot by repeating a page, crop, or near-identical state.
   - Use the application's first/default screen as the dominant screenshot unless the user names another primary workflow. Arrange secondary screenshots by user importance, not filename order.
   - Do not repeat the same page, near-identical state, or duplicated crop inside one collage. Each screenshot must prove a distinct interface or capability.
   - Keep decorative shapes outside screenshot bounds and outside the logo clear space. Decorations must never look like product UI, status indicators, annotations, or screenshot content.
   - Use the original transparent application logo directly on the composition background unless an existing brand system explicitly defines a container. Do not add a dark tile, badge, or frame by default.
   - When the repository has multiple README languages, generate one localized hero per README from a shared layout source. Keep geometry, screenshot order, logo treatment, and visual hierarchy identical; localize only verified copy and typography adjustments.
   - Match the language inside product screenshots to the destination README whenever the application supports that locale. A localized headline over screenshots from another language does not count as a localized hero.
   - Use stable language-qualified filenames such as `product-hero-zh.png` and `product-hero-en.png`, and point each README only to its matching language asset.
   - Preserve the complete product window. Never use `object-fit: cover`, clipping, masks, or manual crops merely to force a screenshot into the reference frame ratio.
   - Capture Product-proof split screenshots at 4:3, preferably 1200×900. When recapture at the target ratio is impossible, use proportional `contain` scaling and disclose the resulting empty space; do not silently remove interface content.
   - Reproduce decorative orientation explicitly. For triangles, arrows, slashes, and asymmetric shapes, record the pointing direction or vertex coordinates; matching only color and approximate location is insufficient.
   - Save project-bound final assets in a tracked repository directory, normally `docs/images/`. Do not leave README assets only in a generated-images or temporary directory.

4. Update README files additively.
   - Keep every existing line unless the user explicitly authorizes removal or rewriting.
   - Place the hero directly after the primary installation or download call to action.
   - Place an interface-preview section after the first workflow explanation, using only the smallest set of screenshots needed to explain the product.
   - Keep language variants factually aligned while writing naturally in each language.
   - Keep localized hero claims semantically equivalent. Do not introduce a capability, provider, pricing, credential, or privacy claim in only one language.
   - Use descriptive alt text and repository-relative image paths.

5. Verify before delivery.
   - Read [the visual checklist](references/visual-checklist.md) and complete every applicable item.
   - For Product-proof split v1, run `python "<resolved-skill-root>/scripts/verify_readme_visuals.py" --repo <repository> --manifest docs/readme-visuals/visual-manifest.json --expected-profile product-proof-split-v1`. This verifies the canonical template, hero dimensions, README/locale mapping, real-capture attestations, complete-window attestations, 4:3 screenshot dimensions, primary-screen order, screenshot uniqueness, and bilingual screenshot-count parity.
   - For an explicit opt-out profile, run `python "<resolved-skill-root>/scripts/verify_readme_visuals.py" --repo <repository>`. Add `--expected-size docs/images/hero.png=1600x900` for exact-size assets. Every expected-size path must match an image referenced by the inspected README files. Treat missing files, empty Markdown alt text, unreadable images, wrong required dimensions, and probable blank/uniform renders as blockers; review localization-count differences as warnings.
   - Treat a GUI hero that does not contain real target-product screenshots as a blocking failure even when separate screenshots appear below it in the README.
   - Inspect the final hero and screenshots at display size. Confirm that the hero conveys the product category and the screenshots remain readable.
   - Compare the final hero against the reference on five structural checks: left/right allocation, dominant screenshot position, screenshot count, overlap/rotation pattern, and text-block hierarchy.
   - Run a duplicate-and-intrusion review: confirm every screenshot is unique, the main screenshot is the intended first screen, and no decoration overlaps a screenshot or logo.
   - Re-check every visible factual claim against the visual-claim ledger. Remove any unsupported API-key, pricing, privacy, offline, provider, or product-capability statement.
   - Inspect every exported language variant independently. A successful render of one locale does not validate another; check for missing images, black render blocks, overflow, unexpected wrapping, and layout drift.
   - Verify both localization layers for every variant: composition copy and in-product screenshot UI. Navigation, headings, tabs, buttons, and settings labels should use the destination README language.
   - For equal-frame references, verify every screenshot has the same rendered width and aspect ratio in the composition source.
   - Confirm every screenshot preserves the complete captured window: title bar, navigation, primary content bounds, and visible window edges must not be removed by the composition.
   - For one-to-one work, render at the reference's exact pixel dimensions and compare reference and output with a 50% opacity overlay or edge overlay. Verify screenshot corner positions, inter-frame gaps, rotation, z-order, canvas-edge clipping, and asymmetric decoration direction before approval.
   - Use a default geometry tolerance of 8 px per measured corner and 0.5 degrees per rotation unless the user specifies a stricter tolerance. Any intentional deviation must be documented and user-driven.
   - Report which images are original generated artwork and which are real product captures.

## Decision Rules

- For a GUI application with no explicit alternative direction, use Product-proof split v1: left-side verified brand/copy and right-side complete real screenshots.
- Use six screenshots by default, or four to five when the product has fewer genuinely distinct states. Do not fabricate or duplicate screens to reach a count.
- For a CLI, library, API, or other product without a GUI, use a truthful diagram, terminal capture, or explicit abstract hero appropriate to the evidence available.
- Use an abstract generated hero for a GUI application only when the user explicitly opts out of the screenshot-led profile or real UI capture is impossible and the user accepts that limitation.
- A separate screenshot section below an illustration does not satisfy the default GUI hero contract.
- Stop and ask for direction only if an unverified visual claim, brand rule, or missing source asset would materially change the result.
