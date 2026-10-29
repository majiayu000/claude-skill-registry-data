---
name: nuclei
description: "Run nuclei v3.11 template scans for CVEs, exposures, default logins, panels, takeovers and misconfigurations, with rate caps and JSONL evidence. Use when you have live HTTP or network services and want known-issue coverage without hand-writing every check. Not for content discovery (use ffuf or feroxbuster) or manual injection exploitation (use sqlmap)."
---

# Nuclei

Nuclei is a template runner. Each YAML template describes requests, matchers and sometimes extractors for one known condition: a CVE, an exposed panel, a default credential, a misconfigured header. It does not think; it sends what the template says and reports what the matchers match. Your job is to choose the right templates, cap the request rate, and verify every finding by hand.

This host has engine v3.11.1 and templates v10.5.1 in `/root/nuclei-templates`, covering thousands of checks across `http/`, `dns/`, `ssl/`, `network/`, `javascript/`, `headless/`, `dast/`, `file/` and `workflows/`.

## When to use

| Goal | Flags | Note |
| --- | --- | --- |
| Full default sweep of one URL | `-u https://target.tld` | thousands of templates, slow |
| Full sweep of a list | `-l urls.txt` | one URL per line |
| Only serious findings | `-s medium,high,critical` | severity filter |
| Specific classes of check | `-tags cve,exposure,panel` | tag list from `-tgl` |
| A directory or one template | `-t http/cves/ -t ssl` | accepts paths and IDs |
| Skip noisy classes | `-etags dos,fuzz -es info` | exclusions apply after includes |
| Technology fingerprint first | `-t http/technologies/tech-detect.yaml` | cheap, informs later tags |
| Authenticated scan | `-H 'Cookie: ...'` | header applies to every request |
| Network protocol checks | `-pt tcp,dns,ssl` | protocol type filter |
| Fuzzing templates | `-dast` | loud; never on production |
| Reproducible evidence | `-jsonl -o out.jsonl` | one JSON object per line |

Nuclei findings are leads, not proof. A matcher can be weak; the default ignore list exists because some templates produced false positives. Confirm exploitable conditions with a manual request or [sqlmap](../sqlmap/SKILL.md).

## Prerequisites

- `/opt/tools/nuclei -version` prints `Nuclei Engine Version: v3.11.1`. Templates live at `/root/nuclei-templates` and report `v10.5.1`.
- `/opt/tools` is added to PATH by `/etc/profile.d/10-redteam.sh`. In a shell without it, call the binary by absolute path.
- The default ignore file `/root/.config/nuclei/.nuclei-ignore` excludes tags `dos`, `local`, `fuzz`, `bruteforce`, `txt-service` and a short list of weak templates. Override with `-itags` or `-include-templates`, never by editing that file.
- Template layout: `http/` holds the web checks (`cves/`, `exposures/`, `misconfiguration/`, `technologies/`, `default-logins/`, `exposed-panels/`, `takeovers/`, `vulnerabilities/`, `fuzzing/`), alongside `dns/`, `ssl/`, `network/`, `javascript/`, `headless/`, `dast/`, `file/`, `workflows/` and `profiles/`. Address them by relative path with `-t`.
- Interactive zsh sources `/opt/segfault/shellrc.sh`, which wraps `nuclei` in an opsec function. See the OPSEC section before trusting a rate you did not type.
- Targets must be live and URL-shaped. Nuclei probes non-URL input with httpx; a bare hostname may not resolve to the port you meant.

## Core invocations

```sh
# 1. default sweep of one host, conservative severity and explicit caps
nuclei -u https://target.tld -s low,medium,high,critical -rl 50 -c 10 -bs 10

# 2. scan a list produced by httpx, nmap or feroxbuster
nuclei -l live-urls.txt -s medium,high,critical -etags dos,fuzz -jsonl -o out/nuclei.jsonl

# 3. targeted tags instead of the full library
nuclei -u https://target.tld -tags cve,exposure,panel,default-login -rl 50

# 4. template directory, then one exact template
nuclei -u https://target.tld -t http/cves/ -t ssl
nuclei -u https://target.tld -t http/cves/2021/CVE-2021-44228.yaml

# 5. technology inventory before anything intrusive
nuclei -u https://target.tld -t http/technologies/tech-detect.yaml -silent

# 6. exclude by tag and severity
nuclei -l urls.txt -etags dos,fuzz,bruteforce -es info -rl 50 -c 10

# 7. silent JSONL for pipelines, stats for a long run
nuclei -l urls.txt -silent -jsonl -o out/run.jsonl -stats -si 15

# 8. authenticated scan with a header and a template variable
nuclei -u https://target.tld -H 'Cookie: session=abc123' -V 'api_key=fake-key' -t http/miscellaneous/

# 9. network, DNS and TLS protocol checks only
nuclei -l hosts.txt -pt tcp,dns,ssl -s medium,high,critical

# 10. validate a custom template before running it
nuclei -validate -t my-check.yaml

# 11. refresh templates (needs egress; changes your evidence baseline)
nuclei -update-templates

# 12. list what is installed and which tags exist
nuclei -tl -t http/cves/ | wc -l
nuclei -tgl | head -20

# 13. headless templates, with the browser cap the host wrapper sets
nuclei -u https://target.tld -headless -headc 2 -hbs 2 -t http/headless/

# 14. DAST fuzzing, only with explicit authorization
nuclei -u https://target.tld -dast -fa low -rl 10 -c 2

# 15. stop a host after the first match per template
nuclei -l urls.txt -spm -rl 50 -c 5
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-u` / `-l` | one target / target file | `-l` is the normal path at scale |
| `-t` | template file or directory, repeatable | accepts multiple `-t` |
| `-tags` / `-etags` | include / exclude template tags | `-tgl` lists available tags |
| `-s` / `-es` | include / exclude severity | `info,low,medium,high,critical,unknown` |
| `-id` / `-eid` | include / exclude by template ID | IDs are stable, tags are broad |
| `-rl` / `-rld` | requests per second / per duration | default 150 |
| `-c` | concurrent templates | default 25 |
| `-bs` | hosts analyzed in parallel per template | default 25 |
| `-headc` / `-hbs` | headless template / host concurrency | default 10 each |
| `-silent` | findings only | banners and progress removed |
| `-jsonl` / `-j` | JSONL output | `-json` does not exist in v3 |
| `-o` | output file | pair with `-jsonl` |
| `-stats` / `-si` | live statistics / interval | writes to stderr, not the target |
| `-update-templates` / `-ut` | refresh the template tree | do not do this mid-engagement |
| `-validate` | syntax-check templates | run before trusting a custom check |
| `-pt` / `-ept` | include / exclude protocol types | `http,dns,tcp,ssl,headless,file,code` |
| `-ni` | disable interactsh (OAST) | removes out-of-band templates from the run |
| `-H` / `-V` | global header / template variable | auth and configuration |
| `-headless` | enable headless templates | needs Chrome; root disables sandbox |
| `-dast` | run fuzzing templates | loud, not for production |
| `-spm` | stop at first match | fewer requests, may break workflows |
| `-mhe` / `-nmhe` | max host errors / disable skipping | default 30 |
| `-timeout` / `-retries` | per-request timeout / retries | default 10s and 1 |
| `-debug` | print requests and responses | leaks cookies and tokens into logs |
| `-itags` / `-include-templates` | override the ignore list | use instead of editing `.nuclei-ignore` |

## Workflow

1. **Build a live URL list.** `httpx -l hosts.txt -o live-urls.txt` or extract HTTP ports from the [nmap](../nmap/SKILL.md) output. Do not point `-l` at unresolved hostnames.
2. **Fingerprint first.** Run `tech-detect.yaml`, note the stack, then choose tags that match it instead of scanning everything.
3. **Set the envelope before the targets.** `-rl 50 -c 10 -bs 10` for shared infrastructure; type the caps so the shell wrapper does not choose them for you.
4. **Filter severity on the first pass.** `-s medium,high,critical` keeps the output reviewable. Add `info` only when inventory is the goal.
5. **Run targeted classes next.** CVEs for the detected version, exposures, panels, default logins, takeovers.
6. **Save JSONL and deduplicate.** Group by `template-id` and `host`; one template firing on fifty hosts is one finding class.
7. **Confirm each finding.** Re-run the single template with `-debug` against one host, then reproduce manually with `curl`. Never report a matcher hit without a response body.
8. **Refresh templates between engagements, not during one.** Record `nuclei -version` and the templates version with the evidence.

## OPSEC and telemetry

- **Host-injected caps.** Interactive zsh defines a `nuclei` function from `/opt/segfault/shellrc.sh` that appends `-rl 15 -c 4 -bs 4 -hbs 2 -headc 2` to any invocation that does not already contain `-rl`, `-rate-limit`, `-c`, `-bs`, `-hbs` or `-headc`. It prints `[opsec] nuclei ...` to stderr when it fires. Help, version and update flags bypass it. `command nuclei ...` bypasses it entirely. Non-interactive shells get no wrapper.
- **Engine defaults without the wrapper.** `-rl 150`, `-c 25`, `-bs 25`. That is fast enough to saturate a small target and to look like scanning.
- Every template sends real requests. The default User-Agent identifies nuclei; `-H 'User-Agent: ...'` changes it but not the request pattern.
- `-tags cve` can still mean thousands of requests per host. Estimate before running a 5,000-URL list.
- OAST templates call public interactsh servers (`oast.pro`, `oast.live`, `oast.site`, `oast.online`, `oast.fun`, `oast.me`). Target-derived data leaves your network. Use `-ni` or a self-hosted `-iserver`.
- The ignore list already blocks `dos`, `fuzz`, `bruteforce` and weak matchers. Forcing them back in raises both noise and risk.
- `-debug` and `-store-resp` write authentication headers and tokens to disk. Treat those files as secrets.
- `-headless` starts Chrome. As root on Linux the sandbox is disabled, and page loads are visible in the app's logs.
- `-dast` generates attack-shaped payloads; run it only under explicit authorization and at `-rl 10` or lower.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `flag provided but not defined: -json` | v3 renamed the flag | use `-jsonl` or `-j` |
| Zero templates execute | path wrong, or everything filtered by the ignore list | `-tl -t <path>`, then `-itags`/`-include-templates` |
| `no templates provided` | `-t` points at a missing directory | check `/root/nuclei-templates/<path>` |
| Host skipped mid-scan | more than 30 errors (`-mhe`) | raise `-mhe`, use `-nmhe`, or fix reachability |
| All requests time out | target slow, or rate too high | `-timeout 20 -retries 2 -rl 25` |
| Templates validate but nothing matches | target is behind auth or a WAF | add `-H`/cookies, check a manual `curl` |
| No OAST findings | egress DNS/HTTP blocked | test egress, or self-host with `-iserver` |
| Headless templates fail | Chrome missing or sandbox issue as root | install Chrome for Testing, run as non-root |
| Scan never finishes | full library across many hosts | `-tags`, `-s`, `-spm`, `-rl`, fewer `-c` |
| Custom template silently skipped | strict syntax or unsigned/ignore list | `-validate`, `-nss`, `-code` for code templates |

## Verification

```sh
nuclei -version                            # Nuclei Engine Version: v3.11.1
nuclei -validate -t /root/nuclei-templates/http/technologies/tech-detect.yaml
                                           # [INF] All templates validated successfully
nuclei -tl -t http/cves/ | head            # template paths print
nuclei -tgl | head -20                     # tag names print
```

Record for every run: engine version, templates version, target list, exact flags (including whether the wrapper injected caps), and the JSONL output.

## Related skills

- [ffuf](../ffuf/SKILL.md) and [feroxbuster](../feroxbuster/SKILL.md) to build the URL list this tool consumes
- [sqlmap](../sqlmap/SKILL.md) to confirm and exploit an injection lead
- [nmap](../nmap/SKILL.md) for the underlying port and service map
- [netexec](../netexec/SKILL.md) for authenticated SMB, LDAP and WinRM follow-up
- [toolchain-router](../toolchain-router/SKILL.md) to pick a different tool