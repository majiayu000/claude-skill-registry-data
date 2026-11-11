---
name: business-audit
description: "Researches everything public about a business with web search (directory and map listings, reviews, mentions, competitors) and returns a prioritised fix list: wrong or duplicate listings, unclaimed profiles, unanswered bad reviews, gaps against competitors. Then drafts review replies and listing correction requests for the owner to post. Use when someone says find everything the internet says about my business, audit my online presence, check my listings, what do people say about us, or why do competitors show up before me. Works in Claude.ai with web search and in Claude Code. Drafts only, never posts."
---

# Business Audit: what the internet says about you

Customers often meet your business on a map listing, a directory or a review site before they see your website. This skill finds those pages, checks what each one says against the truth, and hands back a short list of fixes in priority order, plus drafted replies and correction requests.

By Johann (@johannships). This is the skill from my "I asked Claude to find everything the internet says about my business" reel.

## Turn on web search

- **Claude.ai (web, desktop, mobile):** click **+** in the lower left of the chat box and switch on **Web search**. If you have the new Claude experience there is no toggle: Claude searches the web when it helps. On Team and Enterprise plans an owner has to enable web search first in Organization settings > Capabilities. Source: [support.claude.com "Enabling and using web search"](https://support.claude.com/en/articles/10684626-enabling-and-using-web-search).
- **Claude Code:** web search and web fetch are built in. Approve them when asked.

If Claude cannot search in this chat, say so and stop. Do not audit from memory.

## Inputs (ask once, accept "skip")

1. Business name, and any old or other names it has traded under.
2. Address (or service area), phone number, website, opening hours: the **true** current versions. Everything found is checked against these.
3. Category (for example "dentist", "roofing contractor", "online bookkeeping").
4. Social profiles you run.
5. Up to three competitors, or "find them for me".
6. Anything you already know is wrong.

## Steps

### 1. Find every listing and mention

Search the business name with the city, the phone number on its own, the address on its own, and the old names. Check at least:

- Google Business Profile / Google Maps, Apple Maps, Bing Places
- Yelp, Facebook, Instagram, LinkedIn, TikTok, YouTube
- Industry directories for the category and country (for example Houzz, Healthgrades, TripAdvisor, Avvo, Clutch, Trustpilot, Better Business Bureau, Yellow Pages, local chamber of commerce)
- News, blogs, forums and Reddit threads that mention the business
- Listings for the same phone number or address under a different name (often an old owner or a duplicate)

For each result record: site, URL, name shown, address, phone, website link, hours, rating and review count if shown, date checked. Some sites block automated reading (Google Maps and Yelp often do). If a page cannot be opened, write `could not open, check by hand` and keep the URL. Never fill in a field you did not see.

### 2. Check each one against the truth

Mark each field: matches / wrong / missing. Flag:
- **Wrong details**: name, address, phone, hours, website, category.
- **Duplicates**: two listings for one business on the same site.
- **Unclaimed or someone else's**: listings the owner does not control, including ones an old owner, agency or directory created.
- **Closed or moved** shown for a business that is open.

### 3. Read the reviews

For the sites with reviews: overall rating and count, the three most common praises, the three most common complaints (quote short phrases with the URL), negative reviews with no reply from the owner, and anything that looks like it may break the site's review rules. Do not judge whether a review is fake; say what makes it look odd and let the owner decide.

### 4. Compare with competitors

For each competitor, on the two or three sites that matter most for this category: rating, review count, how complete the profile is (photos, hours, services, posts), and anything they show that this business does not. List gaps, not opinions.

### 5. Prioritise

Score each fix by **impact** (how many customers see that page, how badly it misleads them) and **effort**. Order:

- **P1, fix this week:** wrong phone, address or hours on a big listing; listing showing closed; duplicates on Google or Apple Maps; unanswered one- and two-star reviews from the last 90 days.
- **P2, this month:** unclaimed profiles to claim, wrong details on smaller directories, missing categories or services, gaps against competitors.
- **P3, when you can:** old mentions, minor directories, nice-to-haves.

### 6. Draft the fixes (owner posts them)

- **Review replies:** under 80 words, thank them, address the specific point, no excuses, no private details about the customer, offer a way to talk offline. Never offer anything in exchange for changing a review.
- **Correction requests:** for each wrong listing, the exact field, the wrong value, the right value, and how that site handles it. For Google: claim the profile, or use [Request ownership](https://support.google.com/business/answer/4566671) if someone else owns it, and [report wrong details on Maps](https://support.google.com/maps/answer/3094088) for details. For other sites, find their own claim or correction page and link it; do not guess the process.
- **Missing listings:** which ones to create, in order.

## Output

Use `templates/AUDIT.md`:

1. Three-line summary: listings found, how many have wrong details, the single most urgent fix.
2. Listings table with every field marked.
3. Reviews summary per site.
4. Competitor gaps.
5. Fix list: P1, P2, P3, each with the URL and the exact change.
6. Drafts: review replies (R1, R2...) and correction requests (C1, C2...).
7. What could not be checked, and how to check it by hand.
8. "Nothing has been posted or submitted."

## Rules

- Every finding has a URL and the date it was checked.
- "Not found" means not found in this search, not "does not exist".
- Never post, reply, claim, report or submit anything. The owner does that.
- Never write or suggest fake reviews, review swaps or paid reviews.
- Keep customer names out of the summary; quote review text only where it is needed for the reply.

## A prompt you can paste without installing the skill

```
Search the web for everything public about my business: [name], [address or service area], [phone], [website], category [category].
Check Google Maps, Apple Maps, Bing Places, Yelp, Facebook, the main directories for my industry and country, and any news, forum or Reddit mentions.
For each listing give the URL and what it shows for name, address, phone, hours and website, and flag anything that does not match the details above.
Flag duplicates and listings I may not control.
Summarise the reviews: common praise, common complaints, and bad reviews with no reply.
Compare me with [competitors, or "my top 3 local competitors"].
Finish with a fix list in priority order, then draft replies to the unanswered bad reviews and correction requests for the wrong listings.
If you cannot open a page, say so. Do not guess any detail.
```
