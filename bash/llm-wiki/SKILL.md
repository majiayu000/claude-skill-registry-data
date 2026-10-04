---
name: llm-wiki
description: "Use when the user wants a compiled markdown wiki, Karpathy llm-wiki ingest/query/lint, or to file sources into interlinked pages. Do not use for vault search (that is fde-kb) or typed triple recall (that is graph-memory)."
---

# llm-wiki (compiled pages)

`<skill>` is the directory that contains this SKILL.md.

Raw notes stay immutable in `raw/`. You (the agent) compile them into `wiki/`. The launcher searches and lints those pages. The CLI never calls a model and never picks a model id.

This folder is the whole skill. Copy only `llm-wiki/` if that is the path you want. Do not fold this into fde-kb or graph-memory.

## STOP

For a question: run exactly one `query` command. Show stdout. Answer from those pages. If stdout is `(no wiki pages for this prompt)`, say the wiki has nothing and stop. Do not grep `raw/` to invent an answer.

For a new source: write the file into `raw/` unchanged, then edit `wiki/` (update entity pages, `index.md`, append `log.md`). Write **full names** in page body, not only `[[slug]]`. Then `lint`.

Never write a new search engine or HTTP client. Never dump `raw/` into context when `query` returned pages.

## Launcher

- **macOS / Linux:** `<skill>/scripts/llm-wiki`
- **Windows:** `<skill>/scripts/llm-wiki.cmd`

```bash
<skill>/scripts/llm-wiki query "the user's question"
<skill>/scripts/llm-wiki lint
<skill>/scripts/llm-wiki status
```

Optional, no model: project graph-memory-shaped JSON into pages:

```bash
<skill>/scripts/llm-wiki compile-extracts /path/to/extraction
```

## Ingest (you do this)

1. Copy the source into `raw/`. Do not edit it later.
2. Read it. Update or create wiki pages. Cite `## Sources`.
3. Keep `index.md` as a catalog (one-liners, not the answer dump).
4. Append `log.md` with `## [YYYY-MM-DD] ingest | Title`.
5. Run `lint`. Fix broken links.

Page rules: one topic per file; `[[slug|Full Name]]` so a later query can see the name; flag superseded claims; do not invent aliases like "boss".

## When not to use

- Ordinary vault search over notes as they are → fde-kb
- Who-covers / typed hops you already modelled as triples → graph-memory
- kubernetes-scale dumps. Ingest cost grows with every source. Query stays small.

Benchmark (open in a browser): [docs/benchmark.html](docs/benchmark.html)
