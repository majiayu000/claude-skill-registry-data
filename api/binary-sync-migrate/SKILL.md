---
name: binary-sync-migrate
description: Convert an existing JSON polling or sync endpoint that returns live positions (vehicles, couriers, devices, riders) to gaza-geo-sync's binary frame while keeping JSON as the fallback. Use when the user asks to migrate, convert or shrink an existing positions/locations/sync API, or to make a map refresh cheaper on mobile data.
---

# Migrate a JSON positions sync to gaza-geo-sync

Full guide: `docs/MIGRATION.md` in https://github.com/AQaddora/gaza-geo-sync. Work in this order;
each step ships on its own and nothing breaks between steps.

## 0. Find and measure first
- Locate the endpoint(s) and every client that calls them (`grep -rn "positions\|location\|/sync"`).
- Record today's numbers with the `binary-sync-verify` skill (bytes per refresh gzipped,
  refresh interval, upload interval). No baseline → no claim.
- Write down the exact JSON shape clients parse. That shape is the contract for the fallback
  and for the offline cache.

## 1. Cheap wins that need no binary
- Round coordinates to 5 decimals (`codec.round`) in the JSON too: ~30% less gzipped.
- Standing-still throttle on uploads (`worthSending`): fewer requests, which matters more than bytes
  for small uploads (HTTP headers are ~400–800 B each).

## 2. Give each object a stable small number
- Additive migration: `seq SERIAL UNIQUE` (or equivalent). Backfill happens automatically.
- Expose `n` in the JSON form of the object list so clients can learn it.

## 3. Server: negotiate
- Wrap the handler with `positionsReply` (see `templates/nextjs-route.ts` / `templates/express-server.ts`).
  JSON when `Accept` lacks `application/octet-stream` — identical to before.
- Split the response: everything except positions goes in the frame's JSON part (`extra`), positions
  in binary. Include `index` on full syncs.
- Add `Vary: Accept` (done by the helper) so no cache mixes the two forms.

## 4. Client: decode on arrival
- Replace `await res.json()` with `fetchPositions(...)`. It returns the old JSON shape.
- Store records exactly as before; additionally store the `[n, id]` index.
- Bump the client's local schema/cache version once so existing installs do one full sync
  (they need the numbers).

## 5. Uploads
- Server accepts both bodies (`readPointBody`), replies 204 to binary.
- Client: `createPointSender` (binary first, JSON after a 400/415).

## 6. Prove it
- Run the project's tests + add round-trip tests for the endpoint (both Accept values).
- Use `binary-sync-verify` to measure after; report before/after honestly, including where it did not help.
