---
name: litestar-granian
description: "Auto-activate for litestar_granian, GranianPlugin, litestar run Granian options, runtime threads, HTTP/2, TLS, access logs, metrics, static mounts, or worker lifecycle. Not for non-Granian servers."
---

# litestar-granian

`litestar-granian` 0.16.0 replaces Litestar's `run` command with a
supervised Granian command and bridges Litestar's active log formatter into
Granian worker processes. It requires Granian 2.7.9 or later (the current
lock uses 2.8.3).

## Code Style Rules

- Keep handlers async when they perform I/O.
- Configure the server at the command line or programmatically via `granian.Granian`.
- `GranianPlugin` takes only an optional `static` mode keyword argument (`"off"` or `"auto"`).
- Use the `litestar run` option names documented here. Do not substitute similarly named options from older Granian or Uvicorn releases.

## Quick Reference

### Register the plugin

```python
from litestar import Litestar, get
from litestar_granian import GranianPlugin


@get("/health")
async def health() -> dict[str, str]:
    """Return health check response."""
    return {"status": "ok"}


app = Litestar(
    route_handlers=[health],
    plugins=[GranianPlugin()],
)
```

```bash
litestar --app app:app run
```

`GranianPlugin` registers the Granian-backed `run` command. When `litestar run`
starts, `litestar-granian` inspects the active `"litestar"` standard-library
logger (or `app.logging_config`, including `standard_lib_logging_config`
wrapped by `StructlogPlugin`), serializes the active formatter into a temporary
JSON `dictConfig` (`--log-config`), and reconstructs matching `generic`
(`_granian`) and `access` (`granian.access`) formatters inside Granian worker
processes.

### Defaults in 0.16.0 / Granian 2.8.3

| Concern | Default |
| --- | --- |
| Sockets and Bind | `127.0.0.1:8000` |
| HTTP mode | `auto` (HTTP/1 and HTTP/2 supported; HTTP/3 not supported) |
| Workers | `1` worker (process on GIL builds; thread on free-threaded builds) |
| Runtime threads | `1` per worker |
| Runtime blocking threads | Automatically selected (`512` in Granian when unset) |
| Blocking threads | `1` on ASGI (fixed; `> 1` only supported on WSGI; `30s` idle timeout) |
| Runtime mode | `auto` (resolves to `mt` on ASGI) |
| Event loop | `auto` (Granian's standard selection; optional loops require their extras) |
| Async task implementation | `asyncio` (optional experimental `rust` on Python < 3.12) |
| Backlog | `1024` globally (minimum `128`) |
| Backpressure | `backlog / workers` per worker (minimum `1`) |
| Granian log | Enabled at `info` (`--granian-log`, `--granian-log-level`) |
| Access log | Disabled (`--granian-access-log`, `--granian-access-log-fmt`) |
| WebSockets | Enabled (`--ws`); automatically disabled in HTTP/2-only mode |
| Process supervision | Supervised process group (always) |
| Reload | Disabled (`--reload`; not supported on free-threaded Python) |
| Metrics | Disabled; `127.0.0.1:9090` when enabled with `--metrics` |
| Static-file cache | `86400` seconds; no implicit route or mount |
| Minimum TLS protocol | TLS 1.3 (`--ssl-protocol-min [tls1.2\|tls1.3]`) |

### Valid Production Controls

```bash
litestar --app app:app run \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --runtime-mode auto \
    --runtime-threads 1 \
    --backpressure 1024 \
    --granian-access-log \
    --respawn-failed-workers \
    --workers-lifetime 4h \
    --workers-max-rss 512 \
    --metrics \
    --metrics-address 127.0.0.1 \
    --metrics-port 9090
```

Use these option families:

| Concern | Options |
| --- | --- |
| Processes and runtime | `--workers` (`--wc`, `--web-concurrency`, `-W`), `--blocking-threads`, `--blocking-threads-idle-timeout`, `--runtime-threads`, `--runtime-blocking-threads`, `--runtime-mode`, `--loop`, `--task-impl` |
| Capacity and flow control | `--backlog`, `--backpressure` |
| Protocols | `--http [auto\|1\|2]`, `--ws` / `--no-ws`, `--http1-*`, `--http2-*` |
| Granian logging | `--granian-log` / `--granian-no-log`, `--granian-log-level`, `--granian-access-log` / `--granian-no-access-log`, `--granian-access-log-fmt` |
| Litestar logging | `--log-config` (formatter matching is automatic) |
| TLS & mTLS | `--ssl-certificate` (`--ssl-certfile` alias), `--ssl-keyfile`, `--ssl-keyfile-password`, `--ssl-protocol-min`, `--ssl-ca`, `--ssl-crl`, `--ssl-client-verify` / `--no-ssl-client-verify`, `--create-self-signed-cert` |
| Worker lifecycle | `--respawn-failed-workers` / `--no-respawn-failed-workers`, `--respawn-interval`, `--workers-lifetime`, `--workers-kill-timeout`, `--workers-max-rss`, `--rss-sample-interval`, `--rss-samples` |
| Reload & debug (dev) | `--reload` (`-r`), `--reload-paths` (`--reload-dir`, `-R`), `--reload-include` (`-I`), `--reload-exclude` (`-E`), `--reload-ignore-dirs`, `--reload-ignore-patterns`, `--reload-ignore-paths`, `--reload-tick`, `--reload-ignore-worker-failure`, `--debug` (`-d`), `--pdb` (`--use-pdb`, `-P`) |
| Operations | `--uds` (`--unix-domain-socket`, `-U`), `--uds-permissions`, `--fd` (`--file-descriptor`, `-F`), `--url-path-prefix`, `--process-name`, `--pid-file`, `--working-dir`, `--env-files`, `--metrics` / `--no-metrics`, `--metrics-address`, `--metrics-port`, `--metrics-scrape-interval` |
| Static mounts | Repeatable `--static-path-route` and `--static-path-mount`, plus `--static-path-dir-to-file` and `--static-path-expires` |

### Supervision and Litestar CLI Parity

`litestar run` has one execution model: the Litestar parent enters server
lifespans once and supervises a fresh Granian child process group.

- **POSIX:** Starts Granian in a new session (`start_new_session=True`) and forwards signals (`SIGINT`, `SIGTERM`, `SIGHUP`) to the process group (`os.killpg`).
- **Windows:** Uses a new process group (`CREATE_NEW_PROCESS_GROUP`) and `CTRL_BREAK_EVENT` for graceful shutdown, escalating to list-based `taskkill` only if needed.
- **Graceful Shutdown & Deadlines:** The first termination signal is forwarded once and starts a deadline of `--workers-kill-timeout` plus five seconds (the CLI default is 5 seconds). A second signal or an expired deadline kills the process group.
- **Server Lifespans:** Litestar's server lifespans stay active until Granian exits and are unwound cleanly after child termination.
- **Sidecar Variables:** Server-lifespan sidecars receive the resolved `LITESTAR_APP`, `LITESTAR_HOST`, and `LITESTAR_PORT`, which is how frontend dev-server sidecars (e.g. Vite) learn the real server bind.
- **Socket Activation:** Inherited file descriptors (`-F` / `--fd` / `--file-descriptor`) are supported on POSIX systems (e.g. systemd socket activation).

### Native Static Discovery

`GranianPlugin(static=...)` is the plugin's only constructor option:

```python
app = Litestar(route_handlers=[health], plugins=[GranianPlugin(static="auto")])
```

- `"off"` (the default) keeps Litestar's static routing.
- `"auto"` lets Granian serve exactly one compatible static provider natively when its configuration is safe, and falls back to Litestar otherwise.
- Explicit `--static-path-*` CLI mounts always take precedence over either mode. Any other value raises `ValueError` at construction.

### Metrics and Observability

Metrics are off by default and are controlled only by `--metrics` / `--no-metrics`. `--metrics` exposes Granian server and worker metrics only at `http://<metrics-address>:<metrics-port>/metrics`. When no Litestar Prometheus middleware is detected, the command warns that application-level request metrics are not being exported — register Litestar's `PrometheusPlugin` alongside it when request metrics are desired.

### Programmatic / Embedded Runtime

Granian can also be executed programmatically directly from Python:

```python
from pathlib import Path
from granian import Granian
from granian.constants import HTTPModes, Interfaces, RuntimeModes


def run_embedded() -> None:
    """Execute Granian embedded server."""
    server = Granian(
        target="app.server:app",
        address="0.0.0.0",
        port=8000,
        interface=Interfaces.ASGI,
        workers=2,
        runtime_mode=RuntimeModes.auto,
        http=HTTPModes.auto,
        ssl_cert=Path("/etc/ssl/certs/app.crt"),
        ssl_key=Path("/etc/ssl/private/app.key"),
    )
    server.serve()
```

<workflow>

## Workflow

### Step 1: Match the project's deployment stack

Use `GranianPlugin` when the project already uses `litestar-granian` or needs
its Granian-specific CLI, HTTP/2, runtime, worker-lifecycle, metrics, or static
mount controls.

Keep the project's existing ASGI server when its deployment platform, process
manager, observability, or operational runbooks depend on that server. Do not
replace an established server solely because Granian is available.

Use the bare `granian` CLI only when deployment tooling intentionally invokes
Granian directly. Its CLI is a separate surface; consult the matching Granian
release instead of copying `litestar run` options.

### Step 2: Install and register

```bash
pip install "litestar-granian==0.16.0"
```

Add `GranianPlugin()` to `Litestar(plugins=[...])`, then run the application
through `litestar --app <module>:<app> run`.

### Step 3: Configure logging

0.16.0 always uses supervised execution and matches Granian's formatter to
Litestar's automatically. There is no mode to choose:

```bash
litestar --app app:app run
```

`--in-subprocess` / `--no-subprocess` and `--use-litestar-logger` /
`--no-litestar-logger` are accepted for backwards compatibility, but they are
ignored and print a deprecation warning. Remove them from deployment scripts.

Pass an explicit JSON `--log-config` only when overriding the automatic
formatter matching completely.

### Step 4: Configure the deployment and capacity

Measure the application before changing workers, runtime threads, or
backpressure. Preserve the `auto` runtime defaults unless load tests justify a
specific runtime mode.

```bash
litestar --app app:app run \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --backpressure 1024 \
    --granian-access-log
```

Terminate TLS at the platform proxy when that is the project's established
boundary. For Granian-managed TLS, pass both the certificate and key:

```bash
litestar --app app:app run \
    --ssl-certificate /etc/ssl/certs/app.crt \
    --ssl-keyfile /etc/ssl/private/app.key \
    --ssl-protocol-min tls1.3
```

### Step 5: Verify the effective command

```bash
litestar --app app:app run --help
```

Confirm the required options appear, start the service, exercise health and
WebSocket endpoints, and load-test production capacity settings.

</workflow>

<guardrails>

## Guardrails

- **Use the runtime-specific thread controls.** The 0.16.0 command exposes
  `--runtime-threads`, `--runtime-blocking-threads`, `--blocking-threads`, and `--runtime-mode`.
- **Use the namespaced access-log controls.** The 0.16.0 command exposes
  `--granian-access-log` and `--granian-access-log-fmt`.
- **Do not treat the plugin CLI as the bare Granian CLI.** The option names
  overlap but are not identical (e.g. `--granian-access-log` vs `--access-log`).
- **Do not claim that registering the plugin changes every deployment.**
  `GranianPlugin` replaces Litestar's `run` command; an external ASGI command
  still controls its own server lifecycle.
- **Do not force Granian into an established deployment stack.** Match the
  server to the project's platform and operational requirements.
- **Do not enable HTTP/2-only mode for a WebSocket endpoint.** The 0.16.0
  launcher disables WebSockets when `--http 2` is selected.
- **Do not rely on an implicit static route.** Pair every repeatable
  `--static-path-route` with a `--static-path-mount`.
- **Do not pass the deprecated compatibility flags.** `--in-subprocess` /
  `--no-subprocess` and `--use-litestar-logger` / `--no-litestar-logger` are
  ignored in 0.16.0 and emit warnings.
- **Do not expect `--metrics` to export request metrics.** It exposes Granian
  server and worker metrics only; register Litestar's `PrometheusPlugin` for
  application-level request metrics.
- **Do not perform blocking I/O in an async handler.** Use an async client or
  explicitly offload blocking work according to the application's concurrency
  model; Granian's blocking-thread setting does not make arbitrary ASGI code non-blocking.
- **Do not set `--blocking-threads` greater than 1 on ASGI.** Granian fixes
  `blocking_threads` to `1` on ASGI/RSGI and rejects `--blocking-threads > 1` with `ConfigurationError`.
- **Do not attempt `--reload` or `--workers-max-rss` on free-threaded Python.**
  Free-threaded Python builds (GIL disabled) reject these flags with `UsageError`.
- **Do not expect HTTP/3 support.** Granian 2.8.3 supports HTTP/1.1 and HTTP/2; terminate HTTP/3 at an external proxy.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] The project intentionally selected Granian over its existing ASGI server.
- [ ] `GranianPlugin()` is registered when deployment uses `litestar run`.
- [ ] Every documented option appears in `litestar run --help`.
- [ ] Deployment scripts no longer pass deprecated `--in-subprocess` or
      `--use-litestar-logger` compatibility flags.
- [ ] Logging relies on automatic formatter matching or an intentional
      `--log-config` override.
- [ ] HTTP/2-only mode is not used for required WebSocket endpoints.
- [ ] Static routes and mounts have equal counts and are paired in order.
- [ ] `--metrics` is paired with Litestar's `PrometheusPlugin` when application request metrics are required.
- [ ] Worker, thread, and capacity changes are backed by load-test results.
- [ ] TLS terminates at the documented platform or Granian boundary.
- [ ] Free-threaded Python deployments omit `--reload` and `--workers-max-rss`.

</validation>

<example>

## Example

**Task:** Run an existing Litestar application with Granian, enable access logs,
configure worker recycling, and expose Granian metrics to a local collector.

```python
from litestar import Litestar, get
from litestar_granian import GranianPlugin


@get("/health")
async def health() -> dict[str, str]:
    """Return application health check status."""
    return {"status": "ok"}


app = Litestar(
    route_handlers=[health],
    plugins=[GranianPlugin(static="auto")],
)
```

```bash
litestar --app app:app run \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --runtime-mode auto \
    --runtime-threads 1 \
    --granian-access-log \
    --respawn-failed-workers \
    --workers-lifetime 4h \
    --workers-max-rss 512 \
    --metrics \
    --metrics-address 127.0.0.1 \
    --metrics-port 9090
```

`--metrics` exposes Granian server and worker metrics at `http://127.0.0.1:9090/metrics`.
Register Litestar's `PrometheusPlugin` alongside it to also export
application-level request metrics.

</example>

## References Index

- **[CLI Reference](references/cli-reference.md)** — Exhaustive parameter matrix for `litestar run` with `litestar-granian` and standalone `granian`.
- **[Runtime & Tuning Guide](references/runtime-and-tuning.md)** — Concurrency models, thread pools, HTTP/1 & HTTP/2 flow control, memory limits, and platform constraints.
- **[Embedded Runtime & Lifecycle](references/embedded-and-lifecycle.md)** — Programmatic `granian.Granian` and `granian.server.embed.Server` execution, supervisor architecture, signals, lifespans, and static provider discovery.
- **[litestar](../litestar/SKILL.md)** — Application initialization and plugin registration.
- **[litestar-deployment](../litestar-deployment/SKILL.md)** — Deployment target, proxy, container, and process-manager selection.
- **[litestar plugins](../litestar/references/plugins.md)** — Litestar plugin protocols and initialization behavior.

## Official References

- [litestar-granian v0.16.0 source](https://github.com/cofin/litestar-granian/tree/v0.16.0)
- [v0.16.0 CLI implementation](https://github.com/cofin/litestar-granian/blob/v0.16.0/litestar_granian/cli.py)
- [v0.16.0 plugin implementation](https://github.com/cofin/litestar-granian/blob/v0.16.0/litestar_granian/plugin.py)
- [v0.16.0 changelog](https://github.com/cofin/litestar-granian/blob/v0.16.0/docs/changelog.rst)
- [litestar-granian 0.16.0 on PyPI](https://pypi.org/project/litestar-granian/0.16.0/)
- [granian v2.8.3 repository](https://github.com/emmett-framework/granian/tree/v2.8.3)
- [granian documentation](https://granian.readthedocs.io/)

## Shared Styleguide Baseline

- [General Principles](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
