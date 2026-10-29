---
name: httpx
description: "Probe HTTP services at scale: status, title, technology, web server, redirects, methods and JSONL output, with match/filter and rate controls. Use when turning a host list into live URLs or fingerprinting a web estate. Not for directory brute force (use ffuf) or passive DNS collection (use subfinder)."
---

# httpx

httpx is ProjectDiscovery's HTTP toolkit. It takes hosts or URLs, probes both schemes, and prints one line per live service with whatever attributes you ask for. It is the hinge between passive discovery and every active web tool: nothing else should see a hostname before httpx has confirmed what is listening.

This is the Go binary at `/opt/tools/httpx`, not the Python `httpx` library.

## When to use

| Goal | Command shape |
| --- | --- |
| Confirm which hosts serve HTTP | `httpx -l hosts.txt -silent` |
| Build a live URL inventory | `httpx -l hosts.txt -sc -title -td -o live.txt` |
| Find only successful responses | `httpx -l hosts.txt -mc 200,204,301,302` |
| Remove soft-404 noise | `httpx -l hosts.txt -fc 404,400,503` |
| Fingerprint server and framework | `httpx -l live.txt -web-server -tech-detect -title` |
| Probe extra paths on each host | `httpx -l live.txt -path /api,/health,/admin` |
| Test HTTP methods | `httpx -l live.txt -x all` |
| Machine-readable pipeline output | `httpx -l hosts.txt -json -o out.jsonl` |
| Screenshot a web estate | `httpx -l live.txt -ss` |
| Route through a proxy for evidence | `httpx -l live.txt -proxy http://127.0.0.1:8080` |

Do not use httpx for content discovery wordlists (use `ffuf` or `feroxbuster`), DNS resolution (use `dnsx`), or vulnerability templates (use `nuclei`).

## Prerequisites

- Binary at `/opt/tools/httpx`; `httpx -version` prints `[INF] Current Version: v1.12.0`.
- Config file defaults to `$HOME/.config/httpx/config.yaml`.
- Input is one host or URL per line on stdin, or a file via `-l`. Stdin is read by default; `-no-stdin` disables it.
- Wordlists at `/opt/wordlists` for path lists, for example `web-common.txt` or `dir-medium.txt`.
- Headless screenshots (`-ss`) need a Chrome install; `-system-chrome` selects a local one.

## Core invocations

```sh
# 1. basic liveness sweep, no banner
httpx -l hosts.txt -silent

# 2. single target, two attributes
httpx -u https://app.target.test -sc -title

# 3. the standard inventory line
httpx -l hosts.txt -sc -title -td -web-server -silent -o live.txt

# 4. only responses worth looking at
httpx -l hosts.txt -mc 200,204,301,302,401,403 -silent

# 5. drop dead and blocked noise
httpx -l hosts.txt -fc 404,400,503 -silent

# 6. conservative pacing for a production estate
httpx -l hosts.txt -threads 10 -rl 10 -timeout 10 -retries 1 -silent

# 7. JSONL for later queries, then inspect the real keys
httpx -l hosts.txt -json -o out.jsonl
jq -r 'keys[]' out.jsonl | sort -u

# 8. probe common paths on every live host
httpx -l live.txt -path /api,/health,/admin,/login -mc 200,301,302,401,403

# 9. path list from a file
httpx -l live.txt -path /opt/wordlists/web-common.txt -mc 200 -silent

# 10. method testing (state-changing methods included -- scope check first)
httpx -l live.txt -x all -sc -silent

# 11. follow redirects and record the destination
httpx -l hosts.txt -follow-redirects -location -sc -silent

# 12. subfinder to httpx in one pipe, deduped
subfinder -d target.test -silent | anew subs.txt | httpx -silent -sc -title -td

# 13. keep request and response for a finding
httpx -u https://app.target.test/api/user -irr -json -o finding.jsonl

# 14. screenshot every live host
httpx -l live.txt -ss -system-chrome -silent -o shots.txt

# 15. send traffic through mitmproxy for capture
httpx -l live.txt -proxy http://127.0.0.1:8080 -silent

# 16. enumerate the output fields this build supports
httpx -lof
```

Typical output with `-sc -title -td -web-server`:

```text
https://app.target.test [200] [Login] [React,nginx] [nginx]
https://api.target.test [401] [Unauthorized] [Express] [cloudflare]
```

Fields appear only when requested; exact spacing and order are build-specific. `-silent` removes the banner and progress noise, not the fields.

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-l, -list` / `-u, -target` | input file / target(s) | `-u` is repeatable |
| `-silent` | no banner or stats | still prints results |
| `-sc, -status-code` | status code | cheapest useful probe |
| `-title` | HTML title | forces body read |
| `-td, -tech-detect` | technology detection | wappalyzer dataset |
| `-server, -web-server` | Server header | often masked by CDNs |
| `-mc, -match-code` / `-fc, -filter-code` | match / filter status codes | filters apply after matchers |
| `-ms` / `-fs` | match / filter body string | useful for login pages |
| `-mr` / `-fe` | match / filter regex | escape carefully |
| `-t, -threads` | concurrent workers | default 50 |
| `-rl, -rate-limit` | requests per second | default 150 |
| `-j, -json` | JSONL output | one object per result |
| `-o, -output` | output file | works with any format |
| `-path` | extra paths to probe | comma separated or file |
| `-x` | HTTP methods | `all` probes everything |
| `-fr` | follow redirects | `-location` shows target |
| `-ss` | headless screenshot | needs Chrome |
| `-irr` | include request/response | JSON only; large output |
| `-proxy` | upstream proxy | http or socks |
| `-nf` | no fallback scheme | shows both HTTP and HTTPS results |
| `-ports` | custom ports | nmap syntax |
| `-lof` | list output fields | offline, no traffic |
| `-timeout` / `-retries` | per-request limits | defaults 10s / 0 |

## Workflow

1. **Start from a resolved list.** Pass subdomains or IPs; httpx handles scheme fallback itself.
2. **Baseline with `-sc -title -silent`.** Read the distribution of status codes before adding expensive probes.
3. **Tag with `-td -web-server`.** Group hosts by stack; that decides which follow-up tool is worth running.
4. **Filter deliberately.** Use `-mc` for the statuses you want, then `-fc` for known soft-404 or WAF pages. Keep the unfiltered file.
5. **Expand paths only on live hosts.** `-path` multiplies requests by path count; it is not a fuzzer and has no recursion.
6. **Persist JSONL.** Store the raw JSONL and derive text views with `jq`; re-probing later should not be necessary just to change columns.

## OPSEC and telemetry

- httpx sends real HTTP requests from your IP unless `-proxy` is set. Every request appears in target, CDN and WAF logs.
- `-random-agent` is enabled by default, so the User-Agent rotates. TLS fingerprints and header order still identify the client; `-tlsi chrome` is experimental impersonation, not anonymity.
- Defaults of 50 threads and 150 requests/second are loud. Use `-threads 10 -rl 10` on shared infrastructure.
- `-ss` loads pages in a real browser, including third-party resources, and can trigger client-side telemetry.
- `-x all` may send `PUT`, `DELETE` and `PATCH`. Never run it against endpoints that mutate state without explicit approval.
- `-irr` stores request and response bodies, including tokens and personal data. Treat the JSONL as sensitive.
- `-cdn` is on by default and labels CDN/WAF fronts; do not mistake an edge response for the origin.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `httpx: command not found` or wrong tool starts | Python `httpx` library shadows the Go binary | call `/opt/tools/httpx` or fix PATH order |
| No output at all | input not on stdin and no `-l`, or `-mc` too strict | pass `-l`, drop matchers, add `-debug` |
| Every host returns 403 | WAF or geo block | slow down, set `-H`, check `-cdn` |
| TLS handshake errors | SNI or certificate mismatch | `-sni`, `-tls-grab`, or probe by IP with a Host header |
| Duplicate URLs | both schemes or multiple ports | `-nf`, `sort -u`, or `-fd` for near-duplicates |
| Screenshots missing | no Chrome or sandbox restriction | `-system-chrome`, check the Chrome path |
| Output file empty but terminal shows hits | wrote with `-silent` and a filter that matched nothing | keep `-mc` and `-fc` consistent |
| JSON is huge | `-irr` with large bodies | add `-ob` to omit bodies, or drop `-irr` |
| Scan hangs | filtered ports and no timeout | `-timeout 5 -retries 1`, reduce `-threads` |

## Verification

```sh
httpx -version
# [INF] Current Version: v1.12.0

httpx -lof | head -5
# timestamp, linkrequest, asn, err, cspdata

printf 'http://127.0.0.1:9\n' | httpx -silent -sc
# no result, or a connection error -- never a traceback
```

For a real run, keep the input list, the command, the raw output and the JSONL. Confirm counts match:

```sh
wc -l hosts.txt live.txt out.jsonl
jq -r '.url' out.jsonl | sort -u | wc -l
```

## Related skills

- [subfinder](../subfinder/SKILL.md) for the host list that feeds httpx
- [jsluice](../jsluice/SKILL.md) to mine the JavaScript behind live hosts
- [mitmproxy](../mitmproxy/SKILL.md) when probes must be captured as evidence
- [toolchain-router](../toolchain-router/SKILL.md) to choose between httpx, ffuf and nuclei
