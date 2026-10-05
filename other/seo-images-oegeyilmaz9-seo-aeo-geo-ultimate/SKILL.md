---
name: seo-images
description: Use when reviewing image accessibility, discoverability, metadata, responsive delivery, image sitemaps, or visual performance from a page/media inventory; provide evidence-linked improvements without keyword, format, or ranking guarantees.
---

# SEO Images

## Purpose

Improve the way meaningful visual assets are understood and delivered to people and crawlers. This skill separates accessibility, rendering/performance, asset rights, and image-search discoverability instead of treating them as one score.

Read `references/image-review-protocol.md` before preparing a formal media recommendation.

## Input gate

Require the rendered page or asset inventory, image purpose/context, source URL, intrinsic dimensions/format/size, delivery behavior, locale, accessibility context, and any available field/lab evidence. Ask who owns the image/license and whether an image is content, UI decoration, hero/LCP candidate, product/media asset, or purely decorative.

Do not infer file format, dimensions, loading behavior, or user impact from a filename. Do not recommend an image or alt text without seeing its page context.

## Workflow

1. **Inventory by purpose.** Map each material image to the visible topic, page region, adjacent text/caption, owner/license, and delivery URL. Mark decorative images as decorative rather than inventing alt text.
2. **Review accessibility.** Check meaningful alternative text, captions/nearby explanation, controls, contrast/legibility where text is embedded, and responsive mobile rendering. Alt text explains the image’s purpose in context; it is not a keyword field.
3. **Review delivery.** Inspect dimensions, responsive candidates, intrinsic width/height or aspect-ratio reservation, loading priority, lazy loading behavior, cache/CDN policy, and actual LCP/CLS/interaction evidence when available. A newer format is not automatically an improvement; evaluate support, source quality, byte savings, and visual fidelity.
4. **Review discovery/metadata.** Check whether significant images are reachable in rendered content and whether page context, canonical URLs, structured data, and image sitemap use are truthful and relevant. Route structured data to `seo-schema` and sitemap changes to `seo-sitemap`.
5. **Plan safe changes.** For each action name the asset/template scope, owner, accessibility/content review, visual QA, performance test, approval, and rollback. Send systemic delivery changes through `seo-action-plan`.

## Guardrails

- Do not use keyword-stuffed alt text, duplicate captions, decorative image descriptions, fake EXIF metadata, or image sitemap stuffing.
- Do not promise image search visibility, page ranking, Core Web Vitals, or conversion improvement.
- Respect licenses, consent, privacy, and brand requirements. Do not expose internal image URLs or generate derivative assets without authorization.
- Keep image discovery, user accessibility, and rendering performance as separate verifications.

## Formal evidence handoff

When this work needs a cross-team, approval-ready plan, package evidence-bound findings as an immutable `seo-findings.json` bundle using the checked-out suite contract. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout. Keep every referenced capture/source below `raw/`, retain declined claims and limitations, and run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Send only a passing bundle to `seo-action-plan`; otherwise label the handoff `provisional`.

## Output

Return a media inventory with observations, accessibility/performance/discovery recommendations, source-aware implementation notes, test path, and rollback. Provide alt-text or caption options only with visible context and label them as reviewable suggestions.
