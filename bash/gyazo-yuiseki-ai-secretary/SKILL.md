---
name: gyazo
description: Search, read and summarise a person's Gyazo captures from the command line with the `gyazo` CLI - screenshots and phone photos, their OCR text, the application or page they came from, and where they were taken. Use when asked what someone saw, captured, read, bought, visited or worked on, when a question needs evidence from their screen history, or when a Gyazo image ID, a gyazo.com URL or a collection needs to be read.
---

# Gyazo CLI

`gyazo` reads a Gyazo account: screenshots, phone photos, their OCR text, the
application and page a capture came from, and the coordinates and address of a
photo. It caches everything it reads under `~/.cache/gyazocli`, so repeated
questions about the same period are answered locally.

Check `gyazo config get me` first when a token might be missing; it prints the
account or exits non-zero. Set one with `gyazo config set token <token>`.

Every command exits non-zero on failure, so `&&` chains and `set -e` behave.

## Reading captures

```bash
gyazo ls --limit 10                  # most recent, newest first
gyazo ls --date 2026-08-30           # a local day; also yyyy-mm and yyyy
gyazo ls --today
gyazo ls --hour 2026-08-30-14        # one hour, from the cache only
gyazo ls --photos                    # shorthand for has:location
gyazo get <image_id>                 # one capture in detail
gyazo get <image_id> --ocr           # just the OCR text
gyazo <image_id>                     # same as get
gyazo <https://gyazo.com/...>        # same as get
gyazo ./screenshot.png               # an existing file uploads instead
```

Add `-j`/`--json` to any of these when the output is going to be parsed rather
than read. Add `--no-cache` when the answer must come from the API.

## Searching

`gyazo search <query>` takes Gyazo's own query language. The operators below
were confirmed against the live API; see [references/search-syntax.md](references/search-syntax.md)
for the measurements behind them and the ones that do not exist.

```bash
gyazo search "お好み焼"                        # OCR text, title and description
gyazo search "has:exif"                        # photographs, not screenshots
gyazo search "address:広島"                    # where a photo was taken
gyazo search "date:2026-08-30"                 # a day, a month or a year
gyazo search 'app:"Gyazo Android"'             # the application it came from
gyazo search "ocr:Wi-Fi has:exif"              # terms are ANDed
gyazo search "address:広島 OR address:京都"     # capital OR
gyazo search "has:location -app:Chrome"        # leading - negates
```

Three things worth knowing before composing a query:

- **An operator Gyazo does not know returns nothing**, rather than falling back
  to a text search. A guessed operator looks exactly like "no such captures".
- **`has:exif` is how to narrow to photographs.** The application does not tell
  them apart: `app:"Gyazo Android"` includes screenshots and screen recordings
  from the same phone.
- **There is no coordinate or radius search.** Search by place with `address:`,
  which matches the address in any language and matches postal codes too.

## Summaries and rankings

```bash
gyazo summary                        # the week to yesterday, day by day
gyazo summary --date 2026-08-30
gyazo stats --days 30                # one markdown report
gyazo apps --date 2026-08            # what applications, most used first
gyazo domains --today
gyazo tags --date 2026
gyazo locations --date 2026-08-30
```

The ranking commands take `--date`, `--today`, `--limit`, `--max-pages`,
`--json` and `--no-cache`. Only `stats` takes `--days`.

## Collections

```bash
gyazo collection <collection_id>
gyazo collection https://gyazo.com/collections/<id>
gyazo collection <id> --sort captured   # added | created | captured
gyazo collection <id> --anonymous       # read a public one without the token
```

A collection ID and an image ID are both 32 hex characters and cannot be told
apart on their own, which is why `gyazo <bare id>` reads it as an image. Pass
the `/collections/<id>` URL when the ID is a collection.

A collection larger than 100 images is reported as truncated: the public
endpoint returns the first 100 and cannot page.

## Filling the cache

```bash
gyazo sync --days 7                  # yesterday back through 7 days
gyazo sync --date 2026-08            # a whole month
```

`sync` covers yesterday backwards and never today, because today is still
happening. For anything from today use `ls --today`, `search`, or a ranking
command with `--today`.

## Answering questions with captures

- A day is a local day. `--date 2026-08-30` means that date in this machine's
  timezone, which is also how the cache is laid out.
- Prefer `search` with an operator over `ls` plus filtering. The API does the
  work, and `ls --date` over a wide range walks many pages.
- OCR text is noisy: it comes from screenshots at whatever resolution, and
  `locale` is often `und`. Treat it as a hint, not a transcript.
- `get --objects` prints detected objects, but the API no longer returns the
  field it reads, so it exits non-zero with "Object annotations not found" on
  every capture tested. Use the OCR text instead.
- **Do not turn a capture into a claim it does not support.** A product page or
  a cart is interest; an order confirmation or a payment receipt is a purchase.
  Say which capture the conclusion rests on.
- A phone photo carries coordinates and a reverse-geocoded address in
  `metadata.exif_normalized` and `metadata.exif_address` of the `--json`
  output; the top-level `exif_normalized` is always null. Screenshots carry
  neither.

## Serving the same data over MCP

`gyazo --mcp-server` runs the same functionality as a Model Context Protocol
server over stdio, for a client that speaks MCP rather than shell. Everything
above is the shell path.
