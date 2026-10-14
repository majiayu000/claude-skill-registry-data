---
name: clickmax-drive
description: Use when the user wants to find, organize, share, comment on, restore or clean up files and folders in the Clickmax workspace Drive (spaces, trash, quota, Google Drive).
---

## When this applies

Use this skill for the workspace file library: locating a file or folder, building a folder tree, sharing with a teammate, commenting, reading who has access, trashing/restoring, and answering "why is my storage full".

Not this skill:

- files attached to a CRM opportunity/task, meeting recordings, page images, message media -> they appear in the Drive read-only (see assumptions) but are managed in their own area
- publishing a file on the internet (image on a page, product deliverable) -> `clickmax-pages`, `clickmax-products`
- uploading a file or reading its bytes -> not possible through tools; upload happens in the Clickmax web app

## Key assumptions

- SPACE = unit of access. `personal` ("Meu drive", one per person, private) | `team` (own members + roles) | `system` ("Plataforma": platform-filed files from other areas; everyone reads, nobody writes)
- role per space: reader < commenter < editor < owner. reader = view; commenter = +comment; editor = +create/rename/move/share/trash/restore; owner = +edit/delete space, manage members
- workspace seat only CAPS: viewer/guest/finance_only/attendant = reader max. Workspace owner = owner everywhere. Workspace admin does NOT see spaces they were not invited to
- direct item share = 2nd access source; most permissive wins, then seat cap. Sharing a folder covers everything inside, including future files
- NO public link. Sharing is always to a named, active workspace member. `share` role is `reader | commenter | editor` (never `owner`)
- `drive_files_browse` is not paginated (whole folder); `drive_search` / `drive_favorites_list` / `drive_shares_with_me` are paginated (`page`, `perPage` default 10)
- search = NAME substring only (never file content); needs `q` or a filter
- names: max 200 chars, no `/` `\` `..`, no leading `.`; folder/space names are NOT unique -> create is not idempotent
- move = same space only, never into itself/descendant. No copy. No cross-space move
- trash: soft delete, 30 days, then purged by a daily job. Trashed items STILL count in quota. Only `drive_trash_purge` / `drive_trash_empty` free space. Folder = one trash item with its subtree; list shows roots only
- deleted spaces are not restorable; purge/empty are irreversible and, for Google-backed spaces, delete the file in the customer's own Google Drive
- files with `origin != upload` and folders with `systemOrigin` = platform-filed: cannot be renamed/moved/trashed from the Drive
- quota is per workspace (`quotaBytes` from `drive_storage_usage`, never assume a number). Bytes are decimal strings. `level`: ok | warning >=80% | critical >=95% | exceeded. Google-backed files are `externalBytes`, outside quota
- Drive menu may be hidden in the web app for accounts where it is not released yet; the tools work regardless -> tell the user to contact support, do not try to "enable" it
- `userId` for members/shares/person card: `id` from `mcp__plugin_clickmax_clickmax__workspace_members_list` (every person of the workspace; find by `search` = name or e-mail), `user.id` from `mcp__plugin_clickmax_clickmax__drive_spaces_members_list`, or `personId` (NOT the attendant `id`) from `mcp__plugin_clickmax_clickmax__attendants_list`. Shares and space membership need an `active` person; a `pending` invitation cannot receive access yet
- Google-backed space health = `connectionHealth` on space rows: `connected` | `read_only` (opens/downloads, but folder creation and uploads fail) | `disconnected` (connection gone or authorization revoked). Fixing either = the person who connected Google reconnects in the web app. A folder created in a Google-backed space is created in Google first; a Google refusal saves nothing in Clickmax
- person card numbers (`mcp__plugin_clickmax_clickmax__drive_people_get`) are what the CALLER can see, never a workspace total of that person

## Thought process

1. Locate before acting: known name -> `drive_search`; known space -> browse; nothing known -> `drive_overview`.
2. Check role before proposing writes (`myRole` in space rows). reader/commenter -> explain instead of failing with 403.
3. Reuse before create: browse/list first, create only when nothing matches.
4. Reversible (trash, rename, move, comment) > irreversible (purge, empty, delete space, connect Google). Ask before the irreversible ones and before any grant of access.

## Execute guide

- Overview / discovery: `mcp__plugin_clickmax_clickmax__drive_overview` returns spaces (with `myRole`), counters, storage and the 6 latest recents in one call. Use `mcp__plugin_clickmax_clickmax__drive_spaces_list` when only spaces are needed.
- Find: `mcp__plugin_clickmax_clickmax__drive_search` (`q`, optional `type`, `ownerId`, `spaceId`, `from`/`to`). Each row has `location` (space + folder path) to tell the user where it lives. `mcp__plugin_clickmax_clickmax__drive_search` and `mcp__plugin_clickmax_clickmax__drive_favorites_list` are paginated (`page`/`perPage`, see `meta`): before concluding an item does not exist, picking "the" match or validating a result, read every page `meta` reports (finding one candidate is not a reason to stop); page 1 alone is enough only for a preview the user asked for, and then say more pages exist. For "what did I use lately" -> `mcp__plugin_clickmax_clickmax__drive_recents_list` (not paginated, `limit` up to 100); starred -> `mcp__plugin_clickmax_clickmax__drive_favorites_list`.
- Navigate: `mcp__plugin_clickmax_clickmax__drive_files_browse` with `spaceId` (+ `folderId`; omit for the root). For an item that came through a share, take `location.spaceId` from the share/search row. `mcp__plugin_clickmax_clickmax__drive_folders_path` = breadcrumb.
- Before building a tree in a Google-backed space, read `connectionHealth` (`mcp__plugin_clickmax_clickmax__drive_spaces_get`): anything other than `connected` -> tell the user to reconnect Google first instead of attempting creates.
- Build a tree top-down: `mcp__plugin_clickmax_clickmax__drive_folders_create` with `spaceId` and no `parentId` for level 1, then pass each returned `id` as `parentId`. Never fire sibling creates before checking existing folders.
- Organize: `mcp__plugin_clickmax_clickmax__drive_files_update` / `mcp__plugin_clickmax_clickmax__drive_folders_update` with `name` and/or `folderId` / `parentId` (`null` = root, omitted = unchanged).
- Share one item: resolve `userId` -> `mcp__plugin_clickmax_clickmax__drive_shares_create` with exactly one of `folderId` / `fileId` and the role. Check the result with `mcp__plugin_clickmax_clickmax__drive_items_access`. Revoke with `mcp__plugin_clickmax_clickmax__drive_shares_revoke` (`shareId`; only entries with `inherited = false`). Inherited access is changed in the space (`mcp__plugin_clickmax_clickmax__drive_spaces_members_update` / `mcp__plugin_clickmax_clickmax__drive_spaces_members_remove`) or in the parent share.
- Give a person a whole space: `mcp__plugin_clickmax_clickmax__drive_spaces_members_add` (space owner only). Re-adding updates the role.
- Restore: `mcp__plugin_clickmax_clickmax__drive_trash_list` -> `mcp__plugin_clickmax_clickmax__drive_trash_restore` with `kind` + `id` of the ROOT row. If `restoredToRoot` is true, tell the user the original folder was gone. Something deleted inside a folder is restored by restoring the folder.
- Free space: `mcp__plugin_clickmax_clickmax__drive_storage_usage` -> `mcp__plugin_clickmax_clickmax__drive_trash_list` -> show what goes (name, size, deleted by/when) -> confirmation -> `mcp__plugin_clickmax_clickmax__drive_trash_purge` per item, or `mcp__plugin_clickmax_clickmax__drive_trash_empty` only when the user wants everything they can delete gone. Trashing alone frees nothing.
- Link for the user to open a file: `mcp__plugin_clickmax_clickmax__drive_files_download_url` (300 s, credential-like: hand it only to the requester, never store it). It is not a way to share with others.
- Google Drive: `mcp__plugin_clickmax_clickmax__drive_spaces_google_capabilities` (own connection) or `mcp__plugin_clickmax_clickmax__drive_spaces_google_connections` (all) -> only a `canWrite` connection and only an EMPTY team space (even trashed items count) -> `mcp__plugin_clickmax_clickmax__drive_spaces_connect_google`. One-way; connecting/reconnecting the Google account itself happens in the web app.
- "What does Ana have in the Drive?": resolve her `userId` -> `mcp__plugin_clickmax_clickmax__drive_people_get` (role, totals, team spaces in common, 4 newest files); for the full list, `mcp__plugin_clickmax_clickmax__drive_search` with `ownerId`.
- Comments: `mcp__plugin_clickmax_clickmax__drive_comments_list` / `mcp__plugin_clickmax_clickmax__drive_comments_add` (commenter+). Activity of an item: `mcp__plugin_clickmax_clickmax__drive_items_activity` (not per-person views/downloads).

## Report

- Lead with what was found/changed and WHERE: `Space / Folder / Subfolder`.
- Lists: newest-modified first for search; folders before files when browsing. Show up to 10 rows unless the user asked for everything (then fetch every page and list all); when rows are left out, say how many (`+N more`) and offer to continue.
- Sizes in human units (GB/MB) converted from the byte strings; quota as `used of quota (ratio %)` + level.
- Shares: name the person, the item, the role and what the role allows; mention that access applies to everything inside a shared folder.
- Trash: show `expiresAt` (days left) and say restore is possible until then.
- Follow-up mutations, purges and access grants are opt-in only.

## Warnings

- Sharing exposes data to another person: confirm item + person + role first.
- Purge / empty trash / delete space / connect Google are irreversible; never chain them onto a search result without an explicit user confirmation naming the items.
- Seat cap: a role granted to a viewer/guest/finance_only/attendant seat still behaves as reader; do not promise write access.
- 404 on an item can mean "no access", not only "does not exist".
- A `pending` file is an unfinished upload; an `orphaned` file has a broken Google link (still listed, not downloadable, nothing deleted).

## Anti-patterns

- Promising public links, uploads, downloads of content, cross-space moves, copies or content search.
- Creating a folder or space without listing existing ones.
- Passing an attendant `id` as `userId`.
- Treating trash as freed storage.
- Removing a member or share to "fix" inherited access (it is changed at its origin).
- Deleting a space to clean up a few files (trash the files instead).

---

Clickmax skill revision: `b8294822a4d6`
