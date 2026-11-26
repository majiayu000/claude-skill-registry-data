---
name: sponsored-placement-vetting
description: Vet a sponsored post, guest post, syndication or press release before you pay or publish, the parasite SEO safety check. Use for "is this guest post safe", "should we buy this sponsored post", "syndicate our blog" or "press release links". Checks Google's site reputation and link spam rules, disclosure and canonicals, then gives a go or no-go.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/sponsored-placement-vetting
---

# Vet a sponsored or guest placement before you pay

Checks a paid or third-party placement before money changes hands or the piece goes live: a sponsored article or advertorial, a guest post, a link insertion, a syndication deal, a press release, or a "contributor" slot on someone else's site. It tests whether the host genuinely runs that section, what Google's site reputation and link spam policies say about this exact deal, how the links, canonical and disclosure must be set up, and whether the content is aimed at readers or at rankings and AI answers. You hand back a go, go-with-changes or no-go verdict per placement, with the setup to write into the agreement.

> **Romeo's rule:** Pay for a host's readers, never for its rankings; Google wrote a whole policy about people who pay for the second.

## Use this when

- Someone offers a "sponsored post", "guest post with a dofollow link", "link insertion" or "contributor" spot on another site, and you want to know whether it's safe and worth the price.
- A publication or partner wants to republish (syndicate) your articles, or you want to republish theirs.
- You're about to send a press release through a wire service and want the links and content set up properly.
- An agency's parasite SEO proposal includes paid placements on news sites, universities or other high-authority domains.
- You're the host: someone wants to pay to publish on your site, or your site already runs a sponsored, coupon or partner section.
- A placement you bought stopped ranking, or the host received a site reputation manual action.

## Don't use this for

- Choosing which platforms (LinkedIn, Reddit, YouTube, Medium) to publish on under your own name, per query group → `parasite-seo-plan`.
- Reviewing the whole link profile, "toxic link" worries or a disavow decision → `backlink-profile-review`.
- Earning a fair place on third-party "best X" lists that AI answers cite → `best-of-list-inclusion`.
- Writing the guest article or press release itself → `seo-content-brief`, then `seo-blog-writer`.

## What you need

### Required
- The offer exactly as sent: host URL, the section or page where it will run, price, what's included ("dofollow", "permanent", "no sponsored tag", number of links), and any contract text.
- The content: the draft, the release, or the article to be syndicated, plus the links and anchor text you want in it.
- Your honest goal: readers and referral visits, brand awareness, being cited in AI answers, or links for rankings. The last one decides a lot.
- Which markets the placement should reach, especially whether the searchers are in the European Economic Area (EEA). Google enforces the site reputation policy differently for searchers there, and advertising rules differ by country.

### Helpful
- The URL of the host section, and 5 to 10 existing posts in it, sponsored and editorial.
- The host's rate card, media kit, "write for us" page, or the marketplace listing that sells the slot.
- Traffic or link estimates for the host from a third-party tool (Ahrefs, Semrush, Similarweb), labelled as vendor estimates.
- For syndication: the original URL and publish date, and the partner's proposed URL. For press releases: the wire service and one of its past releases.
- Your `ai-search-visibility` source map, if AI citations are the goal: it shows whether this host is actually cited for your prompts.

### No tools?
Everything here works in a browser. Open the host section and view-source on 3 existing sponsored or guest posts: search for `rel=` on outbound links, `<link rel="canonical"`, `noindex`, the byline and the disclosure label. Search Google for `site:host.com/section/` to see how big the section is, and paste a distinctive sentence from each post in quotes to find copies elsewhere. Check whether the host's own navigation and homepage link to the section. Read the host's "write for us" or advertising page and, if the offer came through a marketplace, its listing.

## Ground rules

- Third-party content isn't the problem; hosting it mainly to borrow the host's ranking signals is. Google's site reputation policy (spam policies page) judges how integrated the content is: presentation, quality next to the rest of the site, real authorship, and whether the same content appears elsewhere. No single factor decides it.
- The host gets the penalty and you lose the money. Outside the EEA, Google can give the host's section a manual action and your piece stops ranking with it. From 30 August 2026, in the EEA, such manual actions no longer affect results there; Google may instead separate the section so it ranks on its own merits (Search Central blog, 28 August 2026). Either way, the borrowed authority you paid for is gone.
- Any link given in return for something of value (money, free product, a service, a swap) carries `rel="sponsored"` or `rel="nofollow"`. "Dofollow guaranteed", "no sponsored tag" and contracts that require a followed link are all on Google's link spam list. Expect visitors and brand searches from a placement, never link equity.
- Anchors are your brand, product name or plain URL. Keyword-rich anchors in articles, guest posts or press releases distributed on other sites are a named link spam example.
- Readers must know it's paid before they read it. In the US, the FTC's Endorsement Guides (revised 2023) require clear disclosure of material connections, and its native advertising guidance holds everyone who helps create or present the ad responsible, the advertiser included.
- One original piece per host. The same article on many sites matches Google's own violating example (sponsored reviews the author also distributes elsewhere) and, at volume, scaled content abuse.
- Don't try to buy your way into AI answers. Google's spam policies now count "attempting to manipulate generative AI responses in Google Search" as spam. Rented pages that plant self-ranking lists or claims for AI tools to repeat are the target; honest, labelled content written for the host's readers isn't.
- Judge a host by its readers, not its metrics. Domain Rating and Authority Score are vendor estimates; a section that exists only to sell posts has no readers whatever its score.
- Read-only. This skill never pays, signs, publishes or emails a host. Draft the reply and the terms; the user sends them.

## Steps

1. **Classify the deal.** Write down what is being bought, who writes it, who publishes it, and what changes hands.
   - Types: sponsored article or advertorial (you pay, host publishes), guest post (you write, host publishes, with or without payment), link insertion (a link added to an old article), syndication (an existing article republished elsewhere), press release (wire distribution), contributor account (you publish directly on a publisher's platform), section rental (a third party runs part of the host's site).
   - Anything of value counts: money, a free product or account, a discount, a link swap, a reciprocal post. That decides the link and disclosure rules below.
   - Link insertions and section rentals start at no-go. An insertion is a paid link with an old date on it; a rented section is what the site reputation policy describes.
2. **Check that the host genuinely oversees the section.** Read 5 to 10 existing posts in the same section, not the host's best editorial work. Mark each test pass, unclear or fail, with the URL you looked at.
   - Real author: a named person with a bio or author page. "Staff", "Admin", "Guest Author" or no byline at all is a fail; Google's CBD example is an unauthored affiliate article.
   - Real editing: an editorial policy, a named editor or "edited by" line, a corrections route, the host's house style and headlines. Copy that reads like the advertiser's own sales page is a fail.
   - Integrated: the section sits in the host's navigation and categories, uses the same template, links to and from the host's own articles, and covers the host's topics. A subfolder or subdomain with its own design, no internal links in, and topics the host never covers is a fail.
   - Original: paste one distinctive sentence from each of 3 posts in quotes into Google. The same text on other sites is a fail.
   - Quality: would the host's own editors have published this? Google's example of a low-quality "best casinos" page on a medical site is the benchmark for no.
   - Two or more fails = no-go. All passes with labelled links and disclosure = the section looks like Google's "not likely to act" examples (an integrated, disclosed coupon section with named editorial responsibility; an authored, original freelance article under the host's editorial standards).
3. **Scan for red flags.** Each one you find is `seen` or `tool`, with the URL.
   - Topic mismatch: coupon, casino, betting, CBD, payday loan, crypto, essay-writing or "best X" sections on a host about something else (news, education, health, a university, a local paper). A coupon section can pass step 2; most rented ones don't.
   - Volume: count posts in the section over the last 30 days from its archive or dated `site:` results. Several sponsored posts a week on unrelated topics means the section is a link shop with a famous name.
   - Mass marketplaces: the offer came from a guest-post marketplace or a "publisher list" spreadsheet with hundreds of sites priced by metrics, with "dofollow", "permanent" and "indexed" columns. Those slots are sold to anyone, and so is the pattern.
   - Offer wording: "dofollow", "no sponsored tag", "no disclosure", "permanent link", "guaranteed indexing", "DA 90 news site", "gets you into ChatGPT". Each one is a fail on its own.
   - Already hit: the section has few or no results in `site:` searches, or a vendor tool shows its visibility collapsing. Don't buy into a section Google may have already acted on.
   - Open contributor platforms: Google's guidance for user-content platforms suggests noindexing posts from new users without an established reputation, so a fresh account's posts may never be indexed. Search the titles of a few recent contributor posts to see.
4. **Set up the links.** View-source on 3 existing paid or guest posts to see what the host really does, then specify yours.
   - Paid, gifted or swapped: every link to you carries `rel="sponsored"` (or `nofollow`). Affiliate links too. If the host refuses to qualify links on a paid deal: no-go.
   - Anchors: brand, product name or naked URL. One or two links, going where a reader would naturally go next, not a stack of money pages.
   - Unpaid editorial guest article: a brand link in the author bio is normal. If the real purpose of the post is the link, or you are doing this at scale, qualify the links anyway.
   - Links you can't see in the draft (added later by the host, in images, in widgets) are part of the deal: ask.
5. **Check the content.**
   - Written for the host's readers: on the section's topic, useful without clicking anything, still worth reading if the brand mention were cut.
   - Unique to this host, unless it's syndication handled as in step 6. A spun copy of your blog post is still a copy.
   - Authored by a real, named person from your side with an accurate bio. No invented experts or reviewers.
   - Claims factual and sourced; no "best", "number one" or comparative claims about yourself without evidence; no hidden text or lines addressed to AI assistants.
   - Regulated topics (gambling, CBD, alcohol, finance, health, legal) carry extra advertising rules: legal review before anything is paid or published.
6. **Syndication: decide which copy should rank.**
   - Your article on a partner site: publish on your own site first. Ask the partner to `noindex` its copy; Google's canonicalization guide says blocking indexing is the most effective fix and that a cross-domain canonical isn't recommended for avoiding syndication duplication. At minimum, the partner copy carries `<link rel="canonical" href="[your original URL]">` and a visible "This article first appeared on [linked title]" line near the top.
   - Without either, Google may rank the partner's copy instead of yours. Check 2 to 4 weeks after it goes live by searching a distinctive sentence in quotes.
   - Their article on your site: the reverse setup, labelled as republished, and only when it fits your section; hosting lots of unrelated syndicated content puts you on the host side of the site reputation policy.
   - Platform cross-posting (Medium's import, LinkedIn) is platform choice → `parasite-seo-plan`.
7. **Press releases.**
   - Newsworthy: a real event a journalist could write about (launch, funding, original data, partnership, key hire). "We published a guide" isn't news; skip the release.
   - Links: `nofollow` or `sponsored` on every link, brand or URL anchors, two or three at most. Many wire services add `nofollow` already; confirm in the source of one of their past releases.
   - Wire services aren't site reputation violations, but hundreds of syndicated copies build no rankings. The value is the journalists who write their own story from it.
   - Never use releases as a link-building or AI-seeding channel: a release written so AI tools repeat a claim is still a release written to manipulate.
8. **Disclosure.**
   - Label paid content where readers look first: "Advertisement", "Paid Advertisement" or "Sponsored Advertising Content" in front of or above the headline. The FTC calls "Promoted" at best ambiguous, and "Sponsored by [brand]" can read as funding without involvement.
   - Bylines state the connection: "Jane Doe is the founder of Acme". Free products, payments or discounts in exchange for coverage are material connections too.
   - EU and UK consumer law ban paid editorial content that isn't clearly identified as advertising; national press codes add rules. Not legal advice: check local rules for the host's market.
9. **Account for the EEA difference.** Note which markets the placement is meant to reach; enforcement follows where the searcher is.
   - Searchers outside the EEA: a manual action on the host's section can demote or remove it from their results. The host can fix it and request reconsideration; your money doesn't come back.
   - In the EEA since 30 August 2026: no manual action effect for EEA users; the section may be separated and ranked on its own merits, and eligible sites can use mediation.
   - A seller saying placements are "safe in Europe" is selling a misunderstanding. The policy still applies; only the enforcement differs, and neither route lets the placement keep the host's authority.
10. **Value it honestly.** Price the placement against what you can measure.
   - Readers: ask for the section's own traffic, newsletter or social numbers and label them host-supplied. No numbers offered for a sponsored section is a signal.
   - AI citations: is this host actually cited for your money prompts in your source map? If an engine cites the host's editorial pages, earning coverage there beats renting an unrelated corner of it (`inferred`).
   - Measurement plan: UTM-tagged links, referral visits, branded search in Search Console, and whether the placement URL ranks or gets cited. Never link equity.
11. **Write the verdict and the setup.** Go, go with changes, or no-go per placement, with the exact terms.
   - Contract terms worth asking for: links qualified with `sponsored` or `nofollow`; disclosure label above the headline; the host keeps editorial control and may edit; content unique to this host; no resale or republishing without a canonical to the original; removal or refund if the section receives a manual action.
   - You're the host: run steps 2 to 4 on your own section. Integrate it, edit it, label it, qualify every paid link, cap the volume and keep it on your topics. If it can't meet that, stop selling it and `noindex` or remove what's there.

## What to hand back

One report per placement (or one row per placement when vetting a list). Every recommendation gets a priority label and an evidence label with confidence.

```markdown
# Placement check: [host / section], [date]

**What I found:** [one line, e.g. "Sponsored section on a news site, unrelated topics, 38 posts in 30 days, followed paid links."]
**What matters most:** [one line, e.g. "It matches Google's site reputation examples; the section is likely to lose its rankings."]
**What to do first:** [one line: go, go with changes, or no-go, and the single change that matters]

## Verdict
- Placement: [URL or offer] | type: [sponsored / guest / insertion / syndication / press release / contributor / section rental]
- Verdict: [Go | Go with changes | No-go] - because: [two or three reasons] - evidence: [seen | tool | inferred], [high | medium | low]

## Host oversight (site reputation policy)
- Real author: [pass / unclear / fail] - [what you saw, URL]
- Editing: [pass / unclear / fail] - [...]
- Integrated into the site's sections: [pass / unclear / fail] - [...]
- Unique to this host: [pass / unclear / fail] - [...]
- Quality next to the main site: [pass / unclear / fail] - [...]

## Red flags
- [flag]: [evidence, URL] ([seen | tool], [high | medium | low])

## Required setup (write into the agreement)
- Links: [n], `rel="sponsored"` [or `nofollow`], anchors: [brand / URL], targets: [URLs with UTM tags]
- Indexing: [n/a | partner copy `noindex` | canonical to [original URL] + visible "first appeared on" link]
- Disclosure: "[label]" above the headline; byline "[name], [role] at [company]"
- Content: original to this host, written for its readers, no claims aimed at AI tools[, legal review because regulated]
- Terms: host keeps editorial control; no resale without canonical; [removal or refund if the section gets a manual action]

## Fixes, in order
1. [Fix now | Fix next | Worth doing | Leave it] [change] - why: [reason] - evidence: [seen | tool | inferred], [high | medium | low]

## How we'll measure it
- [referral visits via UTM / branded search / placement URL ranking or cited]; check on [date]

## What I could not check
- [item]: [why, and what would verify it]
```

## Stop and flag if

- The offer promises followed links, no disclosure, "permanent" links, guaranteed rankings or guaranteed AI mentions. Give the no-go and say which policy it breaks.
- The plan is volume: many placements a month from a marketplace list, link insertions, or the same article across many sites. That's a link scheme or scaled content abuse; stop and route the goal to `parasite-seo-plan`.
- The host already shows signs of a manual action or a rented section, or the user is the host and the section fails step 2. Raise it before anything else.
- The product is regulated (gambling, CBD, alcohol, finance, health). Recommend legal review before any paid content.
- A step would pay, sign, publish or contact the host. Draft it and get explicit permission for that specific action.
- Unacceptable output: invented traffic or authority numbers, a "go" on a paid link without `sponsored` or `nofollow`, a verdict based on a vendor metric alone, or any promise of link equity, rankings or AI citations.

## Next step

- Run `parasite-seo-plan` when the placement fails, to find platforms where you can publish under your own named profile instead.
- Run `backlink-profile-review` if earlier paid placements left followed links or keyword anchors pointing at the site, with the list of placements and dates.
- Run `best-of-list-inclusion` when the real goal was a place on the lists AI answers cite, with the host URLs from your source map.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
