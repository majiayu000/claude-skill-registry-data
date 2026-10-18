---
name: self-traces
description: Reconstruct past activity from Logfire execution traces and Jetstream V2 public record archives. Use for incidents, disputed memories, corrections, and cross-lexicon history; load before query_traces or read_archive.
---

Choose the evidence for the question: `query_traces` shows execution requests,
results, and failures; `read_archive` shows retained public repository events;
PDS reads show records that exist now. A saved memory is your account of an
encounter, not independent confirmation of it.

## historical public records

`read_archive(did, collection, after_seq=0, through_seq=None, contains="", limit=10)`
reads stream.waow.tech's Jetstream V2 archive. Resolve handles to DIDs with the
identity tools first. Choose an exact collection: posts, blog documents,
library records, or your own intent records can all be inspected this way.

- Start at `after_seq=0` for retained history. Continue using `next_after_seq`
  and keep the first response's `through_seq` to pin the same sealed snapshot.
  Sequence numbers belong to this instance, not a date or another host.
- `contains` is a literal substring in record JSON, useful for locating a topic
  or thread URI. It reduces returned matches, not download work. Events without
  record bodies, including deletes, cannot match a text filter.
- Each call stops at 24 blocks, 8 MiB downloaded, 20 requested records, 24,000
  approximate output characters, or 45 seconds. The shared reader admits one
  call at a time and six per minute. A budget stop is a page, not a conclusion;
  busy/429 responses mean wait, not call the same request repeatedly.
- `complete` means the requested sealed archive range was exhausted. It does
  not mean complete account history: unsealed live events, deleted/compacted
  records, unavailable repositories, and archive gaps may be absent. An error
  leaves the last successfully examined sequence available for retry.
- Keep `record.createdAt` distinct from `witnessed_us` and `indexed_us`.
  Bootstrapped records can have old publication dates and much later archive
  times. `create_resync` is recovered state, not proof of a new publication.
  An oversized record is explicitly omitted; use its URI to try a PDS read.

A DID filter finds that author's records, not everything said to them. Once
you find a relevant post, follow its reply parent and root through thread/PDS
reads. Include subsequent replies across authors, including the devlog account.
When checking a correction, recover the original claim, what the correction
actually disputed, and any later resolution. Your apology alone does not
establish which facts were wrong. Cite the source URIs when revising a note;
archive reads themselves do not change memory or authorize public contact.

## execution traces

## the actual situation — read this before querying

- `query_traces(sql, start, end=None)` hits a real analytics database
  holding **weeks of your history, millions of rows**. an unbounded query is
  a firehose that will blow out your context. move carefully: every query
  gets a tight `start`/`end` window, a `LIMIT`, and only the columns you
  need.
- the time window comes from the `start`/`end` tool arguments (ISO 8601),
  not from SQL — a `WHERE start_timestamp > ...` alone does not bound the
  scan.
- the columns this skill names below are the ones that matter; they exist.
  don't guess at others — select what you see here.
- this is read-only. you cannot break anything; you can only waste context.

## span shapes that matter

- `span_name = 'running tool'` — one row per tool call you made.
  `attributes->>'gen_ai.tool.name'` is the tool,
  `attributes->>'tool_arguments'` is the JSON args you passed.
  `attributes->'tool_response'` is the returned result. Inspect its errors,
  pagination, and truncation fields when assessing a search's coverage.
- `span_name = 'agent run'` — one row per run of you (a batch, a cycle, a
  scheduled pass).
- `is_exception = true` — things that broke. `exception_type`,
  `exception_message`. many of these were swallowed so the run could
  continue; you never saw them at the time. this is where your blind spots
  live.
- `trace_id` groups one run's spans; filter on it to reconstruct a single
  incident end to end.

## recipes

locate a call (this lists requests, not their outcomes):

```sql
SELECT start_timestamp, trace_id, span_id, attributes->>'gen_ai.tool.name' AS tool,
       left(attributes->>'tool_arguments', 200) AS args
FROM records WHERE span_name = 'running tool'
ORDER BY start_timestamp LIMIT 50
```

inspect a list_records result's coverage in the same tight time window:

```sql
SELECT start_timestamp, attributes->'tool_response'->>'error' AS error,
       attributes->'tool_response'->>'truncated' AS truncated,
       attributes->'tool_response'->>'shown' AS shown,
       attributes->'tool_response'->>'fetched' AS fetched,
       attributes->'tool_response'->>'cursor' AS cursor,
       attributes->'tool_response'->>'message' AS message
FROM records WHERE span_name = 'running tool'
  AND attributes->>'gen_ai.tool.name' = 'list_records'
ORDER BY start_timestamp LIMIT 20
```

These fields describe the returned page. `limit=100` is a request;
`shown=48, fetched=100, truncated=true` means 48 records reached you.
A null field means that field was absent, not that pagination was exhausted.
For other tools, inspect their own result shape. Fetch one identified span's
`attributes->>'tool_response'` in numbered SQL substring slices when it
exceeds query_traces' 6,000-character output cap. Preserve `trace_id` and
`span_id` so slices and conclusions refer to the same call. Missing or
scrubbed telemetry leaves the corresponding question unresolved.

what failed on me lately (weekly hygiene, or when something feels off):

```sql
SELECT exception_type, left(exception_message, 150) AS msg, count(*) AS n
FROM records WHERE is_exception
GROUP BY 1, 2 ORDER BY n DESC LIMIT 20
```

count tool calls over a period (activity totals, not proof of outcomes):

```sql
SELECT attributes->>'gen_ai.tool.name' AS tool, count(*) AS n
FROM records WHERE span_name = 'running tool'
GROUP BY 1 ORDER BY n DESC LIMIT 30
```

## discipline

traces are for **postmortems, retro receipts, and audits** — answering "what
happened", "why did I do that", "is this claim about myself true". they are
not an input for deciding what to post or trade next; reading your own
reasoning back in ordinary cycles is a mirror, and you already know where
mirrors lead. cite what you find the way you cite any incident: timestamp,
what the trace shows, what you concluded.
