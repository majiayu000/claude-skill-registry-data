---
name: competitor-research
description: "Runs a competitor deep dive on a company or product and turns it into a claim-safe battlecard. Starts from the competitor's own sources (site, docs, pricing page, changelog, filings, job posts, app store listings), checks them against independent sources, and labels every claim VERIFIED, CORROBORATED, VENDOR-CLAIMED, INFERRED or UNKNOWN with a source and a date. Separates what they sell from what they actually deliver, pricing evidence from guesses, and real weaknesses from wishful ones, then writes what your team can say and must not say. Works with web search in Claude.ai or Claude Code. Use when someone says \"research my competitor\", \"competitor deep dive\", \"make a battlecard\", \"how does X compare to us\", \"what does X actually offer\", \"how do we position against X\" or \"what can we say about X\"."
---

# Competitor Research

Most competitor research is marketing copy with opinions on top, and a month later a prospect catches your rep repeating something untrue. This skill does the opposite: every claim has a label, a source and a date, and the battlecard only lets your team say what the evidence supports.

Example used throughout: you sell **Acme Scheduling** and want to know how to position against **Example CRM**, which just added a booking feature.

## What it does

Maps what the competitor sells today from their own sources, checks it against sources they do not control, separates what they sell from what customers actually get, records pricing evidence (never guesses), infers who they target (labelled), finds weaknesses you can use without overclaiming, and writes a battlecard: what we can say, what we must not say, and what to ask the prospect.

## What you need

- **The competitor's name and website.** If the name is common, also the product name or a URL so you research the right company.
- **Your own product in one or two lines**, and what decision this supports (a sales call, a pricing change, a launch, a board question).
- **Web search.** In Claude.ai, turn on web search. In Claude Code, the built-in web search and fetch tools work. Without live search, this skill can only organise what you paste in, and it must say so in the output.
- **Optional:** call notes, lost-deal reasons or a quote you received. Private: they inform the analysis but never appear in anything shared outside your team.

## Steps

### 1. Fix the scope and the date

Write down the research date, competitor, product in scope, your product and the decision. "Current" means checked live today. Memory and old summaries are not evidence: re-find it or label it UNKNOWN.

### 2. Map their official sources first

Before searching the wider web, work through the competitor's own surfaces: homepage and navigation, product pages (one per module), pricing page with its footnotes, docs and help center (they state limits marketing skips), changelog and launch posts, security and terms pages, integrations listings, case studies, careers page and job posts, app store listings, and public filings if they file any. The sitemap often reveals pages the navigation hides. Save the exact URL and the date for every page you use. See `references/source-guide.md` for what each source is good and bad at.

### 3. Build the product map

For every module, record: exact public name, the job it does, who uses it, who buys it, key integrations, availability (generally available, beta, early access, waitlist, announced, roadmap) and which plan includes it.

When a launch post says "early access" and a later product page presents it as standard, record both and mark plan entitlement as UNKNOWN. Docs that describe current behavior beat an older marketing overview, but keep the conflict visible.

### 4. Sold vs delivered

Product pages show the promise. Look for the delivery:

- **Docs and help articles:** limits, quotas, required add-ons, "contact sales to enable".
- **Job posts:** roles in onboarding, implementation, customer success or professional services suggest how much hand-holding the product needs. Many open roles on one feature suggest it is new or struggling. Treat this as INFERRED, never as fact.
- **Changelog:** how often features ship versus how long they stay "coming soon".
- **Reviews and community threads:** setup time, support quality, missing features. Look for patterns across several reviews, not single angry posts.

Keep separate questions separate: does the capability exist, which plan gets it, is it included or extra, and who does the setup.

### 5. Pricing: evidence, not guesses

Record only what you can point to: published list prices, plan names, what each plan includes, billing terms and footnotes. For anything not published ("contact sales", enterprise tiers, discounts), write UNKNOWN and add a question to ask instead. A price from a third-party estimate or a forum post is at most CORROBORATED if two independent sources agree, and the battlecard must not quote it as their price.

### 6. Corroborate independently

Look for sources the competitor does not control: independent news, customer announcements on the customer's own site, review sites, customer conference talks, independent benchmarks. Classify by who wrote it, not where it is hosted: a vendor press release republished on a news site is still the vendor talking.

Never apply a benchmark of a different product to this competitor.

### 7. Infer the target customer

From case studies, pricing tiers, job posts, integrations and messaging, infer company size, industry, buyer role and trigger moment. Label it INFERRED and cite the evidence.

### 8. Find weaknesses you can use

A usable weakness has evidence and matters to your buyer. Write the weakness, its evidence and label, why the buyer cares, and a fair way to raise it (usually a question the prospect can test). Also write where they are genuinely stronger. A battlecard that admits strengths gets trusted.

"Not found in public sources" is not the same as "they don't have it." Say "we could not find X documented publicly", never "they can't do X".

### 9. Write the battlecard and evidence log

Fill `templates/EVIDENCE-LOG.md` as you go, then `templates/BATTLECARD.md` from it. Every battlecard line cites an evidence ID.

## Evidence rules

Every claim gets exactly one label, a source and a date checked.

| Label | Meaning | Can go in "we can say"? |
|---|---|---|
| **VERIFIED** | The competitor's own current source states it directly (product page, docs, pricing page, filing). Verified means they say it, not that it is true in practice. | Yes, phrased as "their site says..." |
| **CORROBORATED** | Two or more independent sources agree, or an independent source confirms a vendor claim. | Yes, with care |
| **VENDOR-CLAIMED** | Performance, scale, ROI or customer results published by the competitor or in a vendor-hosted case study. | Only as "they claim..." |
| **INFERRED** | Your reasoning from evidence. Show the reasoning. | No. Use it to shape questions. |
| **UNKNOWN** | Not established publicly, or sources conflict. | No. Turn it into a question. |

More rules:

- Material claims need a direct URL, not a homepage, and a date checked. Pages change.
- When sources conflict, record both with dates. Do not pick the convenient one.
- A blocked or login-walled page is an access limit, not evidence the feature is missing.
- Customer logos prove a relationship existed at some point, not that the customer uses the product you are comparing today.
- Selected power users are not average users. Task-level time savings are not company-wide ROI. Keep the claim's own scope.
- Never invent numbers. If a figure is not in a source, it is UNKNOWN.

## Output

Three files in the working folder (Claude Code) or three sections in the reply (Claude.ai):

1. **Evidence log** (`evidence-log-<competitor>.md` from `templates/EVIDENCE-LOG.md`): every claim with ID, label, source, date and a one-line note.
2. **Battlecard** (`battlecard-<competitor>.md` from `templates/BATTLECARD.md`): one page a sales or marketing person can use on a call.
3. **Short summary** in the reply, five to eight lines: biggest overlap, strongest honest differentiator, biggest unknown, and any claim the team must stop making.

Before delivering, check: every battlecard line traces to an evidence ID; nothing INFERRED or UNKNOWN sits in "we can say"; no unpublished price is stated as fact; every "they can't" has become "we could not find"; their strengths section is not empty.

## Honest limits

- Public sources show what a company says and ships. Private pricing, contracts, roadmap and real customer outcomes are mostly invisible.
- Reviews skew to the extremes; job posts show intent, not what every customer gets.
- If a key page could not be loaded, the report says so instead of filling the gap.
- Not legal advice. Public claims about a named competitor can carry legal risk; get external copy checked.
- No logging in under false pretences, scraping behind logins, or using confidential material someone should not have shared.
