---
name: feroxbuster
description: "Run feroxbuster 2.13 for recursive content discovery that filters wildcard responses, extracts links and records state you can resume. Use when a target is directory-heavy or you want one pass with extensions and recursion instead of hand-driving every branch. Not for vhost or parameter fuzzing (use ffuf) or template-based CVE checks (use nuclei)."
---

# feroxbuster

feroxbuster is a recursive content discovery scanner: it takes one URL, one wordlist, and keeps going into every directory it finds. It auto-filters wildcard responses, can extract links from HTML and JavaScript, and writes a state file you can resume. That makes it the right default for "map the web root" and the wrong tool for "test this exact parameter position".

Binary: `/opt/tools/feroxbuster`, version 2.13.1. Defaults matter here: 50 threads, no rate limit, recursion depth 4, and wildcard filtering on.

## When to use

| Goal | Flags | Note |
| --- | --- | --- |
| Map a site's directories | `-u`, `-w` | recursive by default, depth 4 |
| Search specific file types | `-x php,html,js` | extensions apply at every depth |
| Limit the blast radius | `-d 2` or `-n` | depth 0 means infinite |
| Reduce manual filtering | `--smart` | auto-tune, collect words, collect backups |
| Everything including dir listings | `--thorough` | smart plus extension and listing collection |
| Suppress known noise | `-C 404,403`, `-S <size>` | status and size deny lists |
| Slow down for a shared host | `--rate-limit 50 -t 20` | limit is per directory |
| Structured results | `--json -o out.json` | newline-delimited JSON, not an array |
| Feed another tool | `--silent` | prints URLs only |
| Resume an interrupted run | `--resume-from <state>` | state written unless `--no-state` |
| Several targets at once | `--stdin` | one URL per line |

Use [ffuf](../ffuf/SKILL.md) instead when the fuzz position is a header, a query parameter, a POST field, or when you need pitchfork pairing. Use [nuclei](../nuclei/SKILL.md) after discovery, not during it.

## Prerequisites

- `/opt/tools/feroxbuster --version` prints `feroxbuster 2.13.1`.
- Wordlists: `/opt/wordlists/dir-medium.txt` (220,559 lines) is the workhorse; `web-common.txt` (4,751) is the quick pass; `dir-big.txt` exists but is usually too slow for a first run.
- A wildcard baseline: request two random paths and compare status, size and body. feroxbuster filters common wildcards automatically; unusual soft-404s still need `--filter-similar-to`.
- Target authorization. Recursion plus `--smart` can produce six figures of requests from one command.
- The JSON output is JSONL: one object per line, suitable for `jq -c` but not for `jq '.'` without `-s`.

## Core invocations

```sh
# 1. first pass: recursive, depth 4, automatic wildcard filtering
feroxbuster -u https://target.tld -w /opt/wordlists/dir-medium.txt -o out/ferox.txt

# 2. restrict depth and add common extensions
feroxbuster -u https://target.tld -w /opt/wordlists/web-common.txt -d 2 -x php,html,js,txt

# 3. single directory, no recursion
feroxbuster -u https://target.tld/admin/ -w /opt/wordlists/web-common.txt -n

# 4. smart collection: auto-tune, words from responses, backup extensions
feroxbuster -u https://target.tld -w /opt/wordlists/web-common.txt --smart

# 5. thorough: smart plus extension discovery and directory listings
feroxbuster -u https://target.tld -w /opt/wordlists/web-common.txt --thorough -d 2

# 6. filter noise by status and size
feroxbuster -u https://target.tld -w /opt/wordlists/dir-medium.txt -C 404,403 -S 1234

# 7. filter a soft-404 page by similarity
feroxbuster -u https://target.tld -w /opt/wordlists/web-common.txt \
  --filter-similar-to https://target.tld/not-a-real-page

# 8. polite scan: per-directory rate cap and fewer threads
feroxbuster -u https://target.tld -w /opt/wordlists/dir-medium.txt --rate-limit 50 -t 20

# 9. structured output, quiet console, bounded runtime
feroxbuster -u https://target.tld -w /opt/wordlists/web-common.txt \
  --json -o out/ferox.json --time-limit 10m -q --no-state

# 10. URLs only, piped to the next tool
feroxbuster -u https://target.tld -w /opt/wordlists/web-common.txt --silent -C 404

# 11. authenticated scan
feroxbuster -u https://target.tld -w /opt/wordlists/web-common.txt \
  -H 'Authorization: Bearer eyJ...' -b 'session=abc123'

# 12. replay a captured request as the template
feroxbuster --request-file req.txt -w /opt/wordlists/web-common.txt -x php

# 13. several targets from stdin, one process
printf '%s\n' https://a.tld https://b.tld | feroxbuster --stdin -w /opt/wordlists/web-common.txt --silent

# 14. reduce speed automatically when errors pile up, or bail out
feroxbuster -u https://target.tld -w /opt/wordlists/dir-medium.txt --auto-tune
feroxbuster -u https://target.tld -w /opt/wordlists/dir-medium.txt --auto-bail

# 15. resume an interrupted run
feroxbuster --resume-from ferox-1606586780.state
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-u` / `--url` | target URL | required unless using `--stdin`, `--request-file` or `--resume-from` |
| `-w` / `--wordlist` | wordlist path or URL | one list per scan |
| `-d` / `--depth` | maximum recursion depth | default 4; 0 means infinite |
| `-n` / `--no-recursion` | scan only the given URL | useful for one directory |
| `-x` / `--extensions` | extensions to append | repeatable or comma list; `@file` reads a list |
| `--smart` | auto-tune + collect words + collect backups | more requests per discovered path |
| `--thorough` | smart + extension discovery + dir listings | loudest preset |
| `-C` / `--filter-status` | status codes to hide | deny list, not an allow list |
| `-s` / `--status-codes` | status codes to include | default is all codes |
| `-S` / `-W` / `-N` | filter by size / words / lines | repeatable and comma lists |
| `-X` / `--filter-regex` | filter by body or header regex | catches changing soft-404s |
| `--filter-similar-to` | filter pages similar to a URL | strongest soft-404 filter |
| `--rate-limit` | requests per second per directory | default 0, no limit |
| `-t` / `--threads` | concurrent threads | default 50 |
| `-L` / `--scan-limit` | concurrent directory scans | total load is roughly threads times this |
| `--auto-tune` | lower rate after excessive errors | reacts, does not prevent |
| `--auto-bail` | stop a directory after excessive errors | earlier stop than auto-tune |
| `--json` | JSONL logs to output and debug log | one record per line |
| `-o` / `--output` | result file | pair with `--json` |
| `--silent` | URLs only, logging off | pipe into nuclei or httpx |
| `-q` / `--quiet` | hide banner and progress bars | good for tmux |
| `--time-limit` | cap total runtime | `10m`, `1h` |
| `--no-state` | do not write state files | keeps the working tree clean |
| `-k` / `--insecure` | skip TLS verification | required for self-signed targets |
| `-r` / `--redirects` | follow redirects | off by default |
| `--dont-filter` / `-D` | disable wildcard auto-filtering | only when the filter is wrong |
| `--burp` / `--burp-replay` | send all / matched requests to Burp | replay uses `-R` codes |

## Workflow

1. **Baseline the wildcard.** `curl -s -o /dev/null -w '%{http_code} %{size_download}\n' https://target.tld/random-1` and repeat with a second random path. If both return 200 at the same size, plan on `--filter-similar-to`.
2. **Start with one list and no extensions.** `web-common.txt`, depth 2. Read the first matches before widening.
3. **Add extensions from evidence.** A PHP site gets `-x php`; a Java site gets `-x jsp,do,action`; backups are `--smart` territory.
4. **Set depth deliberately.** Depth 4 is the default and often too much on a CMS. Use `-d 2` for a first pass, `-n` for a single directory.
5. **Throttle before the target throttles you.** `--rate-limit 50 -t 20` is a sane default on shared infrastructure.
6. **Capture JSON and state.** Keep `--json -o out.json`; drop `--no-state` only when you may need to resume.
7. **Hand off confirmed paths.** Pipe `--silent` output into [nuclei](../nuclei/SKILL.md) or a manual `curl -i` review. Do not report a path you have not fetched.

### When feroxbuster beats ffuf

- Recursion is built in and follows discovered directories without re-invoking the tool.
- It extracts links from HTML and JavaScript, so it finds paths absent from the wordlist.
- Wildcard responses are filtered automatically, including per-directory wildcards.
- `--smart` collects words from responses and probes backup extensions without a second tool.
- State files allow exact resume; ffuf has no equivalent.
- JSONL output is uniform across recursive branches.

ffuf still wins on vhosts, parameter positions, raw request replay, pitchfork pairing, and fine-grained matcher logic.

## OPSEC and telemetry

- Defaults are 50 threads and no rate limit. One `dir-medium.txt` run can exceed 200,000 requests before recursion.
- The default User-Agent is `feroxbuster/2.13.1`. Use `-A` for a random agent or `-H` for a fixed one.
- Link extraction requests pages it did not discover from the wordlist, including static assets and API references; those show up in logs too.
- `--smart` adds backup probes (`~`, `.bak`, `.bak2`, `.old`, `.1`) for every hit, multiplying requests.
- `--auto-tune` reduces speed only after errors appear. It is a reaction, not a budget.
- `--burp-replay` sends matched requests through a local proxy; useful for evidence, invisible to the target as reduced traffic.
- Recursive scanning of a CMS can hit admin actions via GET links. Check `--dont-scan` for logout and delete endpoints.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Could not connect to <url>, skipping` then `Could not connect to any target` | wrong scheme, port closed, or DNS failure | `curl` the base URL, try `-k`, confirm the port |
| Every result is 200 with one size | wildcard response | automatic filtering usually handles it; if not, `--filter-similar-to` |
| Wildcard filter hides real hits | catch-all resembles real pages | `-D` to disable, then filter manually with `-S`/`-X` |
| Everything is 403 | WAF, geo-block, or missing auth | add `-b`/`-H`, lower `--rate-limit`, do not just filter |
| Scan is far too deep | default depth 4 on a large tree | `-d 2`, `-L 4` |
| Host is overloaded by the scanner | 50 threads across many scans | `-t 10`, `--rate-limit 20`, `-L 2` |
| TLS errors on an internal host | self-signed certificate | `-k` |
| Output file is not valid JSON as a whole | JSONL records, one per line | `jq -c . out.json` or `jq -s .` |
| State files litter the directory | default state writing | `--no-state` |
| `--stdin` exits immediately | no piped input | `printf '%s\n' <url> | feroxbuster --stdin ...` |

## Verification

```sh
feroxbuster --version                      # feroxbuster 2.13.1
feroxbuster --help | grep -c '^      --'   # option count, help parser alive
feroxbuster -u http://127.0.0.1:1 -w /opt/wordlists/web-common.txt \
  --time-limit 3s --rate-limit 10 -t 5 --no-state -q
```

The last command must fail cleanly with `Could not connect to http://127.0.0.1:1/` and no panic. Keep the JSONL, the command line and the start time for every real run.

## Related skills

- [ffuf](../ffuf/SKILL.md) for vhosts, parameter positions and precise matcher control
- [nuclei](../nuclei/SKILL.md) to scan the URLs this tool discovers
- [sqlmap](../sqlmap/SKILL.md) when a discovered endpoint carries parameters
- [nmap](../nmap/SKILL.md) for the port scan that precedes web discovery
- [toolchain-router](../toolchain-router/SKILL.md) to pick a different tool