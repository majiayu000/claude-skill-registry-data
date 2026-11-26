---
name: seo-start-here
description: Not sure where to start with SEO? Asks up to five quick questions, takes a quick look at the site, and recommends which RomeoSEO skills to run in what order, with what to gather first and the exact first prompt. Use for "where do I start with SEO", "help with my site's SEO", "which skill should I use".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/seo-start-here
---

# SEO start here

The front door to the library. It asks up to five short questions, takes a
quick look at the site if it can, and recommends which skills to run in what
order, what to gather before each one, and the exact first prompt to paste.
It does not do the SEO work itself; it makes sure the first hour goes on the
right problem.

> **Romeo's rule:** Most SEO time is lost doing a good job on the wrong
> problem, so spend five minutes picking the problem.

## Use this when

- You have a website (or will soon) and don't know where to start with SEO.
- Something happened (traffic fell, a move is coming, a competitor overtook
  you) and you're not sure which skill fits.
- You want a short, ordered list of what to run, not an audit.
- You've just found this library and want a sensible first route through it.

## Don't use this for

- Running the audit itself → `technical-seo-audit` or `seo-performance-audit`
- A full 90-day plan for the business → `seo-strategy-plan`
- Writing a page → `seo-content-brief`, then `seo-blog-writer`

## What you need

### Required
- The site address, or "not live yet".
- Answers to the questions in step 2. "I don't know" is a fine answer.

### Helpful
- Which of these you have: Search Console, Google Analytics, Bing Webmaster
  Tools, a crawler (Screaming Frog, Sitebulb), a keyword tool (Ahrefs,
  Semrush).
- Dates of anything that changed: a redesign, a new platform, a traffic drop.
- The draft or page URL, if the job is checking a draft.

### No tools?
Nothing is required. If the agent can't fetch pages, ask the user to open
`/robots.txt` and `/sitemap.xml` on their site and paste what they see, and to
search Google for `site:theirdomain.com` and say roughly what shows up. Every
skill in the library has a no-tools route. If Search Console isn't set up,
recommend it in almost every situation: it's free, it's Google's own data about
the site, and most later skills get much better with it.

## Ground rules

- **Route, don't do.** The job ends with a sequence and a first prompt. No
  audits, no rewrites, no changes to the site.
- **Five questions at most,** in one message, with choices. Skip anything
  the user already said. A URL plus a situation is enough to start.
- **Urgent beats interesting.** A site-wide `noindex`, a `robots.txt` that
  blocks everything, a traffic crash or a site move next week goes first,
  whatever else was asked.
- **Fewest skills that solve the problem.** Two to four in the first
  sequence, each with one line of why. Not all fifty.
- **Match how hands-on they are.** "Do it for me" → skills that produce
  drafts and lists. "Show me how" → explain each step. "Just tell me what's
  wrong" → the audits, with priorities.
- **Plain English.** Assume a founder who has never opened Search Console.
  Explain any term in brackets the first time it appears.
- **A quick look is a quick look.** Homepage, `robots.txt`, sitemap: a handful
  of requests, not a crawl.
- **Don't guess numbers.** No traffic estimates, no "you're probably ranking
  for…". Anything unchecked is "not checked".
- **Data before the skills that need it.** Name the export to gather before
  recommending a skill that can't work without it.

## Steps

1. **Read what you already have.** Pull the URL, business type, situation,
   tools and urgency out of the user's message. Only ask what's missing.
2. **Ask up to five questions,** in one message:
   1. What's your website? (address, or "not live yet")
   2. What kind of business? (software, online shop, local business or
      services, publisher or blog, agency or freelancer, other)
   3. What's going on? (new site / traffic dropped / want more traffic /
      moving the site / local business / online shop / want to show up in
      ChatGPT and AI answers / want to rank on bigger sites like LinkedIn,
      Reddit or YouTube (parasite SEO) / have a draft to check). If several,
      which hurts most?
   4. What do you have access to? (Search Console, Google Analytics, Bing
      Webmaster Tools, a crawler, a keyword tool, none, not sure)
   5. How hands-on do you want to be? (do it for me / show me how / just tell
      me what's wrong)
3. **Take a quick look,** if you can fetch URLs. Label each finding `seen`.
   - Homepage: status code and final URL after redirects (http to https, www
     or not, consistent); `<title>`; any `noindex` in the meta robots tag or
     `X-Robots-Tag` header; the canonical; whether the main text is in the raw
     HTML or the page is an empty JavaScript shell; platform hints (generator
     meta tag, `/wp-content/`, Shopify, Webflow or Framer asset hosts).
   - `/robots.txt`: missing (fine), `Disallow: /` for all bots (`Fix now`),
     important folders blocked, a `Sitemap:` line, rules for AI crawlers such
     as GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot or Google-Extended
     (note them; judging them is `ai-agent-readiness`'s job).
   - Sitemap (from `robots.txt`, `/sitemap.xml` or `/sitemap_index.xml`):
     returns XML, rough URL count, URLs on the same host and protocol as the
     live site.
   - Anything urgent goes to the top of the hand-back as `Fix now`, routed to
     `technical-seo-audit`.
4. **Pick the playbook** below that matches the situation, then adjust:
   - Online shop → add `ecommerce-seo-audit`. Local business → add
     `local-seo-audit`.
   - No Search Console → setting it up is step zero; use each skill's
     no-tools route meanwhile. `seo-performance-audit` waits until there's
     data to read.
   - Several situations → the most urgent playbook first, then one or two
     skills from the next.
5. **Say what to gather first** for the first skill, named exactly: "Search
   Console → Performance → last 16 months → export queries and pages", "every
   URL on the old site", "the draft plus the search it should rank for".
6. **Write the first prompt.** Copy-pasteable, with their URL, situation,
   what's attached, and how they want the answer. For example: "Use the
   `seo-performance-audit` skill on https://example.com. Traffic fell around
   12 March. I've attached 16 months of Search Console exports for queries and
   pages. I'm not technical: explain what happened and the first three fixes
   in plain English."
7. **Hand back** using the template. One screen, no essay.

### Situation playbooks

- **New site:** `technical-seo-audit` (baseline only: indexable, in a sitemap,
  Search Console set up) → `seo-strategy-plan` → `seo-opportunity-research`
  (pages that sell first) → `comparison-page-writer` or `seo-content-brief` →
  `seo-blog-writer` → `seo-content-qa`. Gather: what you sell and to whom, two
  to five competitors, hours per week.
- **Traffic dropped:** `seo-performance-audit` first, then by cause:
  `technical-seo-audit` (indexing or site faults), `site-migration-check`
  (drop followed a move or redesign), `search-intent-match` (pages lost to a
  different kind of result), `keyword-cannibalization-check` (your own pages
  competing). Finish with `seo-change-monitor`. Gather: 16 months of Search
  Console data, dates of releases and redesigns, and Google's Search Status
  Dashboard for update dates.
- **Want more traffic (some already):** `site-content-inventory` →
  `seo-performance-audit` (pages close to page one) → `title-meta-ctr` →
  `internal-linking-plan` → `seo-opportunity-research` → `topic-cluster-map`
  → `seo-content-brief`. Gather: Search Console exports, analytics landing
  pages with conversions.
- **Moving the site:** `seo-change-monitor` (snapshot before) →
  `site-migration-check` (redirect map and pre-launch checks) → launch →
  `site-migration-check` (post-launch) with `seo-change-monitor` (compare) →
  `xml-sitemap-check`. Adding languages or countries: `hreflang-international`.
  Gather: every old URL (crawl, sitemaps, Search Console pages export,
  analytics landing pages) and the launch date.
- **Local business:** `local-seo-audit` → `local-ai-visibility` ("near me"
  answers in ChatGPT, Gemini and AI Overviews) → `reviews-for-ai-answers`
  (honest reviews on the platforms those answers cite) → `schema-markup` →
  `on-page-seo-review` on the main service pages. Gather: Google Business
  Profile access, services, areas served, and the exact business name,
  address and phone number you use everywhere.
- **Online shop:** `ecommerce-seo-audit` → `ai-shopping-visibility` (products
  in ChatGPT shopping, AI Mode and Gemini) → `technical-seo-audit` (filters
  and duplicate URLs) → `schema-markup` (product markup) → `image-seo`.
  Gather: a crawler export if possible, Merchant Center status if you use it,
  your product feed.
- **Want to show up in ChatGPT and AI answers:** `ai-search-visibility`
  (baseline: where you're named and cited) → `ai-prompt-research` (the
  prompts buyers really ask) → `ai-agent-readiness` (are AI crawlers let in)
  → `ai-brand-facts` (fix what AI gets wrong about you) → `ai-citable-pages`
  (pages AI can quote) → `best-of-list-inclusion` (the third-party lists AI
  cites) → `ai-traffic-analytics` (AI referrals, signups, revenue). Gather:
  10 to 20 questions your customers would ask, your main competitors. If
  Google and Bing haven't indexed the site, fix that first; AI answer tools
  mostly cite pages search engines can already find.
- **Want to rank on bigger sites (parasite SEO):** `parasite-seo-plan` (which
  platforms are worth it for which searches, and which to skip) →
  `linkedin-for-ai-search` → `reddit-quora-answers` → `page-to-social-posts`
  → `sponsored-placement-vetting` (before paying for any sponsored or guest
  post). Gather: the searches or AI prompts you want to appear for, the real
  people who will post under their own names, your best existing pages.
  Owned, named profiles and disclosed affiliation only; no bought accounts or
  mass posting.
- **Have a draft to check:** `seo-content-qa` → if it misses what searchers
  want, `search-intent-match`; if it's a comparison, rebuild its fact-check
  sheet with `comparison-page-writer` → `cms-publishing-adapter` → once live,
  `on-page-seo-review`. Gather: the draft, the target search, the brief if
  any, your product facts.

### All 50 skills

**Start**
- `seo-start-here`: a few questions and a quick look, then which skills, in what order.
- `site-content-inventory`: every page with its intent, keywords, performance and status.
- `seo-strategy-plan`: a 90-day plan: goals, priorities, content pillars, what to skip.

**Research**
- `seo-opportunity-research`: keywords worth targeting, and create vs improve.
- `topic-cluster-map`: keywords grouped by shared results into hubs and spokes.
- `search-intent-match`: is this the kind of page Google ranks for the query?

**Fix**
- `technical-seo-audit`: crawling, indexing, rendering, redirects, canonicals, speed.
- `on-page-seo-review`: one URL in depth against its target query.
- `seo-performance-audit`: what rose, dropped or stalled in Search Console, and why.
- `keyword-cannibalization-check`: your pages competing for one query: merge or split.
- `internal-linking-plan`: orphan pages, weak links, and the exact links to add.
- `schema-markup`: find, validate and write JSON-LD for rich results.
- `xml-sitemap-check`: sitemaps against what should actually be indexed.
- `hreflang-international`: languages, regions and localized URLs.
- `image-seo`: alt text, formats, sizes, lazy loading, image search.
- `site-migration-check`: redirect maps and checks for domain, URL or platform moves.
- `seo-change-monitor`: snapshot SEO signals, compare after deploys.
- `backlink-profile-review`: link profile health and realistic link opportunities.

**Content**
- `seo-content-brief`: turn a chosen opportunity into a precise brief.
- `seo-blog-writer`: write the draft from an approved brief.
- `comparison-page-writer`: honest "best X", "X vs Y" and "alternatives" pages.
- `landing-page-writer`: complete product and feature landing pages from your own proof and screenshots.
- `seo-content-qa`: score a draft before it ships.
- `title-meta-ctr`: better titles and descriptions for pages that get seen but not clicked.
- `eeat-trust-review`: experience, expertise and trust signals.
- `programmatic-seo-plan`: template pages at scale without thin or duplicate content.

**AEO, LLM SEO, GEO**
- `ai-search-visibility`: get cited in AI Overviews, AI Mode, ChatGPT, Perplexity, Copilot, Claude.
- `ai-prompt-research`: the prompts buyers ask AI tools, with demand signals, in priority order.
- `ai-brand-facts`: find what AI gets wrong about the brand, trace it to the source, fix it there.
- `chatgpt-business-profile`: claim and set up the business in ChatGPT's Business Hub, profile and agent tests included.
- `ai-citable-pages`: restructure a page so AI can lift accurate, self-contained answers.
- `query-fan-out-coverage`: the sub-questions behind a money prompt, mapped to pages, gaps filled.
- `google-ai-overviews-audit`: Search Console's AI data: cited, shown but not cited, losing clicks.
- `best-of-list-inclusion`: earn a fair place on the third-party "best X" lists AI cites.
- `reviews-for-ai-answers`: honest reviews on the platforms AI cites for your category.
- `youtube-for-ai-answers`: videos AI engines cite: topics, titles, chapters, captions.
- `local-ai-visibility`: "near me" answers in ChatGPT, Gemini, Copilot, AI Overviews and Siri.
- `ai-shopping-visibility`: products in ChatGPT shopping, AI Mode, Gemini and Perplexity.
- `ai-traffic-analytics`: measure AI referrals, signups and revenue, including hidden AI traffic.
- `dataforseo-ai-tracker`: track AI answers at scale through the DataForSEO API, with cost caps.
- `ai-agent-readiness`: AI crawler rules, llms.txt, Markdown versions, agent-usable pages.

**Parasite SEO**
- `parasite-seo-plan`: which third-party platforms to publish on, per search, and which to skip.
- `page-to-social-posts`: one page into distinct posts for your own accounts, human-approved.
- `reddit-quora-answers`: honest, disclosed answers in threads that rank or get cited.
- `linkedin-for-ai-search`: LinkedIn articles and posts from a real person, written to be cited.
- `sponsored-placement-vetting`: vet sponsored posts, guest posts, syndication and press releases.

**Local and shop**
- `local-seo-audit`: Business Profile, local pages, NAP, reviews, map pack.
- `ecommerce-seo-audit`: product and category pages, filters, product data.

**Publish**
- `cms-publishing-adapter`: approved content into a CMS draft or static-site package.
- `posthog-change-impact` measures website changes against business goals in PostHog.

## What to hand back

One screen, in this shape:

```markdown
**What I found:** <business, situation, stage, anything urgent from the quick look>
**What matters most:** <the one problem to solve first, in plain English>
**What to do first:** <the first skill, and what to gather for it>

## Quick look
- Homepage: <finding> (seen, <confidence>)
- robots.txt: <finding> (seen, <confidence>)
- Sitemap: <finding> (seen, <confidence>)
- Not looked at: <anything skipped, and why>

## Your sequence
1. `Fix now` `<skill>`: <why, one line>. Gather first: <exact export or file>.
2. `Fix next` `<skill>`: <why>. Gather first: <...>.
3. `Worth doing` `<skill>`: <why>.
- `Leave it` for now: `<skill>`: <why it can wait>.

## Your first prompt (copy and paste)
> <exact prompt, with their URL and context filled in>

## What I could not check
- <Item>: <what would verify it>
```

## Stop and flag if

- The quick look shows an emergency: site-wide `noindex`, `robots.txt`
  blocking everything, homepage errors, spam pages the owner didn't create, or
  a manual action the user mentions. Say it first and plainly, then route to
  `technical-seo-audit`.
- The user asks you to change something. This skill is read-only; recommend
  the skill and get permission for each specific change.
- The URL redirects to a different business or domain than described.
  Confirm before going further.
- The need isn't SEO (paid ads, app store ranking, social media growth for
  its own sake). Say so rather than forcing a skill.
- The output is unacceptable if the first sequence has more than five skills,
  the first prompt can't be pasted as-is, or any number is invented.

## Next step

- Paste the first prompt from the hand-back into a new message, with the
  files it asks for.
- Most skills name their own next step. Come back here only if the route
  stops making sense.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
