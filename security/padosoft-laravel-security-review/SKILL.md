---
name: padosoft-laravel-security-review
description: >-
  Use this skill before committing or reviewing a change to a Laravel application that touches a model's
  fillable or guarded, a Blade template printing unescaped, raw SQL, a file upload, a route exempted from
  CSRF, a shell call, a redirect built from input, an id coming from the request, an audit trail, or an
  AI/LLM call — and whenever the user asks for a security review or an audit, or says an endpoint returns
  somebody else's data or an error shows SQL to the user. It runs ten checks with ready pre-screens plus
  ownership, audit integrity and error-leak rules. Do not use it for API-side (padosoft-api-security-review)
  or mobile (padosoft-mobile-security-review) work, nor for infrastructure hardening.
license: MIT
compatibility: >-
  Any Laravel version — these are classes of vulnerability, not framework features. Where a version moved a
  file, it is noted inline. The pre-screens assume a POSIX shell.
metadata:
  version: 0.2.0
  author: Padosoft
  summary: Ten checks plus three rules whose cost is disproportionate to how easy they are to get wrong.
  profiles: laravel
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: laravel, php, security, owasp, idor, mass assignment, blade, csrf, audit, eloquent
---

# Laravel security review

Ten checks plus three rules whose cost is disproportionate to how easy they are to get wrong. Run them on the
diff before committing, and on the PR during review.

Output of a pre-screen is a **list of candidates to confirm or discard**, never an automatic bounce on a
single grep match.

---

## The ten checks — `SEC-OWASP-001`

### 1. Mass assignment

```bash
grep -rnE '->(create|fill|update)\((request\(\)->|.*->all\(\))' --include='*.php' app/
```

`$guarded = []` on a new model is an open door. Declare `$fillable` explicitly, and pass a **validated**
array — `$request->validated()`, not `$request->all()`. A validated array is also the only one whose shape
you can reason about later.

### 2. XSS through unescaped Blade

```bash
grep -rnE '\{!! *\$' --include='*.blade.php' resources/
```

`{!! $var !!}` prints raw. It is legitimate only for HTML you generated, never for anything that passed
through user input or the database. If it must be user content, sanitise it at that point and say so in a
comment.

### 3. Raw SQL with interpolation

```bash
grep -rnE '(whereRaw|orderByRaw|selectRaw|havingRaw|DB::(raw|statement|select))\([^,)]*\$' --include='*.php' app/
```

Bindings, always — including in `orderByRaw`, which people forget because it "is not a value". A column name
or a sort direction goes through an **allow-list plus a ternary**, never a request string.

### 4. File upload

Validate MIME **and** extension **and** size, store outside the web root or on a private disk, and never
build the stored name from the original one. An uploaded file's reported type is caller-controlled.

### 5. CSRF

Every exempted route is listed with a reason. A signed webhook is a legitimate exemption — after the
signature is verified, and with that written next to the exemption.

### 6. Command injection

```bash
grep -rnE '\b(shell_exec|exec|passthru|system|proc_open|popen)\(' --include='*.php' app/
grep -rnE 'new Process\("[^"]*\$' --include='*.php' app/
```

Prefer the array form of the process API, which does not go through a shell. If a string command is
unavoidable, every interpolated value is escaped at the call site.

### 7. Open redirect

```bash
grep -rnE '(redirect|Redirect::to)\(\$request->' --include='*.php' app/
```

A redirect target from input is a phishing primitive. Allow-list the host, or redirect to a **named route**
resolved from a key, never to a URL the caller supplied.

### 8. Hardcoded secrets

```bash
grep -rniE '(api[_-]?key|token|secret|password|jwt)\s*=\s*["\x27][A-Za-z0-9_\-]{20,}' --include='*.php' app/ config/
```

Config reads the environment; the environment is not in the repository. A secret that was committed stays
valid until it is rotated at the provider — `git rm` revokes nothing.

### 9. IDOR — `SEC-IDOR-001`

```bash
grep -rnE 'findOrFail\(\$request->|find\(\$request->|find\(\$id\)' --include='*.php' app/
```

**The owner id comes from the authenticated user, never from the request.** Scope the query, do not filter
after:

```php
// ❌ any id works
$order = Order::findOrFail($request->input('order_id'));
// ✅ the scope is the query
$order = $request->user()->orders()->findOrFail($request->input('order_id'));
```

Policies and `authorize()` are the structural form of the same thing. On a nested resource, scope through the
parent relation — do not assume the parent was checked. A mismatch returns 404, never a distinguishable
error, or the endpoint becomes an existence oracle.

### 10. Unsafe deserialisation

```bash
grep -rnE '\bunserialize\(' --include='*.php' app/
```

`unserialize` on anything a caller can influence — a cookie, a cache entry they can write, a queue payload
from an untrusted producer — is remote code execution. Use JSON.

---

## Six more, from a hardening sprint — `SEC-HARDEN-001`

### 11. Authorisation that is present and empty

A generated request class ships with a permissive authorisation stub. Count how many still have it: in a
codebase of any age the number is in the hundreds, and each one is a route whose authorisation is whatever
the controller remembered to do.

```bash
rg -n -A3 "function authorize\(\)" app/ | rg -B1 "return true;"
```

Then two shapes that pass review and authorise nothing:

- **A presence check used as authorisation.** Validating that a record exists says nothing about who may
  touch it.
- **The tautological check**: the record was fetched *by* the identifier from the request and is then
  verified *against* that same identifier. It always passes.

### 12. The rule of twins

Where two routes reach the same resource — an older one and a newer one, a page and its asynchronous
counterpart, a web form and its API — the controls are on the one built last, and the one built first is
still wired. Review them **side by side**, never one at a time. The same applies to a guest branch next to
an authenticated one: it was written later and looser.

### 13. Formula injection in exports

A cell whose value starts with an operator becomes a formula in the recipient's spreadsheet, and that is a
remote-execution primitive delivered by your own reporting feature. Neutralise at the **single writing choke
point** — a guarded writer and a value binder registered as the default — rather than at each of the dozens
of call sites. Machine-to-machine feeds are deliberately left alone: a quoting prefix breaks the parser at
the other end.

### 14. Outbound requests need a guard, at one choke point

```text
reject: non-HTTP schemes · loopback · private and carrier-grade ranges · the cloud metadata address
        · credentials in the URL · control characters · unresolvable hosts
with:   name resolution ENABLED
```

Without resolution, a hostname that resolves to loopback walks straight through — which is the whole attack.
Put the guard inside the one HTTP client everything uses, mark the call sites that accept untrusted input,
and remember that a guard which is off by default protects nothing. The pooled/concurrent path of the client
is a separate surface; check it.

### 15. Uploads: the choke point owns the name, the disk and the scan

- The stored name is generated by one helper, not by each request class, and **every** dotted segment is
  checked rather than the last one.
- **The destination disk is not taken from the request.** Left to the client, it picks among every
  configured disk — including the ones served over the web.
- Malware scanning hooks in at the same point and **fails closed when enabled**, which is why the flag and a
  reachable engine ship together.
- A staged upload area with no lifecycle becomes a permanent, unindexed, publicly reachable archive.

### 16. Errors, echoes and authored HTML

- **Internal identifiers are technical detail**: a model class name, a table, a path. A validation message
  that names a model tells an attacker the shape of your schema.
- **Keep a standing inventory of unescaped echoes in templates**, front-end and back-office alike, rather
  than reviewing them one diff at a time.
- **Rich text authored in the back-office must render fully and execute nothing**: sanitise against an
  allow-list of elements and attributes. Escaping it makes the feature useless; trusting the author makes
  every back-office account an XSS vector.

## Error messages must not leak internals — `SEC-ERRLEAK-001`

A `QueryException` rendered with its native message is the worst single string an application can show a
user. Laravel builds that message from the driver error **and the statement**, so it carries, in one line:
the SQLSTATE and the driver code, the table and column, the connection host, port and database name, the
full statement — and, because the statement is the one that was executed, **the values that were being
written**. When the row being saved belongs to a person, those values are their data.

That makes it two problems at once: an infrastructure disclosure that tells an attacker where to aim, and a
personal-data exposure that reaches whoever is looking at the screen, plus the support ticket and the chat
the screenshot ends up in.

**No technical detail reaches the client**: no SQL or fragment of it, no SQLSTATE, no table or column name, no
host, port or database name, no filesystem path, no stack trace, no PHP class name.

Build user-facing text through a **sanitising helper**, never `$exception->getMessage()`. Three layers, and
the third is the one people skip:

| Layer | Where | What it does |
|---|---|---|
| Source | the exception handler | `QueryException`/`PDOException` never rendered natively; the framework's default log, which would write SQL and personal data, replaced by a structured masked one |
| Extraction | a `safeErrorMessage()` helper | composes and sanitises the message that goes into the response |
| Safety net | a response middleware | inspects JSON and `>= 400` responses and replaces technical values that a controller let through |

**The safety net logs a warning when it fires**, because it firing means something upstream leaked. It is a
net, not permission to keep writing `$e->getMessage()`.

The user gets a generic message plus a **reference code**; the same code is in the log, so support gets to
the exact row. What goes in the log is in **`padosoft-logging-discipline`** — in short: the parameterised SQL
and the bindings as type and length, never the values.

⚠️ **This code runs in the error path**, so it runs when the database is unreachable. Every settings or
translation read inside it is wrapped in try/catch with a hardcoded default, or a DB error becomes a loop of
errors.

⚠️ **In local you are not seeing production.** Keeping technical messages visible while developing is right,
but it means nobody ever looks at the production path: flip the switch and try the endpoint before calling
the work done.

## Audit trail integrity — `SEC-AUDIT-001`

An audit or log store is **append-only**: no update, no delete in place — the model refuses them. Erasure for
a data-subject request goes through a sanctioned, audited maintenance command, not an `UPDATE`.

An audit row records **who, what, when, from where** and is written in the same transaction as the change it
describes. An audit written after a commit, outside the transaction, is missing precisely for the operations
that failed halfway.

## Concurrency: the invariant is recorded, or it does not exist

A single-use check, a rate limit, a nonce, a quota: the lock is held **until the invariant is recorded**.
The `lockForUpdate()` read and the `update()` write live in the **same** transaction closure — otherwise two
requests both read "not used yet" and both proceed.

```php
DB::transaction(function () use ($code) {
    $row = Coupon::whereCode($code)->lockForUpdate()->firstOrFail();
    abort_if($row->used_at !== null, 409);
    $row->update(['used_at' => now()]);      // same closure, or the lock bought nothing
});
```

Where the business rule demands it, back it with a **database-level unique constraint**: the transaction is
the fast path, the constraint is the one that is still true under a deploy, a replica lag or a retry.

## AI / LLM surface — `SEC-LLM-001`

The provider key lives server-side only. The model's output is **untrusted input** for whatever consumes it:
a URL it produced goes through URL validation, a query it suggests goes through check 3, HTML it produced is
escaped. Tool and function handlers are endpoints — authorise them with the same policies, and never expose
one the caller could not invoke directly. **The model proposes, the server authorises**: a confirmation in
the UI is not a control. Prompts and conversation history are personal data.

---

## Documented exceptions

Every exception to the rules above is annotated inline, with author, date and reason:

```php
// <initials>, <date>: HMAC-signed webhook, CSRF disabled after signature verification
protected $except = ['webhook/stripe'];
```

**No silent exception.** A review that finds an anti-pattern without an explicit marker bounces the PR.

## Gotchas

- **A pre-screen hit is a candidate, not a verdict.** Turning a single grep match into an automatic bounce
  trains everyone to ignore the check.
- **`$request->all()` is not validation** even when a FormRequest ran: it returns everything that was sent.
- **A policy that is never called is not a control.** Check that `authorize()` is actually reached on the path
  you are reviewing.
- **Where the framework moved things:** the exception handler lives in the application bootstrap file in
  recent versions and in a dedicated handler class in older ones. The rule is identical; only the path
  changes, and the same goes for where middleware is registered.

## Final report

```
Laravel security review: <n> files
SEC-OWASP-001  1..10: PASS | FAIL <check n — file:line, and the fix>
SEC-IDOR-001 · SEC-ERRLEAK-001 · SEC-AUDIT-001 · SEC-LLM-001
Documented exceptions found: <n> (all with a marker? yes/no)
Production error behaviour verified locally: yes | no
Verdict: BLOCKED | OK TO COMMIT
```
