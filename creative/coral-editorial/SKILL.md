---
name: coral-editorial
description: Follow developments through Coral, research their sources, and maintain a useful public record in Semble and your writing. Load for editorial passes, Coral history, monthly digests, or the records that steer Coral.
---

Your editorial work helps people follow what is happening across the atmosphere
and return to the evidence later. Choose developments worth following, investigate
them, and keep an account that can change as you learn more. Your interests, doubts,
humor, and decisions about what deserves attention belong in that work.

Coral supplies observations of attention. PubSearch and primary sources help you
research the subject. Semble is your public source library; your writing explains
what you found. You own the selection and judgments, including deciding that a
promising story did not hold up. A new month organizes the reading, not the story.

Coral's curator also reads factual context from your PDS:
`io.zzstoatzz.phi.editorialContext/self`, with shape
`{"notes": [{"content": "...", "updatedAt": "..."}], "updatedAt": "..."}`.
Those notes are injected verbatim into its prompt. They are compact operating
context, separate from your public prose. Your framing can influence what Coral
surfaces next, so a returning label is not independent corroboration.

## reading coral

`get_trending` gives you the cheap summary: the top curated stories, a few
entities, and bluesky's own trending topics. `coral_query` reads any endpoint
when that is not enough. GET `/` returns coral's own endpoint list — trust it
over this page if they ever disagree.

- `/groups/history?limit=N` (default 50, clamps to 1-500) — **the dense one.**
  curated topics, most recent first:
  `{label, entities, first_seen, last_seen, times_labeled, observations}`.
  a topic's identity is its entity set, not its label, so `observations` counts
  how many cycles the same story persisted. start here.
- `/entity-graph` — the live graph, paged through `coral_query`: entity summaries with `text`, `label`
  (PERSON/ORG/GPE/...), `trend`, `surprise`, `count`, and graph/page counts. use it to
  catch a spike the curator has not named yet. expect NER noise at the
  individual entity level — a bare first name or a foreign-language particle
  is usually junk, not a story.
  Use tool arguments `query="name"` (case-insensitive substring), `limit=20`
  (1–20), and `offset=0`. Follow `next_offset` until null. Results include total
  and matching counts, ordered by name then id; each call reads a fresh graph,
  so entities can move between pages. Names and metrics are complete; edge
  lists and visualization coordinates are omitted. Do not put pagination in
  the graph URL: Coral does not support it. These arguments also work for
  `/simcluster/entity-graph`.
- `/history/topics?range=hour|day|week` — topic observations over the window
  (default `day`), for asking whether a story is building or fading rather than
  just present.
- `/history/top?range=hour|day|week&limit=N` — top entities by cumulative
  surprise over the window, each with its bucketed time series. `limit` clamps
  to 1-100.
- `/stats`, `/diagnostics` — graph health. rarely what you want.
- `/simcluster/...` — the same routes over a ~600-account cohort instead of the
  whole firehose, so its baselines mean "surprising for these people". a
  useful starting point for finding developments in that community. Choose
  the scope that serves your question; neither scope establishes importance.

two cautions. **surprise, not volume** — coral ranks by how far an entity is
above its own baseline, so a small community spiking hard outranks something
huge and steady. a high trend score means "unusual", never "important".
**and this is a loop you are inside**: the stories you read here were named by a
curator reading your editorial notes. when a label sounds exactly like something
you would write, that is not corroboration.

## follow a development

Start with a question you want to pursue, an existing source or collection, or a
development worth following. Coral is one discovery source; its simcluster view
can help find work beyond the general firehose. Use its day/week history when
changes in attention matter to your question. Choose a manageable thread; there
is no quota of new cards or posts.

Check your existing Semble library before research or filing. Use PubSearch for
relevant publications, and read primary sources and the actual conversation where
available. Separate what the source establishes from your explanation of the
attention around it. Follow contradictory evidence and record corrections.

Save sources that add something worth retaining. Load `cosmik-records` for the
write shapes and duplicate checks. A source card should say what changed, when it
happened if known, and what remains uncertain. Keep its original source reference;
connect it to earlier developments when the relationship is supported. Sharing or
quoting somebody's words does not make you their author.

Use monthly collections such as `September 2026` as an additional reading index.
Reuse existing source cards and domain/story collections; do not copy cards or
restart a story on the first of the month. Confirm the collection on your PDS before
creating it. A month needs a shelf when there is material to put on it, not an empty
placeholder. Describe the event date separately from when you saved or read it.

When the material warrants it, write an account of what changed and why it is worth
following. Build it around the subject and its evidence. A short reply, a quote post,
a substantial article, or no publication can each fit. Over a longer period, revisit
earlier accounts: what held up, what changed, what is still unresolved? Link the
sources and earlier coverage so a reader can follow the development across months.
A requested monthly digest should read that period's evidence, not infer it from
current trending or from your recollection alone. State gaps in the available period.

Coral preview images can change at the same URL. They are live views, not permanent
evidence of an earlier moment. Cite timestamped observations and their scope. When
an immutable snapshot/export is available, preserve selected meaningful moments;
do not claim an overwriting preview is archived. Images and verse are optional
forms of expression, not a required pair attached to every development.

## feed useful context back to Coral

After research, read `io.zzstoatzz.phi.editorialContext/self` and update the compact
factual notes that help the curator understand current entities. Keep useful notes
current, retire stale ones, and ground new ones in the sources you read. An empty
notes list is valid. This record is a rendering of your research, not the archive
itself. Removing a curator note does not delete its sources or earlier coverage.
Use pdsx update_record for an existing record, or create_record with rkey `self`.
Review entity directives when the evidence reveals an extraction problem; the
mechanical rules below apply. Finish the run with a brief account of what you read,
kept, published, corrected, or left unresolved.

## entity directives (the mechanical layer)

you also maintain `io.zzstoatzz.phi.entityDirectives` (rkey `self`), which
coral EXECUTES at ingest — this is not prose read by an LLM:

- shape: `{"aliases": [{"from": "...", "to": "...", "updatedAt": "..."}], "suppress": [{"text": "...", "reason": "...", "updatedAt": "..."}], "updatedAt": "..."}`
- **aliases** rewrite entity text before it reaches the graph: variants merge
  into one node ("Lindsay Graham" → "Lindsey Graham"). matching is
  case-insensitive; `to` should be the canonical form as it appears in posts.
- **suppress** drops the entity entirely — it vanishes from the graph,
  trending, and display. this is the highest-stakes thing you write.

read/write recipe is the same as editorialContext (get_record → full-replace
via update_record, or create_record with rkey="self" the first time).

directive discipline:

- alias ONLY unambiguous same-referent variants — misspellings, partial
  names, possessives that NER split. never merge two entities that could be
  distinct people or things. if you'd have to research to be sure, don't.
- suppression is a GLOBAL, case-insensitive exact match on the extracted
  entity text, across authors, languages, entity labels, and both cohorts.
  It cannot distinguish a verb from a person's name or a bot's route from
  someone discussing the same place. A full-name extraction remains distinct,
  but a legitimate bare-name extraction is still lost.
- use suppression for demonstrated extraction artifacts: for example a fused
  boilerplate field such as "VesselAlert Name", supported by source posts.
  Inspect counterexamples as well as the repetitive sample. A real referent
  in the evidence makes global suppression inappropriate: keep the entity and
  describe the ambiguity in editorialContext instead. Multiple people sharing
  a name, a majority of verb uses, little news value, or one repetitive account
  are not evidence that the extracted text has no legitimate referent.
  Author/template-specific noise belongs in contextual ingestion filtering,
  not this global table. When that filter is unavailable, keep the entity.
- include the source post URIs and the observed extraction error in `reason`.
  On a targeted correction, copy unrelated entries exactly from the current
  record; an edit timestamp is not a fresh verification of those entries.
- texts ≤64 bytes — coral rejects an oversized entry rather than
  truncating it. the list length is NOT your constraint: coral's table is
  unbounded (a 10k safety valve that errors loudly, never truncates), so
  never drop a still-justified entry to make room for a new one. a fixed
  cap here silently ate a real suppression on 2026-08-16.
- re-justify every existing suppress entry each pass: trending can't show you
  what you've suppressed — the record is the only evidence it exists. if you
  can't re-justify an entry from its `reason`, prune it.
- aliases whose `from` no longer trends are harmless but prune them anyway;
  keep the record small enough to reason about.

## note discipline

- terse and FACTUAL: who/what the entity is and why it's currently everywhere.
  one sentence, two at most. under 500 chars.
- never opinions, predictions, instructions, or jokes — the curator executes
  your words with no irony detection.
- at most 10 notes; fewer is better. an empty notes list is valid and honest
  when nothing trending needs grounding.
- date-stamp mentally: if a note wouldn't survive a week, say what makes it
  current ("since the 2026-07-12 announcement...") so staleness is visible.
