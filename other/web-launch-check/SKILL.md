---
name: web-launch-check
description: "Pre-launch audit for any website. Verifies privacy policy, ToS, cookie consent, sessions, sitemap, robots.txt, SEO meta tags, structured data, accessibility (WCAG AA), Core Web Vitals, and compliance frameworks (GDPR/CCPA). Returns severity-graded findings with a GO / NO-GO verdict."
---

# /web-launch-check

Run this **before any production website launch** to catch missing legal pages, broken SEO, accessibility violations, or compliance gaps that would expose the user to legal risk or hurt search ranking.

## When to use

- Before pushing a marketing site, landing page, or web app to production.
- After a major redesign that changed page structure, routes, or third-party integrations.
- Before adding analytics or tracking scripts.
- When taking over an existing site to assess current state.

## What it checks

### Layer 1 — Legal pages (CRITICAL — block launch)

| Page | Path checked | Required when |
|---|---|---|
| Privacy Policy | `/privacy`, `/privacy-policy`, footer link | Always (any data collection, including cookies/IP) |
| Terms of Service | `/terms`, `/tos`, `/terms-of-service` | Any signup, transaction, or user-generated content |
| Cookie Policy | `/cookies`, section in `/privacy` | EU/UK visitors, or any non-essential cookies |
| Contact / Address | `/contact`, footer | EU jurisdictions (Impressum, EU consumer law); always recommended |
| Refund / Cancellation | `/refunds`, `/cancellation` | Any e-commerce or paid product |

### Layer 2 — Consent & tracking (HIGH)

- Cookie consent banner present **before** any non-essential cookie is set.
- Reject button as prominent as Accept.
- Tracking scripts (Google Analytics, Meta Pixel, etc.) blocked until consent.
- "Do Not Sell or Share" link if California users (CCPA/CPRA).
- Global Privacy Control signal honored.

### Layer 3 — Sessions & auth (HIGH)

- Cookies have `Secure`, `HttpOnly`, `SameSite=Lax` (or `Strict`).
- Auth tokens not in `localStorage` if long-lived.
- Logout invalidates session server-side.
- CSRF protection on state-changing requests.
- Session expiry explicit; idle timeout for sensitive flows.

### Layer 4 — SEO essentials (HIGH)

- Every page has unique `<title>` (≤ 60 chars).
- Every page has unique `<meta name="description">` (~150 chars).
- Every page has `<link rel="canonical">`.
- Every page has Open Graph tags (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`).
- Every page has Twitter Card tags.
- Structured data (JSON-LD) where relevant (Organization, Article, Product, BreadcrumbList, FAQ).
- `<html lang>` set.
- Exactly one `<h1>` per page; heading hierarchy correct.
- Alt text on every meaningful image.

### Layer 5 — Site-wide SEO files (HIGH)

- `robots.txt` at root with explicit rules and sitemap reference.
- `sitemap.xml` at root, all canonical URLs, lastmod dates.
- `/.well-known/security.txt` (recommended).
- 404 page returns HTTP 404.
- 500 page exists for server errors.

### Layer 6 — Performance / Core Web Vitals (HIGH)

- LCP ≤ 2.5s on 75th percentile mobile.
- INP ≤ 200ms.
- CLS ≤ 0.1.
- Total blocking JS ≤ 250 KB gzipped (or justified).

### Layer 7 — Accessibility (WCAG 2.1 AA) (HIGH)

- Keyboard reachable everywhere.
- Focus visible.
- Color contrast ≥ 4.5:1 (text), ≥ 3:1 (large text and UI).
- Form labels associated.
- Error messages with `aria-describedby`.
- `prefers-reduced-motion` respected.
- Skip-to-content link present.

### Layer 8 — Compliance frameworks (situational)

- GDPR (EU users): lawful basis documented, DSAR endpoint, 72-hour breach notification plan.
- CCPA/CPRA (California): "Do Not Sell or Share" link.
- HIPAA (health data): BAAs with vendors, encryption verified.
- PCI-DSS (cards): no raw card numbers handled; tokenization via Stripe/Adyen.

### Layer 9 — Forms & PII (HIGH)

- HTTPS-only.
- Server-side validation on every form.
- Rate limiting on signup, login, contact, password reset.
- CAPTCHA on public forms.
- No PII echoed in URLs (`?email=...`).
- Email verification before privileged actions.

### Layer 10 — Email deliverability (MEDIUM, if applicable)

- DMARC / DKIM / SPF set up.
- Unsubscribe link in every marketing email.
- Physical address in marketing email footer (CAN-SPAM).

## How the check runs

1. Detect the framework (Next.js, Astro, SvelteKit, Nuxt, plain HTML, etc.) by reading the project structure.
2. Walk the routes / pages — collect what exists and what's referenced.
3. Read the build output if available; otherwise inspect source.
4. Check each layer above; mark each finding `Critical | High | Medium | Low | Pass`.
5. Suggest a fix snippet for each failure.

## Output format

```
## Verdict: GO | CONDITIONAL (fix Critical + High) | NO-GO

## Executive summary
2–3 sentences. Most important risk first.

## Findings by layer

### Layer 1 — Legal pages
- [Critical] /privacy missing — add a route and a stub policy.
- [High]    /terms missing — needed because there's a signup form at /signup.

### Layer 4 — SEO essentials
- [High]    No <meta name="description"> on /pricing, /features, /blog/*.
- [Medium]  Open Graph tags missing site-wide.

### Layer 7 — Accessibility
- [High]    Color contrast 3.2:1 on primary CTA — needs ≥ 4.5:1.
…

## Quick wins
3–5 items the user can ship in one PR.

## Defer-with-issue
Items not blocking launch but tracked.
```

## Do / don't

**Do:**
- Always check every layer. Don't skip layers because the project "is just a landing page."
- Cite the exact file and line for each finding.
- Provide a fix snippet for every High and Critical finding.

**Don't:**
- Don't let style/preference issues block the verdict — only Critical and High block.
- Don't recommend frameworks; work with what's there.
- Don't paste full legal text — point to templates (see `/legal-pages` skill).
