---
name: knowledge-ask
description: "This skill should be used when the user asks 'what do I know about [topic]',
  'what does Basic Memory say about [X]', 'do I have notes on [X]', 'look up [X] in
  my knowledge graph', 'ask memory about [X]', 'recall what we captured about [topic]',
  'find notes on [topic]', 'knowledge question', 'query the knowledge graph',
  'what observations do I have about [X]', 'knowledge lookup'. Searches Basic Memory
  for notes and observations matching a specific topic or question -- synthesizes an
  answer with source citations and gap suggestions. NOT for project-wide inventory
  or coverage reports (use /knowledge-prime for that)."
user-invocable: true
argument-hint: "<question>"
allowed-tools:
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
  - mcp__basic-memory__build_context
  - mcp__basic-memory__list_directory
---

# Knowledge Ask

Answer a freeform question by searching the Basic Memory knowledge graph, loading
relevant notes, traversing 1-hop neighbors, and synthesizing a cited answer. Each
answer includes a confidence tier (Direct, Partial, or No Coverage) so the user
knows how much the graph actually covers.

Read-only -- never writes or modifies notes. When coverage is incomplete, suggests
`/intel` or `/knowledge-gaps` to fill the gap.

## Arguments

The user provides a topic or question after the skill invocation:

| Form | Example |
|------|---------|
| Topic phrase | `/knowledge-ask fastify error handling` |
| Natural language question | `/knowledge-ask how does pino redaction work?` |
| Concept | `/knowledge-ask IndieWeb` |
| Package identifier (with prefix) | `/knowledge-ask npm:undici` |
| Tool identifier (with prefix) | `/knowledge-ask brew:ripgrep` |
| gh CLI extension (with prefix) | `/knowledge-ask gh:meiji163/gh-notify` |

Prefixed identifiers (`npm:`, `crate:`, `brew:`, `action:`, `gh:`, etc.) trigger
a fast existence check via `list_directory` in addition to the hybrid search.

## Edge Cases

- **No results** -- assign "No Coverage" confidence. Report "Basic Memory has no
  notes matching this question." Suggest `/intel <pkg>`
  if the query looks like a package or tool name.
- **BM unavailable** -- report the error and suggest trying again later. The
  PostToolUseFailure hook covers BM write-tool errors only; read-tool failures
  (search_notes, read_note, build_context) surface as raw error strings.
- **Ambiguous query** -- if `search_notes` returns results spanning 3+ unrelated
  topics, pick the best-matching cluster and note "Results also touched \[other
  topics\] -- narrow your query for those."
- **Package/tool not in BM** -- if a prefixed query (e.g., `npm:undici`) has no
  `list_directory` match and no search results, report "No note found for
  `npm:undici`." and suggest `/intel undici` to create it.
- **Very broad query** -- if the query maps to an entire ecosystem directory
  (e.g., "what do I know about npm packages"), use
  `list_directory(dir_name="npm", depth=1)` to report directory-level counts
  rather than loading individual notes. Suggest `/knowledge-prime` for
  project-scoped overviews or `/knowledge-gaps` for coverage audits.
- **Schema notes in results** -- exclude notes with titles starting with
  `schema/` from the answer synthesis. These are structural definitions, not
  knowledge content.

## Workflow

### 1. Search

Run a hybrid search (the default mode) against Basic Memory:

```
search_notes(query="<user question>", page_size=10)
```

If the query contains a recognized ecosystem prefix (`npm:`, `crate:`, `go:`,
`composer:`, `pypi:`, `gem:`, `brew:`, `cask:`, `action:`, `docker:`, `vscode:`,
`gh:`), also run a fast existence check:

```
list_directory(dir_name="<ecosystem-dir>", file_name_glob="*<name>*")
```

Prefix-to-directory mapping:

| Prefix | Directory |
|--------|-----------|
| `npm:` | `npm/` |
| `crate:` | `crates/` |
| `go:` | `go/` |
| `composer:` | `composer/` |
| `pypi:` | `pypi/` |
| `gem:` | `gems/` |
| `brew:` | `brew/` |
| `cask:` | `casks/` |
| `action:` | `actions/` |
| `docker:` | `docker/` |
| `vscode:` | `vscode/` |
| `gh:` | `gh/` |

Filter out schema notes (titles starting with `schema/`) from the results.

If fewer than 3 unique note topics are returned, note this as a sparse coverage
signal for the confidence tier in step 4.

### 2. Load candidates

For the top 3 results from step 1, load full note content:

```
read_note(identifier="<note-title>", include_frontmatter=true)
```

Extract observations relevant to the user's question. When multiple observations
match, prioritize by category:
`[gotcha]` > `[breaking]` > `[limitation]` > `[pattern]` > `[decision]` > `[lesson]`

**Token budget:** Load at most 3 notes fully. If a note is very long (50+
observations), extract only the observations relevant to the question rather
than quoting the entire section.

### 3. Traverse graph

Expand the highest-scoring note's immediate neighborhood:

```
build_context(url="<top-result-title>", depth=1, max_related=5)
```

Check whether any 1-hop neighbor is more relevant to the question than the
direct search results. If a neighbor is a better fit, load it:

```
read_note(identifier="<neighbor-title>", include_frontmatter=true)
```

Load at most 1 additional note from graph traversal. Stop at 1 hop -- do not
recurse further.

### 4. Assign confidence

Based on the loaded notes and observations, assign one of three confidence tiers:

| Tier | Condition |
|------|-----------|
| **Direct** | One or more notes directly address the question with specific observations |
| **Partial** | Notes touch the topic but don't fully answer, or only tangential neighbors matched |
| **No Coverage** | No notes found, or only schema notes matched |

### 5. Synthesize answer

Produce a structured answer using this template:

````markdown
## Answer: <question>

**Coverage:** Direct / Partial / No Coverage

<Prose answer, 2-5 sentences. Quote observations directly with
[[note-title]] - [category] citations. Stick to what the graph contains --
never hallucinate facts not present in the loaded notes.>

### Sources
- [[<note-title>]] -- <one-line reason this note was relevant>

### Coverage Gaps
<Only if Partial or No Coverage>
- **<subject>** -- Not documented. Run `/intel <pkg>` to create.
````

**Rules:**
- Omit the "Coverage Gaps" section entirely when confidence is Direct.
- For "No Coverage" answers: report "Basic Memory has no notes matching this
  question." -- never invent content.
- If the query looks project-scoped (mentions "this project", "our deps",
  "this codebase"), add a handoff hint: "For project-wide context, try
  `/knowledge-prime`."
- If the query is broad enough to warrant a coverage audit, suggest
  `/knowledge-gaps` instead.

## Guidelines

- **Read-only** -- this skill never writes, edits, or deletes notes
- **Graph-first** -- always search Basic Memory before answering; never answer
  from general knowledge alone
- **Cite sources** -- every factual claim must reference a `[[note-title]]`
- **Prefer precision** -- a narrow accurate answer beats a broad speculative one
- **Gap-fill suggestions** -- when coverage is incomplete, suggest the right
  skill to fill it (`/intel` or `/knowledge-gaps`)
- **Max 1-hop traversal** -- stop at direct neighbors to keep latency low and
  avoid context bloat
