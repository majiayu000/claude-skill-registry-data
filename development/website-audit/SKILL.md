---
name: website-audit
description: >
  Auto-audit any website end-to-end — technical health, SEO basics, broken links, mobile
  rendering, design quality, copy clarity, and conversion readiness — producing a scored,
  evidence-backed report. Two modes: PROSPECT mode (fast audit of a lead's site to generate
  evidence for outreach; emits a portable audit_packet JSON other tools can consume) and
  QA mode (deep pre-launch / post-launch gate on a site you built, with pass/fail checklist). Use whenever the user asks to "audit this site", "run a website
  audit", "what's broken on this site", "check this prospect's website", "QA this build",
  "is this site ready to launch", or provides a URL asking what works and what doesn't.
---

# Website Audit (Prospect + QA)

You are running a structured website audit. The audit has two layers, always in this order:

1. **Deterministic layer** — run `scripts/audit.mjs` (Playwright crawler). Objective, scriptable facts: status codes, broken links, SEO tags, console errors, HTTPS, mobile viewport, screenshots. Never hand-guess anything the script can measure.
2. **AI judgment layer** — YOU read the script's JSON output and *look at every screenshot* with the Read tool. Judge what a script can't: design era/quality, copy clarity, duplicated content, CTA strength, trust signals, mobile layout breakage.

Then score, and write the report for the selected mode.

## Step 0 — Pick the mode

Ask (or infer from context) which mode applies:

- **PROSPECT mode** — the site belongs to a lead. Goal: fast, evidence-backed ammunition for outreach. Depth: crawl up to ~10 pages, focus on the 5 most compelling problems. Output: `audit_packet` JSON + short human summary.
- **QA mode** — the site is one we built/are delivering. Goal: nothing ships broken. Depth: crawl up to ~30 pages (or full sitemap if small), run the FULL checklist, every item gets pass/fail. Output: QA gate report. A single CRITICAL fail = do not ship.

If the user gave a URL with no context, ask one question: is this a lead's site or one of yours? If you have a lead list or CRM available, checking whether the domain appears there answers it without asking.

## Step 1 — Run the deterministic layer

```bash
cd <skill-dir>/scripts
npm install playwright@latest --no-save 2>/dev/null || npm install playwright --no-save
node audit.mjs <url> --max-pages=<10|30> --out=/home/claude/audit-<domain>
```

The script emits `audit.json` plus a `screenshots/` folder (homepage desktop + mobile full-page, plus desktop shots of every crawled page). If the script fails on a hard-blocked site (Cloudflare challenge etc.), note it, fall back to WebFetch for content checks, and mark technical items "not verifiable".

Additional cheap checks to run yourself alongside the script:

- `curl -sI http://<domain>` → does HTTP redirect to HTTPS?
- Fetch `/<random-string>` → does a real 404 page exist (script covers this; verify the screenshot looks intentional, not a default server page)?
- Optional (QA mode): PageSpeed Insights API for Core Web Vitals: `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<url>&strategy=mobile` (no key needed for light use). Record LCP, CLS, performance score.

## Step 2 — AI judgment layer

Read `audit.json` fully. Then **Read every screenshot** — do not skip the mobile ones; mobile breakage is the most common finding and the script cannot see it, only you can.

Judge each of these, citing the specific screenshot/page as evidence:

- **Design era & polish**: does it look current or 2012? Cramped hero, tiny text, stock-photo soup, clashing colors, inconsistent spacing.
- **Mobile rendering**: overflowing text, overlapping elements, unusable nav, tap targets too small, horizontal scroll.
- **Copy & content**: unclear what the business does within 5 seconds; jargon; walls of text; duplicated info (same phone number 3×, bullet list restating the paragraph above it); placeholder/lorem text; outdated content (old year in footer, expired offers).
- **Conversion path**: is there ONE obvious primary CTA above the fold? Is phone number click-to-call on mobile? Is the contact form short and working? Are trust signals present (reviews, credentials, photos of real people/work)?
- **Consistency**: NAP (name/address/phone) consistent across pages — and matching whatever record you hold for the business, if you have one.

Related installed skills compose here — invoke them when depth is wanted: `ui-oddity-scan` (per-page oddity pass), `ux-audit` (flow-level friction), `fresh-eyes` (first-time-visitor confusion). In PROSPECT mode skip these unless asked; in QA mode run `ui-oddity-scan` on the top 3 pages.

## Step 3 — Score

Use `references/checklist.md` for the full item list. Severity weights:

| Severity | Weight | Meaning |
|---|---|---|
| CRITICAL | 15 | Actively losing customers / broken function (site down, broken forms, no mobile usability, SSL errors) |
| MAJOR | 8 | Meaningfully hurting results (no HTTPS redirect, broken links on key pages, missing titles/meta, dead CTA, unreadable mobile) |
| MINOR | 3 | Polish / best practice (missing alt text, thin meta descriptions, no favicon, slow-ish pages) |

Score = 100 − Σ(weights), floored at 0. Grade: A ≥ 90, B ≥ 80, C ≥ 65, D ≥ 50, F < 50.

## Step 4 — Output

### PROSPECT mode → `audit_packet`

Write `audit_packet.json` next to the audit output. The shape is deliberately portable — a downstream outreach or content-analysis step can consume it directly, or it can enrich an existing prospect record:

```json
{
  "packet_type": "audit_packet",
  "domain": "example.com",
  "audited_at": "<ISO date>",
  "mode": "prospect",
  "score": 47,
  "grade": "F",
  "pages_crawled": 9,
  "top_findings": [
    {
      "severity": "CRITICAL",
      "category": "mobile",
      "finding": "Homepage nav unusable on mobile — links overlap the logo",
      "evidence": "screenshots/home-mobile.png",
      "sales_angle": "60%+ of local searches are mobile; their front door is broken for most visitors"
    }
  ],
  "all_findings": [ "...same shape, every finding..." ],
  "works_well": [ "things that are fine — keeps the audit honest and outreach credible" ],
  "screenshots_dir": "audit-example.com/screenshots"
}
```

Then give the user a short human summary: grade, the top 3–5 findings each with its `sales_angle` line, and one sentence on what's genuinely fine (credibility). Do NOT write outreach copy — that's a downstream stage.

### QA mode → gate report

Markdown report (send as a file): checklist table with pass/fail per item from `references/checklist.md`, findings grouped CRITICAL → MAJOR → MINOR each with evidence path, and a verdict line: **SHIP** (no CRITICAL, ≤2 MAJOR) / **FIX THEN SHIP** / **DO NOT SHIP** (any CRITICAL). Include the before-fix score so re-runs show progress.

## Step 5 — Verify before reporting

Re-check your top 3 findings manually before presenting: re-fetch the page or re-read the screenshot. A false "broken" claim in outreach kills credibility; a false pass in QA ships a bug. Never report a finding you haven't personally confirmed against evidence.

## Recurring audits

If the user wants ongoing monitoring, offer to set up a scheduled task that runs this skill weekly against a list of client sites and reports only regressions (score drops or new CRITICAL/MAJOR findings).
