---
name: fd-audit
description: Audit a Rust change in OpenAlgo Desktop for resource leaks, both descriptors and unbounded memory. Run after building or fixing anything that touches HTTP clients, the SQLite pool, DuckDB, broker or feed WebSockets, the loopback relay, spawned tokio tasks or threads, listeners, channels, caches, registries, subscriptions or session teardown; before calling a wave done; and when a user reports "too many open files", refused connections, dropped sockets, rising memory or a slow app after hours open.
---

# Resource leak audit (Rust): descriptors and memory

The desktop is one long-lived process, open all trading day, reconnecting
broker feeds through outages. Anything leaked per request, per tick or per
reconnect accumulates until the process dies. There is no second worker and
no restart point. Audit **the change you made**, not the whole repo.

| | Symptom | Ceiling |
| --- | --- | --- |
| Descriptors | `Too many open files`, refused database connections, a feed that stops reconnecting | `ulimit -n` (often 256 for a macOS app) |
| Memory | rising RSS, a slow UI, OOM | host RAM (a low-memory laptop or small VM has little) |
| Tasks | CPU and memory creep, work continuing after logout | none until the others hit theirs |

## Step 1: scope

If the change touches none of these, say so and stop.

Descriptor-holding: `reqwest` clients, the SQLite r2d2 pool
(`db/sqlite/mod.rs` `SqliteDb::conn`, `LogsDb::conn`, `sandbox::SandboxDb`),
DuckDB (`db/duckdb/mod.rs` `HistorifyDb::conn`), `tokio_tungstenite` sockets,
the relay (`brokers/common/relay.rs`), `TcpListener`s (the HTTP server, which
also serves `/mcp`; the 8765 feed server; each relay), child processes, files.

Memory-holding: `HashMap` / `BTreeMap` / `Vec` / `VecDeque` behind a `Mutex`
or `RwLock`, `static` collections, caches, event-bus subscribers
(`events::EventBus`), Socket.IO rooms, per-client feed subscriptions
(`feed/registry.rs`), per-symbol registries, channels, retained master
contracts, history or option chains.

Task-holding: `tokio::spawn`, `tauri::async_runtime::spawn`,
`std::thread::spawn`, `spawn_blocking`, `JoinSet`.

## Step 2: run the grep checklist

```bash
python3 .claude/skills/fd-audit/leak_grep.py --diff origin/master   # files you changed
python3 .claude/skills/fd-audit/leak_grep.py                        # all of src-tauri/src
python3 .claude/skills/fd-audit/leak_grep.py --self-test            # prove each check fires
```

Checks (each prints `file:line`, the line, and the question to answer):

| Check | Pattern | The question |
| --- | --- | --- |
| `spawn-unowned` | a spawn used as a statement, handle dropped, not awaited | who aborts this on logout and shutdown? |
| `http-client` | `reqwest::Client::new()` / `Client::builder()` | is this the one client per process, with timeouts? |
| `unbounded-chan` | `unbounded_channel`, std `mpsc::channel`, crossbeam `unbounded` | what bounds the backlog if the consumer stalls? |
| `map-no-evict` | a collection behind a lock, or a static one, with no `remove` / `retain` / `clear` / `drain` / `pop` / `take` of that name (or its lock guard) in the file | what is the key space, and who evicts? |
| `broadcast-lagged` | a file that receives from a channel and never names `Lagged` | is this a broadcast receiver that dies on lag? |
| `conn-across-await` | `let c = ..conn()?;` with an `.await` later in the same block before `drop(c)` | does a pooled connection wait on network I/O? |
| `leak-forget` | `Box::leak`, `mem::forget` | once per process, or per call? |

A suspect is a line to read, not a verdict, and an empty result is not proof
(see the `verify` skill, rule 3). Triage of what the full run prints today, so
a new line stands out:

- `brokers/common/http.rs` (`OnceLock` shared broker client), `state.rs`
  (`AppState`'s one client), `mcp/stdio.rs` (the `mcp` subcommand's one
  client): one per process, with timeouts. Fine.
- `server/ratelimit.rs` `map` (swept at `MAX_ENTRIES` by `sweep`),
  `mcp/http.rs` `buckets` (periodic sweep): bounded, evicted by a helper the
  heuristic cannot follow.
- `feed/source.rs` `FakeSource`, `trading/runner/host.rs` `RecordingHost`:
  test doubles.
- `websocket/manager.rs:421`: the bounded `mpsc` command channel, not a
  broadcast.
- `historify/jobs.rs` `ClaimGuard::hand_over`: `mem::forget` of a guard whose
  release passes to the processor.

## Step 3: descriptor conventions

- **HTTP.** One shared client: `brokers::common::http::client()` for broker
  calls (HTTP/2 by ALPN with HTTP/1.1 fallback; connect 10 s, request 30 s,
  read 30 s, pool idle 30 s, 16 idle per host; `DOWNLOAD_TIMEOUT` 180 s for
  masters) and `AppState`'s client for the rest. Never a client per call; a per-call client is a pool per call.
- **SQLite.** Through the pool (`max_size`, `min_idle(1)`, idle timeout
  300 s in `db::sqlite::open_pool`). Take a connection, use it, let it drop
  before any `.await` on network I/O; inside `async fn`, scope it in a block
  or do the work in `spawn_blocking`. A connection held across an await pins
  a pool slot (two descriptors: the database and its WAL) for the whole
  network round trip.
- **DuckDB.** `HistorifyDb::conn()` returns a cloned connection; use
  `read` / `mutate` / `run` / `write` so it closes on every path.
  `open_connections()` counts them and `close()` / `seal()` end the store.
- **WebSockets.** Broker feeds run on `websocket::WebSocketManager`, which
  closes the old socket before reconnecting, backs off with a cap and
  jitter, and owns one supervisor `JoinHandle` aborted in `disconnect()`. Do
  not write a reconnect loop in an adapter. A relay (`RelayHandle`) owns its
  listener and session in a `JoinSet` aborted when the handle drops.
- **Tasks.** Every long-lived task is owned: `AppState::spawn` (a `JoinSet`
  drained in `AppState::shutdown`), `BrokerRuntime::spawn` (aborted in
  `teardown` on logout, at the 03:00 IST boundary and at shutdown), or a
  `JoinHandle` field aborted in the owner's `shutdown`. An adapter's own
  poller is stopped in `Broker::on_logout`. `spawn_blocking` is fine when
  awaited.
- **Listeners.** The HTTP server (UI, `/api/v1`, `/mcp`) and the 8765 feed
  server stop on app exit and when the port changes; a new listener on a port change
  must not leave the old one bound.

## Step 4: memory conventions

- **Every cache has a bound and an expiry.** Ask "what is the key space?"
  Keyed by user: bounded (one user). Keyed by symbol, order id, request id,
  IP, token or client: unbounded unless something evicts it. Use a size cap
  plus a sweep (`server/ratelimit.rs` `MAX_ENTRIES`), or rebuild the
  collection from the source of truth each time (`common::order_poll`
  snapshots).
- **Every subscription has a removal that also runs on the error path.**
  Bus subscribers, Socket.IO rooms, feed subscriptions per 8765 client
  (`feed/registry.rs`), manager subscriptions (reference counted; the entry
  goes when the last reference goes).
- **Channels are bounded.** `mpsc::channel(n)`; broadcasts with a capacity
  (`TICK_CHANNEL_CAP` 4096). A broadcast receiver handles
  `RecvError::Lagged(n)` by skipping ahead or re-polling
  (`feed/server.rs`, `feed/bridge.rs`, `sandbox/engine.rs`), never by
  ending the loop.
- **Large payloads die with the request.** Master contracts, history and
  option chains are not stashed in a struct field or a closure that outlives
  the call. The symbol master lives once, in `SymbolResolver`, replaced
  whole on reload.

## Step 5: check every exit path

For each resource: released on success, on error (`?` returns early: does
`Drop` release it, or does a manual close get skipped?), and on the retry or
reconnect path, where a `continue` skips the cleanup at the bottom of the
loop. Task cleanup on logout is a path too: what keeps running after
`BrokerRuntime::teardown`?

## Step 6: measure, do not just read

A flat count after many iterations is the only proof. A count that rises and
plateaus is a cache filling; one that rises linearly is a leak.

**The soak test** (`src-tauri/tests/it/soak.rs`): the whole trading day in a
loop on the real `AppState`, HTTP server with Socket.IO and the 8765 feed
server, with `MockBroker` and a fake broker socket. Each cycle signs in,
loads the master, streams ticks, places a live and a sandbox order, drops and
reconnects the broker socket, makes 110 `/api/v1` requests, connects and
disconnects Socket.IO clients and logs out. It samples descriptors, the
database pool, memory (physical footprint on macOS) and live tokio tasks, and
fails on a line, passes on a plateau. Ignored by default (minutes):

```bash
cd src-tauri
export CARGO_TARGET_DIR=/Users/openalgo/openalgo-desktop/openalgo-desktop/src-tauri/target
cargo test --locked --test it soak -- --ignored --nocapture --test-threads=1
```

CI runs the same in `.github/workflows/soak.yml`; record numbers in
`docs/audit/soak.md`.

**Descriptor accounting** (`tests/it/broker_session_e2e.rs` `settled_fds`):
the database pool can legitimately grow by a connection (two descriptors)
during a session when subscribers check out connections at once; r2d2 opens
it on its own thread and reports it in `pool_state()` only once established.
So sample until two reads 20 ms apart agree with an unchanged pool count, and
judge `fds - 2 * pool` growth, not raw `fds`.

**Isolation.** All integration tests share one binary and run in parallel,
so a test that measures the process starts with `crate::isolated!(name);`
(`tests/it/isolate.rs`): it re-runs itself alone in a child process with
inherited descriptors closed. Models: `feed_hygiene.rs`
(`reconnect_loop_does_not_leak_descriptors_or_memory`), `feed_soak.rs`,
`broker_groww_hygiene.rs`, `broker_upstox_feed_hygiene.rs`.

**Tasks.** `tokio::runtime::Handle::current().metrics().num_alive_tasks()`
before and after the path (see `broker_groww_feed.rs`: `before + 1` while
running, back to `before` after logout).

**A running process**: `cargo run --example dev_server`
(`src-tauri/examples/dev_server.rs`: a throwaway data directory, an
in-memory keystore, port 5500), never the app binary against the trader's
real data folder:

```bash
lsof -p "$PID" | wc -l                                        # descriptors
lsof -p "$PID" | awk '{print $5}' | sort | uniq -c | sort -rn | head   # which kind grows
ps -o rss= -p "$PID"                                          # resident KiB
```

Baseline, drive the path 100+ times, sample again. Never `pkill` to stop
it; stop the one process you started, by its PID.

## Step 7: report

If everything holds, name each resource you checked, that it is released on
every path, and whether you verified by reading or by measurement.

If you find a leak, do not fix it silently and do not move on. Report:

- the file and line where the resource is acquired;
- the exit path that misses the release (error return, retry `continue`,
  logout, port change, a dropped `JoinHandle`);
- descriptor, memory or task, and what bounds it (nothing, a cap, the key
  space);
- the cost: a process open all day accumulates it until descriptors run out
  (feeds stop reconnecting, the database refuses connections) or memory does.

Then fix it with a test that fails without the fix (the hygiene tests above
are the pattern) and measure again.
