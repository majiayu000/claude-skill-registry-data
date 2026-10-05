---
name: quiet-signal-xhs
description: Turn Chinese text, articles, URLs, or user-defined page plans into polished 1080×1440 Xiaohongshu image-card series in the Quiet Signal visual language. Use when creating, revising, rendering, or visually auditing 小红书图文; use quiet-signal-design alone for non-Xiaohongshu design work.
---

# Quiet Signal 小红书

This is the production entry point for Quiet Signal Xiaohongshu image-card series. It handles the platform-specific work that the core visual skill deliberately leaves open: necessary content understanding, pagination, 3:4 composition, implementation, rendering, and final visual QA.

## Required references

Before working on a task:

1. Read `../quiet-signal-design/references/SPEC.md` completely. This is the visual identity source of truth. If it is unavailable, report the missing dependency instead of silently inventing a replacement style.
2. Read [references/SPEC.md](references/SPEC.md) completely. This is the Xiaohongshu medium specification.
3. For a new creation or substantial redesign, read [references/DEMOS.md](references/DEMOS.md) and inspect the most relevant one or two demo contact sheets. Use them as visual evidence, never as fixed templates.
4. Before implementing that creation or redesign, read [references/IMPLEMENTATIONS.md](references/IMPLEMENTATIONS.md) and the actual `index.html`, `styles.css`, and `app.js` for the same selected demo or demos. The implementation is required evidence for type scale, spacing, composition mechanics, image treatment, and rendering structure; adapt those methods without copying a fixed page layout.

## Work from the input state

- If the user has fixed the copy, order, page count, or individual pages, preserve those decisions and design the remaining degrees of freedom.
- If the input is an unpaginated passage, article, or URL, do only the understanding, extraction, and pagination needed to make the series coherent. Do not turn it into a different article or impose an external agent workflow.
- Preserve facts, qualifications, sources, image credits, and user-locked wording. Verify unstable facts when current accuracy matters.
- Let the relationship in the content determine each page expression: sequence, comparison, conditions, mechanism, evidence, checklist, warning, or another structure justified by the material.

## Produce the actual deliverable

- Default to `1080 × 1440` (`3:4`) unless the user explicitly overrides the format.
- Create editable source plus final PNGs. Keep the rendering deterministic enough that revisions can be reproduced.
- Use images only when they have a clear role such as subject, evidence, context, route, or explanation. Keep source and credit information when required.
- Keep the Quiet Signal identity stable across the series while allowing compositions to vary with meaning.

## Inspect the rendered result

Render every page and inspect both individual pages and a contact sheet. Do not judge only from HTML, CSS, or container coordinates.

Before delivery, confirm:

- every output is exactly 3:4 and has no clipping or overflow;
- the main judgment and reading path of each page are clear;
- short content has not been inflated into large empty containers;
- no large lower or side region is left without a deliberate role;
- images, arrows, labels, and other relationship-bearing objects are visually centered and aligned in the final pixels;
- the pages belong to one system without mechanically repeating one layout;
- sources and limitations remain legible.

If a page fails, make the smallest structural correction and render again.

## Boundaries

- This skill creates and audits Xiaohongshu image cards; it does not publish them unless the user separately asks and authorizes publishing.
- Do not promote a one-off composition into the specification without explicit user approval.
- Do not copy a demo page merely because the topic is similar. Match the content relationship first.
- Do not expand a local layout issue into a mandatory motif for every page.
