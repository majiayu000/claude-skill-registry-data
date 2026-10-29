---
name: whatweb
description: "Fingerprint web stacks with WhatWeb: CMS, frameworks, servers, JavaScript libraries and versions from response bodies, headers and favicons. Use during triage of a host list to pick which targets deserve a deeper scanner; Not for exploitation, content discovery (use ffuf) or authenticated business-logic testing."
---

# whatweb

WhatWeb sends one request per target at its default aggression and matches 1800+ Ruby plugins against the response. It is a triage layer, not a scanner: its job is to turn `10.0.0.0/24` into "these four run WordPress, that one is a GitLab, this one is an empty nginx" so you know where to spend requests. Version on this host is 0.5.5, plugins in `/usr/share/whatweb/plugins`.

## When to use

| Goal | Invocation |
| --- | --- |
| One-line summary per host | `whatweb --no-errors target` |
| Exact version of a known CMS | `whatweb -a 3 target` |
| Fingerprint a whole subnet | `whatweb --no-errors --url-prefix https:// 10.0.0.0/24` |
| Feed a scanner or a report | `whatweb -i hosts.txt --log-json out.json` |
| Only specific plugins | `whatweb -p title,wordpress,php target` |
| Discover plugins for a product | `whatweb --info-plugins=wordpress` |
| Grep results for a pattern | `whatweb --grep '/nginx[\/ ]?[0-9.]+/' target` |

Do not use it for directory brute force (`ffuf`), TLS/certificate inventory (`openssl s_client`, `testssl.sh`), or anything requiring authentication beyond a simple cookie or basic auth header.

## Prerequisites

- `whatweb --version` prints `WhatWeb version 0.5.5`.
- Ruby is required at runtime; the package ships its own plugin tree, so no gem install is needed.
- Targets must be reachable from this host, or through `--proxy`.
- For authenticated triage, a session cookie (`--cookie`) or basic credentials (`-u user:pass`) is enough; anything more complex needs a real browser.

## Core invocations

```sh
# 1. default aggression: one request, redirects followed, compact one-liner
whatweb --no-errors 10.0.0.5

# 2. aggressive: if a level-1 plugin matches, ask follow-up questions (version, readme, login page)
whatweb -a 3 10.0.0.5

# 3. heavy: tries every URL every plugin knows about; slow and very loud
whatweb -a 4 10.0.0.5

# 4. whole subnet over https, errors suppressed, 25 threads
whatweb --no-errors --url-prefix https:// 10.0.0.0/24

# 5. from a file, one target per line, JSON for later diffing
whatweb -i hosts.txt --no-errors --log-json /tmp/fingerprint.json

# 6. rate-limited sweep for a sensitive range: 5 threads, 1s between connections
whatweb -t 5 --wait 1 --no-errors -i hosts.txt

# 7. present as a normal browser instead of WhatWeb/0.5.5
whatweb --user-agent 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36' 10.0.0.5

# 8. limit to cheap, deterministic plugins
whatweb -p title,ip,country,httpserver,x-powered-by --no-errors 10.0.0.5

# 9. authenticated triage with a session cookie
whatweb --cookie 'PHPSESSID=deadbeef; wordpress_logged_in_x=deadbeef' 10.0.0.5

# 10. do not follow redirects, so the 301 target stays visible
whatweb --follow-redirect=never 10.0.0.5

# 11. what does a plugin detect, and how?
whatweb --info-plugins=wordpress | head -20
whatweb --search-plugins=jira

# 12. filter output without post-processing
whatweb --grep 'WordPress' -i hosts.txt

# 13. verbose plugin descriptions for a single host
whatweb -v 10.0.0.5

# 14. keep both a readable and a machine log in the same run
whatweb -a 3 --log-brief /tmp/brief.txt --log-json /tmp/full.json 10.0.0.5
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-a 1` | one request per target, follows redirects | default; fastest, least detail |
| `-a 3` | extra requests once a level-1 plugin matches | the useful default for a single host |
| `-a 4` | every URL from every plugin | dozens of requests per target; use on one host, not a /24 |
| `-t <n>` | threads, default 25 | 5-10 for fragile or monitored targets |
| `--wait <s>` | pause between connections | only meaningful with low thread counts |
| `-i <file>` | target list, `/dev/stdin` works | one URL/host per line |
| `--url-prefix` | prepend to each target | fastest way to force https on a CIDR |
| `--url-suffix` / `--url-pattern` | append or template a path | `--url-suffix /robots.txt` |
| `-p <list>` | plugin selection, `+`/`-` modifiers | `-p +plugins-disabled` re-enables disabled ones |
| `-g <string\|/regex/>` | show only matching results | quoting matters in sh |
| `-U` / `--user-agent` | override the UA | default `WhatWeb/0.5.5` is a scanner signature |
| `-H` | add or replace a header | `-H 'X-Forwarded-For: 127.0.0.1'` |
| `-c` / `--cookie` | cookie header | combine with `--cookie-jar` for real sessions |
| `-u user:pass` | HTTP basic auth | not form login |
| `--proxy host:port` | egress through a proxy | plus `--proxy-user` |
| `--open-timeout` / `--read-timeout` | 15s / 30s defaults | lower them on a broken range |
| `--log-json` / `--log-xml` / `--log-brief` | structured output | `-` writes to stdout and interleaves with the brief line |
| `-q` / `--no-errors` | less noise | `--no-errors` is the one you want on a /24 |
| `--max-redirects` | default 10 | lower to spot chains |
| `-l`, `-I`, `--search-plugins` | list and inspect plugins | offline, no traffic |

## Workflow

1. **Sweep cheap.** `-a 1 --no-errors --url-prefix https://` over the range, JSON to a file. Expect the first pass to be mostly `HTTPServer` and `IP`.
2. **Read the one-liners.** `Title`, `MetaGenerator`, `HTTPServer` and `RedirectLocation` usually separate the interesting hosts from the empty ones.
3. **Escalate per host.** `-a 3` on the handful that matched a CMS or framework; that is where versions appear.
4. **Confirm with a second plugin set.** `-a 4` or a targeted `-p wordpress,...` beats trusting one heuristic match.
5. **Diff two runs.** JSON in, `jq` across time, to see what changed after an application update.
6. **Hand off.** Feed the CMS/version pairs into `nuclei -tags`, and the live hosts into `ffuf`.

## OPSEC and telemetry

- Default `User-Agent` is `WhatWeb/0.5.5`: any WAF or log review sees the scanner name. Override it or accept being blocked.
- `-a 3` and `-a 4` multiply requests per target; `-a 4` on a /24 is thousands of requests and is a reliable way to get banned mid-engagement.
- Redirects are followed by default, so a scan can silently drift to a CDN or an external login portal; `--follow-redirect=never` keeps the target list honest.
- WhatWeb evaluates only server responses; it does not run JavaScript, so SPA-only stacks look empty.
- The JSON log records full URLs and any cookies you supplied. Treat it as sensitive output.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Every line is `IP[...]` and nothing else | site behind a WAF, or https-only with a bad cert | `--url-prefix https://`, `-a 3`, and consider `--user-agent` |
| `[ERROR] ... SSL_connect` on a whole range | expired or self-signed certificates | `--no-errors`, or accept the noise and read the rest |
| A single host hangs the run | no `--open-timeout`/`--read-timeout` tuning | `--open-timeout 5 --read-timeout 10` |
| Versions never appear | aggression 1 only reads one response | `-a 3` (or `-a 4` on that host) |
| Output and JSON are mangled together | `--log-json -` writes to stdout beside the brief line | log to a real file |
| Nothing matches with `-p` | plugin name wrong or plugin disabled | `-l | grep -i <name>`, then `-p +<name>` |
| Ruby exception / stack trace | a plugin crashed on odd input | `--no-errors` to continue, `--debug` to see it |
| Results change every run | random chain through a proxy, or load-balanced targets | pin `-t 1` and compare full responses |
| CIDR scan hits only port 80 | `--url-prefix` was not set and http was assumed | set `--url-prefix https://` explicitly |

## Verification

```sh
whatweb --version                 # WhatWeb version 0.5.5 ( https://www.morningstarsecurity.com/research/whatweb/ )
whatweb -l | wc -l                # 1835 lines including the header
whatweb --no-errors 127.0.0.1
# http://127.0.0.1 [308 Permanent Redirect] Country[RESERVED][ZZ], HTTPServer[Caddy], IP[127.0.0.1], RedirectLocation[https://127.0.0.1/]

whatweb -a 3 --user-agent 'Mozilla/5.0 (X11; Linux x86_64)' --log-json /tmp/ww.json 127.0.0.1
cat /tmp/ww.json
# [{"target":"http://127.0.0.1","http_status":308,
#   "request_config":{"headers":{"User-Agent":"Mozilla/5.0 (X11; Linux x86_64)"}},
#   "plugins":{"Country":{"string":["RESERVED"],"module":["ZZ"]},
#              "HTTPServer":{"string":["Caddy"]},"IP":{"string":["127.0.0.1"]},
#              "RedirectLocation":{"string":["https://127.0.0.1/"]}}}]
```

A JSON line per target, with `plugins` keyed by plugin name, is the success shape. Empty `plugins` means the response matched nothing, not that the host is down.

## Related skills

- [httpx](../httpx/SKILL.md) for status/title/tech bulk probing before whatweb
- [ffuf](../ffuf/SKILL.md) for content discovery once the stack is known
- [nuclei](../nuclei/SKILL.md) to turn a version into a template set
- [wordlists](../wordlists/SKILL.md) for the lists behind those follow-ups
- [toolchain-router](../toolchain-router/SKILL.md) to pick a different fingerprinting tool