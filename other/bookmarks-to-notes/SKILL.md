---
name: bookmarks-to-notes
description: Exports your daily.dev bookmarks to Markdown notes for Obsidian, Logseq or any folder of files, one note per post with summary, tags and source, and syncs only what's new on later runs.
---

# Bookmarks to Notes

Your bookmarks belong in your second brain. This skill writes each saved post as a Markdown note and keeps the folder in sync.

## Requirements

One of:

- The daily.dev MCP server (`https://api.daily.dev/mcp`) connected to your agent, or
- A daily.dev personal access token in `DAILY_DEV_TOKEN` (https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

The agent needs write access to a local folder the user names, for example an Obsidian vault subfolder.

Each step lists the MCP tool first and the REST call after it.

## Steps

1. **Pick the target folder** from the user. Create `<folder>/.dailydev-sync.json` on first run; it stores `lastBookmarkedAt` and the ids already exported.
2. **Fetch bookmarks newest first.** `getBookmarks` with `limit` 50 (`GET /bookmarks?limit=50`). Each post carries `bookmarkedAt`. Keep paging with `cursor` until you reach a post whose `bookmarkedAt` is at or before `lastBookmarkedAt`, or until `hasNextPage` is false. On the first run export everything (or the number the user asks for). Pass `listId` (from `getBookmarksLists`, `GET /bookmarks/lists`) to export one folder only.
3. **Write one note per post** that isn't already exported. Filename: `<YYYY-MM-DD>-<slugified title>.md`, using `bookmarkedAt` for the date. Content:

   ```markdown
   ---
   title: "<title>"
   url: <url or commentsPermalink>
   source: <source.name>
   tags: [<tags>]
   bookmarked: <bookmarkedAt>
   published: <publishedAt or createdAt>
   read_time: <readTime>
   upvotes: <numUpvotes>
   dailydev: <commentsPermalink>
   ---

   <summary>

   [Read the article](<url>) · [Discussion on daily.dev](<commentsPermalink>)
   ```

   Use the vault's tag convention if the user has one, for example `#tag` lines or a `tags:` list; keep daily.dev tag slugs as they are.
4. **Update the state file** with the newest `bookmarkedAt` seen and the exported ids.
5. **Report**: how many notes were created, the folder, and the first few titles.

## Output

A one-paragraph summary. Don't paste the notes back into the chat.

## Guardrails

- Read-only on daily.dev. Never unbookmark or mark anything read.
- Never overwrite an existing note; if the file exists, skip it and say so, because the user may have added their own notes.
- One request per 50 bookmarks; incremental runs usually cost one request.
