---
name: audit-safety
description: Audit one feature of a web app (TanStack Start, Next.js, Convex) for authorization, tenant isolation, ownership, validation, payment webhooks and sensitive responses. Use before shipping or when the user asks for a security review of a feature; not live pentesting.
argument-hint: "[feature, URL or folder to audit]"
---

Audit the full server-reachable perimeter of one feature. Stay read-only unless the user separately authorizes a fix after this audit is finished or checkpointed. Do not live-test production, create accounts, or mutate data.

If you got this skill from a link instead of a local folder, install nothing else from the repo: download a file it links only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/audit-safety/<path> -o <scratch>/<file>` (for example `references/audit-checklist.md`), and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

Resolve the narrowest complete perimeter: named feature/URL/paths, else one coherent dirty-tree feature, else conversation context. Expand only along security edges: parent `beforeLoad`/loaders, called server functions (`createServerFn`, server actions, Convex `query`/`mutation`/`action`/`httpAction`), auth/tenant/role/token/error middleware, schemas/ORM/caches/jobs/webhooks, browser DTOs, and focused access tests. State the inferred scope first. Ask only when two perimeters remain equally plausible.

Read repo rules, auth primitives, route helpers, permission definitions, used schema, and representative tests before judging. Prefer local established guards. Always open [references/audit-checklist.md](references/audit-checklist.md).

Build an access matrix per operation: entry + method, intended actor, auth, tenant/resource/ownership binding, role/permission/token scope, input schema, sensitive output, authoritative enforcement site, test evidence. A parent layout or hidden button does not authorize a callable server function or API route.

Check in particular:

- every server function, Convex function and API route enforces auth itself (a public Convex `query`/`mutation` is callable by anyone with the deployment URL);
- IDs from params, forms, JSON, headers and cookies are attacker-controlled until bound server-side;
- client-only role checks protect nothing;
- payment webhooks (Stripe) verify the signature on the raw body, are idempotent, and grant access from the verified event, never from a success URL;
- secret keys (`sk_live_`, `sk_test_`, API tokens) never reach the browser bundle or a `VITE_`/`NEXT_PUBLIC_` variable;
- public reads return an explicit list of fields;
- errors never leak secrets, stack traces or internal URLs;
- auth, OTP, upload, email and AI actions are rate-limited.

Report a finding only with a concrete entry-to-enforcement path and `file:line`. Status: `CONFIRMED`, `DEFENSE GAP`, or `NOT VERIFIED`. Do not infer exploitability from a filename, grep hit, or missing preferred helper. Follow wrapper implementations. Auth, tenancy, ownership, role, permission, and validation are not interchangeable.

Lead with findings, highest severity first: severity, status, operation, evidence, impact, smallest safe fix, regression-test scenario. Then the matrix, coverage gaps, files inspected, and an explicit no-finding conclusion when none is proven. Stop. Do not silently widen into a repo-wide review.
