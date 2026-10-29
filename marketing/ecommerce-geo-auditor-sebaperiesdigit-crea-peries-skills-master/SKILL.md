---
name: ecommerce-geo-auditor
description: Use when someone asks for a GEO audit, AI visibility readiness check, AI search audit, citation-readiness review, AI-shopping readiness check, or why a product is hard for AI systems (ChatGPT, Claude, Gemini, Perplexity, etc.) to understand or recommend. Diagnoses readiness only — never claims actual AI mentions, citations, rankings, or positions were observed.
argument-hint: "[URL or scope]"
allowed-tools: WebFetch, AskUserQuestion, Read, Write, Glob, Grep
---

# E-commerce GEO Auditor

Produce an evidence-led GEO (AI-search / AI-citation / AI-shopping) readiness audit that separates page preparation from actual measured AI mentions, positions, and citations. Covers both self-hosted stores (Shopify, WooCommerce, custom) and marketplace listings (Amazon, Etsy, TikTok Shop) — the editable surface differs by platform, so platform identification always comes first.

**Read-only.** This skill inspects and reports. It must never modify a live website, listing, feed, account setting, or campaign.

For classic/traditional search-engine SEO (meta tags, Core Web Vitals, backlinks, crawlability for Googlebot) rather than AI-search readiness, use the `ecommerce-seo-auditor` skill instead. For sales trend/anomaly confirmation once a GEO issue is found, use `ecommerce-sales-tracker`. For overall channel/budget strategy this audit's findings should feed into, use `ecommerce-marketing-strategy-builder` — optional, not a dependency.

## Usage examples

```text
Audit this product page for GEO and do not guess about uninspected areas: [URL]
Audit this Shopify product page for AI-search and citation readiness using the crawl.
Review this Amazon listing under marketplace constraints and explain how to measure actual AI mentions.
```

## Inputs and collection

Collect the page or content, platform, page type, market, language, target audience, priority buyer question, and business goal — but only ask what isn't already obvious from the URL or supplied evidence (see In-workflow questions below).

- If `$ARGUMENTS` (or the conversation) gives a public URL, inspect it using whatever public web-browsing capability is available in the current environment — record exactly what was inspected and how.
- Also inspect any supplied rendered page, HTML, crawl, robots.txt, structured-data export, product feed, or copy the user provides directly (as a file, paste, or upload). Where the user points to a local folder or export bundle rather than a single file, search it to find the relevant files before reading them.
- If the user supplies sampled AI-answer results (e.g. "here's what ChatGPT said about this product"), record them as contextual evidence only under Scope and evidence — never let them drive or score the readiness verdict. Readiness and observed AI visibility answer different questions (see Domain rules).
- For login-gated pages or account-only data, never attempt to fetch — ask the user for an authorized export or screenshot instead.
- If no public-browsing capability is available at all in the current environment, say so plainly and ask the user to paste the best available evidence (rendered HTML, screenshot, crawl export, structured-data output, or feed data). Audit only what was supplied.
- If a fetch fails, is blocked, or isn't possible, that is never treated as evidence of a readiness problem — label the affected area "Not assessed" and say why.
- **If `$ARGUMENTS` is empty and the conversation has no usable URL, scope, or supplied evidence at all, always ask the user directly before proceeding** — as open free text ("What would you like audited — a URL, or content you'll paste/attach?"), never a clickable question (there's no finite set of options here). Never guess, assume a placeholder target, or invent findings to fill the gap.
- Continue with a partial audit whenever some usable evidence exists. Classify every material conclusion as **Confirmed**, **Data-dependent**, or **Not assessed**. Missing evidence never proves a negative finding.

## In-workflow questions

This skill defaults to asking about **any** decision point that has a real, finite set of good answers — not just a short fixed list. Scan the request for every genuine open decision. The only hard limit is: **skip anything already evident** from the URL, supplied evidence, or the conversation.

Common decision points (not exhaustive):

- **Platform** — if it's not obvious whether this is a self-hosted store (Shopify/WooCommerce/custom) or a marketplace listing (Amazon/Etsy/TikTok Shop) — the editable surface (Domain rules below) depends entirely on this.
- **Scope/page type** — if the request could reasonably mean a single page, a template/collection, or a whole site.
- **Audit depth** — if it's unclear whether the user wants a quick top-issues check or the full readiness audit (all pillars, full tables, roadmap).
- **Market/language** — if it plausibly affects findings (e.g. multi-region store, non-English content) and isn't stated.
- **Target audience / priority buyer question** — if prioritizing answerability findings genuinely depends on it and none was given.
- **Multiple plausible targets** — if the request could mean the page itself, a sample of pages within it (e.g. "audit this collection" — the collection page, its products, or both), ask which.
- **Partial-evidence tradeoff** — if only partial evidence is available and more could plausibly be supplied, ask whether to proceed now with a partial audit (labeling gaps "Not assessed") or wait for more.

Ask one question at a time, using a clickable-question tool where available: state the question, offer the recommended option first labeled "(Recommended)" plus 2-3 genuinely distinct alternatives, and always keep a free-text override open. Where no clickable-question tool is available, ask the identical question as plain numbered text with the same "(Recommended)" marking and free-text override. See Platform adapters below for which mechanism applies where.

Before starting the Workflow below, if any of these were asked and answered, post a one-line **scope recap** (e.g. "Auditing this Amazon listing, full depth, prioritizing 'is this compatible with X' as the likely buyer question — sound right?") as a final clickable confirm/adjust question — recommended option "Yes, proceed" — rather than launching straight into the audit unconfirmed. Skip this recap entirely if nothing needed asking.

## Workflow

Resolve all applicable In-workflow questions (including the scope recap) before starting this list.

1. Record the exact scope, page type, platform, sources, and inspection date.
2. Identify the platform (self-hosted store vs. marketplace) and its actual editable surface before recommending anything — ask if not evident.
3. Check verified blockers: access/rendering, product-identity ambiguity, contradictory facts between sections, inaccessible content, or invalid structured data.
4. Review each readiness pillar in GEO readiness pillars below, using the Audit checklist to scope what's assessable given the evidence on hand.
5. Compare visible product content against structured data or feeds for internal consistency where available.
6. If the user supplied sampled AI-answer results, note them as contextual evidence only — do not let them affect any pillar's status or the severity of any finding.
7. Match every recommendation to the user's editable surface on that specific platform.
8. Prioritize verified findings by severity and confidence, and give a validation plan that clearly separates page-readiness checks from actual AI-visibility measurement.
9. Post the full audit in chat, then save it per Output format below where that's possible.

## GEO readiness pillars

- **Access & AI-crawlability** — whether crawlers/answer engines and rendering can actually reach the content: response status, robots directives, JS-rendering dependency, login/paywall gates. Robots/crawl-directive specifics apply to self-hosted stores only; a marketplace listing's crawl surface is controlled by the platform (Platform-limited).
- **Product identity clarity** — whether the product's name, category, core attributes, and use case are stated unambiguously in plain text (not only in images or a linked PDF).
- **Content answerability & structure** — whether the page directly answers likely buyer questions (what is it, who is it for, how does it compare, what does it cost, what's included) in extractable text — headings, Q&A blocks, tables — rather than only in dense marketing paragraphs.
- **Structured data completeness** — presence and internal consistency of relevant Product, Offer, AggregateRating, FAQPage, BreadcrumbList, and Organization markup, checked against the same facts stated on the visible page. Only inspect/describe markup actually present; never invent values or advise adding markup that wouldn't validate.
- **Trust signals** — reviews, ratings, return/warranty/shipping policy visibility, seller/brand identity, certifications — only as actually present on the page; never invented.
- **Media & alt-text readability** — whether images/video carry descriptive alt text and captions an AI system could extract meaning from (this is a readability check, not an image-quality/design review).
- **External evidence & citations elsewhere** — whether independent evidence exists elsewhere (reviews, press, comparison content, brand documentation) that a citing AI answer might draw on. Only assessed from evidence the user supplies or the environment can actually search; never fabricated or assumed.

## Audit checklist by page type / evidence scope

- **Single product page** — all pillars above apply directly.
- **Collection/category page** — identity and answerability checks apply at the template level; individual product facts are assessed only on a sample the user confirms (see Multiple plausible targets).
- **Marketplace listing** — restrict findings to seller-editable fields per Domain rules; the platform's own crawl handling and schema are Platform-limited, not assessed.

Evidence-scope labels: **Live inspected** (fetched/rendered directly), **Content-only** (working from supplied HTML/text/screenshots), **Platform-limited** (marketplace fields only — the platform controls the rest).

## Domain rules

- Readiness signals do not prove that an AI platform mentions, ranks, cites, or recommends a product.
- Do not claim proprietary ranking factors, guaranteed citation patterns, or mandatory keyword/FAQ counts.
- Never invent product facts, AI responses, query results, citations, scores, or competitor metrics.
- If the user supplies sampled AI-answer results, record them as contextual evidence only — never let them drive or score the readiness verdict.
- Treat model, query, market, language, personalization, and run date as part of any supplied visibility evidence — one sample is never representative.
- **Self-hosted stores** (Shopify, WooCommerce, custom): may get crawlability, robots, structured-data (JSON-LD), and content-structure/template recommendations.
- **Marketplace listings** (Amazon, Etsy, TikTok Shop): recommend only editable titles, bullets, attributes, images, and native Q&A/listing fields — never schema markup, robots rules, or anything outside the seller's actual control on that platform.
- Do not forecast rankings, citation counts, traffic, or sales.

Use these priorities for blockers and prioritized findings:

| Severity | Meaning |
|---|---|
| Critical | Verified issue seriously blocks access, crawling, indexing, or rendering of an important page |
| High | Verified issue materially weakens relevance, consistency, discoverability, or a broad template |
| Medium | Meaningful narrower-scope improvement |
| Low | Cleanup, polish, or test opportunity |

Use this scale for the per-pillar readiness table:

| Status | Meaning |
|---|---|
| Strong | Pillar is well covered with confirmed evidence |
| Partial | Some coverage confirmed, meaningful gaps remain |
| Weak | Confirmed but largely missing or inconsistent |
| Unknown | Not assessed — insufficient evidence to judge |

## Output format

Post this in chat:

```markdown
# Ecommerce GEO Readiness Audit — [page or scope]

## Scope and evidence
- Scope: Live inspected / Content-only / Platform-limited
- Platform/page type: [context]
- Inspected: [sources, including whether fetched live or supplied by the user]
- Sampled AI-answer context (if supplied): [noted as context only — not scored into the verdict]
- Not assessed: [areas]

## Executive summary
- [most important verified conclusion]
- [highest-value next action]

## Critical blockers
| Finding | Evidence | Severity | Confidence | Fix (editable on this platform) |
|---|---|---|---|---|
| [finding] | [observation] | [level] | [level] | [action] |

## Readiness by area
| Pillar | Status | Evidence | Top action |
|---|---|---|---|
| [pillar] | Strong/Partial/Weak/Unknown | [evidence] | [action] |

## Prioritized roadmap
1. Now: [blocker or highest-value action] — Validate with: [test]
2. Next: [template or content improvement] — Validate with: [test]
3. Then: [measurement step] — Validate with: [test]

## Measuring actual AI visibility
This audit measures page readiness, not observed AI behavior. To learn whether AI platforms actually mention, cite, or recommend this product, sample real buyer queries directly against the AI platforms relevant to your market, repeated over time — results vary by model, query, market, language, and date.
```

For a **quick top-issues check**, condense to Scope and evidence, Executive summary, and a short top-issues list with fixes — skip the full Readiness by area table and Prioritized roadmap. For a **full audit**, include every section above.

The complete audit posted in chat is the required output on every platform. Only where persistent file writing is actually available, ask the user via a clickable `AskUserQuestion` ("Save this audit to `output/ecommerce-geo-auditor/`?" / "Save it (Recommended)" vs "Just the chat copy") before writing anything — never save without that confirmation, and ask it fresh for every audit rather than assuming a standing yes from an earlier one. If confirmed, save the same markdown to `output/ecommerce-geo-auditor/<page-or-scope-slug>-<YYYY-MM-DD>-audit.md`, using a safe, readable slug derived from the URL or scope and the inspection date; if a prior audit file exists for that slug, create a new dated file rather than overwriting it. Where file writing isn't available, or the user declines, don't claim a file was saved — say the complete copyable report is the one above.

## Platform adapters

**Claude Code adapter:** Fetch a supplied URL directly via WebFetch, no confirmation needed for a normal public-page fetch. Read local files/exports the user points to; use Glob/Grep to locate the relevant files first when pointed at a folder or export bundle rather than a single file. Use AskUserQuestion for every in-workflow clarifying question (see In-workflow questions above) and for the save-confirmation in Output format above. Once confirmed, save the completed audit to `output/ecommerce-geo-auditor/<slug>-<date>-audit.md` via Write, never overwriting a prior audit for the same slug. `allowed-tools: WebFetch, AskUserQuestion, Read, Write, Glob, Grep`.

**Other platforms** (Claude web chat, Claude Cowork, ChatGPT web chat, Codex, or any other surface): use the platform's own native public-browsing capability if it has one to inspect a supplied URL. If it doesn't, say so plainly and ask the user to paste the best available evidence instead (rendered HTML, screenshot, crawl export, structured-data output, or feed data) — audit only that, and mark unsupported checks "Not assessed." Ask in-workflow clarifying questions as plain numbered text (recommended option marked, free-text override open) since no clickable-question tool is assumed. The audit posted in chat is the complete, required output; no file is saved unless the platform itself offers persistent storage the user has authorized.

## Limitations

- Content-only review cannot confirm crawlability, rendered output, index status, or actual AI answers.
- One inspected URL cannot prove a sitewide pattern.
- AI answers vary by model, query, market, language, personalization, and time — a readiness audit does not measure them.
- A readiness audit does not guarantee citations, recommendations, traffic, or sales.
