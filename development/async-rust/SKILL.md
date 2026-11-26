---
name: async-rust
description: Write correct async Rust — runtime choice, Send and Sync bounds, cancellation safety, blocking work inside async contexts, and shared state across tasks. Use when writing or reviewing async code, when a future is held across an await point, when the user hits a Send bound error on a spawned task, when a runtime stalls or deadlocks, or when the user asks about tokio, select!, or spawn_blocking.
---
# Async Rust

Async Rust fails in three places: an executor thread that gets blocked, a guard
held across an await point, and a future dropped mid-operation. This skill
governs *correctness under concurrency and cancellation* — it does not decide
whether the code should be async in the first place.

## Async is not free concurrency

An `async fn` yields a future that does nothing until polled. Concurrency comes
from the runtime and from combining futures — `join!`, `select!`, `spawn` — not
from the `async` keyword:

```rust,ignore
// Serial: the second fetch starts only after the first completes.
let a = fetch_user(id).await;
let b = fetch_orders(id).await;

// Concurrent: both futures are polled at the same time.
let (a, b) = tokio::join!(fetch_user(id), fetch_orders(id));
```

Every `.await` in a function adds to the size of the generated future, and a
large future is copied on every move — into `Box::pin`, into a `JoinSet`.
Many awaits and large locals mean kilobytes; box the inner future or split
the function once a profile says the moves matter.

Three habits keep futures small. Shrink what lives across an `.await`: a big
buffer or collection that is not used after the suspension point should be
dropped or scoped in a block before it. Move setup that does not need to
suspend (building a request, parsing config) outside the `async` block, so
its temporaries are never part of the state machine. And for a hot future, pin
the size down with a test that asserts `std::mem::size_of_val(&future)` stays
under a chosen limit, so growth from a later edit fails a build:

```rust
async fn handle(id: u32) -> u32 {
    id + 1
}

#[test]
fn handle_future_stays_small() {
    let future = handle(7);
    assert!(std::mem::size_of_val(&future) <= 64);
}
```

## Runtime choice, once, at the top

Pick a runtime, in the overwhelming majority of cases `tokio`, deliberately.
The library rules: stay runtime-agnostic if you can (for I/O, accept `futures::io::AsyncRead` and
`AsyncWrite` bounds instead of tokio-specific types), feature-gate the
integration if you cannot, and never start a runtime inside a library
function (`#[tokio::main]` belongs in a binary or test; a `Runtime::block_on`
there hands the consumer a second, conflicting executor).

## Blocking work in an async context

A CPU-bound loop, a synchronous file or network call, or a compute stretch
without an `.await` inside an `async fn` stalls the executor thread and starves
every other task on it. The fix: `tokio::task::spawn_blocking` for blocking I/O
and short CPU work, a dedicated thread pool (`rayon`) for sustained CPU work,
and never a `std::thread::sleep` inside a task. For a compute loop, yielding
periodically is the weaker fix and only works when each chunk between yields is
genuinely short. If yielding is the choice, put `tokio::task::yield_now().await`
inside the loop so a yield lands after somewhere between 10 and 100 microseconds
of work (a rule of thumb, not a measured bound). Yield rarely and neighbouring
tasks starve; yield constantly and the switching costs more than it frees.

## `Send`, `Sync`, and the spawn bound

`tokio::spawn` requires `Send + 'static`: everything held *across* an `.await`
must be `Send` — where `Rc` and `RefCell` fail to compile, and where a
`std::sync::MutexGuard` held across an `.await` becomes a deadlock:

```rust,ignore
// Deadlock waiting to happen: the std guard is held across the await.
let mut guard = state.lock().unwrap();
guard.value = fetch().await;

// Either drop the guard before awaiting…
let value = fetch().await;
state.lock().unwrap().value = value;

// …or use the async-aware mutex when the lock genuinely must span the await.
let mut guard = state.lock().await; // tokio::sync::Mutex
guard.value = fetch().await;
```

Prefer `std::sync::Mutex` unless the lock must span an `.await`, then
`tokio::sync::Mutex` — `clippy::await_holding_lock` catches the common case.

## Cancellation safety

Any future can be dropped at any `.await` point — that is what `select!` and
timeouts do. A future that has consumed input but not yet committed it loses
data when dropped mid-flight. The rule: do the irreversible step in one
non-cancellable piece, or make the operation resumable. The worked cases
live in `CANCELLATION.md`.

## Shared state across tasks

`Arc<Mutex<T>>` for shared mutation, channels for handing work between tasks,
and message passing when the state has one logical owner — a task that owns
its state and is told what to do beats tasks that reach into shared memory.

| Channel | Use for |
|---|---|
| `mpsc` | Many producers to one consumer |
| `oneshot` | A single reply |
| `watch` | The latest value, where missing intermediate values is correct |
| `broadcast` | Every receiver seeing every message, with a bounded backlog |

The choice is semantic, not performance — picking `broadcast` where `watch`
was meant produces a lagging receiver error nobody expected.

Dynamic task groups and their abort semantics are in `CANCELLATION.md`.

## Async in a public API

Prefer `async fn` over `-> impl Future` unless the extra control is needed. The
explicit form earns its place in two spots: trait methods, where it lets the
signature state the `Send` bound, and a hot function whose future size or
captures must be controlled by hand. Elsewhere it is noise, and
the desugared form additionally promises `Send`-ness (or its absence) in ways
the caller then depends on. In traits, `async fn` still lacks `Send` bound
sugar, and `#[async_trait]` remains the pragmatic choice for object-safe
async traits.

## Deferrals

Error types for timeouts and cancellation are `/rust-errors`; shared-ownership,
`/ownership-not-clone`; public-surface commitments, `/rust-api-design`; the
`Pin` invariants of a manual `Future` impl, `/unsafe-rust`.

## Verification

```bash
cargo clippy --all-targets   # add -- -D warnings only if the repo has no lint config
cargo test
```

The async-relevant lints (`await_holding_lock`, `await_holding_refcell_ref`,
`async_yields_async`) come out of its output, not switched on. Async bugs
are timing-dependent — a passing `cargo test` is weak evidence: where
the repo uses `#[tokio::test]`, cover the changed path with
`#[tokio::test(flavor = "multi_thread", worker_threads = 2)]`.
