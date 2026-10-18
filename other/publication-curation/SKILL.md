---
name: publication-curation
description: How to read the atproto publications network (pub-search) and recommend documents you endorse. Load this when you want to see what's circulating among publications, find writing worth reading, or put your own weight behind a piece — curation, not just consumption.
---

the publications network (leaflet, greengale, offprint, pckt, ...) has its own
recommendation graph, separate from bsky likes: readers write small public
records endorsing documents, and surfaces like pub-search's "most-recommended"
rank by them. you can read that surface with your `pub_*` tools and participate
in it with an ordinary record write. no dedicated tool — this is the same
generic-record paradigm as pdsx-fundamentals.

## reading the surface

- `pub_discover_focal_post(window, sort, limit)` — the most-recommended posts,
  exactly what the pub-search "recommended" page shows. `sort="trending"` for
  momentum, `sort="top"` for raw counts. start here.
- `pub_search(...)` / `pub_get_document(uri)` — search, full text.

## recommending is just a record

a recommendation is one record in YOUR repo pointing at the document:

```
mcp__pdsx__create_record(
  collection="site.standard.graph.recommend",
  record={"document": "<at-uri of the site.standard.document>", "createdAt": "<now, iso8601>"}
)
```

that's the whole act. pub-search and the publication platforms index it off
the firehose; your DID shows up in their curator graphs. (an older lexicon,
`pub.leaflet.interactions.recommend` with a `subject` field, exists in the
wild — write the `site.standard.graph.recommend` shape; it's what active
curators use now.)

## curation standards

- **read before you recommend.** `pub_get_document(uri)` first, actually read
  it. a recommendation is a public endorsement with your name on it — the
  publications crowd notices curators whose taste is real, and notices the
  other kind too.
- **recommend sparingly.** the signal is scarcity. a handful a week from
  genuine reading is enough; the weekly pass recommends at most two documents.
  if your honest reaction is "fine, i
  guess", don't.
- **no self-recommendation.** never recommend your own greengale posts.
- **don't double-recommend.** check your own repo first:
  `mcp__pdsx__list_records("site.standard.graph.recommend", repo=<your did>)`.
- **cross-pollinate, don't duplicate.** a document worth recommending is often
  also worth a cosmik card with a one-sentence why (see cosmik-records) — the
  recommend is the public vote, the card is your own library. do both when it
  genuinely earned both.
