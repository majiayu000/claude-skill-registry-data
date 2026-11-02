---
name: design-http-api
description: Use when adding or changing HTTP endpoints, or when the frontend needs typed calls — sets the OpenAPI 3.1 contract, RFC 9457 errors, cursor pagination, idempotency keys, versioning, and a generated typed client behind the frontend fetcher seam.
---

# Design HTTP API

Rules and rationale: [api-contract-patterns.md](api-contract-patterns.md). Per-track generation, client wiring, code: [api-codegen-patterns.md](api-codegen-patterns.md). Layer paths: [service-layout.md](../_shared/service-layout.md). Versions: [stack-versions.md](../_shared/stack-versions.md).

The contract is a committed OpenAPI 3.1 file. Code and client both derive from it, so they cannot drift.

## 1. Audit (change nothing)

```bash
cat .claude/stack-profile.md ~/.claude/stack-profile.md 2>/dev/null   # backend.track, frontend.framework, package_manager
ls openapi.json openapi.yaml oapi-codegen.yaml src/api/schema.d.ts src/libs/api-client.ts 2>/dev/null
grep -rn "application/problem+json" src internal 2>/dev/null | head -3        # error format in place?
grep -rnE "cursor|next_cursor|nextCursor|offset=|page=" src internal 2>/dev/null | head   # pagination style
grep -rniE "idempotency-key|If-Match|ETag" src internal 2>/dev/null | head
grep -rnE "app\.(get|post|put|patch|delete)\(|\.openapi\(|@router\.|HandleFunc" src internal 2>/dev/null | wc -l
```

Record: where the spec comes from (code or file), which errors are problem+json, which list endpoints use offset, which unsafe endpoints lack idempotency. Never ask what the profile or repo answers.

## 2. Decide

- No committed spec and no generator: full setup (steps 3 to 7).
- Spec exists: apply only the missing rules (step 5 list) and the missing client wiring.
- `backend.track` is `nextjs`: use `build-nextjs-backend` for route handlers; this skill still applies to the contract rules. `supabase`: PostgREST is the API; use `set-up-supabase`. Stop here for those unless the repo also ships its own HTTP service.
- Spec committed, `git diff --exit-code openapi.json` clean after regeneration, client builds: report "already in place".

## 3. Detect track

| `backend.track` | Source of truth | Why |
|---|---|---|
| `hono` | Zod route schemas via `@hono/zod-openapi`, emitted as `openapi.json` | One schema validates, types and documents. No second file to keep in sync |
| `fastapi` | Pydantic models and route signatures, emitted by `app.openapi()` | Same reason; FastAPI already emits 3.1 |
| `go` | `openapi.yaml` written first, `oapi-codegen` strict server | Go struct tags cannot carry enums, bounds or nullability; the spec is reviewed in the PR and the compiler forces every handler to match |

Frontend client: `frontend.framework` any; the client is plain TypeScript (`openapi-typescript` + `openapi-fetch`).

## 4. Install only what is missing

```bash
# TS server: already present from scaffold-hono-service (@hono/zod-openapi, zod)
# Go server
go get -tool github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@latest
go get github.com/oapi-codegen/nethttp-middleware@latest
# Frontend (or the repo that owns the client)
pnpm add openapi-fetch
pnpm add -D openapi-typescript
```

Check each line with `npm view <pkg> version` / `go list -m -versions`. `openapi-typescript` 7.13 declares a `typescript ^5` peer; with TypeScript 6 or 7 npm refuses to install, pnpm warns. The output is a `.d.ts` file and works; allow the peer in `pnpm.peerDependencyRules` and say so in the PR.

## 5. Apply the contract rules

Each rule is in [api-contract-patterns.md](api-contract-patterns.md); check the API against this list and fix the delta.

1. Errors: every 4xx/5xx is `application/problem+json` (RFC 9457), declared in the spec with the `Problem` schema. Validation failures are 400 with an `errors[]` extension. Use the scaffold's seam (`src/platform/problem.ts`, `internal/transport/httpapi/problem.go`, `platform/problem.py`).
2. Lists: cursor pagination, `limit` capped, `{ items, nextCursor }`. No `offset`.
3. Unsafe retries: `POST` that creates or charges accepts `Idempotency-Key`; same key and body replays the stored response.
4. Names: plural kebab-case paths, `camelCase` JSON, `operationId` on every operation (it becomes the client method name), ISO 8601 UTC timestamps, string IDs.
5. Versioning: additive changes only, no `/v2` until a breaking change cannot be avoided. CI runs `oasdiff breaking` against the base branch.
6. Concurrency: `ETag` + `If-Match` on resources that users edit concurrently; `If-None-Match` on large cacheable reads.

## 6. Generate and wire

1. Emit the spec and commit it (commands per track in [api-codegen-patterns.md](api-codegen-patterns.md)).
2. Client types: `pnpm exec openapi-typescript openapi.json -o src/api/schema.d.ts`. Commit the output.
3. Client seam: `src/libs/api-client.ts` builds `createClient<paths>` on the frontend `fetcher` seam, so cookies, CSRF and 401 refresh are not redone. The seam needs one small export; see the section "Wire into the fetcher seam" in [api-codegen-patterns.md](api-codegen-patterns.md) and [fetcher.md](../../frontend/_shared/fetcher.md).
4. Scripts: `api:spec` (emit), `api:types` (generate), `api:check` (regenerate and `git diff --exit-code`).
5. CI: run `api:check` and `oasdiff breaking origin/main:openapi.json openapi.json`.

Go: `//go:generate go tool oapi-codegen -config oapi-codegen.yaml ../../openapi.yaml` next to the generated package; `go generate ./...` and `git diff --exit-code` in CI.

## 7. Verify

In a Vite frontend `typecheck` is `tsc -b`; `tsc --noEmit` checks zero files there (see ../../frontend/_shared/conventions.md).

```bash
pnpm api:check                         # spec and types regenerate with no diff
pnpm typecheck                 # a call with a wrong param type fails to compile
curl -si 'localhost:3000/<list-path>?limit=0' | sed -n '1p;/content-type/Ip'
# expect: HTTP/1.1 400 ... content-type: application/problem+json
oasdiff breaking origin/main:openapi.json openapi.json    # expect: no output (exit 0)
```

Go: `go generate ./... && git diff --exit-code && go vet ./...`.
Idempotency: send the same `POST` with one key twice; the second response is identical and no second row exists.

## References
- [api-contract-patterns.md](api-contract-patterns.md): problem details, pagination, idempotency, versioning, conditional requests, naming.
- [api-codegen-patterns.md](api-codegen-patterns.md): spec emission per track, typed client, fetcher wiring.
- [../../core/_shared/security-baseline.md](../../core/_shared/security-baseline.md): input validation and error disclosure.
