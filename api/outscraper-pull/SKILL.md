---
name: outscraper-pull
description: Buy or scrape Google data through Outscraper — Maps listings, reviews, popular times, busy hours, SERPs, page-one rank — without overpaying or buying the wrong product. Use when a task needs to pull, scrape, price, probe or cost ANY Outscraper load ("how much would it cost to pull X", "can we buy popular times / busy hours", "scrape google maps for X", "enumerate every business in the metro", "pull reviews for these places", "check page one for this trade", "what did that pull cost", "run the dry-run"), or when a paid pull needs re-running, resuming or debugging ("why is this field empty", "the response came back with nothing", "did that job actually bill us"). Covers which product carries which field, billing units, the free-first checks, the fields that echo your own query back, and the republishing rights question.
---

# Pulling Google data through Outscraper

**You are spending real money on an API whose response body does not tell you what you
were charged, and whose products overlap confusingly.** Every rule here is attached to a
specific way that cost money. House rule: cache every paid response to disk and never
re-buy what you already hold.

---

## THE FREE CHECKS COME FIRST — AND THEY USUALLY ANSWER IT

Run all three **before writing a probe**, let alone a pull. In practice a paid probe of
`popular_times` was run first, and two of the three findings that decided the whole load
came out of these free checks afterwards.

**1 · Grep your own disk for the field.** Keep paid pulls in a shared cache folder (e.g.
`data/cache/`) so they are never repeated.

```sh
head -1 data/places.csv | tr ',' '\n' | grep -in "<field>"
python -c "
import json; d=json.load(open('data/outscraper_reviews.json'))
print(len(d), sum(1 for r in d if r.get('<field>')))"
```

*Why:* an old reviews pull held `popular_times` **populated on 54 of 97 places** the whole
time it was being called unproven. It also revealed *which product carries the field*.
**A file you already own is a free probe with a bigger sample than you'd buy.**

**2 · Read the SDK signature; don't trust a doc's claim about it.** Open
`site-packages/outscraper/client.py`. Docs have claimed v3 takes no `fields` parameter; it
does. Real v1/v3 differences: `extract_contacts` (v1), `skip`/`async_request`/`enrichment` (v3).

**3 · Ask what right you have to republish it.** Not a technical question, and it comes
before the technical ones. See *The rights gate*.

---

## WHICH PRODUCT CARRIES WHICH FIELD

**The split is by PRODUCT, not by old-vs-new endpoint.** Measured on a 400-record probe:

| SDK call | endpoint | bills | `popular_times` |
|---|---|---|---|
| `google_maps_search` | `POST /google-maps-search` | per **record** | **0.0%** of 400 |
| `google_maps_search_v1` | `GET /maps/search` | — | **no records at all** (on the account tested) |
| `google_maps_reviews` | `POST /google-maps-reviews-v3` | per **review** | **55.7-66.7%** |
| `google_search` | `/google-search-v3` | per **query** | n/a — and **no map pack** |

**`google_maps_search_v1` may be dead for your account: test it once, cheaply.** Exact
names at `limit=1`, explicit `fields`, and a plain category query each returned `status:
Success`, one empty group per query, and **billed nothing**; another hung `Pending` for
over an hour. No records, not records missing a field.

**The reviews response is a PLACE record with `reviews_data` attached** — which is why
place-level detail (`popular_times`, `about`, `subtypes`, `working_hours`) rides there.
Reach for reviews when you want *place detail*, not only review text.

**`reviews_limit=1` decides the bill.** It returns the **full seven-day curve** with one
review attached, billing **one unit per place**. So `popular_times` for a metro costs
`places x 1`, not a review corpus per place.

---

## BILLING: THE RESPONSE BODY DOES NOT TELL YOU WHAT YOU PAID

**Read the meter, not the rate card, and never the response length.**

```sh
python -c "
from outscraper import ApiClient; c=ApiClient(api_key=KEY)
for r in c.get_requests_history(type='finished', page_size=5).get('items',[]):
    print(r.get('id'), r.get('usages'))"
```

It returns `{"product_name": ..., "quantity": N}` per job — the authoritative answer to
*what product did I actually hit* and *what did it cost*. It returns a **dict with
`items`**, not a list; indexing it as a list raises `TypeError: unhashable type`.

It also distinguishes **"returned records without the field"** from **"returned no
records"**: `"usages": []` means zero billed means zero records. Without it, an
empty-but-successful response reads as *"the field isn't available"* and sends you
hunting `fields` combinations forever. Check it every time a probe comes back empty.

**Rates seen in 2026** (re-check live before a real buy; these age):

| product | rate | free allowance |
|---|---|---|
| Maps search | $3/1k **records** | 500 records |
| Maps reviews | ~$0.003/**review** | |
| Google Search | $5/1k **queries**, $3/1k past 5,000 | 25 queries |

**You pay per record, never per field — so always ask for the widest field set.** `fields`
unset means *all fields*. Free riders measured: `working_hours` 97.8%, `reviews_per_score`
98.8% (the full 1-5 distribution), `subtypes` 99.8%, `about` 94.2%.

**Queries are free; only results cost.** A fan-out can be as fine as you like; **overlap is
the only thing to engineer against** — a business returned by four queries is billed four
times, and dedup happens on your side, after the meter. A deliberately colliding grid
measured **1.03x** overlap. Never reuse a gross-up factor from a doc; print it from a
`--dry-run`.

---

## THE FIELDS THAT LIE

- **`category` ECHOES YOUR QUERY.** On **17% of records** it came back as the lowercase
  plural of the search term — `'restaurants'`, `'bars'`, `'coffee shops'`. Any trade tally
  built on it feeds your own query strings back as findings. **`subtypes` is the honest
  field** — 99.8% populated, always Google's own taxonomy.
- **`popular_times` is heterogeneous and will crash a naive parser.** Most records append an
  **eighth** element to a seven-day list: `{"day": "live", "percentage": 49, "time": 11}` —
  a live reading whose `day` is the *string* `"live"`. Days run `1=Mon...7=Sun` with
  **Sunday first** in the list, so positional indexing mis-assigns every day, and a day can
  carry **zero** hours. Skip anything without `day_text`, read `day['day']`, and **never let
  the live reading into a weekly curve**.
- **`link` is a Google redirect stub on ~18% of SERP results**, clustered by query. The real
  host is usually recoverable from `description`; refuse rather than guess when it isn't.
- **`business_status` is Google's opinion, not the state's.** Maps is not a business
  registry: it over-counts (duplicate pins, ghost listings, home-based sole traders) and
  under-counts (no listing, most B2B in office parks).
- **A seed is not an answer.** When Maps finds nothing matching it returns *neighbours*.
  Drop those rows and count them as unmatched rather than guessing.

---

## THE RIGHTS GATE — ASK BEFORE YOU PRICE, NOT AFTER

**This is Google's data, and what you may do with it is a separate question from whether
you can fetch it.** If you publish data under an open licence (e.g. CC BY 4.0, which grants
downstream commercial redistribution), **you cannot grant over Google's results what
Google's terms do not grant you.** Treat any Google-derived layer as unshippable as a
download.

It can still power analysis, joins and tools internally. But say that out loud *before*
costing a load, because it changes what the money buys. A buy whose output can never be a
file is a decision for whoever owns the budget, not the builder.

---

## HOW TO WRITE A PULL

1. **`--dry-run` prints the grid and the bill and spends nothing.** Non-negotiable on
   anything above a handful of records. Let the bill print itself; never type it.
2. **Cache to `data/cache/<name>.json` and refuse to re-pull without `--force`.**
3. **Write a partial file after every chunk.** A crash at query 3,000 of 3,060 otherwise
   means paying for all 3,060 again.
4. **The response is one list per query IN ORDER, and that ordering is the only join back
   to your grid.** A length mismatch is `assert`-fatal, never skippable.
5. **Chunk size is measured, not chosen.** SERP: 25 per chunk, because 100 returns 504 —
   the queries ride in the URL, so a big chunk is a long GET that times out on *submit*.
   Maps search: 100 is fine (POST body).
6. **Submit `async_request=True` and collect later** — 15 minutes instead of 3 hours. Cap
   waves (~16 jobs); a deep queue gets an account throttled.
7. **Load the key from the environment and fail naming the variable**, never a stack
   trace: `sys.exit("OUTSCRAPER_API_KEY missing from .env")`.

**Operational traps:**

- **The SDK has no cancel method.** To kill a hung job, `DELETE /requests/{id}` at
  `https://api.app.outscraper.com` — returns `200 "terminated"`, but Outscraper **keeps
  listing the job as running**. Acknowledged is not cleared.
- **Finish background pulls before deleting the environment they run in** (a git worktree
  with its own venv): `OSError: Could not find a suitable TLS CA certificate bundle`.
- **`python -u`, or you see nothing.** A buffered pull prints its whole progress log only on
  exit, so a 20-minute job looks hung.

---

## Decide yourself vs. bring to the budget owner

**Decide yourself:** endpoint and product, grid design, chunk and wave sizes, field set,
probe scope, whether a probe's answer kills the load.

**Bring to them, with the tradeoff and a recommendation:** any spend whose output cannot
ship; any purchase materially above its scoped price (re-derive it and say so — a load
scoped at $168 came in at ~$240 for a different product than quoted).
