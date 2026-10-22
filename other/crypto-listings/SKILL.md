---
name: crypto-listings
description: Retrieve new cryptocurrency listings from the past 7 days and upcoming listings in the next 7 days across major exchanges. Always trigger immediately when the user's message starts with "cl" or says "crypto listings", "new crypto", "new coins", "upcoming listings", or asks what cryptos just launched or are launching soon. Always verify current listings data before responding; never answer from memory.
version: 1.1.0
---

# Crypto Listings

## Intent

Summarize recent and upcoming crypto exchange listings with clear source freshness and practical risk framing.

## Do Not Use When

- Do not use for investment advice, price predictions, unverified rumors, or stale listing data.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

Retrieve and format new and upcoming cryptocurrency listings across major exchanges. This skill covers coins listed in the last 7 days and coins officially scheduled to list in the next 7 days.

## Trigger When

- The user starts with `cl`
- The user asks for crypto listings, new coins, or upcoming listings
- The user asks what cryptos just launched or what coins are coming soon

## Workflow

1. Verify current listings data before writing anything.
2. Use exact UTC windows for the last 7 days and next 7 days.
3. Separate recently listed items from upcoming officially confirmed listings.
4. Mark gaps honestly instead of filling them with rumor.
5. Output the brief in the required markdown format with sources for every row.

## Data To Collect

Always gather:

- recent listings across major exchanges
- upcoming listings with at least one official exchange announcement URL
- launch price when available
- current USD price when available
- timestamped price snapshot
- exchange-level activity summary
- notes for data gaps, notable listings, and rumored items

## Source Guidance

Prefer current information from:

- official exchange announcement pages
- CoinGecko new listings and market pages
- CoinMarketCap listing pages when needed
- other reputable aggregators only when official sources are incomplete

For upcoming listings, at least one official exchange announcement URL is required.

## Report Format

Use this structure:

```markdown
# Crypto Listings Brief [Month DD, YYYY]
*Past 7 days and next 7 days | Sources: [list sources used]*

## Recently Listed Last 7 Days

| Coin | Ticker | Listed Date | Exchange(s) | Category | Launch Price (USD) | Current Price (USD) | Price Timestamp (UTC) | Source(s) |

## Upcoming Listings Next 7 Days

| Coin | Ticker | Expected Date | Exchange(s) | Category | Notes | Source(s) |

## Exchange Activity Summary

| Exchange | Recent Listings (7d) | Upcoming (7d) |

## Notes
```

End with a short reminder to verify on the exchange before trading.

## Rules

- Verify current listings data before writing
- Use exact UTC windows
- Do not fabricate missing dates, prices, or sources
- Show all exchanges when a coin is multi-listed
- Do not provide price predictions or buy and sell commentary
- Flag Binance listings clearly when present
- Only include an item in Upcoming Listings when official confirmation exists
- Put unconfirmed items in Notes as `Rumored`
- Include source URLs for every row

## Exchange Priority Tiers

Weight listings by venue significance instead of treating all exchanges equally:

- **Tier 1**: Binance, Coinbase, Kraken. Listings here move price and deserve top placement and explicit flags.
- **Tier 2**: OKX, Bybit, Crypto.com, Upbit, Bitstamp. Meaningful but less market-moving.
- **Tier 3**: Gate.io, KuCoin, MEXC, Bitget, and similar. High listing volume, low signal per listing; summarize rather than itemize when the list is long.

Sort each table Tier 1 first. A Tier 3-only listing week is itself a signal worth one line in Notes.

## Catalyst Quality

Label every upcoming item with a confidence grade so confirmed announcements never blend with speculation:

- `Confirmed`: official exchange announcement with date; the only grade allowed in the Upcoming table
- `Probable`: strong indirect evidence such as a deposit-open notice or exchange API symbol appearing, but no announcement; Notes only
- `Rumored`: social posts, influencer claims, or unsourced aggregator entries; Notes only, with the claim's origin named

## Duplicate And Stale Filtering

Before finalizing the brief:

- collapse the same coin listing on multiple exchanges into one row listing all venues, rather than one row per exchange
- drop items that already appeared as Upcoming in a prior brief and have now listed; they belong in Recently Listed only
- drop upcoming items whose expected date has passed without confirmation, noting them once as `lapsed` if they were previously reported
- ignore re-listings and trading-pair additions for already-listed coins unless the user asks for them

## Category Labels

Use the most specific applicable category:

- Layer 1
- Layer 2
- DeFi
- DEX
- Lending
- Stablecoin
- Meme
- AI
- RWA
- Gaming or GameFi
- Infrastructure
- Privacy
- Oracle
- Bridge

## Extended Mode

If the request includes `+detail`, add a detail section for each recent listing with:

1. Project purpose
2. Chain or ecosystem
3. Token utility
4. Notable backers, partnerships, or launch metrics

Keep detail mode factual and avoid hype language.

## Validation Checklist

- [ ] Recent listings use the correct 7-day window
- [ ] Upcoming listings have official confirmation
- [ ] Every row includes at least one source URL
- [ ] Missing data is marked honestly
- [ ] Binance listings are clearly flagged when present
- [ ] Output stays informational and avoids trading advice

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A token, exchange list, or time window to check.

Example prompts:

- `Use crypto-listings to summarize recent Binance, Coinbase, and Kraken listings that matter most.`
- `Track upcoming exchange listings for this token and tell me what to watch next.`
- `Show me a sample prompt for using this skill to monitor exchange listing activity.`

