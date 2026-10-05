---
name: seo-video
description: Use when auditing or planning video discovery and indexing across watch pages, embedded players, thumbnails, VideoObject markup, video sitemaps, transcripts, captions, Key Moments, livestreams, locale variants, and first-party video indexing reports; require captured player/page evidence and never promise video indexing, rich results, views, citations, or watch time.
---

# Video SEO

Audit whether a video and its watch page are understandable, accessible, discoverable, indexable where eligible, and supported by truthful metadata.

Read [video-evidence-protocol.md](references/video-evidence-protocol.md) before a formal audit.

## Procedure

1. Define the video catalog, hosting/player system, watch-page model, locales, live/VOD status, owners, and target surfaces.
2. Capture representative watch pages in raw and rendered form, player availability, stable video/thumbnail URLs, HTTP behavior, canonical/index directives, visible title/description, transcript/captions, and structured data.
3. Reconcile visible facts with VideoObject/BroadcastEvent/Clip/SeekToAction fields, upload/publication dates, duration, embed policy, regions, livestream state, and thumbnails.
4. Inspect video sitemap entries, lastmod and live-state updates, internal discovery, responsive playback, lazy loading, thumbnail eligibility, and content that is hidden behind interaction or authentication.
5. Use authorized Search Console/Bing/video-platform reports when supplied. Distinguish page indexing, video indexing, rich-result eligibility, impressions, plays, and engagement.
6. Validate transcripts/captions as accessibility and content evidence; do not keyword-stuff them. Route page copy to `seo-content`, schema to `seo-schema`, media performance to `seo-images`/`seo-technical`, and regional mappings to `seo-hreflang`.
7. Package findings as SEO Findings `1.1.0` with `video`, `web_page`, `media_set`, or `sitemap` targets and `video`, `media`, `structured-data`, `technical`, or `freshness` categories.

## Guardrails

Never invent transcripts, captions, thumbnails, dates, duration, view counts, indexing reports, or player access. Do not claim that VideoObject or a video sitemap guarantees indexing or placement.

## Formal evidence handoff

Package only supported observations as SEO Findings `1.1.0`. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout, then run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Keep the handoff provisional until this command passes.

## Output

Return the video inventory/sample, watch-page/player evidence, metadata parity, sitemap/indexing findings, accessibility and performance risks, owners, verification, rollback, and limitations.
