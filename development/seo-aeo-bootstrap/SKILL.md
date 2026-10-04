---
name: seo-aeo-bootstrap
description: Ship the SEO + AEO foundation (Google/Bing/Yandex + ChatGPT/Claude/Perplexity) into a Hamzaish product. Adds llms.txt, AI-bot-friendly robots.txt, FAQPage/SoftwareApplication JSON-LD, sitemap, and the meta head block.
---

# /seo-aeo-bootstrap

Usage: `/seo-aeo-bootstrap <product-slug>`

Example: `/seo-aeo-bootstrap muakkil` — scaffolds the SEO+AEO foundation for the Muakkil product.

## What this does

Implements the eight-piece foundation from `factory/playbooks/launch-stage/seo-aeo-foundation.md`:

1. `<title>` + `meta description` (keyword-honest)
2. Open Graph + Twitter Card
3. JSON-LD graph: Person → Organization → WebSite → WebPage → SoftwareApplication → FAQPage
4. `/llms.txt` — markdown summary for LLM ingestion
5. `robots.txt` — explicit allowlist for AI crawlers
6. `sitemap.xml`
7. Canonical, language, robots metas
8. Sane heading hierarchy

## What you do as the assistant

1. **Read the product config first.** Open `products/<slug>/product.config.json` and `products/<slug>/scope.md`. You need:
   - Product name + one-line value prop
   - Founder name + LinkedIn (default to Hamza unless config overrides)
   - Domain (from `code-paths.local.json` if missing, ask)
   - 1-paragraph "what it does" + "who it's for"
   - Code repo URL
   - License (default MIT)
   - Whether it's a tool/SaaS (→ `SoftwareApplication`) or content site (→ `WebSite` only)

2. **Locate the source.** Read `code-paths.local.json` for the local code path. The skill operates inside `app/` (Next.js) or whatever the framework root is.

3. **Generate the head block** from the template at `factory/skills/seo-aeo-bootstrap/templates/head.html.tmpl`. Substitute every `{{var}}` from product config.

4. **Generate `llms.txt`** from `factory/skills/seo-aeo-bootstrap/templates/llms.txt.tmpl`. Same substitution pattern. Place at site root (Next.js: `public/llms.txt`).

5. **Generate `robots.txt`** from `factory/skills/seo-aeo-bootstrap/templates/robots.txt.tmpl`. Site root (`public/robots.txt`).

6. **Generate `sitemap.xml`** from `factory/skills/seo-aeo-bootstrap/templates/sitemap.xml.tmpl`. Site root. If Next.js with dynamic routes, scaffold a `app/sitemap.ts` instead.

7. **Pre-flight check.** Before declaring done, run:
   - JSON-LD parses (`python3 -c "import json; json.loads(...)"`)
   - `<head>` has exactly one `<h1>` referenced (search the body)
   - All `{{vars}}` are substituted (`grep '{{' app/`)
   - Title ≤ 60 chars, description ≤ 160 chars

8. **Document the decision.** Append a line to `products/<slug>/decisions/` with: "SEO+AEO foundation shipped via /seo-aeo-bootstrap. Schemas: Person, Organization, WebSite, WebPage, SoftwareApplication, FAQPage. llms.txt at root."

## What this does NOT do

- Doesn't write content (that's the founder's job)
- Doesn't generate FAQ answers (you need real visitor questions, not made-up ones — but the template includes 6 generic question prompts the founder should answer manually before launch)
- Doesn't do keyword research (use `/keyword-research` later)
- Doesn't publish cornerstone content (`/launch-plan` covers that)

## Validation gate

The skill is **complete** only when all six pre-launch checks from the playbook pass:

- [ ] Rich Results test (Google) → all schemas valid
- [ ] `/llms.txt` returns markdown
- [ ] `/robots.txt` lists AI bots
- [ ] View source → exactly one `<h1>`, title ≤60ch, desc ≤160ch
- [ ] `curl -A "GPTBot" <url>` → 200
- [ ] Open Graph debugger → image + title + description correct

If any fail, print the failure and prompt the founder to fix before re-running.

## Templates

See `templates/` adjacent to this SKILL.md:
- `head.html.tmpl` — full `<head>` block (metas + JSON-LD)
- `llms.txt.tmpl` — markdown summary
- `robots.txt.tmpl` — AI-friendly crawler allowlist
- `sitemap.xml.tmpl` — minimal sitemap

## Source

Codifies the SEO+AEO foundation shipped on hamzaish.com on 2026-06-06. Playbook: `factory/playbooks/launch-stage/seo-aeo-foundation.md`.
