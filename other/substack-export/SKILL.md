---
name: substack-export
description: Export every public post (titles, dates, word counts, full body text) from any Substack publication via its public archive API — no login. Use to pull or back up a newsletter, build an archive page, or feed a writing corpus to an agent ("export my substack", "pull all posts from <sub>.substack.com").
---

# Substack export

Substack exposes a **public JSON archive API** per publication. No auth, no HTML scraping.

```
https://<sub>.substack.com/api/v1/archive?sort=new&limit=50&offset=N   # metadata, paginated
https://<sub>.substack.com/api/v1/posts/<slug>                          # full body_html
```

## Run it

```bash
python3 substack_export.py --sub <subdomain> [--sub <another>] [--out substack_posts.json]
```

Per post: `{sub, title, subtitle, date, slug, wordcount, id, url, audience, body}`, sorted
oldest -> newest, bodies stripped to plain text.

## Traps

- **The archive caps a page at ~24 rows whatever `limit` asks for.** A loop that stops when a
  page is shorter than `limit` sees only the first page (e.g. 23 of 51 posts). The only valid stop
  is an EMPTY page, and the offset advances by rows returned, never by the limit asked. The
  script does this.
- **Only currently-public posts are returned.** Posts you archived or unpublished don't appear;
  for a full history you need your own export (Settings -> Exports) or another copy.
- **Preformatted blocks carry hidden editor boilerplate** ("Text within this block will maintain
  its original spacing when published") inside a `hide-text` label. The stripper drops it; a naive
  tag-strip turns it into fake teaser text.
- Paywalled posts return only the free preview in `body_html` unless you're authenticated.
