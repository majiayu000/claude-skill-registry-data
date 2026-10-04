---
name: rapture-watch
description: Act on Rapture's triaged Markdown notes. Read each new .md note's frontmatter, take the action for its type, optionally send a summary via Telegram.
version: 0.2.0
author: Rapture for Mac contributors
license: Apache-2.0
platforms: [macos]
metadata:
  hermes:
    tags: [Productivity, Capture]
---

# Rapture watcher

Runs from a Hermes cron job. Acts on any new Markdown notes Rapture for Mac has triaged into your notes folder since the last run.

Rapture classifies every capture itself the moment it lands: each one becomes a `.md` note with YAML frontmatter (`captured`, `type`, optional `source` and `raw_media`), auto-titled `YYYY-MM-DD <Title>.md`, filed under `Notes/` (voice notes), `Links/` (YouTube/article links), and — when the user's AI tier is on — `Tasks/`, `Ideas/`, `Journal/`. This skill does no classifying. It reads the frontmatter and acts.

## Resolving the notes folder

At every invocation, resolve `$NOTES_FOLDER` in this order:

1. If `~/Library/Application Support/Rapture for Mac/output-folder.path` exists and is readable, use its contents (one absolute path, possibly with trailing newline — trim whitespace).
2. Otherwise default to `~/Documents/Rapture Notes/`.

This lets users change their notes folder in Rapture's Settings → General without re-creating the cron job or editing the skill.

## When to use

When a Hermes cron job invokes this skill against the resolved `$NOTES_FOLDER`.

## Procedure

1. List `*.md` in the top level of each triaged subfolder: `Notes/`, `Links/`, `Tasks/`, `Ideas/`, `Journal/`. Don't recurse into `Links/Media/` — those are fetched transcript/article artifacts, not notes.
2. Skip any `*.tmp` files (Rapture's in-flight atomic writes) and skip any note whose folder-relative path already appears in `$NOTES_FOLDER/processed-log.md` (grep it; that log is the watermark — notes stay where the app filed them).
3. For each remaining note, ordered by mtime ascending:
   1. Read it. The frontmatter's `type` (`voice-note`, `youtube-link`, `article-link`, `task`, `idea`, `journal`) is the app's classification; use it directly. `captured` is the UTC dictation instant. If the body has a `## Raw` section, that's the verbatim dictation; quote from it when exact wording matters.
   2. Take the action for its type (below).
   3. Append the note's relative path to `$NOTES_FOLDER/processed-log.md` with a shell `>>` append.
4. Send a single summary message via the cron job's configured delivery channel: `📥 Processed N notes: <task: 3, journal: 1, ...>`. Suppress when N = 0. (Hermes' delivery default is `local` / CLI; the cron job must pass `--deliver telegram` or similar for the summary to reach a messaging channel.)

## Actions by type

- **task**: append to `$NOTES_FOLDER/inbox/todos.md` as a Markdown checkbox: `- [ ] <text>  (captured <iso-ts>)`. If the note mentions a date, prepend it.
- **idea**: append a one-line pointer to `$NOTES_FOLDER/inbox/ideas.md`: `- <filename> — <one-sentence gist>  (captured <iso-ts>)`.
- **journal**: nothing per-note. Count it in the summary.
- **youtube-link / article-link**: if the note body has a `Media:` link, Rapture's link enrichment already fetched the transcript/readable text into `Links/Media/` — summarize from that artifact if the summary channel wants substance; don't re-fetch. If there's no `Media:` link, include the note title and URL in the summary so the user can follow up.
- **voice-note**: if clearly actionable ("email Sarah about the deck"), treat as a task. Otherwise just log it; it's already filed and searchable.

## Pitfalls

- Don't process `*.tmp` files. Skip them.
- Don't process root `*.txt` files. In the default mode, Rapture converts any `.txt` at the folder root to a Markdown note within seconds and deletes it — racing that conversion loses.
- Don't edit, move, rename, or delete the triaged `.md` notes. The log entry, not a move, marks a note handled.
- If `$NOTES_FOLDER` doesn't exist, exit cleanly with a message in the summary.
- If the sidecar exists but contains an unreadable / nonexistent path, fall back to the default.
- Rapture for Mac already sends the `✅ Saved` confirmation in the iMessage thread when each capture lands, so this skill's delivery channel is for the *processing* summary, not the per-capture acknowledgement.

## Raw mode

If the user has flipped Rapture's **Settings → Triage → Filing** to **"Raw text files, no triage"**, the triaged subfolders don't fill: captures are `<ISO-timestamp>.txt` files at the folder root, never converted. Only in that mode, fall back to the old contract: list root `*.txt`, classify each yourself, take the equivalent action, and move the source to `$NOTES_FOLDER/processed/YYYY-MM/<original-filename>`.

## Verification

After install + cron setup, dictate a Siri test note to yourself. Within the next cron tick (5 minutes by default), you should see a Telegram message summarizing one processed note, and the corresponding `.md` note (e.g. `Notes/2026-07-13 <Title>.md`) should be listed in `processed-log.md`.
