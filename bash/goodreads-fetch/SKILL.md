---
name: goodreads-fetch
description: Pull a Goodreads shelf (titles, authors, read-dates, star ratings, review text, pages, publication year) via the public per-shelf RSS feed — no login, no scraping. Use when you need your reading history, per-year book lists, ratings/reviews, or to refresh reading data for a site or an agent ("pull my goodreads", "what did I read in 2023").
---

# Goodreads fetch

Goodreads redirects any unauthenticated `/review/list/...` request to sign-in, but the **public
per-shelf RSS feed** isn't behind that wall and carries the real `user_read_at` dates.

```
https://www.goodreads.com/review/list_rss/<USER_ID>?shelf=read
```

## Run it

```bash
python3 goodreads_fetch.py --user-id <numeric id> [--shelf read|to-read|currently-reading] [--out goodreads_reads.json]
```

Your numeric id is in your profile URL: `goodreads.com/user/show/<ID>-name`. The shelf must be
public. The feed paginates 100 per page; the script walks all pages.

Output: `{title, author, read_date, read_year, date_added, published, pages, rating, review,
date_precision, read_date_est}` per book. `rating` is 1-5 or null; `review` is raw
`<br />`-separated HTML (convert before display).

## Traps

- **No read-count field, so re-reads can't be detected.** One item per book. Never claim "never
  re-reads" from this feed; true counts need the CSV export (My Books -> Import/Export).
- **Year-only read dates land on Jan 1** (inflating January in month histograms). `read_year` is
  trustworthy; the script marks these `date_precision: "year"` and uses `user_date_created` to
  localise many of them to a month (`read_date_est`), ignoring bulk-shelving days (`BULK_DAY`).
- **Bulk-shelved backlog has no real read date.** Report the dated and undated counts separately;
  don't drop the undated books silently (many carry ratings or reviews).
- **A gap in early years is often a tracking gap**, not a reading hiatus (the account didn't exist
  yet).
- If a blanket stamp is wrong (a series read across years under one date), add it to
  `UNTRUSTED_STAMPS` so those books are treated as undated.
- **Joining quotes or other data to books: match on normalised title AND author surname, exact
  only.** Title-substring matching mis-attributes (e.g. a quote from one *Meditations* landing
  under another).
