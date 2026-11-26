---
name: eeat-trust-review
description: Review a page and its site for experience, expertise, authoritativeness and trust the way a Google quality rater would. Use for "check our E-E-A-T", "do we need author bios", "is our site trustworthy enough for health or finance content" or traffic lost after a core update. Returns trust gaps with fixes and spam-policy risks.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/eeat-trust-review
---

# Review experience, expertise and trust

Look at one page, and the site around it, the way a Google search quality rater is trained to: who is responsible for it, why they should be believed, whether the page shows the author has actually done or used what it describes, and whether anything looks deceptive. You hand back the trust gaps a rater would notice, each with a concrete fix, a priority and the evidence, plus any spam-policy risks that need attention before content work.

> **Romeo's rule:** Trust is shown, not claimed; one real photo of the product on your own desk beats three paragraphs about your passion for excellence.

## Use this when

- Traffic dropped around a Google core update, especially on health, money, legal, safety or product-review pages.
- The site publishes "Your Money or Your Life" topics: health, finance, legal, safety, major purchases, civic information.
- Content is written by AI, freelancers or an anonymous "Team", with no bylines or author pages.
- Before launching affiliate, review or comparison content.
- A page covers the topic as well as the pages above it but still sits below them, and credibility is the obvious difference.

## Don't use this for

- Whether the page is the right format and angle for its query → `search-intent-match`.
- Scoring a draft before publication → `seo-content-qa`.
- Writing and validating Person, Organization or Article markup in depth → `schema-markup`.
- Google Business Profile, local reviews and NAP consistency → `local-seo-audit`; building an honest review programme on G2, Capterra, Trustpilot or app stores → `reviews-for-ai-answers`.

## What you need

### Required

- The URL or URLs to review, and the topic each covers.
- Who actually wrote each page and their real background. Ask; don't infer it from the byline.
- Who owns and runs the site: legal entity, country, and how to contact them.

### Helpful

- URLs of the About, Contact, author, editorial policy and (for shops) returns, shipping and terms pages.
- Search Console clicks by page across the dates of recent core updates.
- Review profiles: Google Business Profile, Trustpilot, G2, Capterra, app stores, BBB, marketplaces.
- How content is produced: AI use, editing, expert review, fact-checking and update routines.
- Affiliate, sponsorship and advertising arrangements.

### No tools?

Everything here works in a browser. Read the page and its linked author and About pages as a stranger would. Use view-source or the Rich Results Test to read Article, Person, Organization and ProfilePage markup. Search Google for `"Brand" reviews -site:example.com`, `"Brand" complaints`, `"Author Name" [topic]` and the brand on Reddit. Check the Wayback Machine (web.archive.org) for what the domain used to be. Google's Search Quality Rater Guidelines are a free public PDF; check the date on its cover page and use the latest version.

## Ground rules

- Be precise about what E-E-A-T is. It comes from Google's Search Quality Rater Guidelines, used by human raters whose ratings help Google evaluate its systems. Raters don't change rankings, and Google says E-E-A-T itself isn't a specific ranking factor. Its systems use many signals that line up with what raters look for.
- Trust is the centre. Experience, expertise and authoritativeness support it, and a page that isn't trustworthy rates poorly however expert it looks.
- The bar rises with the stakes. A YMYL page (health, money, safety, legal, civic) needs clearly qualified authors and accurate, sourced claims; a page about choosing a candle scent doesn't.
- Match the evidence to the claim. A product review needs proof the author used the product. A tax guide needs proof the author knows tax. A personal story about living with a condition needs the person's experience, not a doctor's byline stuck on top.
- Independent evidence beats self-description. Raters are told to research what others say about the site and its creators. Badges, "trusted by thousands" and stock headshots without proof count for little.
- Never invent people, credentials, reviewers or reviews. Google calls fabricated creator profiles deceptive. No byline is better than a fake one.
- AI-assisted content is fine when it is accurate, edited and genuinely useful. Disclose AI or automated production where a reader would reasonably wonder how the content was made.
- Markup describes trust; it doesn't create it. Person and Organization markup on a page with no real author or owner information changes nothing.
- A drop after a core update isn't proof of a trust problem. Google says core updates aren't penalties; look at what now outranks the page before blaming E-E-A-T (`seo-performance-audit`).
- Not every page needs a byline. Category pages, tools, calculators and product pages earn trust through accurate details, clear ownership and good service information. `Leave it` is often right there.

## Steps

1. **Classify the page.** Note its purpose (inform, sell, review, compare, tool, community), its YMYL level (none, some, high), and who it serves.
   - Is the purpose clear within a few seconds and does it help the reader? A page that exists mainly to rank or to push affiliate clicks is the first gap.
   - High YMYL raises every later check by one priority level.
2. **Check who wrote it.** A rater wants to know who is responsible for the content.
   - Visible byline with a real name, linked to an author page. Missing on YMYL or review content = `Fix now`; missing on a general blog post = `Fix next`.
   - The author page has a real name, photo, role, relevant qualifications or experience in plain words, other work by the author, and links to profiles elsewhere (LinkedIn, publications, professional registers).
   - For YMYL, a named reviewer with credentials and a review date ("Reviewed by [name], [credential], on [date]") only when that review really happened.
   - Red flags: the same generic bio on every author, AI-generated headshots, credentials that can't be found anywhere else, "Admin" or "Staff" bylines on advice content.
3. **Look for first-hand experience.** Most important for reviews, comparisons, tutorials and travel or service pages.
   - Original photos, screenshots or video of the author using the product or doing the task; test results with conditions; measurements; costs actually paid; timelines; specific annoyances only a user would notice.
   - Reviews say how products were tested and chosen, include real drawbacks, and show why the verdict differs between products. Google's own guidance on writing high-quality reviews asks for exactly this kind of evidence; use it as the checklist.
   - Red flags: only manufacturer images, specs copied from the brand site, no downsides anywhere, every product rated 4.5 or higher, "we tested" with no detail of how.
4. **Check accuracy, sources and dates.**
   - Statistics, medical, legal and financial claims link to primary sources (studies, regulators, official docs, original data), and the numbers match those sources.
   - YMYL advice agrees with expert consensus or says clearly where it doesn't and why. Disclaimers where a reader could be harmed by acting alone.
   - Published and updated dates are visible and match `datePublished` and `dateModified`. A date changed without a real content change is a trust problem; Google lists it among signs of content made for search engines first.
   - Affiliate and sponsorship disclosures sit near the top, before the first affiliate link, in plain words.
5. **Check purpose and presentation.**
   - Ads, pop-ups and interstitials don't cover or push down the main content. On mobile, the main content starts on the first screen.
   - The title and headings promise what the page delivers. No bait-and-switch.
   - Affiliate pages add something beyond the merchant's own description: testing, comparison, original photos. Pages that are mostly copied product text with affiliate links match Google's "thin affiliation" spam policy.
6. **Check who runs the site.**
   - About page names the real people and company behind the site, what they do and how long they've done it.
   - Contact details a customer can actually use: email, phone where expected, physical address for businesses, and an imprint where the law requires one (for example Germany and Austria).
   - Legal entity name and ownership are consistent across the footer, About page, terms, Organization markup and external profiles.
   - An editorial policy for content sites: how topics are chosen, who writes and reviews, how AI is used, how errors are corrected, how the site makes money. A corrections note on changed articles is a strong signal.
7. **For shops and services, check customer service information.** The rater guidelines single this out for shopping and other transaction pages.
   - Returns and refunds, shipping costs and times, warranty, payment methods, delivery areas and how to complain, all reachable from product and checkout pages.
   - Prices, taxes and fees shown before checkout. Secure checkout (HTTPS everywhere, recognisable payment providers).
   - Organization markup can carry `hasMerchantReturnPolicy` and `hasShippingService`; the visible pages matter more.
8. **Research reputation.** Look for what independent sources say about the business and its authors, not what the site says about itself.
   - Search `"Brand" reviews -site:example.com`, `"Brand" complaints`, `"Brand" scam`, `"Brand" reddit`, and each key author's name with the topic.
   - Check review platforms, BBB or local equivalents, news coverage, industry awards, Wikipedia (if any), and professional registers for licensed authors (medical, legal, financial).
   - Weigh volume, recency and pattern. A few bad reviews are normal; repeated unresolved complaints about the same issue, or fraud allegations, are a serious trust gap.
   - Quote what you found with URLs. Mark it `tool` or `seen`, never generalise from one review.
9. **Check the markup that describes all this.** It should mirror visible facts. Implementation → `schema-markup`.
   - Article or BlogPosting with `author` as a Person: only the name in `author.name` (no job title or "posted by"), plus `url` pointing to the author page. `datePublished` and `dateModified` in ISO 8601.
   - Author pages: ProfilePage with `mainEntity` Person (`name`, `image`, `description` for the credential, `sameAs` for real external profiles).
   - Home or About page: Organization with `name`, `url`, `logo`, `sameAs`, and `legalName`, `address` and `contactPoint` where real.
10. **Scan for spam-policy risks.** These outrank every other gap. Any confirmed one is `Fix now`; then check Search Console → Security & Manual actions → Manual actions.
    - Scaled content abuse: many pages generated mainly to rank, with little value for readers, whether by AI, templates or scraping. Signs: hundreds of near-identical pages, publishing bursts, swapped place or product names, no editing.
    - Site reputation abuse (Google's spam policies now title it the site reputation policy): third-party content such as coupons, casino, loans or sponsored "best of" pages hosted mainly to exploit the host site's ranking signals. Check subfolders and subdomains run by partners.
    - Expired domain abuse: a domain bought and repurposed mainly to exploit its old reputation. Compare the Wayback Machine history with today's content; a school or charity domain now selling supplements is the textbook case.
    - Fake reviews and testimonials: invented testimonials, paid or incentivised positive-only reviews, review gating, self-serving review stars. They break Google's review snippet guidelines and Business Profile policies. Fake reviews, and incentives that depend on the review being positive, are also illegal in the US (FTC rule, 2024), the UK (DMCC Act, in force April 2025) and the EU.
    - Fabricated authors or credentials, and thin affiliation pages (step 5).
11. **Prioritise like a rater.** Rank gaps by what a rater would notice first on this page, scaled by YMYL level. Anonymous YMYL advice, deceptive elements and spam risks come first; missing author photos and thin bios come later.

## What to hand back

Fill in this template. Every recommendation gets a priority label and an evidence label with confidence.

```markdown
# E-E-A-T and trust review: [URL or site], [date]

**What I found:** [one line, e.g. "Medication guide with no named author or reviewer on a site with no About page."]
**What matters most:** [one line]
**What to do first:** [one line]

## Page profile
- Purpose: [x]. YMYL level: [none / some / high]. Likely rater view: [Lowest / Low / Medium / High / Highest page quality]. This is a judgement against the rater guidelines, not a Google score.

## Trust gaps a quality rater would notice
1. [Fix now | Fix next | Worth doing] [gap, in plain English (term)] - what a rater sees: [observation] - fix: [specific change, who does it] - evidence: [seen | tool | inferred], [high | medium | low]

## Site-level gaps
- [About / contact / ownership / editorial policy / customer service / author pages]: [gap] → [fix] [priority] ([evidence])

## Reputation findings
- [source URL]: [what it says, quoted or summarised] - weight: [why it matters or doesn't]

## Spam-policy risks
- [policy]: [what was found, where] → [action] [Fix now] ([evidence]). Manual actions report: [checked: none / found: x / not checked]

## Leave it
- [thing that looks like a gap but isn't worth the time, and why]

## What I could not check
- [e.g. author credentials not verifiable online; ask the author for proof]
```

## Stop and flag if

- YMYL content has no qualified author or reviewer. Recommend it isn't published or promoted as-is until one reviews it.
- The user asks you to invent authors, credentials, reviewers, reviews, testimonials or "as seen in" logos. Refuse that part and explain why.
- A manual action is present, or the site shows clear scaled content, site reputation or expired domain abuse. That work comes before any trust polish.
- Reputation research turns up fraud allegations, lawsuits or regulator warnings. Report the facts with sources, without speculation, and let the user decide.
- Unacceptable output: calling E-E-A-T a ranking factor or a score, recommending markup in place of real information, or listing a gap without saying what the reader or rater actually sees.

## Next step

- Run `seo-content-brief` for pages that need first-hand evidence, sources or expert input added, with the trust gaps as requirements.
- Run `schema-markup` to implement Person, ProfilePage, Organization and Article markup that matches the fixed pages.
- Run `ai-brand-facts` if the reputation research showed that AI answers or the third-party sources they cite describe the brand wrongly, with each claim quoted and its URL; `ai-search-visibility` for a full AI citation baseline.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
