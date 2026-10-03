---
name: knowledge-base-update
description: Knowledge base sync and health check for the knowledge-base skill. Scans all topic folders, regenerates index.md from every summary's frontmatter so new documents appear and rows for deleted files drop out, refreshes topic descriptions, cleans up stale split directories, and reports health issues (missing summaries, naming inconsistencies, orphaned files, duplicate content). Triggers on "kb update", "kb up", "update kb", and "kb sync".
when_to_use: Use when the user asks to update, sync, or health-check a knowledge base that already exists, so the index is rebuilt from the summaries currently on disk and the corpus is reported on. Use knowledge-base instead when new material is being processed from the inbox, when a question is being answered from the corpus, when it is being searched, or when pipeline output is being filed into a topic folder.
allowed-tools: Bash(python*), Bash(pip*), Bash(ls*), Bash(mv*), Bash(cp*), Bash(mkdir*), Bash(find*), Bash(wc*), Bash(file*), Bash(grep*), Bash(rm -rf *_build/split_*), Bash(rmdir*), Bash(kb-index*), Bash(kb-search*), Bash(kb-recents*), Read, Write, Edit, Glob, Grep, Agent
model: sonnet
effort: medium
---

# Knowledge Base Update

Sync the `knowledge-base` skill's index with the contents of the knowledge base on disk, then run a health check. Companion skill to `knowledge-base`: where `knowledge-base` processes new documents one at a time and answers queries, this skill keeps the index honest and surfaces drift.

## Knowledge Base Location

Edit the path below to match the knowledge base root used by the `knowledge-base` skill on this system:

```
<knowledge-base-root>/
```

All paths in this skill are relative to that root. A common default is `~/knowledge-base/`.

## Directory Structure

The knowledge base supports two document storage patterns:

**Pattern A: Per-document subfolder** (the default for all new filing: the `knowledge-base` Process Inbox mode, `kb move`, and every content pipeline that writes into the knowledge base)
```
<knowledge-base-root>/
├── topic-folder/
│   ├── 2026-01-28 Author. Title/
│   │   ├── 2026-01-28 Author. Title.pdf
│   │   ├── 2026-01-28 Author. Title_text.md
│   │   ├── 2026-01-28 Author. Title_summary.md
│   │   └── 2026-01-28 Author. Title_slides.pdf
```

**Pattern B: Flat files** (legacy; nothing produces this any more, and every reader still handles it)
```
<knowledge-base-root>/
├── topic-folder/
│   ├── 2026-03-18 Author. Title.pdf
│   ├── 2026-03-18 Author. Title_text.md
│   └── 2026-03-18 Author. Title_summary.md
```

Expect most of a working knowledge base to be Pattern A and a shrinking tail of it to be Pattern B. A Pattern B item is not a defect and is never flagged as one; a slides run promotes one to Pattern A when it touches it.

Topic folders are dynamic: any immediate subdirectory of the knowledge base root other than the inbox folder, any blog folder, any auxiliary folders (for example, a recents or symlink folder, a search-index or database folder, or a documentation folder that describes the knowledge base process itself rather than holding indexable content), and any `*_build/` directory is a topic folder. When scanning, search both patterns:
- Flat: `<topic-folder>/*_summary.md`
- Subfolder: `<topic-folder>/*/*_summary.md`

**Reference material (`materials/` subfolders):** any subfolder named `materials/` at any depth inside the knowledge base is reference-only. Skip its contents entirely during sync and health checks. No scanning, no index entries, no missing-summary warnings, no naming checks. Use this to park files that should live inside a topic folder for proximity but are not indexable knowledge base content (third-party reference docs, working notes, artifacts from external projects).

**Intentional non-documents (`.kbskip` sentinel):** a folder that holds real files but is not a knowledge base document (a working capture, a parked external project) can carry a `.kbskip` file. Presence is what matters; the content is optional. The health check in Step 2 then does not flag it for a missing summary. It reports it under SKIP-SUPPRESSED instead, so nothing is silently dropped and a real document added later resurfaces. Unlike `materials/`, this moves and hides nothing: the folder stays where it is, and its content stays findable if it has a summary. Put the sentinel in the specific subfolder, never at a topic root. A root sentinel suppresses nothing and should be reported so it can be moved into the subfolder it was meant for.

## Index Format

`index.md` is a markdown table at the knowledge base root, derived from the `_summary.md` files rather than maintained by hand:

```markdown
| Date | Author | Title | Topic | Summary |
|------|--------|-------|-------|---------|
| 2026-03-18 | Last | Document Title | topic-folder | One-line summary of the document |
```

Each row comes from one summary's frontmatter, so the summaries are the source of truth and the table is the rendering. Regenerate rather than editing a row in place; a hand-edited row is the first thing to go stale, because nothing downstream knows it was changed. If you script the regeneration, the script owns the whole file; if you do not, have Claude rebuild the table from the frontmatter it reads. Either way the unit of work is the whole file, not one row.

**Summary cell rule:** the Summary cell is one sentence that locates and disambiguates the document. It does not summarize it, because the `_summary.md` holds the detail. Target 30 words or fewer. A single dense sentence carrying distinguishing figures may run longer, but it stays one sentence and never becomes a paragraph.

## Topics File Format

`topics.md` describes each topic folder:

```markdown
# Knowledge Base Topics

## topic-folder
One- to two-sentence description of what this folder collects.
```

## Update Steps

### Step 1: Sync the index

**`index.md` is generated from the summaries, so this step regenerates the whole table rather than editing rows into it.** Scan all topic folders. Do not descend into any subfolder named `materials/`; its contents are reference-only and must not appear in the index.

1. **Walk every `_summary.md` under both storage patterns** (`<topic-folder>/*_summary.md` and `<topic-folder>/*/*_summary.md`), render one row per file from its frontmatter, and write `index.md` in a single pass. A document appears because its summary exists, and a row for a file that is gone disappears because the walk no longer finds it, so adding and removing entries are not separate operations here.
2. **Report what changed** by comparing the row count and the stems before and after: N rows added, M rows dropped. That is the sync summary.
3. **A source file with no `_summary.md` produces no row.** Note it as a missing summary and report it; do not generate one, and do not write a placeholder row for it.

**Never append or hand-edit an individual row**, in this step or any other. A row edited in place disagrees with the summary that nothing knows was changed, and the next regeneration silently reverts it. To change what a row says, edit that item's frontmatter and regenerate. If the `knowledge-base` skill's index generator is wired on this system, run it and let it own the whole file; if it is not, Claude does the same walk by hand.

Update `topics.md` with current folder descriptions based on the contents of each folder. Existing descriptions are not overwritten if the folder's purpose has not changed; new folders get a draft description for the user to refine.

The refresh maintains decision tests, not just descriptions. If any filing was corrected since the last update, meaning a document was moved out of the folder it was first assigned, propose a one-line test that would have sent it to the right folder the first time. Where two topic descriptions would both plausibly claim a recent document, propose a test for that border. These are proposals; the user approves each `topics.md` edit.

### Step 1b: Clean up inbox build folder

Scan the inbox build folder (e.g., `<inbox>/<inbox>_build/`) for split directories (`split_*/`). For each split directory, check whether the corresponding source file still exists in the inbox. If the source file has already been moved out of the inbox (i.e., it no longer exists there), the splits are stale and can be deleted.

Present the list of stale split folders with their sizes, then delete them after confirmation. If the inbox build folder is empty after cleanup, remove it too with `rmdir`, which refuses on a folder that still holds anything. **Delete only `split_*` directories inside a `*_build/` folder; that is the one path shape `allowed-tools` grants, and nothing adjacent to it is a target.** Never delete a source file, a `_text.md`, a `_summary.md`, or the item folder itself.

### Step 2: Health check

Skip any path under a `materials/` subfolder. Report any issues found:

- **Missing summaries:** source files without a corresponding `_summary.md`. Flag a folder only when it actually holds a real source file or a non-empty source subfolder. A folder that is empty, holds only build artifacts, holds only a `materials/` subfolder, carries a `.kbskip` sentinel, or is already summarized is not a finding. Build output and a project state file such as `CLAUDE.local.md` are not sources. Without these guards the check reports the same false positives on every run, which is how a report stops being read.
- **Orphaned summaries:** `_summary.md` files without a corresponding source file
- **Naming inconsistencies:** files not matching the expected convention (the default is `YYYY-MM-DD Last. Title.ext`; adjust to whatever convention the `knowledge-base` skill uses on this system). Optional: if your knowledge base intentionally lets legacy and current naming conventions coexist permanently, turn this check off so it does not propose the same renames on every run. The same applies to empty or sparse topic folders kept as deliberate placeholders; do not flag them as defects.
- **Duplicate content:** files with very similar titles or content across different folders
- **Topic suggestions:** documents that might fit better in a different folder based on their summary content
- **Gaps:** topics with few sources where more research would strengthen the knowledge base

Offer to fix automatically where possible (e.g., move misplaced files, rename inconsistencies). Wait for user confirmation before making any moves or renames.

### Step 2b: Overflow re-homing review

Scoped to catch-all folders only, meaning the one or two topic folders that collect anything without an obvious home. The topic-suggestion check above already covers misfits everywhere else, so no other folder gets this sweep.

When a catch-all folder passes about 50 items, count by its `_summary.md` files across both storage patterns, read those items' frontmatter fields rather than the whole `index.md`, and propose specific re-homes into better-fitting topic folders. Approved re-homes run as normal move operations so the frontmatter, the index, and any search index stay in step. Below the threshold, skip this step silently rather than reporting that it did not run.

The threshold is a default, not a constant. It exists because a catch-all folder is fine while it is small and becomes a second unsorted inbox once it is large, and the review costs more than it returns until then.

## Constraints

- **Never delete original source files.** Rename and move only; never delete a source.
- **Never overwrite existing summaries.** If a summary already exists, skip unless the user explicitly asks to regenerate.
- **The summaries are the source of truth, not the index.** Regenerate the whole table from their frontmatter; never add, edit, or delete a row directly. Do not silently change what a summary says in order to change how a row reads.
- **Topic folders are user-created.** Suggest new folders but wait for approval before creating them.
- **Read-only on `materials/`.** Never index, scan, or report on anything under a `materials/` subfolder.

## Customization

This skill assumes the `knowledge-base` skill's directory and naming conventions. If your conventions differ, edit:

- The knowledge base root path at the top of this file
- The directory pattern descriptions if you use a different layout (e.g., topics nested under categories)
- The naming convention used in the health check
- The list of "skip" folder names (`aa-inbox/`, `aa-blog/`, `aa-recents/`, and any search-index or documentation folder) if yours are named differently
