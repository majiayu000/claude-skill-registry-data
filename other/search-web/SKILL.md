---
description: >-
  Structured, budget-disciplined web research that builds a source corpus and
  forms an evidence-backed opinion via a scientific process. Use when a task
  needs current or external information and the answer should be grounded in
  fetched sources rather than recall — e.g. "research X", "investigate Y",
  "what's the state of the art on Z", "compare A vs B", "form a view on...",
  or any web-search task dispatched to a subagent. Treats each web_search call
  as a scarce resource: indexes a corpus in 1-2 searches, batch-fetches the
  pages to markdown, then reasons over the local corpus instead of searching
  more. Designed to run as a dispatched research subagent.
hooks:
  PreToolUse:
    - matcher: "WebFetch"
      hooks:
        - type: command
          command: "bash $HOME/.claude/skills/search-web/scripts/block-webfetch.sh"
---

# Web Research Corpus

## Mental model

Web searches are a roll of film, not a faucet. Every `web_search` call spends a
frame. You cannot buy more mid-shoot. Plan the shot, then take it.

The cost of a search is not the API call — it is the unfocused context it dumps
into the window and the unscientific "search → skim → search again" spiral it
invites. This skill replaces that spiral with a fixed pipeline: **index a
corpus, fetch it once, then reason over local files.**

## Execution model — this skill MUST run in a dispatched subagent

Web research belongs in an isolated context. Search results and fetched
pages are bulky and noisy: running the pipeline in the main conversation
floods its context window, and — under context-compression proxies like
Headroom — search results are silently shredded before they can be used.
A dispatched subagent has its own context window: it absorbs the noise,
runs the full pipeline, and hands back only the one-line corpus path.

**If you are the main conversation** (this skill was invoked directly,
e.g. via `/search-web`, and you are NOT already a subagent): your ONLY
action is to dispatch the `search-web` subagent via the Agent tool. Pass
the research question and any relevant context in the prompt, and include
the literal marker `[search-web-subagent]` so the dispatched agent knows
its role. Do NOT call WebSearch, WebFetch, or `ctx_fetch_and_index`
yourself. When the subagent returns the corpus path, read that file and
report the result.

**If you are the dispatched subagent** (your prompt contains the marker
`[search-web-subagent]`): skip dispatch and execute Phase 0 onward.

Running Phases 0-3 in the main conversation is a process failure.
Dispatching is not optional.

## The pipeline

Execute these phases in order. Do not loop back to an earlier phase to "just
check one more thing" — that is the spiral this skill exists to prevent.

### Phase 0 — Scope and assign a search budget

Restate the research question in one sentence. Classify its depth and fix the
budget **before searching**:

| Depth | Question shape | Search budget | Target corpus |
|-------|----------------|---------------|---------------|
| Shallow | Single fact, definition, current value | 1 search | 2-4 pages |
| Standard | "How does X work", one comparison, one decision | 1-2 searches | 5-8 pages |
| Deep | Multi-faceted, contested, or strategic question | 2-3 searches | 8-15 pages |

Going over budget is a process failure. If results are thin, that is itself a
finding — report it; do not burn more frames.

### Phase 1 — Index the corpus (searches happen ONLY here)

Spend the search budget here and nowhere else. The goal of each search is **URL
discovery**, not answers. Do not try to answer the question from search
snippets.

Rules:
- Write each query to cover a distinct facet of the question. Two searches must
  not be paraphrases of each other.
- From the results, select the URLs that form a deliberate corpus: prefer
  primary sources, official docs, and substantive articles; cover disagreeing
  viewpoints when the question is contested; drop SEO filler and duplicates.
- For each kept URL, record a one-line note on *why* it earned its place.
- Stop searching the moment the budget is spent. Proceed to Phase 2 even if the
  corpus feels imperfect.

Write the kept URLs to a file, one per line, optional `<TAB>note`:

```
https://example.com/primary-source	official spec, authoritative
https://blog.example.org/critique	dissenting view on the tradeoff
```

### Phase 2 — Batch-fetch the corpus (one tool call)

Fetch every indexed URL in a single invocation. Do not fetch pages one at a
time, and do not use `web_search` again.

**If context-mode is available** (the `mcp__plugin_context-mode_context-mode__*`
tools are present), prefer it over the script. For each indexed URL call
`mcp__plugin_context-mode_context-mode__ctx_fetch_and_index(url, source)`,
passing the **same `source` slug** (the `<short-slug>` below) for every URL so
the whole corpus indexes under one searchable source. Page content lands in the
FTS5 knowledge base, not the context window — no raw markdown dump. Skip the
`batch_fetch.py` step. Still create `<work_dir>/corpus-summary.md` listing every
URL, its one-line note, and the shared `source` slug, so the corpus is
inspectable and the output contract holds. Phase 3 then retrieves evidence with
`ctx_search` instead of reading page files.

If context-mode is **not** installed, use the script below.

Default `<work_dir>` is `.claude/research/<short-slug>-<timestamp>/`, relative
to the current working directory — unless the dispatch prompt specifies
otherwise. The script creates the directory (and parents) if absent.

```bash
scripts/batch_fetch.py --urls urls.txt --out <work_dir> --topic "<question>"
```

The script (uv-managed; deps install on first run) fetches concurrently,
extracts main-content markdown with **trafilatura**, falls back to the
**r.jina.ai** reader for pages trafilatura cannot extract, writes one markdown
file per page under `<work_dir>/pages/`, and writes `<work_dir>/corpus-summary.md`
indexing every page (title, original URL, scrape path, method, word count).

It prints the absolute path of `corpus-summary.md` as its only stdout line.

Requires `uv` on PATH. Pass URLs via `--urls <file>` or repeated `--url` flags.

### Phase 3 — Form an opinion (scientific process)

Reason over the fetched corpus — not search snippets — like an experiment, not
a book report. If the corpus was fetched via context-mode in Phase 2, query it
with `mcp__plugin_context-mode_context-mode__ctx_search(queries: [...])` to pull
the passages each hypothesis needs; cite the page URL the passage came from.
Otherwise read the fetched markdown files directly. The full procedure and the brief
template are in **[references/opinion-process.md](references/opinion-process.md)**;
read it now. In short:

1. State a hypothesis (a candidate answer).
2. Gather evidence from the corpus for and against it, each claim cited to a
   specific page file.
3. Weigh source quality and resolve conflicts explicitly.
4. State the opinion with a calibrated confidence level and name what would
   change it.

Append the resulting **Research Brief** section to `corpus-summary.md` (the
template is in the reference). The single file then carries both the opinion
and the corpus it rests on.

## Output contract

**The dispatched subagent** (runs Phases 0-3): the final message MUST be
exactly one line — the absolute path to `corpus-summary.md`. No preamble, no
summary, no commentary. The dispatcher reads the file.

**The dispatcher** (main conversation, after the subagent returns): read
`corpus-summary.md` and report the practical result for the current task — the
opinion, its confidence, and the one or two corpus findings that matter here —
plus anything else genuinely relevant to the surrounding context. Cite page
files or URLs.

## Rules

- Searches happen in Phase 1 only. Never search in Phase 2 or 3.
- Never exceed the Phase 0 search budget. A thin corpus is a finding to report.
- Form the opinion from the fetched corpus, never from search snippets.
- Every claim in the brief cites a specific source — a `pages/NN-*.md` file, or
  the page URL when the corpus was indexed via context-mode.
- Report fetch failures (`method: failed` rows) honestly; do not silently drop
  a source the opinion would have depended on.
