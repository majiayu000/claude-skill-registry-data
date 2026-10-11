---
name: binary-sync-integrate
description: Add gaza-geo-sync (compact binary live-position sync with JSON fallback) to a web or Node project. Use when the user wants map/vehicle/courier/GPS positions to use less data, wants a binary position format, or mentions gaza-geo-sync, low-bandwidth or 2G/EDGE users for a live map.
---

# Integrate gaza-geo-sync

Goal: live positions travel as ~7 bytes per object instead of ~45–100 bytes of JSON,
**without breaking any existing client**. JSON stays the default; binary only when a client asks.

Source of truth: https://github.com/AQaddora/gaza-geo-sync (README, `docs/MIGRATION.md`,
`templates/`). If the repo is vendored or installed, read `src/codec.ts` header comment for the byte layout.

## Steps

1. **Install.** Either `npm install github:AQaddora/gaza-geo-sync` (builds on install), or vendor
   the four files `src/bytes.ts src/codec.ts src/sync.ts src/client.ts` (+ `src/server.ts` server-side)
   into e.g. `src/lib/geo-sync/`. Zero runtime dependencies; `server.ts` needs `node:zlib`.
2. **One shared codec.** Copy `templates/geo-codec.ts`. Set `south`/`west` to the south-west corner
   of the area most points fall in. With the default `scale: 1e5` and `offsetBytes: 2` the cheap box is
   ≈0.655° per side (≈73 km N–S); larger areas → `offsetBytes: 3` or `scale: 1e4`. Points outside still
   work (they cost a few bytes more). Server and client must import the same file.
3. **Stable small numbers.** Each tracked object needs a small integer `n` that never changes:
   add an additive DB column (Postgres `seq SERIAL UNIQUE`, MySQL `AUTO_INCREMENT`, SQLite rowid).
   Never reuse a number for a different id. Send `[n, id]` pairs (`index`) on a first sync.
4. **Server route.** Adapt `templates/nextjs-route.ts` (App Router) or `templates/express-server.ts`.
   Use `positionsReply(...)`; it negotiates on `Accept`, sets `Vary: Accept, Accept-Encoding`,
   gzips binary only when smaller. Keep the JSON branch byte-for-byte compatible with what clients
   already parse — add fields, never rename.
5. **Client.** Replace the positions fetch with `fetchPositions(url, { codec, idOf })`
   (or `templates/use-live-positions.ts`). It sends `Accept: application/octet-stream, application/json;q=0.5`
   and always resolves to the JSON shape, so caches and screens stay unchanged. Persist `payload.index`
   next to your cached records; when `unknown > 0`, drop the cursor so the next request is a full sync.
6. **Uploads (optional).** For a phone sending its GPS point, use `createPointSender` or
   `templates/use-point-sender.ts` and `readPointBody` server-side (`templates/nextjs-point-route.ts`).
   Answer binary uploads with 204. Old servers answering 400/415 switch the sender to JSON.
7. **Service worker.** Do not cache the positions endpoint and never queue point uploads offline
   (`templates/service-worker-cache.js`).
8. **Verify** with the `binary-sync-verify` skill before calling it done.

## Rules

- JSON fallback is not optional. curl, old app versions and debugging must keep working.
- Bump `profile` in the codec options whenever any codec option changes.
- Do not binary-encode text-heavy, diffed data (chat, bookings): gzip'd JSON is fine there.
- Never log decoded coordinates of real users.
