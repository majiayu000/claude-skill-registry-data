---
name: server-function-validation
description: A server function checks every argument against a valibot schema from src/server/validate.ts before it acts, because the parameter types are gone by the time a call arrives. Applies whenever adding a 'use server' function or giving an existing one something new to read.
---

# Server functions check what they are sent

A `'use server'` function is an HTTP endpoint. Its parameter list is erased at build time, so the arguments that reach it are whatever the caller put in the request body, not what the signature says. The modules under `src/server/` then act on those arguments over the table-owner connection, which row-level security does not bind.

Every argument is therefore checked first, at the top of the body:

```ts
async function useMintOnServer(token: string, catchId: string, item: Items): Promise<Natures | null> {
  'use server';
  check(TOKEN, token);
  check(ID, catchId);
  check(GAME_ID, item);
  return useMintOnServerSide(await requireUid(token), catchId, item);
}
```

`check` and the schemas both come from [`src/server/validate.ts`](../../../src/server/validate.ts). A failing check throws, which is what a malformed call deserves.

## The rules

- **One line per parameter**, in the order the parameters are declared, before anything else in the body. `requireUid` comes after them, or `requireReader` for a read (see `server-reads`).
- **Reuse a schema.** `ID` for a row key, `GAME_ID` for a registry id, `CHUNK_COORDINATE` and `CELL` for where somebody says they are, `OFFSET` and `LOCALE` for the caller's zone, `UID` for an account. A new shape gets a new exported schema in `validate.ts` rather than an inline one at the call site.
- **Bound every list.** An array schema carries a `maxLength`, since an unbounded list is a request to do unbounded work.
- **Check the shape, not the rule.** A schema says an argument is a chunk inside the world or a text id of a sane length. Whether the player owns that catch, can afford it or may reach that landmark stays in `src/server/`.
- **Nothing is coerced.** `check` hands the argument back as it arrived, so the `as*` normalizers further in still see what the caller actually sent.

## Why it is not the transform's job

Adding a check never changes a function's parameters, so it does not move anything: see `server-function-order` for why that matters.
