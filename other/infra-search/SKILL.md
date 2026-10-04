---
name: infra-search
description: Manage AICP's search surfaces — KB semantic search (LocalAI Collections + nomic-embed embeddings + bge-reranker reranking via `aicp --kb search` and `aicp_kb_search_collection` MCP), source code search (Grep/Glob via Claude Code), wiki page search (`python3 -m tools.view search` from second brain). AICP has no Elasticsearch/Solr — semantic search is LocalAI-Collections-backed; lexical search is Grep-backed. Loads when the operator says "set up search" / "tune embedding search" / "rerank results" / "why are search results wrong" / "add a new search surface".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: low
---

# infra-search

Manage AICP's search surfaces. AICP exposes 3 distinct search shapes:

1. **Semantic search** (KB) — LocalAI Collections at
   `localhost:8090/app/collections`, embedded via nomic-embed, reranked
   via bge-reranker-v2-m3. Accessed via `aicp --kb search` CLI or
   `aicp_kb_search_collection` MCP tool (Category B KEEP per audit).
2. **Source code search** — Grep + Glob (ripgrep-backed via Claude Code
   tool). No code-specific index; treesitter parsing happens via
   `claude-mem:smart-explore` skill.
3. **Wiki page search** — second brain's `python3 -m tools.view search
   <query>` CLI (project-internal lexical search across wiki/).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: "set up search", "tune embedding search", "rerank
  results", "why are search results wrong", "add a new search surface"
- **KB tuning**: chunking strategy, top_k, threshold values, reranker
  on/off
- **Code-aware search**: when grep is too coarse and operator wants
  structural/semantic — load `claude-mem:smart-explore` instead
- **Multi-store search**: searching across KB + wiki + code in one query

Do NOT load when:

- The concern is the KB ingestion lifecycle (load `infra-storage` for
  KB persistence, `aicp --kb add` for the runtime workflow)
- The concern is monitoring KB health (load `infra-monitoring`)
- The concern is Mission Control's web search UI (separate project)

## Operations

### Operation 1 — Tune semantic search relevance

**When**: KB search returns irrelevant or missing results.

**Process**:

1. Inspect current settings in `config/default.yaml` `rag:` section:
   - `top_k` (default 5) — how many results to retrieve before reranking
   - `chunk_size` / `chunk_overlap` — how source text is split for embedding
   - `threshold` — minimum cosine similarity to consider a match
   - `rerank: true/false` — apply bge-reranker re-scoring
   - `max_context_chars` — RAG context budget passed to the LLM
2. Common failure modes:
   - Missing relevant chunks → lower `threshold`, increase `top_k`,
     decrease `chunk_size` (more granular)
   - Off-topic results → enable rerank, raise `threshold`
   - Truncated results → increase `max_context_chars` (within KB context window)
3. Re-run `aicp --kb search --kb-arg "<query>"` after each tune
4. For systematic tuning, use a test query set (operator-provided) and
   measure precision/recall

**Quality bar**: NEVER tune without a baseline measurement. Tune one
parameter at a time so you can attribute the effect.

### Operation 2 — Add a new search surface

**When**: AICP needs to search a new content type (e.g., GitHub issues,
external docs, log files).

**Process**:

1. Decide indexing strategy:
   - **Embed into existing aicp-kb collection** (preferred) — `aicp --kb
     add --kb-arg <path>` for files
   - **New LocalAI collection** for isolated storage —
     `localhost:8090/app/collections/{new-collection}`
   - **External index** (e.g., GitHub API direct query) — no embed,
     fetch on demand
2. For embedded surfaces: add ingestion command in `aicp/cli/main.py`
   if not already covered by `--kb add`
3. For query: extend `aicp --kb search` with `--kb-arg2 <collection-name>`
   if multi-collection becomes a frequent need
4. Document the new surface in CLAUDE.md `## Knowledge Base` or wiki

**Quality bar**: PREFER extending the existing collection over creating
new ones — multi-collection search increases query complexity.

### Operation 3 — Diagnose search quality

**When**: operator reports unexpected ranking.

**Process**:

1. Reproduce: `aicp --kb search --kb-arg "<query>"` (with rerank on)
2. Look at the top results' source paths — are they ON-TOPIC?
3. If off-topic: re-embed the source (chunking may have split awkwardly)
4. If missing topical content: verify ingestion (`aicp --kb list` shows
   sources)
5. Check reranker score distribution — large gaps signal weak reranking
6. Fall back to grep for sanity check: `Grep "<keyword>" wiki/` —
   does the term even exist in the corpus?

**Quality bar**: search quality is multi-causal (chunking + embedding
+ reranking + threshold). Diagnose one layer at a time.

## Gotchas

- **Detection**: agent assumes AICP uses Elasticsearch.
  **Rule**: AICP uses LocalAI Collections (chromem-backed). No Elasticsearch.
  **Reasoning**: setting expectations correctly avoids time wasted on
  nonexistent infrastructure.

- **Detection**: agent recommends raising `top_k` to 100 to "find more results".
  **Rule**: top_k > 20 typically degrades quality (reranker can't sort 100 items
  well; LLM context fills with noise).
  **Reasoning**: search is precision-first; flooding with low-quality
  matches dilutes the LLM's RAG context.

- **Detection**: agent disables reranker to "speed up search".
  **Rule**: reranker adds <500ms typically; the quality lift is large.
  Disable only with measured evidence the latency matters more.
  **Reasoning**: bge-reranker meaningfully improves precision; the cost
  is rarely the bottleneck for operator-driven queries.

- **Detection**: agent embeds large binary files into KB.
  **Rule**: KB is for TEXT. Binary embedding produces nonsense vectors.
  Skip / convert to text first.
  **Reasoning**: nomic-embed expects text input; binary bytes embed to
  random-ish vectors that pollute results.

## Reference exemplars

- `aicp/core/kb.py` — KB query implementation (search + augment)
- `aicp/core/rag.py` — RAG pipeline + chunker
- `aicp/cli/main.py` `_run_kb()` — `--kb` CLI dispatcher
- `config/default.yaml` `rag:` section — tunable parameters
- `wiki/decisions/01_drafts/4-tier-router-with-profiles-over-hardcoded-routing.md` —
  router that uses RAG context

## Domain context

AICP's KB is the operational knowledge store: ingested via `aicp --kb
add`, queried via `aicp --kb search` or `--rag` flag, persisted in
LocalAI Collections (per `infra-storage` skill). The search pipeline is
embed → similarity → rerank → LLM-context. Precision matters more than
recall for inference quality (per the autocomplete-chain lesson — better
to retrieve nothing than to retrieve wrong context).

## Related skills

| Skill | When to use |
|-------|-------------|
| `infra-storage` | When the concern is KB persistence (Collections directory) |
| `infra-monitoring` | When alerting on KB query rate / latency |
| `quality-performance` | When measuring KB query latency under load |
| `claude-mem:smart-explore` | When code-aware search is needed (treesitter, AST) |
