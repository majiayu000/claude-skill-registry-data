---
name: backlink-profile-review
description: Review a site's backlinks for health, risk and realistic new link opportunities. Use for "check our backlinks", "do we have toxic links", "should we disavow", "we got an unnatural links manual action" or "why do competitors have more links". Covers referring domains, anchors, lost links, 404 reclaim and competitor link gaps.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/backlink-profile-review
---

# Review your backlink profile

Read the link data from Search Console, Bing Webmaster Tools and any third-party exports, separate the links that matter from the background noise, flag the patterns that are genuinely risky, recover links the site has already earned but is wasting, and find a short list of realistic places to earn more. You hand back a profile summary, a risk verdict (which is almost never "disavow"), a reclaim list of redirects, and ranked link opportunities with who to contact.

> **Romeo's rule:** Fix the links you already earned and are wasting before chasing new ones; a 301 on a dead URL is the cheapest link you'll ever get.

## Use this when

- Someone asks "do we have toxic backlinks?" or "should we disavow?", usually after a tool showed a scary score.
- Search Console shows a manual action for unnatural links.
- Referring domains spiked or dropped suddenly, or someone fears negative SEO.
- After a migration or redesign, to find links now pointing at dead URLs.
- Planning link acquisition, or asking why competitors outrank you with similar content.
- Due diligence before buying a domain or a business.

## Don't use this for

- Links between your own pages, orphan pages and anchor text inside the site → `internal-linking-plan`.
- Building a full redirect map for a domain or platform move → `site-migration-check`.
- Getting mentioned and cited in AI answers → `ai-search-visibility`; reputation and trust signals beyond links → `eeat-trust-review`.
- Deciding whether to pay for or accept a specific sponsored post, guest post, syndication deal or press release → `sponsored-placement-vetting`.

## What you need

### Required

- The domain, and access to Search Console (or exports from its Links report and Manual actions report).
- The site's link-building history: agencies used, guest posting, PR, sponsorships, link exchanges, purchased links. Ask directly; it decides whether a disavow is ever justified.

### Helpful

- Bing Webmaster Tools backlink exports for your site and its competitor comparison.
- Third-party exports (Ahrefs, Semrush, Majestic or Moz): referring domains and backlinks with first-seen and lost dates, anchor text, target URL, link attributes and the target's HTTP status.
- A crawl or list of URLs returning 404 or 410, and the Search Console Pages report (Not found).
- 3 to 5 search competitors: the domains that rank for your target queries, which may not be your business rivals.
- Dates of migrations, redesigns, PR campaigns or past link work, to explain spikes and losses.

### No tools?

Search Console's Links report is free: Top linked pages, Top linking sites and Top linking text, plus an export from the report's main page of up to 100,000 rows ("Latest links" and "More sample links"). Bing Webmaster Tools' Backlinks report is free, can be exported, and can compare your referring domains with other sites, including domains that link to them and not to you. Check Security & Manual actions → Manual actions in Search Console. Find unlinked mentions with a Google search for `"Brand" -site:example.com`. Check target URLs' status codes with a browser or `curl -I`. Some link tools offer free tiers for verified sites; none are required.

## Ground rules

- No source sees every link. Search Console shows a sample (tables cap at 1,000 rows), includes links that may no longer exist, and doesn't say which links are `nofollow`. Third-party crawlers each see a different slice of the web.
- Third-party metrics (Domain Rating, Authority Score, Domain Authority, Trust Flow, "toxicity" scores) are vendor estimates, not Google values. Use them to sort, never as proof, and never present them as how Google sees a site.
- Count referring domains, not links. 4,000 sitewide footer links from one partner are one relationship.
- Relevance and real readers beat metrics. A link from a small, active site in your niche that sends visitors is worth more than a high-score domain about everything.
- Most spammy links are noise. Scrapers, auto-generated directories and "website worth" pages link to every site with traffic, and Google says it can usually work out which links to trust without help. A tool's "toxic" label alone is never a reason to act.
- Disavow only in two cases: a manual action for unnatural links, or a link scheme the site itself built (paid links without `rel="sponsored"`, private blog networks, large-scale exchanges) that you can't get removed. Google calls the disavow tool advanced and warns that misuse can hurt performance.
- Buying or selling links for ranking breaks Google's link spam policy. Paying for ads, sponsorships or advertorials is fine when the link carries `rel="sponsored"` or `rel="nofollow"`. "Guest posts" sold with followed links and "link insertions" into old articles are paid links with a different invoice. Vet a specific offer with `sponsored-placement-vetting`.
- `nofollow`, `ugc` and `sponsored` are hints to Google, not walls. Such links still bring visitors, brand searches and mentions that AI answers draw on; don't dismiss them, and don't count on them for ranking value either.
- No promises: never estimate ranking gains per link, and never invent link counts or metrics. Unknown is "not checked".

## Steps

1. **Gather and normalise the data.** Merge the exports into one sheet with the source of each row.
   - Normalise to referring domain (root domain), deduplicate, and keep first-seen and lost dates where available.
   - Write down each source's limits and date range. Results from Search Console alone are a sample; say so in the hand-back.
2. **Check for manual actions first.** Search Console → Security & Manual actions → Manual actions.
   - "Unnatural links to your site" changes the job: clean-up and a reconsideration request come before anything else. `Fix now`.
   - "Unnatural links from your site" means outbound links the site sold or exchanged; mark them `rel="sponsored"` or remove them, then request reconsideration.
   - No manual action and no self-built link scheme? Then a disavow is off the table for the rest of this review.
3. **Describe the profile's shape.**
   - Number of referring domains and the trend over 12 months (from a tool with history, labelled `tool`).
   - The top 30 to 50 referring domains: what share are topically related, in your market's language and country, and real sites with readers.
   - Link types: editorial links in body text, reviews, directories, partner and integration pages, profiles, forums, comments, sitewide footers, images.
   - Target pages: share pointing at the home page versus deep pages, and which pages earn links naturally (usually tools, data, templates and guides). These show what to make more of.
   - Buying a domain or site: compare the anchors' languages and topics with its history in the Wayback Machine. Foreign-language casino or pharma anchors on an English B2B domain mean a spam past; price that in.
4. **Check the anchor text mix.** Group anchors into branded, URL, generic ("here", "this site"), topical phrases, exact-match commercial ("best payroll software uk"), and empty or image anchors.
   - Natural profiles are mostly branded, URL and generic. There is no safe percentage; compare with the top competitors' profiles.
   - Red flag: a cluster of exact-match commercial anchors pointing at money pages from blogs and guest posts. That pattern usually means links were built, so ask about past link work. `Fix next` to investigate, `Fix now` if there's a manual action.
5. **Explain spikes and losses.**
   - Spike in referring domains: open a sample. Scraper and spam networks (ignore, `Leave it`), a viral piece or press coverage (good; find who linked and thank them), a negative SEO attempt (Google usually ignores these; monitor only), or links someone bought (act as in step 2).
   - Lost links: split into link removed, linking page gone, target redirected, and link changed to `nofollow`. Contact the top lost referring domains when an editorial link vanished in their redesign, with the exact page and a working URL.
6. **Check link attributes on both sides.**
   - Inbound: share of `nofollow`, `ugc` and `sponsored` (third-party exports show this; Search Console doesn't). Very high followed shares from obviously paid placements are a risk sign.
   - Outbound: anything the site was paid for (sponsored posts, affiliate links, partner listings) carries `rel="sponsored"`. Missing = `Fix now` if it's a pattern.
   - Outbound links nobody remembers adding (casino, pharma or loan anchors in footers, old posts or plugin output) usually mean the site was hacked. Treat it as a security incident first → `technical-seo-audit`.
7. **Reclaim links pointing at dead URLs.** Usually the fastest win in the whole review.
   - Join every backlink target URL with its current status: 404, 410, soft 404, redirect chains (more than one hop) and loops. In Search Console, the per-site backlink table's "Target URL (if different)" column shows links that land through a redirect.
   - 301 each dead target to the closest equivalent live page. Don't send everything to the home page; Google may treat irrelevant redirects as soft 404s and the value is lost.
   - Collapse chains into a single hop; fix variants caused by case, trailing slashes or `http` versions.
   - Sort by referring domains to the dead URL. Many good domains pointing at dead URLs after a migration = `Fix now`. Redirect changes need approval before they go live.
8. **Make the risk call.** Classify questionable domains as ignore (noise), monitor, or remove/disavow (only for step 2 cases).
   - If a disavow is justified: ask for removal first and keep a record of the outreach. Then a UTF-8 or 7-bit ASCII `.txt` file, one URL or `domain:example.com` per line, `#` for comments, uploaded with Search Console's disavow tool. A new upload replaces the old list; it can take weeks to apply. File a reconsideration request if there's a manual action.
   - Never disavow good or neutral links "to be safe", and never import a tool's whole "toxic" list.
9. **Run a competitor link gap.** Take 3 to 5 search competitors.
   - Find domains linking to two or more competitors but not to you (Bing Webmaster Tools' comparison, or a link-intersect report in a third-party tool).
   - Classify each linking page by why it links: review or listicle, integration or partner, customer story, resource page, news or PR, data citation, community thread, directory, sponsorship or paid. Drop paid placements and network sites.
   - List the competitors' most-linked pages and why they earn links. That's your content brief for linkable assets.
10. **Build the opportunity list, realistic only.** For each, give the target page, who to contact, why they would say yes, effort and likelihood.
    - Unlinked brand mentions: pages that name the brand or product without linking. A short, polite request converts better than any cold outreach.
    - Partner, integration and customer pages: tech partners' integration directories and marketplaces, suppliers, associations you belong to, customers with "powered by" or case-study pages. Real relationships only.
    - Resource pages: curated "tools" or "useful links" pages in your niche, when you have something genuinely worth listing.
    - Original data and digital PR: a survey, benchmark or dataset with one clear finding, pitched to journalists and newsletters that cover the topic.
    - Broken-link replacement: dead outbound links on relevant pages that used to point at a resource like yours (check what it was in the Wayback Machine), and offer yours as the replacement.
    - Never: buying followed links, private blog networks, link exchanges at scale, paid "dofollow guest posts", link insertions, or automated outreach blasts.

## What to hand back

Fill in this template. Every recommendation gets a priority label and an evidence label with confidence.

```markdown
# Backlink profile review: [domain], [date]

**What I found:** [one line, e.g. "112 referring domains, mostly relevant; 38 of them point at URLs that now 404."]
**What matters most:** [one line]
**What to do first:** [one line]

## Data used
- [Search Console Links export, date] / [Bing Webmaster Tools, date] / [third-party tool, date]. Limits: [sample, missing attributes, etc.]
- Manual actions: [none / "Unnatural links to your site" since date / not checked]

## Profile summary
- Referring domains: [n] ([source]); trend: [up / flat / down, or not checked]
- Relevance: [share of top 50 that are on-topic], anchor mix: [branded / URL / generic / commercial shares], top linked pages: [list]

## Risk verdict
- [No action needed | Investigate | Clean up and reconsider], because [reason]. Disavow: [not recommended / recommended for these domains because of manual action or self-built scheme].

## Reclaim list (redirects)
| Dead URL | Referring domains | Redirect to | Priority |
|---|---|---|---|

## Fixes and opportunities, in order
1. [Fix now | Fix next | Worth doing | Leave it] [action] - target page: [URL] - contact: [who] - why they'd say yes: [reason] - evidence: [seen | tool | inferred], [high | medium | low]

## What I could not check
- [e.g. link attributes (Search Console doesn't report them), lost-link dates, competitors' full profiles]
```

## Stop and flag if

- There's a manual action. Pause opportunity work and lead with clean-up and reconsideration.
- The profile shows signs of bought links and the user hasn't told you the history. Ask before recommending removal or disavow.
- The user asks you to buy links, find link sellers, set up exchanges or disavow everything a tool flags. Decline that part and explain the policy.
- The only data is the Search Console sample and the question needs totals or trends. Say what can't be concluded.
- Unacceptable output: invented link counts or authority scores, any vendor metric presented as Google's, a disavow recommendation without a manual action or a self-built scheme, or redirect changes made without permission.

## Next step

- Run `site-migration-check` if most dead link targets came from a past migration, with the reclaim list as input.
- Run `internal-linking-plan` to pass value from the pages that attract the most links to the pages that need it.
- Run `seo-content-brief` for a linkable data asset or tool, using the competitors' most-linked pages as evidence.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
