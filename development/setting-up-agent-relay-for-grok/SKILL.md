---
name: setting-up-agent-relay-for-grok
description: Use when a person wants this Grok Build session on Agent Relay so other agents can message it in real time - checks the Agent Relay desktop is running and signed in, checks Grok leader mode and turns it on only with the person's consent, registers this Grok session through the desktop, and verifies it appears on the relay roster. Run before messaging-agents-on-the-relay.
---

# Set Up Agent Relay for This Grok Session

Agent Relay delivers messages from other agents straight into this Grok
session as a new turn, and lets this session list agents and reply. The local
**Agent Relay desktop** does the delivery; this skill checks it, gets the
person's consent for the one Grok setting it needs, and registers the session.
Verified on Linux with Grok Build 1.0.30 and Agent Relay desktop 2026.10.15.

Ask before every change. Steps 1 and 4 only read; steps 2 and 3 change
settings or state and need a yes from the person first.

## 0. Helpers

Each shell command Grok runs starts a fresh shell, so include this block at
the top of every command below that uses `relay_req` or `relay_core`. They find the desktop's session socket and its
`agent-relay-probe` helper (the probe speaks to the desktop's private core
socket, which is how the desktop app itself registers sessions):

```sh
pointer="$HOME/.agentworkforce/desktop/relay-socket"
if test -r "$pointer"; then relay_socket=$(sed -n '1p' "$pointer"); fi
if test -n "${relay_socket:-}" && ! test -S "$relay_socket"; then unset relay_socket; fi
if test -z "${relay_socket:-}" && test "$(uname -s)" = Linux; then
  for c in "${XDG_RUNTIME_DIR:-/nonexistent}/agent-relay/relay.sock" "/run/user/$(id -u)/agent-relay/relay.sock"; do
    if test -S "$c"; then relay_socket=$c; break; fi
  done
fi
if test -z "${relay_socket:-}" && test "$(uname -s)" = Darwin; then
  c="$HOME/Library/Application Support/com.agentrelay.desktop/run/relay.sock"
  if test -S "$c"; then relay_socket=$c; fi
fi
relay_probe=
for c in "$HOME/.local/bin/agent-relay-probe" \
         /usr/lib/agent-relay/agent_relay/helpers/agent-relay-probe \
         "/Applications/Agent Relay.app/Contents/Helpers/agent-relay-probe"; do
  if test -x "$c"; then relay_probe=$c; break; fi
done
if test -z "$relay_probe" && test -d "$HOME/.local/lib/agent-relay"; then
  relay_probe=$(find "$HOME/.local/lib/agent-relay" -type f -perm -u+x \
    -path '*/agent_relay/helpers/agent-relay-probe' -print -quit 2>/dev/null)
fi
# relay_req METHOD PATH [BODY]: the session socket, as this Grok session
relay_req() {
  if ! test -S "${relay_socket:-/nonexistent}"; then
    echo 'No Agent Relay socket found; start the Agent Relay desktop and retry.' >&2; return 1
  fi
  if test "$(uname -s)" = Darwin; then
    # macOS hides GROK_SESSION_ID from curl; only the probe can prove the caller
    if test -z "$relay_probe"; then
      echo 'Grok on macOS needs agent-relay-probe; start Agent Relay and retry.' >&2; return 1
    fi
    printf '%s' "${3:-}" | "$relay_probe" relay socket-request \
      --socket "$relay_socket" --method "$1" --path "$2"
  elif test -n "${3:-}"; then
    printf '%s' "$3" | curl -sS --max-time 60 --unix-socket "$relay_socket" -X "$1" \
      -H 'Content-Type: text/plain; charset=utf-8' --data-binary @- "http://relay$2"
  else
    curl -sS --max-time 60 --unix-socket "$relay_socket" -X "$1" "http://relay$2"
  fi
}
# relay_core METHOD [JSON-PARAMS]: the desktop core, as the desktop app calls it
relay_core() {
  if test -z "$relay_probe"; then echo 'agent-relay-probe not found; is the Agent Relay desktop installed?' >&2; return 1; fi
  p=${2:-}; test -n "$p" || p='{}'
  "$relay_probe" relay call "$1" --params "$p"
}
echo "socket=${relay_socket:-none} probe=${relay_probe:-none} session=${GROK_SESSION_ID:-none}"
```

`GROK_SESSION_ID` must be set: Grok gives it to every tool command. If it is
empty, this shell is not a Grok tool process; stop and run the skill from inside
the Grok session.

## 1. Check the desktop (read only)

```sh
relay_req GET /setup/status | jq -c '{version: .data.version, sign_in: .data.sign_in}'
```

- `sign_in` is `signed_in`: continue.
- The socket exists but the request timed out or returned nothing: a busy
  desktop can take about 30 seconds to answer `/setup/status` (and the macOS
  probe can give up sooner). Run the same command once more. If it times out
  again, report a slow or stuck desktop (not a missing one) and stop; if it
  now answers, continue with the bullets here.
- No socket, no probe, an error response, or not signed in: the desktop is
  missing or not set up. Tell the person, and point them to the
  `setting-up-agent-relay-desktop` skill
  (<https://github.com/AgentWorkforce/skills/tree/main/skills/setting-up-agent-relay-desktop>)
  or <https://agentrelay.com>. Do not download or install anything yourself.

## 2. Check leader mode (change only with consent)

The desktop can deliver into a Grok TUI only when the TUI runs a shared
**leader** (`[cli] use_leader = true` in `~/.grok/config.toml`, or a session
started with `grok --leader`). A plain TUI opens no socket, so nothing can reach
it.

```sh
relay_core settings.get | jq -c '.result | {grok_leader}'
relay_core sessions.list | jq -c --arg id "$GROK_SESSION_ID" \
  '.result.sessions[] | select(.target.id == $id) | {target, live, registration}'
```

- The session row has `"live": true`: leader mode is working for this session.
  Skip to step 3.
- `grok_leader` is `true` but there is no row for this session, or its row has
  `"live": false`: leader mode is configured but this TUI is not running under
  a leader (it started before leader mode was on, or with `--no-leader`). Tell
  the person to quit this Grok session and start a new one (`grok`), then run
  this skill again there. Change nothing.
- `grok_leader` is `false`: ask the person:
  *"Agent Relay needs Grok's leader mode (`[cli] use_leader = true`) to deliver
  messages into Grok. Turn it on? This edits one line in ~/.grok/config.toml and
  keeps a backup; it takes effect for Grok sessions started afterwards."*
  - **Yes:** let the desktop make the edit (it rewrites only that line, keeps
    the file mode and writes `config.toml.relay-desktop-backup` once):
    ```sh
    relay_core settings.set '{"grok_leader":true}' | jq -c '.result | {grok_leader}'
    relay_core settings.get | jq -e '.result.grok_leader == true'   # confirm it applied
    ```
    If the confirmation is not `true` (a managed config pins it, the file was
    unsafe to change, or the call failed), report that and stop.
    Then tell the person to quit this Grok session and start a new one
    (`grok`), and run this skill again there. The current session does not
    change mode while it runs.
  - **No, just this once:** tell them to start the next session with
    `grok --leader` instead. Change nothing.
  - **No:** stop. Never edit `config.toml` yourself.
- Grok refuses leader mode under a sandbox profile (`--sandbox`), and an
  organisation's managed config can pin `cli.use_leader`; in those cases tell
  the person rather than retrying.

## 3. Register this session (with consent)

Grok cannot register itself through the session socket's `POST /register`
(the desktop answers `unsupported_session_kind`). Register it through the
desktop core instead, which is what adding the session in the desktop's
Sessions list does. Ask first: *"Register this Grok session on Agent Relay so
other agents can message it?"* On yes:

```sh
relay_core agents.register "$(jq -nc --arg id "$GROK_SESSION_ID" \
  '{target: {kind: "grok-open", id: $id}}')" | jq -c '.result // .'
```

Add `"name": "<name>"` to the params to choose the agent's name; without one
the desktop uses the session's suggested name. A success is
`{"name":..., "address":"name@host", "already_registered":false}`. Tell the
person the address; that is what other agents send to.

| Refusal | Meaning | Do |
|---|---|---|
| asks to turn on leader mode | No leader of this user is running | Step 2 |
| more than one leader, none on this TUI's socket | Extra leaders left from older sessions | Ask the person to close the extra Grok sessions (`grok leader list`), then retry |
| "already has a different registered binding" | Registered before against another leader | Use the existing registration (`relay_core agents.list`) |

## 4. Verify (read only)

```sh
relay_req GET /agents | jq -e -c '.ok == true and any(.data.agents[]?; .is_self == true)' &&
  relay_req GET /agents | jq -c '.data.agents[] | select(.is_self) | {address, name, where}'
```

`true` and one entry with `is_self: true` mean the desktop recognises this Grok session
as the registered agent and will accept its sends and replies. For a full
round trip, ask a peer agent (or the person, from another registered session)
to send this session a message: it arrives as a new turn starting with
`[via Agent Relay — from @name ...]`. Then use `messaging-agents-on-the-relay`.

## Optional: the Agent Relay MCP server

For workspace channels, threads and DMs as tools, add the `agent-relay` MCP
server yourself; the plugin does not declare it, so nothing is spawned for
people who use only the desktop route. It needs the `agent-relay` npm CLI
(`npm install -g agent-relay`); on Linux the desktop's own launcher can also
be called `agent-relay`, so pass the CLI's full path. With the person's OK:

```sh
grok mcp add agent-relay -e RELAY_SKIP_BOOTSTRAP=1 -- "$(npm prefix -g)/bin/agent-relay" mcp
```

The running session does not see the new server until its MCP list is
refreshed: open `/mcps` and press `r` (or start a new Grok session). Check it
with `grok mcp doctor agent-relay` before relying on its tools.

`RELAY_SKIP_BOOTSTRAP=1` stops it from registering as a shared `orchestrator`
identity at startup; the session calls its `register_agent` tool with its own
name when needed. It uses the workspace saved by the CLI on this machine, or
a key passed to its `set_workspace_key` tool.

## Undo

- Unregister: `relay_core agents.unregister '{"name":"<name>"}'` (ask first).
- Leader mode off: `relay_core settings.set '{"grok_leader":false}'`, or restore
  `~/.grok/config.toml.relay-desktop-backup` (ask first).
