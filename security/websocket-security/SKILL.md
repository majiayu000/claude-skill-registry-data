---
id: websocket-security
version: "2.0.0"
title: "WebSocket Security"
description: "Securing the WebSocket upgrade and the frames after it: Origin validation against Cross-Site WebSocket Hijacking, authenticating the handshake rather than the first message, the ticket pattern for browsers that cannot set headers, per-frame authorization, and resource limits on a connection that stays open. Use when generating a WebSocket, Socket.IO, SignalR, or Phoenix Channels server, wiring real-time messaging, presence, or collaborative editing, or reviewing a /ws endpoint."
category: prevention
severity: high
applies_to:
  - "when generating a WebSocket / Socket.IO / SignalR / Phoenix Channels server"
  - "when wiring real-time messaging, presence, or collaborative editing"
  - "when authenticating a long-lived connection from a browser"
  - "when reviewing /ws or wss:// endpoint exposure"
languages: ["javascript", "typescript", "python", "go", "java", "csharp", "ruby", "elixir"]
token_budget:
  minimal: 1300
  compact: 1800
  full: 2200
rules_path: "rules/"
related_skills: ["auth-security", "cors-security", "api-security", "protocol-security"]
last_updated: "2026-08-14"
sources:
  - "OWASP WebSocket Security Cheat Sheet"
  - "RFC 6455 — The WebSocket Protocol"
  - "CWE-1385: Missing Origin Validation in WebSockets"
  - "CWE-770: Allocation of Resources Without Limits or Throttling"
---

# WebSocket Security

## Rules (for AI agents)

### ALWAYS
- Validate the **`Origin` header** on the upgrade handshake against an allowlist, and
  understand precisely what that buys: the browser sets `Origin` and script cannot
  forge it, so the check stops **Cross-Site WebSocket Hijacking** — a page on
  `attacker.com` opening `wss://api.example.com/ws` and inheriting the user's cookies.
  It buys nothing against a non-browser client, which sets any header it likes. Origin
  is a CSRF control, not authentication. The same-origin policy and CORS preflight do
  not apply to the upgrade at all, which is why this check must be written by hand.
- Authenticate the **handshake**, not the first frame. Once the upgrade completes the
  connection exists, has consumed the user's cookie context, and is already a resource
  the caller controls. A `subscribe` or `auth` message afterwards is too late.
- For a browser client, pick one of two mechanisms, because the browser `WebSocket`
  constructor **cannot set request headers** — there is no `Authorization` header
  available to you:
  1. **Cookie on the upgrade** plus the `Origin` check above as the CSRF control, or
  2. A **single-use ticket**: the authenticated page calls an ordinary HTTP endpoint,
     receives a short-lived opaque ticket bound to the user and to the intended
     resource, passes it in the URL, and the server **redeems and invalidates it at
     handshake time**. A ticket is safe in a URL precisely because replaying it fails.
- Re-authorize **every frame**, both the action and the subject it names. A frame like
  `{"action":"write","subjectId":"X"}` must be checked against the principal
  established at handshake — an authenticated socket must never be able to assert an
  arbitrary subject id per frame. That is per-frame BOLA, and the forged id reaches
  every consumer downstream of the socket that trusts it. Permissions also change
  while the connection is open: logout, role change, account lock, token expiry. A
  socket opened an hour ago carries an authorization decision an hour old.
- Bound the connection: maximum frame and message size, messages per second per
  connection, concurrent connections per user and per source address, and total
  connection lifetime after which the client must re-handshake. A WebSocket is an
  allocation that persists, so every limit HTTP gets per-request must be re-expressed
  per-connection. Concrete starting values, and the backpressure and heartbeat
  settings, are in `references/limits-and-handshake.md`.
- Use **`wss://`**. `protocol-security` owns the TLS configuration behind it; what
  belongs here is that `ws://` exposes the session token, every frame, and the
  handshake itself to any on-path observer.
- Consult `auth-security` for the token's own properties — lifetime, rotation, and why
  a bearer token does not belong in a URL — and `cors-security` for the origin
  allowlist itself, including how to treat the serialized `null` origin.

### NEVER
- Skip Origin validation on the grounds that "CORS does not apply to WebSockets."
  That is the reason the check is required, not a reason to omit it.
- Put a **bearer token** — a JWT, a session id, an API key — in the WebSocket URL.
  URLs reach access logs, proxy logs, `Referer` headers and browser history, and a
  token that survives being read there is a token an attacker can replay. The
  single-use ticket above is the form that is safe in a URL; a reusable credential is
  not, and `auth-security` owns that rule for every other transport.
- Treat a session cookie as a long-lived connection credential that outlives the
  session it came from. If the socket must survive re-authentication, redeem a fresh
  ticket on reconnect.
- Let a client-supplied **subprotocol** influence server-side routing or handler
  selection without an allowlist. Subprotocol negotiation is attacker-controlled input.
- Run WebSocket handlers on the same bounded thread pool or event loop as HTTP request
  handlers with no separate sizing. A slow or chatty socket then starves ordinary
  request work, which is the same failure as a slow-loris with a longer lease.
- Put internal topology into frames — pod names, node ids, upstream hostnames,
  internal error text. A real-time channel is a chatty reconnaissance surface.
- Reconnect without **bounded exponential backoff and jitter** on the client. An
  outage otherwise converts every client into a synchronized retry flood at the moment
  the service is least able to absorb it.

### KNOWN FALSE POSITIVES
- A **deliberately public** endpoint — a public presence or broadcast feed carrying no
  per-user data — may accept any origin. What it may not skip is the per-connection
  and per-source limits, because an open endpoint is the one most exposed to them.
- A native mobile or desktop client sends **no `Origin` header at all**, which is a
  different case from the string `null`. Absent means "not a browser": decide whether
  to admit it and authenticate it some other way. `null` means an opaque origin — a
  sandboxed iframe, a `data:` URL, a `file://` document — and on a credentialed
  endpoint it should be rejected, exactly as `cors-security` requires.
- A frame that carries no subject id, because the connection is scoped to one resource
  at handshake, is not missing per-frame authorization. Binding the subject once, at
  the upgrade, is the stronger design.
- Plaintext `ws://` between services is acceptable where a **service mesh terminates
  mTLS** underneath it, because the mesh supplies a cryptographic peer identity. It is
  not acceptable because the traffic is inside a VPC — a private network is a location,
  not an authentication.

## Context (for humans)

A WebSocket inverts the assumption every HTTP control is built on. HTTP gets a fresh
authorization decision per request; a WebSocket makes one decision at the upgrade and
then runs on it for as long as the socket lives. Everything in this skill follows from
that: authenticate the handshake because there is only one, re-authorize each frame
because the single decision goes stale, and bound the connection because it is an
allocation nobody is forced to release.

The browser header limitation is worth stating plainly because it is the source of the
worst advice in this area. `new WebSocket(url, protocols)` accepts a URL and a
subprotocol list and nothing else — no headers. Faced with that, developers put the
JWT in the query string, and most guidance lets them. The ticket pattern exists because
it keeps the property that matters: what appears in the URL is worthless once used, so
the log line, the `Referer` and the history entry are all inert.

Frameworks that wrap the upgrade — Socket.IO, SignalR, Phoenix Channels — hide it well
enough that the handshake stops looking like a request, which is why the Origin check
and the handshake auth are the two things most often missing from generated code.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/limits-and-handshake.md` — starting values for message size, rate,
  connection caps and heartbeats; backpressure; the ticket exchange end to end; and
  per-framework notes for Socket.IO, SignalR and Phoenix Channels
- `rules/websocket_hardening.json`
- [OWASP WebSocket Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Cheat_Sheet.html).
- [CWE-1385](https://cwe.mitre.org/data/definitions/1385.html) · [CWE-770](https://cwe.mitre.org/data/definitions/770.html).
- [RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455).
