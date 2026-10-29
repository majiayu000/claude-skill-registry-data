---
name: web-traffic-js-reversing
description: "Work a web target from captured traffic to readable client-side JavaScript: intercept with mitmproxy, export HAR/OpenAPI, harvest endpoints and secrets with jsluice, deobfuscate bundles with webcrack, and drive a real browser through CDP. Use when an API has no documentation, when a bundle hides its routes, or when an agent must inspect live requests. Not for server-side source review (use a code-review skill)."
---

# Web traffic to JavaScript

The order matters: capture first, extract second, read third. Each step narrows the surface, and each has a tool that does it better than the others.

## Pipeline

```text
browser/app ──▶ mitmproxy ──▶ HAR ──▶ mitmproxy2swagger ──▶ OpenAPI
                    │
                    ├──▶ JS files ──▶ jsluice ──▶ endpoints + secrets
                    │                     │
                    │                     └──▶ webcrack ──▶ readable source
                    └──▶ live inspection ──▶ chrome-devtools MCP / mitmproxy-mcp
```

## 1. Capture

```sh
# interactive UI plus a HAR written on exit
mitmweb -p 8080 --set hardump=/root/.omp/captures/run.har --set confdir=~/.mitmproxy

# headless, for a scripted session
mitmdump -p 8080 --set hardump=/tmp/run.har

# phone/app traffic without installing a CA on the device
mitmdump --mode wireguard -p 51820

# forward everything to Burp and keep mitmproxy's view
mitmdump --mode upstream:http://127.0.0.1:8081 -p 8080
```

Client trust for HTTPS: browse `http://mitm.it` from the client and install the CA, or use `--mode wireguard`, which needs no certificate. On Android, apps that pin certificates will still fail; that is a separate problem from traffic capture.

Filtering while live:

```sh
mitmdump -p 8080 -w cap.mitm '~u api\.target\.com && ~m POST'
mitmdump -p 8080 --set save_stream_file=js.bin '~t application/javascript'
```

## 2. Capture to API description

`mitmproxy2swagger` is two-pass by design:

```sh
mitmproxy2swagger -i run.har -o api.yml -p https://api.target.com --examples
$EDITOR api.yml          # remove the `ignore:` prefix from paths you want
mitmproxy2swagger -i run.har -o api.yml -p https://api.target.com --examples
```

The first pass writes `x-path-templates` with every observed path ignored. Editing away `ignore:` is how you tell it which endpoints are real API surface. Run the second pass to expand them into OpenAPI operations with example bodies.

Note: passing a `.mitm` flow file can mis-detect as HAR in 0.15.0; export HAR with `--set hardump=` and feed that.

## 3. Harvest from JavaScript

```sh
# collect JS URLs seen in the capture
jq -r '.log.entries[] | select(.response.content.mimeType | test("javascript")) | .request.url' run.har > js.txt

# endpoints, with method and query parameters
jsluice urls app.js | jq -r '.url' | sort -u

# secrets, typed by kind
jsluice secrets app.js | jq -r '"\(.kind)\t\(.data.key)\t\(.filename)"'

# one bundle at a time, straight out of the HAR
jq -r '.log.entries[] | select(.response.content.mimeType | test("javascript")) | .response.content.text' run.har \
  | jsluice urls /dev/stdin | jq -r '.url' | anew endpoints.txt
```

`jsluice` parses with tree-sitter and emits the AST context, so `fetch("/api/v1/users")` is reported with `method: GET` while a bare string literal is reported without one. That distinction is what makes triage fast.

## 4. Make the bundle readable

```sh
webcrack bundle.js -o out/              # unpack + unminify + deobfuscate (all on by default)
webcrack --no-unpack bundle.js -o out/  # keep one file, still deobfuscate
webcrack --no-deobfuscate bundle.js -o out/   # only unpack and unminify
webcrack -f -m bundle.js -o out/        # overwrite output, mangle names
```

The flags are negative (`--no-unpack`, `--no-deobfuscate`, `--no-unminify`, `--no-jsx`); there is no positive `--unpack` or `--deobfuscate` switch.

Webpack and browserify bundles become a module tree; obfuscator.io output becomes named functions with string arrays resolved. `out/deobfuscated.js` is the readable entry point.

Then re-run extraction on the readable tree, where string concatenation is resolved:

```sh
jsluice urls out/ | jq -r '.url' | sort -u
rg -n 'api[_-]?key|secret|token\s*[:=]' out/ | head -50
```

## 5. Drive a real browser

Two MCP servers are configured in `~/.omp/agent/mcp.json`:

| Server | Use it for |
| --- | --- |
| `mitmproxy` | start/stop a proxy, summarise traffic, inspect a flow, replay it, fuzz an endpoint, export OpenAPI, generate scraper code |
| `chrome-devtools` | navigate, read the console, evaluate script, inspect a single network request, emulate a device |

`chrome-devtools` needs a Chrome binary; this host has Chrome for Testing at `/opt/chrome/chrome/linux-*/chrome-linux64/chrome` and the server is launched with `--headless --isolated --executablePath`. Attaching to an existing browser instead:

```sh
google-chrome --remote-debugging-port=9222      # on the machine with a display
# then start the server with --browserUrl http://127.0.0.1:9222
```

When a page needs the mitmproxy view and the CDP view at once, run the browser through the proxy (`--proxy-server=127.0.0.1:8080`) and query CDP for the runtime state.

## 6. Prove the finding

An endpoint found in JavaScript is a hypothesis. Confirm it with a request that the server answers differently from the baseline:

```sh
curl -s -o /dev/null -w '%{http_code} %{size_download}\n' https://api.target.com/api/v1/users
curl -s -o /dev/null -w '%{http_code} %{size_download}\n' https://api.target.com/api/v1/users/1
```

Record the request, the response status, the body length and the authentication context. A 200 that returns the same login page as everything else proves nothing.

## OPSEC and telemetry

- The proxy is local; the target sees ordinary requests. Its WAF, rate limits and bot detection do not care that a proxy produced them.
- `jsluice` and `webcrack` are offline: no requests, no fingerprints.
- A real browser leaks `navigator`, TLS fingerprint (JA3/JA4), and headless markers. `--isolated` gives a clean profile but does not hide automation.
- HAR files contain cookies and `Authorization` headers. Treat a capture as a credential store; keep it out of the repository and out of shell history.
- `mitmproxy2swagger` writes example bodies into the spec. Redact before sharing.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `SSL: CERTIFICATE_VERIFY_FAILED` from the client | mitmproxy CA not trusted | install from `http://mitm.it`, or `--mode wireguard` |
| Empty HAR | proxy stopped by `SIGKILL` before flush | stop with Ctrl-C / `SIGTERM`, or pass an explicit `--set hardump=` |
| `mitmproxy2swagger` `'int' object is not subscriptable` | fed a `.mitm` flow file | export HAR instead |
| `jsluice` returns nothing | input is not JavaScript, or is a wrapper with no URL literals | check `file`; try `jsluice tree` to confirm it parses, and `jsluice format` to beautify first |
| `webcrack` output still unreadable | control-flow flattening or VM obfuscation | fall back to `restringer`, or manual AST work with babel |
| DevTools server exits instantly | no Chrome at the configured path | update `--executablePath`, or use `--channel` |
| MCP server missing from `/mcp list` | omp drops browser-named servers when its native browser tool is enabled | keep the name `chrome-devtools` |

## Verification

```sh
mitmdump --version                       # 12.x
curl -s -x http://127.0.0.1:8080 -o /dev/null -w '%{http_code}\n' http://example.com/
jsluice urls sample.js | head -3                        # JSON lines
webcrack bundle.js -o /tmp/out && wc -l /tmp/out/*.js   # readable output
mitmproxy2swagger -h | head -3
```

## Related skills

- [mitmproxy](../mitmproxy/SKILL.md) for proxy modes and scripting
- [jsluice](../jsluice/SKILL.md) for AST extraction details
- [webcrack](../webcrack/SKILL.md) for deobfuscation options
- [chrome-devtools](../chrome-devtools/SKILL.md) for CDP tooling
- [httpx](../httpx/SKILL.md) and [ffuf](../ffuf/SKILL.md) to turn harvested endpoints into coverage