---
name: ai-brand-facts
description: Find what ChatGPT, Gemini, Perplexity, Copilot, Claude and Google AI Overviews get wrong about your business, trace each claim to its source and fix it there. Use for "ChatGPT has our pricing wrong", "AI confuses us with another company", a brand fact sheet or an AEO / LLM SEO / GEO entity check.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/ai-brand-facts
---

# Make AI engines describe your business correctly

Check what AI answer engines say when people ask about the business by name, sort every claim into correct, outdated, wrong, missing or confused with another company, follow each bad claim back to the page it came from, and fix it at that source. You hand back a dated fact sheet ready to publish, a claim log with sources and frequencies, an entity consistency check across profiles, a fix list by route, the claims that need the owner's or a lawyer's attention, and a before/after log to re-test monthly.

> **Romeo's rule:** Engines rarely invent your old prices; they read the ones you left lying around, so tidy the web before you complain to the engine.

## Use this when

- An AI answer states the wrong price, plan, feature, location, owner or policy, or says the product does something it doesn't.
- AI tools mix the business up with a company, app or person of the same or a similar name.
- After a rebrand, price change, pivot, acquisition, move or discontinued product, to make sure the old facts stop circulating.
- Sales or support keep hearing "ChatGPT told me…" from prospects or customers.
- Answers to "is [brand] legit", "[brand] complaints" or "[brand] reviews" lean on one stale thread or a namesake's reputation.

## Don't use this for

- Whether the brand is named at all for category prompts like "best X for Y", and the citation-source map across buyer prompts → `ai-search-visibility`.
- Rewriting a page section by section so engines can quote it cleanly → `ai-citable-pages`.
- Writing and validating the Organization JSON-LD this skill asks for → `schema-markup`.
- Earning more genuine reviews on the platforms engines cite → `reviews-for-ai-answers`; a full local listings audit for a physical business → `local-seo-audit`.

## What you need

### Required

- The brand name exactly as written, former names, legal name, common misspellings, and every domain the business has used, old ones included.
- Someone who can confirm the current truth: owner, product or finance lead. Without them, nothing can be called wrong.
- Engines in scope, plus the country and language of the market. Answers differ by market.
- 2 to 5 competitors buyers compare you with, and any company with the same or a similar name.

### Helpful

- A dated changelog of price, plan, product and policy changes, so an outdated claim can be matched to when it stopped being true.
- A list of old URLs: retired pricing and plan pages, PDF price lists, press kits, old help-centre articles, old domains, and the redirect map.
- Logins or owners for: Google Business Profile, Bing Places, Apple Business, LinkedIn, Crunchbase, review-site vendor portals (G2, Capterra, Trustpilot), app store consoles, social accounts, Wikidata.
- Support tickets or call notes quoting what an AI tool said.
- Bing Webmaster Tools AI Performance (grounding queries and cited pages) and Search Console Performance filtered to brand queries.
- An export from an AI visibility tracker. Optional; spot-check 5 answers by hand.

### No tools?

Run the battery by hand in each engine's free tier: ChatGPT with search on, Gemini, Google Search (AI Overview and AI Mode), Perplexity, Copilot and Claude with web search on. Use a private window, log out or turn memory and personalisation off, keep the same country, and paste each answer and its cited links into a sheet, one row per run. Find stale pages with searches like `site:yourdomain.com pricing`, `site:yourdomain.com filetype:pdf` and `"[brand]" "[old price]"` in Google and Bing. The Internet Archive's Wayback Machine dates old versions of a page. Test Organization markup with the Rich Results Test or the Schema Markup Validator. A workable minimum: 20 questions, the 3 engines your buyers use most, 2 runs each.

## Ground rules

- Nothing is wrong until it's checked against a dated, confirmed fact. Build the fact sheet first; an unconfirmed fact is a question for the owner, not a fix.
- Answers vary between runs. Report each claim as a rate ("wrong price in 4 of 6 ChatGPT runs"). A one-off oddity matters less than a repeated claim, except on safety, legal, health or money topics, where one run is enough to escalate.
- A cited claim gets fixed at the cited page. An uncited claim most likely comes from the model's training data (model memory): it changes only when models are retrained, on schedules nobody publishes. Fix the web anyway, and track those claims separately.
- Your own domain is often where outdated claims start (old pricing pages, PDFs, launch posts) and is always the easiest place to fix them. Start there before writing to anyone else.
- Consistency beats volume: one name, one one-line description and one category, worded the same everywhere the business is described.
- A fact only counts as published when it's in visible HTML on a page people can reach. Markup alone, a PDF, an image or a chat widget doesn't count. Google's AI features guidance says no special markup or AI text files are needed, and structured data must match the visible text.
- Accurate criticism isn't a wrong fact. A real complaint pattern is a product or support problem: answer it publicly (a fixed policy, a status page, a reply), never bury it.
- Engines' feedback buttons are a signal, not a fix. None of them promise a correction or a timeline.
- No manipulation: no hidden text or instructions aimed at AI, no AI-only page versions, no fake reviews, no editing Wikipedia about yourself, no sockpuppet posts to drown out a complaint. Google's spam policies list attempting to manipulate generative AI responses in Google Search as spam.

## Steps

1. **Write the dated fact sheet.** One line per fact, each with "true as of" date, who confirmed it, and the public URL where it is visible.
   - Identity: official name and how it's written (capitals, spacing), former names ("formerly X, renamed March 2025"), legal name, parent company, founding year, headquarters, leadership only where already public.
   - One-liner, 25 words or fewer: what it is, who it's for, how it differs. Use it verbatim everywhere.
   - Category: the words buyers use, one primary and at most two secondary. Who it's for, and who it isn't for (team size, industry, budget, platform, country).
   - Offer: every plan with price, currency, billing period, tax treatment, free plan or trial terms, setup fees, and limits (seats, usage caps, storage, contract length). Write "$29 per user per month, billed annually, excl. VAT", never "from $29".
   - Coverage: countries served, languages, locations with addresses and opening hours, service areas.
   - Integrations and platforms, spelled the way each partner spells its own product. Certifications and compliance claims with issuer and date (SOC 2 Type II, ISO 27001, HIPAA), only if current.
   - Policies: refunds, cancellation, data retention, shipping and returns, support hours and channels.
   - Publish: an About or company-facts page holding the identity lines, the one-liner and links to the official profiles; prices on the pricing page; each policy on its own page. Show a visible "last updated" date that changes only when a fact changes.
   - Facts that differ by country get one line per country. Discontinued products get a line too: "Acme Lite was discontinued in June 2025; Acme Core replaced it".

2. **Write the brand battery.** 20 to 30 questions in buyer wording, tagged with the fact-sheet fields each one tests.
   - Identity: "what is [brand]", "who owns [brand]", "where is [brand] based", "is [brand] the same as [namesake]".
   - Pricing: "how much does [brand] cost", "does [brand] have a free plan", "[brand] pricing for a team of 10".
   - Capability: "does [brand] do [Z]", "does [brand] integrate with [tool]". Include 2 or 3 things you deliberately don't do, to catch false yeses.
   - Trust: "is [brand] legit", "is [brand] safe", "[brand] complaints", "[brand] reviews", "[brand] refund policy".
   - Comparison and alternatives: "[brand] vs [competitor]", "is [brand] better than [competitor] for [segment]", "alternatives to [brand]", "[brand] alternatives cheaper".
   - Old facts: the former name, a discontinued product, the old price point.

3. **Run it 2 to 3 times per engine in clean sessions.** Private window, logged out or memory and personalisation off, same country, same day where possible. OpenAI says saved memories can shape how ChatGPT rewrites a prompt into searches, so a logged-in run is not a clean run.
   - Three runs for pricing, trust and comparison questions; two for the rest.
   - Record date, engine, mode and model if shown, whether it searched the web, the full answer, and every cited URL.
   - For Google, "no AI Overview shown" is its own result, not "correct" and not "missing".
   - If a tracker supplied answers, re-run 5 questions by hand; trackers often query through APIs that answer differently from the consumer apps.

4. **Classify every claim.** Split each answer into single claims ("Acme costs $49 a month", "Acme is based in Leeds") and give each one a label, plus how many runs and engines repeated it.
   - Correct: matches the fact sheet.
   - Outdated: was true once. Note the date it stopped being true from the changelog.
   - Wrong: never true, including false yeses to "does [brand] do Z".
   - Missing: a fact the question needed that the answer skipped or said it couldn't find ("pricing isn't publicly listed" when it is).
   - Confused with another company: a namesake's founder, location, product, lawsuit or reviews attached to you. Name the other entity.
   - Framing, logged separately: category and segment it puts you in, which competitors it groups you with, tone, and hedges ("reportedly", "some users say"). A correct fact in the wrong frame ("a cheap tool for freelancers" when you sell to enterprises) is a finding.
   - Priority: `Fix now` for wrong or outdated prices, plans, availability, compliance claims and identity confusion on brand questions; `Fix next` for missing key facts, wrong category or segment, wrong integrations; `Worth doing` for small details; `Leave it` for accurate criticism, opinions and one-off oddities that didn't repeat and carry no risk.

5. **Trace each claim to its source.** For every claim not labelled correct, open each cited URL and find the sentence that supports it.
   - Usual suspects: your own old pricing pages and PDF price lists, launch posts ("Introducing our $19 plan"), help articles describing retired plans, old domains still serving content, app store descriptions, SaaS directories and integration marketplaces, review sites' pricing and feature fields, Crunchbase and LinkedIn (headcount, HQ, description), Wikipedia and Wikidata, old press and funding coverage, affiliate "best X" lists, forum threads.
   - Cited page doesn't contain the claim: label it "cited but unsupported" (the engine merged sources or filled a gap). Look for the ambiguity that invites the merge, often a namesake or an unclear pricing table.
   - No citation: treat it as model memory. Search the exact wording in Google and Bing to find pages that still say it, because those are what a future model trains on and what a search-enabled run may retrieve.
   - Search for the claim even when it was cited. The cited page is rarely the only one repeating it; list the top 3 to 5.
   - If you have Bing Webmaster Tools, look through AI Performance for grounding queries that contain the brand and the pages cited for them: an old pricing or plan URL there is a source Copilot is still using.
   - Confusion: identify the other entity (name, domain, Wikidata item, Knowledge Panel) and what overlaps (name, city, category, similar domain, shared founder name).

6. **Check entity consistency.** Compare name, one-liner, category, logo, URL, address, phone and founding year across every place the business is described.
   - Own site: home, About, footer, pricing, contact, press page, help-centre header, Organization markup.
   - Listings: Google Business Profile (only for businesses that meet customers in person or serve an area; online-only businesses aren't eligible), Bing Places, Apple Business (Apple folded Apple Business Connect into it in April 2026), Yelp and local directories where relevant.
   - Profiles: LinkedIn company page, Crunchbase, G2, Capterra, Trustpilot, App Store, Google Play, Chrome Web Store or other marketplaces you list in, GitHub organisation, social bios, partner and integration directories.
   - Reference sites: Wikidata, Wikipedia if an article exists, Google's Knowledge Panel if one shows for the brand.
   - Organization markup on the home or About page: `name`, `url`, `logo`, a `description` that matches the one-liner, `sameAs` listing only official profiles the business controls (LinkedIn, Crunchbase, Wikidata, social accounts, GitHub; not review sites, per `schema-markup`), plus `legalName`, `address` and `contactPoint` where real. Former names belong in visible text ("formerly X").
   - Name collisions: pair the name with the category wherever it's introduced ("Acme payroll"), use the same logo and one-liner everywhere, and don't fight a much larger namesake for the bare name.
   - Mismatches on money facts (price, plan, availability) are `Fix now`; description, category and logo mismatches are `Fix next`.

7. **Pick the fix route for each claim.** Work from what you control outward.
   - Own pages: update in place; 301 retired pricing and plan URLs to the current equivalent; replace old PDFs with the current version or remove them (404 or 410, or `X-Robots-Tag: noindex` if the file must stay reachable); state discontinuations and renames on a short, live page instead of deleting every trace. Request recrawl with Search Console URL Inspection and IndexNow or Bing URL submission. Search Console's Removals tool only hides a URL for about six months; fix or remove the page as well.
   - Old domains: page-to-page 301s, never a blanket redirect to the homepage, and confirm they don't still serve old copies.
   - Profiles you control: edit directly (Business Profile, Bing Places, Apple Business, LinkedIn, app store listings), and claim the ones you haven't (Crunchbase, review-site vendor portals). Claim a Knowledge Panel through Google's "Get verified on Google" process before suggesting edits.
   - Third-party pages: one correction request with evidence: the exact wrong sentence, the correct fact, a link to the dated public page that shows it, and a named contact. Follow up once. Never offer payment for a correction. Once a page is corrected, Google's "Remove outdated content" tool can refresh a stale result for it.
   - Wikipedia: don't edit the article about your own business. Propose changes on its talk page with independent, reliable sources and disclose your connection, per Wikipedia's conflict-of-interest guideline. On Wikidata, fix factual statements with a reference and disclose your affiliation.
   - Framing: fix the one-liner, category and "who it's for" lines on your own pages and profiles first. If engines group you with the wrong competitors, work on the comparison pages they cite (`ai-search-visibility`, `comparison-page-writer`).
   - Engine feedback: use the thumbs-down or report option in ChatGPT, Gemini, AI Overviews, Copilot, Perplexity and Claude, with the correct fact and a link. Log the date. It promises nothing, so it never counts as the fix.

8. **Escalate what isn't an SEO problem.** Stop and give the user the quote, engine, date, run count, cited source and a screenshot, before any other work on it, when an answer:
   - Makes claims about safety, legal status, lawsuits, fraud or "scam", health effects, financial stability, data breaches, or named people.
   - Could be defamatory. The user and their lawyer decide what to do; don't contact the publisher or the engine about it yourself.
   - Credits the business with something it doesn't have (a certification, a guarantee, a regulated status). Flattering errors create liability too.

9. **Log before and after, then re-test monthly.** Keep one row per claim: claim, engines, rate before, source, fix route, date fixed, date the source changed or was recrawled, rate after.
   - Re-run the same battery with the same method monthly, and 2 to 4 weeks after a big fix for search-enabled engines.
   - Call a claim fixed only when it's gone in two consecutive monthly runs across all runs, not when one answer looks right.
   - Report memory-driven claims separately; they move slower and on no published schedule.
   - Re-check the fact sheet and its pages whenever a price, plan or policy changes: pricing page, PDFs, help centre, app stores, review-site fields, partner listings, Business Profile.

## Run it with DataForSEO (optional)

Replaces step 3 and speeds up step 5 at volume. Connect through the official MCP server (`dataforseo-mcp-server`, endpoints called via its `api_request` tool) or plain HTTPS with Basic auth. Everything else in this skill still applies.

- Existing answers that mention the brand: `POST /v3/ai_optimization/llm_mentions/search_mentions/live`.
  - `target: [{"keyword": "Acme", "search_scope": ["answer"], "match_type": "word_match"}]`; a second call with `"search_scope": ["question"]` finds prompts that ask about the brand by name.
  - `platform`: `"chat_gpt"` (US, English only: `location_code: 2840`, `language_code: "en"`) or `"google"` (AI Overviews). Set `limit` (e.g. 100) and `order_by: ["ai_search_volume,desc"]`.
  - Read `question`, `answer`, `sources[]` (url, publication_date), `ai_search_volume`, `last_response_at`, and on ChatGPT rows `brand_entities[]`, whose title and urls show when a namesake is being merged with you.
  - It's a pre-collected database: good for finding claims and their sources fast, not proof of today's answer.
- Run the battery on ChatGPT and Gemini as users see them: `/v3/ai_optimization/chat_gpt/llm_scraper/task_post` and `/v3/ai_optimization/gemini/llm_scraper/task_post`.
  - Send `keyword` (the question), location and language, and `force_web_search: true` on ChatGPT. Collect with `tasks_ready` and `task_get/advanced`.
  - Read `markdown` (the answer), `sources[]` (what it cited) and `brand_entities[]`.
- Run it on Claude and Perplexity through their APIs: `/v3/ai_optimization/claude/llm_responses/task_post` and `/v3/ai_optimization/perplexity/llm_responses/live`.
  - Send `user_prompt`, `model_name` (list them with the free `models` endpoint), `web_search: true`, `max_output_tokens` ≤ 2,048. Collect Claude tasks with `tasks_ready` and `task_get/$id`; the Standard queue can take up to 72 hours, so use `live` if the user is waiting.
  - Read `items[].sections[].text` and `annotations[]`. Annotations can be empty even with web search on, and API answers can differ from what the apps show, so hand-check 5.
- Example cost: 25 questions × 3 runs on ChatGPT and Gemini via LLM Scraper Standard ≈ $0.18. Claude and Perplexity on the same set add ≈ $0.85 to $4.60, depending on model charges (`money_spent`), which can pass the default cap. Each `search_mentions` call at `limit` 100 ≈ $0.20.
- Guardrails:
  - Estimate the cost and get the user's OK before any paid call (default cap $2 per run). Check `money.balance` with the free `GET /v3/appendix/user_data` first.
  - Always set `limit`. Use the Standard queue for batches and Live only when the user is waiting.
  - Cache results (30 days for LLM Mentions) and keep 3 runs per question; report rates, not single answers.
  - Test new code on `sandbox.dataforseo.com` first. Never print or store the API password.

## What to hand back

Fill in this template. Every claim and fix carries a priority label and an evidence label with confidence.

```markdown
# AI brand facts check: [brand], [date]

**What I found:** [one line, e.g. "ChatGPT gives the 2024 price in 5 of 6 runs; Perplexity mixes us up with Acme Labs."]
**What matters most:** [one line, e.g. "An old pricing PDF on our own domain is the cited source for the wrong price."]
**What to do first:** [one line]

## Method
- Battery: [N] questions ([groups]); engines: [list, mode/model]; runs: [n] each; dates: [dates]; country/language: [x]; sessions: [logged out / memory off]
- Fact sheet confirmed by: [name, role], [date]

## Fact sheet
- [field]: [fact] - true as of [date] - visible at [URL | "not published yet"]

## Claim log
- "[quoted claim]" - [engines], [k of n runs] - [correct | outdated | wrong | missing | confused with: entity] - source: [URL | "uncited: model memory" | "cited but unsupported"] - fix route: [own page | profile | correction request | feedback only] - [Fix now] ([seen], high)

## Framing
- Category: [as described]; segment: [x]; grouped with: [competitors]; tone: [x]; versus the fact sheet: [match / gap]

## Entity consistency
- [platform]: name [ok | "differs"]; one-liner [ok | differs]; category [ok | differs]; action: [x] [label]

## Fixes, in order
1. [Fix now | Fix next | Worth doing] [change, where] - fixes: [claims] - evidence: [seen | tool | inferred], [high | medium | low] - how we'll know: [re-test signal]

## Escalated to you
- "[claim]" - [engine, date, runs] - why it needs you: [safety | legal | health | money | possible defamation]

## Leave it
- [claim or gap, and why it isn't worth the time]

## Before/after log
| Claim | Before (date, rate) | Fixed (date, route) | After (date, rate) |
|---|---|---|---|

Next re-test: [date], same battery, engines, runs and session settings.

## What I could not check
- [engine, profile, old URL or fact not verified, and what would verify it]
```

## Stop and flag if

- An answer makes safety, legal, health, financial or personal claims, or looks defamatory: report it to the user at once, not as item 12 on a list.
- Nobody can confirm the current facts. Stop: comparing answers against guesses produces confident nonsense.
- The user wants accurate criticism removed, or asks for hidden text, AI-only pages, fake or gated reviews, sockpuppets, or self-edits to Wikipedia. Decline that part and say why.
- A fix means editing live pages, redirects, profiles or listings, or sending correction emails: draft it, then get explicit permission for each one.
- You have one run per question or fewer than 15 questions: label the results anecdotal.
- Unacceptable output: claims paraphrased instead of quoted, sources not actually opened, a claim marked fixed after one good answer, or a promised date for model memory to change.

## Next step

- Run `ai-citable-pages` on the pricing, About and top product pages, with the fact sheet and the claims traced to them.
- Run `schema-markup` with the fact sheet and the list of official profiles to write the Organization JSON-LD and `sameAs`.
- Run `ai-search-visibility` once facts are clean, to measure whether the brand is named for the category prompts that bring buyers.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
