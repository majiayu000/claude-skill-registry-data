---
name: ctf-web
description: >
  CTF web challenge playbook — the recurring shapes jeopardy web challenges take: source disclosure
  (.git, backups, flask debug), SSTI/SSRF in their CTF forms, PHP quirks (type juggling, wrappers,
  filters), cookie/JWT games, and chained primitives to read /flag. Load on any CTF challenge whose
  handout is a URL. Signals: "web" category, flask/werkzeug or PHP banner, /flag or flag.txt on the
  box, robots.txt, provided app.py/index.php source, JWT or flask session cookie.
domain: ctf
type: methodology
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A03:2021-Injection, A01:2021-Broken-Access-Control]
cwe: [CWE-94, CWE-918, CWE-697]
tools: [curl, burp, flask-unsign, jwt-tool, ffuf]
schema_version: 1
---

# CTF web challenges

## When it applies
The handout is a URL (sometimes plus source). The goal is almost always to read a flag file
(`/flag`, `/flag.txt`, an env var, or a DB row) — so every bug you find should be steered toward
*read a file*, *run a command*, or *become admin*. This skill is the CTF routing layer; work the
deep techniques with `web-ssti`, `web-ssrf`, `web-sqli`, `web-lfi-path-traversal`, `web-auth-jwt`,
`web-deserialization`, `web-command-injection`, `web-file-upload`.

## Why it works
CTF web challenges strip an app to one intended bug plus decorations, so the surface is small and
the bug is findable by *enumeration*, not luck. Provided source turns black-box guessing into
reading comprehension; the framework banner (Flask/PHP/Express) predicts the bug class before you
send a request.

## Method
1. **Enumerate the obvious first (5 minutes).** `curl -sS -D-` the root; read every HTML comment,
   JS file, cookie, and header. Hit `robots.txt`, `/sitemap.xml`, common admin paths, and run a
   quick `ffuf -w raft-small-words -u <url>/FUZZ`. Check the HTTP methods (`OPTIONS`, try
   `PUT`/`POST` where GET works). CTF apps hide routes in comments and robots more than real ones.
2. **Grab source if it exists — it usually does.**
   - Provided zip / `Dockerfile`: read it; the bug is visible, and the Dockerfile tells you the
     flag's location and any sandbox (read-only fs, seccomp).
   - `.git` exposed: `git-dumper <url>/.git out/` then read history (`recon-github-code-leaks`).
   - Backups: `index.php~`, `index.php.bak`, `.index.php.swp`, `app.py.bak` — ffuf for them.
   - PHP filters as source oracle: `?page=php://filter/convert.base64-encode/resource=index`
     (`web-lfi-path-traversal`).
   - Flask/Werkzeug debugger page exposed → the PIN is crackable from machine-id + boot-id +
     username (leak them via an LFI) or is printed in console output you can reach.
3. **Work the framework's favorite bug:**
   - **Flask/Jinja2** → SSTI: `{{7*7}}` then climb to `{{ self.__init__.__globals__ }}` /
     `config` / `cycler.__init__.__globals__.os.popen('cat /flag').read()`. Filter bypasses:
     `|attr()`, request-args gadgets, hex/octal string building (`web-ssti`,
     `web-python-sandbox-escape`).
   - **PHP** → the quirks are the challenge: loose comparison type juggling (`==` with `"0e..."`
     magic hashes, `0 == "password"`, array params to skip `strcmp`/`md5` checks — `?a[]=1`),
     wrapper chains (`php://filter`, `data://`, `phar://`), `preg_replace /e`, unserialize
     with a provided class → POP chain (`web-deserialization`).
   - **Node/Express** → prototype pollution (`web-prototype-pollution`), SSTI in EJS/Pug,
     `eval` on JSON fields, NoSQL injection (`{"$gt":""}` on login forms).
4. **Play the cookie games.** Flask session cookie → `flask-unsign --decode`, brute the secret
   (`flask-unsign --unsign --wordlist rockyou.txt`) then re-sign `{'is_admin': True}`. JWT →
   `alg:none`, RS256→HS256 confusion with a reachable public key, weak HMAC secret brute
   (`web-auth-jwt`). Homegrown base64/hex cookies → decode, flip the `role` field, handle the MAC
   with `crypto-oracle-attacks`.
5. **SSRF, the CTF shape.** Any URL fetcher (webhook tester, PDF renderer, image proxy) →
   `http://127.0.0.1/` for internal-only routes, `http://169.254.169.254/` only when the Docker
   setup hints cloud, `file:///flag`, and `gopher://` to hit internal Redis/MySQL
   (`web-ssrf`, `web-ssrf-gopher-redis-rce`). In CTF, the internal service on a weird port *is*
   the challenge — scan `127.0.0.1` ports through the SSRF.
6. **Chain to the flag.** One primitive rarely suffices: LFI → source → secret → signed cookie →
   admin panel → SSTI → RCE → `cat /flag`. Treat each confirmed bug as a key that unlocks the next
   stage (`exploit-chaining`).

## Gotchas
- **`{{7*7}}` rendering as `{{7*7}}` doesn't rule out SSTI** — some challenges only evaluate in
  error pages, emails, or PDF exports. Try the sink contexts, and try `${7*7}`, `#{7*7}`, `<%= 7*7 %>`
  for other engines.
- **PHP `assert`/`eval` challenges** filter obvious words; build strings dynamically
  (`$_GET['x']($_GET['y'])` with `x=system&y=cat /flag`) instead of fighting the blocklist.
- **Provided source != deployed source** occasionally — verify a behavior against the live app
  before building an exploit on the reading.
- **The flag may need root** — RCE as www-data with `/flag` readable only by root means a second
  stage: look for setuid binaries, cron, or a SUID flag-reader you must exploit (`privesc` domain).
- **Rate-limited login / captcha** in CTF usually hides race conditions (`web-race-conditions`) or
  SQLi in the login query, not a brute-force task.

## Verify success
The flag string in the correct format, read from the target (file, env, or DB) — not a local
reproduction. If you got RCE, `id; cat /flag` output is the proof.

## References
Deep techniques: `web-ssti`, `web-ssrf`, `web-auth-jwt`, `web-deserialization`,
`web-lfi-path-traversal`, `web-python-sandbox-escape`, `web-command-injection`, `web-sqli`;
source-leak hunting: `recon-content-discovery`, `recon-github-code-leaks`; token attacks:
`crypto-oracle-attacks`. Triage via `ctf-methodology`.
