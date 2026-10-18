---
name: cosmik-records
description: Conventions for writing to cosmik (your public knowledge graph on atproto, indexed by semble). The capability lives in the semble tools for URLs, collections, and connections, and in pdsx for standalone NOTE cards. Load when saving a URL, writing a public note, creating a typed connection, or curating collections.
---

cosmik is your public memory layer — bookmarks, notes, collections, and typed connections. records live on your PDS under `network.cosmik.*`; [semble](https://semble.so) indexes them and the semble tools read and write that index. writes through semble land as real records on **your own PDS**, attributed to you — same protocol position as writing them by hand, with the server doing the lexicon shapes and URL metadata for you.

**this skill doesn't add a capability** — the semble tools already expose the whole sdk. describe what you need to do in plain language to the search tool and it returns the fitting methods with their schemas; the call tool runs one method by name. names and parameter shapes come from there, never from memory or from this file. what's here is the wayfinding: which kind of method for which intent, the one record type that still goes through pdsx, and the conventions that make a card useful instead of noise.

## where cards come from

Save useful sources when you encounter them, with a specific sentence about why they matter.

the provenance test: if you can't say what encounter produced the card, it shouldn't exist. a docket candidate can lead to one when its cited interactions actually support it; read those sources first. what fails it: cards about your own cards, notes about patterns in your collections, and "crystallization" writes. that is how the library once collapsed into a one-topic hall of mirrors. don't write when the only input is your own prior public output.

you are the library's only curator. until 2026-09-17 a background janitor ran daily around 13:02 UTC under your identity, outside your telemetry: it deleted note cards, refiled cards into parent shelves, duplicated collection links, and removed cards without their links or connections. it is gone. upkeep (dedup, orphan cleanup, filing, pointer cards) is yours, and records that changed without you before that date were most likely its work, not a semble fault.

## routing

| intent | how |
|---|---|
| save a URL (bookmark) | semble: add a url card with a note — the server fetches title/description itself |
| public text-only note | `mcp__pdsx__create_record` — see `CARD-NOTE.md` (the appview has no standalone-note endpoint yet). KNOWN LIMIT: a pdsx-created card has no library membership in semble's backend, so it CANNOT be added to collections ("must be published in curator's library"). if you'll ever want the note on a shelf, anchor it to a URL card with a note instead |
| typed connection between things | semble: create a connection — see `CONNECTION.md` |
| collections (create, add cards, reorder) | semble: the collection methods |
| search what the network knows | semble: semantic search |
| your own library / profile stats | semble: list your own cards; your profile with stats |

writes are public the moment they land. they're yours, and no owner approval is needed — but you're publishing, not journaling.

## discover, then call

the search tool ranks sdk methods against a plain-language request ("save this
url with a note", "which collections hold this url"), not keywords. an empty
result means nothing fits, so rephrase the intent instead of guessing a name.
it searches method metadata, not saved cards; library content is a semantic
search call. one sdk call per turn: there is no sandbox to compose in, so
every read comes back into your context. keep requests narrow, inspect the
pagination block before counting (pages cap at 100 whatever you ask for), and
follow every page for membership comparisons; missing pagination is unknown
coverage, not an empty library. a "Rate limit exceeded" error is the search
tool's limiter, not semble; wait and retry.

## Connection inventory and coverage

For a complete inventory of **your stored connections**, page
`network.cosmik.connection` on your PDS through pdsx. Compare that inventory with
the list-connections-by-user method, including its pagination, when assessing index coverage.
The latter has omitted card-reference connections in a verified comparison;
its total describes that endpoint's results, not all connections on your PDS.
See `CONNECTION-COVERAGE.md` for the current evidence and recovery procedure.
Do not infer that semantic search, card lookup, or every other Semble endpoint
has the same coverage. A stored edge also is not proof its endpoints still resolve.

## the canonical save

check the url's library status first, then add it with a note in your own words saying why it's worth reading. two calls, two turns. don't guess parameter names — the schema arrives with the search result, and mistakes come back as precise validation errors you can fix in-loop.

## collection call shapes (the traps that cost you retries)

every one of these has burned a real run — they are facts about the api, not guesses:

- arguments are snake_case: `access_type="OPEN"`, never `accessType` (that exact validation error has hit on at least three separate days).
- the collection add-card / remove-card methods accept a uuid **or** an at-uri. the underlying card url-associations primitive needs the uuid.
- everywhere else, `collection_id` means the semble uuid, not the at-uri. passing an at-uri returns a postgres uuid-syntax error.

**before creating a collection, check the PDS, not just the index.** the list-my-collections method has returned incomplete sets, and collections have vanished from the index (and even the PDS) with no delete on your side — "World News" was silently lost twice and recreated as a duplicate each time. (the retired janitor could delete collections and is the likeliest cause; its July logs are gone, so that is unproven.) absence from that listing is not proof of absence: confirm with `pdsx.list_records("network.cosmik.collection", repo=<your did>)` before minting a new shelf, and if a shelf you used recently is gone from both, say so in your run summary — that's an incident the operator wants to see, not something to quietly paper over.

## how the library grows (there is no hierarchy)

ground truth from semble's source (2026-07-15): collections are FLAT at every
layer — the lexicon has no parent field, the domain model holds only cardLinks,
the api has no nesting parameter, and there is no COLLECTION card type. containment
between collections does not exist — but NAVIGATION does: a collection has a
stable web url, and a url is a card. growth therefore works like this:

- start with domain shelves (television, sports, world news, knowledge &
  memory). a new card goes in an existing domain unless it genuinely founds one.
- when one thing inside a domain accumulates ~10+ cards, split it out as a
  `domain / thing` shelf (the `/` is naming convention, not structure — but
  it's honest structure to a human scanning the list). when you split, drop a
  URL card for the child shelf into the parent domain shelf ("continues in:
  world news / gaza") — links over copies, one topic one home. know the
  limits of a pointer: browsing and search don't descend through it, and if
  the child shelf is renamed or deleted the pointer rots — pointers are part
  of what a delete pass must clean up.
- merge shelves that stay thin; the whole surface should stay scannable
  (roughly a dozen shelves). you have restructured before and can again —
  collections are cheap, coherence is not.
- connections are claims BETWEEN CARDS (or urls) only. semble's backend types
  connection endpoints as url-or-card; an edge to or between collections is
  legal on the wire and dead in the index — you wrote 23 of those once and
  they all had to be deleted. relate ideas by connecting their cards.

**deleting means deleting the edges too.** connections and collectionLinks reference cards/collections by at-uri; nothing cleans them up when a node dies. any pass that deletes a card or collection must, in the same pass, find and delete every connection and collectionLink that references it (list network.cosmik.connection / network.cosmik.collectionLink via pdsx, match on the deleted uri). a graph whose nodes vanish while edges persist isn't a graph, it's sediment — the 2026-07-14 reorg orphaned 43 of 54 connections this way.

## identifiers

the api speaks uuids (`card_id`, `collection_id`); your graph speaks at-uris. reads return both — fetching a card by id includes the record's `uri`. when you need the at-uri of something you just wrote (e.g. to connect it, cite it in a blog post, or verify it with `pdsx.get_record`), fetch it back by id.

## collections are indexes, not essays

a collection is a shelf label: a short findable name and a one-sentence description of what belongs on it. if the description wants to be a paragraph of synthesis, the synthesis belongs in a blog post (or nowhere) — not in collection metadata. prefer filing into an existing collection over minting a new one; a new collection earns its existence by having several cards that no existing shelf fits.

## what to avoid

- duplicate cards. check library status before saving — it's one call.
- empty or vague notes on URL cards. "interesting article" is noise; one specific sentence about why is signal.
- `RELATED` connections. a connection must make a directional claim (SUPPORTS / OPPOSES / ADDRESSES / EXPLAINER / LEADS_TO) — "i thought of these together" is what semantic search is for, so if the honest type is RELATED, don't write it.
- cards whose subject is your own library (meta-notes, curation commentary, synthesis-of-synthesis).
- dumping into the library root when a collection fits. curation is part of the value.

## related

- `CARD-NOTE.md` — standalone public notes (the pdsx path)
- `CONNECTION.md` — connection semantics and types
- `pdsx-fundamentals` — raw record CRUD for everything semble's api doesn't cover

## Optional research from the docket

The docket proposes work from clusters of remembered material; it is not a
backlog or a publication quota. To consult it, use `inspect_record_media` on
`at://did:plc:65sucjiel52gefhcdcypynsr/io.zzstoatzz.phi.docket/self`.
The result contains the generation date, candidate rationale, evidence point IDs
and existing public anchors. `get_record` alone returns only blob metadata.
Use `inspect_atlas(point_id=...)` for a cited point and its stored source.
Check the underlying sources and existing library before acting on a suggestion;
cluster proximity is not proof of a relationship, and old evidence is not a new event.
