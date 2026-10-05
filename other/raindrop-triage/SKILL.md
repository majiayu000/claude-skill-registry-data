---
name: raindrop-triage
description: "This skill should be used when the user asks to 'triage unsorted bookmarks', 'clean up raindrop inbox', 'sort unsorted', 'organize bookmarks', 'raindrop triage', 'process bookmark backlog', 'promote triaged bookmarks', 'classify triaged', 'raindrop cleanup', 'deduplicate bookmarks', 'find duplicate bookmarks', 'tag unsorted', 'process raindrop inbox'. Fetches unsorted Raindrop bookmarks, deduplicates by normalized URL, detects research bursts, clusters by theme, proposes vocabulary-grounded tags, cross-references burst topics against Basic Memory, then moves approved bookmarks to AI-triaged. A second invocation with --promote classifies AI-triaged items into AI-sorted (default), AI-gems (golden), AI-archive, or AI-attention."
user-invocable: true
argument-hint: "[--promote [--source <collection>]|--limit N]"
allowed-tools:
  - Read
  - mcp__raindrop__find_collections
  - mcp__raindrop__create_collections
  - mcp__raindrop__find_bookmarks
  - mcp__raindrop__update_bookmarks
  - mcp__raindrop__delete_bookmarks
  - mcp__basic-memory__search_notes
  - TodoWrite
---

# Raindrop Triage

Interactive triage of unsorted Raindrop bookmarks: deduplicate, detect research
bursts, cluster by theme, propose vocabulary-grounded tags, and move approved
bookmarks to AI-triaged. A second invocation with `--promote` classifies
AI-triaged items into AI-sorted (default), AI-gems (golden), AI-archive,
or AI-attention.

## Arguments

- `--promote` — run the promotion pass on AI-triaged bookmarks instead of
  the default unsorted triage
- `--source <collection>` — (promote only) override the default AI-triaged
  source. Use `--source unsorted` for pre-triaged bookmarks.
- `--limit N` — override the default 200-bookmark fetch limit

## Edge Cases

- **Empty unsorted / empty AI-triaged** — report "No bookmarks to triage" and
  exit cleanly.
- **Raindrop MCP unavailable** — report "Raindrop MCP unavailable — cannot
  triage" and exit. Do not attempt fallback.
- **Vocabulary file missing** — warn "Tag vocabulary not loaded — run
  `/tag-sync` first for consistent tagging." Continue with copy-from-similar
  only, but note degraded tag quality in the session summary.
- **>200 bookmarks** — triage the first page. Report remaining count and
  suggest re-running for the next batch.
- **Partial `update_bookmarks` failure** — report which bookmarks failed.
  Do not retry automatically — the user can re-run the skill.
- **BM unavailable** — skip the cross-reference step (Step 9). Note "Basic
  Memory unavailable — skipping knowledge gap cross-reference" in the summary.
- **Collection name collision** — if a non-AI collection named "AI-triaged"
  (etc.) already exists, report the conflict and stop. Do not create a
  duplicate.
- **Note field too long for attention append** — if the bookmark note exceeds
  10,000 characters after appending, warn the user and skip the append for
  that bookmark.

## AI-Managed Collection Namespace

This skill operates within the AI-managed collection namespace:

| Collection | Purpose | Created by |
|------------|---------|------------|
| AI-bookmarked | Session bookmark captures | `/session-bookmarks` |
| AI-triaged | Default landing zone for triaged unsorted bookmarks | This skill (lazy) |
| AI-sorted | Useful, organized bookmarks (the default promotion destination) | This skill (lazy) |
| AI-gems | Golden stuff — seminal papers, canonical references, high-reuse gems | This skill (lazy) |
| AI-archive | Low-reuse bookmarks (ephemeral shopping, dead pages, one-off lookups) | This skill (lazy) |
| AI-attention | Bookmarks needing human decision or further research | This skill (lazy) |

**CRITICAL:** Never write to user-curated collections. The user's existing
library must remain untouched by AI operations.

## Workflow — First Pass (default)

### Step 0: Parse arguments

Check for `--promote` flag. If present, jump to the Promotion Workflow below.
Parse `--limit N` (default 200).

### Step 0.5: Create progress checklist

Create a TodoWrite checklist to track progress through the triage workflow:

- `[ ] Load tag vocabulary`
- `[ ] Discover collections`
- `[ ] Fetch unsorted bookmarks`
- `[ ] Deduplicate`
- `[ ] Detect research bursts`
- `[ ] Check broken links`
- `[ ] Cluster by theme`
- `[ ] Batch triage (updated with batch count once known)`
- `[ ] Cross-reference bursts vs BM`
- `[ ] Session summary`

Mark each item complete as the corresponding step finishes.

### Step 1: Load tag vocabulary

```
Read(file_path="~/.claude/references/raindrop-tags.md")
```

Parse the vocabulary table into a lookup structure: tag name, count,
characterization, cluster. This file is produced by `/tag-sync` and contains
~150 curated tags.

If the file is missing, warn and continue — copy-from-similar (Step 8a) still
works, but tag consistency will be degraded.

**Freshness check:** Parse the `fetched_at` field from the vocabulary file's
YAML frontmatter. If older than 7 days, warn: "Tag vocabulary is N days old —
consider running `/tag-sync` first for best tag quality." Let the user decide
whether to continue or run `/tag-sync` first.

### Step 2: Discover AI-managed collections

```
mcp__raindrop__find_collections(search="AI-")
```

Check which AI-managed collections already exist. For this first pass, only
AI-triaged is needed. If it does not exist, create it lazily:

```
mcp__raindrop__create_collections(collections=[{title: "AI-triaged"}])
```

Record the collection ID for use in Step 8d.

If a collection named "AI-triaged" exists but is not in the AI-managed
namespace (i.e., it was created by the user for a different purpose), report
the conflict and stop.

### Step 3: Fetch unsorted bookmarks

```
mcp__raindrop__find_bookmarks(collection_ids=[-1], limit=200)
```

Collection ID `-1` is Raindrop's special identifier for unsorted bookmarks.

If 0 results, report "No unsorted bookmarks to triage" and exit.

If the result count equals the limit, note that more bookmarks may exist
beyond this page. Report the total and suggest re-running after this batch.

### Step 4: Deduplication (server + client)

#### Step 4a: Server-side duplicate detection

```
mcp__raindrop__find_bookmarks(collection_ids=[-1], is_duplicate=true)
```

Raindrop's server-side duplicate detection catches exact URL matches and
content-identical pages across the library. Collect these as the initial
duplicate set.

#### Step 4b: Client-side URL normalization

For each bookmark, compute a normalized URL by applying these transformations
in order:

1. Strip protocol (`https://`, `http://`)
2. Strip `www.` prefix
3. Strip known tracking parameters: `utm_*`, `fbclid`, `gclid`, `srsltid`,
   `referer` (when paired with `gclid`)
4. Strip anchor fragments (`#...`)
5. Collapse double slashes (`//` to `/`) in the path
6. Strip trailing slashes
7. Sort remaining query parameters alphabetically

Group bookmarks by normalized URL. For groups of 2+, these are duplicates.

Merge with the server-detected duplicates from Step 4a. Present the combined
set to the user, noting the detection source:

````markdown
## Duplicate Bookmarks Found

| # | Title | URL | Source | Created |
|---|-------|-----|--------|---------|
| 1a | Example Page | https://example.com/?utm_source=twitter | url-norm | 2025-12-15 |
| 1b | Example Page | https://example.com/ | server | 2026-01-03 |

Delete older duplicates (keep newest)? Or specify which to keep (e.g. "keep 1a").
````

For approved deletions:

```
mcp__raindrop__delete_bookmarks(bookmark_ids=[<older-ids>])
```

Remove deleted bookmarks from the working set before continuing.

### Step 5: Detect research bursts

Sort remaining bookmarks by creation timestamp. Walk the sorted list and group
consecutive bookmarks where each is within 30 minutes of the previous one.
Keep only groups of 3 or more — these are research bursts.

Present burst summary (informational, no approval gate):

````markdown
## Research Bursts Detected

**Burst 1** (2025-12-30, 14:20-15:45, 8 bookmarks): stylelint + CSS tooling
- stylelint-config-standard
- postcss-sorting
- stylelint-order
- ...

**Burst 2** (2026-01-15, 09:10-09:40, 4 bookmarks): React testing libraries
- React Testing Library docs
- Vitest integration guide
- ...

6 research bursts detected across 42 bookmarks.
Tag these with `research-burst` + topic tags during triage.
````

Tag each burst bookmark with `research-burst` in addition to topic tags
during the batch triage step.

### Step 6: Check broken links

```
mcp__raindrop__find_bookmarks(collection_ids=[-1], has_broken_link=true)
```

If any broken-link bookmarks are found, present them:

````markdown
## Broken Links

| # | Title | URL | Created |
|---|-------|-----|---------|
| 1 | Dead Product Page | https://defunct.example.com/product | 2024-06-12 |
| 2 | Expired Campaign | https://example.com/promo/2024 | 2024-11-30 |

Delete these broken bookmarks? (approve/skip/select by number)
````

Delete approved broken bookmarks and remove from working set.

### Step 7: Cluster by theme

Group remaining bookmarks into batches of 8-15 using this priority:

1. **Burst membership** — bookmarks in the same research burst stay together
2. **Domain affinity** — bookmarks from the same domain (e.g., `github.com`,
   `stylelint.io`) group together
3. **Title keyword overlap** — bookmarks with shared significant words in
   their titles cluster together
4. **Remainder** — bookmarks that don't cluster get grouped into a
   miscellaneous batch

Each cluster gets a descriptive label (e.g., "CSS Tooling", "GitHub Actions",
"Healthcare Standards").

### Step 8: Interactive batch triage

For each cluster, present a batch for user approval.

#### Step 8a: Propose tags

For each bookmark in the batch, propose tags following the strategy in
`references/tag-selection.md`.

#### Step 8b: Present batch table

````markdown
## Batch 3/7: CSS Tooling (research burst 2025-12-30)

| # | Title | Tags | Action |
|---|-------|------|--------|
| 1 | stylelint-config-standard | `css`, `linting`, `research-burst` | -> AI-triaged |
| 2 | postcss-sorting | `css`, `postcss`, `research-burst` | -> AI-triaged |
| 3 | stylelint-order | `css`, `linting`, `research-burst` | -> AI-triaged |

Approve all, edit tags (e.g. "2: add prettify"), skip batch, or quit?
````

#### Step 8c: Wait for user

Wait for user response before proceeding. Accept these responses:
- **approve** / **yes** / **all** — apply all proposed tags and move
- **edit** — modify specific tags (e.g., "2: add prettify, remove postcss")
- **skip** — skip this batch, move to next
- **quit** — stop triage, report progress so far

#### Step 8d: Apply approved changes

For each approved bookmark, execute TWO separate `update_bookmarks` calls
(split per upstream bug — combining `add_tags` with `collection_id` in one
call silently fails):

**First call — add tags:**

```
mcp__raindrop__update_bookmarks(updates=[{
  bookmark_ids: [<id1>, <id2>, ...],
  update: { add_tags: ["tag1", "tag2", ...] }
}])
```

Batch bookmarks with identical tag sets into a single update call (up to 100
per call).

**Second call — move to AI-triaged:**

```
mcp__raindrop__update_bookmarks(updates=[{
  bookmark_ids: [<id1>, <id2>, ...],
  update: { collection_id: <ai-triaged-id> }
}])
```

### Step 9: Cross-reference burst topics against Basic Memory

For each research burst detected in Step 5, search Basic Memory for coverage:

```
mcp__basic-memory__search_notes(query="<burst topic>", page_size=3)
```

Report knowledge gaps — burst topics with 0 or weak BM coverage:

````markdown
## Knowledge Gaps from Research Bursts

| Burst Topic | BM Coverage | Suggestion |
|-------------|-------------|------------|
| stylelint | 1 note (thin) | Run `/intel npm:stylelint` |
| react-testing | 0 notes | Consider `/intel` or concept note |
| GitHub Marketplace | 0 notes | Low priority — browsing, not research |
````

### Step 10: Session summary

````markdown
## Triage Summary

- **Processed:** 142 bookmarks
- **Duplicates deleted:** 8
- **Broken links deleted:** 3
- **Tagged and moved to AI-triaged:** 131
- **Research bursts:** 6 (42 bookmarks)
- **Knowledge gaps:** 3 topics with weak/no BM coverage
- **Remaining unsorted:** 0

Run `/raindrop-triage --promote` to classify AI-triaged bookmarks into
AI-gems, AI-archive, or AI-attention.
````

---

## Workflow — Promotion Pass (`--promote`)

When `--promote` is passed, follow
`references/promote-workflow.md`.

---

## Reference Files

- **`references/tag-selection.md`** — Tag proposal pipeline (A-F), tag axes,
  vocabulary-first principle, blocklist, and user conventions
- **`references/promote-workflow.md`** — Full promotion pass workflow (Steps 0-6)
  with classification examples and attention note format
