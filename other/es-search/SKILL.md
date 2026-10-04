---
name: es-search
version: 1.0.0
description: Fan one question out across every connected source and return a single ranked, deduplicated, attributed result set.
author: matrixx0070
tags: [enterprise-search, search, retrieval, federated, cross-source, ranking]
capabilities: []
---

# Enterprise Search

## When to use
Reach for this when someone asks "where is..." or "what did we say about..." and the answer could live in any connected source — chat, email, cloud storage, or issue trackers. You run one fan-out and hand back one answer instead of making the user hop tools.

**Not for:** planning a fuzzy, multi-part question (use es-search-strategy first); merging conflicting hits into a narrative (use es-knowledge-synthesis); periodic activity roundups (use es-digest); or auditing what is even connected (use es-source-management).

## Method
1. **Read the intent.** Extract the core entities, the likely artifact type (message, file, thread, ticket), and any person or time constraint stated or implied.
2. **Enumerate live sources.** List which connected sources are up. *Decision:* if a source structurally cannot hold this artifact type, skip it and say so — do not burn a query on it.
3. **Fan out in parallel.** Issue one tailored query per relevant source. Use keyword operators for storage and trackers, semantic phrasing for chat and email. *Decision:* if a source returns zero, loosen its terms once before dropping it.
4. **Normalize hits** to a common shape: title, source, author, timestamp, snippet, link.
5. **Rank globally** by term match, recency, source/author authority, and how directly the snippet answers the question — never by which source replied first.
6. **Deduplicate.** Fold the same artifact surfaced by multiple sources into one entry that notes every place it appears.

## Example
Ask: "Where's the final Q3 pricing deck?" You fan out: storage (keyword `Q3 pricing deck filetype:deck`), chat (semantic "final Q3 pricing"), email ("Q3 pricing attachment"). Storage returns two versions and Slack a link to one of them. You dedupe the Slack link into the storage hit, rank the file titled "Q3-Pricing-FINAL" (yesterday) above "Q3-Pricing-draft" (three weeks old), and answer with the FINAL link plus the draft as a runner-up.

## Pitfalls
- Reusing one query string verbatim across sources — keyword syntax starves semantic sources and vice versa.
- Ranking by source order or first-responder speed instead of relevance and recency.
- Reporting the first hit as *the* answer when two near-identical artifacts exist; surface both.
- Silently skipping an unconnected source, leaving the user to assume it was searched.

## Output format
```
Answer: <one sentence if results settle it, else "Top candidates below">

Ranked results:
1. [source] Title — Author, YYYY-MM-DD
   "snippet"  <link>
2. ...

Coverage: searched <sources>; skipped <source> (<reason>)
Refine: <2-3 narrowing filters — person / date / source>
```
