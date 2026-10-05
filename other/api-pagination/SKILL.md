---
name: api-pagination
description: Implement correct, fast API pagination — cursor vs offset trade-offs, opaque cursor encoding, stable sort keys, page-size limits, total-count costs, and consumer-side iteration that survives inserts, deletes, and retries. With runnable cursor checks.
type: skill
version: 1.0.0
updated: 2026-07-10
---
# API Pagination

Pagination looks trivial until data changes underneath the reader. Offset pagination silently
**skips or duplicates rows** when inserts land mid-iteration; cursor pagination survives churn but
demands a stable sort key and an opaque token contract. This skill covers both sides: designing the
API and consuming one correctly. Deep detail lives in `references/`; copy-paste material in
`examples/`; a runnable cursor round-trip check in `scripts/`.

## Decision: offset vs cursor

| Situation | Use |
|---|---|
| Admin tables, small datasets, "jump to page 7" required | Offset (`LIMIT/OFFSET`) |
| Feeds, sync endpoints, anything users scroll | Cursor (keyset) |
| Data changes while clients iterate | Cursor — offset will skip/duplicate |
| Deep pages (offset > ~10k rows) | Cursor — `OFFSET n` scans and discards n rows |

Offset's failure mode is correctness, not just speed: a row inserted before your current position
shifts everything, so page 3 re-shows an item from page 2 (duplicate) or swallows one (skip).

## Keyset mechanics (the part people get wrong)

The sort key must be **unique and immutable**. `created_at` alone is not unique — two rows with the
same timestamp make the cursor ambiguous and rows vanish. Always add a tiebreaker:

```sql
-- WHERE clause for "next page after (2026-07-01T12:00:00Z, id 4711)" descending
SELECT * FROM items
WHERE (created_at, id) < ('2026-07-01T12:00:00Z', 4711)
ORDER BY created_at DESC, id DESC
LIMIT 51;  -- page_size + 1 to detect has_more without COUNT(*)
```

Fetch `page_size + 1` rows: if you get 51, there is a next page and the 51st row's key becomes the
next cursor. This avoids `COUNT(*)`, which on large tables costs more than the page itself
(see `references/counting-and-totals.md`).

## Cursor token contract

Cursors are **opaque to clients** — never let them parse or build one. Encode the keyset values plus
the sort direction, base64url it, and (for public APIs) HMAC it so tampering is detectable. Include a
version byte so you can change the encoding later. Full recipe: `references/cursor-encoding.md`;
runnable round-trip: `scripts/check-cursor.mjs`.

## Response envelope

```json
{
  "data": [ ... ],
  "page_info": { "has_more": true, "next_cursor": "djEuMj..." }
}
```

Rules: `next_cursor` is absent (not empty-string) on the last page; page size is capped server-side
(a `limit=10000` request gets the cap, documented, not an error); the default page size appears in
the docs and never changes silently. Consumer-side iteration rules — retries, cursor expiry,
resumption — live in `references/consuming-pages.md`.

## Pitfalls

- **Mutable sort keys** (`updated_at`) — rows teleport across pages as they update. Sort on immutable
  columns or accept re-delivery and dedupe client-side.
- **Cursor built from row position** instead of row values — it is offset with extra steps and
  inherits every offset bug.
- **`COUNT(*)` on every page** — the count is stale by the time the client renders it; provide totals
  on a separate, cacheable endpoint if the product truly needs them.
- **Breaking cursor encoding on deploy** — clients hold cursors across releases; version the token.
- **Missing composite index** — keyset needs an index on exactly `(created_at, id)` in sort order, or
  every page is a scan.

## Verification

Run `node scripts/check-cursor.mjs` — encodes, decodes, tampers, and versions a cursor and asserts
every property above. For the SQL side, `examples/keyset-queries.sql` includes an `EXPLAIN` you can
run to confirm the index is used. Pairs with `rest-api-design` (envelopes, limits) and
`sql-index-tuning` (composite indexes).
