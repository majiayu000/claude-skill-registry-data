---
name: operator-notes
description: The operator keeps distilled working notes at notes.zzstoatzz.io — ai (retrieval, memory, local models, prompt caching), systems (queues, cursors, delivery semantics), operations (observability, diagnosis, sizing), storage (sqlite, turso, turbopuffer, redis), languages (python, typescript, zig), protocols (atproto, MCP), music tooling. Load this when a conversation or a check touches one of those subjects and you want what he has already worked out, before reasoning from scratch or asking him.
---

the notes are mostly distilled by an agent from his working sessions and
curated over time. they are a useful distillation, not a final word — a note
can be wrong in a way nobody has noticed yet. every note ends in a `sources`
footer naming the repo, path, and date the claim came from, which is what makes
it checkable.

## finding a note

the notes are published as `site.standard.document` records on his PDS and
pub-search indexes them, but they are marked not-discoverable, so a plain
`pub_search` never returns them. scope to him and opt in:

```
pub_search(query="<what you actually want to know>", author="zzstoatzz.io", include_undiscoverable=True)
```

hybrid mode is the default and is right for a question. to browse instead of
search, leave `query` empty and pass a larger `limit`. the table of contents
lives at https://notes.zzstoatzz.io/llms.txt if you want the whole map.

## reading one

`pub_get_document(uri)` returns the full text, read live from his PDS. read
the note before you lean on it in public; the snippet is a pointer, not the
claim.

## how to use what you find

- cite it. the web url on the result is a link he expects people to follow.
  "nate has a note on this: <url>" is the honest shape.
- disagree with it when your evidence disagrees. a note distilled from a
  session in march is not a ruling about september; say what you saw and
  where it diverges. a real divergence is worth telling him — it is how the
  notes get more accurate.
- do not paraphrase a note as your own finding. the distinction between what
  you measured and what you read is the thing that makes you trustworthy.
- a note is not a reason to skip checking. if the note says a limit is 8
  and you can measure it, measure it.
