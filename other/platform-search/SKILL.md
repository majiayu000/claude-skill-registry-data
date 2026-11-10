---
name: platform-search
description: Use to answer a question about the org's campus or the org itself with Platform's search tool, which tries stored pages, then a live source, then the web.
---

# Search

`search` is the one entry point for questions. It looks in this order and says where the answer came from:

1. The org's stored pages and documents (knowledge).
2. The live source you name, such as `library_hours` or `courses`.
3. The web.

## Steps

1. Write the query as keywords that name the subject in full. Bad: `hours`. Good: `Hayden Library hours Sunday`.
2. Name a `source` only when the question is plainly about it: something current such as hours today, open seats, shuttle times, events, scores or dining.
3. Ask several searches with different wording in one `batch`.
4. Answer from the results and cite the URL each one gives.

## When it is not enough

- `knowledge.read_source` (through `modules.call`) reads a whole source a page at a time.
- `knowledge.search` searches only stored pages. `knowledge.web_search` searches only the web.
- To keep a page for later: `knowledge.add_document` for text, `knowledge.set_crawl` for a web page.

## Watch out

- A 409 that names a sign-in (such as clubs or club events) means the org's saved sign-in expired. An officer signs in again on Explore, Shared. Say so and do not retry.
- Never present a result as stored fact when it came from the web. Say where it came from.
- Nothing is looked up before you call `search`. Do not guess an answer that could have changed.
