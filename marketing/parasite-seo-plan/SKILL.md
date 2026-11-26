---
name: parasite-seo-plan
description: Plan parasite SEO (barnacle SEO) that lasts. Pick which third-party platforms, such as Reddit, YouTube, LinkedIn, Quora or Medium, are worth publishing on for your target searches and AI answers, scored on ranking power, AI citations, rules and ban risk. Use for "where should we post outside our site" or "can we rank on Reddit".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/parasite-seo-plan
---

# Plan where to publish off your own site

Work out which third-party platforms already show up in Google results and AI answers for the searches a site wants, score each one on what it can realistically deliver and what it can cost, cut every tactic that breaks Google's spam policies or the platform's rules, and set up real, named profiles to publish from. You hand back a per-platform verdict (go, test or skip) with the evidence behind it, a no-go list, a profile setup list, a measurement plan, and which skill does each piece of work.

> **Romeo's rule:** Borrow a platform's audience by being useful there under your own name; borrowing its ranking signals with content nobody there asked for is what Google's spam policies were written to stop.

## Use this when

- The site is new or weak, and the searches it wants are full of Reddit threads, YouTube videos, LinkedIn articles or Quora answers.
- AI answers for the money prompts cite platform pages (threads, articles, videos) and never the site itself.
- Someone pitches "parasite SEO" and you need to know which parts are safe, which are spam, and which are a waste of time.
- The team has a few hours a week and must choose one to three platforms instead of posting everywhere.
- A platform account was warned, restricted or banned, and you need a plan that won't repeat it.

## Don't use this for

- Vetting sponsored posts, guest posts, syndication deals or press releases before paying → `sponsored-placement-vetting`.
- Doing the platform work itself → `reddit-quora-answers`, `linkedin-for-ai-search`, `youtube-for-ai-answers`, or `page-to-social-posts` for the brand's own social accounts.
- The full AI visibility baseline across engines, with mention and citation rates → `ai-search-visibility`.
- Getting a fair place on third-party "best X" articles and review sites → `best-of-list-inclusion` or `reviews-for-ai-answers`.

## What you need

### Required

- The domain, what it sells, who buys it, and the target country and language.
- 15 to 40 target searches or AI prompts, ideally from `seo-opportunity-research`, `ai-prompt-research` or Search Console, not guessed.
- Who will publish: named people (founder, experts, staff) willing to post under their own names, and the hours per week each can give.
- Existing platform accounts: handle, age, rough activity history, and any past warnings, removals or bans.

### Helpful

- The citation-source map from `ai-search-visibility` (which domains each engine cites for the money prompts).
- Search Console Performance export (queries, last 3 months) and analytics referral data from reddit.com, youtube.com, linkedin.com, quora.com, medium.com and facebook.com.
- A rank tracker or SERP export that lists every result URL per query, so you can count platform domains without manual searching.
- Any content assets that travel well: original data, how-to videos, founder talks, customer stories with permission.

### No tools?

Search each representative query in a private window set to the target country and note every platform URL in the top 10, plus platform URLs inside the "Discussions and forums", video and short-video blocks. Run the same queries in ChatGPT with search on, Perplexity, Gemini and Google AI Mode, two or three times each in fresh sessions, and copy every cited link. `site:reddit.com [topic]` and `site:quora.com [topic]` find threads Google has indexed. Check a platform's link attributes by right-clicking a link on the page, choosing Inspect, and reading its `rel` and `href`. Log everything in a spreadsheet.

## Ground rules

- The version of parasite SEO that lasts is being present, as yourself, where buyers already read. If a tactic needs a fake account, a rented page on someone else's site or a hundred posts a day, it's the version that gets removed.
- Plan for zero link equity. Most platform links are `nofollow`, `ugc` or routed through a redirect. Success is the platform URL ranking or being cited, referral visits, branded search and AI citation share.
- Choose platforms from the user's own query evidence, never from a platform's reputation. Shares swing month to month: Reddit's share of ChatGPT citations collapsed in September 2025 and again in August 2026. Vendor studies are directional.
- Third-party content on a host isn't a violation by itself. Google's site reputation policy targets content placed on a host mainly to exploit the host's ranking signals; original, authored content that belongs on the platform is the opposite of that.
- When Google acts under that policy, the host's section gets the manual action and the outside author's content simply stops ranking. Either way, the borrowed ranking is gone.
- One to three platforms done well beat six done badly. Every chosen platform gets a named owner and a weekly time budget.
- Platform rules are the floor and community rules (subreddits, groups, Spaces) are stricter. Read both before the first post, not after the first removal.
- One real account per person per platform, with name, role and company affiliation visible. A human approves every post, and posting is manual or through the platform's official API or native scheduler.
- Google's spam policies now list attempting to manipulate generative AI responses in Google Search as spam. Anything written to plant claims for AI rather than to inform people is off the plan.
- No ranking promises and no timelines. New accounts often aren't indexed at first (see step 8).

## Steps

1. **Group the target queries.** Sort the 15 to 40 queries into 3 to 8 groups by what the searcher wants.
   - Typical groups: problem or how-to, "best X for Y", comparisons and alternatives, reviews and "is X legit", local, brand.
   - Pick 3 to 5 representative queries per group and mark the groups where being found leads to a sale (money groups).
2. **Sample Google results per group.** For each representative query, record the top 10 in a clean session for the target country.
   - Per platform result: domain, URL, position, page type (thread, answer, article, video, short, profile, group post), content date, and whether it mentions the brand or competitors.
   - Also log platform URLs in the "Discussions and forums", video and short-video blocks; they count as ranking even outside the ten blue links.
   - Forum and video results move a lot. If you can, sample again a week later and keep both dates.
3. **Sample AI answers per group.** Reuse the `ai-search-visibility` source map if it exists. Otherwise run each representative query 2 to 3 times on the engines the audience uses (Google AI Overviews and AI Mode, ChatGPT search, Perplexity, Gemini, Copilot) in clean sessions.
   - Log every cited platform URL, the engine, the run, and whether the brand or a competitor is named in the cited page.
   - Copilot leans on shopping sites and Wikipedia (Amazon 16.8%, Walmart 12.6%, Wikipedia 7.6% of citations; Reddit, Quora and Medium outside its top 50; Ahrefs, Sep 2026, vendor data). For a Copilot-heavy audience, platform work matters less.
4. **Build the platform log.** One row per platform domain: share of sampled queries where it ranks in the top 10, citation rate per engine, which query groups, which page types win.
   - Drop platforms that appear nowhere in your samples unless there's a separate business reason (an audience that lives there).
   - Note who already wins there: competitors' named profiles, independent creators, or nobody in particular (an opening).
5. **Score each platform.** Rate each factor low, medium or high, with the evidence next to it. Don't add the ratings into a composite score; decide in words.
   - Ranking power for these queries: from step 2, not from domain metrics.
   - AI citation frequency: from step 3, per engine.
   - Link attributes: inspect a real link (`rel="nofollow"`, `ugc`, a redirect URL). Expect referral value only.
   - Rules on promotional and automated content: quote the clause from the platform's current policy page that limits you.
   - Ban or penalty risk: account removal, content removal, and whether the content would fall under a Google spam policy.
   - Effort: hours per item, skills needed (video, writing, community history), and how long before anything can show up.
   - Verdict: `Go` (evidence on money groups, rules allow what you'd do, owner has time), `Test` (some evidence, limited trial with a stop date) or `Skip`.
6. **Check the 2026 state of each platform.** Facts below are as of November 2026, and platform shares are vendor data; re-read each platform's policy page before acting.
   - Reddit: frequent in Google results for questions and comparisons, but volatile; one of the two most-cited domains across AI engines (Peec AI, Mar 2026, vendor data), though its ChatGPT share collapsed twice (Sep 2025, Aug 2026). Its spam policy bans mass-posting repetitive content for exposure or money, using bots or generative AI tools to spread spam, and multiple accounts, and tells people who mostly post links to their business to limit frequency or buy ads. Treat links as `nofollow`. Risk: high for automation, low for genuine disclosed participation.
   - YouTube: the largest share of platform results in Google in one vendor study (25.8% of 6,620 US searches, Oct 2026, method unpublished); the most-cited domain in AI Mode and AI Overviews (Peec AI, Mar 2026); YouTube mentions correlated about 0.74 with AI visibility (Ahrefs, Dec 2025). Its spam policy bans using automated tools or AI to churn out high volumes of similar content with minimal changes. Description links pass through a redirect. High effort, very durable.
   - LinkedIn: Pulse articles' Google traffic collapsed (about -85% US organic visits, Mar 2024 to Jan 2026, Growtika/Ahrefs estimates), yet LinkedIn appeared in 14.3% of ChatGPT search answers, 13.5% of AI Mode and 5.3% of Perplexity answers (Semrush, Mar 2026, 325k prompts, vendor data). Copilot rarely cites it. Article links go through `/redir/redirect`, blocked for Googlebot; post and comment links are `nofollow`. The User Agreement (effective 3 Nov 2025) bans bots, unauthorised automation and false identities.
   - Quora: Google traffic falling (around -45% year on year in 2025, third-party estimates); modest AI citations (about 1.5% of AI Overview citations, Profound 2024-25, vendor data). Bans repeated content, promotional questions and answers, irrelevant links and multiple accounts. Usually `Test` at most.
   - Medium: weak in Google (3.1% of platform results in the vendor study above) but notable in AI Overviews (#5) and Gemini (#4) citations (Peec AI, Mar 2026). Links are `rel="noopener ugc nofollow"`. Rules ban posting primarily to drive traffic to, or raise the rankings of, an external site, clipped teaser posts, and posting automatically, systematically or programmatically. Self-promotion of your own business is allowed; affiliate links need disclosure. Republish your own full articles with Medium's import tool, which sets the canonical to the original.
   - Substack: fine for a real newsletter people subscribe to. Its Content Guidelines (updated 29 Sep 2026) don't permit publications whose primary purpose is advertising, driving traffic to third-party sites or enhancing search engine optimization.
   - Facebook: 19.4% of platform results in the vendor study above, mostly local searches; the #3 cited domain in AI Mode and AI Overviews (Peec AI, Mar 2026). It blocks Perplexity's crawlers, so it won't appear there. Mainly worth it for local businesses and real communities.
   - Blogger, GitHub Pages, Google Sites, Notion: each blog or site behaves like a separate new site or a thin page on a user-content host (blogspot.com, github.io and notion.site are on the Public Suffix List), so there's little authority to borrow. All ban automated or unwanted promotional content, and GitHub's terms say Pages isn't for running an online business. Low upside, medium risk: `Leave it`, except genuine project docs.
   - X, Instagram, Threads, Pinterest, Bluesky: rarely rank for non-brand queries in samples like these (`inferred`; check yours); Pinterest can rank for visual queries such as recipes, decor and crafts. Treat them as distribution for the brand's own accounts.
7. **Apply the no-go list.** Remove anything in the current or proposed plan that matches one of these, and say which policy it breaks.
   - Renting pages or subfolders on reputable sites (coupon, "partner content" or review sections run without the host's editorial oversight): the site reputation policy's core case.
   - Substacks made for SEO, affiliate-only Tumblr blogs, and business or affiliate sites on GitHub Pages, Google Sites or Notion: banned by the platforms' own rules.
   - Doorway pages: many near-identical pages per city, product or keyword on any host.
   - Fake, bought, borrowed or aged accounts; more than one account per person; vote rings and engagement pods.
   - Mass AI posting or templated content across many posts, videos or platforms: scaled content abuse in Google's terms, wherever it's hosted.
   - Keyword-rich anchor links in guest posts or press releases, and paid links not marked `rel="sponsored"` or `nofollow`: link spam.
   - Content designed to make AI repeat a claim (planted "best X" posts, hidden instructions, coordinated mentions): the generative AI manipulation line in the spam policies.
8. **Check the plan against Google's policies.** Read the current spam policies page (developers.google.com/search/docs/essentials/spam-policies) and test each remaining item.
   - Site reputation policy: Google weighs the host's involvement and oversight, presentation, quality, authorship, and whether the same content appears elsewhere. An authored, original piece under real editorial control is "unlikely" to be actioned; an unauthored copy placed for its ranking is the textbook case.
   - Since 30 Aug 2026, inside the EEA, Google may separate the affected section so it ranks on its own instead of applying the manual action's impact; outside the EEA nothing changed. The borrowed signals are gone in both cases.
   - Scaled content abuse: many pages made mainly to manipulate rankings, however they're produced.
   - Link spam: automated link creation, optimised anchors in guest posts and press releases, forum signature links, low-quality directories, unmarked paid links.
   - Google's guidance for user-content platforms (prevent-abuse page, updated Oct 2026) suggests noindexing posts from new users with no reputation and marking their links `nofollow` or `ugc`. Expect a new account's posts to rank late or not at all; history matters.
9. **Set up real, owned profiles.** For each `Go` or `Test` platform:
   - A named person's account (real name, photo, role, company in the bio) and, where the platform has one, the official company page or channel. No personas.
   - Bio links to the site's About or author page, and that page links back. Add the profiles to the author's `Person` and the company's `Organization` markup as `sameAs` (→ `schema-markup`).
   - The same brand name and one-line description as everywhere else (→ `ai-brand-facts`).
   - Company accounts registered to a company email with two-factor sign-in and at least two admins; agree in writing what happens to a personal account's company content if the person leaves.
   - A history of genuine participation before any self-mention on community platforms (→ `reddit-quora-answers`).
10. **Set the operating rules.** One line per platform: owner, cadence, approval step, posting method, disclosure wording.
    - Cadence the owner can keep for 3 months, for example two LinkedIn posts a week and one article a month, or one YouTube video a month. A schedule nobody keeps is worse than a smaller one.
    - Every post approved by a named human before it goes out; manual posting, the platform's native scheduler or its official API only. No browser automation, account tools or AI auto-posting.
    - Disclosure: affiliation stated wherever the product is mentioned, paid partnerships labelled with the platform's own tool, affiliate links disclosed.
11. **Plan the measurement.** Agree it before the first post.
    - Monthly: platform URLs ranking for the sampled queries (same queries, same method), AI citations of those URLs (re-run through `ai-search-visibility`), referral sessions per platform (UTM-tagged links where the platform allows them, referrer data where it doesn't), Search Console impressions for brand queries, and signups or leads from those sessions.
    - Never report link counts or domain metrics as the result of this work.
    - Stop rule per `Test` platform: if nothing ranks, gets cited or sends visits after an agreed number of posts or 90 days, stop and move the hours elsewhere.
12. **Route the work.** Hand each `Go` platform to its skill with its query groups, owner and rules: `reddit-quora-answers`, `linkedin-for-ai-search`, `youtube-for-ai-answers`, `page-to-social-posts`, `reviews-for-ai-answers`, `best-of-list-inclusion`; any paid placement to `sponsored-placement-vetting` first.

## What to hand back

Fill in this template. Every recommendation gets a priority label and an evidence label with confidence.

```markdown
# Parasite SEO plan: [brand], [date]

**What I found:** [one line, e.g. "Reddit ranks for 9 of 15 sampled queries and is cited in 40% of AI runs; Medium appears nowhere."]
**What matters most:** [one line]
**What to do first:** [one line]

## Method
- Queries: [n] in [groups]; Google samples: [dates, country]; AI runs: [engines, runs per prompt, dates]

## Platform evidence
| Platform | Ranks in top 10 (queries) | AI citations (engine, rate) | Groups | Page types |
|---|---|---|---|---|

## Platform scores and verdicts
- [Platform]: ranking [l/m/h], AI citations [l/m/h], links [attribute seen], rules [clause], risk [l/m/h], effort [l/m/h]. Verdict: [Go | Test until date | Skip] - why: [reason] - [Fix now | Fix next | Worth doing | Leave it] ([seen | tool | inferred], [high | medium | low])

## Removed from the plan (no-go)
- [tactic]: breaks [policy or platform rule]; instead: [alternative or nothing]

## Profiles to set up
- [Platform]: [person or company page], bio: [text], links: [URLs], sameAs: [yes/no], admins: [names]

## Operating rules
- [Platform]: owner [name], cadence [x], approval [who], method [manual / native scheduler / official API], disclosure [wording]

## Measurement and stop rules
- [metric, source, baseline, review date]; stop if [condition]

## Next skills
- [skill]: [query groups and inputs]

## What I could not check
- [e.g. engines not sampled, link attributes not inspected, platform policy pages that didn't load]
```

## Stop and flag if

- The user wants multiple accounts, bought or aged accounts, vote or engagement swaps, unofficial automation, or AI posting at volume. Decline that part and say which rule it breaks.
- The plan depends on renting a page or section on another site. Pause it and run `sponsored-placement-vetting` first.
- Nobody will publish under their own name. Say the plan shrinks to company pages and owned channels, and don't invent a persona.
- An account was banned or restricted. Don't create a new one to get around it; ban evasion breaks most platforms' terms. Appeal through the platform's official process.
- The category is regulated (health, finance, gambling, legal, cannabis or CBD). Platforms restrict promotion there and disclosure rules are stricter; get the user's compliance owner involved.
- Unacceptable output: invented ranking or citation rates, a composite platform score, any promise of link equity or rankings, or a plan that names or relies on a commercial parasite SEO product.

## Next step

- Run `reddit-quora-answers` with the threads logged in steps 2 and 3 if Reddit or Quora got `Go` or `Test`.
- Run `linkedin-for-ai-search` with the prompts where LinkedIn URLs were cited, and the named author.
- Run `page-to-social-posts` on the site's strongest page for the brand's own accounts, at the cadence agreed in step 10.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
