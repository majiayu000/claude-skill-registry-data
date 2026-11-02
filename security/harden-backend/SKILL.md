---
name: harden-backend
description: Use when a backend service is about to take untrusted traffic or fails a security review. Adds edge validation, rate and size/time limits, a CORS allow-list, API security headers, SSRF-safe outbound fetch, safe error responses and CI scanning (Hono, Go, FastAPI).
---

# Harden Backend

Nine controls that decide whether untrusted traffic breaks the service. Rules and rationale: [harden-patterns.md](harden-patterns.md). Code per track: [harden-tracks.md](harden-tracks.md). Baseline: [security-baseline.md](../../core/_shared/security-baseline.md) rules 4, 6, 7, 8 and 13. Seam paths: [service-layout.md](../_shared/service-layout.md). The per-caller rate limit keys on the Principal of [set-up-backend-auth](../set-up-backend-auth/SKILL.md); run that first. For a read-only review with severities and no changes, use [audit-security](../../core/audit-security/SKILL.md).

## 1. Audit (change nothing)

Read the profile first; detect only what it leaves open ([stack-profile.md](../../core/_shared/stack-profile.md)).

```bash
cat .claude/stack-profile.md ~/.claude/stack-profile.md 2>/dev/null   # backend.track, package_manager, ci
ls src/transport/edge.ts internal/transport/httpapi/edge.go src/*/transport/edge.py internal/platform/safehttp src/*/platform/outbound.py 2>/dev/null

# Wildcard CORS (Hono / FastAPI / Go)
grep -rn -e "origin: '\*'" -e 'allow_origins=\["\*"\]' -e 'AllowedOrigins: \[\]string{"\*"}' --include='*.ts' --include='*.py' --include='*.go' . 2>/dev/null

# String-built SQL: SQL keywords inside template literals, f-strings or Sprintf
grep -rnE '(SELECT |INSERT INTO|UPDATE |DELETE FROM)' --include='*.ts' --include='*.py' --include='*.go' src internal 2>/dev/null | grep -E '\$\{|f"|Sprintf'

# Outbound calls with a variable URL (SSRF surface)
grep -rnE 'fetch\(|httpx\.|http\.Get\(' --include='*.ts' --include='*.py' --include='*.go' src internal 2>/dev/null

# Raw errors handed to clients
grep -rnE 'err\.message|str\(exc\)|err\.Error\(\)' --include='*.ts' --include='*.py' --include='*.go' src internal 2>/dev/null

# Body limits, deadlines, server timeouts
grep -rn 'bodyLimit\|MaxBytesReader\|MAX_BODY_BYTES' --include='*.ts' --include='*.go' --include='*.py' src internal 2>/dev/null
grep -rn 'http.Server{' --include='*.go' . 2>/dev/null   # no ReadHeaderTimeout beside it = no timeouts

# CI scanning
ls .github/workflows 2>/dev/null && grep -rlE 'gitleaks|osv-scanner|audit' .github/workflows 2>/dev/null
```

Each `fetch`/`httpx`/`http.Get` hit needs one question answered: is the URL hardcoded, or does request data reach it? Fill the checklist; the "where" column names the files you saw, the OWASP IDs follow [harden-patterns.md](harden-patterns.md):

| Control | Present? | OWASP 2025 | Where |
|---|---|---|---|
| Edge schema validation, unknown fields rejected | | A05, A06 | |
| Parameterized SQL only | | A05 | |
| Per-caller rate limit | | A06, A07 | |
| Body cap, request deadline, server timeouts | | A06, A10 | |
| CORS exact allow-list | | A02 | |
| API security headers | | A02 | |
| SSRF-safe outbound fetch | | A01 | |
| problem+json errors, generic 500 | | A10, A09 | |
| CI: secret and dependency scanning | | A03, A08 | |

## 2. Decide

- Controls missing: apply the delta for each, steps 4 to 6. Do not rewrite what works.
- A control present but weak (wildcard CORS, `err.message` to clients, string-built SQL, a server without timeouts): fix it in place with the matching rule from [harden-patterns.md](harden-patterns.md).
- Every row present and step 7 passes: report "already in place" and stop.

## 3. Detect track

| `backend.track` | Do |
|---|---|
| `hono`, `go`, `fastapi` | Continue; the code is in [harden-tracks.md](harden-tracks.md). |
| `nextjs` | Stop. Use [build-nextjs-backend](../build-nextjs-backend/SKILL.md). |
| `supabase` | Stop. Use [secure-supabase-rls](../secure-supabase-rls/SKILL.md) and [set-up-supabase](../set-up-supabase/SKILL.md). |
| `none` or unset | Run `set-up-stack-profile`, then a `scaffold-*-service` skill. |

One more question, answered from the audit grep: does the service call **user-influenced URLs** (webhooks, link previews, imports)? If it does not, skip the SSRF module and say so in the report: install it only when such a call first appears. Everything else applies regardless of the answer.

## 4. Install only what is missing

```bash
pnpm add hono-rate-limiter undici             # hono: limiter middleware; fetch with a connect-time guard (zod is already there)
go get github.com/rs/cors golang.org/x/time   # go: CORS allow-list; token-bucket rate limiter
uv add slowapi httpx                          # fastapi: per-route limiter; the client the SSRF module uses
```

Use the profile's package manager. Verify each line in [stack-versions.md](../_shared/stack-versions.md) before you write it.

## 5. Generate the seams

Create from [harden-tracks.md](harden-tracks.md), skipping files that exist:

```
transport/edge                  CORS allow-list (outermost), secure headers, body cap, request deadline, limiter factory
transport decode (Go only)      JSON with unknown fields and trailing data rejected
platform outbound seam          the only way out to a URL the service did not hardcode
tests/unit                      SSRF refusals, rate limit, decode
.github/workflows/security.yml  secrets + dependency scanning, SHA-pinned actions
```

Paths follow [service-layout.md](../_shared/service-layout.md).

## 6. Wire

1. **Edge defaults on the app.** Order matters: CORS outermost, so a preflight is answered before any body limit or deadline runs.
2. **Body parsing through strict schemas.** Unknown fields rejected, every string, array and number bounded.
3. **Per-caller rate limit after authentication.** The key is the principal, not the IP; tighter on login and token endpoints.
4. **Deadline on the request context; server timeouts in main.** `net/http` has none by default.
5. **Error mapper.** problem+json; the unknown error becomes a generic 500; its detail goes to the logger once; 405 keeps `Allow`; 404 for another tenant's rows.
6. **SQL review.** Every hit from the audit grep moves to a parameterized form; dynamic identifiers come from an allow-list map.
7. **Outbound calls.** A URL that is not hardcoded goes through the SSRF seam only.
8. **CI.** Commit `.github/workflows/security.yml`; keep the native audit of your track, delete the other two.

## 7. Verify

```bash
pnpm typecheck && pnpm vitest run   # hono
go vet ./... && go test ./...          # go
uv run mypy && uv run pytest           # fastapi
```

Expected: all green. Then manual checks against a running service, each with its expected result:

- a body over the cap: 413;
- a request with an unknown `Origin`: no `access-control-allow-origin` in the response;
- `curl -si <URL>/healthz`: response headers include `content-security-policy`, `strict-transport-security`, `x-content-type-options`;
- one request over the limit: 429 with `Retry-After`;
- the scanners, locally, with the docker commands from the workflow.

Then fuzz the contract with schemathesis (install: `uvx schemathesis` or `pipx install schemathesis`):

```bash
schemathesis run http://localhost:8299/openapi.json --checks all -n 25 --exclude-path '/documents/{doc_id}'
```

Expected on the FastAPI scaffold: `55 generated, 55 passed`. The excluded path needs a token the fuzzer has no credentials for. On the unmodified scaffold the first run FAILED with `TRACE returned 405 without required Allow header`: the scaffold's `StarletteHTTPException` handler dropped the exception's headers. The fix (`headers=dict(exc.headers) if exc.headers else None`) is in the Python track. That finding is why the fuzzer is part of hardening: it breaks the HTTP contract in ways the test suite does not.

## References

- [harden-patterns.md](harden-patterns.md): the nine controls, each justified and mapped to OWASP Top 10:2025.
- [harden-tracks.md](harden-tracks.md): edge, decode, SSRF and CI code for Hono, Go and FastAPI, plus the wiring deltas.
- [set-up-backend-auth](../set-up-backend-auth/SKILL.md): authentication; the rate limit and the 404 rule build on it.
- [security-baseline.md](../../core/_shared/security-baseline.md): the cross-stack floor this skill implements for services.
- [audit-security](../../core/audit-security/SKILL.md): the read-only review to run when nothing should change yet.
