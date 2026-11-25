---
name: book-digest
description: >
  Research and write a 90-day digest of software-development and technology
  books released by O'Reilly Media, Manning, Pragmatic Bookshelf, Packt,
  Addison-Wesley Professional, No Starch Press, Apress, Wiley/Sybex,
  Microsoft Press, and MIT Press. Each entry includes a cover, verified release
  metadata, a source link, and a 1-2 paragraph description. Writes to
  __.BookDigest/. Use when asked to "generate the book digest", "fetch new
  technical books", "find books released in the last 90 days", or invokes
  /book-digest.
---

# Book Digest

Create a sourced snapshot of qualifying books released during the 90 days
ending today. Include all verified titles found; do not rank or pad the list.

## Output

Write one Obsidian Markdown note:

```text
__.BookDigest/YYYY-MM-DD-book-digest.md
```

Create the directory if needed. If today's file exists, replace it only after
the complete digest is ready.

## Scope

Search these publishers and imprints:

1. O'Reilly Media
2. Manning Publications
3. The Pragmatic Bookshelf
4. Packt Publishing
5. Addison-Wesley Professional
6. No Starch Press
7. Apress
8. Wiley/Sybex
9. Microsoft Press
10. MIT Press

Include programming, software engineering, architecture, web/mobile, data,
AI/ML, cloud, DevOps/SRE, security, operating systems, networking, computer
science, and embedded/hardware books. Exclude general business, office
productivity, nontechnical management, videos, courses, audiobooks, bundles,
and journals.

A new edition qualifies. A reprint or a new format of an old edition does not.
Exclude preorders, forthcoming titles, Manning MEAP-only books, Pragmatic Beta
books, and any date described as estimated. The book must have reached its
final published release during the window.

## Tools

- Use `tavily_search` for discovery. Set `search_depth: 'advanced'`,
  `topic: 'general'`, and restrict each search to the publisher's official
  domain.
- Use `obscura_web_scrape` on catalog and detail pages. Fetch `html` when cover
  metadata is needed and `text` for descriptions and publication metadata.
- Use `bash` only for date calculation and the final local checks.
- Use `write` to save the finished note.

## Workflow

### 1. Calculate the window

Use the system date, never a hardcoded year:

```bash
python3 - <<'PY'
from datetime import date, timedelta
end = date.today()
print(f"START={end - timedelta(days=90)}")
print(f"END={end}")
PY
```

Treat both printed dates as inclusive boundaries.

### 2. Discover candidates in parallel

Scrape the official discovery pages below. Follow pagination until results are
older than the cutoff. In parallel, run one official-domain Tavily search per
publisher containing every month and year touched by the window. If a search
returns the maximum number of results, repeat it once per month so titles are
not hidden by the result limit.

| Publisher | Official discovery page | Search domain and identifying text |
|---|---|---|
| O'Reilly Media | `https://www.oreilly.com/search/?q=*&type=book&publishers=O%27Reilly%20Media%20Inc.&order_by=published_on` | `oreilly.com` + `"O'Reilly Media, Inc."` |
| Manning | `https://www.manning.com/catalog` | `manning.com` + `site:manning.com/books` |
| Pragmatic Bookshelf | `https://pragprog.com/titles/` | `pragprog.com` + `"Published:"` |
| Packt | `https://www.packtpub.com/en-us/all-products` | `packtpub.com` + `"Publication date"` |
| Addison-Wesley Professional | `https://www.informit.com/imprint/index.aspx?st=61085` | `informit.com` + `"by Addison-Wesley Professional"` |
| No Starch Press | `https://nostarch.com/category/special/new` | `nostarch.com` + `site:nostarch.com` |
| Apress | `https://link.springer.com/search?facet-content-type=%22Book%22&facet-publisher=%22Apress%22&sortOrder=newestFirst` | `link.springer.com` + `"Publisher: Apress"` |
| Wiley/Sybex | `https://www.wiley.com/en-us/General+%26+Introductory+Computer+Science/Programming+%26+Software+Development-c-CS50` and `https://www.wiley.com/en-us/grow/teach-learn/student-resources/exam-guides/sybex` | `wiley.com` + `Wiley OR Sybex` |
| Microsoft Press | `https://www.microsoftpressstore.com/store/browse/all-titles` | `microsoftpressstore.com` + `"Published" -Video` |
| MIT Press | `https://mitpress.mit.edu/books/` | `mitpress.mit.edu` + `"Pub date:"` and a scoped technical topic |

Search example; substitute the publisher, domain, and actual month names:

```text
{publisher identifying text} ("June 2026" OR "July 2026" OR "August 2026")
software programming architecture data AI cloud security computer science book
```

Catalog pages are the primary discovery source. Search fills gaps caused by
JavaScript, blocked pages, or weak catalog filtering. Do not use Amazon lists,
blogs, or generated "best books" pages to discover candidates.

### 3. Verify every candidate

Open the official detail page and retain a title only when all checks pass:

- The displayed publisher or imprint matches the section. O'Reilly's learning
  platform carries other publishers, so its `Publisher` field must be exactly
  O'Reilly Media.
- The item is a book or ebook, not another media type.
- Its actual publication date falls inside the calculated window and is not in
  the future.
- Its subject falls inside this skill's technical scope.
- Its release is final, not early access or estimated.

Use the page's `Published`, `Publication date`, `Release date`, or `Pub date`.
Do not substitute copyright, page-update, MEAP-start, last-updated, preorder,
or estimated dates. If only a month is supplied, include it only when the
whole month falls inside the window. For a boundary month, find an exact date
from a second authoritative source or omit the title.

Deduplicate by ISBN-13. If ISBN is absent, use normalized title, edition, and
author. Keep one entry when print and ebook pages describe the same edition.

### 4. Collect metadata and covers

For each retained book, collect:

- title and edition
- author or editor names
- publisher/imprint
- exact publication date
- ISBN-13 when available
- page count when available
- 3-6 concrete topic tags
- canonical official detail-page URL
- official synopsis and table of contents
- cover image URL

Get the cover from the detail page's visible product image, `og:image`,
`twitter:image`, or schema.org `Book`/`Product` image. Confirm that the URL
loads and is a book cover rather than a logo or generic placeholder.

If the official page exposes no usable cover, query Google Books by exact
ISBN and require an exact ISBN match:

```text
https://www.googleapis.com/books/v1/volumes?q=isbn:{ISBN-13}
```

Then try Open Library with `default=false` and confirm the response is an
image:

```text
https://covers.openlibrary.org/b/isbn/{ISBN-13}-L.jpg?default=false
```

Never invent an image URL. If all cover sources fail, retain the verified book
but write `> Cover unavailable from the publisher and ISBN services.` and list
it under `## Coverage notes`.

### 5. Write the digest

Paraphrase each description from the official synopsis and table of contents.
Write 1-2 paragraphs totaling about 100-220 words: first explain what the book
covers and how it approaches the subject; then state the intended reader and
practical value when the source supports that claim. Use direct prose. Do not
copy marketing language, add unsupported judgments, or claim to have read the
book.

Use this structure:

```markdown
---
category: book-digest
description: "Technical books released from {START} through {END}."
creation: {END}
last_updated: {END}
window_start: {START}
window_end: {END}
tags:
  - digest/books
  - software-development
  - technology
---

# Technical Book Digest
### Releases from {START} through {END}

> **Coverage:** {BOOK_COUNT} verified books from {PUBLISHER_COUNT} publishers.
> Publication dates and publisher identities were checked against official detail pages.

## Index

- [O'Reilly Media](#oreilly-media) — {count}
- [Manning Publications](#manning-publications) — {count}
- [The Pragmatic Bookshelf](#the-pragmatic-bookshelf) — {count}
- [Packt Publishing](#packt-publishing) — {count}
- [Addison-Wesley Professional](#addison-wesley-professional) — {count}
- [No Starch Press](#no-starch-press) — {count}
- [Apress](#apress) — {count}
- [Wiley/Sybex](#wileysybex) — {count}
- [Microsoft Press](#microsoft-press) — {count}
- [MIT Press](#mit-press) — {count}

---

## O'Reilly Media

### [{TITLE}]({OFFICIAL_URL})

![Cover of {TITLE}|220]({COVER_URL})

- **Author(s):** {AUTHORS}
- **Published:** {YYYY-MM-DD}
- **Publisher:** {PUBLISHER_OR_IMPRINT}
- **ISBN-13:** {ISBN_OR_NOT_LISTED}
- **Pages:** {PAGE_COUNT_OR_NOT_LISTED}
- **Topics:** `{topic-one}` · `{topic-two}` · `{topic-three}`

{DESCRIPTION_PARAGRAPH_1}

{OPTIONAL_DESCRIPTION_PARAGRAPH_2}

---
```

Repeat the entry under the correct publisher heading and sort books newest
first, then by title. Include all ten publisher headings. For a publisher with
no verified releases, write:

```markdown
*No verified qualifying releases found in this window.*
```

Finish with `## Coverage notes` only when something material was incomplete:
blocked catalog, month-only boundary date, unavailable cover, or unavailable
metadata. State the limitation; never imply exhaustive coverage when a source
could not be checked.

### 6. Validate before saving

Check the finished content before calling `write`:

- Every entry has one official detail-page link and either one tested cover or
  an explicit cover-unavailable note.
- Every displayed date is inside the window.
- No ISBN or title/edition appears twice.
- All ten publisher sections exist and index counts match their entries.
- Each entry has 1-2 description paragraphs.
- No template tokens such as `{TITLE}` remain.

After writing, run this minimum structural check:

```bash
OUT="__.BookDigest/$(date +%F)-book-digest.md"
BOOKS=$(grep -c '^### \[' "$OUT" || true)
COVERS=$(grep -c '^!\[Cover of ' "$OUT" || true)
MISSING=$(grep -c '^> Cover unavailable ' "$OUT" || true)
test $((COVERS + MISSING)) -eq "$BOOKS"
test "$(grep -c '^## \(O.Reilly Media\|Manning Publications\|The Pragmatic Bookshelf\|Packt Publishing\|Addison-Wesley Professional\|No Starch Press\|Apress\|Wiley/Sybex\|Microsoft Press\|MIT Press\)$' "$OUT")" -eq 10
```

Report the output path, date window, total book count, count by publisher, and
any coverage limitation.
