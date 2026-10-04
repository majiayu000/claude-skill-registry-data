---
name: knowledge-graph
description: "Use for any question about a codebase, its architecture, file relationships, or project content — especially when a knowledge graph output exists. Turns any input (code, docs, papers, images, videos) into a persistent knowledge graph with community detection and query/path/explain tools."
argument-hint: "[path|query|subcommand]"
---

## Required `<project-root>/docs` reads

Read these project-root spec files before any knowledge graph query or build (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/knowledge-graphs.md`

# /graphify (see `<project-root>/docs/knowledge-graphs.md` in the project root for tool interface)

Turn any folder into a navigable knowledge graph with community detection, an audit trail, and three outputs: interactive HTML, GraphRAG-ready JSON, and a plain-language GRAPH_REPORT.md.

## Usage

The knowledge graph tool's commands (see `<project-root>/docs/knowledge-graphs.md` in the project root):

| Command | Purpose |
|---------|---------|
| `/graphify [path]` | Full pipeline (current dir if no path) |
| `--mode deep` | Thorough extraction, richer INFERRED edges |
| `--update` | Incremental: re-extract new/changed files only |
| `--cluster-only` | Rerun clustering on existing graph |
| `--no-viz` | Skip visualization, report + JSON only |
| `--svg/--graphml` | Export graph.svg/graph.graphml |
| `--neo4j-push <url>` | Push directly to Neo4j |
| `--mcp` | Start MCP stdio server |
| `--watch` | Watch folder, auto-rebuild on changes |
| `--wiki` | Build agent-crawlable wiki |
| `add <url>` | Fetch URL, save to ./raw, update graph |
| `query "<q>"` / `path "A" "B"` / `explain "X"` | Query operations |

## Output Discipline
Do not announce that you are using this skill. Do not restate its rules in your response. The skill guides behavior silently; visible output should show the result, not the activation.

## What You Must Do When Invoked

If `/graphify --help` or `/graphify -h` (no other args): print the `## Usage` section verbatim and stop. No commands, no file detection, no path default.

If no path is given, use `.` (current directory). Do not ask.

Follow steps in order. Do not skip.

### Step 1 - Ensure graphify is installed

<!-- script: see references/scripts.md §Step 1 - Ensure graphify is installed -->

If the import succeeds, print nothing and go to Step 2.

**In every subsequent bash block, replace `python3` with the detected Python interpreter (see `<project-root>/docs/knowledge-graphs.md` in the project root).**

### Step 2 - Detect files

<!-- script: see references/scripts.md §Step 2 - Detect files -->

Replace `INPUT_PATH` with the actual path the user provided. Do NOT cat or print the JSON — read it silently and present a clean summary:

```
Corpus: X files · ~Y words
  code:     N files (.py .ts .go ...)
  docs:     N files (.md .txt ...)
  papers:   N files (.pdf ...)
  images:   N files
  video:    N files (.mp4 .mp3 ...)
```

Omit categories with 0 files.

Then act:
- If `total_files` is 0: stop with "No supported files found in [path]."
- If `skipped_sensitive` is non-empty: mention the file count skipped, not the names.
- If `total_words` > 2,000,000 OR `total_files` > 200: show the warning and the top 5 subdirectories by file count, then ask which subfolder to run on. Wait for the answer before proceeding.
- Otherwise: go to Step 2.5 if video files were detected, or Step 3 if not.

### Step 2.5 - Transcribe video / audio files (only if video files detected)

Skip if `detect` returned zero `video` files. Transcribe to text and treat as docs in Step 3.

**Strategy:** Read god nodes from the detect/analysis output, write a one-sentence domain hint, and pass it to Whisper as the initial prompt (see `<project-root>/docs/knowledge-graphs.md` in the project root for Whisper configuration). If the corpus has *only* video files (no docs/code), use fallback: `"Use proper punctuation and paragraph breaks."`

**Step 1 - Write Whisper prompt:** Read top god node labels and compose a domain hint (e.g., `transformer, attention` → `"Machine learning research on transformer architectures. Use proper punctuation."`). Set as `GRAPHIFY_WHISPER_PROMPT`.

**Step 2 - Transcribe:** <!-- script: see references/scripts.md §Step 2.5 - Transcribe video / audio files -->

After transcription: read `graphify-out/.graphify_transcripts.json` (the graph output directory, e.g. `graphify-out/` — see `<project-root>/docs/knowledge-graphs.md` in the project root), add to the docs list for Step 3B, print `Transcribed N video file(s) -> treating as docs`. Warn on failures and continue.

**Whisper model:** Default `base`. If `--whisper-model <name>` was passed, set `GRAPHIFY_WHISPER_MODEL=<name>`.

### Step 3 - Extract entities and relationships

**Before starting:** Note if `--mode deep` was given. Pass `DEEP_MODE=true` to every extraction chunk in Step B2 if set. Track from the original invocation.

Two parts: **structural extraction** (AST, deterministic, free) and **semantic extraction** (your model, costs tokens).

> **The knowledge graph tool needs no external API key. Never ask or block on one.** Code is extracted structurally (AST) with no LLM/key — a code-only corpus skips semantic extraction entirely (go straight to Part A, skip Part B). Semantic extraction (docs/papers/images only) uses your model. Code-only corpus has no semantic work (write an empty semantic file and continue to Part C).

**Run Part A (AST) and Part B (semantic) in parallel. Start AST extraction and semantic extraction in the same message. They run simultaneously across different file types. Merge in Part C.**

#### Part A - Structural extraction for code files

For any code files detected, run AST extraction in parallel with Part B (see `<project-root>/docs/knowledge-graphs.md` in the project root):

<!-- script: see references/scripts.md §Step 3 Part A - Structural extraction (AST) -->

#### Part B - Semantic extraction (parallel chunks)

**Fast path:** If zero docs/papers/images are detected (code-only corpus), skip Part B and go straight to Part C. AST handles code.

Before starting, print a timing estimate:
- Load `total_words`/file counts from `graphify-out/.graphify_detect.json`
- Estimate chunks: `ceil(uncached_non_code_files / 22)` (chunk size 20-25)
- Estimate time: ~45s per chunk batch (parallel, so total ≈ 45s × ceil(chunks/parallel_limit))
- Print: "Semantic extraction: ~N files → X chunks, estimated ~Ys"

**Step B0 - Check extraction cache first**

Before starting, check which files already have cached extraction results:

<!-- script: see references/scripts.md §Step B0 - Check extraction cache -->

Only process files listed in `graphify-out/.graphify_uncached.txt`. If all files are cached, skip to Part C directly.

**Step B1 - Split into chunks**

Load files from `graphify-out/.graphify_uncached.txt`. Split into chunks of 20-25 files each. Each image gets its own chunk (vision needs separate context). Group files from the same directory together so related artifacts land in the same chunk and cross-file relationships are more likely to be extracted.

**Step B2 - Extract each chunk**

Process ALL chunks in parallel.

Concrete example for 3 chunks:
```
[Chunk 1: files 1-15]
[Chunk 2: files 16-30]
[Chunk 3: files 31-45]
```

For each chunk, extract a knowledge graph fragment using this exact prompt (fill in `FILE_LIST`):

```
Read the files listed and extract a knowledge graph fragment.
Output ONLY valid JSON with no commentary: {"nodes": [...], "edges": [...], "hyperedges": [...], "input_tokens": 0, "output_tokens": 0}

Extraction rules:
- EXTRACTED: explicit in source (import, call, citation)
- INFERRED: reasonable inference (shared structure, implied dependency)
- AMBIGUOUS: uncertain — flag it, do not omit
- Code files: extract semantic edges AST cannot find (design patterns, protocol conformance). Do not re-extract imports.
- Doc/paper files: named concepts, entities, citations. Store rationale (WHY decisions) as `rationale` attribute on relevant node. Use `file_type:"rationale"` for concept-like nodes (ideas, principles, mechanisms) and `file_type:"concept"` for named concepts. `file_type` MUST be one of: `code`, `document`, `paper`, `image`, `rationale`, `concept`. When adding `calls` edges: source is caller, target is callee.
- Image files: use vision to understand what the image IS (not just OCR). UI screenshot: layout patterns, design decisions, key elements, purpose. Chart: metric, trend/insight, data source. Tweet/post: claim as node, author, concepts mentioned. Diagram: components and connections. Research figure: what it demonstrates, method, result. Handwritten/whiteboard: ideas and arrows, mark uncertain readings AMBIGUOUS.
- DEEP_MODE (if set): be aggressive with INFERRED edges
- Semantic similarity: if two concepts solve same problem without structural link, add `semantically_similar_to` INFERRED edge (confidence 0.6-0.95). Non-obvious cross-file links only.
- Hyperedges: if 3+ nodes share concept/flow not captured by pairwise edges, add hyperedge. Max 3 per file.
- If file has YAML frontmatter (--- ... ---), copy source_url, captured_at, author, contributor onto every node from that file.
- confidence_score REQUIRED on every edge — never omit, never use 0.5 default:
  - EXTRACTED edges: confidence_score = 1.0 always
  - INFERRED edges: pick exactly ONE value — never 0.5:
    0.95 direct structural evidence (shared data structure, named cross-file reference)
    0.85 strong inference (clear functional alignment, no direct symbol link)
    0.75 reasonable inference (shared problem domain + similar shape, requires interpretation)
    0.65 weak inference (thematically related, no shape evidence)
    0.55 speculative but plausible (surface-level co-occurrence only)
  Models follow discrete rubrics better than continuous ranges; if no value above fits, mark AMBIGUOUS rather than picking 0.4 or below.
- AMBIGUOUS edges: 0.1-0.3

Schema:
{"nodes":[{"id":"filestem_entityname","label":"Human Readable Name","file_type":"code|document|paper|image|rationale|concept","source_file":"relative/path","source_location":null,"source_url":null,"captured_at":null,"author":null,"contributor":null}],"edges":[{"source":"node_id","target":"node_id","relation":"calls|implements|references|cites|conceptually_related_to|shares_data_with|semantically_similar_to|rationale_for","confidence":"EXTRACTED|INFERRED|AMBIGUOUS","confidence_score":1.0,"source_file":"relative/path","source_location":null,"weight":1.0}],"hyperedges":[{"id":"snake_case_id","label":"Human Readable Label","nodes":["node_id1","node_id2","node_id3"],"relation":"participate_in|implement|form","confidence":"EXTRACTED|INFERRED","confidence_score":0.75,"source_file":"relative/path"}],"input_tokens":0,"output_tokens":0}

Files:
FILE_LIST
```

**Step B3 - Cache and merge**

Wait for all chunks. For each result:
- Check that `graphify-out/.graphify_chunk_N.json` exists on disk — this is the success signal.
- If the file exists and contains valid JSON with `nodes` and `edges`, include it and save to cache.
- If the file is missing, print a warning: "chunk N missing from disk." Do not silently skip.
- If a chunk failed or returned invalid JSON, print a warning and skip that chunk — do not abort.

If more than half the chunks failed or are missing, stop and tell the user to re-run.

After each chunk completes, write its result to `graphify-out/.graphify_chunk_N.json`. The chunk JSON has placeholder zeros for token counts — update them with real values before merging. Then merge:

<!-- script: see references/scripts.md §Step B3 - Merge chunks -->

Save new results to cache:
<!-- script: see references/scripts.md §Step B3 - Save new results to cache -->

Merge cached + new results into `graphify-out/.graphify_semantic.json`:
<!-- script: see references/scripts.md §Step B3 - Merge cached + new results -->
Clean up temp files: `rm -f graphify-out/.graphify_cached.json graphify-out/.graphify_uncached.txt graphify-out/.graphify_semantic_new.json`

#### Part C - Merge AST + semantic into final extraction

<!-- script: see references/scripts.md §Part C - Merge AST + semantic into final extraction -->

### Step 4 - Build graph, cluster, analyze, generate outputs

**Before starting:** Code blocks below pass `directed=IS_DIRECTED` to `build_from_json()`. Replace `IS_DIRECTED` with `True` if `--directed` was given (builds `DiGraph` preserving edge direction source->target), otherwise `False` (default undirected `Graph`). Substitute everywhere it appears, the same way as `INPUT_PATH`.

<!-- script: see references/scripts.md §Step 4 - Build graph, cluster, analyze, generate outputs -->

If it prints `ERROR: Graph is empty`, stop and tell the user what happened — do not proceed to labeling/visualization.

Replace `INPUT_PATH` with the actual path.

### Step 5 - Label communities

Read `graphify-out/.graphify_analysis.json`. For each community key, look at the node labels and write a 2-5 word plain-language name (e.g., "Attention Mechanism", "Training Pipeline", "Data Loading").

Regenerate the report and save labels for the visualizer:

<!-- script: see references/scripts.md §Step 5 - Label communities -->

Replace `LABELS_DICT` with the actual dict (e.g., `{0: "Attention Mechanism", 1: "Training Pipeline"}`). Replace `INPUT_PATH` with the actual path.

### Step 6 - Generate Obsidian vault (opt-in) + HTML

**Generate HTML always** (unless `--no-viz`). **Obsidian vault only if `--obsidian` was explicitly given** — skip otherwise (generates one file per node).

If `--obsidian` was given:

<!-- script: see references/scripts.md §Step 6 - Obsidian vault (only if --obsidian) -->

Generate the HTML graph (always, unless `--no-viz`):

<!-- script: see references/scripts.md §Step 6 - HTML visualization -->

### Step 6b - Wiki (only if --wiki flag)

**Only run this step if `--wiki` was explicitly given in the original command.**

The wiki is an agent-crawlable export — `index.md` plus one article per community and god-node articles.

Run this before Step 9 (cleanup) so `graphify-out/.graphify_labels.json` is still available.

<!-- script: see references/scripts.md §Step 6b - Wiki (only if --wiki) -->

### Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag)

**If `--neo4j`** — generate a Cypher file for manual import:

<!-- script: see references/scripts.md §Step 7 - Neo4j export (only if --neo4j) -->

**If `--neo4j-push <uri>`** — push directly to a running Neo4j instance. Ask the user for credentials if not provided:

<!-- script: see references/scripts.md §Step 7 - Neo4j push (only if --neo4j-push) -->

Replace `NEO4J_URI`, `NEO4J_USER`, and `NEO4J_PASSWORD` with actual values. Defaults: URI `bolt://localhost:7687`, user `neo4j`. Uses MERGE — safe to re-run without creating duplicates.

### Step 7b - SVG export (only if --svg flag)

<!-- script: see references/scripts.md §Step 7b - SVG export (only if --svg) -->

### Step 7c - GraphML export (only if --graphml flag)

<!-- script: see references/scripts.md §Step 7c - GraphML export (only if --graphml) -->

### Step 7d - MCP server (only if --mcp flag)

<!-- script: see references/scripts.md §Step 7d - MCP server (only if --mcp) -->

This starts a stdio MCP server exposing `query_graph`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `graph_stats`, and `shortest_path`. Add it to Claude Desktop or any MCP-compatible orchestrator so other agents can query the graph live.

To configure in Claude Desktop, add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "graphify": {
      "command": "python3",
      "args": ["-m", "graphify.serve", "/absolute/path/to/graphify-out/graph.json"]
    }
  }
}
```

### Step 8 - Token reduction benchmark (only if total_words > 5000)

If `total_words` from `graphify-out/.graphify_detect.json` is greater than 5,000, run:

<!-- script: see references/scripts.md §Step 8 - Token reduction benchmark (only if total_words > 5000) -->

Print the output directly in chat. If `total_words <= 5000`, skip silently — for small corpora the value is structural clarity, not token compression.

---

### Step 9 - Save manifest, update cost tracker, clean up, and report

<!-- script: see references/scripts.md §Step 9 - Save manifest, update cost tracker, clean up -->

Tell the user (omit the `obsidian/` line unless `--obsidian` was given; omit the `wiki/` line unless `--wiki` was given):
```
Graph complete. Outputs in PATH_TO_DIR/graphify-out/ (the graph output directory — see `<project-root>/docs/knowledge-graphs.md` in the project root)

  graph.html            - interactive graph, open in browser
  GRAPH_REPORT.md       - audit report
  graph.json            - raw graph data
  obsidian/             - Obsidian vault (only if --obsidian was given)
  wiki/                 - agent-crawlable wiki, start at wiki/index.md (only if --wiki was given)
```

Replace `PATH_TO_DIR` with the actual absolute path of the processed directory.

Then paste these sections from GRAPH_REPORT.md into the chat:
- God Nodes
- Surprising Connections
- Suggested Questions

Do NOT paste the full report — only those three sections.

Then offer to explore. Pick the single most interesting suggested question — the one that crosses the most community boundaries or has the most surprising bridge node — and ask:

> "The most interesting question this graph can answer: **[question]**. Want me to trace it?"

If the user says yes, run `/graphify query "[question]"` and walk them through the answer using the graph structure: which nodes connect, which community boundaries are crossed, and what the path reveals. Keep going as long as they want. End each answer with a natural follow-up ("this connects to X — want to go deeper?") so the session feels like navigation, not a one-shot report.

---

## Interpreter guard for subcommands

Before running any subcommand below (`--update`, `--cluster-only`, `query`, `path`, `explain`, `add`), check that `.graphify_python` exists. If it's missing (e.g. the user deleted `graphify-out/`), re-resolve the interpreter first:

<!-- script: see references/scripts.md §Interpreter guard for subcommands -->

---

## For --update (incremental re-extraction)

Use when you have added or modified files since the last run. Only re-extracts changed files.

<!-- script: see references/scripts.md §--update - Detect incremental changes -->

If new files exist, first check whether all changed files are code files:

<!-- script: see references/scripts.md §--update - Check if code-only -->

If `code_only` is True: print `[graphify update] Code-only changes detected - skipping semantic extraction (no LLM needed)`, run only Step 3A (AST) on the changed files, skip Step 3B entirely, then merge and run Steps 4-8.

If `code_only` is False (any changed file is a doc/paper/image): run the full Steps 3A-3C pipeline as normal.

If no new files exist (only deletions), create an empty extraction so the merge step can prune:

<!-- script: see references/scripts.md §--update - Empty extraction for deletions only -->

Then:

<!-- script: see references/scripts.md §--update - Merge new extraction into existing graph -->

Run Steps 4-8 on the merged graph as normal.

After Step 4, show the graph diff:

<!-- script: see references/scripts.md §--update - Graph diff -->

Before the merge step, save the old graph: `cp graphify-out/graph.json graphify-out/.graphify_old.json`
Clean up after: `rm -f graphify-out/.graphify_old.json`

---

## For --cluster-only

Skip Steps 1-3. Load the existing graph from `graphify-out/graph.json` and re-run clustering:

<!-- script: see references/scripts.md §--cluster-only -->

Then run Steps 5-9 as normal.

---

## For /graphify query, path, and explain

For detailed query examples, see `queries.md`.

Fetch a URL and add it to the corpus, then update the graph.

<!-- script: see references/scripts.md §/graphify add - Fetch URL and add to corpus -->

Replace `URL` with the actual URL, `AUTHOR` with the user's name if provided, and `CONTRIBUTOR` likewise. After a successful save, automatically run the `--update` pipeline on `./raw` to merge the new file into the existing graph.

Supported URL types (auto-detected):
- Twitter/X -> fetched via oEmbed, saved as `.md` with tweet text and author
- arXiv -> abstract + metadata saved as `.md`
- PDF -> downloaded as `.pdf`
- Images (.png/.jpg/.webp) -> downloaded, vision extraction runs on next build
- Any webpage -> converted to markdown via html2text

---

## For --watch

Start a background watcher that monitors a folder and auto-updates the graph when files change.

<!-- script: see references/scripts.md §--watch -->

Replace `INPUT_PATH` with the folder to watch. Behavior depends on what changed:

- **Code files only (.py, .ts, .go, etc.):** re-runs AST extraction + rebuild + cluster immediately, no LLM needed. `graph.json` and `GRAPH_REPORT.md` update automatically.
- **Docs, papers, or images:** writes a `graphify-out/needs_update` flag and prints a notification to run `/graphify --update` (LLM semantic re-extraction required).

Debounce (default 3s): waits until file activity stops before triggering, so a wave of parallel agent writes doesn't trigger a rebuild per file.

Press Ctrl+C to stop.

---

## For git commit hook

Install a post-commit hook that auto-rebuilds the graph after every commit. No background process needed — it triggers once per commit and works with any editor.

<!-- script: see references/scripts.md §git commit hook -->

After every `git commit`, the hook detects which code files changed, re-runs AST extraction on those files, and rebuilds `graph.json` and `GRAPH_REPORT.md`. Doc/image changes are ignored by the hook — run `/graphify --update` manually for those.

---

## For always-on context in Devin sessions

Run once per project to make the knowledge graph tool always-on in Devin sessions:

<!-- script: see references/scripts.md §Devin always-on context -->

This writes a `## graphify` section to `.windsurf/rules/graphify.md` that instructs Devin to check the graph before answering codebase questions and rebuild it after code changes (see `<project-root>/docs/knowledge-graphs.md` in the project root).

<!-- script: see references/scripts.md §Devin always-on context -->

---

## Honesty Rules

- Never invent an edge. If unsure, use AMBIGUOUS.
- Never skip the corpus check warning.
- Always show token cost in the report.
- Never hide cohesion scores behind symbols — show the raw number.
