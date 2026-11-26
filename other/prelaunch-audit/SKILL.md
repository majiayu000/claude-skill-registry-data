---
name: prelaunch-audit
description: Get a website production-ready in one pass - finds and fixes bugs, security holes, missing legal pages, SEO gaps, accessibility and speed problems, then load-tests and attacks it locally, and checks 20 signs of a "vibe-coded" site. Use when the user says "audit this site", "make it production-ready", "review before launch", "launch checklist", "will it handle traffic?" or "look for vulnerabilities" on their own or a client's site.
author: sant1jmnz
tags:
  - web
  - security
  - seo
---

# Pre-launch audit

Leaves a website ready for production. **Not included:** UI/UX redesign or building a new backend; those are separate requests.

## Rules

- Only your own sites or clients' sites with permission. Attacks and load **only against localhost or staging**, never production or third parties (payment providers, Google, etc.).
- Fix what you find; don't commit, push or deploy without OK.
- Nothing invented: if legal data is missing (company name, tax ID), mark it as pending.
- Report with evidence (command + result), not "it should work".

## Order of work

1. **Read** the project's CLAUDE.md/README, `git status`, routes and environment variables.
2. **Baseline**: types, lint, production build, `npm audit --omit=dev`.
3. **Checklist** (table below): verify each item in the code and on the running site.
4. **Security**: read every API/server route in full, then attack it with `curl`.
5. **Load**: run the production build locally and measure.
6. **Fix**, re-run 2–5, and deliver the report.

## Checklist

| Item | How to check |
|---|---|
| Terms / legal notice | Own page, linked in the footer and in the form where they're accepted |
| Privacy policy | Controller, data, purpose, third parties, rights (follow the local data-protection law) |
| Cookies | List the real cookies. With no tracking cookies, no banner is needed: a section in the privacy policy is enough |
| HTTPS enforced | HSTS + `upgrade-insecure-requests`; hosting redirects http→https |
| Titles and descriptions | One per page, unique; Open Graph with a 1200×630 image |
| Structured data | JSON-LD for the business type with address, hours, phone (same as visible) |
| sitemap.xml and robots.txt | Exist, with the real domain; private pages `noindex` + `Disallow` |
| Google Business Profile | Not visible from the code: search the business on Maps and confirm it links to the site. Owner's task |
| Favicon | SVG + 180×180 PNG for iOS |
| Alt text | Every `<img>` has a descriptive `alt` (check the DOM, not only grep) |
| Images | WebP/AVIF, reasonable weight, main image with `loading="eager"` and `fetchpriority="high"` |
| Speed | Lighthouse on the production build; no artificial delays or extra blocking fonts |
| Contrast | Lighthouse accessibility; text ≥ 4.5:1 |
| Mobile | 375 px: no horizontal overflow (measure per element), touch targets ≥ 44 px |
| Custom 404 | Returns **status 404** and offers ways out (home, main action, contact) |
| Broken links | Internal against the real routes; external with `curl -I` |
| Forms vs. spam | Per-IP rate limit on every public route, body size cap, server-side validation |
| Contact button | Floating chat/WhatsApp button that doesn't cover the main action |
| Analytics | Installed; prefer a cookieless one (no banner needed) |
| One call to action | A single primary button repeated; the rest secondary |

## Security: what to look for in each route

- Input: is everything validated on the server? Is any raw field forwarded to a third party? Length and body caps?
- Money: does the server set the amount? Can a payment be used for only one purchase, even with two simultaneous requests? Is the refund idempotent?
- Access: can you read or change someone else's data by changing an id, email or cookie (IDOR)?
- Business rules: valid hours, dates and prices checked on the server, not only in the form.
- Secrets: no keys in the browser bundle; constant-time comparison; signed tokens with expiry.
- Output: HTML escaped in emails and pages; never build links from the `Host` header.
- Abuse: rate limit on everything that costs money or quota (payments, email, AI, external APIs).
- AI: filter roles in the history (user/assistant only), cap output tokens.
- Headers: CSP, HSTS, `X-Frame-Options`, `nosniff`, `no-store` on the API.
- Errors: visitors see a fixed message, never the internal error text.

Minimum `curl` attacks against localhost: tampered amount, reused payment, date/time outside the rules, HTML and `\r\n` in fields, huge body, malformed cookie, someone else's id, fake token, burst to see the 429.

## Load

```bash
npx -y autocannon -c 200 -d 15 http://127.0.0.1:PORT/
```

Run against the local production build, on the home page and one API route. Look at errors and p99 latency. Always say it measures a single local process: on serverless the host scales, and the real bottleneck is external APIs (quotas) and whatever isn't cached.

## Final report

Short: what was fixed (with file), what's pending and who it depends on, and the load-test numbers. Separate "critical" from "improvement".

## 20 signs of a "vibe-coded" site (commit none)

Check one by one on the running site, on top of the checklist:

1. `*.vercel.app` (or similar) URL instead of an own domain.
2. Empty "view source": HTML must arrive with content (SSR or prerender), not a bare `<div id="root">`.
3. No 404 page.
4. Everything client-side Vite + React, no server rendering.
5. The same title on every page.
6. No meta description.
7. No Open Graph image.
8. No structured data.
9. Several `<h1>` per page.
10. No `<h1>`.
11. No canonical tag.
12. No `llms.txt`.
13. `robots.txt` blocking AI crawlers. Instead, explicitly allow GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc., so AI assistants recommend the site.
14. No favicon.
15. No sitemap.
16. No language attribute (`<html lang>`).
17. Images without alt text.
18. Source maps published in production.
19. Console errors.
20. Huge `bundle.js`: measure the initial JS and split it if needed.

## Tools to combine with

- `security-bounty-hunter`: think like an attacker over the code (real routes, user-controlled input, demonstrable impact).
- `design-taste-frontend`: for the visual side when the audit includes UI/UX.
- Shannon or Strix (`usestrix/strix`): automated pentest against localhost or staging. Need Docker.
- `samber/cc-skills@site-launch-checklist`: longer checklist (directories, Product Hunt, GDPR), aimed at SaaS.
