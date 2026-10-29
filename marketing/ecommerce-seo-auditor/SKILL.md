---
name: ecommerce-seo-auditor
description: Use when someone asks to audit an ecommerce store for SEO, run a store SEO checkup, review a product page, run a technical SEO diagnosis, do a ranking-readiness review, check crawlability or indexability, or get prioritized SEO fixes for a Shopify/WooCommerce store, custom site, or a marketplace listing (Amazon, Etsy, TikTok Shop).
argument-hint: "[URL or scope]"
allowed-tools: WebFetch, AskUserQuestion, Read, Write, Glob, Grep
---

# Ecommerce SEO Auditor

Produce an evidence-led ecommerce SEO audit with prioritized, platform-feasible fixes and named validation steps. Covers both self-hosted stores (Shopify, WooCommerce, custom) and marketplace listings (Amazon, Etsy, TikTok Shop) — the editable surface differs by platform, so platform identification always comes first.

**Read-only.** This skill inspects and reports. It must never modify a live website, listing, feed, account setting, or campaign.

For AI-search, answerability, and AI-citation readiness, use the separate `ecommerce-geo-auditor` skill instead. For sales trend/anomaly confirmation once an SEO issue is found, use `ecommerce-sales-tracker`. For overall channel/budget strategy this audit's findings should feed into, use `ecommerce-marketing-strategy-builder` — optional, not a dependency.

## Usage examples

```text
Audit this product page for SEO and do not guess about unavailable data: [URL]
Audit this Shopify collection page using the crawl and Search Console exports.
Review this Amazon listing and recommend only fields a marketplace seller can edit.
```

## Inputs and collection

Collect the platform, page type, market, language, device, priority query, and business goal — but only ask what isn't already obvious from the URL or supplied evidence (see In-workflow questions below).

- If `$ARGUMENTS` (or the conversation) gives a public URL, inspect it using whatever public web-browsing capability is available in the current environment — record exactly what was inspected and how.
- Also inspect any supplied rendered page, HTML, crawl, robots.txt, sitemap, Search Console export, analytics, PageSpeed/CrUX data, structured-data result, feed, or copy the user provides directly (as a file, paste, or upload). Where the user points to a local folder or export bundle rather than a single file, search it to find the relevant files before reading them.
- For login-gated pages or account-only data (e.g. Search Console, ads accounts), never attempt to fetch — ask the user for an authorized export or screenshot instead.
- If no public-browsing capability is available at all in the current environment, say so plainly and ask the user to paste the best available evidence (rendered HTML, screenshot, crawl export, Search Console data, PageSpeed/CrUX results, structured-data output, or feed data). Audit only what was supplied.
- If a fetch fails, is blocked, or isn't possible, that is never treated as evidence of an SEO problem — label the affected area "Not assessed" and say why.
- **If `$ARGUMENTS` is empty and the conversation has no usable URL, scope, or supplied evidence at all, always ask the user directly before proceeding** — as open free text ("What would you like audited — a URL, or content you'll paste/attach?"), never a clickable question (there's no finite set of options here). Never guess, assume a placeholder target, or invent findings to fill the gap.
- Continue with a partial audit whenever some usable evidence exists. Classify every material conclusion as **Confirmed**, **Data-dependent**, or **Not assessed**. Missing evidence never proves a negative finding.

## In-workflow questions

This skill defaults to asking about **any** decision point that has a real, finite set of good answers — not just a short fixed list. Don't narrow this down to only the most obvious 1-2 triggers; scan the request for every genuine open decision. The only hard limit is: **skip anything already evident** from the URL, supplied evidence, or the conversation — never ask what you can already tell, and never pad the interview with questions that have an obvious or inconsequential answer.

Common decision points (not exhaustive):

- **Platform** — if it's not obvious whether this is a self-hosted store (Shopify/WooCommerce/custom) or a marketplace listing (Amazon/Etsy/TikTok Shop) — the editable surface (Domain rules below) depends entirely on this.
- **Scope/page type** — if the request could reasonably mean a single page, a template/collection, or a whole site.
- **Audit depth** — if it's unclear whether the user wants a quick top-issues check or the full evidence-led audit (all workflow steps, full findings table, 30-day plan).
- **Market/language** — if it plausibly affects findings (e.g. multi-region store, non-English content) and isn't stated.
- **Business goal / priority query** — if prioritizing findings genuinely depends on it and none was given.
- **Multiple plausible targets** — if the request could mean the page itself, a sample of pages within it (e.g. "audit this collection" — the collection page, its products, or both), ask which.
- **Partial-evidence tradeoff** — if only partial evidence is available and more could plausibly be supplied, ask whether to proceed now with a partial audit (labeling gaps "Not assessed") or wait for the user to provide more.

Ask one question at a time, using a clickable-question tool where available: state the question, offer the recommended option first labeled "(Recommended)" plus 2-3 genuinely distinct alternatives, and always keep a free-text override open. Where no clickable-question tool is available, ask the identical question as plain numbered text with the same "(Recommended)" marking and free-text override. See Platform adapters below for which mechanism applies where.

Before starting the Workflow below, if any of these were asked and answered, post a one-line **scope recap** (e.g. "Auditing this Amazon listing, full depth, prioritizing the 'wireless charger' query — sound right?") as a final clickable confirm/adjust question — recommended option "Yes, proceed" — rather than launching straight into the audit unconfirmed. Skip this recap entirely if nothing needed asking (everything was already evident).

## Workflow

Resolve all applicable In-workflow questions (including the scope recap) before starting this list.

1. Record the exact scope, page type, platform, sources, and inspection date.
2. Identify the platform (self-hosted store vs. marketplace) and its actual editable surface before recommending anything — ask if not evident (see In-workflow questions).
3. Check verified blockers affecting access, status, and rendering on any platform. For self-hosted stores, also check crawlability, indexability, redirects, and canonicalization. For marketplace listings, the seller does not control these — mark them "Not assessed: outside seller control on this platform" rather than checking them.
4. Review title, heading, URL, copy, images, and buyer-intent alignment.
5. Check unique product facts, trust, policies, internal links, and information architecture.
6. Compare visible product data with structured data or feeds when available.
7. Assess images and real-user page experience only from appropriate evidence.
8. Match every recommendation to the user's editable surface on that specific platform.
9. Prioritize verified findings and provide a validation plan for unknowns.
10. Post the full audit in chat, then save it per Output below where that's possible.

## Domain rules

- Treat title and description lengths as display heuristics, not hard ranking rules.
- Do not recommend keyword repetition that reduces clarity or accuracy.
- Never invent specifications, reviews, ratings, certifications, guarantees, or test results.
- Never claim live findings for evidence that was not inspected.
- Valid Product or Offer markup creates eligibility, not guaranteed rich results.
- One URL cannot prove sitewide duplication, orphan status, or template behavior.
- Use field data for definitive Core Web Vitals conclusions; label lab data diagnostic.
- **Self-hosted stores** (Shopify, WooCommerce, custom): may get canonical, robots, redirect, structured-data (JSON-LD), and template-level recommendations.
- **Marketplace listings** (Amazon, Etsy, TikTok Shop): recommend only editable titles, attributes, bullet copy, images, and native listing fields — never canonicals, robots rules, custom JSON-LD, or anything outside the seller's actual control on that platform.
- Do not forecast rankings, traffic, or revenue without a transparent model and supplied data.

Use these priorities:

| Severity | Meaning |
|---|---|
| Critical | Verified issue seriously blocks access, crawling, indexing, or rendering of an important page |
| High | Verified issue materially weakens relevance, consistency, discoverability, or a broad template |
| Medium | Meaningful narrower-scope improvement |
| Low | Cleanup, polish, or test opportunity |

## Output format

Post this in chat:

```markdown
# Ecommerce SEO Audit — [page or scope]

## Scope and evidence
- Platform/page type: [context]
- Inspected: [sources, including whether fetched live or supplied by the user]
- Not assessed: [areas]

## Executive summary
- [most important verified conclusion]
- [highest-value next action]

## Prioritized findings
| # | Finding | Evidence | Scope | Severity | Confidence | Fix (editable on this platform) | Validate with |
|---|---|---|---|---|---|---|---|
| 1 | [finding] | [observation] | Page/template/site | [level] | [level] | [action] | [test] |

## 30-day action plan
1. Now: [blocker or highest-value action]
2. Next: [template or content improvement]
3. Then: [measurement or experiment]
```

The complete audit posted in chat is the required output on every platform. Only where persistent file writing is actually available, ask the user via a clickable `AskUserQuestion` ("Save this audit to `output/ecommerce-seo-auditor/`?" / "Save it (Recommended)" vs "Just the chat copy") before writing anything — never save without that confirmation, and ask it fresh for every audit rather than assuming a standing yes from an earlier one. If confirmed, save the same markdown to `output/ecommerce-seo-auditor/<page-or-scope-slug>-<YYYY-MM-DD>-audit.md`, using a safe, readable slug derived from the URL or scope and the inspection date; if a prior audit file exists for that slug, create a new dated file rather than overwriting it, so sequential audits of the same page stay comparable. Where file writing isn't available, or the user declines, don't claim a file was saved — say the complete copyable report is the one above.

## Platform adapters

**Claude Code adapter:** Fetch a supplied URL directly via WebFetch, no confirmation needed for a normal public-page fetch. Read local files/exports the user points to; use Glob/Grep to locate the relevant files first when pointed at a folder or export bundle rather than a single file. Use AskUserQuestion for every in-workflow clarifying question (see In-workflow questions above) and for the save-confirmation in Output format above. Once confirmed, save the completed audit to `output/ecommerce-seo-auditor/<slug>-<date>-audit.md` via Write, never overwriting a prior audit for the same slug. `allowed-tools: WebFetch, AskUserQuestion, Read, Write, Glob, Grep`.

**Other platforms** (Claude web chat, Claude Cowork, ChatGPT web chat, Codex, or any other surface): use the platform's own native public-browsing capability if it has one to inspect a supplied URL. If it doesn't, say so plainly and ask the user to paste the best available evidence instead (rendered HTML, screenshot, crawl export, Search Console data, PageSpeed/CrUX results, structured-data output, or feed data) — audit only that, and mark unsupported checks "Not assessed." Ask in-workflow clarifying questions as plain numbered text (recommended option marked, free-text override open) since no clickable-question tool is assumed. The audit posted in chat is the complete, required output; no file is saved unless the platform itself offers persistent storage the user has authorized.

## Limitations

- Content-only review cannot confirm crawlability, index status, rendered output, or real-user performance.
- Search Console, analytics, crawl, backlink, feed, and Merchant Center findings require the corresponding data.
- Platform and search-feature requirements change; verify current official documentation where needed.
- SEO changes do not guarantee rankings, rich results, traffic, conversions, or revenue.
