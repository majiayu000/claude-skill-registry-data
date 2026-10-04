---
name: validate-ws
description: Run a bounded, protocol-aware WebSocket probe with an OIDC bearer token
argument-hint: "<ws-path-or-url>"
user-invocable: true
---

# Validate WebSocket

Resolve `WS_BASE_URL` and `WS_PATH` (or a complete URL) from `$ARGUMENTS` and
project configuration. Confirm before contacting production.

Discover or ask for the application's first message, expected response,
subprotocol, and Origin policy. A generic JSON ping is not a WebSocket control
ping and must not be invented.

Use `$TOKEN` or `${TOKEN_COMMAND:-scripts/get-backend-token.sh}`; if missing,
route through `/backend-validator:get-dev-token`.

Run a one-message probe with a bounded command timeout and verified websocat
flags. Do not use verbose mode unless handshake evidence is needed, because it
can expose Authorization.

Report handshake, send, reply, timeout, close, and protocol evidence separately.
No reply is not automatically failure for a one-way protocol.

Load `references/websocat-patterns.md` for subprotocol, Origin, framing,
reconnect, and failure-interpretation details.
