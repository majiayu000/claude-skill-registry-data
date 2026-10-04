---
name: msw-cli
description: >-
  Control MSW mocks at runtime via msw-cli (open session, add/update/remove handlers).
  Use when mocking APIs, changing mock responses, or debugging MSW without restarting the app.
---

# msw-cli

Dynamically add, update, and remove MSW handlers while the app keeps running. Run commands from the project directory (or pass `-s <name>` for a named session).

Project not set up yet? Use the **msw-setup** skill or run **`msw-cli setup`** first.

## Agent guidelines

When using this skill to change mocks:

1. **Do not edit local handler files** (e.g. `handlers.ts`, `mocks/handlers`). `msw-cli` applies `add` / `update` / `remove` / `reset` to the **browser runtime** over the WebSocket session. Changing on-disk handler modules is the wrong tool and can confuse the next dev reload.

2. **Before `open`**, check whether a session is already running: run **`msw-cli list`** (all open sessions) and, if a session for this project already exists, **`msw-cli status`** (or `status -s <name>`) to see connection and handlers. Only run **`open`** when no suitable session is active—avoid duplicate daemons for the same work.

## Quick start

```bash
msw-cli open                    # prints WebSocket URL + port
# If port ≠ app config, update MSW_WS_URL (or VITE_MSW_WS_URL / NEXT_PUBLIC_MSW_WS_URL) to match output
msw-cli add "http.get('/api/users', () => HttpResponse.json([{ id: 1 }]))"
msw-cli status                  # connected must be true for mocks to apply
msw-cli close
```

Use `msw-cli open --port 6789` when the app already hard-codes that port. **`list`** works without a session. Handler commands (`add`, `update`, `remove`, `reset`, `status`) **require** an open session for that cwd (or `-s`) — otherwise you get "Session not open".

## Workflow

1. **`list`** / **`status`** — confirm no session is already open (or reuse it). Then **`open`** only if needed — start daemon; read **Port** and **WebSocket** from markdown output.
2. Sync app — if port auto-changed (6789 busy), set `ws://127.0.0.1:<port>` in `MSW_WS_URL` / `VITE_MSW_WS_URL` / `NEXT_PUBLIC_MSW_WS_URL` env.
3. `add` / `update` / `remove` / `reset` — handler changes.
4. `status` — confirm browser connected.
5. `close` when finished.

Sessions: default name = current directory basename. State: `~/.msw-cli/sessions/`.

## Handler rules

- Valid JS strings; `http`, `graphql`, `HttpResponse`, `bypass`, `passthrough`, `delay` are in scope (no imports).
- Wrap handlers in double quotes; use single quotes inside JS.
- Return a `Response` via `HttpResponse` (e.g. `HttpResponse.json({ ok: true })`).
- **Passthrough / partial override** — fetch the real response, then override fields. Always wrap the request in `bypass()` to avoid an infinite intercept loop:

```bash
msw-cli add "http.get('*/api/user', async ({ request }) => { const res = await fetch(bypass(request)); const data = await res.json(); return HttpResponse.json({ ...data, role: 'admin' }) })"
```

## Pattern matching (remove / update)

`status` displays handlers as `METHOD URL`, e.g. `GET */api/v1/users/*`. But `remove` / `update` patterns match the **handler URL only** (substring or `*` glob) — not the method.

| Command           | Pattern is…                    | Example                |
| ----------------- | ------------------------------ | ---------------------- |
| `status`          | Display only: `METHOD` + `URL` | `GET */api/v1/users/*` |
| `remove`/`update` | URL substring or `*` glob      | `*/api/v1/users/*`     |

- To filter by method, use `-m, --method <methods...>` (e.g. `remove "*/api/users" -m GET`).
- A leading method token in the pattern (e.g. `"GET */api/users"`, copied from `status`) is auto-split into a method filter, so pasting a status line works — but prefer the URL-only pattern plus `-m` for clarity.
- `remove`/`update` report how many handlers matched. **`Removed 0`** or **`0 matched`** means the pattern matched nothing — fix the pattern, do not retry with another `update` (that just adds a duplicate).

## Commands

| Command                                                                                      | Purpose                                   |
| -------------------------------------------------------------------------------------------- | ----------------------------------------- |
| `open [--port N] [-s name] [--no-persist-handlers] [--persist-handlers N] [--single-client]` | Start/reuse daemon (required first)       |
| `add "<handler>"`                                                                            | Add handler(s)                            |
| `update "<pattern>" [-m METHOD...] -h "<handler>"`                                           | Replace handlers matching pattern         |
| `remove "<pattern>" [-m METHOD...]`                                                          | Remove handlers (reports match count)     |
| `reset [handlers...]`                                                                        | Clear runtime handlers (optional new set) |
| `status`                                                                                     | Connection + active handlers              |
| `list`                                                                                       | All open sessions                         |
| `close [name]` / `close-all`                                                                 | Stop daemon(s)                            |

## Troubleshooting

- **Session not open** → run `msw-cli list`; if no session for this project, run `open`, then retry.
- **No browser clients connected** → app not wired to the WebSocket URL from `open`; fix port/env and reload.
- **Mock not firing** → match request path exactly or use wildcards (`*/api/users/*`).
- **`remove` says "Removed 0"** → the pattern matched no handler. Drop any HTTP method prefix (patterns match the URL only) and match the URL from `status`, e.g. `remove "*/api/v1/users/*"`. Use `-m GET` to filter by method.
- **Duplicate handlers after `update`** → the `update` pattern matched nothing, so it added a second handler instead of replacing (the CLI warns `0 matched`). `remove "*/api/..."` the extras, then `update`/`add` once with a correct URL pattern.
- **`open --port` fails** → port in use; free it or use `open` without `--port` and sync app to the new port.
- **Handler syntax errors** → check shell quoting and JS validity.
