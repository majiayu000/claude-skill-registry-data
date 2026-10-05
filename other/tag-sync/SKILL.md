---
name: tag-sync
description: "This skill should be used when the user asks to 'manage tag vocabulary', 'update raindrop tags', 'sync tag vocabulary', 'curate tags', 'refresh tags file', 'rebuild tag vocabulary', 'what tags should I use', 'tag reference', 'raindrop tag vocabulary', 'create tags reference', 'tag inventory', 'tag sync'. Fetches the user's Raindrop tags, selects the top N by usage count, adds one-line characterizations, groups them by cluster, and writes or syncs the vocabulary file at ~/.claude/references/raindrop-tags.md."
user-invocable: true
argument-hint: "[count|--reset]"
allowed-tools:
  - Read
  - Write
  - mcp__raindrop__find_tags
  - mcp__raindrop__find_bookmarks
---

# Tag Sync

Fetch tags from Raindrop, curate the top N by usage, characterize each with
a one-line description, and write or sync the vocabulary file. Follows the
vendor-sync pattern: registry (vocabulary file) -> fetch from external
(Raindrop API) -> diff against local -> preview -> apply after approval.

The output file at `~/.claude/references/raindrop-tags.md` is consumed by
`/session-bookmarks` when selecting tags for new bookmarks.

## Arguments

- `/tag-sync` — sync existing vocabulary (or create if no file exists)
- `/tag-sync 100` — set tag count to 100, then sync/create
- `/tag-sync --reset` — force full recreation (re-characterize + re-cluster all)

## Edge Cases

- **Raindrop MCP unavailable** — report error and exit. Do not write a partial file.
- **`find_tags` returns fewer than `tag_count`** — use all available tags. Store
  the actual count in frontmatter so the next sync has a realistic target.
- **`ai-bookmarked` not in top N** — always inject it regardless of rank. It is
  listed in `mandatory_tags` frontmatter.
- **No bookmarks found for a tag** (characterization step) — infer from tag name
  alone. Flag with `*` in preview: `*auto-inferred from name`.
- **`~/.claude/references/` directory missing** — create it before writing.
- **Vocabulary fetched today, no explicit args** — warn: "Vocabulary was
  already synced today. Pass a count or `--reset` to force." Do not re-fetch.
- **User declines all changes** — report "No changes made" and exit.

## Workflow

### Step 1: Parse arguments

Accept an optional integer argument or `--reset` flag.

- Integer sets `tag_count` (how many tags to include).
- `--reset` forces creation mode even if the file exists.
- No argument: use `tag_count` from existing file, or default 75.

### Step 2: Load existing vocabulary

```
Read(file_path="~/.claude/references/raindrop-tags.md")
```

- **File exists** — enter **sync mode**. Extract `tag_count`, `fetched_at`,
  and existing tag entries (tag name, count, characterization, cluster).
  Also extract optional config fields from frontmatter: `blocklist`,
  `context_tags`, `conventions`. **Preserve these unchanged through the
  sync cycle** — they are user-authored config, not Raindrop-derived data.
  Record which of the three are *absent* from frontmatter — Step 8 will
  backfill them from the seed values defined below.
  Check staleness: if `fetched_at` matches today's date and no explicit
  arguments were passed, warn "Vocabulary was already synced today. Pass a
  count or `--reset` to force." and **Stop.** Do not proceed to Step 3.
- **File missing** (or `--reset`) — enter **creation mode**. Seed default
  config fields: `blocklist: ["5", "4", "3", "2", "imported", "toread",
  "unread", "for:*"]`, `context_tags: []`, `conventions: []`.

### Step 3: Fetch tags from Raindrop

```
mcp__raindrop__find_tags()
```

Returns tags with usage counts. Paginate if `has_more=true`. Sort by count
descending. Take the top `tag_count` entries. Always include `ai-bookmarked`
in the target set regardless of rank.

### Step 4: Diff (sync mode only)

Compare target set against existing vocabulary:

| Category | Action |
|----------|--------|
| **New tags** (in Raindrop, not in file) | Must characterize (Step 5) |
| **Dropped tags** (in file, below threshold now) | Candidate to remove |
| **Retained tags** (in both) | Keep characterization, update count |
| **Count-only changes** | Apply silently, no user action needed |

If no new tags and no dropped tags (only count changes), report "Tag
vocabulary is in sync — only usage counts updated" and offer to apply
count updates in place.

### Step 5: Characterize new tags

For each new tag (creation mode: all tags; sync mode: only new arrivals),
sample 2-3 bookmarks to ground the description:

```
mcp__raindrop__find_bookmarks(has_tags=["<tag-name>"], limit=3, sort="random")
```

From bookmark titles and excerpts, write a concise one-line characterization
(10-15 words max). If `find_bookmarks` returns empty, infer from the tag
name (e.g., `conways-law` -> "Org structure effects on system architecture").

Do NOT call `find_bookmarks` for tags that already have characterizations
in the existing file (sync mode).

### Step 6: Assign clusters

Four groups:

| Cluster | What goes here |
|---------|---------------|
| **Ecosystem** | Language, framework, platform, tool names |
| **Architecture** | Design patterns, methodology, structural concepts |
| **Content Type** | Article genre, reference type, quality tier |
| **Other** | Anything that doesn't clearly fit above |

- **Retained tags** keep their existing cluster (stability across syncs).
- **New tags** are auto-assigned from name + sample bookmark content.
- `--reset` forces re-assignment of all clusters.

### Step 7: Preview

Show the proposed state before writing.

**Creation mode** — full vocabulary table grouped by cluster.

**Sync mode** — diff summary first, then full table:

````markdown
## Tag Vocabulary Preview

**Mode:** Sync | **Count:** 75 | **Fetched:** 2026-04-06

### New tags to add (3)

| Tag | Count | Cluster | Characterization |
|-----|-------|---------|-----------------|
| `basis-ecosystem` | 12 | Architecture | Foundational stack choices and tradeoffs |

### Tags to remove (1)

| Tag | Count | Cluster | Characterization |
|-----|-------|---------|-----------------|
| `old-unused-tag` | 2 | Other | Below threshold |

### Count updates (silent, no approval needed)

- `javascript`: 398 -> 412
- `nodejs`: 280 -> 287

### Summary after changes

75 tags: 31 Ecosystem | 24 Architecture | 12 Content Type | 8 Other

Approve all, or specify adjustments (e.g. "keep old-unused-tag",
"move basis-ecosystem to Content Type", "change characterization for X").
````

Wait for user response before writing.

### Step 8: Write

After approval, build the complete file and write atomically:

```
Write(file_path="~/.claude/references/raindrop-tags.md", content="...")
```

Full-file overwrite (not incremental edit). Create `~/.claude/references/`
directory if it does not exist.

**Reincorporate preserved config fields** into the written file's YAML
frontmatter. Do not overwrite or strip `blocklist`, `context_tags`, or
`conventions` — these are user-authored and must survive the sync cycle.

**Additively heal pre-seeding vocab files.** If sync mode encountered a file
that pre-dates the Step 2 seeding behavior, one or more of `blocklist`,
`context_tags`, or `conventions` will be absent from the frontmatter
extracted in Step 2. For each of these three fields, apply this rule when
building the written frontmatter:

- **Field present** (even if empty — `blocklist: []` or `blocklist:` with no
  value) — preserve as-is. Treat presence as an intentional user choice.
- **Field absent** (key not in the frontmatter at all) — backfill with the
  Step 2 creation-mode seed value (the same defaults applied when seeding a
  new file: `blocklist: ["5", "4", "3", "2", "imported", "toread", "unread",
  "for:*"]`, `context_tags: []`, `conventions: []`).

Healing is additive only — never replace, merge, or augment an existing
field's contents. The three fields are evaluated independently (a file may
have `context_tags` set but be missing `blocklist`). Mention any healed
fields in the Step 9 report so the user sees what was backfilled.

### Step 9: Report

````markdown
## Tag Vocabulary Synced

File: ~/.claude/references/raindrop-tags.md
Tags: 75 (31 Ecosystem | 24 Architecture | 12 Content Type | 8 Other)
Mandatory: ai-bookmarked (always applied)

Changes: added 3, removed 1, updated 18 counts

Next: `/session-bookmarks` will use this vocabulary when creating bookmarks.
````

## Output File Format

The vocabulary file uses YAML frontmatter for machine-readable metadata
and markdown tables for human-readable content:

```markdown
---
tag_count: 75
fetched_at: 2026-04-06
mandatory_tags:
  - ai-bookmarked
blocklist:
  - "5"
  - "4"
  - "3"
  - "2"
  - imported
  - toread
  - unread
  - "for:*"
context_tags: []
conventions: []
---

# Raindrop Tag Vocabulary

Always include `ai-bookmarked`. Choose 2-5 additional tags per bookmark.

## Ecosystem

| Tag | Count | Characterization |
|-----|-------|-----------------|
| `javascript` | 412 | Core JS language, runtime, ecosystem |
| `nodejs` | 287 | Node.js server-side runtime and tooling |

## Architecture

| Tag | Count | Characterization |
|-----|-------|-----------------|
| `protocol-design` | 156 | Specs, RFCs, protocol architecture |

## Content Type

| Tag | Count | Characterization |
|-----|-------|-----------------|
| `foundational-text` | 89 | Seminal papers, essays, reference works |

## Other

| Tag | Count | Characterization |
|-----|-------|-----------------|
| `indieweb` | 67 | IndieWeb movement, ownership, POSSE |
```

