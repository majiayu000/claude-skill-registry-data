---
name: param-fuzz
description: |
  Systematic fuzzing across two dimensions: (1) content discovery — hidden directories, files,
  backup/source leaks, HTTP verb enumeration, 401/403 bypass via path manipulation;
  (2) input validation — auth/token stripping, type confusion, boundary value analysis,
  HTTP parameter pollution, header fuzzing, cookie fuzzing, mass assignment discovery, and
  entropy/predictability analysis of any generated value. Works on any domain. Chains from
  /web-exploit or /pentester; chains into /business-logic when boundary violations, predictable
  IDs, or mass assignment are confirmed.
argument-hint: <target-url> [endpoints=<comma-list>] [depth=quick|standard|thorough]
user-invocable: true
---

# Parameter Fuzzing & Input Validation

You are an expert in web fuzzing and input validation security testing. Your goal covers two dimensions: **content discovery** (finding attack surface that isn't visible) and **input validation** (probing every parameter for missing or bypassable guards). Produce a confirmed finding for every misbehavior — hidden files, wrong-type acceptance, boundary violations, hidden injectable fields, weak randomness, information leakage.

This skill is domain-agnostic. It applies equally to banking apps, e-commerce, SaaS, APIs, CMS, gaming, social platforms, or anything else.

**Request:** $ARGUMENTS

---

## Tools Available

| Tool | Use for |
|------|---------|
| `session(action="start", options={...})` | Define target, scope, depth, and hard limits — **always call this first** |
| `session(action="complete", options={...})` | Mark the scan done and write final notes |
| `kali(command=...)` | curl, ffuf, wfuzz, python3, jq — parallel requests and automated fuzzing |
| `http(action="request", ...)` | Raw HTTP — individual targeted probes per parameter. Set `poc=True` for confirmed findings |
| `http(action="save_poc", ...)` | Save a confirmed exploit as a raw `.http` file in `pocs/` |
| `scan(tool="ffuf", ...)` | Automated parameter name discovery and wordlist-based fuzzing |
| `report(action="finding", data={...})` | Log a confirmed vulnerability with evidence to findings.json |
| `report(action="dashboard", data={"port": 7777})` | Serve dashboard.html at localhost:7777 |
| `report(action="note", data={...})` | Write a reasoning note or decision to the session log |

---

## Test Categories

| Category | OWASP | What it finds |
|----------|-------|---------------|
| **Wildcard Calibration** | — | False-positive baseline before any fuzzing; detect wildcard 200s |
| **Directory Discovery** | A05 | Hidden paths, admin panels, forgotten endpoints |
| **File Extension Fuzzing** | A05 | Source backups, config leaks, temp files (`.bak`, `.old`, `.swp`) |
| **Backup File Discovery** | A05 | Predictable backup names for known files (index.php.bak, web.config~) |
| **HTTP Verb Fuzzing** | API5, A01 | Methods accepted that shouldn't be (PUT, DELETE, TRACE, CONNECT) |
| **Header Fuzzing** | A01, A05 | X-Forwarded-For bypass, custom-header-gated features, User-Agent gates |
| **Cookie Fuzzing** | A01, A05 | Hidden feature flags, trust switches, session privilege escalation |
| **401/403 Path Bypass** | A01 | Case, encoding, double-slash, null-byte, path traversal to bypass ACL |
| **Auth Stripping** | API2, A01 | Endpoints that respond without valid credentials |
| **Type Confusion** | A03, API6 | Crashes, info leaks, silent wrong-type acceptance |
| **Boundary Values** | A04 | Missing min/max/zero/overflow validation on any numeric field |
| **Parameter Pollution** | A03 | Duplicate keys, array/scalar confusion, unexpected parsing |
| **Mass Assignment** | API6 | Undocumented fields accepted and persisted |
| **Entropy Analysis** | A07 | Predictable or brute-forceable generated values |
| **Error Disclosure** | A05 | Stack traces, internal paths, query structure leaked in errors |

---

## Depth Presets

| Depth | What runs | Default limits |
|-------|-----------|----------------|
| `quick` | Wildcard calibration + directory discovery (common.txt) + auth stripping + mass assignment | $0.10 · 15 min · 10 calls |
| `standard` | Quick + extension fuzzing + backup files + verb fuzzing + header/cookie fuzzing + type confusion + boundary values + parameter pollution | $0.50 · 45 min · 25 calls |
| `thorough` | Standard + recursive directory scan + 401/403 bypass + entropy analysis + ffuf param discovery + full error triage | unlimited · unlimited · unlimited |

---

## Workflow

### Before running any tool

If depth is not specified, ask:

> **Target:** `<extracted URL>`
> **Which depth?**
> - `quick` — auth stripping + mass assignment only *($0.10 · 15 min · 10 calls)*
> - `standard` — + type confusion + boundary values + parameter pollution *($0.50 · 45 min · 25 calls)*
> - `thorough` — + entropy analysis + param discovery + error triage *(unlimited)*

---

### Phase 0 — Scope & Setup

0. `session(action="start", options={...})` with target URL, depth, and limits
1. `report(action="dashboard", data={"port": 7777})`
2. Load endpoint inventory from coverage matrix (`session(action="status")`), or spider if none exists
3. `report(action="note", ...)` with: total endpoints, which require auth, which params are numeric/boolean/array, which endpoints mutate state (POST/PUT/PATCH/DELETE)

---

### Phase 1 — Wildcard Calibration (ALWAYS FIRST)

Before running any wordlist scan, determine whether the server returns a meaningful response for nonexistent paths. A server that returns **200** for everything makes all fuzzing results noise.

**Test:**
```
kali(command="curl -s -o /dev/null -w '%{http_code} %{size_download}' https://TARGET/$(cat /dev/urandom | tr -dc 'a-z0-9' | head -c 16)")
kali(command="curl -s -o /dev/null -w '%{http_code} %{size_download}' https://TARGET/api/$(cat /dev/urandom | tr -dc 'a-z0-9' | head -c 16)")
```

| Response | What to do |
|----------|------------|
| 404 | Safe to fuzz — filter out 404s with `-fc 404` |
| 200 with constant body size | Wildcard 200 — calibrate with `-fs <size>` or `-ac` |
| 200 with variable body size | Must use `-fw` (word count filter) or `-fl` (line count filter) or `-fr` (regex) |
| 302 to login | Filter the redirect: `-fc 302` or `-mc 200,403,500` |

**Always pass `-ac` (auto-calibrate) to ffuf unless you have a specific reason not to.** It performs multiple probe requests internally and sets size/word/line filters automatically.

---

### Phase 2 — Content Discovery: Directories & Files

**Step 2a — Directory enumeration:**

```
kali(command="ffuf -ac -u https://TARGET/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -mc 200,201,204,301,302,307,401,403,405 -t 40 -o /tmp/dirs.json -of json")
```

After finding directories, recurse into them (thorough depth):
```
kali(command="ffuf -ac -u https://TARGET/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -recursion -recursion-depth 2 -mc 200,201,204,301,302,307,401,403,405 -t 20 -o /tmp/dirs-recursive.json -of json")
```

**Step 2b — File discovery (with common extensions):**
```
kali(command="ffuf -ac -u https://TARGET/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt -mc 200,201,204,301,302,307,401,403,405 -t 40")
```

**Step 2c — Extension fuzzing on known paths:**

For every discovered file path (e.g., `/index`), brute-force extensions:
```
kali(command="ffuf -ac -u https://TARGET/indexFUZZ -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt -mc 200,201,204,301,302,307,401,403 -t 20")
```

Extension wordlist to cover: `.php`, `.php3`, `.php5`, `.phtml`, `.asp`, `.aspx`, `.jsp`, `.jspx`, `.do`, `.action`, `.html`, `.htm`, `.xml`, `.json`, `.yaml`, `.yml`, `.txt`, `.cfg`, `.conf`, `.config`, `.ini`, `.env`, `.log`, `.sql`, `.db`, `.sqlite`, `.bak`, `.backup`, `.old`, `.orig`, `.copy`, `.swp`, `.~`, `.zip`, `.tar.gz`, `.gz`, `.7z`.

**Step 2d — Backup file discovery:**

For every known file (`index.php`, `config.php`, `app.py`, `web.config`, `settings.py`, etc.), probe predictable backup names:
```
kali(command="for f in index.php config.php app.py settings.py web.config application.properties; do
  for ext in .bak .backup .old .orig .copy .swp ~ .zip .tar.gz .1 .0; do
    code=$(curl -s -o /dev/null -w '%{http_code}' https://TARGET/${f}${ext})
    [ \"$code\" != \"404\" ] && echo \"HIT: ${f}${ext} -> $code\"
  done
done")
```

Also check editor swap files for any discovered `.php` or `.py` files:
```
kali(command="ffuf -ac -u https://TARGET/FUZZ -w /usr/share/seclists/Discovery/Web-Content/Common-DB-Backups.txt -mc 200,206 -t 20")
```

**Step 2e — Sensitive file hunting:**
```
kali(command="ffuf -ac -u https://TARGET/FUZZ -w /usr/share/seclists/Discovery/Web-Content/CommonBackdoors-PHP.fuzz.txt -mc 200 -t 20")
```

Always probe these regardless:
```
http(action="request", url="https://TARGET/.git/HEAD")
http(action="request", url="https://TARGET/.git/config")
http(action="request", url="https://TARGET/.env")
http(action="request", url="https://TARGET/.DS_Store")
http(action="request", url="https://TARGET/wp-config.php.bak")
http(action="request", url="https://TARGET/config.php.bak")
http(action="request", url="https://TARGET/database.yml")
http(action="request", url="https://TARGET/secrets.yml")
http(action="request", url="https://TARGET/phpinfo.php")
http(action="request", url="https://TARGET/server-status")
http(action="request", url="https://TARGET/server-info")
http(action="request", url="https://TARGET/crossdomain.xml")
http(action="request", url="https://TARGET/clientaccesspolicy.xml")
```

**Finding criteria:**
- `.git/HEAD` returns `ref: refs/heads/` → **Critical** — dump the whole repo with `kali(command="git-dumper https://TARGET/.git /tmp/repo")`
- `.env` or `config.php.bak` with credentials → **Critical**
- `phpinfo.php` accessible → **Medium**
- Any `.bak`/`.old` file with source code → **High**
- `.DS_Store` present → **Low** (lists directory contents)

---

### Phase 3 — HTTP Verb Fuzzing

For every endpoint in the coverage matrix, test every HTTP method. Many apps only implement GET/POST but don't explicitly reject PUT/DELETE/TRACE, leading to logic bypasses or unintended state changes.

```
kali(command="wfuzz -c -z list,GET-POST-PUT-DELETE-PATCH-HEAD-OPTIONS-TRACE-CONNECT-PROPFIND-PROPPATCH-MKCOL-COPY-MOVE-LOCK-UNLOCK -X FUZZ https://TARGET/api/user/1 2>/dev/null | grep -v '404'")
```

Or with ffuf:
```
kali(command="ffuf -u https://TARGET/api/user/1 -X FUZZ -w /usr/share/seclists/Fuzzing/http-request-methods.txt -mc 200,201,204,302,400,405,500 -t 10")
```

**What to look for per method:**

| Method | Finding if accepted |
|--------|-------------------|
| `PUT` on a resource URL | May allow arbitrary file write or resource replacement |
| `DELETE` on a resource | May allow unauthorized deletion |
| `TRACE` | Reflects request headers → Cross-Site Tracing (XST), useful for bypassing HttpOnly |
| `OPTIONS` | Check `Allow:` header — lists every method the server supports, including undocumented ones |
| `CONNECT` | Proxy abuse if accepted |
| `HEAD` | If different response than GET (different auth behavior, different headers) |
| Any method returning `405` on path A but `200` on path A/ (trailing slash) | WAF/router inconsistency |

Also test **method override headers** on POST endpoints:
```
http(action="request", url="https://TARGET/api/user/1", method="POST",
  headers={"X-HTTP-Method-Override": "DELETE", "X-Method-Override": "DELETE", "_method": "DELETE"})
```

---

### Phase 4 — Header Fuzzing

HTTP headers are frequently gated by trust assumptions. Applications often expose different functionality or bypass access controls based on header values.

**Step 4a — IP source spoofing / internal bypass:**
```
# Try to bypass IP-based access controls:
http(action="request", url="https://TARGET/admin",
  headers={
    "X-Forwarded-For": "127.0.0.1",
    "X-Real-IP": "127.0.0.1",
    "X-Originating-IP": "127.0.0.1",
    "X-Remote-IP": "127.0.0.1",
    "X-Client-IP": "127.0.0.1",
    "True-Client-IP": "127.0.0.1",
    "CF-Connecting-IP": "127.0.0.1"
  }
)
```
Send each header individually — some apps only trust one specific header.

**Step 4b — Custom header discovery:**
```
kali(command="ffuf -u https://TARGET/ -H 'FUZZ: test' -w /usr/share/seclists/Discovery/Web-Content/x-custom-headers.txt -mc 200,302,403,500 -fw <baseline_word_count> -t 20")
```

Common high-value headers to probe manually:
```
X-Internal: true
X-Admin: true
X-Debug: 1
X-Original-URL: /admin
X-Rewrite-URL: /admin
X-Override-URL: /admin
X-Forwarded-Host: internal.target.com
X-Forwarded-Proto: https
X-Api-Version: 2
X-Feature-Flag: admin
X-Tenant-ID: 1
X-User-ID: 1
X-Role: admin
X-Auth-Override: admin
```

**Step 4c — User-Agent gating:**
```
kali(command="ffuf -u https://TARGET/ -H 'User-Agent: FUZZ' -w /usr/share/seclists/Fuzzing/User-Agents/user-agents.txt -mc 200,302,403 -fw <baseline> -t 10")
```
Some admin panels or mobile-only features only render for specific User-Agent strings.

**Step 4d — Host header injection (for password reset / OAuth):**
```
http(action="request", url="https://TARGET/password-reset", method="POST",
  headers={"Host": "ATTACKER.com"},
  body="email=victim@example.com"
)
```
If the password reset email contains `ATTACKER.com` in the link → Host header injection confirmed.

---

### Phase 5 — Cookie Fuzzing

**Step 5a — Discover hidden cookie names:**
```
kali(command="ffuf -u https://TARGET/ -H 'Cookie: FUZZ=1' -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -mc 200,302,403,500 -fw <baseline> -t 20")
```

**Step 5b — Boolean feature flag cookies:**
For every cookie the app sets, try toggling boolean-looking values:
```
# If app sets: Cookie: beta=false
http(action="request", url="https://TARGET/", headers={"Cookie": "beta=true"})
http(action="request", url="https://TARGET/", headers={"Cookie": "beta=1"})
http(action="request", url="https://TARGET/", headers={"Cookie": "debug=1"})
http(action="request", url="https://TARGET/", headers={"Cookie": "admin=1"})
http(action="request", url="https://TARGET/", headers={"Cookie": "role=admin"})
http(action="request", url="https://TARGET/", headers={"Cookie": "internal=true"})
```

**Step 5c — Cookie value injection:**
For every session/auth cookie, try:
- Modifying the `role`, `is_admin`, `tier`, `user_id` sub-fields if the cookie is a JSON blob or base64-encoded JWT
- Setting cookie to `null`, `""`, `undefined`, `0`, `-1` to test null-bypass
- Appending `;Path=/admin` or `;Domain=target.com` to test cookie scoping

---

### Phase 6 — 401/403 Bypass via Path Manipulation

When a path returns 401 or 403, try these bypass variants before accepting the access control:

```
# Baseline: GET /admin → 403
# Try all variants:
/ADMIN
/Admin
/admin/
//admin
/./admin
/admin/.
/%2fadmin
/admin%20
/admin%09
/admin%00
/admin;/
/admin..;/
/%61dmin         (URL-encoded 'a')
/%2561dmin       (double-encoded)
/admin#
/admin?
/admin/..%2f
/admin/../admin
```

Automate with ffuf's `-w` on a bypass wordlist:
```
kali(command="ffuf -u https://TARGET/FUZZ -w /usr/share/seclists/Fuzzing/403-ignore/path-bypass.txt -mc 200,301,302 -t 20")
```

Also test HTTP method override and adding `..;/` before the protected segment:
```
http(action="request", url="https://TARGET/public/..;/admin", method="GET")
http(action="request", url="https://TARGET/api/v1/..;/admin/users", method="GET")
```

---

### Phase 7 — Auth & Token Stripping

For every endpoint that normally requires authentication:

**1a — Remove auth entirely**
Send the request with no `Authorization` header, no session cookie, no API key. Any 2xx response or data body → **High** finding.

**1b — Invalid/malformed token**
Send `Authorization: Bearer AAAAAAAAAAAAAAAA`. Any 2xx → **High** (no signature/validity check).

**1c — Expired token**
If you can obtain an expired token (or craft one with a past `exp` claim) — send it. Any 2xx → **High**.

**1d — Other user's token**
Authenticate as User B. Use User B's token to request User A's resource by substituting the resource ID. 2xx with User A's data → BOLA — chain to `/business-logic` for full authorization matrix.

**1e — Strip individual required parameters**
For each non-auth required parameter, send the request with that param removed, then set to `""`, then set to `null`. Record:
- 400/422 with clear validation message → working
- 500 → server crash → **Medium** (logic error / information disclosure)
- 200 → param was not actually required → flag for manual review

---

### Phase 8 — Type Confusion

For every parameter, send the mismatched-type probe set below. Send each as a separate request — watch for status code changes, response body changes, and error messages.

| Declared type | Probes to send |
|--------------|----------------|
| `integer` | `"foo"`, `null`, `true`, `false`, `1.5`, `-1`, `0`, `9999999999`, `""`, `[]`, `{}` |
| `string` | `0`, `true`, `false`, `null`, `[]`, `{}`, `""`, `" "`, 10 000-char string, `%00`, `%0a%0d` |
| `boolean` | `"yes"`, `"no"`, `"true"`, `"false"`, `"1"`, `"0"`, `0`, `1`, `-1`, `null`, `""`, `[]` |
| `array` | plain string, `{}`, single string item, deeply nested `[[[[[]]]]]`, `null` |
| `object/JSON` | plain string, integer, `[]`, `null`, malformed JSON `{key:}` |
| `email` | `foo`, `foo@`, `@bar.com`, `a@b`, `javascript:alert(1)`, plain integer, 500-char string |
| `URL/URI` | `foo`, `javascript:alert(1)`, `file:///etc/passwd`, `//evil.com`, plain integer, empty |
| `date/datetime` | `"foo"`, `0`, `-1`, `"9999-99-99"`, `"1970-01-01"`, `"2099-01-01"`, negative timestamp |
| `uuid` | `"not-a-uuid"`, `"00000000-0000-0000-0000-000000000000"`, integer `1`, empty |

Batch same-endpoint probes into a loop via `kali(command="for val in ...")` for efficiency. Use `ffuf` with a type-confusion wordlist when hitting a large number of params on the same endpoint.

**Finding criteria**:
- 5xx on any probe → **Medium** (missing validation; may escalate if stack trace returned)
- Stack trace in response body → **High** (information disclosure)
- Silent acceptance of wrong type that changes behavior or response data → **High**
- Consistent difference in error message between valid and invalid inputs → **Low** (enumeration vector)

---

### Phase 9 — Boundary Value Analysis

Target: every numeric, quantity, size, count, rating, score, or date parameter.

**Standard probe set per param:**
```
0
-1
-0
1
MIN - 1   (use documented minimum, or 1 as default)
MIN
MIN + 1
MAX - 1
MAX
MAX + 1   (use documented max, or a large reasonable value)
2147483647    (INT32_MAX)
2147483648    (INT32_MAX + 1 — causes signed overflow in 32-bit systems)
-2147483648   (INT32_MIN)
9223372036854775807   (INT64_MAX — useful for systems using 64-bit integers)
9999999999999
0.001
0.0001
0.00001
NaN
Infinity
-Infinity
```

**Domain-agnostic special probes** — apply to any field whose value represents a quantity, price, limit, rating, or score:
- Negative value: does the app credit the actor instead of debiting?
- Zero: is it accepted? Does it create a record? Skip side effects?
- Sub-unit value (0.001): does rounding favor the attacker?
- Value exceeding a stated limit: is the limit enforced server-side?
- MAX + 1: does integer overflow produce an unexpected result?

**Temporal boundary probes** for date/time fields:
- Past dates: `1970-01-01`, `2000-01-01`, yesterday
- Future dates: `2099-01-01`, `9999-12-31`
- Boundary of active period: exactly at expiry, one second before/after

**Finding criteria**:
- Negative value accepted that modifies any counter, balance, score, or quantity → **Critical/High**
- Value exceeding a documented limit that is processed anyway → **High**
- 5xx on any boundary probe → **Medium**
- Zero-value operation that creates a record or consumes a quota slot → **Medium**

---

### Phase 10 — HTTP Parameter Pollution & Format Confusion

**4a — Duplicate parameter keys**
Send the same parameter twice in the same request with different values. Different frameworks resolve this differently (last wins, first wins, array, error):
```
POST /search?q=foo&q=bar
POST /api/users with body: {"role":"user","role":"admin"}
GET /items?id=1&id=2
```
Watch for: unexpected value used, server error, behavior matching the second value (last-wins = injection vector).

**4b — Array vs scalar confusion**
Send a scalar param as an array and vice versa:
```json
// Expected scalar → send array:
{"user_id": [1, 2, 3]}
{"role": ["user", "admin"]}

// Expected array → send scalar:
{"permissions": "admin"}
{"tags": "important"}
```
Watch for: first item used, all items processed (mass operation), server crash.

**4c — Nested object injection**
For flat key-value params, try sending nested objects:
```json
// Expected: {"name": "foo"}
// Inject:   {"name": {"$gt": ""}}    ← NoSQL operator
//           {"name": {"toString": "admin"}}
//           {"user": {"id": 1, "is_admin": true}}
```

**4d — Content-Type confusion**
For endpoints that expect `application/json`, also try:
- `application/x-www-form-urlencoded` with the same payload
- `multipart/form-data`
- `text/plain`
- No Content-Type header

Watch for: params parsed differently, validation bypassed, different code path triggered.

**Finding criteria**: Any different behavior between the two content types on the same params → **Medium** (inconsistent parsing = exploitable inconsistency). Array accepted when scalar expected + processed as multiple items → **High** (mass operation injection).

---

### Phase 11 — Mass Assignment Discovery

For every POST / PUT / PATCH endpoint, inject additional fields alongside the normal valid body. Three passes:

**Pass 1 — Privilege / role fields**
```json
"is_admin": true,
"is_staff": true,
"role": "admin",
"roles": ["admin", "superuser"],
"permissions": ["read", "write", "admin", "delete"],
"is_verified": true,
"verified": true,
"approved": true,
"active": true,
"locked": false,
"subscription_tier": "enterprise",
"plan": "unlimited",
"beta_access": true,
"feature_flags": {"admin": true, "debug": true}
```

**Pass 2 — Value / quantity / pricing fields** (applicable to any domain)
```json
"price": 0,
"price": 0.01,
"cost": 0,
"discount": 100,
"discount_percent": 100,
"quantity": -1,
"amount": -1,
"score": 9999999,
"credits": 9999999,
"quota": -1,
"limit": 999999,
"max_uses": 999999,
"rate_limit": 0,
"storage_gb": 999999,
"exchange_rate": 10000,
"fee": 0,
"tax_rate": 0
```

**Pass 3 — Ownership / relationship fields**
```json
"user_id": 1,
"owner_id": 1,
"created_by": 1,
"account_id": 1,
"org_id": 1,
"tenant_id": 1,
"admin_id": 1,
"parent_id": null,
"group_id": 1
```

**Detection method — three-step check for each endpoint:**
1. Does the injected field appear in the response body?
2. Does the response body change (different role, status, value shown)?
3. Make a follow-up GET on the same resource — does the injected value appear?

Step 3 confirms persistence. Log finding + save PoC immediately.

**Finding criteria**: field accepted and persisted → **High** (generic BOPLA). Privilege field persisted and grants elevated access → **Critical**.

**Automated parameter name discovery** (thorough depth):
```
scan(tool="ffuf", target="URL", options={"wordlist": "burp-parameter-names.txt"})
```
Then inject the discovered parameter names as additional fields in Pass 1-3.

---

### Phase 12 — Entropy & Predictability Analysis

*Standard and thorough depth.*

Collect **10 samples** of every type of generated value the application produces. Trigger generation via the action that creates each value type.

| Value type | How to collect 10 samples | Flag if... |
|-----------|--------------------------|-----------|
| Password reset token / OTP / PIN | Trigger reset flow 10× | ≤ 6 chars numeric, or consistent delta |
| Registration / email verification token | Register 10 accounts | Short, sequential, or low-entropy |
| Session tokens / auth tokens | Login 10× from different accounts | UUID v1, entropy < 80 bits |
| Resource IDs (any type: orders, posts, tickets, cards) | Create 10 resources | Consistent arithmetic delta (+1, +2, +N) |
| Reference / confirmation numbers | Perform 10 state-changing operations | Predictable pattern, timestamp-based |
| Invite / coupon codes | Generate 10 codes | Short, sequential, dictionary-word-based |
| API keys | Generate 10 keys (if possible) | Short, sequential, low-entropy |
| File upload names / paths | Upload 10 files | Predictable name = overwrite or enumeration |

**Entropy script** (run via `kali`):
```python
import math
samples = ["REPLACE_WITH_COLLECTED_SAMPLES"]
charset = len(set("".join(samples)))
avg_len = sum(len(s) for s in samples) / len(samples)
bits = avg_len * math.log2(max(charset, 2))
deltas = []
for i in range(len(samples) - 1):
    try:
        deltas.append(int(samples[i+1]) - int(samples[i]))
    except (ValueError, TypeError):
        pass
print(f"Charset: {charset} | Avg length: {avg_len:.1f} | Entropy: {bits:.1f} bits")
if deltas:
    consistent = len(set(deltas)) == 1
    print(f"Deltas: {deltas} | Consistent: {consistent} (sequential={consistent})")
```

**Severity mapping**:
- Entropy < 32 bits → **Critical** (e.g., 3-digit PIN = ~10 bits — trivially brute-forceable)
- Entropy < 80 bits → **High** (brute-forceable with enough requests, especially without lockout)
- Entropy < 128 bits → **Medium** (marginal — flag for review with context of lockout policy)
- Consistent sequential delta on any ID → **High** (full resource enumeration trivial)
- UUID v1 format (`xxxxxxxx-xxxx-1xxx-...`) → **Medium** (time-based, predictable within window)
- Timestamp-derived prefix → **Medium** (narrows the search space significantly)

---

### Phase 13 — Error Disclosure Triage

Review every 4xx/5xx response collected across all phases. Flag:

| Pattern in response body | Severity | Notes |
|--------------------------|----------|-------|
| Language runtime traceback (Python, Java, Ruby, PHP, Node, etc.) | **High** | Reveals framework version, file paths, code lines, internal logic |
| SQL query fragments (`SELECT`, `WHERE`, table or column names) | **High** | Confirms injection surface; reveals schema |
| NoSQL query operators in error (`$where`, `$regex`, etc.) | **High** | Confirms NoSQL injection surface |
| Internal hostname, private IP, or internal URL | **Medium** | Internal network topology leak |
| Library/framework version string | **Low** | Enables targeted CVE lookup |
| Filesystem path (`/var/www/`, `/app/`, `C:\inetpub\`) | **Medium** | Internal path disclosure |
| Different error messages for valid vs invalid user input | **Medium** | Enumeration vector — note which field and what differs |
| Full request echoed back in error | **Low** | Confirms input reflection point — test for XSS/SSTI |

For each finding: save the exact response snippet as evidence, save a PoC via `http(action="save_poc", ...)`.

---

### Chaining

| Condition | Chain to |
|-----------|---------|
| Mass assignment confirmed (field persisted) | `/business-logic` — test if the injected access enables workflow or value abuse |
| Sequential IDs or low-entropy tokens found | `/business-logic` — Phase 5 predictability for enumeration impact |
| Auth stripping reveals unauthenticated surface | `/web-exploit` — injection testing on now-accessible endpoints |
| Stack trace reveals DB query | `/web-exploit` — SQLi depth testing on the triggering param |
| Negative/zero value accepted on quantity field | `/business-logic` — financial/value logic abuse |
