---
name: batched-queries
description: Where `batchedQuery` from src/utils/batched-query.ts belongs, which is the browser, and why the server reads many keys with one query instead. Applies whenever writing or reviewing a read that fetches one key at a time, or reaching for batchedQuery.
---

# Batched queries belong in the browser

`batchedQuery` gathers every call made in the same moment into one read of all their keys. It only pays when those calls reliably arrive together, and the place they do is one browser tab rendering a list.

## Use it in the browser

Reach for it where many components each read one key as they mount: list rows, cards, lobby parties, a page of history. Every row asks in the same instant, so twenty server calls become one.

The existing ones show the shape: `getCaughtBatched` in `src/auth/caught.ts`, `getTeamBatched` and `getTeamSnapshotBatched` in `src/auth/teams.ts`, and `getProfileBatched` in `src/auth/profile.ts`. Each sits beside the single-key read it batches, which stays for one-off callers.

## Not to merge separate server requests

Do not use it on the server to merge calls from different requests. Separate requests rarely land in the same moment, so the batch mostly adds a timer. When they do land together, one failed query fails every request in it, other players' included. A batched `requireUid` was tried for this and reverted.

## Within one server request, query many keys directly

A handler that needs many rows reads them with one query that takes the list: `readCaughtMany`, `readStacksIn`, or `where id = any(${ids})`. That is simpler than a batch and runs inside the transaction when there is one.

Use `batchedQuery` inside a single request only when that request fans out through code that cannot easily be handed a list, and never inside a transaction: the batched read runs a moment later on its own connection, without the transaction's locks or its writes.

## Setting one up

- Give `key` for object queries, since without it only the same object is read once.
- Give `limit`, since the server function checks the list's length (`ID_BATCH` allows 50). The existing ones use 50.
- Have the callback return a `Map` by key, so `lookup` is one `get` rather than a search.
- Read the result through `settled` where a list re-reads, so a refetch keeps the rows on screen rather than suspending them.
