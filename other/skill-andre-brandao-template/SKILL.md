---
name: template-cli
description: Run and talk to the template app from the terminal — serve the api/mcp/auth/dashboard surfaces, call any API endpoint through the generated SDK, and manage login. Use when asked to start a local server, hit an endpoint, or check the current user.
---

# template-cli

`bun run cli <command>` from the repo root, or `template-cli <command>` once the bin is
linked.

## Serve

```sh
template-cli serve api         # Hono API on API_PORT (default 3000)
template-cli serve mcp         # MCP server on MCP_PORT (default 3001), at /mcp
template-cli serve auth        # OpenAuth issuer on PORT (default 3002)
template-cli serve dashboard   # SvelteKit prod build on PORT (auto-builds if missing)
```

All except `dashboard` need a reachable `DATABASE_URL`. For a local DB run `bun dev`
first.

## Call the API

The method list is reflected off the generated `@template/sdk`, so it always matches the
current endpoints. Discover before guessing:

```sh
template-cli api                              # list callable methods
template-cli api getTodo                      # GET /todo
template-cli api postTodo --title "Ship it"   # POST /todo
template-cli api postTodo '{"title":"Ship"}'  # same, as a JSON blob
template-cli api getTodoById --id tod_123
```

Flags become call params (`--key value`, `--key=value`, or bare `--flag` for `true`).
Values coerce to number/boolean when they look like one. `--token` and `--url` are
consumed by the client and never sent as params.

Results print as JSON on stdout; errors print as JSON on stderr and exit non-zero — so
pipe into `jq` and check the exit code.

## Auth

```sh
template-cli login     # opens the browser, PKCE, saves tokens
template-cli whoami    # current user
template-cli logout
```

`login` writes `~/.config/template/config.json` (respects `XDG_CONFIG_HOME`) and opens a
loopback server on port 3006 for the callback; it times out after 2 minutes. It needs a
browser — in a headless session, set `TEMPLATE_TOKEN` to an `sk-` API key instead.

Token: `--token` › `TEMPLATE_TOKEN` › saved key › saved OAuth access (auto-refreshed).
Base URL: `--url` › `API_URL` › saved config › `http://localhost:3000`.
Issuer: `--issuer` › `AUTH_URL` › saved config › `http://localhost:3002`.
