---
name: mitmproxy
description: "Intercept, inspect, replay and export HTTP(S) traffic with mitmproxy, mitmweb, mitmdump, its proxy modes and mitmproxy2swagger. Use when capturing browser or app traffic, chaining to Burp, or building OpenAPI from observed requests. Not for passive DNS work (use subfinder) or raw packet capture."
---

# mitmproxy

mitmproxy is one engine with three frontends: `mitmproxy` (terminal UI), `mitmweb` (browser UI) and `mitmdump` (headless). All share the same options, modes, flow filters and Python addon API. It terminates TLS with its own CA, so it sees plaintext for every client that trusts that CA.

## When to use

| Goal | Frontend or mode |
| --- | --- |
| Explore a browser session interactively | `mitmweb -p 8080` |
| Record a HAR without a UI | `mitmdump --set hardump=run.har` |
| Triage flows in a terminal | `mitmproxy -p 8080` |
| Stream only matching traffic to disk | `mitmdump -w cap.mitm '~u api'` |
| Put Burp in front of mitmproxy | `--mode upstream:http://127.0.0.1:8081` |
| Capture a phone without installing a CA | `--mode wireguard` |
| Intercept traffic from a gateway | `--mode transparent` |
| Produce OpenAPI from a capture | `mitmproxy2swagger` two-pass |

## Prerequisites

- `mitmdump --version` reports `Mitmproxy: 12.3.1`, `Python: 3.12.3`. Binaries are in `/root/.local/bin` (pipx).
- Config directory defaults to `~/.mitmproxy` and holds the CA: `mitmproxy-ca-cert.pem`, `mitmproxy-ca-cert.cer`, `mitmproxy-ca-cert.p12`, `mitmproxy-ca.pem`, `mitmproxy-ca.p12`.
- Clients must trust the CA: browse `http://mitm.it` from the client and install it. Android apps targeting API 24+ ignore user CAs unless they opt in. `block_global` defaults to `true`, so only local clients may proxy.
- Default regular port is `8080`; the web UI defaults to `8081`.
- `mitmproxy2swagger` is a separate pipx console script with no `--version` flag.

## Core invocations

### Modes

| Mode | Wire form | Use |
| --- | --- | --- |
| `regular` | default | explicit HTTP proxy |
| `transparent` | `--mode transparent` | traffic redirected by the OS or gateway |
| `socks5` | `--mode socks5` | SOCKS clients |
| `reverse:SPEC` | `--mode reverse:https://host:443` | front one upstream service |
| `upstream:SPEC` | `--mode upstream:http://127.0.0.1:8081` | chain through Burp or another proxy |
| `wireguard` | `--mode wireguard` | device traffic with no CA install |

`--mode` is repeatable and accepts a `@listen_port` suffix per mode.

```sh
# 1. interactive web UI plus a HAR written on clean shutdown
mitmweb -p 8080 --set hardump=/tmp/run.har

# 2. headless capture
mitmdump -p 8080 --set hardump=/tmp/run.har

# 3. stream flows as they arrive, only API URLs
mitmdump -p 8080 -w /tmp/cap.mitm '~u /api/'

# 4. filter what reaches the HAR too
mitmdump -p 8080 --set hardump=/tmp/js.har --set save_stream_filter='~t application/javascript'

# 5. read a capture offline, no proxy server
mitmdump -nr /tmp/cap.mitm

# 6. chain to Burp while keeping mitmproxy's view
mitmdump --mode upstream:http://127.0.0.1:8081 -p 8080

# 7. phone or app traffic over WireGuard
mitmdump --mode wireguard -p 51820

# 8. transparent interception behind redirect rules
mitmdump --mode transparent -p 8080

# 9. expose one internal service locally
mitmdump --mode reverse:https://internal.target.test:8443 -p 8443

# 10. load an addon and isolate the engagement CA
mitmdump -p 8080 -s /tmp/addon.py --set confdir=/tmp/mitm-engagement
```

A minimal addon. `request` and `response` are the hooks; `flow.request` and `flow.response` are mutable.

```python
from mitmproxy import http
def request(flow: http.HTTPFlow) -> None:
    flow.request.headers["X-Scope"] = "authorized-test"
def response(flow: http.HTTPFlow) -> None:
    if flow.response:
        flow.response.headers["X-Seen"] = "1"
```

### Flow filters

Filters are positional arguments and apply to display and the save stream.

| Filter | Selects |
| --- | --- |
| `~u regex` | URL |
| `~d regex` | domain |
| `~t application/javascript` | content type |
| `~hs Set-Cookie` | response header |
| `~bs secret` | response body |

```sh
mitmdump -p 8080 -w api.mitm '~u /api/ & ~hs Set-Cookie'
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-p, --listen-port` | proxy port | default 8080 |
| `-m, --mode` | proxy mode | repeatable |
| `--set option=value` | set any core option | `hardump`, `confdir`, `block_global` |
| `--set hardump=PATH` | write HAR on exit | needs graceful shutdown |
| `-w, --save-stream-file` | stream flows to a file | mitmproxy format, not HAR |
| `-r, --rfile` | read flows from a file | pair with `-n` offline |
| `-n, --no-server` | do not start a proxy | offline analysis |
| `-s, --scripts` | load an addon | repeatable |
| `--set save_stream_filter` | filter what is written | same syntax as filters |
| `--ignore-hosts` | pass through without interception | regex on host or IP |
| `-k, --ssl-insecure` | skip upstream TLS validation | hides real certificate problems |
| `--proxyauth` | require proxy authentication | `user:pass`, `any`, htpasswd |
| `--modify-headers` / `--modify-body` | rewrite in flight | pattern based |

## mitmproxy2swagger

Two passes, by design: the first records every path as `ignore:`, you curate the templates, the second expands the rest into operations.

```sh
mitmproxy2swagger -i /tmp/run.har -o api.yml -p https://api.target.test
# edit api.yml: remove the "ignore:" prefix from templates you want
mitmproxy2swagger -i /tmp/run.har -o api.yml -p https://api.target.test
```

Pass 1 output:

```yaml
paths: {}
x-path-templates:
- ignore:/v1/users/{id}
- ignore:/v1/users/42
```

After removing `ignore:` from the templated line and re-running, pass 2 filled:

```yaml
paths:
  /v1/users/{id}:
    get:
      summary: GET users by id
```

Lines closer to the top take precedence and matching is greedy. `-e/--examples` and `-hd/--headers` include values that may be sensitive. `-f/--format {flow,har}` overrides detection, `-r/--param-regex` turns matching segments into placeholders, and `-s/--suppress-params` keeps only placeholder paths.

## Workflow

1. **Pick the least invasive mode.** Regular proxy with a dedicated `confdir` for a browser; WireGuard for an app; transparent only when redirect rules already exist.
2. **Establish trust once.** Install the CA from `mitm.it`, verify one HTTPS request, then capture.
3. **Filter early.** Pass a filter to `-w`; use `save_stream_filter` for HAR so files stay small.
4. **Stop cleanly.** `hardump` is written on graceful shutdown; a kill can leave it empty. Prefer streaming `-w` for long sessions.
5. **Triage offline** with `mitmdump -nr`, then export, curate and export again; the second swagger pass is what produces usable operations.

## OPSEC and telemetry

- The CA private key in `confdir` is a skeleton key for every client that trusts it. Use a per-engagement `confdir` and remove the CA from clients afterwards.
- HAR and flow files contain plaintext credentials, cookies and personal data. Encrypt at rest and delete on schedule.
- `--ssl-insecure` disables upstream validation and hides interception or pinning problems.
- `block_global=true` is a safety boundary. Disable it only on an isolated test network.
- WireGuard exposes a UDP listener; transparent mode's redirect rules affect the whole host, so scope them to the target CIDR.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Blocked connection to external host` | `block_global` is true | `--set block_global=false` on a trusted network |
| Browser certificate error | CA not installed or wrong store | install from `mitm.it`, restart the browser |
| App ignores the CA | pinning or user-store restriction | WireGuard plus instrumentation; re-signing is separate |
| `Address already in use` | port taken | change `-p` or stop the other proxy |
| `502 Bad Gateway` | upstream proxy or reverse target down | start Burp or check the reverse SPEC |
| HAR is empty | killed before shutdown | use `-w` streaming, stop with Ctrl-C |
| HTTP/2 or gRPC breaks | protocol unsupported on the path | `--set http2=false`, retest |
| swagger ignores every path | `ignore:` prefixes untouched | edit `x-path-templates`, rerun |
| swagger misreads a `.mitm` file | auto-detection guessed HAR | add `-f flow`, or export HAR |

## Verification

```sh
mitmdump --version
# Mitmproxy: 12.3.1 / Python: 3.12.3

mitmdump --options | grep -E '^(hardump|confdir|block_global)'
# hardump: ''
# confdir: ~/.mitmproxy
# block_global: true
```

## Related skills

- [web-traffic-js-reversing](../web-traffic-js-reversing/SKILL.md) for the full capture-to-OpenAPI pipeline
- [jsluice](../jsluice/SKILL.md) to mine captured JavaScript
- [webcrack](../webcrack/SKILL.md) to unpack the bundles you capture
- [httpx](../httpx/SKILL.md) to probe hosts through the proxy
