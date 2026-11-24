---
name: seo-design
description: "Structure crawlers and readers understand the same way."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, seo]
    category: web
    related_skills: [web-design, ux-copywriting, performance-design]
    web_designer_stages: [copy, build]
---

# SEO-Aware Design Skill

This skill makes pages that search engines can crawl, render, and understand: semantic HTML, one h1 with logical h2/h3, unique titles and meta descriptions, descriptive link text, text as text, canonical URLs, and JSON-LD structured data matching visible content. It covers the structure and metadata built into the page itself. It does not write the page's copy — the copy stage owns that — and it does not do off-page work such as link building. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- For every public page, from the first HTML structure — not as metadata added afterwards.
- When a page's title, description, heading outline, or structured data is being decided.
- When content is at risk of being baked into images, where crawlers and readers cannot see it.

It is NOT for:

- Writing headlines or body copy — that is the copy stage.
- Off-page SEO: link building, listings, or promotion.
- Keyword strategy; it covers the structure that makes a page understandable, not which terms to target.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage(s).
- The copy stage records each page's title and meta description, so uniqueness can be checked across pages.
- The build stage is in progress or complete, so the semantic structure is checked in the built pages.

## How to Run

1. Emit semantic landmarks in the build itself: header, nav, main, footer, article, section.
2. Give each page one h1 with logical h2/h3 beneath it — the same outline a screen reader reads.
3. Write a unique `<title>` per page, primary topic first, and a unique meta description per page.
4. Write descriptive link text; never 'click here'.
5. Keep text as text, not baked into images.
6. Set canonical URLs and add JSON-LD structured data (Schema.org: Article, Product, Organization, BreadcrumbList) only for content actually on the page, validated in Rich Results Test.
7. Record the titles, descriptions, and structured data in the copy record and the build log, then hand the work to the judger; do not grade it here.

## Quick Reference

- Semantic HTML: header, nav, main, footer, article, section.
- One h1 per page, logical h2/h3.
- Unique `<title>` per page (primary topic first) and unique meta description per page.
- Descriptive link text; text as text, never baked into images.
- Canonical URLs.
- JSON-LD structured data (Schema.org: Article, Product, Organization, BreadcrumbList) matching visible content, validated in Rich Results Test.

## Procedure

### 1. What it is

Design that search engines can crawl, render and understand: semantic HTML (header/nav/main/footer/article/section), one h1 per page with logical h2/h3, unique <title> (primary topic first) and meta description per page, descriptive link text, text as text (not baked into images), canonical URLs, and JSON-LD structured data (Schema.org: Article/Product/Organization/BreadcrumbList) matching visible content, validated in Rich Results Test.

### 2. How Hermes applies it

Hermes emits semantic landmarks and heading order in the build itself, writes unique titles/descriptions, adds JSON-LD only for content actually on the page, and its judger checks crawlability, heading outline and structured-data validity.

### 3. What it returns to the stage

- `copy` stage — `pages`: each page records its unique title and meta description. `meta`: the per-page metadata, including canonical URLs and structured-data notes.
- `build` stage — `files`: the built pages carry the semantic landmarks, heading order, and JSON-LD. `build_log`: notes the structured data added per page. `token_drift`: nothing new; SEO adds no tokens.

### 4. Good looks like

A crawler and a screen reader read the same clear outline; each page has a unique title/description; rich results are eligible, not guaranteed, and markup matches what the user sees.

## Pitfalls

- Text baked into images, invisible to crawlers and to screen readers.
- Duplicate titles or meta descriptions across pages.
- Structured data for content that is not actually on the page — markup must match what the user sees.
- A title that buries the primary topic, or a meta description copied from another page.
- Heading levels skipped, or more than one h1, so the outline a crawler reads is not the outline a reader sees.
- Metadata added afterwards as a patch, instead of built into the page's structure from the start.
- Claiming rich results as guaranteed; structured data makes a page eligible, not entitled.

## Verification

- A crawler and a screen reader read the same clear outline: one h1, logical h2/h3, semantic landmarks.
- Every page has a unique title and meta description; link text is descriptive.
- Structured data validates in Rich Results Test and matches the visible content.
- The content judger checks crawlability, heading outline, and structured-data validity; the skill does the work and the judger checks it. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: copy, build. Returns: `copy` — `pages`, `meta`; `build` — `files`, `build_log`, `token_drift`. Judger boundary: content judger checks crawlability, heading outline, and structured-data validity.
