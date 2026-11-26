---
name: ai-agent-readiness
description: Make a site readable and usable by AI crawlers and browsing agents. Use for "should we block GPTBot", "set up robots.txt for AI bots", "do we need llms.txt", "is Cloudflare blocking ChatGPT" or "can AI agents use our pricing and signup". Covers per-bot robots rules, firewall blocks, llms.txt, Markdown pages and the accessibility tree.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/ai-agent-readiness
---

# Make the site work for AI crawlers and agents

Check whether AI crawlers can fetch the site, whether robots.txt says what the business actually intends for training, search and user-requested bots, and whether an AI agent driving a browser can read the content, understand the pricing and complete the core actions. You hand back a per-bot access table (what robots.txt says versus what each bot really gets), a draft robots.txt, the firewall and rendering blockers, an llms.txt decision, and a short list of agent-usability fixes.

> **Romeo's rule:** Decide separately whether a bot may train on you, index you or fetch for a user; blocking all three to stop one is the most common own goal in this area.

## Use this when

- Someone asks "should we block GPTBot?" or "what should robots.txt say about AI bots?"
- The site is missing from ChatGPT, Perplexity or Claude answers and you suspect the bots can't get in.
- The site moved to a CDN or host with bot protection (Cloudflare, Akamai, Fastly, Vercel, Netlify), or someone switched on "block AI bots".
- Someone asked for llms.txt, Markdown docs or an "AI-ready" site.
- Browser agents misread pricing, get stuck in signup or checkout, or can't find the contact form.

## Don't use this for

- Measuring whether AI answers mention or cite the brand → `ai-search-visibility`.
- General crawling, indexing, rendering and speed problems for Googlebot → `technical-seo-audit`.
- Writing or validating JSON-LD in depth → `schema-markup`.
- Fixing the content of a page that agents can read but that says little → `on-page-seo-review`.

## What you need

### Required

- The domain and every subdomain that serves public content (www, docs, blog, help, app).
- The live robots.txt for each host, fetched over HTTPS, not the copy in the repo. CDNs can add rules in front of yours.
- The business stance on AI training: allow, block, or undecided. This is a commercial or legal call, not an SEO one.
- 5 to 10 key URLs: home, pricing, main product or service pages, docs, signup or contact, checkout if there is one.

### Helpful

- 30 days of server or CDN logs with user agent, IP, URL and status code.
- Screenshots or exports of CDN and firewall bot settings (bot fight modes, AI crawler toggles, rate limits, country blocks).
- Search Console and Bing Webmaster Tools access (URL Inspection shows what Googlebot and bingbot received).
- A crawler or headless-browser setup (Screaming Frog, Sitebulb, Playwright) to fetch pages with chosen user agents.

### No tools?

Open `https://example.com/robots.txt` for each host in a browser. Use view-source on each key URL and search for the price, the H1 and the main paragraph: if they're not in the source, crawlers that don't run JavaScript won't see them. Turn JavaScript off in the browser and reload. In Chrome DevTools, open Elements → Accessibility and switch on the full-page accessibility tree to see what an agent reads. Run Lighthouse's accessibility audit. Use Search Console URL Inspection (View crawled page) and the Rich Results Test to see Googlebot's rendered HTML. If `curl` is available, it shows exactly what a bot receives.

## Ground rules

- There are three kinds of AI bot, each needing its own decision. Training crawlers collect data for model training. Search crawlers build the indexes AI answers are drawn from. User-triggered fetchers load one page because a person asked an assistant to.
- robots.txt is a request, not a lock. Most major vendors' crawlers honour it, but user-triggered fetchers often don't: OpenAI says robots.txt "may not apply" to ChatGPT-User, and Perplexity and Google say their user-triggered fetchers generally ignore it, while Anthropic says its bots honour it. Real enforcement needs firewall rules on verified IP ranges.
- Never block Googlebot or bingbot to keep content out of AI answers. That removes you from search. For Google, use snippet controls or Search Console's site-wide Search generative AI setting (covers AI Overviews, AI Mode and Discover's generative features); for Bing, its grounding preference when it takes effect.
- Verify before trusting a user agent. Anyone can send "GPTBot" in a header; vendors publish IP range files, and Google supports reverse DNS checks.
- A crawler follows only the most specific `User-agent` group that matches it. Once you add a `GPTBot` group, GPTBot ignores everything under `User-agent: *`, so repeat any rules it should still obey.
- llms.txt is a proposal, not a standard. No major search engine has said it uses llms.txt for ranking, and since June 2026 Google's documentation says Google Search doesn't use llms.txt files at all. It's cheap and useful for docs-heavy products, and close to pointless for a ten-page brochure site.
- Bots and people must get the same content. Markdown copies and llms.txt summaries must say what the HTML says; serving bots different claims is cloaking.
- Agents read pages much as screen readers do: names, roles, labels, states. Fixing accessibility is most of agent readiness.
- Emerging standards (WebMCP, AI usage preferences in robots.txt) are worth noting and piloting where there's a clear use; don't rebuild anything around a draft.

## Steps

1. **See which bots actually arrive.** Group 30 days of logs by user agent and status code.
   - Check that these appear and get 200s: Googlebot, bingbot, OAI-SearchBot, PerplexityBot, Claude-SearchBot, plus the user-triggered fetchers ChatGPT-User, Claude-User, Perplexity-User and Google-Agent.
   - 403, 429, 503 or an HTML challenge page served to a search or retrieval bot you want is `Fix now`. A training bot getting 403 is fine if blocking it was the decision.
   - Verify suspicious hits against the vendor's published IP list before drawing conclusions. Fake "GPTBot" traffic is common.
   - No logs? CDN analytics often break out AI crawlers (Cloudflare's AI Crawl Control is one example).
2. **Read the live robots.txt for every host.** Rules apply per host and protocol, so docs.example.com needs its own file.
   - It returns 200 with `text/plain`. For Google, a 404 means "no rules" while a 5xx or 429 can pause crawling of the whole site; other bots vary.
   - Look for a broad `User-agent: *` / `Disallow: /`, leftover staging rules, and CDN-managed blocks or `Content-Signal` lines you didn't write.
   - Check each named AI group: does it accidentally drop rules from `*` (see ground rules), or block `/` when only a path was meant?
3. **Write the policy, bot by bot.** Confirm every token on the vendor's current crawler page; names and behaviour change.
   - Training: `GPTBot` (OpenAI), `ClaudeBot` (Anthropic), `CCBot` (Common Crawl, used in many training sets), `Google-Extended` (a control token, not a separate crawler; it also covers grounding in Gemini Apps and Vertex AI, but not Google Search or AI Overviews), `Applebot-Extended` (a control token that doesn't crawl; blocking it doesn't remove you from Siri, Spotlight or Safari results).
   - Search and retrieval: `OAI-SearchBot` (ChatGPT search), `Claude-SearchBot`, `PerplexityBot`, plus `Googlebot` (Google Search, AI Overviews, AI Mode) and `bingbot` (Bing and Copilot).
   - User-triggered: `ChatGPT-User`, `Claude-User`, `Perplexity-User`, `Google-Agent` (agents on Google infrastructure that browse and act for a user).
   - Default for a business that wants AI visibility: allow search crawlers and user-triggered fetchers; decide training separately. Blocking GPTBot or ClaudeBot doesn't, per their vendors' docs, remove you from ChatGPT or Claude search, because those use different bots. Blocking Google-Extended does take you out of Gemini app grounding.
   - Draft it like this (example for "visible in AI search, no training"), keeping any existing rules each group still needs:
     ```
     User-agent: GPTBot
     User-agent: ClaudeBot
     User-agent: CCBot
     User-agent: Google-Extended
     User-agent: Applebot-Extended
     Disallow: /

     User-agent: *
     Disallow: /admin/
     Disallow: /cart/

     Sitemap: https://example.com/sitemap.xml
     ```
   - Drop `Google-Extended` from that list if Gemini app citations matter more to the business than opting out of Gemini training.
   - If server load is the worry rather than training, rate-limit at the CDN or add `Crawl-delay` for bots that honour it (Anthropic says its bots do; Google ignores it) instead of blocking.
   - Vendors take time to pick up changes: OpenAI says about 24 hours for search, Perplexity up to 24 hours.
   - Coming changes, check before implementing: Google says it aims to support a shared AI-training policy token in robots.txt, based on the IETF AIPREF work, in 2027 (October 2026 Search Central blog). Bing adopts the same training signal and adds a page-level AI grounding preference (meta tag or `X-Robots-Tag`) from 1 February 2027, replacing `NOARCHIVE` and `NOCACHE` for Copilot use.
4. **Check the firewall, CDN and other silent blockers.** robots.txt can say "allowed" while the CDN says no.
   - Review bot-fight or bot-management modes, one-click AI crawler blocking, JavaScript or CAPTCHA challenges, rate limits, country blocks and "under attack" modes.
   - Allow wanted bots by verified-bot category or published IP ranges, not by user-agent string. Some CDNs can also verify cryptographically signed agent requests (Web Bot Auth, an IETF draft); worth enabling if offered.
   - Testing with `curl -A "<bot UA>"` from your own machine only shows rules keyed on the user agent. Rules keyed on verified bots or IP reputation only show up in the CDN's logs for the real bot.
   - Also check: `noindex`, `nosnippet` or `X-Robots-Tag` headers on HTML and PDFs; cookie or consent walls that replace content in the HTML; IP-based geo-redirects (most AI crawlers fetch from US addresses, so they may never see other locales); login walls on docs or pricing.
5. **Run the text-only test.** For each key URL, fetch the raw HTML with a bot user agent: `curl -sL -A "<full user-agent string from the vendor's crawler page>" https://example.com/pricing -o pricing.html`, then search the file for the facts that matter.
   - Main content, H1, product name, prices, plan limits and internal links should be in that HTML. Many AI crawlers are reported not to execute JavaScript; Googlebot does. Core content that appears only after JavaScript runs is `Fix now` for the pages you want cited.
   - Compare with the rendered version (URL Inspection or Rich Results Test). Big differences point to client-side rendering; the fix is server-side or static rendering for those templates.
   - Title, meta description, canonical and JSON-LD should be in the raw HTML too, not injected later.
   - Read the page with JavaScript off or in a text browser (lynx, w3m). If a person can't follow it that way, a crawler can't either.
6. **Check the accessibility tree for browsing agents.** Browser agents work from screenshots, the DOM and the accessibility tree. Use Chrome DevTools' accessibility tree, Lighthouse, or Playwright's `ariaSnapshot()`.
   - Every button and link has an accessible name. Icon-only buttons without `aria-label` show up as "button" with no name: `Fix next`, or `Fix now` on signup and checkout.
   - Form fields have real `<label>` elements (placeholders don't count), clear error messages in text, and no time-limited steps without warning.
   - Core actions use real `<button>`, `<a href>`, `<select>` and `<input>`; custom widgets have correct ARIA roles and states. A `div` with a click handler is invisible as a control.
   - Pricing is readable as text: plan name, price, currency, billing period, what's included and limits. Monthly/annual toggles keep both prices in the DOM. "Contact us" pricing is a business choice; say so on the page.
   - Nothing essential depends on hover, drag, infinite scroll without paginated URLs, or a CAPTCHA on read-only pages.
   - Headings follow order, the page has `main` and `nav` landmarks, and dialogs have names.
7. **Keep URLs stable and addressable.** Agents and AI answers link to specific URLs and come back to them.
   - Key pages and states (each plan, each docs page, search results via `?q=`) have their own crawlable URL.
   - Renamed pages get a single 301 to the new URL. A 404 on an old pricing or docs URL is how AI answers end up quoting nothing, or the wrong thing.
8. **Make structured data match.** Organization on the home or About page; Product or SoftwareApplication with `offers` on product and pricing pages; Article with `author` on content; BreadcrumbList. It helps machines identify things; it's not an AI ranking switch. Values must match the visible text. Details → `schema-markup`.
9. **Decide on llms.txt.** It's a Markdown file at `/llms.txt` (or under a path such as `/docs/llms.txt`) proposed by Jeremy Howard in 2024, spec at llmstxt.org.
   - Format: an H1 with the site or project name (the only required part), a blockquote summary, optional short notes, then H2 sections that list links as `- [Title](url): one-line note`. An H2 called "Optional" holds links an agent can skip.
   - Worth adding: developer tools, APIs, SaaS with large docs or help centres, where coding assistants fetch documentation. Rarely worth it: small brochure sites, local businesses, shop catalogues. `Leave it` is a valid verdict.
   - Keep it curated (tens of links, not thousands), generated from the same source as the docs so it can't go stale, and free of marketing claims.
   - `llms-full.txt` (all docs in one file) is a common convention, not part of the proposal. Useful for API docs that fit in a model's context; skip it for large or fast-changing sites.
   - Don't promise traffic or rankings from it. Check logs after 30 to 60 days to see whether anything fetches it.
10. **Offer Markdown versions where agents read a lot.** Docs, API reference, pricing, product overview and changelog first.
    - The llms.txt proposal puts a Markdown copy at the page's URL with `.md` added (for example `/docs/setup.md`, or `index.html.md` for directory-style URLs). Advertise it with `<link rel="alternate" type="text/markdown" href="…">`. Some servers also return Markdown when a request sends `Accept: text/markdown`.
    - The Markdown must carry the same facts as the HTML. Generate it from the same source.
    - Keep `.md` copies out of search results as duplicates: send `X-Robots-Tag: noindex` on them, or an HTTP `Link: <html URL>; rel="canonical"` header.
11. **Note emerging agent standards, cautiously.** WebMCP is a proposed web standard, developed in the W3C Web Machine Learning group's repository, that lets a page expose tools to browser agents through annotated HTML forms or a JavaScript API. Chrome offers an origin trial from Chrome 149, and Google says the API is subject to change.
    - Only consider a pilot for sites with real actions an agent would take (search inventory, book, configure, get a quote). Well-labelled HTML forms are the right first step either way.
    - Label it `Worth doing` at most. It is not a search ranking factor.
12. **Re-test after changes.** Re-fetch every robots.txt, repeat the curl and accessibility checks, and watch logs for two weeks for the bots you allowed. Changes to robots.txt, firewall rules or headers need explicit approval for each change.

## What to hand back

Fill in this template. Every recommendation gets a priority label and an evidence label with confidence.

```markdown
# AI crawler and agent readiness: [domain], [date]

**What I found:** [one line, e.g. "robots.txt allows AI search bots, but the CDN challenges OAI-SearchBot and PerplexityBot."]
**What matters most:** [one line]
**What to do first:** [one line]

## Bot access
| Bot | Type | robots.txt says | Actually gets | Recommended |
|---|---|---|---|---|
| OAI-SearchBot | search | allowed | 403 challenge (CDN log) | allow verified bot |

## Draft robots.txt
[full proposed file for each host, with a comment on every changed line]

## Blockers and fixes
1. [Fix now | Fix next | Worth doing | Leave it] [issue, in plain English (term)] - where: [URL/template/setting] - fix: [change] - evidence: [seen | tool | inferred], [high | medium | low]

## Agent usability
- [element or flow]: [what an agent sees in the accessibility tree] → [fix] [priority] ([evidence])

## llms.txt and Markdown
- Verdict: [add / don't add / already fine], because [reason]. [Draft file attached if adding.]

## What I could not check
- [bots, hosts, logs or settings not seen, and what would verify them]
```

## Stop and flag if

- Any change to robots.txt, firewall rules, CDN bot settings or headers would go live. Draft it, explain the risk, and get explicit permission for that change; one wrong line can remove the site from search.
- robots.txt or the CDN blocks Googlebot or bingbot site-wide. Report this first, before anything about AI.
- The training stance is undecided, or the content is licensed, paywalled or covered by contracts. Ask the user; it's a legal and commercial decision.
- Logs show unverified bots hammering the site. Recommend verification and rate limits, not blanket AI blocks that also hit the bots you want.
- Unacceptable output: crawler names or behaviour not checked against vendor docs, claims that llms.txt or WebMCP improve rankings, advice to serve bots different content from people, or a test result reported as "seen" when it came from a spoofed user agent.

## Next step

- Run `ai-search-visibility` once search bots get through, to set a citation baseline per prompt and engine, then `ai-citable-pages` on the key pages that now pass the text-only test, so what engines lift from them is accurate.
- Run `technical-seo-audit` if the text-only test showed client-side rendering, redirect or indexing problems beyond AI bots.
- Run `schema-markup` with the list of templates whose structured data is missing or doesn't match the visible text, and `ai-brand-facts` if the Organization facts, Markdown copies or llms.txt summary disagree with each other or with the brand's profiles elsewhere.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
