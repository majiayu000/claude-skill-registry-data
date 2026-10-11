---
name: realtime
description: Supabase Realtime/WebSocket — broadcast, presence, Postgres changes.
---

# Realtime (WebSocket)

## Detection Signals

| Signal | Meaning |
|---|---|
| `supabase.channel()` in code | Supabase Realtime |
| `REALTIME_*` env vars | Supabase Realtime service config |
| `realtime` service in `docker-compose.yml` | Self-hosted Realtime |
| `ws://` / `wss://` URLs in code | Generic WebSocket |
| `socket.io`, `ably`, `pusher` dependencies | Third-party WS providers |

## Supabase Realtime

Supabase Realtime is built on Phoenix channels (Elixir). It exposes three features via a single WebSocket connection:

| Feature | What it does |
|---|---|
| **Broadcast** | Send arbitrary messages between clients via a named channel |
| **Presence** | Track which clients are connected to a channel and their state |
| **Postgres Changes** | Stream database mutations (INSERT/UPDATE/DELETE) to clients |

## RLS and Realtime

Supabase Realtime enforces RLS for Postgres Changes. The JWT used to connect to the channel determines what data is streamed.

Pass the user JWT when creating the client (happens automatically if using `supabase-js` with active session). For server-side Realtime subscriptions, use the service-role key deliberately and be aware that all changes will flow through.

## Common Pitfalls

- Not calling `removeChannel` / `unsubscribe` on cleanup — channels accumulate and cause memory leaks
- Missing `replica identity full` — `payload.old` is empty on UPDATE/DELETE
- Subscribing to `postgres_changes` without RLS — all rows stream to all clients
- Opening multiple WebSocket connections for the same channel — use a singleton or channel registry
- Not handling `CHANNEL_ERROR` and `TIMED_OUT` statuses — the subscription silently stops working
- Sending large payloads via broadcast — keep under 1 MB; use Postgres + Postgres Changes for larger data
- Generic WebSocket: reconnecting on a fixed interval instead of exponential backoff with jitter — causes reconnect storms against a recovering server
- Generic WebSocket: ignoring the `CloseEvent` code — `1000`/`1001` are intentional closes, everything else should trigger a reconnect
- Generic WebSocket: no application-level heartbeat — a dead connection can sit in `OPEN` state for minutes before the OS notices
- Generic WebSocket: using `ws://` on an HTTPS page — browsers block the mixed-content connection outright; always use `wss://`
- Generic WebSocket: authorizing the connection by `Origin` header alone, or skipping token validation on the upgrade handshake

## Load on Demand

| When | Load |
|------|------|
| Implementing broadcast, presence, Postgres Changes, or generic WebSocket patterns | `references/implementation.md` |
