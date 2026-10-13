---
name: recipe-checkdeals
description: "Research recent used Reverb listings for electric guitars above a price threshold to identify deals and market activity."
metadata:
  version: 0.1.0-alpha.1
  openclaw:
    category: "recipe"
    domain: "purchasing"
    requires:
      bins:
        - revcli
      skills:
        - reverb-listings
---

# Check Deals: Recent Used Electric Guitar Listings

> **PREREQUISITE:** Load the following skills to execute this recipe: `reverb-listings`, `recipe-pricecheck`

Fetch recent used electric guitar listings on Reverb.com above a price floor, then extract and present each listing's
key details for deal evaluation.
If the user does not provide a PRICE_FLOOR, default to 1000.

## Steps

1. Fetch listings and write to file:
   ```
   revcli listings list --params '{"product_type":"electric-guitars","price_min":"PRICE_FLOOR","condition":"used","ships_to":US_CON","sort":"published_at"}' --per-page 30 --format json --output /tmp/recent_listings.json
   ```

2. Parse the file with Python. The output is a single JSON object (no `--page-all`):
   ```python
   import json

   with open('/tmp/recent_listings.json') as f:
       data = json.load(f)

   listings = data.get('listings', [])
   ```

3. For each listing, extract:
    - `title` — listing title
    - `condition.display_name` — condition label (e.g. `"Excellent"`, `"Very Good"`)
    - `price.display` — current asking price (e.g. `"$1,299"`)
    - `original_price.display` — original listing price before discounts (if present; gap signals negotiability)
    - `state.description` — should be `"Live"` for active listings
    - `created_at` — listing creation date (staleness indicator — older listings may be more negotiable)
    - `description` — HTML; strip tags and scan for condition caveats (repairs, modifications, replaced parts, damage)
    - `_links.web.href` — direct link to listing (cite as source)

4. Present results as a list, one listing per entry, including all extracted fields.
5. Annotate each cited listing with any condition qualifiers found in the description (e.g. "replaced tuners", "
   refret", "crack repair", "only taken out for photos")
6. Make an initial judgment on deal quality based on price relative to market norms (e.g. "below typical range for
   condition/model", "priced at market", "above typical range")
7. Run recipe-pricecheck sequentially for the models which are deemed good deals to gather more comprehensive market
   data on recent sold prices and active listings for those specific models. If your initial judgements were not
   accurate, run the checks for the other models as well to gather more data and refine your understanding of the
   market.
8. Present the best deals (e.g. those priced below market norms with no major condition caveats) in a final summary
   table, citing all sources and noting any relevant condition qualifiers.
9. Present the rest of the listings in a secondary table for reference, annotated with your deal quality judgment and
   condition qualifiers.

## Parsing Notes

- **Exclude**: listings where `condition.display_name` is `Brand New` — not used-market data
- **Flag with caveat, do not exclude**: listings noting repairs, modifications, or replaced parts — note the specific
  caveat alongside the price
- **Discount depth**: when `original_price.display` is present, note the gap — a large spread signals the asking price
  is negotiable or that prior asks were inflated
- **Staleness**: listings with older `created_at` dates that haven't sold may indicate the ask is above market
- **Always cite sources**: include `_links.web.href` for every listing
- **Description is HTML**: strip `<p>`, `<ul>`, `<li>`, `<br>` etc. before reading condition notes
- **Data presentation**: present the final output as a table with clearly labeled columns for each extracted field
