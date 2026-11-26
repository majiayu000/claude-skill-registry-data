---
name: product-price-monitor
description: "Watch product, flight, or listing prices; alert on target."
version: 0.1.0
author: Ben Barclay (benbarclay), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Prices, Availability, Shopping, Travel, Alerts]
    related_skills: [maps]
---

# Product Price Monitor

Monitor a concrete purchasable item and alert on a normalized all-in price or availability condition. Handle variants, taxes, fees, currencies, stock, cancellation terms, and duplicate alerts explicitly. Setup runs once in the foreground; the recurring check runs as a `cronjob` tick (the `price-watch` automation blueprint scaffolds this).

## When to Use

- "Alert me when this laptop drops below $1,000."
- "Watch these flights for a fare under $500."
- "Tell me when this hotel has a refundable room."
- "Track ticket/listing availability."
- A cron tick fires for an existing price watch (steps 4-6).

Don't use for: one-off "what does this cost right now" lookups (use `web_search`/`web_extract` directly).

## Procedure — Setup (foreground, once)

### 1. Define the exact item

Record source URL/provider, product/listing ID where available, variant, quantity, location, dates, travelers/guests, membership/login assumptions, condition, seller, and acceptable substitutes. Done when two variants cannot be confused.

### 2. Define the alert condition

Specify currency, all-in vs pre-tax price, maximum price, availability/stock rule, shipping, refundability, cabin/room/ticket class, cooldown, and notification destination. Done when synthetic examples have deterministic alert decisions.

### 3. Establish a live baseline, then schedule

Fetch a bounded live result with `web_extract` or `browser_navigate` and record retrieval time, source price, fees/taxes, availability, and terms. Do not schedule until one foreground fetch works. Write the watch contract (item, condition, baseline observation) to a state file under `${HOMINEM_HOME:-$HOME/.hominem}/price-watches/<watch-slug>.json`, then create the job:

```
cronjob(action="create",
        schedule="every 6h",
        prompt="Load the product-price-monitor skill and run the tick for the watch contract at ${HOMINEM_HOME:-$HOME/.hominem}/price-watches/<watch-slug>.json.",
        deliver=<user's destination>)
```

Pick a cadence that respects rate limits and site terms. Done when the baseline matches the exact item contract and the job exists.

### 3b. History file (append-only)

Each watch keeps `price-watches/<watch-slug>.observations.jsonl` beside its contract — one JSON object per tick, including failed fetches (marked `"status": "failed"` so reliability is analyzable too):

```json
{"retrieved": "2026-11-09T12:20:00Z", "price": 24.99, "source_currency": "GBP", "availability": "for sale", "status": "ok"}
```

At 4–6h cadence this is ~2k lines/year — negligible; keep it raw, never downsample in place. Analysis (drop velocity, sale cycles, weekday effects) loads the file into pandas at query time; the store itself stays dependency-free and grep-able.

## Procedure — Tick (each scheduled run)

### 4. Fetch and normalize

Re-fetch the source. Convert currency only with a timestamped rate and retain the source currency. Separate base price, mandatory fees, shipping/taxes, total, and availability. Exclude volatile page metadata. A failed fetch means unknown state: report or skip, but never overwrite the last good observation with an error page. **Append one line per attempt to the observations file** (failed attempts included, with `"status": "failed"` and no price). Done when the observation is comparable to the baseline or explicitly marked failed, and the history line is written.

### 5. Compare and suppress duplicates

Alert on threshold entry, qualifying availability, material lower price, or recovery as requested. Store the last good observation and last alert fingerprint in the state file. Replaying the same offer must send no second alert; respect the cooldown. Done when the alert decision is deterministic against stored state.

### 6. Deliver or stay silent

When a condition is met, the alert includes: exact item/variant, observed all-in price and source currency, availability/terms, threshold, retrieval timestamp, source link, and important uncertainty. Never claim inventory is reserved. When nothing qualifies, stay silent — no "still watching" noise unless a periodic all-clear was requested. Done when the state file reflects this run.

## Pitfalls

- Comparing a base fare with an all-in threshold.
- Alerting on the wrong size, seller, cabin, dates, or room terms.
- Overwriting a last-known-good value with an error page.
- Polling aggressively enough to trigger blocking or violate site terms.
- Scheduling before a single foreground fetch has succeeded.

## Verification

- [ ] The watch contract pins the item so two variants cannot be confused.
- [ ] One foreground fetch succeeded before any job was created.
- [ ] Alert decisions replay deterministically from the state file; duplicates suppressed.
- [ ] Failed fetches never replaced last-known-good state.
- [ ] Every attempt appended exactly one history line (ok or failed).
- [ ] Alerts carry all-in price, source currency, timestamp, and source link.
