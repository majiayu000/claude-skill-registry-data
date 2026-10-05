---
name: padosoft-api-security-review
description: >-
  Use this skill before committing or reviewing any change to an HTTP API that touches routing, auth
  middleware, settings or config endpoints, logging and telemetry, SQL, error handling, response shaping,
  client IP, rate limits or an outbound fetch — and whenever the user asks for a security review, an audit,
  or says an endpoint "seems public", "returns too much" or "leaks something": it runs ten checks with ready
  grep pre-screens (auth on every mutating route, ownership from the authenticated id, no secrets or PII in
  responses, bound SQL, fail-safe env gates, resource caps, redacted logs, downstream injection, no trust
  from caller input, supply chain) and blocks the commit on each violation. Do not use it for infrastructure
  hardening (WAF, DNS, firewall) or for dependency CVE triage.
license: MIT
compatibility: >-
  Any HTTP API. The grep pre-screens assume a POSIX shell and a TypeScript/JavaScript codebase; the rules
  themselves are language-agnostic. Some notes are specific to Hono, and are marked as such.
metadata:
  version: 0.3.0
  author: Padosoft
  summary: Ten checks on an API change, each carrying the mistake that produces it.
  profiles: api, node
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: security, api, audit, auth, idor, secrets, sql injection, rate limit, owasp, review
---

# API security review

Ten checks to run **before committing** a change to an API, and when reviewing a PR. Each one carries the
mistake that produces it: these are failure modes that have been seen in production code, not items from a
generic checklist.

The complete rules, with identifiers and rationale, are in [`references/rules.md`](references/rules.md).
Read it when a check fires and you need the full reasoning, or when you have to decide whether something is
a real exception.

---

## 0. How to run it

```bash
git diff --cached --name-only --diff-filter=ACMR | grep -E '\.(ts|js|mjs)$'
# empty? then: git diff --name-only
```

Apply the relevant checks to those files. **For every violation: block the commit**, name the rule, propose
the fix. Skip a check that does not apply to the diff — do not report it as passed.

**A pre-screen is a screen, not a verdict.** Each one is tuned to surface candidates, and a healthy codebase
still produces hits: they are the compliant implementations of the very rule being checked. Where that
happens, the check below shows what a compliant hit looks like — recognise it, say so in one line, move on.
A check that reports 40 lines every time gets ignored, and then it protects nothing.

Severity: a violation of checks 1, 2, 3 or 5 is **critical** — each of them is, on its own, enough to expose
data or credentials. The others block the commit but can be discussed.

---

## 1. Auth on every mutating route — `API-SEC-AUTH-001`

Every POST/PUT/PATCH/DELETE endpoint is authenticated, and every route group has an auth middleware.

```bash
# commented-out auth: this is exactly how three endpoint groups became public
grep -rnE '^\s*//\s*.*\.use\(\s*\w*[Aa]uth\w*' src/routes src/app
# wildcard auth inside a sub-app (see the flattening gotcha below)
grep -rnE '\.use\("\*",\s*\w*[Aa]uth' src/routes
```

- **A commented-out auth line is a critical bug**, never a temporary state.
- **Internal/debug endpoints are deleted, not gated.**
- **Authentication is not authorization.** A middleware that resolves "any valid user token" lets a customer
  through on a back-office endpoint. Staff-only routes need a **positive role check** after it.
- Prefer a **positive role allow-list** (`["SALES_ASSOCIATE","admin"]`) over a negative predicate ("has no
  customer row"): the negative form both under-blocks generic internal accounts and over-blocks hybrid users
  who are staff *and* customers.
- **Hono flattening gotcha:** when several sub-apps mount on the same prefix, `route.use("*", authMw)`
  **inside** a sub-app leaks to its siblings. Apply auth on the **exact path** where the app is composed.
  The grep flags every `use("*", …auth…)`, so before calling it a violation check the two things that make it
  one: **is the prefix shared** with other sub-apps, and **is it a gate**? A wildcard `optionalAuthMiddleware`
  on a sub-app with its own prefix is neither — it populates the context, it does not block.


**Audit every equivalent mutating route, not only the newest one.** When a second import, upload or
provisioning path exists for the same resource, the controls added to the one built last are routinely
absent from the one built first — and the old path is still wired. List the routes that mutate a given
resource and compare their middleware stacks side by side, rather than reviewing the one in the diff.

**A permissive cross-origin default on a control plane is an opening.** An administrative API that answers
with a wildcard origin while authenticating with cookies or credentials has given every site the ability to
act for a logged-in operator. Default to same-origin, allow exact configured origins, vary the cache by
origin, and reject a disallowed cross-origin state-changing request **before** the route handler runs.

## 2. Ownership from the authenticated id — `API-SEC-IDOR-001`

```bash
grep -rnE 'valid\("(query|json|param)"\)' src/controllers | grep -iE 'user|customer|client|order|receipt|return|device|lock|lease'
```

The owner id comes **only** from the authenticated context. Never trust an id from query/body/param for
ownership — scope the SQL to the authenticated id.

- A nested sub-resource with no owner column needs an **explicit ownership join**; "the parent was checked"
  is not a guarantee.
- An identifier is not a credential: a `device_id` or a `lease_token` proves nothing on its own. Bind the
  lease to `(token, expiry, resource, owner)` and verify it against the authenticated identity.
- On mutations: `SELECT … FOR UPDATE`, verify ownership **inside** the transaction, check `affectedRows`, and
  make a mismatch an **idempotent no-op / 404** — a distinguishable error turns the endpoint into an
  existence oracle.

## 3. No secrets or PII in responses — `API-SEC-SECRET-001`

```bash
grep -rnE 'FROM settings' src/query
grep -rniE 'select .*(password|secret|token|api_?key|private_key)' src/query
grep -rnE 'SELECT \*' src/query
```

**Why this rule is first:** a credential in a settings table is one public endpoint away from being handed
out. Settings are read by many callers and are the kind of table nobody re-reviews, so a key that lands
there is served to whoever asks — and a leaked deploy credential means someone else can ship your code.

- Secrets do not live in a settings table. Until they move to a key store, the runtime filter is the only
  barrier — and no endpoint may bypass it.
- **Allow-list the response fields.** Never return whole rows; mask credential columns to `null`. The
  `SELECT *` grep also hits derived tables (`SELECT * FROM ( … ) x`), which never reach the client: what the
  rule is about is the **projection returned to the caller**, not every star in the file.
- A **permissive allow-list is a trap**: combine an exact deny-list *with* name and value detectors. Do not
  "allow everything not explicitly secret".
- Strip identity fields from public projections and honour "hidden" flags **fail-closed**.

If the project has a secret classifier, three ordering rules are load-bearing (each one is a bug that already
happened — the details are in `references/rules.md`):

1. **The inclusion allow-list runs before the value scan**, otherwise a legitimate key that merely *looks*
   like a secret gets filtered and the safety belt becomes the outage.
2. **A name exemption is anchored to its own dot-segment**, otherwise an innocuous word anywhere in the key
   disarms the match everywhere — fail-open, and silent.
3. **Exclusions match exactly**, never as substrings.

Filtering is **never silent**: log every removal once per key with the deciding rule.

## 4. Logs and telemetry without secrets or PII — `API-SEC-LOG-001`

```bash
# 1. a secret named in the log call
grep -rniE 'logger\.(info|debug|warn|error)\(.*(token|cookie|authorization|password|session|email|JSON\.stringify\((headers|req|request|body|row))' src
# 2. an OBJECT handed to the logger — the case the first grep cannot see
grep -rnE 'logger\.(error|warn|info|debug)\([^)]*,\s*(err|error|e)\)' src \
  | grep -viE 'sanitize|redact|safeError|\.message'
grep -rnE 'console\.(log|error|warn|info|debug)\(' src --include=*.ts | grep -v '\.test\.ts'
```

Never log `Authorization`/Bearer, cookies, API secrets, tokens, passwords, auth bodies, or national id /
VAT / email. Log non-sensitive markers instead (`has_session_cookie=true`). No `console.*` in runtime paths.

> The invariants behind this check — and the fact that the redaction goes in a **different place** depending
> on the stack — are in **`padosoft-logging-discipline`**. Read it when the finding is about what ends up in
> a log line; what follows here is the API-specific part.

⚠️ **The second grep is the one that matters, and it is noisy on purpose.** Grep 1 reads the *message*; the
leak is usually in the *object*. Narrow it to the dangerous context — a `catch` around a database call:

```bash
for f in $(grep -rlE 'logger\.(error|warn)\([^)]*,\s*(err|error|e)\)' src); do
  grep -qE 'client\.execute|getConnection' "$f" && echo "$f"
done
```

**A driver error object carries the query already formatted, with the bound values substituted.** In mysql2
that is `err.sql`. So `logger.error("db lookup failed:", err)` on a query bound with `:tokenHash` writes the
token hash into the log — an equivalent of the token for anyone reading, enough to find the row in the token
table. And the branch that logs is the **failure** branch: exactly the one people open when something breaks,
copy into a ticket and paste into a chat.

Do not redact the whole thing — that makes the logs useless precisely when they are needed. Keep what
diagnoses (`code`, `errno`, `message` truncated) and drop `sql`, `sqlMessage` and the stack:

```ts
export function safeDbErrorDetails(err: unknown) {
    if (typeof err !== "object" || err === null) return { code: "UNKNOWN" };
    const e = err as { code?: string; errno?: number; message?: string };
    return { code: e.code, errno: e.errno, message: e.message?.slice(0, 200) };
}
```

*This is a real finding: the line existed, the previous commit had left it untouched, and its comment
declared it already safe.*

Telemetry: never export a **raw** query string, a client IP read straight from a header, or a raw exception.
Sanitize the query (redact credential-like keys, email-shaped values, blobs), truncate the user agent, and
replace exceptions with a neutral error **after** the handler has built the response, so the real status and
payload survive.

## 5. Environment gates must be fail-SAFE — `API-SEC-ENV-001`

```bash
# the PARSED value only: a raw process.env read is the correct form, do not flag it
grep -rnE '(^|[^.[:alnum:]_])env\.NODE_ENV\s*(===|!==)' src | grep -v 'process\.env'
```

If the env schema defaults `NODE_ENV` to `"development"`, a production deploy that simply **omits** it makes
every `env.NODE_ENV !== "production"` gate **fail-open** — debug output and mock auth in production.

```ts
// WRONG — fail-open when NODE_ENV is unset in prod
if (env.NODE_ENV !== "production") returnDebugInfo();
// RIGHT — fail-closed, from raw process.env; unknown counts as production
export const isNonProdRuntime = new Set(["development", "test"]).has(process.env.NODE_ENV ?? "");
if (isNonProdRuntime) returnDebugInfo();
```

Mock auth must **abort startup** unless the raw `NODE_ENV` is exactly `development`/`test`.

## 6. Bound SQL — `API-SEC-SQL-001`

```bash
# exclude the sanctioned forms, or the signal drowns: on a clean codebase the raw
# grep returned 89 hits, of which ~45 were generated placeholders and offsets
grep -rnE "(WHERE|SELECT|LIKE|VALUES|SET|ORDER BY)[^\n]*\$\{" src/query \
  | grep -viE '\$\{([a-zA-Z_]*[Pp]laceholders|ph|offset|safeOffset|limit)\}'
grep -rnE "'\\\$\{" src/query          # a literal '${x}' is injection too
grep -rn 'client.query(' src           # use the parameterized execute
```

Always named bound params. **A SELECT literal is injection as well**: `'${lang}' as lang` is a hole.

Narrow exceptions: `LIMIT`/`OFFSET` only if they are schema-coerced numbers; column name and sort direction
only through an allow-list plus a ternary; `IN (…)` through a placeholder builder — and **merge** the params
it returns.

**What a compliant hit looks like** — recognise it and move on, instead of re-investigating it on every
commit:

```ts
const sortCol  = SORT_COLUMN_WHITELIST[f.sort] ?? "bc.updated_at";   // ✅ allow-list + fallback
const orderDir = f.order === "asc" ? "ASC" : "DESC";                 // ✅ ternary, two outcomes
const op       = getDbOperatorByQueryStringOp(input.operator);       // ✅ mapper, not the raw string
sql += ` ORDER BY ${sortCol} ${orderDir} LIMIT ${f.perPage} OFFSET ${offset}`;
```

The three questions for a remaining hit: does the value come from the request? If yes, does it pass through
an allow-list or a ternary? If it is a number, is it coerced by the schema? Three yeses, it is fine.

⚠️ `LIMIT`/`OFFSET` are often interpolated **deliberately**: mysql2 does not bind them as named placeholders.
Do not "fix" one back into `:limit` — the query breaks. Check the coercion instead.

Adjacent correctness trap, same file: in a translation join, put the language filter **inside that join's own
`ON`**. On a second `LEFT JOIN` it cannot reduce rows — it only nulls the non-matching ones, so the query
returns N rows per source row. That inflates paginated responses *and* makes `rows[0]` without `ORDER BY`
return the translated row only sometimes: the bug filed as "sometimes it doesn't translate" that nobody
closes. With a single language both forms look identical, which is why it survives.

## 7. Structural resource caps — `API-SEC-LIMITS-001`

```bash
grep -rnE 'fetch\(' src | grep -viE 'signal|timeout|AbortSignal'
```

Every attacker-controlled collection, body, cursor, cache and outbound fetch needs an explicit cap **before**
the business logic runs. Reference values that worked: 16 MiB body, 100 items per batch (dedup first), 64 KiB
cursor with a mandatory expiry, 8 MiB response, 10s end-to-end fetch deadline held until the body is
consumed, bounded LRU + TTL for in-memory caches, recursion depth capped, stable `ORDER BY` with a max
`LIMIT` on paginated reads.

Per-identity rate limiting, if present:

- **Mount it after the route's auth**, so the bucket is the authenticated identity and not a shared NAT IP.
- Put the numbers in a **policy table**, not inline at the mount site: the policy name is part of the key, so
  a duplicate name silently merges two quotas.
- The PII-enumeration endpoint (a customer search) stays the strictest policy.
- A limiter that **fails open** when its store is down is a deliberate choice, not a bug: rate limiting is an
  availability control and authorization is upstream. Do not "fix" it to fail closed without a decision.
- Never log the identity value — log its *kind*. An IP is personal data.


**A process-local counter protects one process.** With more than one replica, the window has to be decided
by shared storage — serialised inside a transaction, or on a store that can make the decision atomically.
The in-process fallback is fine for development, and it does not support a claim about production. Key the
limit on the tenant or the credential, never on a client-supplied address header.

## 8. Injection into downstream consumers — `API-SEC-OUTPUT-001`

```bash
grep -rniE 'javascript:|vbscript:|data:' src/services src/repositories
grep -rnE '\.csv|text/csv|writeCsv|toCsv|join\(","\)' src
```

A stored URL that will later be rendered or redirected to: reject `javascript:`, `data:`, `vbscript:`,
`file:`, protocol-relative `//host`, embedded credentials and CRLF — **on write and on read**. Rows already
in the database were written before the validation existed.

CSV: a cell starting with `=`, `+`, `-` or `@` (also after whitespace or a BOM) is executed as a formula by
spreadsheet apps. Use an RFC 4180 encoder that neutralizes formulas; never hand-concatenate CSV.

## 9. No trust from caller input — `API-SEC-TRUST-001`

```bash
grep -rniE 'header\(\s*["'"'"']?(x-session-token|is_logged_in|cf-connecting-ip|x-forwarded-for|x-real-ip|x-client-ip)' src
grep -rniE 'etag|if-none-match|304' src/middlewares
```

- Privileged claims (audience, embargo, "is logged in") are **signed**, not query params: HMAC-SHA256 over
  timestamp + method + exact URL, short anti-replay window, timing-safe compare, fail-closed with no secret.
- An explicit `Authorization` header takes **absolute precedence** and never downgrades to an ambient session
  cookie.
- **The client address is a two-hop model.** At the edge, the trustworthy header is the one the platform
  sets itself. At the origin, that same header now carries the **edge's** address, so the origin reads what
  the edge forwarded instead — and that value is only trustworthy while the origin refuses traffic that did
  not come through the edge. See **`padosoft-edge-worker-security`**.
- Read the client IP through **one helper**, from the single header your edge actually sets, and validate the
  charset. Behind a proxy that forwards, the hop-by-hop headers are the *proxy's* address. Even the right
  header is spoofable unless the origin only accepts traffic from that edge (mTLS or IP allow-list) — so
  per-IP limits are an obstacle, not a barrier.
- **An allowlist on the initial URL does not survive a redirect.** Disable automatic following, validate
  the destination against the same explicit allowlist, reject credential-bearing URLs, and surface the
  blocked response as evidence instead of silently following it.
- **Redirect safety is not name-resolution safety.** Re-checking the allowlist at send time and disabling
  redirects is necessary and is not protection against a destination that resolves inward; that belongs in
  a connection-aware egress layer, and claiming it from a portable client wrapper is claiming something you
  do not have.
- **When the caller is a browser you drive, constrain the whole context, not the navigation.** Validating
  the URL handed to a navigation call says nothing about redirects, subresources or form-triggered
  requests: install the network policy on the context before the page exists, and abort anything that is
  not allowlisted.
- Cache: default `private`/`no-store`; any `Authorization`/`Cookie` forces it. Evaluate `If-None-Match`
  **after** auth, never before — and derive the ETag from the body only once the handler has run.

## 10. Supply chain and build — `API-SEC-SUPPLY-001`

- Pin images and CI actions to a **digest/SHA**, never a floating tag.
- Build secrets through secret mounts; never write a token into a layer or a committed `.env`.
- Frozen, lockfile-exact production install.
- Distroless base, non-root, read-only runtime artifacts, deploy by immutable digest.
- Transport policy **fail-closed in production**: plaintext or unverified DB/cache/SMTP is rejected, not
  warned about.
- Do not add or widen a static-secret export in CI, and do not add a production deploy path with no approval
  gate.

---

## Gotchas

- **Grepping for the secret's name finds the wrong half of the problem.** The two real leaking lines were
  caught because their message happened to contain the word "token"; the same call with the message "db
  lookup failed" is invisible to that grep and just as dangerous. Check **what is handed to the logger**, not
  what the sentence says.
- **"It's behind the gateway" is not auth.** Every audit finding above was in a service someone believed was
  private.
- **A green test suite proves nothing here** if the tests are not mounted in CI. Check that the security
  tests actually run before trusting them.
- **Documentation that teaches the broken pattern reopens the defect.** When you fix instances of a pattern,
  fix the example in the project docs in the same PR, or the next query will reintroduce it.
- **Fix the form, not the instance.** Scan for the *shape* of the bug across the codebase (every `*_languages`
  join, every `fetch(` without a signal) rather than the one case the report named.
- **An exception is one line with a written reason**, in the allow-list — never a widened regex.

## Final report

```
Security review: <n> files  ·  <n> critical  ·  <n> blocking  ·  <n> notes
API-SEC-AUTH-001   PASS | FAIL <file:line — what and the fix>
API-SEC-IDOR-001   …
API-SEC-SECRET-001 …
API-SEC-LOG-001 · API-SEC-ENV-001 · API-SEC-SQL-001 · API-SEC-LIMITS-001
API-SEC-OUTPUT-001 · API-SEC-TRUST-001 · API-SEC-SUPPLY-001
Not applicable to this diff: <rules>
Verdict: BLOCKED | OK TO COMMIT
```
