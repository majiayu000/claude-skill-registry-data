---
name: recall
description: Semantic-search personal knowledge (memory, plans, handoffs, skills, Codex rules) via the local RAG index at ~/.claude/rag-index/. Use when a query is fuzzy or cross-file ("how did we fix X", "what did we decide about Y", "which skill handles Z"). Complements grep (exact) and Serena (code symbols). If the user asks a recall question that doesn't map to a specific known file, reach here first.
type: skill
mcp_servers: [rag-index]
---

# recall

Semantic search over your personal knowledge corpus — chunked + embedded with `all-MiniLM-L6-v2`, stored in SQLite at `~/.claude/rag-index/index.sqlite`. Local-only.

## When to use

- Fuzzy / cross-file recall: "how did we fix pi-hole v6 volume shadow?"
- Skill discovery by intent: "which skill covers X"
- Past-decision lookup: "why did we choose Caddy over nginx-proxy"
- Handoff resumption: "what was I doing Thursday"

## When NOT to use

- Code symbols / refs in a live repo → use Serena instead.
- Grep for a literal string → use Grep tool.
- Reading a file you already know the name of → use Read tool.

## Usage

```bash
~/.claude/rag-index/venv/bin/python ~/.claude/rag-index/query.py "<natural-language question>"
```

Flags:

- `--top N` (default 5)
- `--scope memory,plans,handoffs,skills,codex` (default all)
- `--format json` (structured output for programmatic callers)

## No results / missing index

Don't fail silently — say which case you hit:

- **Index missing** (no `~/.claude/rag-index/index.sqlite`): the index hasn't been built. Say so and point to **Rebuild** below — do not hard-fail the turn.
- **Zero hits**: report "no matches" plainly. Suggest broadening the query or a narrower `--scope`, and confirm the relevant files are actually indexed (see **Index sources**).
- **Lead with the verdict**: state hit count + top result first, then detail.

## Index sources

- `~/.claude/projects/<project>/memory/*.md`
- `~/.claude/plans/*.md`
- `~/.claude/handoffs/*/*.md`
- `~/.claude/skills/*/SKILL.md`
- `~/.codex/AGENTS.md` + `~/.codex/rules/*.rules`

## Rebuild

```bash
~/.claude/rag-index/venv/bin/python ~/.claude/rag-index/build.py              # full (~5s, 900 chunks)
~/.claude/rag-index/venv/bin/python ~/.claude/rag-index/build.py --incremental path/to/file.md  # single file
```

A `PostToolUse` hook auto-runs `--incremental` whenever Claude writes to a tracked directory, so day-to-day you never need to rebuild manually. Full rebuild only after schema changes or bulk file moves.

## Output format

```text
#1  rrf=0.0312 cos=0.41 bm=7.82  [memory]  /path/to/file.md:40-53
   <400-char snippet>
```

`rrf` is the fused rank score; `cos` is MiniLM cosine similarity; `bm` is BM25 lexical score.
With rerank enabled, the CLI also includes cross-encoder ordering from the top fused candidates.

## Tuning notes

- Markdown fallback chunks are ~300 words with small overlap; code chunks are symbol-aware.
- Local model only (no network, ~90 MB).
- Reference deployment is ~17k chunks × 384 dims; full rebuild ~55 s on Apple Silicon.
- Reranker is supported via `--rerank on|off|auto`; use `--fast` to disable it for latency.

## Integration

- `plan` skill: append "related past plans" by running `recall --scope plans` on the task description.
- `pr-flow` / `ship`: inject related ADR / spec references into PR body.
- `sync-memories`: chains into `build.py --incremental` automatically.
