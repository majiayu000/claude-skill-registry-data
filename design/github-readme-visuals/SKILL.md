---
name: github-readme-visuals
description: Create or refresh original product hero images, interface screenshots, and image-led README sections for GitHub repositories. Use when a user asks to make a GitHub README show the product visually, add screenshots, design a README hero image, or prepare repository-bound visual documentation.
---

# GitHub README Visuals

Create a fast, trustworthy visual explanation of the product without replacing its factual README content.

## Workflow

1. Inspect the repository before designing.
   - Read the README, product notes, local instructions, existing assets, and available screenshots.
   - For application repositories, prioritize real product screenshots as proof. Do not present generated UI as a real screen.
   - Identify the user journey a first-time visitor should understand in one glance.
   - Build a visual-claim ledger before writing hero copy: every product, pricing, privacy, credential, provider, and deployment claim must be supported by the README, source, or user-confirmed facts. Omit ambiguous claims instead of guessing.

2. Establish visual direction.
   - When Creative Production is available, use its style intake before generating a new direction. Use `moodboard-explorer` when the user asks for multiple visual territories or concept options.
   - If the user does not choose a direction, use a restrained default: one original hero, product-led composition, readable hierarchy, and a palette derived from the repository's existing UI or brand assets.
   - Directly inspect every supplied reference before production. Record its canvas ratio, major spatial split, dominant visual, screenshot count, overlap, rotation, off-canvas clipping, shadows, typography blocks, and decorative motifs.
   - When the user explicitly requests a layout or style match, preserve the reference's composition grammar and visual hierarchy while replacing its UI, logo, copy, branding, and assets with material from the target repository.
   - Measure repeated screenshot frames instead of estimating them independently. If the reference uses equal-size frames, define one canonical width and aspect ratio for every screenshot; create hierarchy through position, overlap, off-canvas clipping, rotation, contrast, and z-order rather than arbitrary scaling.
   - When the brief says one-to-one, exact, or fully replicated, create a pixel geometry table before editing. Record canvas size; each screenshot's four corners, frame width and height, rotation, off-canvas clipping, and z-order; distances between adjacent frames; and each decorative shape's orientation and anchor point.
   - Derive CSS positions from measured corners and rotation. Do not substitute a visually similar arrangement or independently eyeball each frame.
   - Do not start final production from a moodboard or verbal summary alone when an exact reference image is available.

3. Produce assets.
   - Use deterministic composition for a software hero whose reference is built from real interface screenshots. Image generation may add a non-product polish layer, but it must not invent, redraw, or replace the product UI.
   - Use real captured screenshots for implementation, settings, privacy, or workflow proof. Review each one for secrets, personal data, and legibility.
   - Make the repository's real screenshots the dominant visual whenever the reference does. A screenshot collage may use four to eight captures when that count is part of the requested composition.
   - Use the application's first/default screen as the dominant screenshot unless the user names another primary workflow. Arrange secondary screenshots by user importance, not filename order.
   - Do not repeat the same page, near-identical state, or duplicated crop inside one collage. Each screenshot must prove a distinct interface or capability.
   - Keep decorative shapes outside screenshot bounds and outside the logo clear space. Decorations must never look like product UI, status indicators, annotations, or screenshot content.
   - Use the original transparent application logo directly on the composition background unless an existing brand system explicitly defines a container. Do not add a dark tile, badge, or frame by default.
   - When the repository has multiple README languages, generate one localized hero per README from a shared layout source. Keep geometry, screenshot order, logo treatment, and visual hierarchy identical; localize only verified copy and typography adjustments.
   - Match the language inside product screenshots to the destination README whenever the application supports that locale. A localized headline over screenshots from another language does not count as a localized hero.
   - Use stable language-qualified filenames such as `product-hero-zh.png` and `product-hero-en.png`, and point each README only to its matching language asset.
   - Preserve the complete product window. Never use `object-fit: cover`, clipping, masks, or manual crops merely to force a screenshot into the reference frame ratio.
   - When source and reference aspect ratios differ, recapture the real application at the target ratio. If recapture is impossible, use proportional `contain` scaling and disclose the resulting empty space; do not silently remove interface content.
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

- Use a single hero image when the README needs immediate visual identity.
- Use two or three screenshots by default, but follow the reference when a screenshot collage is an explicit part of the requested design.
- Use an abstract generated hero when exact UI would be risky or inaccurate; pair it with real screenshots below.
- Stop and ask for direction only if an unverified visual claim, brand rule, or missing source asset would materially change the result.
