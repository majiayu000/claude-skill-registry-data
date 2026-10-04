---
name: updating-worklog-vault
description: Writes files in the ~/worklog SilverBullet vault. Use when logging a run, appending to a journal, or building a results table.
argument-hint: what to log, or the page to update
allowed-tools: Bash(cat:*), Bash(date:*), Bash(mkdir:*), Bash(cp:*), Bash(sed:*), Bash(head:*), Bash(tail:*), Bash(wc:*)
---

# Updating the worklog vault

Vault is `~/worklog`, plain `.md` on disk. The server watches the folder and
pushes to open browsers, so a file write is the whole mechanism — no API call.
For docs lookup, tags advice, and log prose conventions, use the `silverbullet`
skill instead; this one is only about writing.

**Before writing, read `/home/jke/worklog/CLAUDE.md`** — the vault's contract for
what an entry may contain (transcribe what the user said, concisely; numbers
verbatim; every entry findable by both tag and wikilink). It auto-loads only for
sessions whose cwd is `~/worklog`, so read it explicitly from anywhere else. This
skill governs *how* to write safely; that file governs *what* goes in.

## Rules

- **Append, never overwrite.** `cp page.md /tmp/page.bak` first, then
  `cat >> page.md <<'MDEOF'`. Say where the backup is.
- **Get the date from `date +%F`**, never from memory. Journal pages are
  `Journal/YYYY-MM-DD.md`.
- **Leave frontmatter alone** when appending to an existing page. Verify with
  `head -5` afterwards.
- **Replacing a section**: find its start with `grep -n '^## Heading'`, keep the
  prefix with `head -n $((start-1))`, append the new version. Do not sed in
  place across a multi-line block.
- **Quote the heredoc** (`<<'MDEOF'`) so `$req` and backticks survive. Pick an
  outer token that cannot appear in the content; `EOF` inside the body is safe
  as long as the outer token differs.
- A page open in the browser with unsaved edits can lose them to a disk write.

## Where things go

| Content | Location |
|---|---|
| Dated activity, one day's runs | `Journal/YYYY-MM-DD.md` |
| Anything outliving the day | topic page, e.g. `rbf-improve.md` |
| One record per artifact (a job, a run) | subfolder page, e.g. `simtest/<job-id>.md` |

Link the record from the journal rather than pasting it twice. Reverse links
show under Linked Mentions, so linking is the index.

## Results table style

Worked example — the table holds only what you scan and compare; anything long
lives on a linked page.

```markdown
## Simtest runs #simtest

| Time (PDT) | Job | Command | Scene set | Variant | Status |
| --- | --- | --- | --- | --- | --- |
| 11:31 | [g152dn4u](http://bates.corp.nuro.team/tasks/simtest/g152dn4u) | [[simtest/g152dn4u]] | aev_rbf_aev_from_behind | scope12_bce | RUNNING as of 11:36 |
```

- **External artifact → inline hyperlink** `[id](url)`, with the id as the link
  text so the cell is still readable as data.
- **Long reproducible content → wikilink** `[[folder/page]]`, never pasted below
  the table. Commands, configs, and output all belong on that page.
- **No `[[page|alias]]` in a table cell** — the pipe splits the cell. Rename the
  page instead. `displayName` frontmatter is honored only "in certain contexts",
  so do not rely on it for rendering inside a cell.
- **A status column is a snapshot.** Write "RUNNING as of 11:36", not "RUNNING",
  so a stale row reads as stale.
- **Timestamps**: convert to local and label the zone. Source-of-truth systems
  usually record UTC.
- **Tag the heading** (`## Simtest runs #simtest`) so rows are findable; table
  rows are also queryable via `index.tables()`.

## Record page shape

Frontmatter carries the queryable fields, body carries the evidence:

```markdown
---
tags: simtest
date: 2026-08-27
job: g152dn4u
commit: <full sha>
status: RUNNING
---
# simtest g152dn4u

[BATES task](<url>) · submitted 11:31 PDT · 8 subtasks

## Command

<fenced block with the exact command>

Where each field was verified from, so the record is auditable later.
```

State facts from the authoritative source (job metadata, resolved config), not
from terminal scrollback, and say which you used.
