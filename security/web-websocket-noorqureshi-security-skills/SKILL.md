---
name: web-websocket
description: >
  Attack WebSocket endpoints — CSWSH (cross-site hijacking), message tampering, and auth gaps.
  Load on ws:// or wss:// connections, Socket.IO, real-time chat/notifications/trading, or
  "websocket". Signals: Upgrade: websocket, ws handshake, JSON messages over a socket, token in the handshake.
domain: web
type: technique
stability: learning
modes: [bugbounty, pentest]
severity: high
owasp: [A01:2021-Broken-Access-Control]
cwe: [CWE-1385, CWE-346]
tools: [burp]
schema_version: 1
---

# WebSocket attacks

## When it applies
The app uses WebSockets for realtime features. They're often less-tested than HTTP and skip the
authz/validation the REST API has — plus the handshake can be CSRF-able.

## Why it works
The WS handshake is an HTTP request that carries cookies; if the server authenticates by cookie
alone and doesn't check `Origin`, any site can open a socket as the victim (Cross-Site WebSocket
Hijacking). And per-message authorization is frequently missing — the server trusts the connection.

## Method
1. **Intercept & replay**: use Burp's WebSocket history to read/modify messages; tamper fields
   (ids, roles, amounts) and resend — test per-message authz (IDOR/BOLA over the socket).
2. **CSWSH**: check if the handshake validates `Origin`. If not and auth is cookie-based, host a
   page that opens `new WebSocket('wss://target/…')` as the victim, then exfiltrate the messages
   the server sends back → data theft / actions.
3. **Injection**: message fields feed backends — test XSS (messages rendered to other users),
   SQLi/NoSQLi in socket payloads.
4. **Auth gaps**: connect without/with a low-priv token; access channels/rooms you shouldn't.

## Gotchas
- CSWSH impact = whatever the socket exposes (private messages, actions) — prove it reads/does something sensitive.
- Origin check present ≠ safe if it's a weak regex; test bypasses like `web-cors`.
- Stored-XSS via chat messages hits other connected users — high impact, easy to miss.

## Verify success
Cross-origin socket reading victim data (CSWSH), a tampered message performing an unauthorized
action, or an injection firing through a socket message.

## References
PortSwigger WebSocket labs; OWASP testing WebSockets (WSTG).
