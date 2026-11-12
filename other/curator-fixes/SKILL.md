---
name: curator-fixes
description: >
  The curator's supplemental diagnostic checks, the nine safe auto-fixes, the
  automatic judgment-fix procedure, and the lint-report template for
  claude-wiki-pages. Documents what the curator checks and how it repairs wiki
  structure under a git checkpoint, so the curator agent can apply fixes without
  inlining the catalog. Trigger when an agent or user asks "what does the curator
  check/fix", "how are wiki lint issues repaired", or invokes
  /claude-wiki-pages:curator-fixes. Reference, not action.
allowed-tools: Read
disable-model-invocation: true
---

# Wiki Curator — Checks & Fix Catalog (reference)

The supplemental diagnostic checks, the Phase 3 auto-fix catalog, and the
Phase 4 judgment-fix procedure for `claude-wiki-pages-curator-agent`. The agent
reads this skill during Phase 1 (diagnose) and Phases 3–4 (apply). Schema
authority remains `vault/CLAUDE.md`; the contract, engine-heal preflight,
severity classification, re-verify, report, and hard rules live in the agent
body.

## Supplemental checks (Phase 1.2 — not covered by the script)

Run each via `Grep`/`Glob` against `vault/wiki/`:

- **Broken wikilinks** — `[[Target]]` where `Target` matches neither any page's `title:` nor any entry in `aliases:`.
- **Orphan pages** — non-bookkeeping pages (excluding `index.md`, `log.md`, `dashboard.md`, folder notes, and legacy `_index.md`) with zero inbound wikilinks (index `children:` counts).
- **Title collisions** — two pages with the same `title:` → ambiguous wikilinks.
- **Title missing from `aliases`** — for every page: `title` must appear as the first entry in `aliases` (ghost-node prevention per `vault/CLAUDE.md`).
- **Missing graph color groups** — for each top-level topic folder (not `_sources`, `_synthesis`), check `obsidian eval code="JSON.stringify(app.internalPlugins.plugins['graph'].instance.options.colorGroups)"` for a matching `path:wiki/<folder>` query.
- **Flat folder sprawl** — any topic folder with > 12 direct `.md` children (excluding the folder's own index note).
- **Excessive nesting** — any folder deeper than 4 levels from `wiki/`.
- **Stale confidence** — pages with `confidence < 0.5` and `updated` > 30 days ago.
- **High confidence with single source** — pages with `type: entity | concept | synthesis` where `confidence ≥ 0.8` and `sources:` has only one entry.
- **Ghost wikilinks in `log.md`** — `[[...]]` targets in log entries that match no real page → should be replaced with backtick code formatting.

Heavier computational checks (Jaccard similarity for near-duplicate bodies, content-block deduplication) are **not** run from this agent. If the user wants them, extend `verify-ingest.sh` with `--deep` mode in a separate change.

## Stale agent-session memories (no memory-specific auto-deletion)

A `source_type: agent-session` page in `wiki/_sources/` is a first-class source
note subject to the same lifecycle as every other source. The curator handles
stale agent-session memories exactly like any stale page — there is no
memory-specific deletion path, no separate staleness field, and no parallel
staleness mechanism. The standard tools apply:

- **`status: stale` + `confidence`** — when an S4 WARN or 30-day calendar
  staleness finding targets a wiki page whose `sources:` list includes an
  agent-session source, the curator sets `status: stale` on the wiki page and
  may lower `confidence`, the same mutation it applies to any stale page.
- **Agent-session source note itself** — if the session source is unconfirmed
  past the staleness threshold or contradicted by newer sources, the curator
  sets `status: stale` on the source note and lowers `confidence` to reflect
  reduced evidentiary weight. This is flag-and-decay, not deletion.
- **No memory-specific auto-deletion** — the curator never auto-deletes an
  agent-session source note. Deletion of any page (including stale session
  memories) requires explicit editorial intent from the user, surfaced as a
  report-only item.

In all cases the curator uses `status: stale` and `confidence` — the canonical
lifecycle fields defined in `vault/CLAUDE.md` — with no new field and no
parallel staleness system.

## Phase 3 — Auto-apply safe fixes

Execute in order. Each fix is idempotent and content-preserving.

### 3.1 Wrap plain-string `sources:` in wikilinks

For every page where `sources:` contains entries not in `[[...]]` form:

1. Read the file.
2. For each non-wikilink entry, search `wiki/_sources/` for a page with matching `title:`.
3. If found, wrap as `"[[Title]]"`. If not, **do not wrap** — surface as a report-only item.

Same rule for `related`, `contradicts`, `supersedes`, `depends_on`, `scope`, `parent`, `children`, `child_indexes`.

### 3.2 Fill missing `parent:` / `path:`

For every page missing `parent:` or `path:`:

1. Determine the containing folder (relative to `wiki/`).
2. Set `path:` to that folder path.
3. Set `parent:` to the folder's folder-note title (the folder note is `<folder>/<folder>.md`; legacy `_index.md` if present), wrapped as `"[[Title]]"`.
4. Special cases: `_sources/` and `_synthesis/` → `parent: ""` and `path: "_sources"` / `"_synthesis"`. Top-level folder notes → `parent: "[[Wiki Index]]"`.

### 3.3 Add `title` to `aliases` (ghost-node prevention)

For every page where `title` is not the first entry in `aliases`:

1. If `aliases` is missing or empty, create it with `title` as the first entry.
2. Otherwise prepend `title`. Keep all existing aliases.
3. For folder notes, also add topic-name variants (kebab-case slug, Title Case, common abbreviations).

### 3.4 Repair folder-note children drift

For every per-folder index — the folder note (`<folder>/<folder>.md`), or legacy `_index.md` if present:

1. List actual `.md` files in the folder (excluding the index note itself).
2. **Add missing** titles to `children:`.
3. **Remove stale** entries from `children:` that have no matching file.
4. **Add missing body entries** — children listed but not mentioned in the index body get a `- [[Title]] — summary` line.
5. **Populate `child_indexes:`** from subfolders that have an index note (folder note, or legacy `_index.md`), as quoted `"[[wikilink]]"` entries.

### 3.5 Repair `wiki/index.md`

1. Read every wiki page's `title:` and `type:`.
2. **Add missing** under the correct heading:
   - `type: source` → `## Sources`
   - `type: entity | concept` → under the topic heading in `## Topics`
   - `type: synthesis` → `## Synthesis`
3. **Remove stale** entries with no matching file.
4. **Deduplicate** repeated titles.

### 3.6 Clean ghost wikilinks in `log.md`

For each `[[Target]]` in `log.md` where `Target` matches no real page title/alias, replace with backtick code formatting (e.g., `` `_index` ``).

### 3.7 Resolve broken and ghost wikilinks (safe paths only)

Always rewrite to **piped basename form** `[[file-basename|Display]]` — never to a
page's bare `title:`. Obsidian resolves a written link by path/basename only, so a
bare `[[Title Case]]` link relying on alias/title is itself a ghost node.

For each **ghost** link (a `wikilink-ghost` finding from the verifier §1.1b —
resolves only via `alias:`/`title:`, not path/basename):

1. The finding names the file it resolves to. Rewrite the link to that file's
   basename in piped form, preserving the existing display text:
   `[[Context Engineering]]` → `[[context-engineering|Context Engineering]]`.
2. If the bare target's basename is not unique vault-wide, path-qualify instead.

For each **broken** (dangling) `[[Target]]` that resolves to nothing:

1. **Alias / unique-fuzzy match** — if exactly one page matches `Target` via its
   `aliases:`, or via a case-only/hyphen-only difference, rewrite the link to that
   page's basename in piped form `[[file-basename|Display]]`.
2. Anything else → leave the link, surface in the report-only list. Do **not** create stub pages. Do **not** delete the link.

### 3.8 Connect orphan pages (link-only, non-destructive)

For each orphan page:

1. Find the containing folder's folder note (or legacy `_index.md`). If the page is not in the body, add `- [[file-basename|Title]] — summary` (piped basename, not a bare `[[Title]]`).
2. For sibling pages in the same folder sharing 2+ sources, add this page to their `related:`.

**Do NOT auto-edit `sources:` fields to connect `type: source` orphans.**
Mutating `sources:` forges a provenance claim the user never made and is the
exact drift `SECURITY.md` calls out. Surface every unlinked `type: source`
orphan as a **Report-only** item with candidate pages suggested in the report
(most relevant concept/entity pages found by grep over body text + shared
entities). The user — not this agent — decides whether the source actually
backs the target page.

Never delete an orphan. Unresolvable orphans stay as report-only items.

### 3.9 Add missing graph color groups

For each top-level topic folder without a matching `path:wiki/<folder>` color group:

1. Read current groups via `obsidian eval`.
2. Pick the next unused palette color per `/claude-wiki-pages:obsidian-graph-colors`.
3. Insert before the `_sources` / `_synthesis` special groups (there is no index catch-all — folder notes take their topic's color; never add groups for `raw/`, `_templates/`, or `_proposed/` — those paths are excluded from Obsidian's index).
4. Apply via `obsidian eval` + `graph.saveOptions()`.

## Phase 4 — Judgment fixes (automatic, under the checkpoint)

Judgment fixes apply **automatically** — there is no approval prompt. The
preflight `engine.sh heal` already wrote a git checkpoint, so every change here
is reversible with `git revert <healCommit>`. Record what you do in a
heal log at `vault/output/_heal-log-YYYY-MM-DD.md` (a record, not a request):

```
# Lint plan — YYYY-MM-DD

## Flat folders to restructure (WARN: >12 children)
<folder-a>/ (18 pages) → proposed:
  <folder-a>/subtopic-x/  (<n> pages: <list>)
  <folder-a>/subtopic-y/  (<n> pages: <list>)

## Title collisions to resolve (ERROR)
- "<Title>" appears in: <file-a>, <file-b>
  Proposal: rename <file-b> to "<Title> (Context)"

## Body wikilinks to densify (INFO, opt-in)
- N mentions across M pages

## Mergeable near-duplicates (INFO, opt-in)
- <page-a> and <page-b> (Jaccard ≥ 0.6) — canonical: <page-a>

## Summary
- git mv: N
- frontmatter rewrites: N
- body edits: N
```

Then execute the changes directly:

1. **Backlink-safe rename first (renames and moves).** For each rename or move, try
   `bash ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-rename.sh --target <vault> --from <old-rel.md> --to <new-rel.md>`.
   - **Exit 0** — Obsidian performed the rename and updated every `[[wikilink]]`
     backlink from its metadata cache: **skip the manual body-wikilink rewrite
     for that page** (title-collision renames especially — that is the
     error-prone rewrite this path eliminates). Note: the CLI write bypasses
     the PreToolUse hooks, which is why the Phase 5 re-verify below is
     mandatory, not optional.
   - **Exit 3** (`[skip] cli-rename: obsidian-cli unavailable`) — fall back to
     the manual sequence: `git mv`, then for a **rename** also rewrite the old
     `[[Title]]` body wikilinks across pages (folder **moves** don't break
     title-based wikilinks).
   - **Exit 2** — argument error; fix the paths, do not fall back blindly.
2. **Frontmatter and indexes (both branches — Obsidian does not know our schema).**
   Update `parent:`/`path:` on every moved page. Update the parent folder note
   (`children:` / `child_indexes:`). Update `wiki/index.md`.

After executing, re-run `engine.sh verify --json`; if errors remain, iterate once more, then surface any residual that genuinely needs editorial intent (deletions, ambiguous merges) for the user — do not guess at intent.

Tell the user where the rollback point is:

```
Applied N judgment fixes (restructures, merges, densification) automatically.
Reversible: git revert <healCommit>   (or: git checkout <checkpoint>)
Heal log: vault/output/_heal-log-YYYY-MM-DD.md
```

## Phase 6 — Report template

Print this report (the agent body summarizes the section list):

```
## Lint & Fix report

### Diagnosis
- Errors: N   Warnings: N   Info: N

### Classification
- Repaired by engine: N
- Auto-applied: N
- Judgment fixes applied: N
- Surfaced for review: N

### Auto-fixes applied
- sources fields wrapped: N
- parent/path filled: N
- titles added to aliases: N
- folder-note children repaired: N
- wiki/index.md repaired: N
- ghost wikilinks in log.md cleaned: N
- broken wikilinks auto-resolved: N
- orphans connected: N
- graph color groups added: N

### Judgment fixes applied (automatic, under checkpoint)
<list with before/after>

### Surfaced for review (editorial intent required)
<list each item with file path>

### Verification
- engine verify errors: before N → after N
- engine verify warnings: before N → after N
- Rollback: git revert <healCommit>  ·  Heal log: vault/output/_heal-log-YYYY-MM-DD.md
```
