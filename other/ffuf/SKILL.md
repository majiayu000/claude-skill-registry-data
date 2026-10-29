---
name: ffuf
description: "Fuzz paths, virtual hosts, parameter names and values with ffuf 2.1, and separate real hits from wildcard noise. Use when you have a URL and a wordlist and need content, vhost or parameter discovery with precise control over requests. Not for crawl-first recursive discovery (use feroxbuster) or template-based CVE checks (use nuclei)."
---

# ffuf

ffuf places one or more wordlist values into marked request positions and shows you the responses that differ from the baseline. It is a request engine, not a crawler: you decide the URL, the keyword position, the method, the headers and the filters. That control is why it wins on vhosts, parameters, login bodies and odd APIs, and why it loses to feroxbuster on deep directory trees.

The binary is `/opt/tools/ffuf`, version 2.1.0-dev. There is no user config file on this host, so every behavior below comes from flags you pass.

## When to use

| Goal | Position | Key flags |
| --- | --- | --- |
| Find files and directories | `-u https://t/FUZZ` | `-w`, `-mc`, `-fs`, `-e` |
| Find virtual hosts | `-H "Host: FUZZ.t"` | `-fs` or `-ac` in vhost mode |
| Find parameter names | `-u https://t/api?FUZZ=1` | `-fs`, `-fw` |
| Fuzz a value | `-u https://t/item?id=FUZZ` | `-w` numeric list, `-mc all` |
| Fuzz a JSON body | `-X POST -d '{"user":"FUZZ"}'` | `-H "Content-Type: application/json"` |
| Replay a captured request | `-request req.txt` | `-request-proto https` |
| Credential body brute force | two wordlists | `-mode pitchfork` |
| Recursive path discovery | `-u https://t/FUZZ/` | `-recursion`, `-recursion-depth` |

For open-ended crawling, response-driven recursion, link extraction and automatic wildcard suppression, use [feroxbuster](../feroxbuster/SKILL.md). For known CVEs and exposure templates, use [nuclei](../nuclei/SKILL.md).

## Prerequisites

- `/opt/tools/ffuf -V` prints `ffuf version: 2.1.0-dev`. On a shell without `/etc/profile.d/10-redteam.sh`, call the absolute path.
- Wordlists: `/opt/wordlists/web-common.txt` (4,751 lines), `dir-medium.txt` (220,559), `subs-20k.txt` (20,000), `users-top.txt`, `pass-top1m.txt`, `rockyou.txt`.
- Know the baseline response before fuzzing: status, size, word count and title. Filters are meaningless without it.
- Match the keyword exactly. `FUZZ` is the default, other keywords are declared as `-w list.txt:KEYWORD`, and both are case-sensitive.
- Scope: a 220k-line wordlist at 40 threads is 220k requests. Cap `-rate` before the first run on a shared host.

## Core invocations

```sh
# 1. directory discovery with an explicit matcher set
ffuf -w /opt/wordlists/web-common.txt -u https://target.tld/FUZZ \
  -mc 200,204,301,302,307,401,403 -o out/dirs.json -of json

# 2. let ffuf calibrate wildcard responses automatically
ffuf -w /opt/wordlists/web-common.txt -u https://target.tld/FUZZ -ac -t 25 -rate 50

# 3. add extensions to every word (php, bak and txt variants)
ffuf -w /opt/wordlists/web-common.txt -u https://target.tld/FUZZ -e .php,.bak,.txt -ac

# 4. virtual host discovery: keep the URL fixed, fuzz the Host header
ffuf -w /opt/wordlists/subs-20k.txt -u https://target.tld/ -H "Host: FUZZ.target.tld" \
  -fs 1234 -rate 100

# 5. parameter-name fuzzing on a known endpoint
ffuf -w /opt/wordlists/web-common.txt -u 'https://target.tld/api/item?FUZZ=1' -fs 482 -mc all

# 6. POST body fuzzing, URL-encoded
ffuf -w /opt/wordlists/pass-top1m.txt -X POST -d 'username=admin&password=FUZZ' \
  -H 'Content-Type: application/x-www-form-urlencoded' -u https://target.tld/login -fc 401 -rate 20

# 7. replay a raw request saved from Burp or a proxy
ffuf -request req.txt -request-proto https -w /opt/wordlists/web-common.txt -ac

# 8. two wordlists in lockstep for a login form
ffuf -w /opt/wordlists/users-top.txt:USER -w /opt/wordlists/pass-1050.txt:PASS \
  -mode pitchfork -u https://target.tld/login -d 'u=USER&p=PASS' -X POST -fc 401

# 9. recursive discovery, URL must end in the keyword
ffuf -w /opt/wordlists/web-common.txt -u https://target.tld/FUZZ -recursion -recursion-depth 2 -ac

# 10. authenticated run with a bearer token and redirects enabled
ffuf -w /opt/wordlists/web-common.txt -u https://target.tld/FUZZ -H 'Authorization: Bearer eyJ...' -r

# 11. throttle and delay for a sensitive target
ffuf -w /opt/wordlists/dir-medium.txt -u https://target.tld/FUZZ -rate 30 -t 10 -p 0.2 -ac

# 12. send everything through a local proxy for inspection
ffuf -w /opt/wordlists/web-common.txt -u https://target.tld/FUZZ -x http://127.0.0.1:8080

# 13. stop on mass 403 and cap total runtime
ffuf -w /opt/wordlists/dir-medium.txt -u https://target.tld/FUZZ -sf -maxtime 600 -noninteractive

# 14. write every format at once and skip the file when nothing matched
ffuf -w /opt/wordlists/web-common.txt -u https://target.tld/FUZZ -ac \
  -o out/all -of all -or -od out/responses
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-w <file>[:KEYWORD]` | wordlist and optional keyword | repeat for multiple wordlists |
| `-u <url>` | target with FUZZ somewhere in it | required unless `-request` is used |
| `-mc` / `-fc` | match / filter status codes | default matches 200-299,301,302,307,401,403,405,500 |
| `-ms` / `-fs` | match / filter response size | sizes accept comma lists and ranges |
| `-mw` / `-fw` | match / filter word count | good for template pages |
| `-ml` / `-fl` | match / filter line count | good for JSON and CSV responses |
| `-mr` / `-fr` | match / filter regex | apply to the body |
| `-ac` / `-acc` / `-ach` | auto-calibrate / custom calibration string / per host | `-ac` is the normal choice |
| `-rate` | requests per second | `0` means unlimited; set 30-100 on shared hosts |
| `-t` | concurrent threads (default 40) | 2 vCPU: keep at or below 40 |
| `-p` | delay per request or random range | `0.1` or `0.1-2.0` |
| `-H` | extra header, repeatable | vhost, auth, content type |
| `-X` / `-d` | HTTP method / POST body | PUT and PATCH work |
| `-b` | cookie header | `-b 'session=abc'` |
| `-e` | extensions appended to each word | `.php,.bak`; comma list |
| `-request` / `-request-proto` | raw HTTP request file / scheme | fastest path from Burp |
| `-mode` | `clusterbomb`, `pitchfork`, `sniper` | pitchfork for user/pass pairing |
| `-recursion` / `-recursion-depth` | recurse on matches | URL must end in FUZZ |
| `-x` | HTTP or SOCKS5 proxy | `http://127.0.0.1:8080` |
| `-r` | follow redirects | without it 301s are shown, not followed |
| `-o` / `-of` / `-od` | output file / format / matched bodies | `-of all` writes every format |
| `-or` | do not create an empty output file | useful in pipelines |
| `-sf` | stop when >95% of responses are 403 | WAF or blanket deny |
| `-maxtime` | total runtime cap in seconds | pair with `-noninteractive` |
| `-ignore-body` | skip reading bodies | faster when only status matters |
| `-D` | DirSearch wordlist compatibility | use with `-e` |

## Workflow

1. **Baseline with curl.** Request a random path twice: `curl -s -o /dev/null -w '%{http_code} %{size_download}\n' https://target.tld/zzz-not-real`. Note status, size and body hash.
2. **Choose the position.** Path, Host header, query name, query value or body. Put the keyword where the variable belongs, not where it is convenient.
3. **Choose the wordlist.** `web-common.txt` for a first pass, `dir-medium.txt` only after the baseline is stable, `subs-20k.txt` for vhosts.
4. **Start small and calibrated.** `-ac -t 20 -rate 50`, no extensions. Read the first 20 results, not the summary count.
5. **Add filters from evidence.** Identical 200s mean a wildcard: use `-fs <size>`, or let `-ac` do it. Variable soft-404 bodies need `-fw` or `-fr`.
6. **Expand only on signal.** Add extensions, recursion or a second wordlist after a clean first pass.
7. **Confirm by hand.** Every result you plan to report gets a `curl -i` and a look at the body. A 200 from a catch-all route is not a finding.

### False positives and calibration

- `-ac` sends random strings before the scan, detects wildcard behavior, and adds the matching filters. It is the default answer to "everything returns 200".
- `-ach` calibrates per host in vhost mode; a single global baseline is wrong when one vhost behaves differently.
- SPA catch-alls return the same body for every path. Filter by size, then check whether the body is the shell HTML.
- WAF block pages often return 403 with a fixed body. `-fc 403` hides the noise but does not bypass the WAF; lower `-rate` and change the User-Agent instead.
- A single unusual status is not proof. Compare the body, title, headers and response time.
- `-mc all` plus explicit filters beats a narrow matcher when you do not yet know the normal status.

## OPSEC and telemetry

- One request per wordlist line, plus calibration requests. `web-common.txt` is 4,751 requests; `dir-medium.txt` is 220,559.
- Default concurrency is 40 threads with no rate limit. On this 2 vCPU host and any shared target, set `-rate 30` to `-rate 100` and `-t 20`.
- The default User-Agent advertises ffuf. Set `-H 'User-Agent: Mozilla/5.0 ...'` when blending in matters.
- Every request lands in the web server's access log, including 404s. WAF and CDN logs keep the full path list.
- Recursion multiplies traffic by the number of discovered directories; a depth-2 run can be tens of thousands of requests.
- Aggressive fuzzing can trigger account lockout on login forms. Cap `-rate`, use a known-valid user, and stop after a few attempts.
- `-x` to Burp keeps a local record but does not reduce target-side telemetry.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Every result is 200 with the same size | wildcard route or SPA | `-ac`, or `-fs <baseline size>` |
| Zero results on a known-live path | wrong scheme, Host, or keyword case | `curl` the URL, confirm `FUZZ` spelling and `-u` |
| Results all 403 | WAF, geo-block, or missing auth | add `-b`/`-H`, lower `-rate`, `-sf` to stop early |
| 429 or 503 bursts | rate too high for the target | `-rate 10`, `-p 0.5`, fewer threads |
| Recursion never descends | `-u` does not end in FUZZ | use `-u https://t/FUZZ/` |
| TLS handshake failure on a self-signed host | no skip-verify flag in 2.1.0-dev | use http, or proxy via a client that ignores certs |
| Output file missing | no matches and `-or` was set | drop `-or` or check filters |
| Run stops immediately | 95% 403 with `-sf` | remove `-sf`, verify the baseline first |
| Slow scan on a large list | no rate floor, high latency | `-t 40`, `-ignore-body` when only status matters |

## Verification

```sh
ffuf -V                                  # ffuf version: 2.1.0-dev
ffuf -h 2>&1 | grep -c '^  -'            # option count, help parser alive
ffuf -w /opt/wordlists/web-common.txt -u http://127.0.0.1:1/FUZZ \
  -t 2 -rate 5 -maxtime 3 -noninteractive -s
```

The last command should exit without a traceback and print a short summary; connection refused against a closed local port is the expected result. Keep `-o` JSON per run, with the command line and timestamp beside it.

## Related skills

- [feroxbuster](../feroxbuster/SKILL.md) when you want recursion, link extraction and automatic wildcard handling in one pass
- [nuclei](../nuclei/SKILL.md) to turn discovered URLs into template checks
- [sqlmap](../sqlmap/SKILL.md) once a parameter fuzz result looks injectable
- [nmap](../nmap/SKILL.md) for the port scan that precedes web fuzzing
- [toolchain-router](../toolchain-router/SKILL.md) to pick a different tool