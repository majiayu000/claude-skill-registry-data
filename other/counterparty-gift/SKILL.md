---
name: counterparty-gift
description: Build a local business a list of its NEXT CUSTOMERS from public records (building permits, wrecking permits, business closings), host it on a private-link page with a CSV, and draft the email that hands it over. Use when you say "build something for <business>", "can we make them something free", "what could we give them", "find businesses we could help", "build 5 more and send them", "no strings attached", or want a lead-list product per trade. The gift is the other side of their deal — not advice, not an audit.
---

# A list of their next customers

**The gift is the other side of their deal.** Not advice, not an audit, not a fix to their
website: a map and spreadsheet of the specific addresses where their next job is about to
exist, derived from records a city publishes before the job does. **Swap test:** swap in another
business's name and the page must stop making sense.

**Done** = a live page at `/for/<8-hex>/` with a CSV beside it, an email drafted (sent only on an
explicit go), and a ledger row.

## 1. Find the business

- **Marketplace service posts** (e.g. Craigslist services / business-for-sale sections) are rich:
  a business that posts has written down, in its own words, who it wants as a customer, and that
  line becomes your opening quote (see `distribution-channel` rule 11).
- **A local business dataset** (e.g. Overture places, filtered to independents with a website)
  works for sweeps. Never call a site vacant from a dataset alone.
- **Pick by counterparty, not by sector.** Keep a business only if you can name the public record
  where its buyer appears *first*. Fits that worked with a city permit register (see
  `mpls-permits` for one such register's traps):

| business type | their next customer in the record |
|---|---|
| arborist | residential dig/build permits (construction compaction damages trees) |
| commercial cleaner | commercial build-outs at final inspection (post-construction clean) |
| architectural salvage | open wrecking permits + year built; wrecking contractor named |
| sign painter | street-level storefront build-outs |
| store fixtures | retail and dispensary fit-outs |
| restaurant equipment (new + used) | new kitchens (buyers) and kitchen remodels (sellers) |
| landscaper | residential work that just reached final inspection |
| restaurant bookkeeper | restaurant/bar/cafe build-outs by stage (final inspection = about to open a set of books) |
| used-equipment reseller | commercial wrecking permits + state WARN closure notices with a site |

- **Reject**: vendors who sell what you build, chains/franchises, and businesses with no
  counterparty that only your data finds.
- **Verify before building**: fetch their live site, find a real email on THEIR domain (not a
  guessed pattern), and read what they actually sell (a cleaner listing "post-construction
  cleanup", an equipment dealer that also *buys* used gear — both change the list).

## 2. Build the list

- **Every number on the page and in the email is computed from the rows**, printed by the render
  script, and pasted from that output. A typed number is a false fact.
- **Drop anything you parsed that you can't verify.** Business names regex'd out of free-text
  permit comments come back as junk ("Levels", "ACW"); show the raw description instead.
- **Leave out homeowner names** and individual applicants. Show a builder only when the name reads
  as a company.
- Page shape that works: one H1 with the count in their words, a lede quoting what THEY sell, three
  stats, an SVG dot map (no tile servers), filter chips, sorts including "closest to you" from their
  geocoded address (the Census geocoder is free), a CSV download, a note on the source and what's
  excluded, and "Free. Nothing to sign up for."

## 3. Host it

- A private chat artifact can't be the gift: the recipient can't open it. Host it on your own site
  at `/for/<secrets.token_hex(4)>/index.html` plus the CSV.
- Add `<meta name="robots" content="noindex">` and your analytics tag, plus a persistent
  per-browser id (e.g. PostHog) if you need to tell one reader opening it four times from four
  readers; daily-rotating visitor hashes can't.
- Verify live: poll until the title serves, then `curl -w %{http_code}` every page and CSV (a CSV can
  404 for a minute on deploy lag).

## 4. The email

~120 words: the subject is the count in their terms ("42 buildings about to come down near you");
line 1 quotes what they sell or said; "So I pulled..."; three real numbers; one named example near
them; the link; what it does; "It's free, no strings attached." Sign with a real name and a way to
check who you are. **Draft only; a human sends.** Plain text.

## 5. Log it

A ledger row: date, business, to, page, list size. Replies go in verbatim (see `business-inbox`).

## Open questions to read honestly

Whether anyone replies, and whether a paid follow-on exists. Read the ledger before claiming the
mechanism works; fewer than ~50 sends is a probe. A variant that worked as a product: the same lists
sold per segment for a small fixed price, with a free slice (see `product-paywall`).
