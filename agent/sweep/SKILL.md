---
name: sweep
description: Cross-company language sweep via Quartr full-text search — date the adoption curve of a term/phrase across the global transcript+filing corpus, identify which companies (and which speaker roles) use it and when they started, and cross-reference against vault theses and graph adjacency to flag terms propagating through supply chains the book owns. Use when user says "sweep", "who is talking about X", "language scan", "adoption curve for X", or "is X inflecting".
model: opus
effort: max
allowed-tools: Read Grep Glob Edit Write ToolSearch mcp__quartr Bash(date * jq * ls * cat * grep * printf * wc *)
---

The mechanised version of the vault's core mandate: connect optically insignificant datapoints to macro-level shifts. Corporate language is a leading indicator — managements adopt a term (`capacity auction`, `asset light`, `inventory digestion`, `agentic`) before the economics it names show up in reported numbers, and when several companies along one value chain adopt it within a few months, a schelling point is forming ([G-3]). This skill dates that curve from primary sources and names the adopters, producing an immutable Research note.

**What the tool can and cannot do (probe-validated 2026-09-09):**
- `search_documents` returns `totalCount` + company/event/document pointers per date window — but **no snippets** (`text: null`). The sweep therefore has a hard two-stage structure: search finds WHERE, summaries/deep reads establish HOW the term is used. No usage claim is ever made from a hit-list alone.
- The `documentTypes` filter is loosely honoured (transcript queries return slide hits) — always read each hit's actual `documentType`.
- **Query syntax is fragile in compounds**: an exact phrase AND'd with an extra term can silently 0-hit while each part alone returns hundreds. Keep queries to a single term or a single backtick-quoted phrase; express restrictions via the `filter` parameter (GICS, country, `speaker.role`, companyId), never via extra query words. A 0-hit result on a term you know exists means the query is malformed — simplify and retry once before trusting it.
- **Terms have prior language communities.** Validated live: "capacity auction" ran 45 hits in Jun-Sep 2025 vs 21 in Jun-Sep 2026 — a naive read says the term is dying, but the 2025 base is utilities (RWE, Constellation, Alliant: electricity capacity auctions), and the real signal is Nebius entering that community in 2026 with a new meaning. Raw counts track the blended series; the adoption read requires **segmenting the curve by GICS** and tracking community composition, not volume.

## Arguments

`/sweep "<term>"` plus optional flags:
- `--since YYYY-MM-DD` — curve start (default 24 months back)
- `--gics "<GICS name>"` — segment/restrict to an industry (repeatable up to 2; e.g. `"Information Technology"` at level 1, `"Semiconductor Materials and Equipment"` at level 3/4)
- `--country XX` — ISO country filter
- `--role CEO|CFO|Analyst` — transcript speaker-role filter (who says it matters: CEO adoption ≠ analyst questioning)
- `--types transcripts,slides,reports` — default `transcripts,slides`
- `--portfolio` — restrict to the Vault Active watchlist companyIds (from `.data/quartr_watchlist.json`)

Multi-word input without quotes → treat as an exact phrase. Multiple unrelated terms → ask the user to run separate sweeps (comparability of one curve is the product; blended queries are uninterpretable).

## Step 0: Pre-flight

1. **Lock**: `vault-wide` per `_shared/preflight.md` Procedure 1, timeout 10 min (writes one Research note; reads theses + graph).
2. **Quartr probe** (hard): per `_shared/quartr.md` §1 load `search_documents,get_document_summary,get_event_summary,list_companies`. Unavailable → abort (`❌ /sweep has no fallback source`).
3. **Mental models (analytical tier — this skill renders judgements)**: read `[[Generalist - Overview]]` always; the matching `Industry -` / `Lens -` file(s) when `--gics`/the term's obvious domain puts a covered sector in play. Apply the READING PROTOCOL: an adoption curve that flatters an existing thesis is a disconfirmation trigger, not a victory lap.
4. Read `_graph.md` (adjacency primer per `_shared/graph-primer.md`) and `.data/quartr_ids.json` (build the reverse map companyId→vault ticker) in the same batch.

## Step 1: Adoption curve (bounded window scan)

Bucket the lookback into windows: **monthly for ≤12 months, quarterly beyond** (cap: 14 window queries). Per window:

```
mcp__quartr__search_documents {query: "`<term>`", documentTypes: [...], startDate, endDate, limit: 1}
```

`totalCount` is the datapoint; `limit: 1` keeps responses tiny. When `--gics`/`--country`/`--role` is set, pass it via `filter` (e.g. `gics.level1:=["Information Technology"]`, `speaker.role:=[CEO]`). **When the term shows cross-industry usage** (Step 2 reveals a mixed community), re-run the LAST 6 windows with the target-industry filter to produce the segmented curve (cap: +6 queries) — the segmented series is the one the note leads with; the blended series is context.

Curve shape readings (hypotheses, not verdicts): sustained acceleration = diffusion; a step-function = one event echoing (check whether hits cluster on one company's reporting week); flat-high = established vocabulary, no inflection signal; decline in blended + rise in segmented = community handoff (the validated capacity-auction case).

## Step 2: Who — the language community

One discovery query on the most recent window at `limit: 100` (+1 page if totalCount > 100 and the run is unfiltered). Group hits by company; record documentType (verified per hit), event, date. Then:

- **First-mention dating** for the most thesis-relevant companies (vault names, graph-adjacent names, repeated hitters): per company, `filter: "companyId:=[<id>]"` with a wide date range, `order` implied by windowing — bisect with at most 2 windows per company to date their earliest use. **Cap: 6 companies.**
- **Role composition** when `--role` unset but transcripts dominate: one extra query with `speaker.role:=[CEO]` on the latest window — CEO-mouth adoption is the strong form of the signal.

## Step 3: Vault cross-reference

Map hit companyIds → vault tickers (reverse ID map; unmapped hit companies are looked up by name against thesis/watchlist names before being declared outside-vault). Then against `_graph.md`:

- **Adjacency propagation flag** (the payoff): ≥2 companies that are graph-adjacent (same cluster, shared supplier/customer edges) adopting the term within a 2-quarter span → flag as a candidate schelling point, naming the chain and the implicated theses.
- Term present in hit companies but ABSENT from the vault's own thesis/sector vocabulary (grep the implicated notes) → vocabulary gap: the market is naming something the vault hasn't framed yet.
- Inverse check: the vault uses the term but the corpus barely does → the vault may be early (good) or idiosyncratic (check which, via Step 4 context).

## Step 4: Context verification (the two-stage rule)

For the **top ≤5 most load-bearing hits** (by thesis-relevance, then recency): `get_event_summary` (events) or `get_document_summary` (documents) to establish how the term is actually used — new meaning vs incumbent meaning, offensive vs defensive framing, management-initiated vs analyst-prompted. A hit whose summary is null and whose usage matters → note it as unverified and recommend `/transcript TICKER --event <id>`; never guess. No figure or usage claim enters the Evidence section without this layer or a deep read behind it.

## Step 5: Write the Research note

`Research/YYYY-MM-DD - Sweep [term] - data.md` — immutable record per Research-note conventions. Frontmatter: `date`, `tags: [research, data, sweep + implicated tickers/sector tags]`, `status: active`, `source: Quartr search_documents corpus sweep — query "<term>", windows <start>..<end>`, `source_type: data`, `publish` omitted (Research notes don't carry it).

Body (all 4 required sections):
- `## Thesis Delta` — which theses the curve touches and how (hypothesis language; trigger touches flagged per `_shared/trigger-touch.md` discipline — flag, never auto-action)
- `## Summary` — the curve's shape and the community's composition shift, led by the segmented series; the mechanism the term names; what adoption timing implies
- `## Evidence` — the curve table (window | blended count | segmented count), the adopter table (company | vault link/outside | first mention | role | verified context), each verified usage tagged `[Quartr]` with its deep link
- `## Contradiction Check` — the strongest mundane explanation (reporting-calendar clustering, one-event echo, incumbent-industry base rate, Quartr coverage growth inflating late-period counts — state this one explicitly every time, since corpus size is not constant over the lookback)
- `## Source Excerpts` — the ≤5 verified usages, quoted short with links

Wikilink implicated theses/sectors. No thesis Log writes (multi-thesis fanout is `/sync`'s job — the note's links make it discoverable); remind the user to run `/graph last`.

## Step 6: Release lock + report

Stats line (windows, total hits, community size, vault overlap), the curve in miniature, the adjacency-propagation flags, the deep-read queue, and suggested follow-ups (`/transcript --event`, `/deepen`, `/monitor` if the term deserves a standing alert).

## Design constraints (xxx DO NOT VIOLATE xxx)

1. **Counts are hypotheses.** Every curve reading ships with its mundane alternative (Contradiction Check). Corpus-growth inflation is stated in every note.
2. **Community composition beats volume.** A blended count is never presented without the who — the validated failure mode is reading a community handoff as a decline.
3. **Two-stage always.** Hits carry no snippets; usage claims require the summary/deep-read layer. No exceptions for "obvious" terms.
4. **Simple queries only.** One term or one exact phrase; restrictions go in `filter`. On unexpected 0-hits, simplify once, then report the anomaly rather than working around it with compound guesses.
5. **Bounded budget.** ≤14 curve + ≤6 segmented + ≤2 discovery + ≤12 first-mention + ≤5 summary calls per run. A sweep that wants more is two sweeps.
6. **No thesis writes.** One immutable Research note; propagation stays with `/sync`, conviction with `/status`.
