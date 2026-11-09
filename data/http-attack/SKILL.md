---
name: http-attack
description: Break-test an HTTP API the user runs locally before shipping it. Sends malformed bodies, hostile paths, raw parser errors, concurrent duplicate creates, never-ending bodies, LIKE/SQL injection in search, database faults, missing auth, IDOR and CSRF, and reports each failure with its severity and the correct response. Use when asked to attack, harden, fuzz or break-test a local API, or to check it never answers 500. Not for code review, load tests, full OpenAPI conformance, or hosts the user does not own.
---

# http-attack

Unit tests prove the handler does what the developer thought of. This skill sends what the developer did not think of,
against the real server, and reports each failure with its severity and the response that would have been correct.

## Scope and safety

- Only an app the user owns, running on this machine (`localhost`, `127.0.0.1`, `::1`). The script refuses other hosts.
- **Loopback is not proof the app is local.** `kubectl port-forward`, `ssh -L`, a cloud SQL proxy or a dev tunnel all answer on
  `127.0.0.1` while the data lives elsewhere. Confirm with the user that the app behind the port is a local process.
- The probes create about 20-40 rows per write route, delete rows, lock the database and send 50 MB bodies. **Use a
  throwaway database** (a scratch SQLite file, or a Postgres/MySQL database created for this run), never one with data
  that matters. If you cannot confirm it is throwaway, stop and ask.

## Method

1. **Discover the surface.** Read the router (or the OpenAPI file) and list every route as one of: *create* (POST that
   stores), *update/delete*, *read one* (`/items/{id}`), *list*, *search* (list with a free-text parameter). Note per route: the
   auth scheme (bearer, cookie, API key, custom header), the unique keys of the stored entity, the body limit, the
   database, the maximum header size, whether the route is public by design, and the headers every response must carry
   (request id, `Cache-Control`, security headers).
2. **Start the app** on a free port with the scratch database and get credentials for two users (see below).
3. **Run the script** (below) with one `--write` per create/update route, `--read` per list, `--search` per search route,
   `--unique` per create guarded by a unique key.
4. **Triage every row.** `FAIL` is a finding; `NOT RUN` is a probe that could not reach a verdict (the legitimate body was
   refused, no item route is known, no rows to search): fix the input and run again, it is never a pass. A finding that is
   correct behaviour for this app is not a bug: say so and suppress it in the config with the reason (next section), do not
   change the app to satisfy the probe.
5. **Fix** real findings at the right layer (`references/fixes.md` has the fix per finding and stack), not by special-casing
   the probe. Add a regression test per fixed finding to the app's own suite.
6. **Re-run the same command** until it reports **0 findings, or every remaining one is suppressed in the config with its
   reason**, and no row is `NOT RUN` (or each is suppressed with a reason). Exit code 0 means exactly that.
7. **Clean up**: the run left rows in the scratch database; drop the database (or the file), do not reuse it.

## Running it

If the project lists `http-attack` in its `devDependencies`, run `npx --no-install http-attack` instead of
`node "${CLAUDE_SKILL_DIR}/scripts/http-attack.mjs"` in every command below: it is the version CI runs. Without that
dependency, use the copy bundled with this skill, as written.

Git Bash / macOS / Linux:

```bash
MSYS_NO_PATHCONV=1 node "${CLAUDE_SKILL_DIR}/scripts/http-attack.mjs" http://127.0.0.1:3000 \
  --header "Authorization: Bearer $TOKEN_A" --other-header "Authorization: Bearer $TOKEN_B" \
  --write 'POST /items {"name":"Ana","email":"ana@example.com"}' \
  --read "/items?limit=10" --search "/items q" \
  --unique 'POST /items {"name":"Uno","email":"uno@example.com"}' \
  --item-path "/items/{id}" --common-headers "X-Request-Id, Cache-Control" --body-limit 65536 \
  --fault-sqlite ./data/app.db
```

Windows PowerShell (5.1 strips the quotes inside inline JSON, so put bodies in files):

```powershell
Set-Content -Encoding ascii body.json '{"name":"Ana","email":"ana@example.com"}'
node "${CLAUDE_SKILL_DIR}/scripts/http-attack.mjs" http://127.0.0.1:3000 `
  --header "Authorization: Bearer $env:TOKEN_A" --write "POST /items @body.json" --read "/items?limit=10"
```

An inline JSON body that does not parse exits 2 and shows what arrived. `node "${CLAUDE_SKILL_DIR}/scripts/http-attack.mjs" --help` lists every option.
Notes:

- Zero dependencies; Node 22.13 or newer.
- Every write body gets a per-run suffix on one string field (the first containing `@`, else the first string; `--vary /item/email`
  picks another, also nested) so a uniqueness rule never answers in place of the defense under test.
- `--content-type application/vnd.api+json` for non-default media types; `--auth-header-name X-Auth-Token` when credentials
  travel in a custom header; `--auth-env VAR` / `--other-auth-env VAR` keep tokens off the command line.
- Cookie authentication: add `--csrf` and pass the cookie with `--header "Cookie: ..."`.
- `--origin-check always` sends every write and read from a foreign Origin (another site, another port, no `Sec-Fetch`,
  `Origin: null`) with the given credentials, cookie or not; each must be refused. A 409, 422 or 400 there is `NOT RUN`: the
  body was judged, not the origin. `--no-ambient` declares that no credential a browser sends on its own reaches the API: the
  origin rows are replaced by one check (no legitimate response sets `Set-Cookie` or asks `WWW-Authenticate`).
- `--host-check` also sends every write and read with a foreign `Host` (after a read answered 2xx legitimately). Accepted, it is
  an `info` row; with `--strict-host` it is a finding. A 409 or 422 there is `NOT RUN`.
- `--leak-path /backup.sql` (repeatable) adds a file the app must not serve: a 2xx with a non-HTML body is `file-served`.
- A body that never ends is sent chunked and with a large `Content-Length`; with a declared body limit only a 413 passes.
  HEAD goes to write-only routes too (a 405 with `Allow` is fine, a 5xx is not). In the race a 3xx counts as a success.
- `--json` sends form bodies as JSON objects. Without it, a form write whose legitimate request answers 415 is sent as JSON
  from then on, and the `legit-write` row says so.
- `--openapi openapi.yaml` checks every status the app answered against the statuses the contract declares for that
  operation (the most specific template; `2XX` and `default` count). A path the contract lacks is not judged.
- Persistence is a two-step run around a restart: `--persist-save state.json`, restart the app, `--persist-verify state.json` (the file must be inside the working or temp
  directory, or the config must name its directory in `persistDir`).
- Other databases: `faultCmd` (`"docker pause db"`) and `faultRestore` (`"docker unpause db"`) in the config file: any shell
  command that breaks the database and the one that heals it (the restore always runs). They are read only from the config
  file, never from the command line, because they run a shell: have the user review them before the run.
- On Git Bash for Windows set `MSYS_NO_PATHCONV=1` so `/items` is not rewritten into a Windows path, and give the app and
  `--fault-sqlite` the same absolute Windows path (`D:/app/data/app.db`).

**Two users' tokens.** Use the app's own seed or signup: create two users (alice, bob) against the scratch database, log in
as each, and export the tokens (`TOKEN_A`, `TOKEN_B`) or the session cookies. If the app has no login, a test helper that
signs a token for two different user ids works. The ownership rows need both; without user B they are skipped.

## Config file

`http-attack.config.json` in the project (or `--config <path>`) holds what the command line cannot say. Per-route settings
go under `routes` (key `"/items"`, `"POST /items"` or a template such as `"/items/{id}"`); `bodyLimit`, `maxHeaderBytes`,
`invalidUtf8`, `vary` and `contentType` may also be given at the top level for every route. `public` and `idempotentCreate` relax
a check, so they are accepted only inside one route and only with a `reason`:

```json
{
  "bodyLimit": 65536,
  "commonHeaders": ["x-request-id", "cache-control"],
  "routes": {
    "/catalog": { "public": true, "reason": "public read-only catalogue" },
    "/imports": { "bodyLimit": 10485760, "invalidUtf8": "replace" },
    "POST /things": { "idempotentCreate": true, "reason": "ON CONFLICT DO NOTHING answers 200 with the same item" }
  },
  "ignore": [
    { "id": "parser-accepted:big-header:raw", "reason": "the load balancer in front caps headers at 1 MB" }
  ]
}
```

| Setting | Meaning |
|---|---|
| `public` + `reason` | reads and writes of this route without credentials are expected to succeed (the reason is mandatory) |
| `bodyLimit` | the documented limit in bytes: the never-ending body sends limit+1 bytes, the multibyte probe is built from it |
| `maxHeaderBytes` | the app's header limit: the oversized-header probe sends limit+1 KB |
| `invalidUtf8` | `reject` (default) or `replace` (the parser substitutes U+FFFD by design) |
| `idempotentCreate` + `reason` | several 2xx for one key are expected (`ON CONFLICT DO NOTHING`); the reason is mandatory |
| `vary`, `contentType` | as the flags |
| `ignore` | `{id, reason}`: `id` is a finding id (shown in every report row), a rule name (`stack-leak`), `<rule>:<probe>` (every target of that probe), or `<rule>:<prefix>*`. It must start with a known rule and a reason is mandatory. `not-run` is never accepted alone: name the probe (`not-run:<probe>`) so one gap cannot hide the others |

The config can also hold `faultCmd`, `faultRestore`, `persistDir`, and list `writes`, `reads`, `searches`, `uniques` (bodies as objects or `"@file"`) and `persistIgnore`
(fields skipped when comparing the persisted item).

## Reading the report

Each row is `pass`, `FAIL <severity>`, `NOT RUN`, `suppressed`, `skipped` (the config says it does not apply) or `info`
(seen, neither a pass nor a finding). Failures show
`expected:`, `evidence:` and an `id:` that is stable between runs. `--format json` prints `{schemaVersion: 1, summary, findings,
rows}`; the summary counts `run`, `passed`, `failed`, `suppressed`, `notRun`, `skipped`, `info` and findings by severity.
Exit codes: `0` no findings, `1` findings, `2` the run could not complete (bad argument, app down, crash, zero probes run, or
some probe not run).

## Severity

Every rule the script can emit; the finding id is `<rule>:<probe>:<target>`.

| Rule | Severity | Meaning |
|---|---|---|
| `process-died` | critical | the app stopped answering during a probe |
| `unauthenticated-access` | critical | a write or read is granted (2xx) without credentials |
| `idor` | critical | another user's credentials reach this user's object (2xx) |
| `sql-injection` | critical | an injected OR returns rows that a no-match control does not |
| `duplicates-stored` | critical | concurrent identical creates stored more than one distinct item |
| `file-served` | critical | a repo, secret or OS file came back over HTTP |
| `csrf` | critical | a cookie-authenticated write from a foreign Origin was accepted |
| `not-durable` | critical | a saved item is gone or different after a restart |
| `foreign-origin-accepted` | high | a request from a foreign Origin was accepted (`--origin-check always`) |
| `ambient-credentials` | high | with `--no-ambient`, a legitimate response sets Set-Cookie or asks WWW-Authenticate |
| `connection-dropped` | high | the connection was closed without a response while the app stayed up |
| `server-error` | high | a 5xx on client input (including path params, quotes and unique violations) |
| `accepted-invalid` | high | input that must be refused got a 2xx/3xx (bad JSON, invalid UTF-8, wrong type, other methods) |
| `no-body-limit` | high | a body over the limit is accepted, or a body that never ends is read forever |
| `double-slash-mismatch` | high | `//x` answers 2xx with something other than `/x` |
| `wildcard-unescaped` | high | `%` or `_` in a search reach LIKE as wildcards |
| `parser-accepted` | high | the HTTP parser let a malformed raw request through |
| `fault-not-reported` | high | a write during a database fault was not answered with a 5xx |
| `limit-counts-characters` | medium | the body limit counts characters, not bytes |
| `read-before-reject` | medium | a 50 MB body was read in full before the 415 |
| `media-type-strict` | medium | a case or parameter variant of the media type is refused (RFC 9110 8.3.1) |
| `stack-leak` | medium | a 5xx body leaks a stack trace, driver error or SQLSTATE |
| `parser-no-common-headers` | medium | a parser-level error lacks the app's common headers |
| `headers-missing` | medium | a response lacks a header every response must carry |
| `foreign-host-accepted` | medium | a request with a foreign Host was accepted (`--strict-host`; an info row without it) |
| `undocumented-status` | medium | with `--openapi`, the app answered a status the contract does not declare for that operation |
| `missing-allow` | low | 405 without an `Allow` header |
| `head-unsupported` | low | HEAD on a readable route answers 405 (RFC 9110 9.1) |
| `not-run` | - | a probe could not reach a verdict; never a pass |

A 5xx whose body leaks internals is reported twice on purpose: `server-error` (the app failed on client input) and `stack-leak`
(what the body disclosed) have different fixes and different owners, so each keeps its own id and can be suppressed on its own.

## What the script probes

| Group | Probes | Correct response |
|---|---|---|
| input | truncated JSON, invalid UTF-8 inside a string, no `Content-Type`, `Application/JSON; charset=utf-8`, a string field sent as number/null/array/object, 1 MB body, limit+1 bytes of multibyte characters, PUT/DELETE/PATCH on the route | 4xx, never 5xx, nothing coerced or stored |
| paths | `//x` vs `/x`, `/%`, `?x=%FF%`, 30-digit numbers in query and path parameters (`/items/999...`, `/items/abc`, invalid UUID), HEAD/OPTIONS, `/.git/config`, `/.env`, `../../etc/passwd`, win.ini | 4xx or the same resource, never 5xx; files 404 |
| search | `%`, `_`, quotes, `\`, `' OR 1=1 --`, compared as parsed rows against a search that matches nothing | only rows containing the literal text |
| parser (raw socket) | `GARBAGE` request line, non-ASCII bytes in the path, an oversized header, `Content-Length` with `Transfer-Encoding` | 400/431 with the common headers, connection closed |
| resources | 50 MB `text/plain` to a JSON route, a chunked body that never ends (sends limit+1 bytes) | 415 at the first bytes; 413 at the limit or 408/close |
| concurrency | N identical creates released together (last-byte sync) | exactly one 201, the rest 409 |
| faults | a legitimate write while the database is locked or broken (`--fault-sqlite`, or `faultCmd` in the config) | 503/500 with a generic body, the process keeps answering |
| auth | each write and read without credentials; user B reads and deletes A's item (after checking B can use its own) | 401 (or a redirect to login); 404/403 for B |
| csrf | write with a foreign `Origin`, another port of the same host, `Origin: null` | 4xx |
| origin | `--origin-check always`: foreign Origin, another port, no `Sec-Fetch`, `Origin: null` with the given credentials; `--no-ambient`: no `Set-Cookie` or `WWW-Authenticate` | 4xx; no ambient credential |
| host | each write and read with `Host: attacker.example` | 4xx (421) |
| contract | `--openapi`: every status answered, per operation | a declared status |
| durability | create, restart, read back | same status and body |

Also check by hand what the script cannot: mass assignment (`"role":"admin"` on create/update), excessive data exposure, function-level
authorization (a regular user calling admin routes), rate limits on login, business-logic abuse (double-spend of a one-time token,
two updates with the same version, a counter below zero). Map findings to OWASP API Security Top 10 (API1, API2, API4, API5) and ASVS
level 1 for the security floor of a whole application.

## What this skill does not do

- Schema conformance against an OpenAPI file (only statuses are checked) and property-based input generation: Schemathesis.
- Stateful sequence fuzzing over a whole API: RESTler.
- Known-CVE and misconfiguration scanning of the stack: OWASP ZAP API scan or Nuclei templates.
- Content discovery of unlinked routes: ffuf with a wordlist.
- Load and latency limits: a load tool.
