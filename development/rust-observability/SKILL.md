---
name: rust-observability
description: Logs are structured events with named fields, not formatted strings — tracing over log over println!, spans for async context, error chains logged once, and never a secret in a field. Use when adding or reviewing logging, tracing, or metrics in Rust, when println! or string-interpolated log messages appear, when a library installs a subscriber, or when the user asks how to instrument Rust code.
---

# Rust Observability

A log line is a structured event with named fields, and a library never installs
a subscriber. This skill governs *how Rust code reports what it is doing*; what
an error type contains is `/rust-errors`, and span behaviour across cancellation
is `/async-rust`.

## A log line is an event, not a sentence

The core move: fields stay fields.
`error!(user_id, %path, "config load failed")` is queryable — `user_id` and
`path` are named columns. The interpolated form,
`error!("config load failed for user {user_id} at {path}")`, is a string
someone will later write a regex against. The difference shows up the first
time somebody needs "all failures for one user" — the moment logging either
pays for itself or does not.

## The three layers, and which to use

`println!` writes to stdout with no level, no filter, and no structure; it
belongs in a CLI producing output the user asked for, never in a library.
`log` is the older facade, right when the dependency budget is tight.
`tracing` is the default here: spans carry context across `.await` points,
which is the problem async code actually has.

## Naming events

`component.operation.state` — `config.load.failed`,
`pool.connection.acquired`. A consistent scheme is what makes a dashboard
possible; ad-hoc English messages are what make it impossible. Message
templates with placeholder syntax are one implementation of the field idea,
not the idea itself — a codebase already on templates is fine.

Name fields after the OpenTelemetry semantic attribute names where one
exists (`http.request.method`, `url.full`, `error.type`, `server.address`),
so a backend that understands them groups your data without a mapping layer;
invent a dotted name of your own only where no standard one fits.

## Spans

`#[tracing::instrument]` on a function makes every event inside it inherit the
request context; `skip` keeps large or secret arguments out of the fields.
The rule: a span is a unit of work with a beginning and an end; an event is a
point in time.

## Levels and filtering

- `error!` — someone should look at this.
- `warn!` — something went wrong and the code handled it.
- `info!` — lifecycle events a reader wants without a bug.
- `debug!` / `trace!` — developer detail, off in production.

The boundary that matters is `error!`: because it means someone should look, a
handled and expected failure is `warn!` or `debug!` at most. `EnvFilter`
gives per-module control, and in a library, filtering is the whole story:

A library emits and never installs a subscriber. Installing one is global
state the application owns: the binary installs the subscriber exactly once,
and a library that installs one too fights for the global — a panic at
startup with `tracing`, a re-formatted event stream with `log`.

## Errors are logged once, with the chain

Log at the boundary that handles the error, not at every level it passes
through, and log the whole `source` chain rather than the top-level `Display`
alone, which is usually the least specific sentence available. What the error
type contains is `/rust-errors`.

## Never log a secret

Tokens, passwords, keys, personal data. The structural answer, not a review
habit: a newtype whose `Debug` and `Display` print a redacted form, so the
secret cannot be logged even by a future careless call site. The `?` form
prints via `Debug`, the `%` form via `Display`, and the bare form does not
compile for a custom type at all — every path redacted or absent:

```rust
struct ApiToken(String);

impl std::fmt::Debug for ApiToken {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("ApiToken(<redacted>)")
    }
}

impl std::fmt::Display for ApiToken {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("<redacted>")
    }
}
```

Whether the newtype is the right model is `/type-driven-design`.

## Overhead

Keep telemetry out of hot inner loops altogether. Even a disabled event costs
an enablement check per iteration, and an enabled one swamps the work. Emit
one event around the loop, or one per batch, carrying a count.

Building an event that a filter discards still costs when the work is done
before the macro call. The macros take field values lazily, so do not
`format!` or allocate an argument eagerly for a `debug!` that is off in
production: `let summary = summarize();` before `debug!(?summary);` runs on
every call, level or not, while `debug!(summary = ?summarize());` runs only
when the event is enabled.

## Deferrals

What an error type contains and how it chains is `/rust-errors`. Whether the
redacting newtype is the right model is `/type-driven-design`. Span behaviour
across cancellation is `/async-rust`.

## Verification

```bash
cargo clippy --all-targets
rg 'println!|eprintln!' src/     # expect zero in a library
rg 'info!\("|warn!\("|error!\("' src/   # a message with interpolation and no fields is the smell
cargo test
```

Run clippy at the lint level the target repo configures —
`cargo clippy -- -D warnings` is the fallback only when the repo
configures no lints at all. The greps are a starting point, not a
verdict: a CLI printing its actual output is a legitimate `println!`.
