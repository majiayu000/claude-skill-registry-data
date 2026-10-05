---
name: seo-audit
description: "Behind-the-scenes SEO sweep of the website: page metadata, canonicals, sitemap, robots, social preview tags, structured data. Verifies the rendered HTML, fixes technical issues on a local branch, and a clean pass is a valid outcome. Use when asked to run the SEO audit or check the site's SEO. Never pushes, merges, or deploys."
icon: travel_explore
displayDescription: "Sweeps the technical SEO surface of the site: page titles and descriptions, canonical URLs, the sitemap and robots rules, social preview tags, and structured data. It checks the HTML the server actually sends rather than trusting the source, fixes what it finds on a branch for approval, and reports a clean pass when there is nothing worth changing."
invoke: ["run the SEO audit","/seo-audit"]
---

# seo-audit

A recurring optimizer sweep over the website's technical SEO, in the same spirit as the growth loop: each run inspects everything a crawler or link unfurler sees, fixes what is safely fixable on a local branch, and reports for approval. **A run that finds nothing to fix is a valid outcome** — say so briefly and stop; never invent a change to have something to ship.

## When invoked

Run when asked to "run the SEO audit" (`/seo-audit`).

## Scope guardrails (read first)

- **Behind the scenes only.** Head metadata, crawl/index surfaces, link unfurl tags, structured data, redirects, internal-link integrity. Nothing a sighted visitor sees changes: no layout, no CSS, no component structure, no visible copy. (Meta titles and descriptions are in scope — they render in search results, not on the page.)
- **Crawl-policy changes are report-only.** Anything that changes what gets indexed or where the canonical site lives (robots rules, `noindex`, canonical host, redirect policy) gets proposed in the report, not implemented — unless it is an outright bug, like a page accidentally marked `noindex`.
- **Local branch only.** Never push, merge, or deploy; never touch the user's working tree. Follow the temporary-worktree recipe in `.claude/skills/growth-loop/SKILL.md` (step 4), with branch name `seo/YYYY-MM-DD-<slug>`. Skip the worktree entirely on a clean pass.
- **No hardcoded facts.** New metadata prose follows `content-design.md`; anything countable derives from a registry (see CLAUDE.md — never write a component count into a meta description).

## The sweep

### 1. Inventory the surfaces

The crawl/index surface lives in `website/src/app/`: the root `layout.tsx` (site-wide metadata and `metadataBase`), `sitemap.ts`, `robots.ts`, `manifest.ts`, `opengraph-image.tsx`, `icon.tsx` and `apple-icon.tsx`, and the `llms.txt` route — plus the structured data the layout injects, built in `website/src/lib/structuredData.ts` (its `sameAs` derives from `website/src/config/social.ts`). Per-page metadata comes from each page's `layout.tsx`; component pages derive theirs from the registry via `componentPageMetadata`. Read these fresh each run — the list above says where to look, not what is there.

### 2. Verify the rendered output, not the source

Build the site (`npm run build` in `website/`), then serve it via the `website-prod` entry in `.claude/launch.json` — it wraps `npm run start` and takes any assigned port, so it never collides with a running dev server; read the port from what it reports. Then fetch the served HTML — plain HTTP requests are enough; no browser needed. Sample every section of the site (at least one page per top-level route group, plus the home page and one component page), and fetch the sitemap, robots, and manifest routes directly. For each sampled page check the `<head>`:

- Title present, unique across pages, and following the site's title template.
- Meta description present, sensible length (~70–160 characters), and specific to the page.
- Canonical URL correct — one canonical host, no duplicate-content splits.
- Open Graph and Twitter card tags complete enough for a clean unfurl (title, description, image, type, url).
- No accidental `noindex`/`nofollow`; viewport and charset present.
- Structured data (JSON-LD) valid where present; note opportunities where a page type clearly warrants it (e.g. article markup on writing pages).

### 3. Cross-check the crawl graph

- Every public route appears in the sitemap, and every sitemap URL returns 200 from the running server. Registry-driven collections (components, case studies, writing) must be complete in it — if one is missing, the fix belongs in how `sitemap.ts` derives the list, not in a hand-added entry. Nav-linked does not imply sitemap-listed: a deliberately noindex page may sit in the nav (its own metadata comment is the record of that decision), and it stays out of the sitemap by design.
- Robots rules and the sitemap agree (nothing disallowed that the sitemap advertises).
- Internal links resolve: no anchors pointing at routes that 404. (Largely already automated: `scripts/validate-internal-links.mjs` enforces this on every build for prerendered hrefs — spend the crawl on what it cannot see: external links, redirect chains, and the live HTTP status of anything client-rendered.)
- The 404 page itself returns HTTP 404, not 200.

### 4. Fix, verify, hand off

Apply the mechanical, clearly-safe fixes in one coherent batch on the branch; leave judgment calls (crawl policy, new structured-data strategy, description rewrites that change meaning) as proposals in the report. Verify the website build passes in the worktree before committing. Metadata edits are page prose, so the build regenerates the site chat's corpus (`website/src/data/site-corpus.generated.ts`) — commit the regenerated file in the same batch (see the commit-scope rule in the growth-loop recipe), then remove the worktree (the branch survives).

Where a finding is deliberately not a bug — a page intentionally out of the sitemap, an intentionally bare head — record why in a short comment at the site of the decision, so future runs read the reason instead of re-flagging it.

### 5. Report

Repeat the full report in the final message (no report file — the in-place comments from step 4 are the durable record). Plain English, findings grouped as **fixed on the branch** (with before → after), **proposed** (needs a decision), and **checked clean** (what was verified and passed). End with the branch name if one exists, confirmation the build passed, and the reminder that nothing is pushed or deployed: merging the branch (or saying `ship`) approves it; deleting it rejects it.
