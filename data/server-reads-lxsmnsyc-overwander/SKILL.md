---
name: server-reads
description: The browser reads the database only through server functions. A read checks its arguments, verifies the caller with `requireReader`, applies who may see the rows itself, and is registered with `readOnly`. Applies whenever adding or changing something the browser reads, or a table the browser follows live.
---

# Reads go through the server

Nothing in the browser talks to the database. Every read is a `'use server'` function in `src/auth/`, calling a read in `src/server/` over the owner connection. There are no row policies behind it, so the function is the only thing that decides what a player may see.

## The shape

```ts
export async function listTrades(uid: string): Promise<[string, TradeRecord][]> {
  // ...
  for (const row of await listTradesOnServer(await getIdToken(), uid)) {
  // ...
}

async function listTradesOnServer(token: string, player: string): Promise<Record<string, unknown>[]> {
  'use server';
  check(TOKEN, token);
  check(UID, player);
  const uid = await requireReader(token);

  return player === uid ? readTradeRows(uid) : [];
}
readOnly(listTradesOnServer);
```

## The rules

- **`requireReader`, not `requireUid`.** A read moves nothing, so it skips the pace bucket's write, the ban and the switches. `requireUid` is for writes.
- **Decide visibility in the function.** A row only its owner may see is read for the uid the token names. When the browser passes a uid, another player's answers empty. A row every signed-in player may see is read for any uid.
- **Register it with `readOnly(fn)`** on the line after the function. Every server call marks the kept bag stale, and a registered read does not.
- **Batch in the browser** with `batchedQuery`, and read the batch with one query on the server (see `batched-queries`). A batched id list is checked with `ID_BATCH` or `UID_BATCH`.

## Following a table live

`watchRow` and `watchTable` in `src/auth/watch.ts` read once, then again whenever the live feed says the table changed. A table the browser follows needs two things:

- the `live_changes` trigger, added in a migration under `db/migrations`;
- an entry in `src/server/live/rules.ts` saying who may read its rows whole. A follower who may not gets the row's keys and reads again through the server.

`test/live-feed.test.ts` fails when the two lists disagree.
