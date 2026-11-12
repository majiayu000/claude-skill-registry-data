---
name: query
description: >
  Answer a natural-language question from the wiki with [[wikilink]] citations.
  Trigger when the user asks "what does the wiki say about X", "search the
  wiki for Y", "which sources cover Z", or invokes
  /claude-wiki-pages:query directly. Read-only against wiki content —
  only log.md receives an append.
allowed-tools: Read Glob Grep Edit
---

# LLM Wiki — Query

Answer a question from `vault/wiki/` with citations back to specific pages.

Unlike a general-purpose search, this skill commits to the wiki's provenance
model: every claim in the answer carries one or more `[[wikilink]]` citations,
and every cited page must resolve. No hallucinated titles, no paraphrase
without a source.

## When to invoke

- The user asks a natural-language question about a topic that might be
  covered in the wiki.
- An agent (`claude-wiki-pages-analyst-agent`) is chaining query as a step.

Do NOT invoke for questions about the *plugin itself* (how to install, which
hooks fire, what a skill does) — those are answered from the docs, not the
wiki.

## Reading contract

- `vault/CLAUDE.md` — the schema. Read first.
- `vault/wiki/index.md` — the top-level catalog. First pass to shortlist
  candidate pages.
- `vault/wiki/<topic>/<topic>.md` — per-folder MOCs (folder notes; legacy
  `_index.md` where still present). Second pass to narrow.
- `vault/wiki/<topic>/*.md` — candidate typed pages, plus any pages reached by
  following `[[wikilinks]]` from them.
- `vault/wiki/_synthesis/*.md` — prior syntheses, if relevant.
- `vault/wiki/_sources/*.md` — source summaries, when provenance matters to
  the answer.

### C1 — Budget-aware MOC descent (reading engine JSON)

When a `search --json` candidate set is available (produced by
`bash scripts/engine.sh search "<query>" --target <vault> --json`), the
descent reads the engine's ranked output and takes a budget-bounded prefix.

**Input shape.** Each `SearchHit` in the `hits` array carries:

| Field | Role in C1 |
| --- | --- |
| `score` | Authoritative rank key — the only ordering key C1 uses. |
| `matched[]` | Read for cut-off explanation and channel-aware tie-breaking. |
| `wikilink` | Page reference for citation. |
| `type` | Page type (for display / filter context). |
| `file` | Vault-relative path used to read the page. |

All five fields are **read-only**. C1 does not inspect `snippet` for ranking
purposes.

**Descent algorithm.**

1. Receive the `hits` array, already ordered by `score` descending (ties
   broken alphabetically by title) as emitted by the engine.
2. Walk the list top-down. Include each page in the reading set until the
   **context budget** is exhausted — i.e. until adding the next page would
   exceed the token allowance reserved for the answer synthesis step.
3. If two adjacent hits share the same `score` (a tie at the budget boundary),
   prefer the hit whose `matched[]` array contains a higher-priority channel
   entry (`title-phrase` or `title-term`) over a `body-only` / `body-term`
   entry. This is **channel-aware tie-breaking** inside the score-ordered
   sequence — it does not reorder pages that already have different scores.
4. Cite the included pages highest-scored first.

**Hard invariant — no re-ranking (§6 one-score-object).**
C1 takes a score-ordered **prefix** of the engine's output under a context
budget. It **never re-ranks**: it may not (a) compute any new numeric score,
(b) re-weight or re-sum `matched[].points`, or (c) reorder hits by any key
other than the engine-supplied `score` (lexicographic title tiebreak). The
emitted reading order is a **sub-sequence** of `search`'s order — C1 subsets,
it never re-ranks. This preserves the determinism R4 guarantees and keeps the
one-score-object invariant intact.

**Threshold.** C1 may additionally drop pages whose `score` falls below a
fraction of the top hit's score (e.g. below 20 % of `hits[0].score`). This
threshold is a **subset filter** — it only removes low-signal tail pages; it
does not alter the order of remaining pages.

## R3 — Agent-vs-human retrieval contract

`query` sits at the junction of two consumption paths for `search` output. Both
paths read the **same score** — the single score object (R4's `score` +
`matched[]`) that `search` emits. Neither path re-ranks.

### Agent path

The agent path is the C1 budget-aware MOC descent (see "C1 — Budget-aware MOC
descent" above). C1 reads the `search --json` output — specifically `score`,
`matched[]`, `wikilink`, `type`, and `file` — to select the reading set under
the context budget. `matched[]` is read only for channel-aware tie-breaking at
the budget boundary; C1 never recomputes or re-weights it.

### Human path

The human path is the rendered ranked list that `query` presents to the user: a
list of `[[wikilinks]]` cited in the answer, ordered highest-scored first. The
human path does not expose `matched[]` — humans navigate via wikilinks; they do
not need the per-channel score breakdown.

### One ranking, two consumption forms

There is one ranking, produced once by `search`, shared by both paths. The
agent path gets the structured form (`score` + `matched[]` + machine-readable
fields); the human path gets the rendered form (citations in prose + the
"Supporting pages" list). The same score object drives both — only the
consumption form differs. This keeps the one-score-object invariant intact
(Brief §6) and preserves the determinism R4 guarantees.

## Writing contract

- Append a single line to `vault/wiki/log.md`:
  `## [YYYY-MM-DD] query | <question summary>`
- No other writes unless the user accepts the optional offer to file the
  answer as a synthesis note — in which case control is passed to
  `/claude-wiki-pages:synthesize` and the write happens there, not here.

This skill MUST NOT:

- Mutate any wiki page to "fix" content it disagrees with (that is a lint-fix
  or a human decision).
- Fabricate a wikilink. Every `[[link]]` in the answer must point to an
  existing page.

## Workflow

1. **Schema.** Read `vault/CLAUDE.md`.
2. **Candidate set.** Run `bash scripts/engine.sh search "<query>" --target
   <vault> --json` to obtain a `SearchHit[]` array ordered by `score`
   descending. This is the C1 descent entry point.
3. **Shortlist (C1 descent).** Apply the budget-aware MOC descent (see
   "C1 — Budget-aware MOC descent" above): walk `hits` top-down; include
   pages until the context budget is exhausted or `score` drops below the
   threshold; use `matched[].channel` for channel-aware tie-breaking at the
   budget boundary. Never re-rank — the emitted reading order is a
   sub-sequence of the engine's score-ordered output. Fall back to reading
   `wiki/index.md` directly when the engine is unavailable.
4. **Gather.** Read the included pages. Follow `related:`, `sources:`,
   `scope:`, `children:`, and `child_indexes:` wikilinks to extend coverage.
5. **Synthesize.** Build an answer whose every claim resolves to at least one
   cited wiki page. Cite the highest-scored pages first. Prefer the most
   specific page over the most general one.
6. **Verify citations.** For each `[[link]]` in the answer, confirm the target
   page exists. Strip unresolved links — never print a dangling wikilink.
7. **Offer.** If the answer is substantial and no existing synthesis covers
   it, offer to file the answer as a new synthesis note under
   `wiki/_synthesis/`. Wait for the user to opt in.
8. **Log.** Append the query entry to `wiki/log.md`.

## Answer shape

Prefer this structure:

```
<direct answer in 1–3 sentences, with inline [[citations]]>

### Supporting pages
- [[Page A]] — <one-line why this page matters for the question>
- [[Page B]] — ...

### Caveats
- <contradictions, low-confidence claims, gaps>

## Sources

1. [[Page A]] — raw/<path-to-underlying-source>.md
2. [[Page B]] — raw/<path>.md, raw/<other-path>.md
```

Omit "Caveats" if there are none. Keep the direct answer tight — long prose
belongs in a synthesis note, not a query response.

### The `## Sources` grounding ledger (mandatory tail section)

Every answer ends with a `## Sources` section, research-paper style — the
grounding ledger. Inline `[[wikilink]]` citations stay; the tail section
traces them to raw evidence:

- Numbered entries, one per unique wiki page cited in the answer, in
  first-citation order.
- Each entry cites the wiki page as a `[[wikilink]]` plus the underlying raw
  source path(s) taken from that page's `sources:` frontmatter (resolved
  through its `_sources/` summary to the `raw/` file), e.g.
  `1. [[Offline Policy]] — raw/adr/ADR-0018-offline-policy-and-degraded-mode-routing.md`.
- Never invent a raw path. If a cited page's source chain does not resolve to
  a `raw/` file, write `(no raw source resolved)` — visible, not silent.
- Verbatim-quote and fabrication rules are unchanged; the ledger adds
  traceability, not new claims.

## Completion signal

Print the answer. Then, on a new line:

```
Logged: query | <truncated question>
```

If the user accepted the synthesis offer, additionally print:

```
Handing off to /claude-wiki-pages:synthesize.
```
