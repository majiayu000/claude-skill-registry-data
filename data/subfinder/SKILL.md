---
name: subfinder
description: "Passive subdomain enumeration across dozens of public sources with provider keys, match/filter rules and JSONL output. Use when scoping a domain, expanding a host list, or feeding httpx and dnsx. Not for active DNS brute force (use dnsx) or HTTP probing (use httpx)."
---

# Subfinder

Subfinder collects subdomains from passive sources: certificate transparency logs, search engines, DNS datasets, threat-intel APIs and archive crawls. It sends no traffic to the target itself, so it is the safe first step of external reconnaissance. The quality of the result is directly proportional to how many provider API keys you have configured.

## When to use

| Goal | Command shape |
| --- | --- |
| Initial host list for one domain | `subfinder -d target.test -silent` |
| Many domains from a scope file | `subfinder -dL domains.txt -silent -oD out/` |
| Exhaustive pass with every source | `subfinder -d target.test -all -silent` |
| Only sources that return sub-subdomains | `subfinder -d target.test -recursive -silent` |
| Keep environment hosts, drop marketing | `subfinder -d target.test -match-regex '^dev\.'` |
| Machine-readable output | `subfinder -d target.test -oJ -silent` |
| Only hosts that currently resolve | `subfinder -d target.test -nW -silent` |
| Feed a probe pipeline | `subfinder ... -silent \| anew subs.txt \| httpx -silent` |

Use it before any active tool. Do not use it to brute force names (that is `dnsx` with `/opt/wordlists/subs-20k.txt`) or to decide whether a host is alive over HTTP (that is `httpx`).

## Prerequisites

- Binary at `/opt/tools/subfinder`; `subfinder -version` prints `[INF] Current Version: v2.17.0` on this host.
- Config directory `/root/.config/subfinder` is created on first run. Effective config: `config.yaml`; provider keys: `provider-config.yaml`.
- `subfinder -ls` lists 54 sources. `*` means the source requires a key, `~` means a key improves results but is optional.
- No wordlist is needed. Enumeration is passive.

The provider file is a YAML map of source name to a list of credentials. On a fresh host every entry is an empty list:

```yaml
# shape only -- never commit real keys
github:
  - ghp_EXAMPLE
shodan:
  - FAKEKEY0000000000000000000000000000
```

Some providers expect two values joined by `:` inside one list entry; check the provider's own console before filling it. Keep the file at mode `600`.

Why keys matter: keyless sources (`crtsh`, `commoncrawl`, `waybackarchive`, `rapiddns`, `anubis`, `thc`, `sitedossier`) return a baseline, but `*` sources silently return nothing without a token. Keys also raise per-source quotas; `-rls` shows the built-in defaults such as `github=30/m` and `virustotal=4/m`. An invalid key usually produces a source error in verbose mode, not a hard failure.

## Core invocations

```sh
# 1. baseline, passive, banner-free
subfinder -d target.test -silent

# 2. exhaustive: every source, slow and quota-hungry
subfinder -d target.test -all -silent -o all.txt

# 3. bulk scope file, one output directory per domain
subfinder -dL domains.txt -silent -oD out/

# 4. restrict to sources that can return deeper names (not a brute force)
subfinder -d target.test -recursive -silent

# 5. pin the source set when a provider is down or out of quota
subfinder -d target.test -s crtsh,commoncrawl,waybackarchive,rapiddns -silent

# 6. exclude noisy or slow providers
subfinder -d target.test -es alienvault,zoomeyeapi,robtex -silent

# 7. keep only likely-interesting names
subfinder -d target.test -match-regex '^(dev|stg|uat|admin|api)\.' -silent

# 8. drop CDN and parked-name noise
subfinder -d target.test -filter-regex 'cdn|akamai|cloudfront' -silent

# 9. JSONL, then inspect the actual keys before writing jq filters
subfinder -d target.test -oJ -silent | tee subs.jsonl
jq -r 'keys[]' subs.jsonl | sort -u

# 10. active-only: adds DNS resolution on top of the passive result
subfinder -d target.test -nW -silent

# 11. conservative pace for shared or rate-limited keys
subfinder -d target.test -rl 20 -t 5 -timeout 20 -max-time 5 -silent

# 12. dedupe across runs and feed the prober in one pipe
subfinder -d target.test -silent | anew subs.txt | httpx -silent -sc -title

# 13. per-domain files for a large scope
subfinder -dL domains.txt -oD out/ -silent

# 14. alternate provider file for a second key set
subfinder -d target.test -pc ./provider-config.yaml -silent

# 15. verify which sources exist on this build
subfinder -ls | sed -n '1,25p'
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-d` | domain(s) to enumerate | repeatable, also `string[]` |
| `-dL` | file of domains | pair with `-oD` |
| `-all` | use every source | slow; burns quotas |
| `-recursive` | restrict to recursive-capable sources | does not recurse itself |
| `-s` / `-es` | include / exclude sources | comma separated |
| `-m` / `-f` | string match / filter | not regex; files accepted |
| `-match-regex` / `-filter-regex` | regex include / exclude | use these for patterns |
| `-nW` | only active (resolving) names | performs DNS lookups |
| `-oJ` | JSONL output | one object per host |
| `-o` / `-oD` | single file / directory | `-oD` is for `-dL` |
| `-silent` | hosts only | suppress banner and logs |
| `-rl` / `-t` | global requests/sec / concurrency | lower on shared keys |
| `-timeout` / `-max-time` | per-request seconds / total minutes | defaults 30 and 10 |
| `-pc` | provider config path | default `~/.config/subfinder/provider-config.yaml` |
| `-r` / `-rL` | custom DNS resolvers | needed for `-nW` behind split DNS |
| `-ip` / `-exclude-ip` | include / strip IPs | `-ip` requires active mode |
| `-duc` | disable update check | avoids an update-check request per run |
| `-stats` | per-source statistics | use when a source looks empty |

## Workflow

1. **Confirm scope and authorization.** Enumerate only domains you may test; passive results can include unrelated third parties.
2. **Run the keyless baseline** with `-s crtsh,commoncrawl,waybackarchive,rapiddns` for a fast first picture.
3. **Add keys, then run `-all`.** Compare counts; a large jump means keyed sources are contributing.
4. **Normalize.** Lowercase, strip `*.` wildcards and trailing dots, then `sort -u`. Keep the raw file untouched.
5. **Resolve.** `dnsx -l subs.txt -silent` or `subfinder -nW` separates live names from stale records.
6. **Hand off.** Feed live names to [httpx](../httpx/SKILL.md), then probe paths and JS. Re-run subfinder later; certificate transparency grows continuously.

## OPSEC and telemetry

- Queries go to passive providers, not the target, so the target's DNS logs stay clean. Providers still log your source IP, API key and the domain queried.
- `-nW`, `-ip` and custom resolvers perform DNS lookups. Those are visible to authoritative DNS and to the resolver operator.
- `-all` can exhaust provider quotas and get keys temporarily banned. Prefer a pinned `-s` list during a time-boxed engagement.
- Without `-duc`, subfinder performs an update check over the network. Disable it on engagements that forbid unexpected egress.
- Results may include expired, parked, wildcard or transferable names. Verify ownership before scanning; an out-of-scope hostname is still out of scope.
- Store raw output with a timestamp. Passive data changes daily and is your evidence of what was known when.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Zero or near-zero results | all keyed sources skipped, keys invalid | run `-v`, add `-s crtsh`, check `provider-config.yaml` |
| `429` or source errors in verbose output | provider quota | lower `-rl`, wait, or exclude that source |
| Only a few names with `-recursive` | flag restricts the source set | drop it or add `-all` |
| `-oD` writes nothing | used without `-dL` or directory not writable | use `-o` for one domain, fix permissions |
| Output full of `*.target.test` | wildcard records from passive data | strip in post-processing; do not scan wildcards blindly |
| Names resolve to a CDN | wildcard DNS or hosted service | check CNAME with `dnsx -cname` before probing |
| `no such host` / resolver timeouts | broken local resolver or filtered egress | pass `-r 1.1.1.1` or `-rL resolvers.txt` |
| Same host listed twice | multiple sources | dedupe with `anew` or `sort -u` |
| Config ignored | `-pc` path typo or unreadable file | print the path and test with `ls -l` |

## Verification

```sh
subfinder -version
# [INF] Current Version: v2.17.0

subfinder -ls | head -5
# banner, then "Current list of available sources"

subfinder -d example.com -s crtsh -silent | head
# one hostname per line, no log lines
```

Check that `-silent` output is clean enough for a pipe:

```sh
subfinder -d example.com -s crtsh -silent | grep -c '^[a-z0-9._-]*example\.com$'
```

Keep the exact command, timestamp, source list and raw output as evidence. If a count looks wrong, re-run with `-v` and `-stats` before concluding the source is dead.

## Related skills

- [httpx](../httpx/SKILL.md) to turn names into live HTTP services
- [jsluice](../jsluice/SKILL.md) once probing reveals JavaScript
- [redteam-toolchain](../redteam-toolchain/SKILL.md) for binary paths and host layout
- [toolchain-router](../toolchain-router/SKILL.md) when another discovery tool fits better
