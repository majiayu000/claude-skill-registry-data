---
name: whats-new
description: Generate/update the public /whats-new/ weekly digest from merged-PR history across the DevRel repos. Use when asked to build, refresh, or produce the "What's New" report.
---

# What's New digest builder

Generates `hugo/data/whats_new.json` from the **merged pull requests** of the
repos listed in that file's `repos[]`. You (Claude) write the summaries. Runs
locally; the developer reviews and commits. No server infra.

## Prerequisites
- `gh` installed and authenticated (`gh auth status`).
- Run from the repo root.

## Steps

1. **Fetch pending PRs.** Choose a cutoff:
   - Normal refresh: default 90-day lookback (omit `--since`).
   - Explicit start (e.g. go-live): pass `--since <ISO-8601 UTC>`.

   ```bash
   node scripts/whats-new/fetch-prs.mjs \
     --data hugo/data/whats_new.json \
     --out /tmp/whats-new-pending.json
   # or, with an explicit cutoff:
   #   ... --since 2026-08-10T16:00:00Z
   ```
   Note any repos skipped (placeholder slug or unreachable) from the log.

2. **Read** `/tmp/whats-new-pending.json`. If empty, tell the developer there
   is nothing new and stop.

3. **Summarize each pending PR.** For every stub produce
   `{ "id", "category", "summary" }`:
   - `category` ∈ `Feature | Fix | Performance | Docs | Maintenance`. Use the
     conventional-commit prefix in the title as a hint (`feat`→Feature,
     `fix`→Fix, `perf`→Performance, `docs`→Docs; `chore/refactor/build/ci/test/
     style`→Maintenance) but reclassify from the actual PR body when it's clearer.
   - `summary`: ONE plain-language sentence describing the change and, where
     possible, its value to a developer using the platform. Strip issue numbers,
     internal ticket refs, deploy/CI mechanics, and jargon. Community voice.
   - Optionally override the display `title` with a cleaner one via a `title`
     field (otherwise the PR title is used).
   Write the array to `/tmp/whats-new-summaries.json`.

4. **Merge** into the data file:
   ```bash
   node scripts/whats-new/merge.mjs \
     --data hugo/data/whats_new.json \
     --pending /tmp/whats-new-pending.json \
     --summaries /tmp/whats-new-summaries.json
   ```

5. **Report** to the developer: how many new entries, which repos, which weeks.
   Remind them to review `hugo/data/whats_new.json` and commit it. The page
   ships through the normal build/deploy pipeline (this skill does not deploy).

## Notes
- Idempotent: PRs already in the file are never re-summarized (wording stays put).
- On Windows, use a temp dir you can write to instead of `/tmp` if needed.
