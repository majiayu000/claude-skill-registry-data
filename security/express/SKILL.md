---
name: express
description: "Express engineering the Node way: middleware chains, async errors, validation, security headers, graceful shutdown. Use for Express services; never FastAPI patterns in disguise."
---

# express

Express is unopinionated middleware: you own the structure, the error paths, and the security headers.

## Activate when

- Building or changing Express apps: routing, middleware, validation, auth, testing, deployment.

## Do NOT activate for

- Next.js/React rendering (see nextjs, react); FastAPI services (see fastapi).

## Procedure

1. Version: detect Express major + Node release from package.json/engines; research in https://expressjs.com/ for that major — Express 4 vs 5 async-error behavior differs, so never assume. Check https://github.com/expressjs/express releases for the pinned line.
2. Structure: routers per resource, thin handlers, service layer for logic; middleware ordered deliberately (security → parsing → auth → routes → 404 → error).
3. Async: every async handler wrapped (or Express 5 semantics confirmed) so rejections reach the error middleware; centralized error middleware producing one envelope; 404 before errors, errors last.
4. Validation: schema-validate params/query/body at the boundary (Zod or equivalent, pinned); reject unknown fields on security-sensitive routes.
5. Auth: sessions vs JWT chosen per threat model; authorization checks on every route; CORS allowlisted, CSRF tokens for cookie auth, `helmet` security headers, rate limiting on auth + expensive routes.
6. Lifecycle: graceful shutdown (stop accepting, drain, close pools); structured request logging with ids; health endpoint with real dependency checks.
7. Testing: supertest/app-level tests for routes (happy, validation, authz-cross-user), unit tests for services; see testing pyramid in `../../core/testing/`.
8. Deploy: `NODE_ENV=production`, pinned Node, no devDeps in image, secret-free logs.
9. Verify: error paths exercised (every throw mapped to a status), shutdown drill, header audit, authz matrix green.

## Failure modes

- Unhandled async rejections crashing the process; error middleware in the wrong position; CORS `*` with credentials; trusting `req.ip` behind proxies without `trust proxy` review.

## References
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (nodejs, npm, pnpm, bun, zod).
