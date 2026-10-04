---
name: kickstart-backfill
description: One-shot Day-1 backfill that pre-fills an empty vault from one to six months of calendar, Drive and Slack history, creating people, project, meeting and decision notes in dependency order. Use when the user says "kickstart", "backfill", "initialize the vault", "pre-fill with the last three months". Single use — after that, daily-digest keeps the vault current.
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, bootstrap, ingestion]
    related_skills: [meeting-ingest, doc-ingest]
    requires_toolsets: [second_brain, second_brain_sources]
---

# Kickstart backfill (Hermes edition)

Months of history do not fit in one context window, so this skill never tries. It runs one batch,
records it, and stops. Interrupting it is safe; rushing it is not.

1. `sb_brief`, then confirm the range with the user (three months is the usual sweet spot) and which
   sources to use.
2. `sb_backfill_plan(since="YYYY-MM-DD", until=<optional>, sources=[...])`. It writes a state note and
   returns `remaining` batches. If `resuming` is true, say which batch you are picking up.
3. Run **one batch**, the first entry in `remaining`. Do not run ahead, even if the batch is small.
   - `people` and `projects` batches come first and cover the whole range: they are the deduplication
     foundation. Get them wrong and every later batch multiplies the error.
   - Fetch the window from the configured sources: `sb_calendar`, `sb_drive_changes`, `sb_slack`.
4. Per batch phase:
   - **people** → recurring participants only (three or more interactions, or a 1-1). `sb_find_person`
     each name first. **Ask the user before creating any person note**, in one grouped question, not
     one question per name.
   - **projects** → recurring work threads with a name the user would recognise. One note each.
   - **meetings** → only those with a transcript or a real outcome. A status call with no decision is
     noise; skip it and say how many you skipped. Follow `/meeting-ingest` for each.
   - **decisions** → decisions actually made and still live. `05-decisions/` is append-only from
     the moment the note exists.
   - **knowledge** → patterns that recur across the range, not one-offs. Then hubs via `sb_curate`.
5. Every backfilled note carries the `(Backfilled)` marker in its timeline entries and
   `ingestion-mode: auto` in frontmatter, so later skills can tell reconstruction from live capture.
6. Dates come from the source. When a date is not in the source, write `unknown` — never infer one
   from context, and never use today's date for a past event.
7. `sb_commit("backfill: <batch id>")`, then `sb_backfill_done(batch_id)`.
8. Report: what the batch produced, what you skipped and why, and the next batch id. Then **stop**.
   Tell the user to run `/kickstart-backfill` again for the next batch, in a fresh session.
9. When `remaining` is empty: run `sb_maintain(scope="all")`, commit, and say the vault is live —
   from here on `daily-digest` keeps it current.
