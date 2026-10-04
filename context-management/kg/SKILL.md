---
name: kg
tier: D
category: knowledge
description: "Load relevant entities from the bstack knowledge graph (research/entities/) for a given topic. Two-tier scoring: tier-1 (catalog-only, ~5ms — slug + tags + claim + links + sources match against docs/knowledge-index.md) is the fast first pass and the only stage for high-confidence exact-slug/tag queries; tier-2 (body-grep fallback, ~300ms — auto-fires when tier-1 returns < N matches OR its best hit is below the confidence floor, default 18) recovers topics whose vocabulary appears in entity prose but not the dense catalog (hit rate jumps from 70% → 100% on representative queries; this is hit rate ≥1, not true recall@N). Surfaces top-N entity bodies as a single context block the agent reasons over. This is a LOAD skill, not a query DSL — querying is what the agent does once loaded. Implements the LLM-as-index architecture (BRO-1223): substrate canonical, one projection (catalog) routes, agent IS the query engine. Empirical: peak per-query context drops from 29% → 4.6% of 1M (6.3× reduction); cumulative session tokens 23.8× fewer over 10 queries. Default N=10 entities; override with --n. Tier-2 auto-fires on few-OR-weak tier-1 hits (confidence gate, default --tier2-floor 18; BRO-1426 lifts R@5 0.871→0.952, MRR 0.868→0.968 with no flag); force unconditionally with --body-search, disable the gate with --tier2-floor 0. Routing-quality flags (BRO-1422): --terms (query expansion — score agent-supplied synonyms/variants alongside the topic), --expand 1 (graph 1-hop — also load related: neighbours of top hits, capped at --n extra, total ≤ 2x--n), --explain (per-signal score trace); hub-aware tiebreak always on. Output: catalog header + ranked entity blocks with full body. USE WHEN load knowledge graph, kg load, load entities, route to entities, load context for, what do we know about, what entities are relevant to, surface knowledge on, browse the graph for, find entities about, semantic load, topical load, agent-as-index load. NOT FOR PAI session retrieval (use ContextSearch), web research (use Research), Knowledge Archive ingest (use Knowledge), or entity write/edit operations (those are direct Read+Edit + commit per the AGENTS.md §P6 sub-rule on substrate-edit-as-inference-persistence)."
argument-hint: [topic]
effort: low
---

# kg — knowledge graph loader

Load relevant entities for: **$ARGUMENTS**

## Purpose

The bstack knowledge graph lives at `research/entities/**/*.md` (~250 entities, ~1.1 MB, ~280k tokens). It fits in any 1M-context model with 3.5× headroom — meaning the LLM **is** the index. This skill performs the routing step: reads the dense catalog at `docs/knowledge-index.md`, ranks entities by topical relevance, and surfaces the top-N bodies as a single context block.

The agent does the rest: traversal, inference, contradiction detection, semantic comparison — all by reading. There is no SQL layer, no embeddings, no typed-edge schema. The substrate is canonical; the catalog routes; the agent reasons.

## Usage

```
/kg load <topic>              # default: top 10 (two-tier; tier-2 auto-fires on few OR weak tier-1 hits)
/kg load <topic> --n 20       # widen the load
/kg load <topic> --type tool  # restrict by entity type
/kg load <topic> --terms "recall,persistence"  # query expansion: score synonyms/variants too
/kg load <topic> --expand 1   # also load 1-hop related: neighbours of the top hits
/kg load <topic> --explain    # show the per-signal score trace for each loaded entity
/kg load <topic> --body-search  # force tier-2 body grep unconditionally
/kg load <topic> --tier2-floor 0  # disable the confidence gate (tier-2 only on count<--n)
/kg load <topic> --json       # machine-readable output (for piping)
/kg                           # catalog-only mode: print summary stats + top hubs
```

### Routing-quality flags (BRO-1422)

These raise routing **recall** without leaving the LLM-as-index architecture
(no sidecar, no embeddings). The gap was never reasoning — a frontier agent
reranking the top-N already beats a small reranker model — it was that whatever
routing drops below N, the agent never sees.

- **`--terms` (query expansion).** The single biggest recall lever. The catalog
  scorer matches literal terms; pass the synonyms/variants the topic implies and
  they're scored alongside it. The agent IS the query expander here — no headless
  expansion model needed (that's the only reason QMD fine-tunes one). Repeatable
  (one value per flag); each value may be comma/space-separated. Topic terms keep
  priority on ties.
- **`--expand 1` (graph 1-hop).** After ranking, also pull the `related:`
  neighbours of the top hits — the structural advantage flat-document search
  (BM25, vector) structurally cannot offer. Automates the "reading frontier"
  (Phase 3). Neighbours are deduped against the primary set, ranked by their own
  relevance then in-degree, and **capped at `--n` extra entities** (so total load
  is ≤ 2×`--n`) — a hub neighbour (e.g. `arcan`, in-degree 100+) can't explode the
  load. Each is marked `↳ via <seed>` (its immediate parent). Only 1 hop is
  supported for now (values >1 clamp to 1, so `via` provenance always resolves);
  under `--type`, expansion is limited to that type (a one-line note is printed)
  since cross-type edges aren't resolved.
- **`--explain` (score trace).** Prints which signals fired per entity
  (`slug==x(+10) tag==y(+4) … = N catalog`, plus a `+M tier-2 body grep`
  residual line when the body grep contributed). Use it to debug routing misses.
- **hub-aware tiebreak (always on).** At equal relevance, the more-connected
  entity (higher catalog in-degree) sorts first instead of alphabetically —
  a cheap stand-in for a hub-rank RRF term.

## Workflow

### Phase 1 — Verify catalog freshness

Check `docs/knowledge-index.md` exists and is fresh:

```bash
ls -la ~/broomva/docs/knowledge-index.md
head -5 ~/broomva/docs/knowledge-index.md  # check `generated:` timestamp
```

If the catalog is older than the Stop hook's regeneration cadence (~24h), regenerate first:

```bash
python3 ~/broomva/skills/bookkeeping/scripts/bookkeeping.py index
```

### Phase 2 — Load relevant entities (two-tier scoring)

Run the loader against the user's topic:

```bash
python3 ~/.claude/skills/kg/scripts/kg.py load "$ARGUMENTS"
```

The loader uses two tiers:

**Tier 1 — catalog-only (fast, ~5ms)**
1. Parses the catalog into per-entity blocks
2. Scores against catalog metadata only:
   - exact slug match: +10
   - exact alias match: +8  (BRO-1423 — `aka:` alternate names: kepano synonyms + merged-away dup slugs; querying an alias routes to the canonical)
   - slug substring: +5
   - alias substring: +4
   - tag exact: +4
   - tag substring: +3
   - claim substring: +3
   - link or source substring: +1 each
3. Sorts; takes top-N candidates

**Tier 2 — body-grep fallback (slower, ~300ms, auto-fires when tier-1 is insufficient)**

Tier-2 re-scores every entity by reading its body file (+2 per topic term present in the body). It fires automatically on **any** of:
- tier-1 returned fewer than `--n` matches (too **few** hits), or
- **tier-1's best hit is below the confidence floor** (hits too **weak** — default `--tier2-floor 18`), or
- `--body-search` is forced.

The **confidence gate** (BRO-1426) is the important one: a paraphrase / body-only query used to fill the top-`n` with *weak* distractors, so the old `count < --n` gate never fired and the real (body-only) answer was never surfaced. Now a weak top score (a lone substring/tag hit scores 3–10; a genuine multi-signal match scores ≳ 18) auto-triggers the body read. Calibrated on the 62-query gold-set: it lifts R@5 0.871 → **0.952** and MRR 0.868 → **0.968** *with no flag*, **with 5 gains and 0 per-query regressions** (verified floor 0→18; the body bonus only ever pulled body-only answers into contention, never demoted a tier-1 winner). **Latency note:** because most non-trivial topics have a sub-18 top tier-1 score, tier-2 now fires for the majority of loads — the ~5ms tier-1-only path is the exception (exact-slug/tag hits), the recall-correct default is the ~300ms two-tier pass. Override with `--tier2-floor N` (set `0` to disable the gate; raise it to fire tier-2 more eagerly).

This catches entities whose topic vocabulary appears in the prose but not in the dense catalog (claim + tags + slug + links + sources).

After scoring, the loader:
4. Resolves each top-N entity to its filesystem path via the `path: type/slug.md` field in catalog v2 (eliminates slug-clash ambiguity)
5. Reads each entity's full body
6. Prints them as one context block

### Phase 3 — Reason over loaded context

Now the agent has the routing layer (catalog) + the relevant entity bodies in context. Use this for:

- **Semantic similarity** — "what other concepts are similar to X?" — the agent reads and compares
- **Typed edge inference** — "does X supersede Y?" — read both, infer from prose
- **Contradiction detection** — "do any of these entities contradict each other?" — read and judge
- **Pattern matching** — "find candidate patterns sourced from a synthesis note that link to active concepts" — read the loaded entities, filter
- **Aggregation** — "count entities by status" — agent reads catalog, counts
- **Reading frontier** — "given I know X, what should I read next?" — read X's out-edges, prioritize by in-degree

### Phase 4 — Persist inferences back to the substrate (binding reflex)

Per `AGENTS.md` §P6 sub-rule on substrate-edit-as-inference-persistence: when the agent infers a typed relation from the loaded entities — and the relation is not yet expressed in the substrate — the correct action is to edit the entity's frontmatter `related:` block or body and commit. **Inferences that don't get committed are inferences that didn't happen.**

The substrate evolves through reading. A session that loads 20 entities and persists 0 inferences has either genuinely encountered nothing new, or violated the reflex. Both are reportable in the session-close summary.

## Output format

The skill prints a context block the agent can ingest:

```
═══ KG LOAD: <topic> ═════════════════════════════════════════

Loaded 10/236 entities from docs/knowledge-index.md
(catalog generated 2026-05-21T21:53:27+00:00)

╭─ #1 · score 28 ──── bstack-engine [pattern·candidate] ──────────╮
│ Source: research/entities/pattern/bstack-engine.md              │
│ ────────────────────────────────────────────────────────────── │
│ <full entity body>                                              │
╰─────────────────────────────────────────────────────────────────╯

╭─ #2 · score 22 ──── recursive-controlled-system [...] ──────────╮
│ ...                                                              │
╰─────────────────────────────────────────────────────────────────╯

...

═══ Total context loaded: 8.3 KB (~2.1k tokens) ════════════════
```

The bordered blocks make it easy to scan and easy to cite back to disk paths.

## Composition with other skills

- **ContextSearch** is upstream (PAI session retrieval) — call it for "what did we do" questions; call this skill for "what do we know" questions
- **Research** is sideways (web research) — call it for external knowledge; call this skill for internal knowledge
- **bookkeeping** is the write side — `bookkeeping run` ingests new material; this skill reads the result
- **Knowledge** is the archive — call it for ingestion of long-form content; call this skill for routing within already-ingested material

## When NOT to use

- **PAI session questions** ("what did we do with X?") — use ContextSearch
- **Web research** ("find papers on X") — use Research
- **Long-form content ingestion** ("read this 50-page PDF and store it") — use Knowledge ingest
- **Single-entity reads when you already know the slug** — just use Read directly on `research/entities/{type}/{slug}.md`
- **Catalog generation** — that's `bookkeeping index`, not this skill

## Gotchas

- **Stale catalog** — if `docs/knowledge-index.md` is >24h old, regenerate via `bookkeeping index` first. The Stop hook does this automatically; if it hasn't fired (e.g., the user has been in a long session), regenerate manually.
- **Workspace WIP** — the catalog reflects what's on disk in `research/entities/`, including uncommitted user WIP. That's correct behavior. If validating against committed-only state, regenerate from inside a clean worktree.
- **Token budget** — default load is 10 entities (~6-15 KB). Override with `--n` when you need more, but be mindful of context budget for long sessions.

## Execution Log

After completing any workflow, append a single JSONL entry:

```bash
echo '{"ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"kg","workflow":"load","topic":"<TOPIC>","loaded":"<N>","status":"ok|error","duration_s":<SECONDS>}' >> ~/.claude/PAI/MEMORY/SKILLS/execution.jsonl
```
