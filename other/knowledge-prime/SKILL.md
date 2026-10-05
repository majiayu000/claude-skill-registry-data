---
name: knowledge-prime
description: "This skill should be used when the user asks to 'prime context', 'load project knowledge', 'what do we know about this project', 'knowledge brief', 'project context', 'what packages are documented', 'show coverage for this project', 'dependency coverage report', 'which of our deps have notes', 'knowledge primer', 'prime session', 'context for this project'. Surfaces project-relevant Basic Memory knowledge at session start or on demand — dependency coverage, key gotchas, engineering context, and gaps. NOT for freeform topic questions about individual packages or concepts (use /knowledge-ask for that)."
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - mcp__basic-memory__read_note
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__build_context
  - mcp__basic-memory__list_directory
  - mcp__basic-memory__recent_activity
---

# Knowledge Primer

Surface project-relevant Basic Memory knowledge as a concise context brief.
Identifies which dependencies and tools are documented, loads key gotchas and
patterns, and highlights gaps worth filling.

## Flags

- **`--deep`** — expand observation loading from 800 to 2000 tokens and include
  `[pattern]`, `[feature]`, `[usage]` categories alongside the default critical
  categories. Also expands graph traversal from top 6 to top 12 notes.

## Edge Cases

- **No manifest files found** — report "No package or tool manifest files
  detected in the current directory" and skip steps 2–5. Suggest running
  in a project root.
- **Empty BM directories** — treat as 0 documented. Don't error.
- **Very large dependency lists (100+)** — cap at top 50 by frequency/
  alphabetical for the cross-reference. Note total count in the brief.
- **`--deep` on a small graph (<10 notes)** — treat as compact mode.
  Report "Graph has fewer than 10 notes — showing all relevant notes."

## Workflow

### 1. Identify project stack

Detect manifest files in the current working directory:

| Manifest file | Ecosystem | BM directory | Prefix |
|---------------|-----------|--------------|--------|
| `package.json` | npm | `npm/` | `npm:` |
| `Cargo.toml` | Rust | `crates/` | `crate:` |
| `go.mod` | Go | `go/` | `go:` |
| `composer.json` | PHP | `composer/` | `composer:` |
| `pyproject.toml` or `requirements.txt` | Python | `pypi/` | `pypi:` |
| `Gemfile` | Ruby | `gems/` | `gem:` |
| `Brewfile` | Homebrew | `brew/`, `casks/` | `brew:`, `cask:` |
| `.github/workflows/*.yml` | Actions | `actions/` | `action:` |
| `Dockerfile` | Docker | `docker/` | `docker:` |
| `.vscode/extensions.json` | VSCode | `vscode/` | `vscode:` |

Use `Read` to check for root-level manifest files — do not use `Glob`, which recurses into `node_modules/` and similar directories. Use `Glob` only for wildcard paths like `.github/workflows/*.yml`. For detected package manifests, use
`Read` to extract dependency names:
- `package.json` → `dependencies` + `devDependencies` keys
- `Cargo.toml` → `[dependencies]` + `[dev-dependencies]` tables
- `go.mod` → `require` block
- `composer.json` → `require` + `require-dev` keys
- `pyproject.toml` → `[project.dependencies]` or `dependencies` key
- `requirements.txt` → package names (before `==`/`>=`/etc.)
- `Gemfile` → `gem '...'` lines

For tool manifests, extract tool names:
- `Brewfile` → `brew "..."`, `cask "..."`, `vscode "..."` lines
- `.github/workflows/*.yml` → `uses:` lines (extract `owner/repo`)
- `Dockerfile` → `FROM` lines (extract image names)
- `.vscode/extensions.json` → `recommendations` array

### 2. Query Basic Memory

For each detected ecosystem, list documented notes:

```
list_directory(dir_name="npm", depth=1)
list_directory(dir_name="crates", depth=1)
list_directory(dir_name="brew", depth=1)
# ... (only for ecosystems detected in step 1)
```

Each `list_directory` call costs ~50 tokens — only query ecosystems that have
manifest files in the project.

Cross-reference: for each dependency from step 1, check if a corresponding
note title exists in the `list_directory` results. Build two lists:
- **Documented** — deps with a BM note
- **Undocumented** — deps without a BM note

### 3. Score relevance

Assign relevance scores to documented notes using three passes:

**Pass 1 — Dependency match (score: 3):**
Notes whose title matches a direct project dependency.

**Pass 2 — Graph expansion (score: 2):**
For top-scoring notes from pass 1, expand via:
```
build_context(url="<ecosystem-dir>/<note-title>", depth=1, max_related=5)
```
Use each note's own resolved path from pass 1 (e.g. `npm/npm-fastify`,
`crates/crate-tokio`, `brew/brew-ripgrep`) — never hardcode to a single
ecosystem; a Cargo-only or Brewfile-only project will have pass 1 top-scoring
on crate or brew notes, not npm. Related notes that appear get score 2
(transitive relevance).

**Pass 3 — Beads/activity boost (score: 1):**
Fetch recent activity now (needed for scoring before sorting):
```
recent_activity(timeframe="7d", output_format="json")
```
Set an explicit `page_size` and paginate by incrementing `page` until a page
returns fewer items than `page_size` (or an empty result) — `recent_activity`
has no `has_more` field, unlike `search_notes` — to ensure complete 7-day
activity window. The response is a flat top-level `result` array (singular
key, not nested under `results`); collect the set of active permalinks
mentally, deduplicating as you go (`recent_activity` was observed returning
duplicate rows for the same entity in live testing).

If the project has `.beads/` (check via `Glob(pattern=".beads/*")`) or
`recent_activity` shows notes updated in the last 7 days, those notes get
+1 boost.

Sort all scored notes descending. Take top 6 (or top 12 with `--deep`).

### 4. Load observations

For each top-scored note, load critical observations:

```
read_note(identifier="<note-title>", include_frontmatter=true)
```

Extract only observations tagged with critical categories:
- `[gotcha]` — known pitfalls
- `[limitation]` — constraints to be aware of
- `[breaking]` — breaking changes
With `--deep`, also include `[pattern]`, `[feature]`, and `[usage]` categories.

**Token budget:** 800 tokens total (2000 with `--deep`). If observations
exceed the budget, prioritize `[gotcha]` > `[breaking]` > `[limitation]` >
`[pattern]`.

### 4b. Observation sweep (supplementary)

Search for critical observations beyond the top-scored notes:

```
search_notes(query="gotcha breaking limitation", search_type="text", entity_types=["observation"], page_size=10)
```

Note: BM's search treats space-separated terms and `OR` identically (hybrid
search, not strict FTS5 boolean). The query above is equivalent to
`"gotcha OR breaking OR limitation"` — use the simpler form.

**Post-filter:** Keep only observations whose content starts with `[gotcha]`,
`[breaking]`, or `[limitation]`. Discard others — the text query matches
these words anywhere, including prose mentions that are not category tags.

**Deduplication:** Build a set of note titles loaded in Step 4. Discard
observations from notes already in that set — Step 4 extracted their critical
observations in full context. Keep only observations from new notes.

**Token budget:** 200 tokens (400 with `--deep`), separate from Step 4's
800/2000 budget. Prioritize `[gotcha]` > `[breaking]` > `[limitation]`.

**Output:** Swept observations appear in a separate `### Other warnings`
section in the brief (Step 6), after `### Key gotchas`. Include the parent
note title as attribution. **Max 3 entries** to protect the "scannable in
30 seconds" goal. Omit the section entirely if no new observations survive
filtering.

If `search_notes` fails or returns an error, skip this step and proceed to
Step 5. Note "Observation sweep skipped (BM search unavailable)" in the
brief header.

10 results is sufficient — do not paginate even if `has_more` is true.

### 5. Cross-reference recent activity

Using the `recent_activity` results fetched in Step 3, note which of the
top-scored notes were recently updated — these are most likely to be relevant
to current work. Include in the brief output.

### 6. Synthesize brief

Produce a structured context brief:

````markdown
## Project Knowledge Brief

### Stack detected
- npm: 45 deps (38 documented, 7 undocumented)
- brew: 12 tools (10 documented, 2 undocumented)

### Key gotchas
- **npm-fastify** — [gotcha] reply.send() after reply.redirect() causes hang
- **npm-pino** — [limitation] redaction doesn't work on nested arrays

### Other warnings
- **npm-helmet** — [gotcha] CSP defaults are permissive — tighten for production

### Recent activity
- 3 notes updated in last 7 days: npm-fastify, npm-pino, brew-ripgrep

### Gaps worth filling
- Top undocumented dep: `undici`
- Run `/knowledge-gaps` for full coverage analysis
- Run `/intel undici` to document the top gap
````

### 7. Suggest next steps

Based on the brief:
- If undocumented deps exist in the detected stack: suggest
  `/intel <pkg>` for the top one
- If no manifest files found: suggest running in a project directory
- If knowledge graph is empty for all detected ecosystems: suggest
  `/knowledge-gaps` first, then batch `/intel`
- If all deps are documented: note good coverage, suggest checking
  for staleness with the knowledge-gardener agent
