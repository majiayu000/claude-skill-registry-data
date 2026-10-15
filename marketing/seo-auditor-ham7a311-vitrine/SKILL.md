---
name: seo-auditor
description: Audit on-page SEO page by page - title tags, meta descriptions, heading outline, semantic HTML, internal links, image alt text, content hierarchy and search intent - and write the exact replacement for each problem. Use before launch, after a redesign, or when pages don't appear for the searches they should.
---

# /seo-auditor

This is about what each page says and how it is structured. For crawling, sitemaps, canonicals and structured data, run `/technical-seo-audit`. Nothing here guarantees rankings; it removes the reasons a good page gets misread.

## 0. Inventory first

- List every indexable route (from the sitemap, the router, or a crawl). For each, record: URL, `<title>`, meta description, `h1`, the `h2` outline, word count, and inbound internal links.
- Put it in a table. Most problems are only visible side by side: duplicate titles, empty descriptions, orphan pages.

## 1. Search intent, per page

- For each page write one line: *who searches for this, with what words, wanting what?* ("a developer searching 'react glass button' wants a copyable component and its code").
- **Pass when** the `h1`, the first paragraph and the first screen answer that intent directly. A page that needs scrolling before it says what it is fails.
- If two pages answer the same intent, merge them or make one clearly different. They compete with each other otherwise.

## 2. Titles

- 50–60 characters, unique per page, the page's subject first, brand last: `Silk Field — React WebGL background · Vitrine`.
- Generated pages (products, components, posts) build the title from real data, never a fixed string. Check that 100 generated pages give 100 different titles.
- **Fix format:** write the new title for every failing page, not a rule.

## 3. Meta descriptions

- 120–160 characters, a plain sentence describing what's on the page and what you can do there. No keyword lists, no "Welcome to".
- Unique per page. On generated pages use the item's own description; fall back to a template only if it includes the item's name and category.

## 4. Headings and semantics

- Exactly one `h1`, which matches the page's subject (it can differ from the title in wording).
- `h2`/`h3` form an outline you could read alone. Never skip levels for styling; style the right level instead.
- Landmarks exist: `header`, `nav`, `main`, `footer`. Lists are `ul`/`ol`, navigation is links (`<a href>`), actions are buttons. Search engines and screen readers read the same structure.
- Content that matters is in the HTML on first load, not only after a click or a client-side fetch.

## 5. Internal links

- Every important page is reachable in ≤ 3 clicks from the home page and has at least 2 inbound links from relevant pages.
- Anchor text describes the target ("glass buttons", not "click here" or "more").
- Related pages link to each other (a component links to its category and to recipes that use it; a category links to its components).
- **Find orphans:** pages in the sitemap with zero inbound internal links.

## 6. Images

- Informative images have `alt` text that says what the image shows in context. Decorative images (backgrounds, flourishes) have `alt=""`.
- Use descriptive file names and real `width`/`height` so they don't shift layout.

## 7. Content hierarchy

- The most important thing on the page is the most visible, and appears first in the source order.
- Thin pages (a heading and a widget) get a sentence or two of real explanation: what it is, when to use it, what makes it different.

## Output

A table: URL · problem · current value · replacement. Then apply the fixes, re-run the inventory, and confirm every row passes.
