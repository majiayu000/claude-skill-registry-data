---
name: spec-site-sale
description: Build a working website for a local business that didn't ask for one — their name, address and hours already on it — and pitch it to the owner, with the honesty guards that keep agency spec-work from passing as their real site. Covers picking a region, building the prospect table from JSON-LD rather than regex, scanning current sites with medians (a single sample was wrong by 13x), per-prospect re-skins with a measured side-by-side, verifying every link by opening it, a short email, a send ledger and pricing by city. Use for "build them a site and sell it", "take the site pitch to another city", or any spec build pitched to an owner. A human sends.
---

# Selling a website nobody asked for

**The bar: the owner opens a link and sees their own shop, already built.** Not a mockup, not a
portfolio, not a proposal: a working site with their name, address and hours on it. That is the
whole pitch.

## Step 0: the honesty guard, before anything renders

Publishing pages that carry a real company's name without permission is legitimate spec-work
**only** while it cannot be mistaken for their real site. Every skin ships with:

- a persistent visible line: *"Independent concept by <you>. Not affiliated with <them>."*
- `<meta name="robots" content="noindex,nofollow">` **and** a robots.txt disallowing everything
- demo inventory labelled as demo data
- their colours and type *referenced*, **never their logo reproduced as if licensed** (a clearly
  marked placeholder wordmark with their real name)

A concept mistaken for the real store kills the deal and invites a trademark complaint. Never take
payments, collect customer data or accept orders on a concept site.

## Step 1: pick the region by the city, not the postcode

Most postcodes hold one business of a type, so there is nobody to compare against. A city is a real
set. Rank candidate cities by **businesses with a reachable site AND a contact email**, not raw count.

## Step 2: build the prospect table from structured data

1. Walk a directory that republishes the licence or listing data; cache every detail page to disk.
2. Parse the page's **JSON-LD `LocalBusiness` block**, not a regex over rendered text: name, street,
   city, postcode, lat/lon, phone, rating, review count, and their own site from `sameAs`. (A regex
   pass once returned addresses for 0 of 16 pages that carried a complete `PostalAddress` all along.)
3. Re-parse from cache; never re-fetch.

Official registries are often bot-walled (a captcha served with a 200). A third-party republisher of
the same data is usually reachable; respect each site's terms.

## Step 3: scan every prospect's current site, with medians

On a **phone user-agent**, measure load time, page weight, viewport tag, JSON-LD count, iframes, and
platform. **Sample at least three times and take the median.** This is the rule that matters most:
one single sample said 12.1 seconds; the median of three was 474ms. Every "your site is slow" lead
built from single samples was an artifact. The pitch is literally "I measured your site", and the
owner can check it in one tap; wrong by 13x in the first sentence inverts the email. If samples
disagree by more than 2x, the metric isn't assertable: say something else.

## Step 4: re-skin per prospect

One script reads a prospect row and emits a brand file; the site builds per slug at `/demo/<slug>`
with their name, address, hours, and two colours from their current site. Put a **measured
side-by-side** on their page (their load time vs yours, their structured-data count vs yours), every
cell driven off the scan. **A slug with no skin falls back to the generic demo, never to another
prospect's page**; pin that with a test. Showing a shop their competitor's site is unrecoverable.

## Step 5: verify every link by opening it

A URL inferred from a repo name or a config file is a guess (one shipped CTA pointed at a stranger's
template on someone else's hosting, "confirmed" by a 200). Fetch each link **out of the shipped
artefact**, read the title and body, confirm it's yours. Better: make a bare URL unable to render;
require `{url, expect, title, verifiedAt}` written by a script that fetches and refuses on mismatch.

## Step 6: the email

Subject: `<your name> / <their company>`. Body, short:

1. **One measured fact about their site**, stated flat. If their site is genuinely fine, say so and
   pivot ("Your site loads fine. The problem is what happens after someone lands on it.").
2. "I built you a new one. It's live now, with your name, address and hours on it:" + their URL.
3. One paragraph on what it does for them.
4. The price, alone on a line.
5. The opt-out: "If this isn't for you, reply no and I'll drop you from the list." Honour it the same
   day.

**Never assert a fact verified for one prospect about all of them.** Where the address obviously
isn't the owner (a law firm, an unrelated domain), say so and ask to be pointed to the right person.

## Step 7: the ledger, before sending

One row per recipient: token, slug, organisation, email, drafted, sent, message id, reply kind, reply
date, note. Record each send **immediately**. Keep contact data out of git.

## Step 8: send (a human's decision)

- Cap around 40 a day from a personal mailbox and stop the moment it throttles; providers refuse (not
  queue) after "unusual activity", and can block the whole mailbox. A transactional sender is safer.
- Check the spam folder for the provider's own block notice.
- Verify against the Sent folder, not an API 200.
- Count bounces before each new batch; at 5% or more, stop.

## Pricing

**Hold one price within a city; vary it across cities.** n=14 can't measure price sensitivity, and
every shop in one young local market talks to the others: two owners finding different prices for
the same thing is a credibility problem you can't unwind.

## Refuse

Any fabricated bid, review, testimonial or record attributed to a real company (e.g. a fake opening
bid credited to a competitor to drive an auction). That is shill bidding. Decline in one sentence,
offer the honest substitute ("your competitor has genuinely been sent a build"), and keep building.

## Known limits

The build, scan and send are proven; whether the offer sells is not, and the first batch got no
replies. Measure yours.
