---
name: llm-wiki
description: "Karpathy's LLM Wiki — build and maintain a persistent, interlinked markdown knowledge base. Ingest sources, query compiled knowledge, and lint for consistency."
version: 3.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wiki, knowledge-base, research, notes, markdown, rag-alternative, batch-ingest]
    category: research
    related_skills: [obsidian, arxiv, agentic-research-ideas]
    config:
      - key: wiki.path
        description: Path to the LLM Wiki knowledge base directory
        default: "~/wiki"
        prompt: Wiki directory path
---

# Karpathy's LLM Wiki

Build and maintain a persistent, compounding knowledge base as interlinked markdown files.
Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Unlike traditional RAG (which rediscovers knowledge from scratch per query), the wiki
compiles knowledge once and keeps it current. Cross-references are already there.
Contradictions have already been flagged. Synthesis reflects everything ingested.

**Division of labor:** The human curates sources and directs analysis. The agent
summarizes, cross-references, files, and maintains consistency.

## When This Skill Activates

Use this skill when the user:
- Asks to create, build, or start a wiki or knowledge base
- Asks to ingest, add, or process a source into their wiki
- Asks a question and an existing wiki is present at the configured path
- Asks to lint, audit, or health-check their wiki
- References their wiki, knowledge base, or "notes" in a research context
- Wants to batch-ingest hundreds/thousands of documents into wiki format

## Wiki Location

Configured via `skills.config.wiki.path` in `~/.hermes/config.yaml` (prompted
during `hermes config migrate` or `hermes setup`):

```yaml
skills:
  config:
    wiki:
      path: ~/wiki
```

Falls back to `~/wiki` default. The resolved path is injected when this
skill loads — check the `[Skill config: ...]` block above for the active value.

Before setting `wiki.path`, verify the target actually exists. A stale default like
`~/wiki` is easy to leave behind even when the real wiki lives elsewhere.

For the workspace-hub multi-wiki layout, the preferred root is usually:

```yaml
skills:
  config:
    wiki:
      path: /mnt/local-analysis/workspace-hub/knowledge/wikis
```

This points at the domain-wiki root (`engineering/`, `marine-engineering/`,
`maritime-law/`, `naval-architecture/`, etc.) rather than a single flat `~/wiki`
folder.

The wiki is just a directory of markdown files — open it in Obsidian, VS Code, or
any editor. No database, no special tooling required.

## CLI Tool (workspace-hub)

The `llm-wiki` CLI at `scripts/knowledge/llm_wiki.py` provides 6 commands for
operating wikis programmatically. All commands use the pattern:

```bash
uv run scripts/knowledge/llm_wiki.py <command> --wiki <domain>
```

| Command | Purpose |
|---------|---------|
| `init <domain>` | Scaffold a new domain wiki under `knowledge/wikis/<domain>/` |
| `status --wiki <d>` | Report page counts, source counts, link density |
| `ingest <file> --wiki <d>` | Copy source file + generate LLM processing instructions |
| `query "..." --wiki <d>` | Keyword search across wiki pages with relevance ranking |
| `lint --wiki <d>` | Health checks (orphans, empty pages, index consistency, link density) |
| `batch-ingest <file> --wiki <d> --batch-size N` | Bulk-create source pages from metadata JSONL/JSON/YAML |

**batch-ingest** is designed for scale:
- Checkpoint-based resume (`.checkpoint.jsonl` in wiki root)
- `--dry-run` for preview
- Progress reporting every batch
- Skips already-processed records
- Used to ingest 22K conference papers → 12K source pages in one run
- Proven: 100 records/batch, ~400 records per 10 seconds

Location: `knowledge/wikis/<domain>/` (not `~/wiki`). This is a multi-wiki
ecosystem — multiple domain wikis coexist under `knowledge/wikis/`. Force-add
to git despite `.gitignore` since wiki content is the compounding artifact.

## Architecture

### Multi-Wiki Pattern

In workspace-hub, wikis are organized as a multi-domain ecosystem under
`knowledge/wikis/<domain>/`, not a single `~/wiki`. Each domain
(marine-engineering, maritime-law, naval-architecture) has its own
complete three-layer structure. Cross-wiki linking connects related topics
across domains.

### Three Layers (per domain wiki)

```
knowledge/wikis/<domain>/
├── AGENTS.md             # Schema: conventions, structure rules, domain config
├── raw/                  # Layer 1: Immutable source material
│   ├── papers/           # PDFs, standards, papers
│   ├── standards/        # Standards documents
│   ├── articles/         # Web articles, clippings
│   └── assets/           # Images, diagrams
└── wiki/                 # Layer 2: The LLM-maintained wiki
    ├── index.md          # Content catalog with sectioned entries
    ├── log.md            # Chronological action log (append-only)
    ├── overview.md       # Domain synthesis summary
    ├── entities/         # Entity pages (things: equipment, orgs, vessels)
    ├── concepts/         # Concept pages (ideas: methods, principles)
    ├── sources/          # Source summary pages (one per ingested document)
    ├── comparisons/      # Filed query outputs
    └── visualizations/   # matplotlib plots, Marp slide decks
```

**Layer 1 — Raw Sources:** Immutable. The agent reads but never modifies these.
**Layer 2 — The Wiki:** Agent-owned markdown files. Created, updated, and
cross-referenced by the agent.
**Layer 3 — The Schema:** `AGENTS.md` defines structure, conventions, and tag taxonomy.

### Scaling Pattern (learned from 12K+ source ingestion)

- **Metadata-first approach**: Don't extract PDF content (hits 5-min timeouts on
  large files). Instead, read structured metadata (titles, topics, sizes) and
  create wiki source pages.
- **Proven at scale**: 22K conference metadata records → 12K unique source pages,
  skipping 10K+ duplicates via checkpoint file.
- **Batch size**: 100 records per batch, progress reported every batch.
- **Checkpoint resume**: `.checkpoint.jsonl` tracks processed records by unique ID.
- **Index management**: Updates index.md after each batch, not after every record.
- **Git considerations**: Wiki pages must be force-added (`git add -f`) even if
  `.gitignore` excludes the wikis directory. Wiki content is the compounding artifact.
- **Workspace-hub hook gotcha**: `knowledge/wikis/<domain>/AGENTS.md` files are wiki schema/config files generated by `llm-wiki init`, not harness adapter files. If the repo hook `.Codex/hooks/check-Codex-md-limits.sh` applies the 20-line harness limit to all `AGENTS.md` paths, commits touching wiki `AGENTS.md` can fail with a false positive. The minimal safe fix is to exclude `^knowledge/wikis/` from that hook's staged-file filter so harness limits still apply to real adapter files while wiki schema files remain editable.

## Resuming an Existing Wiki (CRITICAL — do this every session)

When the user has an existing wiki, **always orient yourself before doing anything**:

① **Read `AGENTS.md`** (or `SCHEMA.md`) — understand the domain, conventions, and tag taxonomy.
② **Read `index.md`** — learn what pages exist and their summaries.
③ **Scan recent `log.md`** — read the last 20-30 entries to understand recent activity.

```bash
WIKI="${wiki_path:-$HOME/wiki}"
# Orientation reads at session start
read_file "$WIKI/SCHEMA.md"
read_file "$WIKI/index.md"
read_file "$WIKI/log.md" offset=<last 30 lines>
```

Only after orientation should you ingest, query, or lint. This prevents:
- Creating duplicate pages for entities that already exist
- Missing cross-references to existing content
- Contradicting the schema's conventions
- Repeating work already logged

For large wikis (100+ pages), also run a quick `search_files` for the topic
at hand before creating anything new.

## Initializing a New Wiki (via CLI)

```bash
uv run scripts/knowledge/llm_wiki.py init <domain>
```

This scaffolds the full three-layer structure, creates `AGENTS.md` with
domain-specific schema, initializes `index.md` and `log.md`, and creates
the `raw/` and `wiki/` subdirectories.

After scaffolding:
1. Add some sources: `ingest <file> --wiki <domain>`
2. For bulk: `batch-ingest metadata.jsonl --wiki <domain> --batch-size 100`
3. Check health: `lint --wiki <domain>`

## Core Operations

### 1. Ingest

When the user provides a source (URL, file, paste), integrate it into the wiki:

① **Capture the raw source:**
   - URL → use `web_extract` to get markdown, save to `raw/articles/`
   - PDF → use `web_extract` (handles PDFs), save to `raw/papers/`
   - Pasted text → save to appropriate `raw/` subdirectory
   - Name the file descriptively: `raw/articles/karpathy-llm-wiki-2026.md`

② **Discuss takeaways** with the user — what's interesting, what matters for
   the domain. (Skip this in automated/cron contexts — proceed directly.)

③ **Check what already exists** — search index.md and use `search_files` to find
   existing pages for mentioned entities/concepts. This is the difference between
   a growing wiki and a pile of duplicates.

④ **Write or update wiki pages:**
   - **New entities/concepts:** Create pages only if they meet the Page Thresholds
     in SCHEMA.md (2+ source mentions, or central to one source)
   - **Existing pages:** Add new information, update facts, bump `updated` date.
     When new info contradicts existing content, follow the Update Policy.
   - **Cross-reference:** Every new or updated page must link to at least 2 other
     pages via `[[wikilinks]]`. Check that existing pages link back.
   - **Tags:** Only use tags from the taxonomy in SCHEMA.md

⑤ **Update navigation:**
   - Add new pages to `index.md` under the correct section, alphabetically
   - Update the "Total pages" count and "Last updated" date in index header
   - Append to `log.md`: `## [YYYY-MM-DD] ingest | Source Title`
   - List every file created or updated in the log entry

⑥ **Report what changed** — list every file created or updated to the user.

A single source can trigger updates across 5-15 wiki pages. This is normal
and desired — it's the compounding effect.

### 2. Query

When the user asks a question about the wiki's domain:

① **Read `index.md`** to identify relevant pages.
② **For wikis with 100+ pages**, also `search_files` across all `.md` files
   for key terms — the index alone may miss relevant content.
③ **Read the relevant pages** using `read_file`.
④ **Synthesize an answer** from the compiled knowledge. Cite the wiki pages
   you drew from: "Based on [[page-a]] and [[page-b]]..."
⑤ **File valuable answers back** — if the answer is a substantial comparison,
   deep dive, or novel synthesis, create a page in `queries/` or `comparisons/`.
   Don't file trivial lookups — only answers that would be painful to re-derive.
⑥ **Update log.md** with the query and whether it was filed.

### 3. Lint

When the user asks to lint, health-check, or audit the wiki:

① **Orphan pages:** Find pages with no inbound `[[wikilinks]]` from other pages.
```python
# Use execute_code for this — programmatic scan across all wiki pages
# Scan all .md files in entities/, concepts/, comparisons/, queries/
# Extract all [[wikilinks]] — build inbound link map
# Pages with zero inbound links are orphans
```

② **Broken wikilinks:** Find `[[links]]` that point to pages that don't exist.

③ **Index completeness:** Every wiki page should appear in `index.md`. Compare
   the filesystem against index entries.

④ **Frontmatter validation:** Every wiki page must have all required fields
   (title, created, updated, type, tags, sources). Tags must be in the taxonomy.

⑤ **Stale content:** Pages whose `updated` date is >90 days older than the most
   recent source that mentions the same entities.

⑥ **Contradictions:** Pages on the same topic with conflicting claims. Look for
   pages that share tags/entities but state different facts.

⑦ **Page size:** Flag pages over 200 lines — candidates for splitting.

⑧ **Tag audit:** List all tags in use, flag any not in the SCHEMA.md taxonomy.

⑨ **Log rotation:** If log.md exceeds 500 entries, rotate it.

⑩ **Report findings** with specific file paths and suggested actions, grouped by
   severity (broken links > orphans > stale content > style issues).

⑪ **Append to log.md:** `## [YYYY-MM-DD] lint | N issues found`

### 4. Bulk Ingest (CLI-based)

For large-scale ingestion (100+ sources), use the `llm-wiki batch-ingest` CLI:

```bash
# Dry-run first to preview
uv run scripts/knowledge/llm_wiki.py batch-ingest metadata.jsonl --wiki <domain> --batch-size 100 --dry-run

# Then run for real (resume-safe via .checkpoint.jsonl)
uv run scripts/knowledge/llm_wiki.py batch-ingest metadata.jsonl --wiki <domain> --batch-size 100
```

The CLI handles:
- ✅ Checkpoint-based resume (safe to interrupt/restart)
- ✅ Progress reporting every batch — 100 records per batch at ~400 records per 10s
- ✅ Skip already-processed records (10K+ duplicates in a 22K run)
- ✅ Batch index.md/log.md updates (efficient)
- ✅ `--dry-run` mode to preview filenames and counts

### 5. Seed Migration (YAML → Wiki)

For structured YAML knowledge seeds in `knowledge/seeds/`:

1. Parse the YAML to extract entries
2. Group entries by domain/category
3. For each entry: create entity/concept/source page
4. Cross-link with existing wiki pages
5. Update index.md with all migrated entries
6. Append structured entries to log.md

Proven pattern: 18 mooring failure entries → 4 wiki pages (source + 2 concepts + 1 entity)
                10 law cases + 6 conventions → 20 wiki pages with cross-references

## Working with the Wiki

### Searching

```bash
# Find pages by content
search_files "transformer" path="$WIKI" file_glob="*.md"

# Find pages by filename
search_files "*.md" target="files" path="$WIKI"

# Find pages by tag
search_files "tags:.*alignment" path="$WIKI" file_glob="*.md"

# Recent activity
read_file "$WIKI/log.md" offset=<last 20 lines>
```

### Seed Migration Pattern

For structured YAML seeds (like `knowledge/seeds/naval-architecture-resources.yaml`):

1. **Parse YAML categories** (textbooks, hydrostatics, portals, ship plans, etc.)
2. **Create concept pages** for each major topic domain (5-6 pages)
3. **Create source pages** for each individual resource (17-36 pages per seed)
4. **Update index.md** with structured tables
5. **Update log.md** with migration entry

This approach is much faster than full PDF extraction and creates structured
wiki pages that can be enhanced later with LLM content.

### Cross-Wiki Linking

When managing multiple domain wikis, look for natural connections:
- Deepwater Horizon → marine-engineering (lng-carrier-mooring) + maritime-law (OPA 90)
- Mooring failures → marine-eng + naval-arch stability concepts
- Classification rules → naval-arch + maritime-law liability conventions

## Obsidian Integration

The wiki directory works as an Obsidian vault out of the box:
- `[[wikilinks]]` render as clickable links
- Graph View visualizes the knowledge network
- YAML frontmatter powers Dataview queries
- The `raw/assets/` folder holds images referenced via `![[image.png]]`

For best results:
- Set Obsidian's attachment folder to `raw/assets/`
- Enable "Wikilinks" in Obsidian settings (usually on by default)
- Install Dataview plugin for queries like `TABLE tags FROM "entities" WHERE contains(tags, "company")`

## Pitfalls

- **Automated wiki health cron gotchas** — For workspace-hub `scripts/knowledge/wiki_health_cron.py` runs, verify the domain list before trusting the report. Hidden/operational directories under `knowledge/wikis/` (for example `.planning/`) are not domain wikis and should be skipped. Directories that contain only `AGENTS.md` or otherwise lack `wiki/` should be reported as critical missing scaffold/index/log issues, not allowed to crash the cron before reports are written. Health reports under `knowledge/wikis/health-reports/` may be ignored by `.gitignore`; use `git add -f knowledge/wikis/health-reports/health-YYYY-MM-DD.{json,md}` when committing them.
- **Never modify files in `raw/`** — sources are immutable. Corrections go in wiki pages.
- **Always orient first** — read SCHEMA + index + recent log before any operation in a new session.
  Skipping this causes duplicates and missed cross-references.
- **Always update index.md and log.md** — skipping this makes the wiki degrade. These are the
  navigational backbone.
- **Don't create pages for passing mentions** — follow the Page Thresholds in SCHEMA.md. A name
  appearing once in a footnote doesn't warrant an entity page.
- **Don't create pages without cross-references** — isolated pages are invisible. Every page must
  link to at least 2 other pages.
- **Frontmatter is required** — it enables search, filtering, and staleness detection.
- **Tags must come from the taxonomy** — freeform tags decay into noise. Add new tags to SCHEMA.md
  first, then use them.
- **Keep pages scannable** — a wiki page should be readable in 30 seconds. Split pages over
  200 lines. Move detailed analysis to dedicated deep-dive pages.
- **Ask before mass-updating** — if an ingest would touch 10+ existing pages, confirm
  the scope with the user first.
- **Rotate the log** — when log.md exceeds 500 entries, rename it `log-YYYY.md` and start fresh.
  The agent should check log size during lint.
- **Handle contradictions explicitly** — don't silently overwrite. Note both claims with dates,
  mark in frontmatter, flag for user review.
- **PDF extraction timeout** — Large PDFs hit 5-min sandbox timeouts. Use metadata-first
  approach for speed. Full extraction = enhancement when async workers exist.
- **Git force-add required** — Wiki dirs may be in `.gitignore`. Use `git add -f` to commit
  content. Wiki content is the compounding artifact and must be tracked.
- **Batch size trade-off** — 100 records/batch balances speed with index update frequency.
  Smaller = more frequent updates, slower. Larger = fewer index commits, risk more on crash.
- **Low link density early** — Newly created wikis naturally have low link density.
  This resolves as cross-references grow during normal ingest operations.
- **YAML seed migration is fast** — Converting structured YAML to wiki pages is 10x faster
  than PDF extraction. Use this pattern whenever seeds exist.