---
name: elixir
description: Use when building Elixir applications with Phoenix and OTP — JSON APIs described with OpenAPI, scheduled work with supervised processes, outbound webhooks (for example a daily chat digest), ExUnit tests and releases in Docker. Also use when deciding between a GenServer, a Task and a plain module, or when a periodic job silently stops.
---

# Elixir, Phoenix and OTP

Default: current Elixir and Erlang/OTP, Phoenix for HTTP (API-only with `--no-html --no-assets` when there is no UI), Req for HTTP clients, ExUnit, `mix release` in a Docker image.

## Setup

1. `mix phx.new app --no-ecto --no-html --no-assets` for a pure API (keep Ecto if you store data).
2. Format and lint from day one: `mix format`, `mix credo` (optional), `mix compile --warnings-as-errors`.
3. Pin Elixir/OTP versions in `.tool-versions` and in the Dockerfile base image together.

## Choosing the process shape

| Need | Use |
|---|---|
| Pure computation | Plain module functions (no process) |
| One-off concurrent work | `Task` / `Task.async_stream` under a `Task.Supervisor` |
| State or a timer that must survive errors | `GenServer` started by the application supervisor |
| Many independent workers | `DynamicSupervisor` + `Registry` |

Start with plain functions; add a process only when you need state, concurrency or fault isolation.

## Periodic jobs

- A `GenServer` that schedules itself with `Process.send_after(self(), :tick, ms)` in `init/1` and again in `handle_info/2`.
- Compute the next run from the wall clock (e.g. next 07:00 in the configured time zone), not a fixed interval, so drift and restarts do not shift it.
- Make the job idempotent per day (remember "sent for date X") so a restart does not send twice.
- Wrap the work in `try`/`rescue` or a `Task` so a failure is logged and the schedule continues; otherwise a crash loop can exhaust the supervisor's restart budget.

## APIs and webhooks

- Describe the JSON API with an OpenAPI 3 document (e.g. via `open_api_spex`) and test that responses match it; clients can then be generated.
- Send outgoing webhooks with `Req`, a timeout and a small retry; keep the webhook URL in runtime configuration (`config/runtime.exs` reading the environment), never in source.

## Testing

- `mix test` with `async: true` where tests do not share global state.
- Inject the clock and the HTTP client (behaviours + Mox, or a function argument) so schedule logic is testable without waiting.

## Verification loop

1. `mix format --check-formatted` and `mix compile --warnings-as-errors`.
2. `mix test`.
3. Build the release image and hit a health endpoint.

## Pitfalls

- **Compile-time vs runtime config:** values in `config/config.exs` are baked in at build time; secrets and URLs belong in `config/runtime.exs`.
- **Large mailboxes:** a GenServer that receives faster than it handles grows memory without bound; use back-pressure or `call` instead of `cast`.
- **`GenServer.call` default timeout is 5 s;** long work inside a call blocks every other caller.
- **Time zones** need a database package (`tzdata` or `tz`) configured; `DateTime` alone only knows UTC.
- **Atoms are not garbage-collected;** never convert untrusted strings with `String.to_atom/1`.
