---
name: convex
description: Set up, secure and optimize a Convex backend. Use for Convex project setup, schema and indexes, queries and mutations, auth checks in Convex functions, env vars, dev vs prod deploys, and reducing bandwidth, Documents Read, .filter/.collect scans or OCC conflicts from live insights.
---

Set up a project with two deployments, dev (break anything) and prod (real users), and never point local dev at prod data:

```bash
npx convex login                 # the user approves in the browser, or run the setup-convex skill
npx convex dev --once            # creates the project + dev deployment, writes .env.local
npx convex env set KEY value     # server secrets (dev); add --prod for production
npx convex deploy                # production deploy
```

Write every function so it is safe and cheap:

- Every public `query`, `mutation` and `action` is callable by anyone who has the deployment URL. Check the user (`ctx.auth` or the Better Auth helper) and ownership inside each one; use `internalQuery`/`internalMutation` for anything only the server calls.
- Validate every argument with `v.*` validators.
- Read with `.withIndex(...)` on a selective index, never `.filter` on a large table. Define the index in `schema.ts` for each access pattern (`by_userId`, `by_courseId_order`, ...).
- Bound reads: `.take(n)` or `.paginate()` before enriching rows; never `.collect()` a table that grows.
- Return only the fields the client needs.
- Secrets live in Convex env vars, never in client code.

To optimize, start from live evidence:

```bash
npx convex insights --prod --details
```

Extract function name, warning type, per-table docs/bytes, and whether it failed or only neared a limit. Prioritize high Documents Read with low Documents Returned.

Map each hot export to `convex/**` and its client callsites, then diagnose before patching:

- `.filter` / `.collect` without a selective `.withIndex`, or an index that narrows only by tenant and still scans thousands of rows;
- per-row related fetches (N+1); recount helpers on hot mutations;
- jobs or crons that scan every row on every run;
- concurrent patches on the same document (OCC conflicts).

Apply the smallest change: add the index used by the query; `.take`/`paginate` before enrichment; denormalize list previews and fetch full rows only on detail; incremental counters instead of full recounts; cursor + per-run limit for jobs; skip no-op patches and merge same-document writes; move high-churn state to a narrower table.

Verify with the project's typecheck, tests and build, plus `npx convex codegen`. Re-run insights after deploy and report: hot functions, root cause, change, expected read/byte/OCC impact, validation.
