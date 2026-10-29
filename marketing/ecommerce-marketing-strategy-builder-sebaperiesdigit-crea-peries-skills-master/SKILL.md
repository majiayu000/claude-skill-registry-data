---
name: ecommerce-marketing-strategy-builder
description: Use when someone asks to build an e-commerce marketing strategy, plan channel priorities and budget allocation, define a target audience and competitive positioning, or create a 90-day marketing roadmap for Amazon, Shopify, WooCommerce, Etsy, TikTok Shop, or other platforms. Produces overall strategic direction — never ad-copy, detailed PPC campaign setup, technical SEO fixes, listing rewrites, social-post creation, or live account changes.
argument-hint: "[business/product details]"
allowed-tools: WebFetch, AskUserQuestion, Read, Write, Glob, Grep
---

# E-commerce Marketing Strategy Builder

Build a complete, evidence-led omnichannel marketing strategy — target audience, competitive landscape, pricing position, 2-4 prioritized channels with budget allocation, a 90-day phased action plan, and measurement KPIs. This is a strategy skill, not an execution skill: it sets direction, it doesn't build ad copy, set up campaigns, fix technical SEO, rewrite listings, or touch any live account.

**Read-only / strategy only.** Output is analysis, recommendations, drafts, and an execution checklist. Never publish or change campaigns, budgets, prices, listings, audiences, email flows, website content, or account settings.

This skill sets overall direction. For page-level SEO diagnosis, use `ecommerce-seo-auditor`. For AI-shopping/AI-search visibility, use `ecommerce-geo-auditor`. For ongoing KPI tracking once the strategy is running, use `ecommerce-sales-tracker`. None of these are required to use this skill.

## Reference files

Detailed, changeable material lives outside this file — read the relevant one when you reach that step:

- `references/marketing-benchmarks.md` — channel ROI, budget-as-%-of-revenue, and budget-allocation benchmark tables, with sources and dates. These are point-in-time figures, not permanent facts — verify current data via research where possible before citing them as current.
- `references/channel-guidance.md` — what to include in the channel-by-channel plan (email/SMS, SEO/content, paid ads, social, influencer/affiliate, referral/loyalty) for whichever channels get prioritized.
- `references/strategy-output-template.md` — the full report template with every section's exact format (persona, competitive landscape, channel plan, 90-day plan, KPI table).

## Usage examples

```text
I'm launching a Shopify store selling premium dog treats, $24.99 per bag. Margin is 65%. Budget: $3,000/month. Target: US dog owners. Help me build a marketing strategy.
I sell handmade jewelry on Etsy and my own site. Price $40-120. 2,000 Instagram followers, 800 email subscribers. $1,500/month budget. Want to grow beyond Etsy.
We're a new DTC skincare brand on Shopify. AOV $55, margin 70%. $10,000/month budget, want to hit $100K revenue in 6 months.
```

## Inputs and collection

Extract before asking anything: product/offer, price or AOV, margin/costs, business stage, marketing goal, monthly budget, sales channels, target market/language/currency, existing assets (email list, social following, content, reviews), competitors, team capacity, and any evidence already supplied (URLs, exports, screenshots).

- If public browsing is available, research current competitor, pricing, market, and channel evidence where it would materially improve the result — record exactly what was inspected and the date. Also read any supplied file, export, screenshot, or pasted content directly; where the user points to a folder or bundle, search it for the relevant files first.
- If no browsing capability is available and nothing else useful is supplied, ask for the best alternative evidence (product copy, screenshots, reports, analytics exports, competitor URLs, customer research) and produce an evidence-limited strategy from that. Never pretend unavailable browsing or files were inspected.
- Never invent competitor facts, prices, reviews, audience behavior, channel activity, performance, demand, rankings, policies, or product claims. An unavailable fact is **Not assessed**, never a guess.
- **If nothing usable is supplied at all, ask before proceeding** — one clickable question, recommended option first, free-text override open: "Describe my product/business (Recommended)" / "I have a URL or files to share" / "Not sure yet — help me figure out scope." If they choose to share a URL/file, follow with one more clickable question for how: "Paste it directly in chat (Recommended)" / "Provide a file path or location for me to read." If they choose "Not sure yet," don't bundle a list of questions into one free-text message — move straight into In-workflow questions below and ask its items one at a time, starting with Product/offer description. Skip this whole step once the user has already given usable input.
- Continue with a partial strategy whenever some usable input exists. Label every material statement in the output as **Confirmed fact**, **Research finding**, **Calculation**, **Recommendation**, **Assumption ⚠️**, or **Not assessed** — never let missing data pass as fact.

## In-workflow questions

Ask only genuinely material missing questions — never what's already evident from the message or supplied evidence. **One question per turn, always** — never bundle two or more of the items below into a single message, even to save turns. Clickable where the item has a finite set of good answers (recommended option first, free-text/"Other" override always open); numbered plain text with the same marking where a clickable tool isn't available (see Platform adapters); genuine free text only for items with no finite set of good answers (product/offer description, exact price/budget figures, named competitors).

Common decision points (not exhaustive — skip anything already evident):

- **Product/offer description** — if nothing about what they sell (or plan to sell) is known yet, ask this first, as its own single free-text question ("What are you selling, or planning to sell?") — there's no finite set of good answers here, so it's never clickable, but it's still exactly one question, not bundled with platform/price/stage.
- **Business stage** — new/pre-launch, early (<$10K/mo), growing ($10K-$50K/mo), or scaling ($50K+/mo) — changes priority order and budget benchmarks.
- **Marketing goal** — brand awareness, direct sales, or both — changes channel mix.
- **Sales channels** — Shopify/own site only, a specific marketplace, or multiple platforms — affects strategy and which platform constraints apply.
- **Budget and margin** — if not stated, needed to calculate what's affordable to spend acquiring a customer; ask directly (these are numeric, not multiple-choice).
- **Existing assets** — email list size, social following, existing content, reviews — what there already is to build on.
- **Competitors to analyze** — named competitors, or research the category's leading brands instead.
- **Depth** — if the request is an explicit strategy request, default straight to the full strategy without asking. Only if genuinely ambiguous (e.g. "where should I start?"), ask: "Quick triage — top priorities and direction only (Recommended)" / "Full strategy — complete persona, competitive landscape, channel plan, 90-day roadmap, KPIs."
- **Multiple products/markets** — if more than one is in scope, ask which is the priority product-market combination; that one gets the full strategy, the others get a short expansion note.
- **Evidence gap** — if browsing/files aren't available and nothing else useful is supplied, ask what alternative evidence they can share (see Inputs and collection).
- **Conflicting data** — if supplied figures conflict with each other or with research findings, show both values and sources; ask the user to decide only if it affects a material recommendation, otherwise present labelled scenarios instead of asking.

Before starting the Workflow below, if anything was asked, post a one-line **scope recap** (e.g. "Full strategy for the Shopify dog-treats launch, $3K/mo budget, brand-awareness + sales goal — sound right?") as a final clickable confirm/adjust question, recommended = "Yes, proceed." Skip the recap if nothing needed asking.

## Workflow

Resolve all applicable In-workflow questions (including the scope recap) before starting this list.

1. Record the business snapshot: product/offer, price/AOV, margin, stage, goal, budget, sales channels, target market/language/currency, existing assets, team capacity, and the priority product-market combination if more than one was in scope.
2. Gather evidence per Inputs and collection above; record every source and inspection date, and what's evidence-limited or **Not assessed**.
3. Build the target audience persona: use real customer data if supplied; otherwise infer from product category, price point, and platform, marking inferred fields **Assumption ⚠️**. Use `references/strategy-output-template.md` for the exact persona format.
4. Build the competitive landscape: research named or category-leading competitors for pricing, positioning, strengths/weaknesses (from reviews where available), and marketing channels; identify market gaps and a pricing recommendation. Never invent an exact selling price — only an evidence-supported position or a validation plan. Use `references/strategy-output-template.md` for the format.
5. Assess all relevant channels, then prioritize only 2-4 for the next 90 days based on stage, budget, goal, and audience. State what's deferred and the condition that would justify revisiting it. Use `references/marketing-benchmarks.md` for allocation benchmarks and `references/channel-guidance.md` for what to include per prioritized channel.
6. Build budget and profitability scenarios from confirmed economics; where economics are incomplete, give clearly labelled scenarios explaining the relevant unknowns (returns, fulfilment, shipping, discounts, tax, payment/platform fees, repeat purchase rate). Never treat gross margin or a generic benchmark/ROAS figure alone as proof of profitability.
7. Build the 90-day action plan in 0-30/31-60/61-90 day phases (adapt the horizon only for a stated material reason — launch date, seasonal event, cash runway, goal). Plan around the real team: identify available owners, weekly capacity, and skills; mark each item do-now, defer, or optional-outsource. Never assume added spend, agencies, or contractors the user hasn't confirmed.
8. Define baseline, KPIs, review cadence, and continue/fix/pause/test thresholds for each prioritized channel. Never promise a specific outcome (revenue, ROAS, rankings, traffic, sales).
9. Note optional specialist handoffs (`ecommerce-seo-auditor`, `ecommerce-geo-auditor`, `ecommerce-sales-tracker`, or a dedicated PPC-execution workflow if the user has one) and what evidence would most improve the next iteration.
10. Assemble the full report in the order defined in `references/strategy-output-template.md`, post it in chat, then save it per Output format below where that's possible.

## Domain rules

- Label every material statement **Confirmed fact**, **Research finding**, **Calculation**, **Recommendation**, **Assumption ⚠️**, or **Not assessed** — never blur a guess into a stated fact.
- Never invent competitor facts, prices, reviews, audience behavior, channel activity, performance, demand, rankings, policies, or product claims.
- Never invent an exact selling price — only an evidence-supported position, price range, or validation plan.
- Never treat gross margin, a generic benchmark, or a generic ROAS target as proof of profitability on its own.
- Prioritize only 2-4 channels for the 90-day plan; name what's deferred and why, even though all relevant channels get assessed.
- Plan around the real operating team's actual owners, weekly capacity, skills, and approved budget — never assume agencies, creators, developers, or added spend the user hasn't confirmed.
- Use minimum-necessary customer/account data, preferably aggregated or anonymized; never reproduce personal customer data, credentials, tokens, or confidential account-access details.
- Never guarantee revenue, ROAS, rankings, traffic, sales, or any other performance result.
- When inputs conflict, show every value and its source; ask the user to decide only if it's material to a recommendation, otherwise present labelled scenarios.
- This skill never makes a live change of any kind — no campaigns, budgets, prices, listings, audiences, email flows, website content, or account settings.

## Output format

Assemble the report in this fixed order (full template with exact section formats in `references/strategy-output-template.md`):

1. Business snapshot and scope
2. Evidence, assumptions, conflicts, and unassessed areas
3. Target audience and buyer journey
4. Competitive landscape and differentiation opportunities
5. Pricing position or pricing-validation plan
6. Channel assessment and the 2-4 prioritized channels
7. Budget and profitability scenarios
8. Action plan: days 0-30, 31-60, 61-90
9. Owners, weekly capacity, required assets, and deferred work
10. Baseline, KPIs, review cadence, and continue/fix/pause/test thresholds
11. Optional specialist handoffs and next evidence to collect

The complete report posted in chat is the required output on every platform. Only where persistent file writing is actually available, ask the user via a clickable `AskUserQuestion` ("Save this strategy to `output/ecommerce-marketing-strategy-builder/`?" / "Save it (Recommended)" vs "Just the chat copy") before writing anything — never save without that confirmation, and ask it fresh for every strategy rather than assuming a standing yes from an earlier one. If confirmed, save the same markdown to `output/ecommerce-marketing-strategy-builder/<business-or-scope-slug>-<YYYY-MM-DD>-report.md`, using a safe, readable slug and the report date; if a prior report exists for that slug, create a new dated file rather than overwriting it. Where file writing isn't available, or the user declines, don't claim a file was saved — say the complete copyable report is the one above.

## Platform adapters

**Claude Code adapter:** Use WebFetch to research public competitor/market/pricing evidence when it would materially improve the result — no confirmation needed for a normal public-page fetch. Read local files/exports the user points to; use Glob/Grep to locate the relevant files first when pointed at a folder or bundle. Use AskUserQuestion for every in-workflow clarifying question (see In-workflow questions above) and for the save-confirmation in Output format above. Read `references/marketing-benchmarks.md`, `references/channel-guidance.md`, and `references/strategy-output-template.md` at the workflow steps that need them. Once confirmed, save the completed report to `output/ecommerce-marketing-strategy-builder/<slug>-<date>-report.md` via Write, never overwriting a prior report for the same slug. `allowed-tools: WebFetch, AskUserQuestion, Read, Write, Glob, Grep`.

**Other platforms** (Claude web chat, Claude Cowork, ChatGPT web chat, Codex, or any other surface): use the platform's own native public-browsing capability if it has one to research competitor/market evidence. If it doesn't, say so plainly and ask the user for the best available evidence instead (product copy, screenshots, reports, analytics exports, competitor URLs, customer research) — build an evidence-limited strategy from that, and mark unresearched areas **Not assessed**. Ask in-workflow clarifying questions as plain numbered text (recommended option marked, free-text override open) since no clickable-question tool is assumed. The report posted in chat is the complete, required output; offer it as a downloadable file or ask where to save it if the platform supports authorized persistent storage — otherwise state plainly that no file was saved.

## Limitations

- This skill cannot access live analytics, ad accounts, or platform dashboards — all figures come from what's supplied or researched, never from a direct account connection.
- Strategic recommendations are not guarantees; actual results depend on execution quality, market conditions, and factors this skill cannot observe.
- Benchmark figures in `references/marketing-benchmarks.md` are point-in-time and must be verified against current sources before being cited as fact in a report.
- This skill does not diagnose page-level SEO or AI-search issues, generate ad copy, or set up campaigns — see the cross-references above for those.
