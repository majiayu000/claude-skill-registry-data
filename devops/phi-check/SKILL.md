---
name: phi-check
description: >
  Inspect Phi's health, behavior, and public history across AT Protocol
  collections using PDS records, AppView context, Logfire, and Fly. Use for
  activity or voice reviews, capability checks, and specific interactions.
---

# phi-check

Phi is `phi.zzstoatzz.io`, DID `did:plc:65sucjiel52gefhcdcypynsr`, Fly app
`zzstoatzz-phi`. Start with the operator's question and a bounded time window;
record the observation time and relevant deployment boundary. A voice review
needs complete writing and context; it does not need every infrastructure check.

## Read history across collections

Resolve the DID's current PDS service, then use `describeRepo` (or the equivalent
pdsx tool) to discover collections. Inspect available tool schemas before calling
them. Public PDS reads do not require signing in as Phi.

Select relevant surfaces from the discovered inventory:

- `app.bsky.feed.post`: authored posts, replies, and quote commentary.
- `app.greengale.document`: full articles, including publication visibility.
- `network.cosmik.*`: library notes, sources, collections, and connections.
- `sh.tangled.*`: code reviews, issues, and other authored project discussion.
- Other writing or media collections when present and relevant to the question.

Likes, reposts, and library links show attention, not necessarily authored prose.
Personality, SELF, goals, and private run summaries explain context; do not count
them as public writing samples merely because a record is publicly readable.

Use `com.atproto.repo.listRecords` with cursors. Check the returned ordering:
`reverse=true` traverses ascending record keys; record-key order is not guaranteed
to be event-time order. Do not stop at the first old timestamp or assume the first
page is newest. If bounded pagination leaves a cursor, report the sample limit;
claim collection completeness only after exhaustion. For larger histories use an
appropriate history index or export rather than silently widening the crawl.

Preserve raw records locally with URI, CID, collection, timestamps, and pagination
coverage. Read full text before judging it. Keep publication time, update time,
AppView indexing time, and observation time distinct. Current PDS records do not
reconstruct earlier edits or deletions; use captured operations and traces for that.

Hydrate reply parents, roots, quoted records, and relevant intervening replies via
AppView or their source repos. Read images when the exchange depends on them.
Join split continuations before assessing prose. Exclude others' reposted text
from Phi's sample, and distinguish spontaneous writing from operator-led tests.

## Connect writing to execution

Find the publication tool call and receipt in Logfire, then follow its trace.
A model summary is a lead, not proof of a successful action or future intention.
Multiple records can be one split post; silence can be a deliberate completed turn.

When a public voice failure appears, immediately capture the actual model request
that generated it using [hone-prompts](../hone-prompts/SKILL.md): instructions,
conversation through that turn, tool results, offered tools, model, and output.
The initial request alone misses context loaded later. Keep raw captures local;
share focused excerpts without credentials or unrelated personal material.

Pass explicit query time bounds. The Logfire MCP defaults to a 30-minute scan;
a SQL timestamp condition alone does not widen it. Respect the tool's current
range limits. Tool spans use `span_name = 'running tool'`, with the name in
`attributes->>'gen_ai.tool.name'`. Inspect actual names and arguments: reactions
can be MCP record writes, not a dedicated `like_post` tool.

For health questions, add `/health`, Fly release/machine state, expected scheduled
runs, and grouped exceptions. Verify whether retries recovered before calling an
error benign. Check the runtime pause separately from the operator override.

## Report what the evidence supports

Lead with the answer, then a few exact examples with source links. For voice,
explain what the writing does differently and what still misses the operator's
preferences; punctuation counts alone do not establish personality. State sample
size, time coverage, and which surfaces lack fresh examples. Separate factual
mistakes, consent failures, and prose quality rather than treating them as one score.

This is inspection. Posting feedback uses `devlog-to-phi` when authorized;
changing live personality, policies, or models is a separate action. Keep history
review here and prompt diagnosis in `hone-prompts`, rather than adding another skill.
