---
name: mcp-server-triage
description: Use when an MCP server fails, is missing, or is being added.
trigger: MCP server shows "failed" in the banner, MCP tools missing, "failed initial connection", "parked", OAuth token problems, registering a new stdio MCP server
category: mcp
version: 1.1.0
---

# MCP server connection triage

## Trigger

- The startup banner's **MCP Servers** block shows `— failed` or a server with
  `0 tool(s)` next to it.
- An MCP tool the user expects is not in the toolset.
- `logs/errors.log` contains `MCP server '<name>' failed initial connection ...`
  or `MCP OAuth setup failed for '<name>'`.

**The banner's MCP block is ground truth.** It is rendered from the live
connection state (per-server tool counts), so read it BEFORE theorising:

```
MCP Servers
  blender (stdio) — disabled
  linear  (http) — 68 tool(s)
  notion  (http) — 69 tool(s)
  sentry  (http) — failed
  stripe  (http) — 15 tool(s)
```

`— disabled` means the config entry has `enabled: false` (not a failure).
`— failed` means the connect attempt did not reach a live session.

## The two failure classes (they look identical in the log)

| Log line | Class | Fix |
|---|---|---|
| `MCP server 'X' failed initial connection after 3 attempts, parking ...: TimeoutError` | **Transport/handshake** — the server was reachable but the session never came up | see the probe ladder below |
| `MCP OAuth setup failed for 'X': MCP OAuth for 'X': non-interactive environment and no cached tokens found` | **Credentials** — there is no usable token on disk | `openamer mcp login X` (needs a TTY) |
| `MCP server 'X' failed initial OAuth authentication, not retrying automatically: OAuthNonInteractiveError` | same as above, worded from the other code path | same |

The `TimeoutError` is a **symptom, not a diagnosis**. A server with no cached
OAuth token can surface as a timeout, because the OAuth provider never gets a
usable bearer token and the handshake never completes. Do not report "the MCP
server is down" until you have separated the two classes.

## Step 1 — the cheap discriminator: does a token exist, and is it live?

```bash
cd "$OPENAMER_HOME"
for n in linear notion stripe sentry supabase vercel; do
  f="mcp-tokens/$n.json"
  if [ -f "$f" ]; then
    python -c "import json,time;d=json.load(open(r'$f'));print('$n','expires_in',round(d['expires_at']-time.time()),'s')"
  else
    echo "$n NO TOKEN FILE"
  fi
done
```

- **No token file at all** ⇒ that server was never authorized here. It can never
  connect in a non-interactive context. Fix: `openamer mcp login <name>`.
- **Token file exists but `expires_in` is negative** ⇒ expired; the provider
  should refresh it, but only if a refresh token is present.
- **Token file exists and is fresh** ⇒ the credential is fine, so the failure is
  transport/handshake. Continue to step 2.

A `<name>.client.json` (dynamic client registration) and `<name>.meta.json`
(OAuth server metadata) may sit next to the token; their absence is normal for
pre-registered clients.

## Step 2 — the probe ladder (prove where it breaks)

Run all three; the first level that fails localises the fault. Use
`scripts/probe_mcp_servers.py` for levels 2 and 3.

1. **Raw HTTP** — is the endpoint alive and does it answer `initialize`?
   ```bash
   curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" -m 20 -X POST https://mcp.linear.app/mcp \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json, text/event-stream' \
     -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}'
   ```
   `401` = the endpoint is alive and demands auth (expected without a token).
   `000`/timeout = the host is genuinely unreachable.
2. **Raw SDK** — `mcp.client.streamable_http.streamable_http_client` + `ClientSession`
   with the stored bearer token. Success here proves the MCP handshake works.
   On mcp >= 1.24 the client must be constructed explicitly and passed in:
   ```python
   async with httpx.AsyncClient(follow_redirects=True,
                                timeout=httpx.Timeout(30.0, read=300.0),
                                headers={"Authorization": f"Bearer {tok}",
                                         "Accept": "application/json, text/event-stream"}) as c:
       async with streamable_http_client(url, http_client=c) as (r, w, sid):
           async with ClientSession(r, w) as s:
               await s.initialize(); await s.list_tools()
   ```
   Gotcha: `streamable_http_client(url, headers=...)` raises `TypeError` on
   mcp 1.24+ — the `headers=` kwarg was removed. Build the `httpx.AsyncClient`.
3. **The real OpenAmer path** — `tools.mcp_tool.MCPServerTask(name).start(config)`
   with the config from `mcp_tool._load_mcp_config()`. This is the only level
   that exercises OpenAmer's own OAuth provider, transport options and parking
   logic. A level-2 success plus a level-3 failure means the fault is in
   OpenAmer's connection code, not in the network or the credentials.

**Do not conclude "the network is broken" from level 3 alone.** Measure the
levels separately and report which one failed.

## Step 3 — the fix per class

- **Missing/expired token** → `openamer mcp login <name>` **interactively**
  (needs a real TTY; a background/cron/daemon context cannot complete the
  browser flow). Then restart the surface so it reconnects.
- **Handshake timeout on a server that HAS a token** → re-run the probe ladder
  once (startup races are common when every server connects concurrently) and
  only then treat it as a real fault. Check `connect_timeout` in the server's
  `mcp_servers` config entry.

## The other direction: ADDING a server without flooding context

Registering a server is the same object as triaging one — same config entry, same
`.client.json` / token directory, same banner — but the failure mode is inverted:
it connects fine and then costs context in **every** session, because every
advertised tool schema is paid for on load. Measured on a 229-tool server: 229
tools unscoped vs **79** after a scope of six families, with `expected 79 /
observed 79 / missing []` from the server's own doctor.

Rules:

- **Search before you build.** `openamer a2a mcp-catalog "<keywords>" --limit 10`
  queries the official registry (~40k servers, keyless) and falls back to the
  community README (~1.9k). Search only *finds*; installing still goes through
  `openamer mcp add` / `openamer mcp install <approved-name>` because those are
  supply-chain-pinned. Do not hand-pin an arbitrary repo from a search hit.
- **Measure the menu before registering.** `openamer mcp add` runs a
  discovery-first install and asks `Enable all N tools? [Y/n/select]`. That `N` is
  the number you are about to pay. If the server supports family scoping via an env
  var, set it in the registration (`--env VAR=family-a,family-b`) so the count is
  bounded at source, not by deselecting 150 rows.
- **Use an absolute interpreter path** for a stdio server when more than one
  runtime is installed. `--command node` resolves to whatever is first on `PATH`
  (possibly a version the package's `engines` rejects); pin
  `--command "C:/Users/<u>/tools/node-v<ver>/node.exe"`.
- **Headless registration hangs on the prompt.** `openamer mcp add` waits for
  stdin: `printf 'y\n' | openamer mcp add <name> --env … --command … --args …`.
  Without it the output ends in `Enable all N tools? … Cancelled.` and nothing is
  written — which reads like a failed install.
- **`--args` must be the LAST option** (it is variadic and swallows what follows).
- Verify both halves, because they are separate facts: `openamer mcp list` shows
  the entry enabled, `openamer mcp test <name>` proves it connects **and**
  enumerates the tools it will advertise.
- A new session is required before the tools appear in the agent's own toolset
  (`Start a new session to use these tools.`) — do not read the current session's
  unchanged tool list as a failed registration.
- When the server's error says `Tool … disabled`, the fix is the **family id**, not
  a reinstall; and when an invalid family id fails startup, the server prints the
  complete valid list in one line — that is the cheapest way to discover them.

## Pitfalls

- **A "This tip only shows once" banner hint is not a defect.** `openclaw`
  residue tips are gated by `onboarding.seen.<flag>` in `config.yaml`; if the
  flag is `true` the tip is correctly suppressed. Verify with
  `is_seen(config, OPENCLAW_RESIDUE_FLAG)` before reporting it as a bug.
- **The `ctx --` in the status bar is not a missing context window.** It means
  the agent was not yet initialised when the bar was rendered. The real window
  is measurable: `agent.context_compressor.context_length` and
  `agent.model_metadata.get_model_context_length(model, base_url=..., provider=...)`.
  Report the measured number, not the placeholder.
- **The banner's `upstream <sha> · local <sha> (+N carried commits)` is a
  snapshot from process start.** Re-run `git fetch origin main` and
  `git rev-list --count origin/main..HEAD` before quoting it; the local commit
  may already be pushed.
- **Never "fix" a failing MCP server by disabling it** to make the banner look
  clean. Either fix the credential, or report it as failed with the measured
  evidence.

## Verify

```bash
# after `openamer mcp login <name>`, restart the surface and re-read the banner
openamer chat -q "list your MCP tools"     # or just start the CLI and read the block
# or measure directly:
python scripts/probe_mcp_servers.py       # prints READY/FAIL per server
```

## References & scripts

- `references/mcp-ecosystem-2026.md` — where servers come from (official
  registry endpoint + response shape + the three parsing traps), the protocol
  versions actually installed vs current, the exact `FastMCP` → `MCPServer`
  break in mcp 2.x, and the A2A / WebMCP / commerce state. Read this before
  changing catalog, transport or protocol code.
- `references/session-measurements.md` — a measured 6-server triage on this
  host: which ones connect in ~2 s, which ones park, and the exact log lines.
- `scripts/probe_mcp_servers.py` — token-file/expiry check plus the raw-SDK and
  real-OpenAmer-path probes, with per-server timing.
