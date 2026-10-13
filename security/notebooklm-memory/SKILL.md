---
name: notebooklm-memory
description: "Use to query, curate or audit Google NotebookLM research notebooks: market data, tech best practices, industry patterns. Modes QUERY, CURATE (add sources, create/tag notebooks), AUDIT (stale notebooks). Uses mcp__notebooklm-mcp__* tools and reads the notebook registry (if one exists) first."
---

# notebooklm-research

description: "Topic-based research library via Google NotebookLM MCP. Query curated domain notebooks for market data, tech best practices, and industry patterns. Three modes: QUERY (ask questions across notebooks), CURATE (add sources, create/tag notebooks), AUDIT (check source counts, surface stale notebooks). All operations use mcp__notebooklm-mcp__* MCP tools — no CLI. Registry-first: every operation starts by reading {agency-root}/memory/notebooklm-registry.md, if it exists."

> `{agency-root}` resolves to `$AGENCY_HOME`, else `$CLAUDE_CONFIG_DIR`, else the default Claude Code config directory — see `docs/HOOKS.md` for the exact resolution order.

## Activation

**Explicit:** User says "/notebooklm-memory", "/notebooklm-research", "query research notebooks", "add source to notebook", "create a research notebook"

**Intent detection:**
- "What does the research say about Vietnamese SMEs?"
- "Look up AI agent patterns in the notebooks"
- "Add this URL to the market research notebook"
- "Create a new research notebook for fintech"
- "How many sources are in the market notebook?"
- "What do we know about Supabase best practices?"

## Prerequisites

- NotebookLM MCP server running (`mcp__notebooklm-mcp__*` tools available)
- Authenticated via Google OAuth (your Google account)
- Registry at `{agency-root}/memory/notebooklm-registry.md`, if it exists (operator-accumulated — no template ships)

## Mode 1: QUERY — Ask Questions

Query curated research notebooks for grounded answers with citations.

### Single Notebook Query

1. Read `{agency-root}/memory/notebooklm-registry.md` (if it exists) to find the notebook slug and ID
2. Call `mcp__notebooklm-mcp__notebook_query` with the notebook ID and question
3. Return the answer with source citations

### Cross-Notebook Query

For questions spanning multiple domains:

1. By tag: `mcp__notebooklm-mcp__cross_notebook_query(tags=["vietnam", "sme"], query="...")`
2. All notebooks: `mcp__notebooklm-mcp__cross_notebook_query(all=true, query="...")`

### Query Tips

- Narrow queries outperform broad ones (NotebookLM uses RAG, not full re-read)
- Ask for citations: "Quote the exact sentence and cite the source"
- Ask for contradictions: "Do any sources disagree on this?"
- Ask for gaps: "What's missing from these sources on this topic?"

## Mode 2: CURATE — Manage Sources & Notebooks

### Add a Source

1. Read registry to get the notebook ID for the target slug
2. Check current source count (call `mcp__notebooklm-mcp__notebook_describe` or check registry)
3. If source count >= 45: warn the user and suggest archiving old sources first
4. Add the source:
   - URL: `mcp__notebooklm-mcp__source_add(source_type="url", url="https://...")`
   - Text: `mcp__notebooklm-mcp__source_add(source_type="text", text="...")`
   - Drive: `mcp__notebooklm-mcp__source_add(source_type="drive", document_id="...")`
   - File: `mcp__notebooklm-mcp__source_add(source_type="file", file_path="...")`
5. Update the source count in `notebooklm-registry.md`

### Create a New Notebook

1. `mcp__notebooklm-mcp__notebook_create(title="[CATEGORY] Full Title")`
   - Use prefix convention: `[MARKET]`, `[TECH]`, `[SALES]`, `[CONTENT]`, `[AI]`, `[OPS]`
2. Tag it: `mcp__notebooklm-mcp__tag(action="add", tags=["tag1", "tag2"])`
3. Seed with 5-10 initial sources (URL preferred)
4. Add entry to `{agency-root}/memory/notebooklm-registry.md` (create the file if it doesn't exist yet):
   - slug, notebook_id, title, tags, source count, project dependencies
5. Update `Last updated` date in registry

### Source Selection Guidelines

| Priority | Source Type | Example |
|----------|-----------|---------|
| Highest | Industry reports, government data (URL) | GSO Vietnam, e-Conomy SEA report |
| High | Official documentation (URL) | Next.js docs, Supabase docs |
| High | Research papers, whitepapers (URL) | Academic papers, policy documents |
| Medium | Curated blog posts, case studies (URL) | Vetted quality articles |
| Medium | Internal synthesis docs (text) | Audience profiles, research summaries |
| Avoid | Session logs, decisions.md, code files | These belong in graphify/Pinecone |

## Mode 3: AUDIT — Check Notebook Health

### Quick Health Check

1. Read `{agency-root}/memory/notebooklm-registry.md`, if it exists
2. For each active notebook:
   - Call `mcp__notebooklm-mcp__notebook_describe` to verify it exists and get current state
   - Compare source count against the 45-source soft limit
   - Flag notebooks approaching the limit
3. Report: slug, title, source count, status (healthy / near-limit / stale)

### Source Freshness Audit

1. For each notebook, call `mcp__notebooklm-mcp__source_add` with `source_type="list"` or check source metadata
2. Flag sources older than the notebook's refresh cadence:
   - AI/ML notebooks: monthly refresh
   - Market notebooks: quarterly refresh
   - Tech stack notebooks: semi-annual refresh
3. Recommend: which sources to refresh (re-add URL) or archive

## Integration with Curator Agent

The curator agent (`{agency-root}/agents/specialized/curator.md`) uses NotebookLM as L2.5 in its retrieval protocol. When a PD spawns a curator with a domain-level question (market research, tech best practices, industry patterns), the curator:

1. Reads the registry to find relevant notebooks
2. Matches question domain to notebook tags
3. Queries via `mcp__notebooklm-mcp__notebook_query`
4. Returns answer with NotebookLM source citations

This skill is for direct human-invoked operations. The curator handles agent-to-agent queries autonomously.

## Autonomy Rules

**Auto-approve (no confirmation needed):**
- `notebook_query`, `cross_notebook_query` — reads
- `notebook_list`, `notebook_describe` — reads
- `notebook_get` — reads
- `source_describe`, `source_get_content` — reads
- `tag(action="list")` — reads
- Reading `notebooklm-registry.md` — reads

**Require user confirmation:**
- `notebook_create` — creates new notebook
- `source_add` — modifies notebook content
- `notebook_delete` — destructive
- `source_delete` — destructive
- `tag(action="add")`, `tag(action="remove")` — modifies organization
- `studio_create` — long-running generation
- `notebook_share_*` — exposes content externally

## Relationship to Other Systems

| Layer | Tool | Purpose |
|-------|------|---------|
| Project structure | graphify (L1-L2) | Code relationships, project knowledge graph |
| Curated research | NotebookLM (L2.5) | Domain knowledge — markets, tech, industry |
| Semantic search | Pinecone (L3) | Broad vector search across all indexed content |
| Raw files | Read tool (L4) | Direct file access — decisions.md, lessons/, heartbeat |

NotebookLM does NOT replace any existing layer. It fills the gap between project-structural knowledge (graphify) and broad semantic search (Pinecone) with curated, citation-grounded domain research.
