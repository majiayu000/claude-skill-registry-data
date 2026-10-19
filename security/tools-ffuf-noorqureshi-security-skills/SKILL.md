---
name: tools-ffuf
description: >
  Fuzz web targets with ffuf for content, parameter, and vhost discovery — FUZZ keyword placement in
  paths, query strings, POST bodies and Host headers, matcher/filter calibration (-mc/-fs/-ac),
  recursion, and when to switch to feroxbuster/gobuster/dirsearch. Load when a web target needs hidden
  paths, files, parameters, or virtual hosts enumerated. Signals: ffuf -w FUZZ, directory brute force,
  gobuster dir, feroxbuster, dirsearch, raft-medium-directories, burp-parameter-names, 404 filtering.
domain: tools
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: info
mitre: [T1595.003]
tools: [ffuf, gobuster, feroxbuster, dirsearch, wfuzz]
schema_version: 1
---

# ffuf & web content fuzzing

## When it applies
You have an in-scope web target (`tradecraft-scope-roe`) and need what the site map doesn't show:
hidden directories and files, undocumented GET/POST parameters, or name-based virtual hosts. This is
the active half of `recon-content-discovery` — wordlist-driven, noisy, and governed by `roe.md` rate
limits.

## Why it works
ffuf replaces the `FUZZ` keyword anywhere in a request — path, query, body, header — with each
wordlist entry, then classifies responses by status/size/word-count. Discovery is a filtering
problem: a wildcard or SPA route answers 200 to *everything*, so the skill is teaching ffuf what
"nothing found" looks like, then listing only the deviations.

## Method
1. **Directory/file brute force** with an extension set matched to the stack:
   ```bash
   ffuf -u http://target.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
   ffuf -u http://target.com/FUZZ -w wordlist.txt -e .php,.html,.txt
   ffuf -u http://target.com/FUZZ -w wordlist.txt -recursion -recursion-depth 2
   ```
2. **Calibrate the noise floor** — run once, note the junk response's status/size/words, then filter:
   `-mc 200,301,302` (match codes), `-fs 1234` (hide size), `-fc 403`, or just `-ac` to auto-calibrate
   against random canary words. Without this step every wildcarded app "finds" thousands of pages.
3. **Parameter discovery:**
   ```bash
   ffuf -u "http://target.com/api?FUZZ=test" -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -fs 0
   ffuf -u http://target.com -X POST -d "user=FUZZ&pass=test" -w wordlist.txt
   ```
4. **Virtual hosts** — whole apps hide behind one IP, answering only to the right `Host:` name:
   ```bash
   ffuf -u http://target.com -H "Host: FUZZ.target.com" -w subdomains.txt -fs 0
   ```
   The default vhost answers everything with the same 200 — filter by the *different* size/words.
5. **Carry auth when testing behind login** — replicate the session:
   `-H "Cookie: session=abc"` / `-H "Authorization: Bearer token"`.
6. **Switch tools when the fit is better:**
   ```bash
   feroxbuster -u https://target.com -w raft-medium-directories.txt -d 3 -C 403,404 -x php,asp,html --rate-limit 50
   feroxbuster -u https://target.com --auto-tune --smart        # self-tuning filters/rate
   gobuster dir -u http://target.com -w common.txt -x php,txt -b 404,403
   gobuster dns -d target.com -w subdomains.txt                 # DNS-mode subdomain brute
   dirsearch -u https://target.com -e php,asp,aspx,jsp -r -R 3 --exclude-status=403,404
   wfuzz -c -z file,big.txt --hc 404 https://target.com/FUZZ    # FUZZ/FUZ2Z multi-payload
   ```
   feroxbuster = recursion by default; gobuster = simple and steady (+ DNS mode); dirsearch = sane
   defaults; wfuzz = multi-wordlist combos (`-z file,a -z file,b`).
7. **Feed results back** — discovered paths go to the Burp/`web-*` testing loop; discovered params
   go to arjun for confirmation and then to the relevant injection skills.

## Gotchas
- **Unfiltered output is fiction** — a "1000 hits" run against a wildcard app is 1000 copies of the
  same 200. Calibrate first (`-ac` or manual `-fs/-fc/-fw`), then trust the short list.
- **SPA catch-alls** — any-path-200 with identical body size means a frontend router, not real
  endpoints; filter by size and move on.
- **Rate limits and WAFs** — default ffuf speed trips Cloudflare/ModSecurity and breaches many
  bug-bounty RoEs; use `-rate`/`-p` (delay) and check `roe.md` before launching.
- **Recursion explodes** — depth 3 on a big wordlist × every found dir can run for hours; cap with
  `-recursion-depth` and scope recursion to interesting dirs.
- **Windows/curl quirk** — when verifying hits with curl, `[]` in URLs (e.g. `__proto__[test]`)
  needs `--globoff` or curl misparses them as ranges.
- **Match the wordlist to the stack** — raft/directory-list for general, CMS-specific lists after
  fingerprinting (`recon-techstack-fingerprinting`), `burp-parameter-names` for params,
  `subdomains-top1million-5000` for vhosts.

## Verify success
Every reported path/param/vhost is manually re-requested (curl/Burp) and returns content that
differs from the calibrated baseline — a page of unverified scanner hits is a lead list, not a
result.

## References
ffuf GitHub; SecLists wordlists; feroxbuster/gobuster/dirsearch/wfuzz docs. Discovery methodology:
`recon-content-discovery`; full web toolbelt: `web-arsenal`; pipeline: `automation-recon-pipeline`.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
