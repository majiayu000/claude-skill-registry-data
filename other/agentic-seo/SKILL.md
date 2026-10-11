---
name: agentic-seo
description: "Audit and implement SEO for a website: meta tags, canonical URLs, Open Graph, X/Twitter cards, JSON-LD structured data, sitemap and robots controls. Use when auditing a site's SEO, adding or fixing meta tags or structured data, or checking how a site appears in search and AI answers."
allowed-tools: Read Write Edit Bash Glob Grep WebFetch
compatibility: The build audit script needs Python 3 (standard library only)
user-invocable: true
argument-hint: "[audit|implement|structured-data|llms-txt|crawler-controls|checklist|audit-build] [target]"
metadata:
  author: 23blocks
  version: 2.2.0
---

# Agentic SEO

Repeatable workflow for auditing and implementing SEO on a web page. Standard SEO practice applies; the reference files hold the checks, templates and decisions specific to this skill.

## First-Time Setup: Gather Site Configuration

**Before running any sub-command for the first time in a session**, ask the user for their website details if not already known. Store these as working context:

| Setting | Ask For | Example |
|---------|---------|---------|
| **Site Name** | "What is your site/company name?" | `Acme Corp` |
| **Domain** | "What is your website domain?" | `https://acme.com` |
| **X/Twitter Handle** | "What is your X/Twitter handle?" (optional) | `@acme_corp` |
| **Social Image Path** | "Where are your social sharing images stored?" | `/assets/social/` |
| **Social Links** | "Any social profile URLs?" (optional) | Twitter, GitHub, LinkedIn URLs |
| **Framework** | "What framework is your site built with?" | Angular, React, Next.js, etc. |
| **Build Output Path** | "Where does your built/prerendered HTML output to?" | `dist/apps/web/browser/` |
| **Sitemap Path** | "Where is your sitemap.xml?" | `public/sitemap.xml` |

If the project has a CLAUDE.md with SEO patterns already defined, read it and extract these values automatically instead of asking.

Use these values as `{SITE_NAME}`, `{DOMAIN}`, `{TWITTER_HANDLE}`, `{SOCIAL_IMAGE_PATH}`, `{BUILD_OUTPUT}`, `{SITEMAP_PATH}` throughout all sub-commands.

## When to use this skill

Trigger this skill when:
- A **new page** is created and needs SEO implementation
- An **SEO audit** is requested on an existing page
- **Structured data** (JSON-LD) needs to be added or updated
- **llms.txt** or **llms-full.txt** needs maintenance
- A quick **checklist** verification is needed before deploying
- A page is missing meta tags, OG tags, canonical URL, or sitemap entry

## What Google says about AI search

Dated 2026-10-10: Google's guide "Optimizing your website for generative AI features on Google Search" (https://developers.google.com/search/docs/fundamentals/ai-optimization-guide, last updated 2026-07-10) says you don't need new machine readable files, AI text files, markup or Markdown to appear in Google Search; structured data isn't required for generative AI search and there is no special schema.org markup to add; Google Search doesn't use llms.txt, and having one neither harms nor helps visibility or rankings there; content does not need to be broken into tiny pieces. Standard SEO applies; re-check the guide before relying on this.

For performance, measure the Core Web Vitals (LCP, INP, CLS; https://web.dev/articles/vitals) rather than asking for "fast load times".

## Sub-Commands

| Command | Description | Reference |
|---------|-------------|-----------|
| `audit [path]` | Audit one page's source (component and template): pass/fail table | `reference/audit.md` |
| `implement [path]` | Implement SEO on a new page from scratch (Angular example; adapt to the framework) | `reference/implement.md` |
| `structured-data [path]` | Add or update JSON-LD | `reference/structured-data.md` |
| `llms-txt` | Maintain llms.txt, only if the owner wants it | `reference/llms-txt.md` |
| `crawler-controls` | Decide what Google and AI vendor crawlers may use (neutral guide) | `reference/crawler-controls.md` |
| `checklist [path]` | Quick 15-item check against one page's built HTML | `reference/checklist.md` |
| `audit-build [dir]` | Audit every page of the built HTML of a whole site, optionally diffed against the live build; framework-agnostic | `reference/audit-build.md` |

`audit` reads the source of one page; `audit-build` reads the built HTML of every page. With no sub-command, default to `audit` on the target path. Use `audit-build` when a change touches many pages (a rebuild, a migration, a redesign) or when you need to know what it does to pages that already rank.

## Running the build audit script

`scripts/audit_build.py` is executed, not read into context. Python 3 standard library only.

```bash
python3 scripts/audit_build.py BUILD_DIR --domain {DOMAIN} [--baseline BASE_DIR] [--csv out.csv] [--twitter-handle @handle] [--strict-claims]
python3 scripts/audit_build.py --self-test
```

Exit codes: `0` no page failed a hard check and no site-wide issue was found; `1` at least one page failed a hard check or a site-wide issue was found; `2` bad arguments (missing `BUILD_DIR` or `--domain`). An unreadable file stops the run with a message naming it. Run `--self-test` after changing the script.

## Implementation

Follow `reference/implement.md` for the per-page steps (meta tags, canonical link, JSON-LD, sitemap, prerender). In any framework, JSON-LD must be rendered during SSR/SSG (no browser-only guard) and removed when the component is destroyed.

## Done means validated

Before reporting done, run `audit` or `checklist` on the built page, then run Google's Rich Results Test and the Schema Markup Validator on it and fix errors.

## Anti-Patterns

- **Schema for its own sake**: add structured data only when it matches visible content; never add a schema to reach a count.
- **Inaccurate `lastmod`**: set it only when the page content really changed.
- **Hardcoded dates**: use the real modification date for `dateModified`.
